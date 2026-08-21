#!/usr/bin/env python3
"""Resolve whether persisted IVDIVO project state may auto-continue.

Read-only utility aligned to:
IVDIVO_NARRATIVE_OS/13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md v1.1

It never calls providers, spends credits, changes canon, mutates project state,
or claims human evidence. It converts explicit persisted gates into a fail-closed
CONTINUE / STOP decision for the already-selected next action.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


STOP_STATE_STATUSES = {
    "BLOCKED",
    "AUTHORITY_UNRESOLVED",
    "FRONTIER_CONFLICT",
    "CANON_APPROVAL_REQUIRED",
    "HUMAN_EVIDENCE_REQUIRED",
    "EXTERNAL_PROVIDER_REQUIRED",
    "HOLD",
}

REQUIRED_ACTION_FLAGS = (
    "freshness_valid",
    "authority_unambiguous",
    "dependencies_pass",
    "executable_here",
    "requires_new_founder_choice",
    "requires_human_evidence",
    "requires_external_provider",
    "reopens_locked_layer",
    "irreversible_high_impact",
)


def _stop(reason: str, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision": "STOP",
        "reason": reason,
        "state_revision": state.get("state_revision"),
        "selected_next_action": state.get("selected_next_action"),
    }


def _continue(state: dict[str, Any]) -> dict[str, Any]:
    return {
        "decision": "CONTINUE",
        "reason": (
            "fresh authority + dependencies PASS + executable action; "
            "no decision/human/provider/locked-layer/irreversible blocker"
        ),
        "state_revision": state.get("state_revision"),
        "selected_next_action": state.get("selected_next_action"),
    }


def resolve(state: dict[str, Any]) -> dict[str, Any]:
    status = str(state.get("state_status", "")).strip().upper()
    if not status:
        return _stop("STATE_STATUS_MISSING", state)
    if status in STOP_STATE_STATUSES:
        return _stop(f"STATE_STATUS:{status}", state)
    if status == "COMPLETE":
        return _stop("PROJECT_STATE_COMPLETE", state)
    if status != "ACTIVE":
        return _stop(f"UNKNOWN_STATE_STATUS:{status}", state)

    authority_sources = state.get("authority_sources")
    if not isinstance(authority_sources, list) or not authority_sources:
        return _stop("AUTHORITY_SOURCES_MISSING", state)

    source = state.get("current_source")
    if not isinstance(source, dict) or not str(source.get("ref", "")).strip():
        return _stop("CURRENT_SOURCE_MISSING", state)

    blocked = state.get("blocked_reasons")
    if not isinstance(blocked, list):
        return _stop("BLOCKED_REASONS_MISSING_OR_INVALID", state)
    if blocked:
        return _stop("BLOCKED_REASONS_PRESENT", state)

    fatal_major = state.get("unresolved_fatal_major")
    if not isinstance(fatal_major, list):
        return _stop("UNRESOLVED_FATAL_MAJOR_MISSING_OR_INVALID", state)
    if fatal_major:
        return _stop("FATAL_MAJOR_UNRESOLVED", state)

    action = state.get("selected_next_action")
    if not isinstance(action, dict):
        return _stop("SELECTED_NEXT_ACTION_MISSING_OR_INVALID", state)

    missing = [name for name in REQUIRED_ACTION_FLAGS if name not in action]
    if missing:
        return _stop("ACTION_FLAGS_MISSING:" + ",".join(missing), state)

    if action["freshness_valid"] is not True:
        return _stop("STALE_OR_UNVERIFIED_FRONTIER", state)
    if action["authority_unambiguous"] is not True:
        return _stop("AUTHORITY_UNRESOLVED", state)
    if action["dependencies_pass"] is not True:
        return _stop("DEPENDENCY_GATE_NOT_PASS", state)
    if action["executable_here"] is not True:
        return _stop("TOOL_RUNTIME_LIMITATION", state)

    if action["requires_new_founder_choice"] is True:
        return _stop("DECISION_GATE", state)
    if action["requires_human_evidence"] is True:
        return _stop("HUMAN_EVIDENCE_REQUIRED", state)

    if action["requires_external_provider"] is True:
        if action.get("external_provider_available") is not True:
            return _stop("EXTERNAL_PROVIDER_REQUIRED", state)

    if action["reopens_locked_layer"] is True:
        if action.get("locked_layer_reopen_authorized") is not True:
            return _stop("LOCKED_LAYER_REOPEN_NOT_AUTHORIZED", state)

    if action["irreversible_high_impact"] is True:
        if action.get("approval_present") is not True:
            return _stop("IRREVERSIBLE_APPROVAL_REQUIRED", state)

    return _continue(state)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed resolver for an IVDIVO persisted execution-state JSON file."
    )
    parser.add_argument("state", type=Path, help="Path to project CURRENT_EXECUTION_STATE JSON")
    parser.add_argument("--compact", action="store_true", help="Emit compact JSON")
    args = parser.parse_args()

    try:
        state = json.loads(args.state.read_text(encoding="utf-8"))
        if not isinstance(state, dict):
            raise TypeError("top-level execution state must be a JSON object")
    except Exception as exc:  # fail closed
        result = {"decision": "STOP", "reason": f"STATE_READ_ERROR:{exc}"}
        print(
            json.dumps(
                result,
                ensure_ascii=False,
                separators=(",", ":") if args.compact else None,
                indent=None if args.compact else 2,
            )
        )
        return 2

    result = resolve(state)
    print(
        json.dumps(
            result,
            ensure_ascii=False,
            separators=(",", ":") if args.compact else None,
            indent=None if args.compact else 2,
        )
    )
    return 0 if result["decision"] == "CONTINUE" else 1


if __name__ == "__main__":
    raise SystemExit(main())
