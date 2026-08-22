#!/usr/bin/env python3
"""Cycle32D local candidate validator.

Purpose: detect stale aggregate-router pointers when a fresher project-specific
state has a terminal/next obligation that conflicts with the aggregate router.
This is a local self-improvement candidate. It does not mutate canon or CURRENT.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set


def _project_id(project: Dict[str, Any]) -> str | None:
    return project.get("project_id") or project.get("project")


def _project_next(project: Dict[str, Any]) -> str | None:
    terminal = project.get("terminal_frontier") or {}
    return terminal.get("next_obligation") or project.get("next_unblocked_obligation")


def _prohibitions(project: Dict[str, Any]) -> Set[str]:
    values: List[str] = []
    for key in ("prohibited", "do_not_repeat"):
        value = project.get(key) or []
        if isinstance(value, list):
            values.extend(str(x) for x in value)
    terminal = project.get("terminal_frontier") or {}
    if terminal.get("do_not_generate"):
        values.append(f"DO_NOT_GENERATE_{terminal['do_not_generate']}")
    return set(values)


def _normalized_tokens(text: str) -> Set[str]:
    return {t for t in text.upper().replace("-", "_").split("_") if t}


def _violates(action: str, prohibition: str) -> bool:
    if not action or not prohibition:
        return False
    p = prohibition.upper()
    a = action.upper()
    if p.startswith("DO_NOT_GENERATE_"):
        target = p.removeprefix("DO_NOT_GENERATE_")
        return target in a
    if p.startswith("DO_NOT_"):
        target = p.removeprefix("DO_NOT_")
        pt = _normalized_tokens(target)
        at = _normalized_tokens(a)
        return bool(pt) and pt.issubset(at)
    return False


def validate_frontier(aggregate: Dict[str, Any], project: Dict[str, Any]) -> Dict[str, Any]:
    findings: List[Dict[str, Any]] = []
    decision = "ALLOW"

    active = (aggregate.get("portfolio_frontier") or {}).get("active_project") or {}
    active_id = active.get("project_id")
    project_id = _project_id(project)

    if active_id and project_id and active_id != project_id:
        return {
            "decision": "NOT_APPLICABLE",
            "project_id": project_id,
            "aggregate_project_id": active_id,
            "findings": [],
        }

    aggregate_next = active.get("next_unblocked_obligation")
    project_next = _project_next(project)

    if aggregate_next and project_next and aggregate_next != project_next:
        findings.append({
            "code": "STALE_ROUTER_POINTER",
            "aggregate_next": aggregate_next,
            "project_next": project_next,
        })
        decision = "QUARANTINE"

    for prohibition in sorted(_prohibitions(project)):
        if aggregate_next and _violates(aggregate_next, prohibition):
            findings.append({
                "code": "PROHIBITED_CONTINUATION",
                "aggregate_next": aggregate_next,
                "prohibition": prohibition,
            })
            decision = "QUARANTINE"

    return {
        "decision": decision,
        "project_id": project_id,
        "aggregate_next": aggregate_next,
        "project_next": project_next,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("aggregate_json", type=Path)
    parser.add_argument("project_json", type=Path)
    args = parser.parse_args()

    aggregate = json.loads(args.aggregate_json.read_text(encoding="utf-8"))
    project = json.loads(args.project_json.read_text(encoding="utf-8"))
    result = validate_frontier(aggregate, project)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["decision"] == "QUARANTINE" else 0


if __name__ == "__main__":
    raise SystemExit(main())
