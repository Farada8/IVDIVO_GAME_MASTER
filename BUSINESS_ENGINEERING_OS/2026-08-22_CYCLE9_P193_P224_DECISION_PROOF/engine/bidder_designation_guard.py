from dataclasses import dataclass
from typing import Optional, Dict, Any


TEST_FIXTURE_ONLY = "TEST_FIXTURE_ONLY"
ACTUAL_BIDDER = "ACTUAL_BIDDER"


@dataclass(frozen=True)
class BidderDesignationObject:
    resource_id: Optional[str]
    legal_entity_name: Optional[str]
    registration_number: Optional[str]
    designation_mode: Optional[str]
    authorized_designator: Optional[str]
    designated_at: Optional[str]
    designation_scope: Optional[str]
    active: bool = False


def designation_state(obj: BidderDesignationObject) -> Dict[str, Any]:
    """Keep internal fixture identity separate from a real case-specific bidder designation."""
    if not obj.resource_id or not obj.legal_entity_name:
        return {
            "status": "HOLD_MISSING_RESOURCE_OR_ENTITY",
            "explicit_bidder_designation": False,
            "internal_fixture_allowed": False,
        }

    if obj.designation_mode == TEST_FIXTURE_ONLY:
        return {
            "status": "TEST_FIXTURE_ONLY_NOT_BIDDER",
            "explicit_bidder_designation": False,
            "internal_fixture_allowed": True,
            "resource_id": obj.resource_id,
            "legal_entity_name": obj.legal_entity_name,
        }

    if obj.designation_mode != ACTUAL_BIDDER:
        return {
            "status": "HOLD_UNKNOWN_DESIGNATION_MODE",
            "explicit_bidder_designation": False,
            "internal_fixture_allowed": False,
        }

    required = [
        obj.authorized_designator,
        obj.designated_at,
        obj.designation_scope,
        obj.active,
    ]
    if not all(bool(x) for x in required):
        return {
            "status": "HOLD_INCOMPLETE_EXPLICIT_DESIGNATION",
            "explicit_bidder_designation": False,
            "internal_fixture_allowed": False,
        }

    return {
        "status": "EXPLICIT_BIDDER_DESIGNATION_PRESENT",
        "explicit_bidder_designation": True,
        "internal_fixture_allowed": True,
        "resource_id": obj.resource_id,
        "legal_entity_name": obj.legal_entity_name,
        "designation_scope": obj.designation_scope,
    }


def requirement_join_authorized(
    designation: BidderDesignationObject,
    *,
    target_pack_complete: bool,
    bidder_capability_packet_complete: bool,
) -> bool:
    state = designation_state(designation)
    return bool(
        state["explicit_bidder_designation"]
        and target_pack_complete
        and bidder_capability_packet_complete
    )
