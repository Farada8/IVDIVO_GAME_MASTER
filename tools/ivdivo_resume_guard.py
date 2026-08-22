#!/usr/bin/env python3
"""Candidate pre-execution guard for IVDIVO v2 resume/autopilot routing.

This file is intentionally candidate-only on the Cycle32D branch. It does not
change canon or CURRENT authority. It fails closed when aggregate portfolio
routing disagrees with the active project's persisted frontier.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
from typing import Any, Dict

_HERE = Path(__file__).resolve().parent.parent
_VALIDATOR = _HERE / "SELF_IMPROVEMENT_DELTAS" / "CYCLE32D_2026-08-22" / "tools" / "cycle32d_stale_router_validator.py"
_spec = importlib.util.spec_from_file_location("cycle32d_stale_router_validator", _VALIDATOR)
_mod = importlib.util.module_from_spec(_spec)
assert _spec and _spec.loader
_spec.loader.exec_module(_mod)
validate_frontier = _mod.validate_frontier


def gate_resume(aggregate: Dict[str, Any], project: Dict[str, Any]) -> Dict[str, Any]:
    gate = validate_frontier(aggregate, project)
    if gate["decision"] == "QUARANTINE":
        return {"decision":"STOP_REBASE_REQUIRED","selected_next_action":None,"gate":gate}
    if gate["decision"] == "NOT_APPLICABLE":
        return {"decision":"PROJECT_NOT_ACTIVE","selected_next_action":None,"gate":gate}
    project_next = gate.get("project_next")
    if not project_next:
        return {"decision":"STOP_NO_PROJECT_FRONTIER","selected_next_action":None,"gate":gate}
    return {"decision":"EXECUTE","selected_next_action":project_next,"gate":gate}


def main() -> int:
    p=argparse.ArgumentParser(description="Guard IVDIVO resume routing before selecting next production action")
    p.add_argument("aggregate_json", type=Path)
    p.add_argument("project_json", type=Path)
    a=p.parse_args()
    result=gate_resume(json.loads(a.aggregate_json.read_text(encoding="utf-8")), json.loads(a.project_json.read_text(encoding="utf-8")))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["decision"].startswith("STOP_") else 0

if __name__ == "__main__":
    raise SystemExit(main())
