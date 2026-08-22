from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from typing import Iterable, Optional, Sequence, Dict, Any


SOURCE_RANK = {
    "CURRENT_CERTIFIED_AUTHORITY": 100,
    "OFFICIAL_INTERFACE_CAPTURE": 80,
    "PRIVATE_PRIMARY": 70,
    "THIRD_PARTY": 30,
    "UNVERIFIED": 10,
}


@dataclass(frozen=True)
class BidderDesignationV2:
    resource_id: Optional[str]
    legal_entity: Optional[str]
    authorized_designator: Optional[str]
    designated_at: Optional[str]
    scope: Optional[str]
    active: bool
    mode: str = "ACTUAL_BIDDER"


def designation_v2_state(obj: BidderDesignationV2) -> dict:
    if obj.mode == "TEST_FIXTURE_ONLY":
        return {"status": "TEST_FIXTURE_ONLY_NOT_BIDDER", "explicit": False}
    required = [obj.resource_id, obj.legal_entity, obj.authorized_designator, obj.designated_at, obj.scope, obj.active]
    if not all(bool(x) for x in required):
        return {"status": "HOLD_INCOMPLETE_EXPLICIT_DESIGNATION", "explicit": False}
    return {"status": "EXPLICIT_BIDDER_DESIGNATION_PRESENT", "explicit": True}


@dataclass(frozen=True)
class IdentityEvidence:
    field: str
    value: Optional[str]
    evidence_id: str
    source_class: str
    observed_at: Optional[str] = None
    current_certified: bool = False


def reconcile_identity_field(field: str, evidence: Iterable[IdentityEvidence]) -> dict:
    items = [e for e in evidence if e.field == field and e.value is not None]
    if not items:
        return {"field": field, "value": None, "status": "UNKNOWN_NO_EVIDENCE"}
    ranked = sorted(items, key=lambda e: SOURCE_RANK.get(e.source_class, 0), reverse=True)
    top_rank = SOURCE_RANK.get(ranked[0].source_class, 0)
    top = [e for e in ranked if SOURCE_RANK.get(e.source_class, 0) == top_rank]
    values = sorted({e.value for e in top})
    if len(values) != 1:
        return {
            "field": field,
            "value": None,
            "status": "CONFLICTING_TOP_AUTHORITY_IDENTITY_EVIDENCE",
            "evidence_ids": [e.evidence_id for e in top],
        }
    winner = top[0]
    return {
        "field": field,
        "value": winner.value,
        "status": "CURRENT_CERTIFIED" if winner.current_certified else "OBSERVED_NOT_CURRENT_CERTIFIED",
        "evidence_id": winner.evidence_id,
        "source_class": winner.source_class,
    }


@dataclass(frozen=True)
class CredentialEvidence:
    credential_type: str
    evidence_id: str
    issued_at: Optional[str]
    expires_at: Optional[str]


def credential_state(item: CredentialEvidence, as_of: str) -> dict:
    if not item.evidence_id:
        return {"status": "UNKNOWN_NO_EVIDENCE"}
    if not item.expires_at:
        return {"status": "UNKNOWN_UNDATED_EXPIRY", "evidence_id": item.evidence_id}
    expiry = datetime.fromisoformat(item.expires_at)
    at = datetime.fromisoformat(as_of)
    if expiry <= at:
        return {"status": "EXPIRED", "evidence_id": item.evidence_id, "expires_at": item.expires_at}
    return {"status": "CURRENT_BY_EXPIRY_FIELD", "evidence_id": item.evidence_id, "expires_at": item.expires_at}


@dataclass(frozen=True)
class CapabilityClaim:
    capability: str
    evidence_id: Optional[str]
    source_class: Optional[str]
    timeframe: Optional[str]
    project_context: Optional[str]
    reviewer_state: Optional[str]


def capability_claim_state(claim: CapabilityClaim) -> dict:
    required = [claim.evidence_id, claim.source_class, claim.timeframe, claim.project_context]
    if not all(bool(x) for x in required):
        return {"status": "UNKNOWN_UNBOUND_CAPABILITY_CLAIM", "capability": claim.capability}
    if claim.reviewer_state not in {"REVIEWED", "INDEPENDENTLY_CORROBORATED"}:
        return {
            "status": "EVIDENCE_BOUND_REVIEW_PENDING",
            "capability": claim.capability,
            "evidence_id": claim.evidence_id,
        }
    return {
        "status": "EVIDENCE_BOUND_REVIEWED_CLAIM",
        "capability": claim.capability,
        "evidence_id": claim.evidence_id,
    }


def target_specific_scope_gate(claim_tags: Sequence[str], target_required_tags: Sequence[str]) -> dict:
    claim = set(claim_tags)
    required = set(target_required_tags)
    missing = sorted(required - claim)
    return {
        "status": "TARGET_SCOPE_MATCH" if not missing else "TARGET_SCOPE_NOT_PROVEN",
        "missing_tags": missing,
        "match": not missing,
    }


@dataclass(frozen=True)
class ReferenceProject:
    evidence_id: str
    project_date: Optional[str]
    scope_tags: Sequence[str]
    role: Optional[str]
    contract_value: Optional[float]
    client_evidence_id: Optional[str]


def reference_project_state(
    ref: ReferenceProject,
    *,
    as_of: str,
    lookback_years: int,
    required_scope_tags: Sequence[str],
) -> dict:
    if ref.project_date:
        event = datetime.fromisoformat(ref.project_date)
        now = datetime.fromisoformat(as_of)
        age_years = (now - event).days / 365.25
        within_lookback = 0 <= age_years <= lookback_years
    else:
        within_lookback = None
    scope = target_specific_scope_gate(ref.scope_tags, required_scope_tags)
    dimensions = {
        "date_within_lookback": within_lookback,
        "scope_match": scope["match"],
        "role_proven": bool(ref.role),
        "value_proven": ref.contract_value is not None,
        "client_evidence_proven": bool(ref.client_evidence_id),
    }
    fully_supported = all(v is True for v in dimensions.values())
    return {"status": "REFERENCE_FULLY_SUPPORTED" if fully_supported else "REFERENCE_PARTIAL", "dimensions": dimensions}


@dataclass(frozen=True)
class WorkforceCapacityEvidence:
    named_personnel_available: Sequence[str]
    subcontractor_intent: Sequence[str]
    current_workload_evidence_id: Optional[str]
    speculative_future_hires: Sequence[str]


def workforce_capacity_state(item: WorkforceCapacityEvidence) -> dict:
    return {
        "named_available_count": len(item.named_personnel_available),
        "subcontractor_intent_count": len(item.subcontractor_intent),
        "current_workload_proven": bool(item.current_workload_evidence_id),
        "speculative_future_hires_count": len(item.speculative_future_hires),
        "speculative_hires_count_as_current_capacity": 0,
        "status": "PARTIAL_CAPACITY_EVIDENCE" if item.named_personnel_available or item.current_workload_evidence_id else "UNKNOWN_CAPACITY",
    }


def privacy_minimized_packet(
    decision_fields: Dict[str, Any],
    *,
    allowed_fields: Sequence[str],
    private_evidence_ids: Sequence[str],
) -> dict:
    allowed = set(allowed_fields)
    exposed = {k: v for k, v in decision_fields.items() if k in allowed}
    evidence_hashes = [sha256(e.encode("utf-8")).hexdigest() for e in private_evidence_ids]
    return {
        "decision_fields": exposed,
        "private_evidence_hashes": evidence_hashes,
        "private_raw_values_exposed": False,
    }
