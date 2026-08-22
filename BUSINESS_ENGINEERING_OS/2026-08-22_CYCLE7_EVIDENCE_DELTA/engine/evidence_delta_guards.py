from dataclasses import dataclass
from typing import Optional, Sequence

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


def resolve_versioned_formation_field(values: Sequence[str]) -> dict:
    """Never collapse conflicting formation-form versions into a current registry fact."""
    distinct = sorted({v for v in values if v})
    if not distinct:
        return {"value": None, "status": "UNKNOWN_NO_FORMATION_VERSION"}
    if len(distinct) == 1:
        return {
            "value": distinct[0],
            "status": "SINGLE_FORMATION_VERSION_NOT_CURRENT_REGISTRY_PROOF",
        }
    return {
        "value": None,
        "status": "CONFLICTING_FORMATION_VERSIONS_FINAL_AUTHORITY_REQUIRED",
        "observed_versions": distinct,
    }


def registry_presence_state(*, listed: bool, active_status_proven: bool = False) -> dict:
    """A public registry/index listing proves presence, not active/inactive legal status."""
    if not listed:
        return {"presence": False, "status": "NOT_OBSERVED"}
    return {
        "presence": True,
        "status": (
            "ACTIVE_STATUS_PROVEN"
            if active_status_proven
            else "PUBLIC_REGISTRY_PRESENCE_ONLY_ACTIVE_STATUS_UNKNOWN"
        ),
    }


SOURCE_PRECEDENCE = {
    "OFFICIAL_FIRST_PARTY_CURRENT": 100,
    "OFFICIAL_FIRST_PARTY_HISTORICAL": 80,
    "PRIVATE_PRIMARY": 70,
    "PUBLIC_REGISTRY_INDEX": 60,
    "THIRD_PARTY_AGGREGATOR": 30,
    "UNVERIFIED_SECONDARY": 10,
}


def resolve_conflicting_source_claims(claims: Sequence[dict]) -> dict:
    """Resolve conflicts by authority class without allowing lower-ranked sources to override."""
    usable = [c for c in claims if c.get("value") is not None and c.get("source_class") in SOURCE_PRECEDENCE]
    if not usable:
        return {"value": None, "status": "UNKNOWN_NO_ADMISSIBLE_CLAIM"}
    ranked = sorted(
        usable,
        key=lambda c: SOURCE_PRECEDENCE[c["source_class"]],
        reverse=True,
    )
    top_rank = SOURCE_PRECEDENCE[ranked[0]["source_class"]]
    top = [c for c in ranked if SOURCE_PRECEDENCE[c["source_class"]] == top_rank]
    top_values = {c["value"] for c in top}
    if len(top_values) > 1:
        return {
            "value": None,
            "status": "CONFLICTING_TOP_AUTHORITY_CLAIMS_REVIEW_REQUIRED",
            "source_class": top[0]["source_class"],
        }
    winning_value = top[0]["value"]
    lower_conflicts = [
        c for c in ranked
        if SOURCE_PRECEDENCE[c["source_class"]] < top_rank and c["value"] != winning_value
    ]
    return {
        "value": winning_value,
        "status": (
            "AUTHORITATIVE_VALUE_WITH_LOWER_SOURCE_CONFLICT"
            if lower_conflicts
            else "AUTHORITATIVE_VALUE"
        ),
        "source_class": top[0]["source_class"],
        "lower_conflict_count": len(lower_conflicts),
    }


def document_route_state(*, route_published: bool, attachment_inventory_recovered: bool) -> dict:
    """A published documents URL is not equivalent to the actual current attachment inventory."""
    if attachment_inventory_recovered:
        return {"route_known": True, "inventory": "RECOVERED", "authority_complete": True}
    if route_published:
        return {
            "route_known": True,
            "inventory": "NOT_RECOVERED",
            "authority_complete": False,
            "status": "DOCUMENT_ROUTE_NEQ_ATTACHMENT_INVENTORY",
        }
    return {"route_known": False, "inventory": "NOT_RECOVERED", "authority_complete": False}


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
