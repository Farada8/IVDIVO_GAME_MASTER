from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Optional


GAP_STATES = {"MET", "UNKNOWN", "CURABLE_BEFORE_DEADLINE", "NONCURABLE", "NOT_APPLICABLE"}


@dataclass(frozen=True)
class TenderWorkspace:
    resource_id: str
    authority: str
    ca_unique_id: Optional[str]
    evaluation_mechanism: Optional[str]
    estimated_value_eur: Optional[float]
    clarification_deadline: Optional[str]
    submission_deadline: Optional[str]
    opening_time: Optional[str]
    duration_months: Optional[int]
    source_url: str


@dataclass(frozen=True)
class Attachment:
    title: str
    filename: str
    source_resource_id: str
    addendum_id: Optional[str] = None
    byte_hash: Optional[str] = None
    version: Optional[str] = None


@dataclass
class SupplierClaim:
    field: str
    value: Any
    source_ref: Optional[str] = None
    expiry: Optional[str] = None


@dataclass
class EvidenceObject:
    grade: str
    user_class: Optional[str] = None
    before_decision: Optional[str] = None
    after_decision: Optional[str] = None
    interaction_artifact: Optional[str] = None
    timestamp: Optional[str] = None
    behavioral_commitment: Optional[str] = None
    cash_received_eur: Optional[float] = None
    transaction_ref: Optional[str] = None


def target_pack_status(workspace: TenderWorkspace, attachments: Optional[Iterable[Attachment]]) -> dict:
    items = list(attachments or [])
    if not workspace.resource_id:
        return {"pack_complete": False, "status": "NO_TARGET_ID", "count": 0}
    if not items:
        return {
            "pack_complete": False,
            "status": "BLOCKED_INCOMPLETE_TARGET_PACK",
            "count": 0,
            "resource_id": workspace.resource_id,
        }
    wrong = [a for a in items if a.source_resource_id != workspace.resource_id]
    if wrong:
        return {
            "pack_complete": False,
            "status": "NON_TARGET_ATTACHMENTS_REJECTED",
            "count": len(items),
            "wrong_resource_count": len(wrong),
        }
    return {"pack_complete": True, "status": "TARGET_INVENTORY_PRESENT", "count": len(items)}


def benchmark_fixture(target_resource_id: str, benchmark_resource_id: str, attachments: Iterable[Attachment]) -> dict:
    items = list(attachments)
    if target_resource_id == benchmark_resource_id:
        return {"valid_fixture": False, "target_promoted": False, "reason": "BENCHMARK_EQUALS_TARGET"}
    valid = bool(items) and all(a.source_resource_id == benchmark_resource_id for a in items)
    return {
        "valid_fixture": valid,
        "target_promoted": False,
        "inventory_count": len(items),
        "reason": "BENCHMARK_FIXTURE_ONLY" if valid else "INVALID_BENCHMARK_INVENTORY",
    }


def lineage_object(records: list[dict]) -> dict:
    return {
        "records": records,
        "relation": "POSSIBLE_PROJECT_LINEAGE" if len(records) > 1 else "SINGLE_RECORD",
        "requirements_carried_over": False,
    }


def authority_gap_certificate(target_id: str, missing: list[str], blocked_decisions: list[str]) -> dict:
    return {
        "target_resource_id": target_id,
        "missing_objects": sorted(set(missing)),
        "blocked_decisions": sorted(set(blocked_decisions)),
        "status": "HOLD_INSUFFICIENT_AUTHORITY" if missing else "NO_AUTHORITY_GAP",
    }


def bind_supplier_claim(claim: SupplierClaim) -> dict:
    if claim.value is None:
        return {"accepted": False, "state": "NULL"}
    if not claim.source_ref:
        return {"accepted": False, "state": "UNSOURCED_REJECTED"}
    return {"accepted": True, "state": "SOURCE_BOUND", "expiry": claim.expiry}


def route_requirement_gap(requirement_present: bool, supplier_evidence_present: bool, curable: bool = False,
                          before_deadline: bool = False, not_applicable: bool = False) -> str:
    if not_applicable:
        return "NOT_APPLICABLE"
    if not requirement_present or not supplier_evidence_present:
        if requirement_present and curable and before_deadline:
            return "CURABLE_BEFORE_DEADLINE"
        return "UNKNOWN"
    return "MET"


def requirement_join(pack_complete: bool, supplier_verified: bool, requirements: list[dict], claims: list[SupplierClaim]) -> dict:
    if not pack_complete or not supplier_verified:
        return {"ready": False, "status": "BLOCKED_INPUT_AUTHORITY", "joined": []}
    sourced_claims = {c.field: c for c in claims if bind_supplier_claim(c)["accepted"]}
    joined = []
    for req in requirements:
        field = req.get("field")
        joined.append({"field": field, "gap": "MET" if field in sourced_claims else "UNKNOWN"})
    return {"ready": True, "status": "JOINED", "joined": joined}


def critical_path(workspace: TenderWorkspace, internal_decision_deadline: Optional[str] = None) -> dict:
    return {
        "clarification_deadline": workspace.clarification_deadline,
        "submission_deadline": workspace.submission_deadline,
        "opening_time": workspace.opening_time,
        "internal_decision_deadline": internal_decision_deadline,
        "dates_conflated": False,
        "demand_proven": False,
    }


def evaluation_detail(workspace: TenderWorkspace, weights: Optional[dict] = None, price_rule: Optional[str] = None) -> dict:
    if workspace.evaluation_mechanism and not weights:
        return {"mechanism": workspace.evaluation_mechanism, "weights": None, "price_rule": price_rule,
                "numeric_score_allowed": False, "status": "PACK_OR_CLARIFICATION_REQUIRED"}
    return {"mechanism": workspace.evaluation_mechanism, "weights": weights, "price_rule": price_rule,
            "numeric_score_allowed": bool(weights)}


def finance_object(estimated_value_eur: Optional[float], payment_terms=None, retention=None, bonds=None, insurance=None) -> dict:
    return {
        "estimated_value_eur": estimated_value_eur,
        "payment_terms": payment_terms,
        "retention": retention,
        "bonds": bonds,
        "insurance": insurance,
        "margin": None,
        "cash_need": None,
    }


def bid_burden(document_count: Optional[int], team_hours: Optional[float], hourly_cost: Optional[float]) -> dict:
    if document_count is None or team_hours is None:
        return {"observed": False, "hours": None, "cost": None}
    cost = None if hourly_cost is None else team_hours * hourly_cost
    return {"observed": True, "hours": team_hours, "cost": cost, "document_count": document_count}


def pa4_gate(pack_complete: bool, supplier_verified: bool, independent_reviewer: bool, blinded: bool) -> dict:
    ok = pack_complete and supplier_verified and independent_reviewer and blinded
    return {"pa4": ok, "status": "PA4" if ok else "HOLD_NO_INDEPENDENT_COMPLETE_PACKET"}


def substitution_matrix(classes: dict[str, list[str]], residual_job: Optional[str]) -> dict:
    return {"classes": classes, "residual_job": residual_job, "paid_value_proven": False,
            "route": "TEST_RESIDUAL" if residual_job else "HOLD_RESHAPE"}


def field_half_life_policy() -> dict:
    return {
        "deadline_status_addenda": "HIGHEST_REFRESH_PRIORITY",
        "pack_revision": "REVALIDATE_BEFORE_DECISION",
        "method_policy": "LOWER_FREQUENCY",
        "is_policy_not_truth": True,
    }


def immutable_refresh(history: list[dict], observation: dict) -> list[dict]:
    out = [dict(x) for x in history]
    out.append(dict(observation))
    return out


def false_confidence_guard(*, contract_value_present: bool, polished: bool, pack_complete: bool,
                           supplier_verified: bool) -> dict:
    return {
        "proof_upgraded": False,
        "pa4": False if not (pack_complete and supplier_verified) else None,
        "value_or_polish_ignored_for_proof": contract_value_present or polished,
    }


def wip_gate(active: list[str], cap: int = 3) -> dict:
    return {"active": active[:cap], "frozen": active[cap:], "bounded": len(active[:cap]) <= cap}


def pareto_protect_no_change(lanes: list[dict]) -> dict:
    decisive = [x for x in lanes if x.get("decisive_delta")]
    return {"route": "REROUTE" if decisive else "PROTECT_NO_CHANGE", "magic_score": None}


def si_candidate(defect: str, distinct_cases: list[str]) -> dict:
    unique = sorted(set(distinct_cases))
    return {"defect": defect, "cases": unique, "candidate": len(unique) >= 2, "auto_promoted": False}


def independent_review_protocol(reviewer_class: Optional[str], blinded: bool, target_packet_hash: Optional[str],
                                supplier_packet_hash: Optional[str], first_output_hidden: bool) -> dict:
    ready = all([reviewer_class, blinded, target_packet_hash, supplier_packet_hash, first_output_hidden])
    return {"ready": bool(ready), "divergence_log_required": True, "same_packet_required": True}


def pa5_evidence(obj: EvidenceObject) -> dict:
    required = [obj.user_class, obj.before_decision, obj.after_decision, obj.interaction_artifact, obj.timestamp]
    return {"pa5": all(bool(x) for x in required), "generated_scenario_acceptable": False}


def e3_evidence(obj: EvidenceObject) -> dict:
    return {"e3": pa5_evidence(obj)["pa5"] and bool(obj.behavioral_commitment), "compliment_sufficient": False}


def e4_evidence(obj: EvidenceObject) -> dict:
    return {"e4": e3_evidence(obj)["e3"] and bool(obj.cash_received_eur and obj.cash_received_eur > 0) and bool(obj.transaction_ref),
            "listed_price_sufficient": False}


def authority_pointer_fresh(main_sha: str, pointer_known_merges: list[str]) -> dict:
    return {"fresh": main_sha in pointer_known_merges, "status": "FRESH" if main_sha in pointer_known_merges else "STOP_RECONCILE"}


def evidence_ceiling(public_only: bool = True) -> dict:
    return {"max_market_grade": "E2_PLUS" if public_only else None, "e3": False if public_only else None,
            "e4": False if public_only else None}
