from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class DocumentRouteEvidence:
    resource_id: str
    route_known: bool
    inventory_acquired: bool = False
    authenticated_or_user_provided: bool = False

    @property
    def pack_acquired(self) -> bool:
        return self.inventory_acquired

    @property
    def state(self) -> str:
        if self.inventory_acquired:
            return "PACK_ACQUIRED"
        if self.route_known:
            return "DOCUMENT_ROUTE_KNOWN_ATTACHMENT_INVENTORY_NOT_ACQUIRED"
        return "DOCUMENT_ROUTE_UNKNOWN"


@dataclass(frozen=True)
class BidderDesignation:
    case_id: str
    bidder_name: Optional[str] = None
    provenance_id: Optional[str] = None

    @property
    def designated(self) -> bool:
        return bool(self.bidder_name and self.provenance_id)


@dataclass
class SupplierEvidencePacket:
    bidder_name: Optional[str] = None
    evidence: Dict[str, Any] = field(default_factory=dict)

    def verified(self, field_name: str) -> Optional[Any]:
        value = self.evidence.get(field_name)
        return value if value not in (None, "", [], {}) else None

    @property
    def has_capability_evidence(self) -> bool:
        capability_fields = {
            "tax_clearance",
            "insurance",
            "financial_capacity",
            "hs_competence",
            "personnel",
            "references",
            "current_capacity",
        }
        return any(self.verified(name) is not None for name in capability_fields)


@dataclass(frozen=True)
class RequirementRow:
    requirement_id: str
    mandatory: bool
    supplier_state: str = "UNKNOWN"


ALLOWED_JOIN_STATES = {
    "MET",
    "UNKNOWN",
    "CURABLE_BEFORE_DEADLINE",
    "NONCURABLE",
    "NOT_APPLICABLE",
}


def content_hash(content: Optional[bytes]) -> Optional[str]:
    if content is None:
        return None
    return sha256(content).hexdigest()


def indexed_absence_claim(index_results_found: bool) -> str:
    if index_results_found:
        return "INDEX_RESULT_PRESENT"
    return "DOCUMENT_EXISTENCE_UNKNOWN"


def benchmark_may_satisfy_target(benchmark_resource_id: str, target_resource_id: str) -> bool:
    return benchmark_resource_id == target_resource_id


def bidder_bound_identity(
    designation: BidderDesignation, company_name: Optional[str]
) -> bool:
    return bool(
        designation.designated
        and company_name
        and designation.bidder_name == company_name
    )


def bind_supplier_field(
    designation: BidderDesignation,
    company_name: Optional[str],
    evidence_value: Any,
) -> Optional[Any]:
    if not bidder_bound_identity(designation, company_name):
        return None
    if evidence_value in (None, "", [], {}):
        return None
    return evidence_value


def target_authority_ready(route: DocumentRouteEvidence) -> bool:
    return route.pack_acquired


def bidder_authority_ready(
    designation: BidderDesignation, packet: SupplierEvidencePacket
) -> bool:
    return bool(
        designation.designated
        and packet.bidder_name == designation.bidder_name
        and packet.has_capability_evidence
    )


def join_precondition_state(
    route: DocumentRouteEvidence,
    designation: BidderDesignation,
    packet: SupplierEvidencePacket,
) -> str:
    target_ready = target_authority_ready(route)
    bidder_ready = bidder_authority_ready(designation, packet)
    if target_ready and bidder_ready:
        return "READY_FOR_ATOMIC_JOIN"
    if not target_ready and not bidder_ready:
        return "BLOCKED_TARGET_AND_BIDDER_AUTHORITY"
    if not target_ready:
        return "BLOCKED_TARGET_AUTHORITY"
    return "BLOCKED_BIDDER_AUTHORITY"


def validate_join_state(state: str) -> str:
    if state not in ALLOWED_JOIN_STATES:
        raise ValueError(f"unsupported join state: {state}")
    return state


def fatal_gap_ids(rows: Iterable[RequirementRow]) -> List[str]:
    return [
        row.requirement_id
        for row in rows
        if row.mandatory and row.supplier_state == "NONCURABLE"
    ]


def unknown_ids(rows: Iterable[RequirementRow]) -> List[str]:
    return [row.requirement_id for row in rows if row.supplier_state == "UNKNOWN"]


def bounded_decision(
    join_ready: bool,
    rows: Iterable[RequirementRow],
) -> str:
    rows = list(rows)
    if not join_ready or not rows:
        return "HOLD_PRECONDITIONS_NOT_MET"
    if unknown_ids(rows):
        return "HOLD_UNKNOWN_REQUIREMENTS"
    if fatal_gap_ids(rows):
        return "NO_BID_CANDIDATE_REQUIRES_PA4"
    return "BID_CANDIDATE_REQUIRES_PA4"


def dependency_cut_set(
    route: DocumentRouteEvidence,
    designation: BidderDesignation,
    packet: SupplierEvidencePacket,
) -> List[str]:
    blockers: List[str] = []
    if not route.pack_acquired:
        blockers.append("ROOT_A_TARGET_PACK_NOT_ACQUIRED")
    if not designation.designated:
        blockers.append("ROOT_B_NO_EXPLICIT_BIDDER_DESIGNATION")
    elif not bidder_authority_ready(designation, packet):
        blockers.append("ROOT_B_BIDDER_PACKET_INCOMPLETE")
    return blockers


def acquisition_next_action(route: DocumentRouteEvidence) -> str:
    if route.pack_acquired:
        return "BUILD_TARGET_FILE_MANIFEST"
    if route.route_known:
        return "AUTHENTICATED_EXPORT_OR_USER_PROVIDED_OFFICIAL_PACK"
    return "DISCOVER_OFFICIAL_DOCUMENT_ROUTE"


def bidder_next_action(designation: BidderDesignation) -> str:
    if designation.designated:
        return "ACQUIRE_BIDDER_PRIMARY_EVIDENCE"
    return "OBTAIN_EXPLICIT_CASE_SPECIFIC_BIDDER_DESIGNATION"


def proof_frontier() -> Dict[str, Any]:
    return {
        "public_ceiling": "E2+",
        "pa4": False,
        "pa5": False,
        "e3": False,
        "e4": False,
        "wtp": None,
        "price": None,
        "profitability": None,
    }


def protect_no_change(route: DocumentRouteEvidence, designation: BidderDesignation) -> bool:
    return not route.pack_acquired or not designation.designated
