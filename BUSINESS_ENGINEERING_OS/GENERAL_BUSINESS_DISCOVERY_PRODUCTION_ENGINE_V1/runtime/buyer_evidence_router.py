from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping, Optional, Sequence


BEHAVIOR_LEVELS = ("E0", "E1", "E2", "E3", "E4", "E5", "E6")
ROLE_TYPES = ("USER", "BUYER", "BUDGET_OWNER", "INFLUENCER", "UNKNOWN")
REVIEW_STATES = ("UNREVIEWED", "ACCEPTED", "CONTRADICTED", "STALE", "REJECTED")
ACTIVE_OPPORTUNITIES = ("OPP-33", "OPP-36", "OPP-37")
EXPECTED_SCREENING_SLOTS = 10


@dataclass(frozen=True)
class EvidenceRecord:
    evidence_id: str
    opportunity_id: str
    candidate_id: str
    organization: str
    role_type: str = "UNKNOWN"
    role_verified: bool = False
    source_type: str = "PUBLIC"
    observed_at: str = ""
    behavior_level: str = "E0"
    claim: str = ""
    contradicts: Sequence[str] = ()
    review_state: str = "UNREVIEWED"
    artifact_hash: Optional[str] = None


def validate_screening_queue(opportunity_id: str, candidates: Sequence[str]) -> Mapping[str, object]:
    if opportunity_id not in ACTIVE_OPPORTUNITIES:
        return {"status": "HOLD_UNKNOWN_OPPORTUNITY", "valid": False}
    if len(candidates) != EXPECTED_SCREENING_SLOTS:
        return {"status": "HOLD_SCREENING_QUEUE_MUST_HAVE_10_SLOTS", "valid": False, "count": len(candidates)}
    if len(set(candidates)) != len(candidates):
        return {"status": "HOLD_DUPLICATE_SCREENING_CANDIDATE", "valid": False}
    return {
        "status": "SCREENING_QUEUE_VALID_NOT_BUYER_PROOF",
        "valid": True,
        "opportunity_id": opportunity_id,
        "count": len(candidates),
        "buyer_proof": False,
        "demand_proof": False,
    }


def validate_evidence(record: EvidenceRecord) -> Mapping[str, object]:
    if record.opportunity_id not in ACTIVE_OPPORTUNITIES:
        return {"status": "REJECT_UNKNOWN_OPPORTUNITY", "accepted": False}
    if record.role_type not in ROLE_TYPES:
        return {"status": "REJECT_UNKNOWN_ROLE_TYPE", "accepted": False}
    if record.behavior_level not in BEHAVIOR_LEVELS:
        return {"status": "REJECT_UNKNOWN_BEHAVIOR_LEVEL", "accepted": False}
    if record.review_state not in REVIEW_STATES:
        return {"status": "REJECT_UNKNOWN_REVIEW_STATE", "accepted": False}
    if record.contradicts or record.review_state == "CONTRADICTED":
        return {
            "status": "HOLD_CONTRADICTION_REQUIRES_RESOLUTION",
            "accepted": False,
            "proof_promotion": False,
        }
    if record.review_state in ("STALE", "REJECTED"):
        return {"status": f"HOLD_{record.review_state}", "accepted": False, "proof_promotion": False}
    if record.source_type == "PUBLIC" or record.behavior_level == "E0":
        return {
            "status": "ACCEPT_SCREENING_ONLY",
            "accepted": True,
            "buyer_role_verified": False,
            "demand_proof": False,
            "proof_promotion": False,
        }
    if not record.role_verified and record.role_type in ("BUYER", "BUDGET_OWNER"):
        return {
            "status": "HOLD_BUYER_ROLE_UNVERIFIED",
            "accepted": False,
            "proof_promotion": False,
        }
    if record.behavior_level in ("E1", "E2", "E3", "E4"):
        return {
            "status": "ACCEPT_BEHAVIOR_EVIDENCE_REVIEW_REQUIRED",
            "accepted": True,
            "transaction": False,
            "repeatability": False,
            "proof_promotion": False,
        }
    if record.behavior_level == "E5":
        return {
            "status": "ACCEPT_TRANSACTION_EVIDENCE_REVIEW_REQUIRED",
            "accepted": True,
            "transaction": True,
            "repeatability": False,
            "proof_promotion": False,
        }
    return {
        "status": "ACCEPT_REPEAT_EVIDENCE_REVIEW_REQUIRED",
        "accepted": True,
        "transaction": True,
        "repeatability": True,
        "proof_promotion": False,
    }


def fatal_test_behavior_sufficient(opportunity_id: str, levels: Iterable[str]) -> Mapping[str, object]:
    levels = tuple(levels)
    if opportunity_id not in ACTIVE_OPPORTUNITIES:
        return {"status": "HOLD_UNKNOWN_OPPORTUNITY", "sufficient": False}
    if any(level not in BEHAVIOR_LEVELS for level in levels):
        return {"status": "HOLD_INVALID_BEHAVIOR_LEVEL", "sufficient": False}
    # E1 stated problem alone is deliberately insufficient. At least one E2/E3+ event is required.
    sufficient = any(BEHAVIOR_LEVELS.index(level) >= BEHAVIOR_LEVELS.index("E2") for level in levels)
    return {
        "status": "BEHAVIOR_THRESHOLD_REVIEW_READY" if sufficient else "HOLD_VERBAL_ONLY",
        "sufficient": sufficient,
        "auto_pass_fatal_test": False,
        "proof_promotion": False,
    }


def next_route(*, external_action_authorized: bool = False) -> Mapping[str, object]:
    return {
        "state": "S3_FATAL_TEST_READY",
        "executed_next64": 24,
        "remaining_next64": 40,
        "internal_test_ready": "TEST-37",
        "external_tests": ["TEST-33", "TEST-36"],
        "external_action_authorized": external_action_authorized,
        "next_internal_action": "RUN_TEST_37_INTERNAL_NEGATIVE_CONTROL",
        "proof_promotion": False,
    }
