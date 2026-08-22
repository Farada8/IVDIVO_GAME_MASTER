from dataclasses import dataclass, asdict
from typing import Dict, Any, Tuple


@dataclass(frozen=True)
class BusinessResumeState:
    target_pack_acquired: bool = False
    target_requirement_registry_ready: bool = False
    actual_bidder_designation: bool = False
    authoritative_bidder_packet_ready: bool = False
    frozen_target_manifest: bool = False
    frozen_bidder_manifest: bool = False
    bounded_decision_packet_ready: bool = False
    independent_reviewer_ready: bool = False
    external_interaction_authorized: bool = False
    real_decision_use_ready: bool = False


def _result(route: str, earliest_prompt: int | None, reason: str, state: BusinessResumeState) -> Dict[str, Any]:
    return {
        "route": route,
        "earliest_prompt": earliest_prompt,
        "reason": reason,
        "state": asdict(state),
        "external_action_authorized": False,
        "proof_promotion": False,
    }


def validate_state(s: BusinessResumeState) -> Tuple[bool, str]:
    # Downstream readiness may not exist without upstream authority.
    if s.target_requirement_registry_ready and not s.target_pack_acquired:
        return False, "REGISTRY_WITHOUT_AUTHENTIC_TARGET_PACK"
    if s.authoritative_bidder_packet_ready and not s.actual_bidder_designation:
        return False, "BIDDER_PACKET_WITHOUT_ACTUAL_DESIGNATION"
    if s.frozen_target_manifest and not s.target_requirement_registry_ready:
        return False, "FROZEN_TARGET_WITHOUT_REQUIREMENT_REGISTRY"
    if s.frozen_bidder_manifest and not s.authoritative_bidder_packet_ready:
        return False, "FROZEN_BIDDER_WITHOUT_AUTHORITATIVE_PACKET"
    if s.bounded_decision_packet_ready and not (s.frozen_target_manifest and s.frozen_bidder_manifest):
        return False, "DECISION_PACKET_WITHOUT_BOTH_FROZEN_MANIFESTS"
    if s.independent_reviewer_ready and not s.bounded_decision_packet_ready:
        return False, "REVIEWER_READY_WITHOUT_BOUNDED_DECISION_PACKET"
    if s.real_decision_use_ready and not s.external_interaction_authorized:
        return False, "REAL_USE_WITHOUT_EXPLICIT_EXTERNAL_AUTHORIZATION"
    return True, "VALID"


def route_business_resume(s: BusinessResumeState) -> Dict[str, Any]:
    valid, reason = validate_state(s)
    if not valid:
        return _result("HOLD_INCONSISTENT_STATE", None, reason, s)

    # Both independent roots are absent. There is no deterministic autonomous action:
    # either P225 or P235 may progress only if a new authority event appears.
    if not s.target_pack_acquired and not s.actual_bidder_designation:
        return _result(
            "PROTECT_NO_CHANGE",
            None,
            "NO_NEW_ADMISSIBLE_ROOT_EVENT; WAIT_FOR_P225_OR_P235_AUTHORITY",
            s,
        )

    # Target root has moved: continue only the target processing chain.
    if s.target_pack_acquired and not s.target_requirement_registry_ready:
        return _result("RESUME_P226_P234", 226, "AUTHENTIC_TARGET_PACK_ACQUIRED", s)

    # Bidder root has moved while target remains absent: target acquisition is now the earliest missing root.
    if not s.target_pack_acquired and s.actual_bidder_designation:
        return _result("RESUME_P225", 225, "ACTUAL_BIDDER_DESIGNATED_BUT_TARGET_PACK_MISSING", s)

    # Target registry is ready, but bidder designation is not.
    if s.target_requirement_registry_ready and not s.actual_bidder_designation:
        return _result("RESUME_P235", 235, "TARGET_REGISTRY_READY; ACTUAL_BIDDER_DESIGNATION_MISSING", s)

    # Actual bidder is designated; collect/freeze only authoritative bidder evidence.
    if s.actual_bidder_designation and not s.authoritative_bidder_packet_ready:
        return _result("RESUME_P236_P251", 236, "ACTUAL_BIDDER_DESIGNATED; AUTHORITATIVE_BIDDER_PACKET_INCOMPLETE", s)

    # Both authority chains exist, but manifests are not frozen yet.
    if not (s.frozen_target_manifest and s.frozen_bidder_manifest):
        return _result(
            "HOLD_FREEZE_BOTH_MANIFESTS",
            252,
            "TARGET_AND_BIDDER_AUTHORITY_EXIST_BUT_BOTH_FROZEN_MANIFESTS_REQUIRED",
            s,
        )

    # Atomic join and bounded decision can now proceed.
    if not s.bounded_decision_packet_ready:
        return _result("RESUME_P252_P280", 252, "BOTH_FROZEN_MANIFESTS_PRESENT", s)

    # Independent validation is the next legal layer.
    if not s.independent_reviewer_ready:
        return _result("HOLD_P281_P283_REVIEWER", 281, "REAL_INDEPENDENT_REVIEWER_NOT_PROVEN", s)

    # Reviewer can run P281-P283 internally; external action remains separate.
    if not s.external_interaction_authorized:
        return _result("RESUME_P281_P283_THEN_HOLD_EXTERNAL", 281, "INDEPENDENT_REVIEW_READY; EXTERNAL_AUTHORIZATION_ABSENT", s)

    # External authorization exists, but a real decision-use event has not yet occurred.
    if not s.real_decision_use_ready:
        return _result("RESUME_P284_P287", 284, "EXPLICIT_EXTERNAL_AUTHORIZATION_PRESENT", s)

    # P288 is already consumed; do not repeat it. New frontier must be derived as a new cycle.
    return _result(
        "DERIVE_NEW_FRONTIER_AFTER_REAL_EVIDENCE",
        None,
        "P225_P287_PRECONDITIONS_AND_REAL_USE_COMPLETE; DO_NOT_REEXECUTE_P288",
        s,
    )
