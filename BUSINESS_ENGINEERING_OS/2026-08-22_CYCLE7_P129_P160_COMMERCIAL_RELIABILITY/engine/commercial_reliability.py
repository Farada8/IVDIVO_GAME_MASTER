from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Iterable

PUBLIC_CEILING = "E2+"


def residual_job(proposed_jobs: set[str], alternatives: Iterable[dict]) -> dict:
    covered: set[str] = set()
    for alt in alternatives:
        if alt.get("available") and alt.get("class") in {"PUBLIC", "FREE", "VENDOR", "INTERNAL", "CONSULTANT"}:
            covered.update(alt.get("jobs", []))
    residual = sorted(proposed_jobs - covered)
    return {
        "covered": sorted(covered),
        "residual": residual,
        "paid_residual_proven": False,
        "status": "RESIDUAL_JOB_EXISTS" if residual else "HOLD_ZERO_RESIDUAL_JOB",
    }


def decision_utility(before: Any, after: Any, *, real_user: bool) -> dict:
    if not real_user or before is None or after is None:
        return {"decision_delta": None, "status": "HOLD_REAL_DECISION_DELTA"}
    return {"decision_delta": before != after, "status": "OBSERVED_REAL_USER"}


def external_price_gate(price: float | None, *, external_signal: bool) -> dict:
    if price is None or not external_signal:
        return {"price": None, "status": "HOLD_NO_EXTERNAL_PRICE_SIGNAL"}
    return {"price": price, "status": "EXTERNAL_PRICE_SIGNAL"}


def behavior_first_record(*, past_event: str | None, actual_spend: float | None, hypothetical: bool = False) -> dict:
    if hypothetical or not past_event:
        return {"valid_for_discovery": False, "status": "HOLD_NOT_PAST_BEHAVIOR"}
    return {"valid_for_discovery": True, "actual_spend": actual_spend, "status": "PAST_BEHAVIOR_RECORDED"}


def legal_handoff(field: str, source_pointer: str | None, ambiguity: str | None) -> dict:
    blocked = bool(ambiguity)
    return {
        "field": field,
        "source_pointer": source_pointer,
        "ambiguity": ambiguity,
        "human_review_required": blocked,
        "status": "HUMAN_HANDOFF" if blocked else "NO_HANDOFF",
    }


def credential_state(*, source: str | None, issuer: str | None, verified_at: str | None, expires_at: str | None) -> str:
    if not source or not issuer or not verified_at:
        return "UNKNOWN"
    if not expires_at:
        return "REVALIDATE_HOLD"
    return "VERIFIED_WITH_EXPIRY"


def supplier_identity_state(identity_verified: bool, capability_fields_verified: int) -> str:
    if not identity_verified:
        return "UNVERIFIED_IDENTITY"
    if capability_fields_verified <= 0:
        return "PARTIAL_IDENTITY_ONLY"
    return "PARTIAL_CAPABILITY"  # never means tender eligibility


def negative_relevance_filter(*, category_match: bool, scope_match: bool, geography_match: bool) -> str:
    if not category_match or not scope_match or not geography_match:
        return "REJECT_OBVIOUS_IRRELEVANCE"
    return "PASS_TO_FULL_QUALIFICATION_NOT_ELIGIBILITY"


def stale_status_guard(*, label: str, deadline_passed: bool) -> str:
    if label.upper() == "OPEN" and deadline_passed:
        return "REVALIDATE_STATUS"
    return "NO_CONTRADICTION"


def lane_unlock(required_packet_id: str | None) -> str:
    return "UNLOCK_FOR_PROCESSING" if required_packet_id else "HOLD_REAL_INPUT"


def minimize_private_record(payload: dict, required_fields: set[str]) -> dict:
    return {k: payload[k] for k in required_fields if k in payload}


def public_safe_derivative(payload: dict, sensitive_fields: set[str], verified_fields: set[str]) -> dict:
    out = {}
    for k, v in payload.items():
        if k in sensitive_fields:
            out[k] = "PRIVATE_VERIFIED" if k in verified_fields else "PRIVATE_UNVERIFIED"
        else:
            out[k] = v
    return out


def decision_value_vector(*, decision_delta: bool | None, human_minutes: float | None, observed_errors: int | None, next_action_clear: bool | None) -> dict:
    return {
        "decision_delta": decision_delta,
        "human_minutes": human_minutes,
        "observed_errors": observed_errors,
        "next_action_clarity": next_action_clear,
        "total_score": None,
    }


def cash_gap(*, required_outflow: float | None, payment_received_before_outflow: float | None) -> float | None:
    if required_outflow is None or payment_received_before_outflow is None:
        return None
    return max(0.0, required_outflow - payment_received_before_outflow)


def contribution_margin(*, external_price: float | None, variable_cost: float | None, observed_delivery_hours: float | None, labor_rate: float | None) -> float | None:
    if None in (external_price, variable_cost, observed_delivery_hours, labor_rate):
        return None
    return float(external_price) - float(variable_cost) - float(observed_delivery_hours) * float(labor_rate)


def service_capacity(*, available_human_hours: float | None, observed_hours_per_delivery: float | None) -> float | None:
    if available_human_hours is None or observed_hours_per_delivery in (None, 0):
        return None
    return available_human_hours / observed_hours_per_delivery


def artifact_identity(*, source_identity: str | None, schema_version: str, artifact_version: str, reviewer: str | None, generated_at: str, readback_at: str | None) -> dict:
    complete = all([source_identity, schema_version, artifact_version, generated_at, readback_at])
    return {
        "source_identity": source_identity,
        "schema_version": schema_version,
        "artifact_version": artifact_version,
        "reviewer": reviewer,
        "generated_at": generated_at,
        "readback_at": readback_at,
        "status": "IDENTITY_COMPLETE" if complete else "IDENTITY_INCOMPLETE",
    }


@dataclass(frozen=True)
class Edge:
    src: str
    dst: str
    relation: str


def provenance_path(edges: list[Edge], start: str, end: str) -> bool:
    adjacency: dict[str, set[str]] = {}
    for e in edges:
        adjacency.setdefault(e.src, set()).add(e.dst)
    seen = {start}
    stack = [start]
    while stack:
        node = stack.pop()
        if node == end:
            return True
        for nxt in adjacency.get(node, set()):
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False


def persistence_state(*, github_written: bool, drive_written: bool, readback_verified: bool) -> str:
    if github_written and drive_written and readback_verified:
        return "READBACK_VERIFIED"
    if github_written or drive_written:
        return "PARTIAL_FAILURE"
    return "NOT_WRITTEN"


def authority_promotion_gate(*, ci_green: bool, unresolved_review_threads: int, drive_readback: bool, fresh_main_reconciled: bool) -> str:
    ok = ci_green and unresolved_review_threads == 0 and drive_readback and fresh_main_reconciled
    return "PROMOTION_ELIGIBLE" if ok else "STOP_RECONCILE"


def next_frontier(*, full_target_pack: bool, verified_supplier_packet: bool, independent_pa4: bool, real_user_interaction: bool) -> str:
    if not full_target_pack:
        return "ACQUIRE_CURRENT_TARGET_PACK"
    if not verified_supplier_packet:
        return "ACQUIRE_VERIFIED_SUPPLIER_PACKET"
    if not independent_pa4:
        return "RUN_ATOMIC_JOIN_AND_INDEPENDENT_PA4"
    if not real_user_interaction:
        return "RUN_SMALLEST_REAL_DECISION_USE_TEST"
    return "EVALUATE_PA5_E3_WITH_REAL_EVIDENCE"
