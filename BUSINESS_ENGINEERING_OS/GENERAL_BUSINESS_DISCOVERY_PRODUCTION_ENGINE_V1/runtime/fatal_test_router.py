from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping


MAX_WIP = 3


@dataclass(frozen=True)
class FatalTest:
    opportunity_id: str
    role: str
    fatal_1: str
    test_id: str
    threshold_declared: bool
    negative_control: str
    external_action_required: bool
    internal_negative_control_ready: bool = False


CURRENT_TESTS = (
    FatalTest(
        opportunity_id="OPP-33",
        role="PRIMARY",
        fatal_1="BUYER_COORDINATION_GAP_EXISTS",
        test_id="TEST-33",
        threshold_declared=True,
        negative_control="OFFICIAL_SEAI_SELF_NAVIGATION_PLUS_DIRECT_INSTALLER",
        external_action_required=True,
    ),
    FatalTest(
        opportunity_id="OPP-36",
        role="PILOT",
        fatal_1="IN_SCOPE_UNRESOLVED_OPERATIONAL_GAP_EXISTS",
        test_id="TEST-36",
        threshold_declared=True,
        negative_control="COMMISSION_GUIDANCE_PLUS_VENDOR_DOCUMENTATION_ONLY",
        external_action_required=True,
    ),
    FatalTest(
        opportunity_id="OPP-37",
        role="PILOT",
        fatal_1="AI_SPECIFIC_INCREMENTAL_GAP_BEYOND_ORDINARY_SEO",
        test_id="TEST-37",
        threshold_declared=True,
        negative_control="ORDINARY_SEO_WEB_AUDIT_SAME_SITE_SAME_WINDOW",
        external_action_required=True,
        internal_negative_control_ready=True,
    ),
)


def validate_portfolio(tests: Iterable[FatalTest] = CURRENT_TESTS) -> Mapping[str, object]:
    tests = tuple(tests)
    if not tests:
        return {"status": "HOLD_EMPTY_PORTFOLIO", "ready": False}
    if len(tests) > MAX_WIP:
        return {"status": "HOLD_WIP_LIMIT_EXCEEDED", "ready": False, "wip_count": len(tests)}
    ids = [t.opportunity_id for t in tests]
    if len(ids) != len(set(ids)):
        return {"status": "HOLD_DUPLICATE_OPPORTUNITY", "ready": False}
    if sum(t.role == "PRIMARY" for t in tests) != 1:
        return {"status": "HOLD_PRIMARY_COUNT", "ready": False}
    if any(not t.threshold_declared for t in tests):
        return {"status": "HOLD_THRESHOLD_NOT_PREDECLARED", "ready": False}
    if any(not t.negative_control for t in tests):
        return {"status": "HOLD_NEGATIVE_CONTROL_MISSING", "ready": False}
    return {
        "status": "FATAL_TEST_PORTFOLIO_READY",
        "ready": True,
        "wip_count": len(tests),
        "state": "S3_FATAL_TEST_READY",
        "proof_promotion": False,
        "market_proof": False,
    }


def route_test(test: FatalTest, *, external_action_authorized: bool, new_behavior_evidence: bool = False) -> Mapping[str, object]:
    portfolio = validate_portfolio()
    if not portfolio.get("ready"):
        return portfolio
    if test.external_action_required and not external_action_authorized:
        if test.internal_negative_control_ready:
            return {
                "status": "RUN_INTERNAL_NEGATIVE_CONTROL_ONLY",
                "test_id": test.test_id,
                "external_action": False,
                "proof_promotion": False,
            }
        return {
            "status": "HOLD_EXTERNAL_ACTION_AUTHORIZATION_REQUIRED",
            "test_id": test.test_id,
            "external_action": False,
            "proof_promotion": False,
        }
    return {
        "status": "EXTERNAL_TEST_AUTHORIZED_NOT_EXECUTED" if not new_behavior_evidence else "BEHAVIOR_EVIDENCE_REQUIRES_REVIEW",
        "test_id": test.test_id,
        "external_action": True,
        "proof_promotion": False,
    }


def next_internal_action() -> Mapping[str, object]:
    routed = [route_test(t, external_action_authorized=False) for t in CURRENT_TESTS]
    internal = [r["test_id"] for r in routed if r["status"] == "RUN_INTERNAL_NEGATIVE_CONTROL_ONLY"]
    return {
        "status": "INTERNAL_WORK_AVAILABLE" if internal else "WAIT_FOR_AUTHORIZATION",
        "tests": internal,
        "external_action_authorized": False,
        "next_block": "P09-P16_TARGETED_TO_CURRENT_WIP",
    }
