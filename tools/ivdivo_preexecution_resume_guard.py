#!/usr/bin/env python3
"""Fail-closed pre-execution resume guard for IVDIVO project routing.

Project-specific persisted state outranks stale aggregate router pointers.
Candidate mechanism only; does not mutate canon.
"""
from __future__ import annotations
from typing import Any, Dict


def _active_project(aggregate: Dict[str, Any]) -> Dict[str, Any]:
    return (aggregate.get("portfolio_frontier") or {}).get("active_project") or {}


def _project_id(project: Dict[str, Any]) -> str | None:
    return project.get("project_id") or project.get("project")


def _project_next(project: Dict[str, Any]) -> str | None:
    terminal = project.get("terminal_frontier") or {}
    return terminal.get("next_obligation") or project.get("next_safe_action") or project.get("next_action") or project.get("next_unblocked_obligation")


def guard_resume(aggregate: Dict[str, Any], project: Dict[str, Any] | None) -> Dict[str, Any]:
    active = _active_project(aggregate)
    active_id = active.get("project_id")
    aggregate_next = active.get("next_unblocked_obligation")
    if not active_id:
        return {"decision": "STOP_NO_PROJECT_FRONTIER", "reason": "aggregate router has no active project"}
    if not project:
        return {"decision": "STOP_NO_PROJECT_STATE", "project_id": active_id, "reason": "project-specific state missing"}
    project_id = _project_id(project)
    if project_id and project_id != active_id:
        return {"decision": "PROJECT_NOT_ACTIVE", "project_id": project_id, "active_project_id": active_id}
    project_next = _project_next(project)
    if not project_next:
        return {"decision": "STOP_NO_PROJECT_FRONTIER", "project_id": active_id, "reason": "project-specific next action missing"}
    if aggregate_next and aggregate_next != project_next:
        return {"decision": "STOP_REBASE_REQUIRED", "project_id": active_id, "aggregate_next": aggregate_next, "project_next": project_next, "reason": "aggregate router conflicts with project-specific frontier"}
    return {"decision": "EXECUTE", "project_id": active_id, "selected_next_action": project_next}
