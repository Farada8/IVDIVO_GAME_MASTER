from dataclasses import dataclass
from typing import Optional

IDENTITY_FIELDS = {"legal_name", "legal_form", "formation_activity_code"}


@dataclass(frozen=True)
class EvidenceBinding:
    field: str
    value: Optional[str]
    source_class: str
    verified: bool
    admissible: bool
    reason: str


def bind_formation_evidence(field: str, value: Optional[str]) -> EvidenceBinding:
    """Formation documents verify identity/formational facts, never delivery capability."""
    if field in IDENTITY_FIELDS and value is not None:
        return EvidenceBinding(
            field,
            value,
            "PRIVATE_PRIMARY_FORMATION_DOC",
            True,
            True,
            "IDENTITY_OR_FORMATION_ONLY",
        )
    return EvidenceBinding(
        field,
        None,
        "PRIVATE_PRIMARY_FORMATION_DOC",
        False,
        False,
        "FORMATION_DOC_NOT_CAPABILITY_EVIDENCE",
    )


def split_blocker_state(
    *,
    current_pack_complete: bool,
    supplier_identity_verified: bool,
    supplier_capability_complete: bool,
) -> dict:
    authority = "FULL" if current_pack_complete else "INCOMPLETE"
    supplier = (
        "CAPABILITY_COMPLETE"
        if supplier_capability_complete
        else ("PARTIAL_IDENTITY_ONLY" if supplier_identity_verified else "UNVERIFIED")
    )
    join_unlocked = current_pack_complete and supplier_capability_complete
    if not current_pack_complete:
        state, next_action = (
            "HOLD_MISSING_AUTHORITY",
            "ACQUIRE_COMPLETE_CURRENT_OFFICIAL_PACK",
        )
    elif not supplier_capability_complete:
        state, next_action = (
            "HOLD_CAPABILITY_EVIDENCE",
            "ACQUIRE_VERIFIED_SUPPLIER_CAPABILITY_EVIDENCE",
        )
    else:
        state, next_action = (
            "READY_FOR_REQUIREMENT_JOIN",
            "RUN_REQUIREMENT_BY_REQUIREMENT_JOIN",
        )
    return {
        "authority_side": authority,
        "supplier_side": supplier,
        "requirement_join_unlocked": join_unlocked,
        "state": state,
        "next_action": next_action,
    }


def can_assert_bid_decision(
    current_pack_complete: bool, supplier_capability_complete: bool
) -> bool:
    return bool(current_pack_complete and supplier_capability_complete)
