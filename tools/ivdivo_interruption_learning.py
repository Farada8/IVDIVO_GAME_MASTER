#!/usr/bin/env python3
"""IVDIVO interruption/recovery learning evidence summarizer.

Schema 1.1 separates one physical interruption incident from one or more
project recovery slices. This prevents a single browser/session failure that
affects multiple projects from being counted as multiple genuine interruption
events.

The output is advisory evidence only. It never promotes a Self-Improvement
candidate automatically.
"""
from __future__ import annotations

import hashlib
import json
from typing import Any

SCHEMA_VERSION = "ivdivo.interruption_learning/1.1"
DECISIONS = {
    "RESUME_EXACT",
    "REBASE_FIRST",
    "RECOVER_VOLATILE_FIRST",
    "RECOVER_PERSISTED_AUTHORITY_FIRST",
    "RECOVER_PERSISTED_AUTHORITY_THEN_APPLY_SI0015_FRESHNESS",
    "STOP",
    "QUARANTINE_EXTERNAL_SIDE_EFFECT",
    "VERIFY_STORE_BEFORE_RETRY",
}

REQUIRED_GENUINE_INCIDENTS = 3
REQUIRED_DISTINCT_PROJECTS = 2


def _canonical(obj: Any) -> bytes:
    return json.dumps(
        obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _sha(obj: Any) -> str:
    return hashlib.sha256(_canonical(obj)).hexdigest()


def _required_text(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} required")
    return value.strip()


def validate_event(raw: dict[str, Any]) -> dict[str, Any]:
    """Normalize one recovery-slice evidence row.

    Backward compatibility:
    - legacy ``event_id`` becomes ``incident_id`` when incident_id is absent;
    - ``project_slice_id`` is accepted as an alias for project_id;
    - a deterministic recovery_id is derived when absent;
    - legacy real_interruption=True rows remain qualifying unless a newer
      explicit readback/qualification field proves otherwise.
    """
    if not isinstance(raw, dict):
        raise TypeError("event must be object")

    event_id = _required_text(raw.get("event_id"), "event_id")
    project_id = _required_text(
        raw.get("project_id") or raw.get("project_slice_id"), "project_id"
    )
    work_unit = _required_text(raw.get("work_unit"), "work_unit")
    decision = _required_text(raw.get("recovery_decision"), "recovery_decision").upper()
    if decision not in DECISIONS:
        raise ValueError("invalid recovery_decision")

    incident_id = _required_text(raw.get("incident_id") or event_id, "incident_id")
    recovery_id = raw.get("recovery_id")
    if recovery_id is None:
        recovery_id = f"{incident_id}::{project_id}::{work_unit}"
    recovery_id = _required_text(recovery_id, "recovery_id")

    for key in (
        "real_interruption",
        "false_resume",
        "false_stop",
        "project_slice_readback_complete",
        "qualifying_recovery",
        "qualifies_as_genuine_si0014_recovery_event",
    ):
        if key in raw and not isinstance(raw[key], bool):
            raise ValueError(f"{key} must be bool")

    normalized: dict[str, int] = {}
    for key in (
        "duplicate_work_units_avoided",
        "writes_reconciled",
        "checkpoint_bytes",
        "checkpoint_tool_calls",
        "recovery_tool_calls",
    ):
        value = raw.get(key, 0)
        if not isinstance(value, int) or value < 0:
            raise ValueError(f"{key} must be non-negative int")
        normalized[key] = value

    real_interruption = raw.get("real_interruption", False)
    false_resume = raw.get("false_resume", False)
    false_stop = raw.get("false_stop", False)

    # Legacy real rows had no readback flag. Preserve their old semantics while
    # newer evidence can explicitly fail closed with readback_complete=False.
    project_slice_readback_complete = raw.get(
        "project_slice_readback_complete", real_interruption
    )

    explicit_qualification = raw.get("qualifying_recovery")
    if explicit_qualification is None:
        explicit_qualification = raw.get(
            "qualifies_as_genuine_si0014_recovery_event"
        )

    if explicit_qualification is None:
        qualifying_recovery = bool(
            real_interruption
            and project_slice_readback_complete
            and not false_resume
        )
    else:
        qualifying_recovery = bool(explicit_qualification)

    # Explicit qualification may never override hard safety prerequisites.
    if not real_interruption or not project_slice_readback_complete or false_resume:
        qualifying_recovery = False

    notes = raw.get("notes", [])
    if not isinstance(notes, list):
        notes = []

    return {
        "event_id": event_id,
        "incident_id": incident_id,
        "recovery_id": recovery_id,
        "project_id": project_id,
        "work_unit": work_unit,
        "recovery_decision": decision,
        "real_interruption": real_interruption,
        "project_slice_readback_complete": project_slice_readback_complete,
        "qualifying_recovery": qualifying_recovery,
        "false_resume": false_resume,
        "false_stop": false_stop,
        **normalized,
        "notes": list(notes),
    }


def _validate_incident_consistency(rows: list[dict[str, Any]]) -> None:
    """Reject one incident_id being described as both real and synthetic."""
    flags: dict[str, set[bool]] = {}
    for row in rows:
        flags.setdefault(row["incident_id"], set()).add(row["real_interruption"])
    inconsistent = sorted(
        incident for incident, values in flags.items() if len(values) > 1
    )
    if inconsistent:
        raise ValueError(
            "incident_id mixes real_interruption states: " + ", ".join(inconsistent)
        )


def _incident_rollup(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_incident: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_incident.setdefault(row["incident_id"], []).append(row)

    result = []
    for incident_id in sorted(by_incident):
        group = by_incident[incident_id]
        qualifying = [row for row in group if row["qualifying_recovery"]]
        result.append(
            {
                "incident_id": incident_id,
                "real_interruption": group[0]["real_interruption"],
                "recovery_slice_count": len(group),
                "qualifying_recovery_slice_count": len(qualifying),
                "projects": sorted({row["project_id"] for row in qualifying}),
                "recovery_ids": sorted(row["recovery_id"] for row in group),
                "false_resume_present": any(row["false_resume"] for row in group),
                "false_stop_present": any(
                    row["false_stop"] for row in qualifying
                ),
            }
        )
    return result


def summarize_events(events: list[dict[str, Any]]) -> dict[str, Any]:
    if not isinstance(events, list):
        raise TypeError("events must be list")

    rows = [validate_event(event) for event in events]

    recovery_ids = [row["recovery_id"] for row in rows]
    if len(recovery_ids) != len(set(recovery_ids)):
        raise ValueError("duplicate recovery_id")

    _validate_incident_consistency(rows)

    total_rows = len(rows)
    real_rows = [row for row in rows if row["real_interruption"]]
    qualifying_rows = [row for row in real_rows if row["qualifying_recovery"]]

    all_incidents = sorted({row["incident_id"] for row in rows})
    real_incidents = sorted({row["incident_id"] for row in real_rows})
    qualifying_incidents = sorted({row["incident_id"] for row in qualifying_rows})
    projects = sorted({row["project_id"] for row in qualifying_rows})

    false_resume_count = sum(1 for row in rows if row["false_resume"])
    real_false_resume_count = sum(1 for row in real_rows if row["false_resume"])
    false_stop_count = sum(1 for row in rows if row["false_stop"])
    qualifying_false_stop_count = sum(
        1 for row in qualifying_rows if row["false_stop"]
    )

    duplicate_avoided = sum(row["duplicate_work_units_avoided"] for row in rows)
    writes_reconciled = sum(row["writes_reconciled"] for row in rows)
    checkpoint_tool_calls = sum(row["checkpoint_tool_calls"] for row in rows)
    recovery_tool_calls = sum(row["recovery_tool_calls"] for row in rows)
    checkpoint_bytes = sum(row["checkpoint_bytes"] for row in rows)

    qualifying_false_stop_rate = (
        qualifying_false_stop_count / len(qualifying_rows)
        if qualifying_rows
        else 0.0
    )

    # Any false resume, even synthetic, is a safety regression signal and blocks
    # promotion. Synthetic/controlled rows may block for safety but can never
    # satisfy the genuine incident threshold.
    if false_resume_count:
        recommendation, reason = "HOLD", "FALSE_RESUME_PRESENT"
    elif len(qualifying_incidents) < 1:
        recommendation, reason = "HOLD", "NO_QUALIFIED_REAL_INTERRUPTION_EVIDENCE"
    elif (
        len(qualifying_incidents) < REQUIRED_GENUINE_INCIDENTS
        or len(projects) < REQUIRED_DISTINCT_PROJECTS
    ):
        recommendation, reason = (
            "CONTINUE_PILOT",
            "INSUFFICIENT_GENUINE_INCIDENT_OR_PROJECT_DIVERSITY_EVIDENCE",
        )
    elif qualifying_false_stop_rate > 0.10:
        recommendation, reason = "NARROW", "REAL_FALSE_STOP_RATE_TOO_HIGH"
    else:
        recommendation, reason = (
            "ELIGIBLE_FOR_PROMOTION_REVIEW",
            "MINIMUM_RECOVERY_EVIDENCE_MET",
        )

    metrics = {
        # Backward-compatible field names with corrected incident semantics.
        "event_count": total_rows,
        "real_interruption_count": len(qualifying_incidents),
        "real_project_count": len(projects),
        "projects": projects,
        # Explicit 1.1 metrics.
        "recovery_slice_count": total_rows,
        "real_interruption_row_count": len(real_rows),
        "qualifying_recovery_slice_count": len(qualifying_rows),
        "incident_count_all": len(all_incidents),
        "real_incident_count_observed": len(real_incidents),
        "qualified_real_incident_count": len(qualifying_incidents),
        "qualified_real_incidents": qualifying_incidents,
        "false_resume_count_all": false_resume_count,
        "false_resume_count_real": real_false_resume_count,
        "false_stop_count_all": false_stop_count,
        "false_stop_count_real": qualifying_false_stop_count,
        "real_false_stop_rate": qualifying_false_stop_rate,
        "duplicate_work_units_avoided": duplicate_avoided,
        "writes_reconciled": writes_reconciled,
        "checkpoint_tool_calls": checkpoint_tool_calls,
        "recovery_tool_calls": recovery_tool_calls,
        "checkpoint_bytes_total": checkpoint_bytes,
        "checkpoint_bytes_mean": (
            checkpoint_bytes / total_rows if total_rows else 0.0
        ),
    }

    return {
        "schema_version": SCHEMA_VERSION,
        "decision": "ADVISORY_ONLY",
        "promotion_recommendation": recommendation,
        "reason": reason,
        "promotion_progress": {
            "genuine_incidents": len(qualifying_incidents),
            "required_genuine_incidents": REQUIRED_GENUINE_INCIDENTS,
            "distinct_projects": len(projects),
            "required_distinct_projects": REQUIRED_DISTINCT_PROJECTS,
            "zero_false_resume": false_resume_count == 0,
            "promotion_authorized": False,
        },
        "metrics": metrics,
        "incident_rollup": _incident_rollup(rows),
        "events_sha256": _sha(rows),
        "evidence_boundary": [
            "NO_AUTOMATIC_PROMOTION",
            "NO_FOUNDER_APPROVAL_INFERRED",
            "NO_HUMAN_QUALITY_EVIDENCE_INFERRED",
            "ONE_PHYSICAL_INTERRUPTION_COUNTS_ONCE_EVEN_WITH_MULTIPLE_PROJECT_SLICES",
            "SYNTHETIC_EVENTS_MAY_BLOCK_FOR_SAFETY_BUT_CANNOT_SATISFY_REAL_EVIDENCE_THRESHOLD",
        ],
    }
