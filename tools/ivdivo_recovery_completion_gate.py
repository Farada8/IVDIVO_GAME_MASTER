#!/usr/bin/env python3
"""Fail-closed semantic completion gate for IVDIVO reconciled transcript recovery.

This tool validates *recovery completion semantics* only. It does not decide
canon, search Drive/GitHub, verify provider/human evidence, or choose creative
branches. It consumes a Reconciled Recovery State v2 artifact produced after
semantic reconciliation and returns whether the recovery layer is complete
and eligible to hand off to the normal next-action resolver.

Authority:
- IVDIVO_NARRATIVE_OS/18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md
- schemas/IVDIVO_RECONCILED_RECOVERY_STATE_SCHEMA_v2.json
- SI-0009 Reconciled Recovery State v2 + Recovery Completion Gate
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

REQUIRED_TRUE_FLAGS = (
    "all_material_items_dispositioned",
    "all_accepted_writes_read_back",
    "authority_unambiguous",
    "frontier_fresh",
    "no_material_conflicts",
    "input_tail_processed",
    "ingestion_complete",
)

TERMINAL_VERIFICATION_RESULTS = {
    "VERIFIED",
    "MISSING",
    "SUPERSEDED",
    "UNRECOVERABLE",
    "NOT_APPLICABLE",
}

RESOLVED_CONFLICT_STATES = {"RESOLVED", "SUPERSEDED"}
SAFE_WRITE_STATES = {"PLANNED", "WRITTEN", "ROLLED_BACK", "REPAIRED", "SKIPPED_DUPLICATE"}


def _stop(state: dict[str, Any], reason: str, detail: Any = None) -> dict[str, Any]:
    out = {
        "decision": "STOP",
        "reason": reason,
        "recovery_id": state.get("recovery_id"),
        "recovery_status": state.get("recovery_status"),
        "handoff_to_next_action_resolver": False,
    }
    if detail is not None:
        out["detail"] = detail
    return out


def _pass(state: dict[str, Any]) -> dict[str, Any]:
    gate = state["completion_gate"]
    return {
        "decision": "RECOVERY_COMPLETE",
        "reason": "all fail-closed recovery completion checks passed",
        "recovery_id": state.get("recovery_id"),
        "recovery_status": state.get("recovery_status"),
        "handoff_to_next_action_resolver": True,
        "can_auto_continue_after_normal_action_gates": gate.get("can_auto_continue") is True,
        "next_action": state.get("next_action"),
    }


def evaluate(state: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(state, dict):
        return {"decision": "STOP", "reason": "STATE_NOT_OBJECT", "handoff_to_next_action_resolver": False}

    if state.get("schema_version") != "2.0":
        return _stop(state, "UNSUPPORTED_SCHEMA_VERSION", state.get("schema_version"))

    if not state.get("recovery_id"):
        return _stop(state, "RECOVERY_ID_MISSING")

    status = state.get("recovery_status")
    if status != "INGESTION_COMPLETE":
        return _stop(state, "RECOVERY_NOT_COMPLETE", status)

    source = state.get("source")
    if not isinstance(source, dict):
        return _stop(state, "SOURCE_STATE_MISSING")
    if source.get("input_tail_processed") is not True:
        return _stop(state, "INPUT_TAIL_NOT_PROCESSED")
    if not source.get("sha256"):
        return _stop(state, "SOURCE_HASH_MISSING")

    gate = state.get("completion_gate")
    if not isinstance(gate, dict):
        return _stop(state, "COMPLETION_GATE_MISSING")
    for flag in REQUIRED_TRUE_FLAGS:
        if gate.get(flag) is not True:
            return _stop(state, f"COMPLETION_FLAG_NOT_TRUE:{flag}")
    if gate.get("secrets_persisted") is not False:
        return _stop(state, "SECRET_FIREWALL_NOT_GREEN")

    authority = state.get("authority")
    if not isinstance(authority, dict) or authority.get("authority_unambiguous") is not True:
        return _stop(state, "AUTHORITY_UNRESOLVED")

    partitions = state.get("project_partitions")
    if not isinstance(partitions, list) or not partitions:
        return _stop(state, "PROJECT_PARTITIONS_MISSING")
    for partition in partitions:
        if not isinstance(partition, dict):
            return _stop(state, "PROJECT_PARTITION_INVALID")
        if partition.get("material_items_dispositioned") is not True:
            return _stop(state, "MATERIAL_ITEMS_NOT_DISPOSITIONED", partition.get("partition_id"))
        frontier = partition.get("frontier")
        if not isinstance(frontier, dict) or frontier.get("fresh") is not True:
            return _stop(state, "FRONTIER_NOT_FRESH", partition.get("partition_id"))

    tasks = state.get("verification_tasks")
    if not isinstance(tasks, list):
        return _stop(state, "VERIFICATION_TASKS_INVALID")
    for task in tasks:
        if not isinstance(task, dict):
            return _stop(state, "VERIFICATION_TASK_INVALID")
        result = task.get("result")
        if result not in TERMINAL_VERIFICATION_RESULTS:
            return _stop(state, "VERIFICATION_TASK_NOT_TERMINAL", {"task_id": task.get("task_id"), "result": result})
        if result in {"VERIFIED", "SUPERSEDED"} and not task.get("evidence_ref"):
            return _stop(state, "VERIFICATION_EVIDENCE_MISSING", task.get("task_id"))

    unknowns = state.get("unknowns")
    if not isinstance(unknowns, list):
        return _stop(state, "UNKNOWNS_INVALID")
    material_unknowns = [u.get("unknown_id") for u in unknowns if isinstance(u, dict) and u.get("material") is True]
    if material_unknowns:
        return _stop(state, "MATERIAL_UNKNOWNS_REMAIN", material_unknowns)

    conflicts = state.get("conflicts")
    if not isinstance(conflicts, list):
        return _stop(state, "CONFLICTS_INVALID")
    open_material_conflicts = [
        c.get("conflict_id")
        for c in conflicts
        if isinstance(c, dict)
        and c.get("material") is True
        and c.get("status") not in RESOLVED_CONFLICT_STATES
    ]
    if open_material_conflicts:
        return _stop(state, "MATERIAL_CONFLICTS_REMAIN", open_material_conflicts)

    writes = state.get("writes")
    if not isinstance(writes, list):
        return _stop(state, "WRITES_INVALID")
    for write in writes:
        if not isinstance(write, dict):
            return _stop(state, "WRITE_RECORD_INVALID")
        status = write.get("status")
        if status not in SAFE_WRITE_STATES:
            return _stop(state, "WRITE_STATE_NOT_SAFE", {"write_id": write.get("write_id"), "status": status})
        if status in {"WRITTEN", "REPAIRED"} and write.get("readback_status") != "PASS":
            return _stop(state, "WRITE_READBACK_NOT_PASS", write.get("write_id"))
        if status == "PLANNED":
            return _stop(state, "PLANNED_WRITE_REMAINS", write.get("write_id"))

    next_action = state.get("next_action")
    if not isinstance(next_action, dict):
        return _stop(state, "NEXT_ACTION_MISSING")

    # The recovery gate does not itself authorize execution. It only makes the
    # state eligible for the normal action resolver. can_auto_continue is a
    # declaration that normal action gates may be evaluated next.
    if gate.get("can_auto_continue") is True:
        if next_action.get("requires_new_founder_choice") is True:
            return _stop(state, "AUTO_CONTINUE_CONTRADICTS_FOUNDER_DECISION_GATE")
        if next_action.get("requires_human_evidence") is True:
            return _stop(state, "AUTO_CONTINUE_CONTRADICTS_HUMAN_EVIDENCE_GATE")
        if next_action.get("requires_external_provider") is True:
            return _stop(state, "AUTO_CONTINUE_CONTRADICTS_PROVIDER_GATE")
        if next_action.get("executable_here") is not True:
            return _stop(state, "AUTO_CONTINUE_CONTRADICTS_EXECUTABILITY")

    return _pass(state)


def main() -> int:
    parser = argparse.ArgumentParser(description="Fail-closed IVDIVO Reconciled Recovery State v2 completion gate")
    parser.add_argument("state", type=Path)
    parser.add_argument("--compact", action="store_true")
    args = parser.parse_args()

    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
    except Exception as exc:
        result = {"decision": "STOP", "reason": f"STATE_READ_ERROR:{exc}", "handoff_to_next_action_resolver": False}
        print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
        return 2

    result = evaluate(state)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":") if args.compact else None, indent=None if args.compact else 2))
    return 0 if result["decision"] == "RECOVERY_COMPLETE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
