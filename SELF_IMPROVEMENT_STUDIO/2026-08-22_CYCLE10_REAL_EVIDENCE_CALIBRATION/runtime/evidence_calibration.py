#!/usr/bin/env python3
from __future__ import annotations
from typing import Mapping

NULLABLE_MEASURED_FIELDS = {
    "operator_minutes",
    "tool_calls_for_recovery",
    "time_saved_minutes",
    "money_saved",
    "productivity_percent",
    "probability_of_failure_without_guard",
}


def validate_improvement_event(event: Mapping) -> dict:
    errors = []
    if not event.get("event_id"):
        errors.append("event_id")
    if event.get("real_event") is not True:
        errors.append("real_event_true_required")
    roots = event.get("raw_evidence_roots") or []
    if not roots:
        errors.append("raw_evidence_roots")
    if event.get("genuine_interruption_event_count") != 1:
        errors.append("single_raw_interruption_must_count_once")
    slices = event.get("project_slices") or []
    if event.get("distinct_project_recoveries") != len({x.get("project_id") for x in slices if x.get("project_id")}):
        errors.append("project_recovery_count_mismatch")
    if event.get("false_resume") not in (True, False):
        errors.append("false_resume_boolean_required")
    measurement = event.get("measurement") or {}
    for key in NULLABLE_MEASURED_FIELDS:
        if key not in measurement:
            errors.append(f"missing_measurement_field:{key}")
    return {
        "status": "PASS" if not errors else "FAIL_EVENT_CONTRACT",
        "valid": not errors,
        "errors": errors,
    }


def validate_avoided_failure_receipt(receipt: Mapping) -> dict:
    errors = []
    if not receipt.get("receipt_id") or not receipt.get("event_id"):
        errors.append("identity")
    observed = receipt.get("observed_failures_prevented_or_contained") or []
    for row in observed:
        if row.get("observed") is not True:
            errors.append("unobserved_failure_in_observed_list")
        if not row.get("evidence"):
            errors.append("missing_failure_evidence")
    q = receipt.get("recovery_quality") or {}
    if q.get("genuine_event_count") != 1:
        errors.append("event_double_count")
    if q.get("distinct_project_slices", 0) < 1:
        errors.append("project_slice_count")
    wrong = receipt.get("rejected_wrong_resume_paths") or {}
    if wrong.get("count") != len(wrong.get("paths") or []):
        errors.append("wrong_resume_path_count_mismatch")
    economics = receipt.get("economic_metrics") or {}
    for key in ("operator_minutes", "time_saved_minutes", "money_saved", "cost_of_wrong_resume", "roi"):
        if key not in economics:
            errors.append(f"missing_economic_field:{key}")
    return {
        "status": "PASS" if not errors else "FAIL_RECEIPT_CONTRACT",
        "valid": not errors,
        "errors": errors,
    }


def reject_hypothetical_benefit_laundering(*, observed: bool, measured_value, claim_type: str) -> dict:
    if not observed:
        return {"status": "BLOCK_HYPOTHETICAL_BENEFIT", "allowed": False}
    if claim_type.upper() in {"TIME_SAVED", "MONEY_SAVED", "ROI", "PRODUCTIVITY"} and measured_value is None:
        return {"status": "HOLD_UNMEASURED_BENEFIT", "allowed": False}
    return {"status": "PASS_OBSERVED_OR_MEASURED", "allowed": True}


def recovery_progress(*, genuine_event_ids, project_ids, false_resume_count: int, required_events: int = 3, required_projects: int = 2) -> dict:
    events = len(set(genuine_event_ids))
    projects = len(set(project_ids))
    eligible = events >= required_events and projects >= required_projects and false_resume_count == 0
    return {
        "genuine_events": events,
        "distinct_projects": projects,
        "false_resume_count": false_resume_count,
        "eligible_for_promotion_review": eligible,
        "auto_promote": False,
        "status": "ELIGIBLE_FOR_REVIEW" if eligible else "HOLD_RECOVERY_EVIDENCE_GATE",
    }
