from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Iterable

PUBLIC_EVIDENCE_CEILING = "E2+"

class AuthorityState(str, Enum):
    FULL = "FULL"
    PARTIAL = "PARTIAL"
    MISSING = "MISSING"

class GapState(str, Enum):
    MET = "MET"
    UNKNOWN = "UNKNOWN"
    CURABLE_BEFORE_DEADLINE = "CURABLE_BEFORE_DEADLINE"
    NONCURABLE = "NONCURABLE"
    NOT_APPLICABLE = "NOT_APPLICABLE"

class DecisionState(str, Enum):
    REJECT_IRRELEVANT = "REJECT_IRRELEVANT"
    HOLD_MISSING_AUTHORITY = "HOLD_MISSING_AUTHORITY"
    HOLD_CAPABILITY_EVIDENCE = "HOLD_CAPABILITY_EVIDENCE"
    HOLD_REQUIREMENT_GAPS = "HOLD_REQUIREMENT_GAPS"
    HOLD_TECHNICAL_PACKAGE = "HOLD_TECHNICAL_PACKAGE"
    READY_FOR_INDEPENDENT_REVIEW = "READY_FOR_INDEPENDENT_REVIEW"
    READY_FOR_REAL_DECISION_USE_TEST = "READY_FOR_REAL_DECISION_USE_TEST"

@dataclass(frozen=True)
class EvidenceItem:
    field: str
    value: object
    source_id: str | None
    source_class: str
    current: bool = True

@dataclass(frozen=True)
class RequirementClaim:
    key: str
    required: bool
    source_id: str | None
    fatal_if_unmet: bool = False

@dataclass(frozen=True)
class CapabilityClaim:
    key: str
    value: object
    source_id: str | None
    verified: bool = False
    expires_at: str | None = None

@dataclass
class OpportunityCase:
    case_id: str
    relevant: bool = True
    authority: AuthorityState = AuthorityState.MISSING
    profile_complete: bool = False
    technical_package_ready: bool = False
    independent_review_ready: bool = False
    market_grade: str = "E2+"
    blockers: list[str] = field(default_factory=list)

def authority_completeness(required_ids: Iterable[str], present_ids: Iterable[str], *, intentionally_partial: bool = False) -> AuthorityState:
    required, present = set(required_ids), set(present_ids)
    if required and required.issubset(present):
        return AuthorityState.FULL
    if present or intentionally_partial:
        return AuthorityState.PARTIAL
    return AuthorityState.MISSING

def profile_completeness(required_keys: Iterable[str], claims: Iterable[CapabilityClaim]) -> dict:
    verified = {c.key for c in claims if c.verified and c.source_id and c.value not in (None, "", [])}
    missing = sorted(set(required_keys) - verified)
    return {"complete": not missing, "missing": missing}

def join_requirements(requirements: Iterable[RequirementClaim], capabilities: Iterable[CapabilityClaim]) -> list[dict]:
    caps = {c.key: c for c in capabilities}
    out = []
    for req in requirements:
        cap = caps.get(req.key)
        out.append({
            "key": req.key,
            "requirement_source": req.source_id,
            "fatal_if_unmet": req.fatal_if_unmet,
            "capability_value": None if cap is None else cap.value,
            "capability_source": None if cap is None else cap.source_id,
            "capability_verified": False if cap is None else cap.verified,
            "unmatched": cap is None,
        })
    return out

def classify_gap(requirement: RequirementClaim, capability: CapabilityClaim | None, *, can_cure: bool | None = None, deadline_proven: bool = False, not_applicable: bool = False) -> GapState:
    if not_applicable:
        return GapState.NOT_APPLICABLE
    if capability is not None and capability.verified and capability.source_id and bool(capability.value):
        return GapState.MET
    if capability is None or not capability.verified or capability.source_id is None:
        if can_cure is True and deadline_proven:
            return GapState.CURABLE_BEFORE_DEADLINE
        return GapState.UNKNOWN
    if can_cure is True and deadline_proven:
        return GapState.CURABLE_BEFORE_DEADLINE
    if requirement.fatal_if_unmet and can_cure is False:
        return GapState.NONCURABLE
    return GapState.UNKNOWN

def decision_state(case: OpportunityCase, gap_states: Iterable[GapState]) -> DecisionState:
    if not case.relevant:
        return DecisionState.REJECT_IRRELEVANT
    if case.authority is not AuthorityState.FULL:
        return DecisionState.HOLD_MISSING_AUTHORITY
    if not case.profile_complete:
        return DecisionState.HOLD_CAPABILITY_EVIDENCE
    gaps = list(gap_states)
    if any(g in (GapState.UNKNOWN, GapState.NONCURABLE) for g in gaps):
        return DecisionState.HOLD_REQUIREMENT_GAPS
    if not case.technical_package_ready:
        return DecisionState.HOLD_TECHNICAL_PACKAGE
    if not case.independent_review_ready:
        return DecisionState.READY_FOR_INDEPENDENT_REVIEW
    return DecisionState.READY_FOR_REAL_DECISION_USE_TEST

def reason_graph(case: OpportunityCase, gap_states: Iterable[GapState]) -> dict:
    gaps = list(gap_states)
    state = decision_state(case, gaps)
    reasons = []
    if state == DecisionState.REJECT_IRRELEVANT:
        reasons.append("OPPORTUNITY_NOT_RELEVANT")
    if case.authority is not AuthorityState.FULL:
        reasons.append("AUTHORITY_INCOMPLETE")
    if not case.profile_complete:
        reasons.append("CAPABILITY_PROFILE_INCOMPLETE")
    if any(g == GapState.UNKNOWN for g in gaps):
        reasons.append("UNKNOWN_REQUIREMENT_OR_CAPABILITY_GAP")
    if any(g == GapState.NONCURABLE for g in gaps):
        reasons.append("PROVEN_NONCURABLE_GAP")
    if not case.technical_package_ready:
        reasons.append("TECHNICAL_OR_PROPOSAL_PACKAGE_INCOMPLETE")
    if not case.independent_review_ready:
        reasons.append("INDEPENDENT_REVIEW_NOT_READY")
    return {"state": state.value, "reasons": reasons}

BLOCKER_PRIORITY = {
    "AUTHORITY_INCOMPLETE": 0,
    "CAPABILITY_PROFILE_INCOMPLETE": 1,
    "UNKNOWN_REQUIREMENT_OR_CAPABILITY_GAP": 2,
    "PROVEN_NONCURABLE_GAP": 2,
    "TECHNICAL_OR_PROPOSAL_PACKAGE_INCOMPLETE": 3,
    "INDEPENDENT_REVIEW_NOT_READY": 4,
}

def next_evidence_action(reasons: Iterable[str]) -> str:
    reasons = list(reasons)
    if not reasons:
        return "PROTECT_NO_CHANGE"
    blocker = min(reasons, key=lambda r: BLOCKER_PRIORITY.get(r, 99))
    return {
        "AUTHORITY_INCOMPLETE": "ACQUIRE_OR_VERIFY_AUTHORITY",
        "CAPABILITY_PROFILE_INCOMPLETE": "VERIFY_CAPABILITY_PROFILE",
        "UNKNOWN_REQUIREMENT_OR_CAPABILITY_GAP": "CLOSE_SPECIFIC_REQUIREMENT_GAP",
        "PROVEN_NONCURABLE_GAP": "STOP_OR_ROUTE_NO_GO_REVIEW",
        "TECHNICAL_OR_PROPOSAL_PACKAGE_INCOMPLETE": "BUILD_MINIMUM_TECHNICAL_PACKAGE",
        "INDEPENDENT_REVIEW_NOT_READY": "BUILD_BLIND_INDEPENDENT_REVIEW_PACKET",
    }.get(blocker, "PROTECT_NO_CHANGE")

def recurring_missing_authority(cases: Iterable[dict], *, minimum_distinct_cases: int = 2) -> dict:
    case_ids = {x["case_id"] for x in cases if x.get("missing_required_authority")}
    return {
        "distinct_cases": sorted(case_ids),
        "candidate": len(case_ids) >= minimum_distinct_cases,
        "scope": "BUSINESS_ENGINEERING" if len(case_ids) >= minimum_distinct_cases else "OBSERVATION_ONLY",
    }

def proof_invariants(records: Iterable[dict]) -> dict:
    violations = []
    for record in records:
        if record.get("public_only") and record.get("market_grade") not in (None, "E0", "E1", "E2", "E2+"):
            violations.append((record.get("case_id"), "PUBLIC_TO_MARKET_LEAK"))
        if record.get("official_brief_validated") and record.get("applicant_ready") and not record.get("applicant_evidence"):
            violations.append((record.get("case_id"), "OFFICIAL_BRIEF_TO_APPLICANT_READY_LEAK"))
        if record.get("unknown_treated_as_fail"):
            violations.append((record.get("case_id"), "UNKNOWN_AS_FAIL"))
        if record.get("unknown_treated_as_pass"):
            violations.append((record.get("case_id"), "UNKNOWN_AS_PASS"))
    return {"pass": not violations, "violations": violations}
