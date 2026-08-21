#!/usr/bin/env python3
"""IVDIVO interruption/recovery learning evidence summarizer.

Produces advisory promotion evidence only. Never promotes Self-Improvement candidates.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA_VERSION = "ivdivo.interruption_learning/1.0"
DECISIONS = {
    "RESUME_EXACT", "REBASE_FIRST", "RECOVER_VOLATILE_FIRST", "STOP",
    "QUARANTINE_EXTERNAL_SIDE_EFFECT", "VERIFY_STORE_BEFORE_RETRY",
}


def _canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def validate_event(raw: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw, dict):
        raise TypeError("event must be object")
    for key in ("event_id", "project_id", "work_unit", "recovery_decision"):
        if not isinstance(raw.get(key), str) or not raw[key].strip():
            raise ValueError(f"{key} required")
    decision = raw["recovery_decision"].upper()
    if decision not in DECISIONS:
        raise ValueError("invalid recovery_decision")
    for key in ("real_interruption", "false_resume", "false_stop"):
        if key in raw and not isinstance(raw[key], bool):
            raise ValueError(f"{key} must be bool")
    normalized = {}
    for key in (
        "duplicate_work_units_avoided", "writes_reconciled", "checkpoint_bytes",
        "checkpoint_tool_calls", "recovery_tool_calls",
    ):
        value = raw.get(key, 0)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{key} must be non-negative int")
        normalized[key] = value
    return {
        "event_id": raw["event_id"].strip(),
        "project_id": raw["project_id"].strip(),
        "work_unit": raw["work_unit"].strip(),
        "recovery_decision": decision,
        "real_interruption": raw.get("real_interruption", False),
        "false_resume": raw.get("false_resume", False),
        "false_stop": raw.get("false_stop", False),
        **normalized,
        "notes": list(raw.get("notes", [])) if isinstance(raw.get("notes", []), list) else [],
    }


def summarize_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(events, list):
        raise TypeError("events must be list")
    rows = [validate_event(e) for e in events]
    ids = [e["event_id"] for e in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate event_id")
    total = len(rows)
    real = [e for e in rows if e["real_interruption"]]
    projects = sorted({e["project_id"] for e in real})
    false_resume_count = sum(1 for e in rows if e["false_resume"])
    real_false_resume_count = sum(1 for e in real if e["false_resume"])
    false_stop_count = sum(1 for e in rows if e["false_stop"])
    real_false_stop_count = sum(1 for e in real if e["false_stop"])
    duplicate_avoided = sum(e["duplicate_work_units_avoided"] for e in rows)
    writes_reconciled = sum(e["writes_reconciled"] for e in rows)
    checkpoint_tool_calls = sum(e["checkpoint_tool_calls"] for e in rows)
    recovery_tool_calls = sum(e["recovery_tool_calls"] for e in rows)
    checkpoint_bytes = sum(e["checkpoint_bytes"] for e in rows)
    real_false_stop_rate = real_false_stop_count / len(real) if real else 0.0

    # Any false resume, even synthetic, is a safety regression signal and blocks promotion.
    if false_resume_count:
        recommendation, reason = "HOLD", "FALSE_RESUME_PRESENT"
    elif len(real) < 1:
        recommendation, reason = "HOLD", "NO_REAL_INTERRUPTION_EVIDENCE"
    elif len(real) < 3 or len(projects) < 2:
        recommendation, reason = "CONTINUE_PILOT", "INSUFFICIENT_CROSS_PROJECT_RECOVERY_EVIDENCE"
    elif real_false_stop_rate > 0.10:
        recommendation, reason = "NARROW", "REAL_FALSE_STOP_RATE_TOO_HIGH"
    else:
        recommendation, reason = "ELIGIBLE_FOR_PROMOTION_REVIEW", "MINIMUM_RECOVERY_EVIDENCE_MET"

    metrics = {
        "event_count": total,
        "real_interruption_count": len(real),
        "real_project_count": len(projects),
        "projects": projects,
        "false_resume_count_all": false_resume_count,
        "false_resume_count_real": real_false_resume_count,
        "false_stop_count_all": false_stop_count,
        "false_stop_count_real": real_false_stop_count,
        "real_false_stop_rate": real_false_stop_rate,
        "duplicate_work_units_avoided": duplicate_avoided,
        "writes_reconciled": writes_reconciled,
        "checkpoint_tool_calls": checkpoint_tool_calls,
        "recovery_tool_calls": recovery_tool_calls,
        "checkpoint_bytes_total": checkpoint_bytes,
        "checkpoint_bytes_mean": (checkpoint_bytes / total) if total else 0.0,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "decision": "ADVISORY_ONLY",
        "promotion_recommendation": recommendation,
        "reason": reason,
        "metrics": metrics,
        "events_sha256": _sha(rows),
        "evidence_boundary": [
            "NO_AUTOMATIC_PROMOTION",
            "NO_FOUNDER_APPROVAL_INFERRED",
            "NO_HUMAN_QUALITY_EVIDENCE_INFERRED",
            "SYNTHETIC_EVENTS_MAY_BLOCK_FOR_SAFETY_BUT_CANNOT_SATISFY_REAL_EVIDENCE_THRESHOLD",
        ],
    }
