from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Any, Dict, Iterable, List, Optional, Sequence


@dataclass(frozen=True)
class BidderDesignationV2:
    target_resource_id: str
    legal_entity_name: str
    legal_entity_id: str
    authorized_designator: Optional[str]
    designated_at: Optional[str]
    scope: Optional[str]
    active: bool
    mode: str = "REAL"


@dataclass(frozen=True)
class IdentityEvidence:
    field: str
    value: Optional[str]
    source_id: str
    source_class: str
    authority_rank: int
    observed_at: Optional[str]
    currentness_proven: bool


@dataclass(frozen=True)
class CredentialEvidence:
    credential_type: str
    evidence_id: str
    valid_from: Optional[str]
    expires_at: Optional[str]
    observed_at: Optional[str]


@dataclass(frozen=True)
class CapabilityClaim:
    claim_id: str
    capability: str
    evidence_id: Optional[str]
    source_class: Optional[str]
    observed_from: Optional[str]
    observed_to: Optional[str]
    project_context: Optional[str]
    claim_scope: Optional[str]
    reviewer_state: str


@dataclass(frozen=True)
class ReferenceProject:
    project_id: str
    completion_date: Optional[str]
    role: Optional[str]
    scope_tags: tuple[str, ...]
    contract_value: Optional[float]
    value_source: Optional[str]
    client_provenance: Optional[str]
    completion_proof: Optional[str]


@dataclass(frozen=True)
class WorkforceEvidence:
    person_or_resource_id: str
    role: Optional[str]
    competence_evidence_id: Optional[str]
    available_from: Optional[str]
    available_to: Optional[str]
    current_workload_state: Optional[str]
    source_state: str


def real_designation_state(obj: BidderDesignationV2) -> Dict[str, Any]:
    missing = []
    if not obj.target_resource_id:
        missing.append("target_resource_id")
    if not obj.legal_entity_name or not obj.legal_entity_id:
        missing.append("legal_entity_identity")
    if not obj.authorized_designator:
        missing.append("authorized_designator")
    if not obj.designated_at:
        missing.append("designated_at")
    if not obj.scope:
        missing.append("scope")
    if obj.mode != "REAL":
        missing.append("real_designation_mode")
    if not obj.active:
        missing.append("active")
    if missing:
        return {"status": "HOLD_NO_EXPLICIT_BIDDER_DESIGNATION", "real_designation": False, "missing": missing}
    return {"status": "REAL_BIDDER_DESIGNATION_PRESENT", "real_designation": True, "missing": []}


def resolve_identity(evidence: Sequence[IdentityEvidence]) -> Dict[str, Any]:
    by_field: Dict[str, List[IdentityEvidence]] = {}
    for item in evidence:
        by_field.setdefault(item.field, []).append(item)
    out: Dict[str, Any] = {}
    for field, items in by_field.items():
        admissible = [i for i in items if i.value]
        if not admissible:
            out[field] = {"value": None, "status": "UNKNOWN", "conflicts": []}
            continue
        values = sorted({i.value for i in admissible if i.value})
        max_rank = max(i.authority_rank for i in admissible)
        highest = [i for i in admissible if i.authority_rank == max_rank]
        current_highest = [i for i in highest if i.currentness_proven]
        candidate_set = current_highest or highest
        candidate_values = sorted({i.value for i in candidate_set if i.value})
        if len(candidate_values) == 1:
            chosen = candidate_values[0]
            status = "RESOLVED_CURRENT_AUTHORITY" if current_highest else "RESOLVED_BEST_AVAILABLE_NOT_CURRENT_PROOF"
            out[field] = {"value": chosen, "status": status, "conflicts": [v for v in values if v != chosen]}
        else:
            out[field] = {"value": None, "status": "CONFLICT_UNRESOLVED", "conflicts": candidate_values}
    return out


def _parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def credential_state(credential: CredentialEvidence, at_time: str) -> str:
    now = _parse_iso(at_time)
    start = _parse_iso(credential.valid_from)
    end = _parse_iso(credential.expires_at)
    observed = _parse_iso(credential.observed_at)
    if now is None:
        raise ValueError("at_time is required")
    if start and now < start:
        return "NOT_YET_VALID"
    if end and now > end:
        return "EXPIRED"
    if not end or not observed:
        return "UNDATED_REVALIDATE"
    return "VALID"


def capability_claim_state(claim: CapabilityClaim) -> str:
    if not claim.evidence_id or not claim.source_class:
        return "UNKNOWN_NO_EVIDENCE_BINDING"
    if not claim.claim_scope or not claim.project_context:
        return "PARTIAL_CONTEXT_INCOMPLETE"
    if claim.reviewer_state not in {"VERIFIED", "REVIEWED_PARTIAL"}:
        return "UNKNOWN_REVIEW_PENDING"
    return "VERIFIED_CAPABILITY" if claim.reviewer_state == "VERIFIED" else "PARTIAL_CAPABILITY"


def target_specific_control(*, evidence_tags: Iterable[str], required_tag: str) -> Dict[str, Any]:
    tags = {t.strip().lower() for t in evidence_tags if t}
    required = required_tag.strip().lower()
    if required in tags:
        return {"status": "DIRECT_TAG_MATCH_CANDIDATE", "met": False, "requires_requirement_evidence_join": True}
    return {"status": "NO_TARGET_SPECIFIC_MATCH", "met": False, "requires_requirement_evidence_join": True}


def validate_reference(project: ReferenceProject, *, earliest_completion_date: Optional[str] = None,
                       required_scope_tag: Optional[str] = None, require_third_party_completion: bool = True) -> Dict[str, Any]:
    dimensions: Dict[str, Any] = {
        "date_fit": None,
        "role_present": bool(project.role),
        "scope_fit": None,
        "value_evidenced": project.contract_value is not None and bool(project.value_source),
        "client_provenance": bool(project.client_provenance),
        "completion_proof": bool(project.completion_proof),
    }
    if earliest_completion_date and project.completion_date:
        dimensions["date_fit"] = _parse_iso(project.completion_date) >= _parse_iso(earliest_completion_date)
    if required_scope_tag:
        dimensions["scope_fit"] = required_scope_tag.lower() in {t.lower() for t in project.scope_tags}
    if require_third_party_completion and not project.completion_proof:
        overall = "PARTIAL_REFERENCE_THIRD_PARTY_COMPLETION_UNPROVEN"
    elif False in [v for v in dimensions.values() if isinstance(v, bool)]:
        overall = "REFERENCE_DIMENSION_FAIL"
    else:
        overall = "REFERENCE_DIMENSIONS_RECORDED"
    return {"status": overall, "dimensions": dimensions}


def workforce_capacity_state(resources: Sequence[WorkforceEvidence]) -> Dict[str, Any]:
    verified_current = []
    future_or_intent = []
    for r in resources:
        if r.source_state in {"PLANNED_HIRE", "SUBCONTRACTOR_INTENT"}:
            future_or_intent.append(r.person_or_resource_id)
            continue
        complete = all([r.role, r.competence_evidence_id, r.available_from, r.available_to, r.current_workload_state])
        if complete and r.source_state == "VERIFIED_CURRENT":
            verified_current.append(r.person_or_resource_id)
    return {
        "status": "CURRENT_CAPACITY_EVIDENCE_PRESENT" if verified_current else "HOLD_CURRENT_CAPACITY_UNPROVEN",
        "verified_current": verified_current,
        "future_or_intent_not_counted": future_or_intent,
    }


def privacy_minimized_packet(fields: Dict[str, Dict[str, Any]], allowed_fields: Iterable[str]) -> Dict[str, Any]:
    allowed = set(allowed_fields)
    public: Dict[str, Any] = {}
    private_dependencies: List[str] = []
    for name, payload in fields.items():
        source_state = payload.get("source_state", "UNKNOWN")
        if name in allowed:
            public[name] = {
                "status": payload.get("status"),
                "hash": payload.get("hash"),
                "source_state": source_state,
            }
        if source_state.startswith("PRIVATE_"):
            private_dependencies.append(name)
    return {
        "public_derivative": public,
        "private_dependencies": sorted(private_dependencies),
        "proof_upgrade": False,
    }
