#!/usr/bin/env python3
"""Validate durable project-state coverage for portfolio resumability.

A project is routable only when it has a durable state pointer whose recovery is
PASS-like, or an explicit BLOCKED_RECOVERY record with a reason. The validator
checks routing completeness only; it never upgrades story/canon/Founder status.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("coverage index must be an object")
    return data


def audit(data: dict[str, Any]) -> dict[str, Any]:
    required = data.get("required_project_ids")
    if not isinstance(required, list) or not required:
        return {"status": "FAIL", "errors": [{"error": "MISSING_REQUIRED_PROJECT_IDS"}]}

    coverage = data.get("coverage") or []
    blocked = data.get("blocked_recovery") or []
    errors: list[dict[str, Any]] = []
    routed: dict[str, dict[str, Any]] = {}
    blocked_map: dict[str, dict[str, Any]] = {}

    for row in coverage:
        pid = row.get("project_id")
        if not pid:
            errors.append({"error": "COVERAGE_ROW_MISSING_PROJECT_ID"})
            continue
        if pid in routed:
            errors.append({"project_id": pid, "error": "DUPLICATE_COVERAGE_PROJECT"})
        routed[pid] = row
        if not row.get("state_path"):
            errors.append({"project_id": pid, "error": "MISSING_STATE_PATH"})
        recovery = str(row.get("recovery", ""))
        if not recovery.startswith("PASS"):
            errors.append({"project_id": pid, "error": "NON_PASS_RECOVERY_IN_COVERAGE", "value": recovery})

    for row in blocked:
        pid = row.get("project_id")
        if not pid:
            errors.append({"error": "BLOCKED_ROW_MISSING_PROJECT_ID"})
            continue
        if pid in blocked_map:
            errors.append({"project_id": pid, "error": "DUPLICATE_BLOCKED_PROJECT"})
        blocked_map[pid] = row
        if row.get("status") != "BLOCKED_RECOVERY":
            errors.append({"project_id": pid, "error": "INVALID_BLOCKED_STATUS"})
        if not row.get("reason"):
            errors.append({"project_id": pid, "error": "BLOCKED_WITHOUT_REASON"})

    overlap = sorted(set(routed) & set(blocked_map))
    for pid in overlap:
        errors.append({"project_id": pid, "error": "PROJECT_BOTH_ROUTED_AND_BLOCKED"})

    for pid in required:
        if pid not in routed and pid not in blocked_map:
            errors.append({"project_id": pid, "error": "UNROUTED_PROJECT"})

    expected_claim = "PASS_WITH_BLOCKED_RECOVERY" if blocked_map else "PASS_FULL"
    actual_claim = data.get("portfolio_resumability_claim")
    if actual_claim != expected_claim:
        errors.append({
            "error": "RESUMABILITY_CLAIM_MISMATCH",
            "expected": expected_claim,
            "actual": actual_claim,
        })

    return {
        "status": "PASS" if not errors else "FAIL",
        "required_project_ids": required,
        "routed_project_ids": sorted(routed),
        "blocked_project_ids": sorted(blocked_map),
        "portfolio_resumability_claim": actual_claim,
        "errors": errors,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--coverage", type=Path, default=Path("PROJECT_STATES/00_PROJECT_STATE_COVERAGE_INDEX.json"))
    args = p.parse_args()
    try:
        result = audit(load(args.coverage))
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "FAIL", "errors": [{"error": str(exc)}]}, ensure_ascii=False, indent=2))
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
