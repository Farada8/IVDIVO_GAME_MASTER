#!/usr/bin/env python3
"""Advisory state-convergence auditor for IVDIVO persisted routing artifacts.

This tool never mutates canon or project state. It compares persisted routing
claims for one or more projects and identifies lower-authority stale pointers,
same-precedence conflicts, terminal-gate overrides, and stale source revisions.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

AUTHORITY_RANK = {
    "FOUNDER_NEWEST_DIRECT_INSTRUCTION": 100,
    "LOCKED_PROJECT_OR_BOOK_CANON_AND_SOURCE_OF_TRUTH": 95,
    "PROJECT_SOURCE_OF_TRUTH_OR_TERMINAL_GATE": 90,
    "CURRENT_DOMAIN_AUTHORITY": 80,
    "PROJECT_SPECIFIC_EXECUTION_STATE_OR_DRAFT_STATUS": 70,
    "CURRENT_IVDIVO_SYSTEM_STATE": 60,
    "CURRENT_PROMPTS_AND_WORKSTATE_MIRRORS": 50,
    "EXTERNAL_MODEL_HANDOFF_WITH_DISPOSITION": 40,
    "WORKING_CANDIDATE": 30,
    "REFERENCE_ONLY": 10,
}

TERMINAL_STATES = {
    "COMPLETE",
    "FINAL_STORY_GATE_PASS",
    "EXTERNAL_FEEDBACK_READY",
    "FOUNDER_LOCK_DECISION_GATE",
    "HUMAN_EVIDENCE_REQUIRED",
    "EXTERNAL_PROVIDER_REQUIRED",
    "HOLD",
    "BLOCKED",
}


def _rank(artifact):
    return AUTHORITY_RANK.get(str(artifact.get("authority_class", "")), -1)


def _terminal(artifact):
    return bool(artifact.get("terminal")) or str(artifact.get("state", "")).upper() in TERMINAL_STATES


def audit(payload):
    artifacts = payload.get("artifacts")
    if not isinstance(artifacts, list):
        return {"status": "FAIL_CLOSED", "reason": "ARTIFACTS_MISSING_OR_INVALID", "projects": []}

    grouped = {}
    for artifact in artifacts:
        if isinstance(artifact, dict) and artifact.get("project_id"):
            grouped.setdefault(str(artifact["project_id"]), []).append(artifact)

    projects = []
    global_status = "PASS"

    for project_id, items in sorted(grouped.items()):
        issues = []

        for artifact in items:
            expected = artifact.get("expected_source_revision")
            observed = artifact.get("observed_source_revision")
            if expected is not None and observed is not None and expected != observed:
                issues.append({
                    "type": "STALE_SOURCE_REVISION",
                    "artifact_id": artifact.get("artifact_id"),
                    "expected": expected,
                    "observed": observed,
                    "disposition": "REBASE_DO_NOT_OVERWRITE",
                })

        ranked = [artifact for artifact in items if _rank(artifact) >= 0]
        if not ranked:
            projects.append({
                "project_id": project_id,
                "status": "FAIL_CLOSED",
                "issues": [{"type": "NO_RECOGNIZED_AUTHORITY"}],
            })
            global_status = "FAIL_CLOSED"
            continue

        max_rank = max(_rank(artifact) for artifact in ranked)
        strongest = [artifact for artifact in ranked if _rank(artifact) == max_rank]
        actions = {str(a.get("next_action")) for a in strongest if a.get("next_action") is not None}
        unresolved = len(actions) > 1
        if unresolved:
            issues.append({
                "type": "AUTHORITY_UNRESOLVED_SAME_PRECEDENCE",
                "artifact_ids": [a.get("artifact_id") for a in strongest],
                "actions": sorted(actions),
                "disposition": "STOP_AUTHORITY_UNRESOLVED",
            })

        winner = sorted(strongest, key=lambda a: (not _terminal(a), str(a.get("artifact_id"))))[0]
        winner_action = winner.get("next_action")

        for artifact in ranked:
            if artifact is winner:
                continue
            if _rank(artifact) < max_rank and artifact.get("next_action") is not None and artifact.get("next_action") != winner_action:
                issues.append({
                    "type": "STALE_LOWER_AUTHORITY_POINTER",
                    "artifact_id": artifact.get("artifact_id"),
                    "stale_next_action": artifact.get("next_action"),
                    "stronger_artifact_id": winner.get("artifact_id"),
                    "stronger_next_action": winner_action,
                    "disposition": "PATCH_POINTER_ONLY",
                })

        if _terminal(winner):
            for artifact in ranked:
                if _rank(artifact) < max_rank and str(artifact.get("state", "")).upper() == "ACTIVE":
                    issues.append({
                        "type": "TERMINAL_GATE_OVERRIDES_ACTIVE_POINTER",
                        "artifact_id": artifact.get("artifact_id"),
                        "terminal_artifact_id": winner.get("artifact_id"),
                        "disposition": "STOP_OR_ROUTE_TO_TERMINAL_NEXT_EVIDENCE",
                    })

        status = "FAIL_CLOSED" if unresolved else ("ISSUES_FOUND" if issues else "PASS")
        if status == "FAIL_CLOSED":
            global_status = "FAIL_CLOSED"
        elif status != "PASS" and global_status == "PASS":
            global_status = "ISSUES_FOUND"

        projects.append({
            "project_id": project_id,
            "status": status,
            "selected_authority": winner.get("artifact_id"),
            "selected_next_action": winner_action,
            "issues": issues,
        })

    return {"status": global_status, "projects": projects}


def main():
    parser = argparse.ArgumentParser(description="IVDIVO advisory state-convergence auditor")
    parser.add_argument("input", type=Path)
    args = parser.parse_args()
    try:
        payload = json.loads(args.input.read_text(encoding="utf-8"))
    except Exception as exc:
        print(json.dumps({"status": "FAIL_CLOSED", "reason": f"INPUT_READ_ERROR:{exc}"}))
        return 2
    result = audit(payload)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] in {"PASS", "ISSUES_FOUND"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
