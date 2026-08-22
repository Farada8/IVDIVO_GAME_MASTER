from dataclasses import dataclass
from enum import Enum
from typing import Optional


class HistoricalAnalogUse(str, Enum):
    RETRIEVAL_HINT = "RETRIEVAL_HINT"
    CURRENT_REQUIREMENT = "CURRENT_REQUIREMENT"


IDENTITY_FIELDS = {"legal_name", "legal_form", "formation_activity_code"}
CAPABILITY_FIELDS = {
    "company_number",
    "current_cro_status",
    "tax_clearance",
    "turnover",
    "working_capital",
    "insurance",
    "personnel",
    "references",
    "safety_statement",
    "pscs_capability",
    "roofing_capability",
    "insulation_capability",
}


@dataclass(frozen=True)
class EvidenceBinding:
    field: str
    value: Optional[str]
    source_class: str
    verified: bool
    admissible: bool
    reason: str


def historical_analog_admissible(use: HistoricalAnalogUse) -> bool:
    """Historical tenders may guide retrieval only, never current requirements."""
    return use == HistoricalAnalogUse.RETRIEVAL_HINT


def bind_formation_evidence(field: str, value: Optional[str]) -> EvidenceBinding:
    """Formation documents can verify identity/formational facts, not delivery capability."""
    if field in IDENTITY_FIELDS and value is not None:
        return EvidenceBinding(
            field=field,
            value=value,
            source_class="PRIVATE_PRIMARY_FORMATION_DOC",
            verified=True,
            admissible=True,
            reason="IDENTITY_OR_FORMATION_ONLY",
        )
    return EvidenceBinding(
        field=field,
        value=None,
        source_class="PRIVATE_PRIMARY_FORMATION_DOC",
        verified=False,
        admissible=False,
        reason="FORMATION_DOC_NOT_CAPABILITY_EVIDENCE",
    )


def split_blocker_state(
    *,
    current_pack_complete: bool,
    supplier_identity_verified: bool,
    supplier_capability_complete: bool,
) -> dict:
    authority = "FULL" if current_pack_complete else "INCOMPLETE"
    if supplier_capability_complete:
        supplier = "CAPABILITY_COMPLETE"
    elif supplier_identity_verified:
        supplier = "PARTIAL_IDENTITY_ONLY"
    else:
        supplier = "UNVERIFIED"

    join_unlocked = current_pack_complete and supplier_capability_complete
    if not current_pack_complete:
        state = "HOLD_MISSING_AUTHORITY"
        next_action = "ACQUIRE_COMPLETE_CURRENT_OFFICIAL_PACK"
    elif not supplier_capability_complete:
        state = "HOLD_CAPABILITY_EVIDENCE"
        next_action = "ACQUIRE_VERIFIED_SUPPLIER_CAPABILITY_EVIDENCE"
    else:
        state = "READY_FOR_REQUIREMENT_JOIN"
        next_action = "RUN_REQUIREMENT_BY_REQUIREMENT_JOIN"

    return {
        "authority_side": authority,
        "supplier_side": supplier,
        "requirement_join_unlocked": join_unlocked,
        "state": state,
        "next_action": next_action,
    }


def can_assert_bid_decision(current_pack_complete: bool, supplier_capability_complete: bool) -> bool:
    return bool(current_pack_complete and supplier_capability_complete)
