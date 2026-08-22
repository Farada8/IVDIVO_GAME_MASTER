#!/usr/bin/env python3
"""Cycle32D candidate integration gate for v2 resume/autopilot routing."""
from __future__ import annotations
from typing import Any, Dict
from cycle32d_stale_router_validator import validate_frontier

def select_next_obligation(aggregate: Dict[str, Any], project: Dict[str, Any]) -> Dict[str, Any]:
    gate = validate_frontier(aggregate, project)
    if gate["decision"] == "QUARANTINE":
        return {"decision":"STOP_REBASE_REQUIRED","gate":gate,"selected_next_action":None}
    if gate["decision"] == "NOT_APPLICABLE":
        return {"decision":"PROJECT_NOT_ACTIVE","gate":gate,"selected_next_action":None}
    project_next = gate.get("project_next")
    if not project_next:
        return {"decision":"STOP_NO_PROJECT_FRONTIER","gate":gate,"selected_next_action":None}
    return {"decision":"EXECUTE","gate":gate,"selected_next_action":project_next}
