#!/usr/bin/env python3
"""Post-render -> IVDIVO Self-Improvement evidence bridge.

Learning is mechanism-level only. Project story facts remain project-scoped. A project
pilot may emit a candidate event, but domain promotion requires independent real
replication and human evidence.
"""
from __future__ import annotations

from typing import Any, Iterable

from production_control import canonical_hash
from post_render_contracts import promotion_gate

EVIDENCE_CLASSES = {
    "STATIC_CODE",
    "SYNTHETIC_TEST",
    "PRODUCTION_BYTES",
    "HUMAN_REVIEW",
    "PROVIDER_ACCOUNT",
    "MEASURED_ECONOMICS",
    "MARKET_SIGNAL",
}


def normalize_metrics(metrics: dict[str, Any] | None) -> dict[str, Any]:
    metrics = metrics or {}
    out = {
        "provider_spend": metrics.get("provider_spend"),
        "provider_requests": metrics.get("provider_requests"),
        "human_minutes": metrics.get("human_minutes"),
        "rework_cycles": metrics.get("rework_cycles"),
        "accepted_audio_minutes": metrics.get("accepted_audio_minutes"),
        "avoided_rerender_minutes": metrics.get("avoided_rerender_minutes"),
        "false_positive_count": metrics.get("false_positive_count"),
        "manual_override_count": metrics.get("manual_override_count"),
    }
    for field in ("provider_spend", "human_minutes", "accepted_audio_minutes", "avoided_rerender_minutes"):
        value = out[field]
        if value is not None and float(value) < 0:
            raise ValueError(f"NEGATIVE_METRIC:{field}")
    for field in ("provider_requests", "rework_cycles", "false_positive_count", "manual_override_count"):
        value = out[field]
        if value is not None and int(value) < 0:
            raise ValueError(f"NEGATIVE_METRIC:{field}")
    return out


def project_leakage_scan(payload: Any, forbidden_tokens: Iterable[str]) -> dict[str, Any]:
    text = str(payload).lower()
    hits = sorted({token for token in forbidden_tokens if token and token.lower() in text})
    return {"status": "PASS" if not hits else "FAIL_PROJECT_LEAKAGE", "hits": hits}


def build_improvement_event(
    *,
    event_id: str,
    project_id: str,
    mechanism_id: str,
    problem_class: str,
    earliest_failure_layer: str,
    evidence_refs: list[dict[str, Any]],
    candidate_delta: str,
    regression_results: list[dict[str, Any]],
    metrics: dict[str, Any] | None = None,
    synthetic_only: bool = False,
    forbidden_project_tokens: Iterable[str] = (),
) -> dict[str, Any]:
    if not all((event_id, project_id, mechanism_id, problem_class, earliest_failure_layer, candidate_delta)):
        raise ValueError("IMPROVEMENT_EVENT_IDENTITY_MISSING")
    if not evidence_refs:
        raise ValueError("IMPROVEMENT_EVENT_EVIDENCE_REQUIRED")
    bad_classes = [ref.get("evidence_class") for ref in evidence_refs if ref.get("evidence_class") not in EVIDENCE_CLASSES]
    if bad_classes:
        raise ValueError("IMPROVEMENT_EVENT_EVIDENCE_CLASS_INVALID")
    if not regression_results:
        raise ValueError("IMPROVEMENT_EVENT_REGRESSION_REQUIRED")
    failing = [row.get("id") for row in regression_results if row.get("status") not in {"PASS", "EXPECTED_FAIL_CAUGHT"}]
    event = {
        "schema_version": "ivdivo.self_improvement.post_render_event/1.0",
        "event_id": event_id,
        "project_id": project_id,
        "mechanism_id": mechanism_id,
        "problem_class": problem_class,
        "earliest_failure_layer": earliest_failure_layer,
        "evidence_refs": evidence_refs,
        "candidate_delta": candidate_delta,
        "regression_results": regression_results,
        "metrics": normalize_metrics(metrics),
        "synthetic_only": bool(synthetic_only),
        "regression_gate": "PASS" if not failing else "HOLD",
        "promotion_claim": "NONE",
        "learning_scope": "CANDIDATE_MECHANISM_ONLY",
    }
    leakage = project_leakage_scan(
        {
            "mechanism_id": mechanism_id,
            "problem_class": problem_class,
            "earliest_failure_layer": earliest_failure_layer,
            "candidate_delta": candidate_delta,
        },
        forbidden_project_tokens,
    )
    if leakage["status"] != "PASS":
        raise ValueError("PROJECT_STORY_CONTENT_LEAKAGE:" + ",".join(leakage["hits"]))
    event["event_hash"] = canonical_hash(event)
    return event


def reconcile_learning_events(events: Iterable[dict[str, Any]]) -> dict[str, Any]:
    """Cluster duplicate evidence families before counting replication."""
    rows = list(events)
    families: dict[str, list[dict[str, Any]]] = {}
    for event in rows:
        mechanism = str(event.get("mechanism_id") or "UNKNOWN")
        evidence_family = str(event.get("evidence_family") or event.get("project_id") or "UNKNOWN")
        families.setdefault(f"{mechanism}:{evidence_family}", []).append(event)
    independent = []
    duplicates = []
    for key, group in sorted(families.items()):
        best = sorted(group, key=lambda item: (item.get("synthetic_only", True), item.get("regression_gate") != "PASS"))[0]
        independent.append(best)
        if len(group) > 1:
            duplicates.append({"family": key, "count": len(group), "counted_as": 1})
    return {
        "status": "PASS",
        "independent_events": independent,
        "duplicates_collapsed": duplicates,
        "input_count": len(rows),
        "independent_count": len(independent),
    }


def domain_promotion_review(project_results: Iterable[dict[str, Any]]) -> dict[str, Any]:
    result = promotion_gate(project_results)
    result["self_improvement_decision"] = (
        "ACCEPT_DOMAIN_MECHANISM_CANDIDATE_FOR_FOUNDER_REVIEW"
        if result["status"] == "DOMAIN_PROMOTED"
        else "HOLD_FOR_REAL_INDEPENDENT_REPLICATION"
    )
    result["machine_may_change_current_authority"] = False
    return result
