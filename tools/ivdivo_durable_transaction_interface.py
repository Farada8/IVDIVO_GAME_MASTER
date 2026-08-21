#!/usr/bin/env python3
"""Versioned compatibility facade for SI-0012 transaction semantics + SI-0014 recovery.

This module does not replace either candidate runtime. It normalizes their decisions,
qualifies interruption evidence fail-closed, and keeps promotion advisory-only.
"""
from __future__ import annotations

import hashlib
from typing import Any

from tools.ivdivo_durable_write_reconciler import reconcile_transaction
from tools.ivdivo_interruption_learning import summarize_events

INTERFACE_VERSION = "ivdivo.durable_transaction_interface/1.0"

QUALIFIED_REAL = "QUALIFIED_REAL_PACKET"
EXCLUDED_CONTROLLED = "EXCLUDED_CONTROLLED"
EXCLUDED_SYNTHETIC = "EXCLUDED_SYNTHETIC"
UNVERIFIED_REAL_CLAIM = "UNVERIFIED_REAL_CLAIM"

GENUINE_ORIGINS = {
    "UNPLANNED_UI_SESSION_LOSS",
    "UNPLANNED_PROCESS_TERMINATION",
    "UNPLANNED_RUNTIME_RESTART",
    "UNPLANNED_NETWORK_OR_PLATFORM_DISCONNECT",
}


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def adapt_si0012_bytes_transaction(old_bytes: bytes, new_bytes: bytes, expected_hash: str) -> dict[str, Any]:
    """Map the SI-0012 single-store stale-hash contract into the unified vocabulary."""
    actual = _sha(old_bytes)
    if actual != expected_hash:
        return {
            "interface_version": INTERFACE_VERSION,
            "source_runtime": "SI-0012",
            "decision": "STOP",
            "reason": "STALE_REJECTED",
            "actual_hash": actual,
        }
    if old_bytes == new_bytes:
        return {
            "interface_version": INTERFACE_VERSION,
            "source_runtime": "SI-0012",
            "decision": "STOP",
            "reason": "NO_EFFECT_REJECTED",
            "actual_hash": actual,
        }
    return {
        "interface_version": INTERFACE_VERSION,
        "source_runtime": "SI-0012",
        "decision": "EXECUTE_MISSING_SAFE_ACTIONS",
        "reason": "LEGACY_SINGLE_STORE_READY",
        "action_ids": ["SI0012_SINGLE_STORE_WRITE"],
        "old_hash": actual,
        "new_hash": _sha(new_bytes),
    }


def verify_si0012_readback(expected_new: bytes, readback: bytes) -> dict[str, Any]:
    """Map SI-0012 readback semantics into STOP / TRANSACTION_COMPLETE."""
    if expected_new != readback:
        return {
            "interface_version": INTERFACE_VERSION,
            "source_runtime": "SI-0012",
            "decision": "STOP",
            "reason": "READBACK_MISMATCH",
            "expected": _sha(expected_new),
            "readback": _sha(readback),
        }
    return {
        "interface_version": INTERFACE_VERSION,
        "source_runtime": "SI-0012",
        "decision": "TRANSACTION_COMPLETE",
        "reason": "READBACK_VERIFIED",
        "hash": _sha(readback),
    }


def reconcile_si0014(
    plan: dict[str, Any],
    *,
    current_repo_main_sha: str,
    current_state_revision: str,
    external_blockers: list[Any] | None = None,
) -> dict[str, Any]:
    """Delegate multi-store recovery to SI-0014 without forking its planner."""
    out = reconcile_transaction(
        plan,
        current_repo_main_sha=current_repo_main_sha,
        current_state_revision=current_state_revision,
        external_blockers=external_blockers,
    )
    return {"interface_version": INTERFACE_VERSION, "source_runtime": "SI-0014", **out}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _evidence_refs_ok(value: Any) -> bool:
    return isinstance(value, list) and len(value) >= 2 and all(_nonempty(v) for v in value)


def qualify_interruption_event(event: dict[str, Any], evidence: dict[str, Any] | None) -> dict[str, Any]:
    """Fail-closed qualification for genuine interruption evidence.

    A caller-provided real_interruption=true is never trusted by itself. Controlled,
    synthetic, or incomplete packets are normalized to real_interruption=false.
    External reference existence must still be verified by the caller/readback layer.
    """
    if not isinstance(event, dict):
        raise TypeError("event must be object")
    evidence = evidence or {}

    origin = str(evidence.get("interruption_origin", "")).upper()
    checks = {
        "controlled_false": evidence.get("controlled") is False,
        "synthetic_false": evidence.get("synthetic") is False,
        "unplanned_true": evidence.get("unplanned") is True,
        "genuine_origin": origin in GENUINE_ORIGINS,
        "restart_observed": evidence.get("restart_observed") is True,
        "pre_interrupt_checkpoint_id": _nonempty(evidence.get("pre_interrupt_checkpoint_id")),
        "post_restart_authority_readback": evidence.get("post_restart_authority_readback") is True,
        "recovery_readback_verified": evidence.get("recovery_readback_verified") is True,
        "project_state_before": _nonempty(evidence.get("project_state_before")),
        "project_state_after": _nonempty(evidence.get("project_state_after")),
        "source_evidence_refs": _evidence_refs_ok(evidence.get("source_evidence_refs")),
    }

    if evidence.get("controlled") is True:
        qualification = EXCLUDED_CONTROLLED
    elif evidence.get("synthetic") is True:
        qualification = EXCLUDED_SYNTHETIC
    elif all(checks.values()):
        qualification = QUALIFIED_REAL
    else:
        qualification = UNVERIFIED_REAL_CLAIM

    qualified_real = qualification == QUALIFIED_REAL
    normalized_event = dict(event)
    normalized_event["real_interruption"] = qualified_real

    return {
        "interface_version": INTERFACE_VERSION,
        "qualification": qualification,
        "qualified_real_interruption": qualified_real,
        "normalized_event": normalized_event,
        "evidence_checks": checks,
        "evidence_boundary": [
            "RAW_REAL_INTERRUPTION_BOOLEAN_IS_NOT_SELF_VERIFYING",
            "CONTROLLED_OR_SYNTHETIC_EVENTS_CANNOT_SATISFY_REAL_THRESHOLD",
            "QUALIFICATION_DOES_NOT_VERIFY_EXTERNAL_REFERENCE_EXISTENCE",
            "NO_AUTOMATIC_SELF_IMPROVEMENT_PROMOTION",
        ],
    }


def summarize_qualified_records(records: list[dict[str, Any]]) -> dict[str, Any]:
    """Qualify packets first, then reuse SI-0014's advisory interruption summarizer."""
    if not isinstance(records, list):
        raise TypeError("records must be list")

    normalized: list[dict[str, Any]] = []
    qualifications: list[dict[str, Any]] = []
    for record in records:
        if not isinstance(record, dict) or not isinstance(record.get("event"), dict):
            raise ValueError("record.event required")
        result = qualify_interruption_event(record["event"], record.get("evidence"))
        normalized.append(result["normalized_event"])
        qualifications.append(
            {
                "event_id": record["event"].get("event_id"),
                "qualification": result["qualification"],
                "qualified_real_interruption": result["qualified_real_interruption"],
            }
        )

    summary = summarize_events(normalized)
    summary["interface_version"] = INTERFACE_VERSION
    summary["qualification_results"] = qualifications
    summary["genuine_evidence_rule"] = (
        "Only QUALIFIED_REAL_PACKET events may satisfy the real-interruption threshold; "
        "the summary remains advisory and cannot promote a candidate."
    )
    return summary
