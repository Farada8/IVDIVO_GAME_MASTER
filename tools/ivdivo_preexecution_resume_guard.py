#!/usr/bin/env python3
"""Bounded Cycle32D candidate: guard against stale aggregate-router execution.

This module does not mutate canon or choose story content. It only decides
whether an aggregate next-action may be trusted before execution.
"""
from __future__ import annotations

from typing import Any, Dict


def _project_id(project: Dict[str, Any]) -> str | None:
    return project.get("project_id") or project.get("project")


def _project_next(project: Dict[str, Any]) -> str | None:
    terminal = project.get("terminal_frontier") or {}
    return (
        terminal.get("next_obligation")
        or project.get("next_unblocked_obligation")
        or project.get("next_safe_action")
        or project.get("next_action")
    )


def guard_resume(aggregate: Dict[str, Any], project: Dict[str, Any] | None) -> Dict[str, Any]:
    active = (aggregate.get("portfolio_frontier") or {}).get("active_project") or {}
    active_id = active.get("project_id")
    aggregate_next = active.get("next_unblocked_obligation")

    if not active_id or not aggregate_next:
        return {
            "decision": "STOP_NO_PROJECT_FRONTIER",
            "reason": "aggregate active project/frontier missing",
        }

    if not project:
        return {
            "decision": "STOP_NO_PROJECT_STATE",
            "project_id": active_id,
            "reason": "project-specific state missing",
        }

    project_id = _project_id(project)
    if project_id and project_id != active_id:
        return {
            "decision": "PROJECT_NOT_ACTIVE",
            "project_id": project_id,
            "aggregate_project_id": active_id,
        }

    project_next = _project_next(project)
    if not project_next:
        return {
            "decision": "STOP_NO_PROJECT_FRONTIER",
            "project_id": active_id,
            "reason": "project-specific next obligation missing",
        }

    if aggregate_next != project_next:
        return {
            "decision": "STOP_REBASE_REQUIRED",
            "project_id": active_id,
            "aggregate_next": aggregate_next,
            "project_next": project_next,
            "reason": "aggregate pointer conflicts with project-specific state",
        }

    return {
        "decision": "EXECUTE",
        "project_id": active_id,
        "next_action": project_next,
    }
