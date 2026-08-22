from __future__ import annotations
from dataclasses import dataclass
from collections import deque
from typing import Iterable, Mapping, Optional, Sequence, Tuple


class BusinessIntegrationError(RuntimeError):
    pass


PROOF_ORDER = {"E0": 0, "E1": 1, "E2": 2, "E2_PLUS": 2.5, "E3": 3, "E4": 4, "E5": 5, "E6": 6, "E7": 7}


@dataclass(frozen=True)
class SharedDependencyPassport:
    name: str
    version: str
    sha256: str
    size_bytes: int
    drive_file_id: str
    allowed_capabilities: Tuple[str, ...]
    forbidden_semantics: Tuple[str, ...] = ()


def validate_dependency_passport(p: SharedDependencyPassport) -> bool:
    if not p.name or not p.version or len(p.sha256) != 64 or p.size_bytes <= 0 or not p.drive_file_id:
        raise BusinessIntegrationError("incomplete dependency passport")
    if not p.allowed_capabilities:
        raise BusinessIntegrationError("dependency must expose bounded reusable capabilities")
    return True


@dataclass(frozen=True)
class BusinessArtifact:
    artifact_id: str
    artifact_type: str
    proof_level: str
    locked: bool = False


def proof_transition(current: str, requested: str, *, real_buyer_event: bool = False, real_payment_event: bool = False, public_ceiling: str = "E2_PLUS") -> str:
    if current not in PROOF_ORDER or requested not in PROOF_ORDER or public_ceiling not in PROOF_ORDER:
        raise BusinessIntegrationError("unknown proof level")
    if real_payment_event:
        return "E4"
    if real_buyer_event:
        return "E3"
    return requested if PROOF_ORDER[requested] <= PROOF_ORDER[public_ceiling] else public_ceiling


@dataclass(frozen=True)
class DependencyEdge:
    source: str
    target: str
    edge_type: str


ALLOWED_EDGE_TYPES = {
    "READS", "DERIVES_FROM", "REQUIRES", "INVALIDATES", "CONSTRAINS", "CHANGES", "FINANCES", "DELIVERS", "MEASURES"
}


def build_dependency_index(edges: Sequence[DependencyEdge]) -> Mapping[str, Tuple[str, ...]]:
    out = {}
    tmp = {}
    for e in edges:
        if e.edge_type not in ALLOWED_EDGE_TYPES:
            raise BusinessIntegrationError(f"unknown edge type: {e.edge_type}")
        tmp.setdefault(e.source, []).append(e.target)
    for k, vals in tmp.items():
        out[k] = tuple(sorted(set(vals)))
    return out


def selective_invalidation(index: Mapping[str, Sequence[str]], changed: Iterable[str], locked: Iterable[str] = ()) -> Mapping[str, Tuple[str, ...]]:
    dirty = set(changed)
    blocked = set()
    locked_set = set(locked)
    q = deque(changed)
    while q:
        node = q.popleft()
        for nxt in index.get(node, ()): 
            if nxt in locked_set:
                blocked.add(nxt)
                continue
            if nxt not in dirty:
                dirty.add(nxt)
                q.append(nxt)
    return {"dirty": tuple(sorted(dirty)), "blocked_locked": tuple(sorted(blocked))}


@dataclass(frozen=True)
class FounderLock:
    artifact_id: str
    lock_type: str
    reason: str


def founder_lock_gate(lock: FounderLock, mutation_scope: str) -> bool:
    if not lock.reason.strip():
        raise BusinessIntegrationError("lock requires reason")
    if lock.lock_type == "FOUNDER_LOCKED" and mutation_scope not in {"EVIDENCE_ONLY", "METADATA_ONLY"}:
        raise BusinessIntegrationError("Founder-locked business artifact cannot be silently mutated")
    return True


@dataclass(frozen=True)
class DecisionLineage:
    decision_id: str
    evidence_refs: Tuple[str, ...]
    interpretation: str
    competing_hypothesis: str
    decision: str
    expected_consequence: str
    actual_consequence: Optional[str] = None


def lineage_gate(d: DecisionLineage) -> bool:
    if not d.evidence_refs:
        raise BusinessIntegrationError("decision requires evidence references")
    if any(not x.strip() for x in (d.interpretation, d.competing_hypothesis, d.decision, d.expected_consequence)):
        raise BusinessIntegrationError("decision lineage incomplete")
    return True


@dataclass(frozen=True)
class BusinessTransition:
    signal_id: str
    opportunity_id: str
    experiment_id: Optional[str]
    offer_id: Optional[str]
    contract_id: Optional[str]
    delivery_id: Optional[str]
    economics_id: Optional[str]
    finance_id: Optional[str]
    scale_id: Optional[str]


def transition_completeness(t: BusinessTransition) -> Tuple[str, ...]:
    sequence = (
        ("SIGNAL", t.signal_id),
        ("OPPORTUNITY", t.opportunity_id),
        ("EXPERIMENT", t.experiment_id),
        ("OFFER", t.offer_id),
        ("CONTRACT", t.contract_id),
        ("DELIVERY", t.delivery_id),
        ("ECONOMICS", t.economics_id),
        ("FINANCE", t.finance_id),
        ("SCALE", t.scale_id),
    )
    missing_started = False
    holes = []
    for stage, value in sequence:
        if not value:
            missing_started = True
        elif missing_started:
            holes.append(stage)
    return tuple(holes)


def finance_after_proof(proof_level: str, path: str) -> str:
    if proof_level not in PROOF_ORDER:
        raise BusinessIntegrationError("unknown proof level")
    if PROOF_ORDER[proof_level] < PROOF_ORDER["E4"]:
        return "HOLD_DEMAND_PROOF_REQUIRED"
    return f"READY_TO_ASSESS_{path.upper()}"


def economics_gate(*, revenue_eur: Optional[float], direct_cost_eur: Optional[float], delivery_minutes: Optional[float]) -> Optional[Mapping[str, float]]:
    if revenue_eur is None or direct_cost_eur is None or delivery_minutes is None:
        return None
    if revenue_eur < 0 or direct_cost_eur < 0 or delivery_minutes < 0:
        raise BusinessIntegrationError("observed economics cannot be negative")
    return {
        "revenue_eur": revenue_eur,
        "direct_cost_eur": direct_cost_eur,
        "delivery_minutes": delivery_minutes,
        "contribution_eur": revenue_eur - direct_cost_eur,
    }


def mechanism_disposition(*, semantic_duplicate: bool, current_sufficient: bool, decision_delta: bool) -> str:
    if semantic_duplicate and current_sufficient:
        return "REUSE_CURRENT"
    if semantic_duplicate:
        return "MERGE_DELTA"
    if not decision_delta:
        return "NO_OP"
    return "KEEP_NEW_BOUNDED"


def self_improvement_promotion(*, observed_defect: bool, regression_pass: bool, provenance_bound: bool, readback_pass: bool) -> str:
    if not observed_defect:
        return "PROTECT_NO_CHANGE"
    if regression_pass and provenance_bound and readback_pass:
        return "READY_FOR_BOUNDED_PROMOTION"
    return "HOLD_EVIDENCE_INCOMPLETE"


def compose_profile(profile: str) -> Tuple[str, ...]:
    profiles = {
        "ZERO_CAPITAL": ("ZERO_NEW_FOUNDER_CASH", "BUYER_BEFORE_BUILD", "FINANCE_AFTER_PROOF"),
        "REGULATORY_SHOCK": ("OFFICIAL_SOURCE", "DATE_SEMANTICS", "LIABILITY_BOUNDARY", "PUBLIC_EVIDENCE_CEILING"),
        "CREATIVE_OPPORTUNITY": ("OFFICIAL_SOURCE_FRESHNESS", "ELIGIBILITY_GATE", "PROJECT_BUDGET_NEQ_INCOME"),
        "PUBLIC_ART": ("SITE_CONSTRAINT", "FEE_VS_PRODUCTION_BUDGET", "INSURANCE_HANDOFF", "INSTALLATION_CASH_TIMING"),
        "HOSPITALITY": ("BUYER_WORKFLOW", "CAPEX_VS_SERVICE", "OUTCOME_PROXY_GUARD", "MANUAL_V0"),
        "CONSTRUCTION": ("TENDER_SIGNAL", "SCOPE_LIABILITY", "QUOTE_JOB_DOC_WORKFLOW", "CASH_CONVERSION"),
        "ACQUISITION": ("DEAL_SPECIFIC_ECONOMICS", "DOWNSIDE_FIRST", "CASHFLOW_ASSET", "FINANCE_AFTER_PROOF"),
    }
    key = profile.upper()
    if key not in profiles:
        raise BusinessIntegrationError("unknown business profile")
    return profiles[key]
