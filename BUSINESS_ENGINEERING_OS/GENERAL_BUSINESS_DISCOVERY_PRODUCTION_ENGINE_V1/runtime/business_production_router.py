from dataclasses import dataclass
from enum import Enum


class Route(str, Enum):
    RESTORE = "RESTORE"
    DISCOVER = "DISCOVER"
    QUALIFY = "QUALIFY"
    TEST_FATAL = "TEST_FATAL"
    BOUND_VALUE = "BOUND_VALUE"
    BUILD_OFFER = "BUILD_OFFER"
    BOUND_ECONOMICS = "BOUND_ECONOMICS"
    PREPARE_SALES_TEST = "PREPARE_SALES_TEST"
    WAIT_EXTERNAL_EVIDENCE = "WAIT_EXTERNAL_EVIDENCE"
    PROCESS_TRANSACTION = "PROCESS_TRANSACTION"
    PROVE_DELIVERY = "PROVE_DELIVERY"
    PROVE_REPEATABILITY = "PROVE_REPEATABILITY"
    SCALE_GATE = "SCALE_GATE"
    HOLD = "HOLD"
    KILL = "KILL"


@dataclass(frozen=True)
class BusinessState:
    authority_restored: bool = False
    opportunity_defined: bool = False
    micro_market_defined: bool = False
    buyer_problem_defined: bool = False
    fatal_assumption_identified: bool = False
    fatal_test_result: str | None = None  # PASS / FAIL / AMBIGUOUS
    measurable_value_hypothesis: bool = False
    offer_testable: bool = False
    economics_bounded: bool = False
    external_action_authorized: bool = False
    sales_test_packet_ready: bool = False
    buyer_behavior_observed: bool = False
    transaction_evidence: bool = False
    delivery_accepted: bool = False
    repeatability_evidence: bool = False
    scale_constraints_bounded: bool = False
    specialist_blocker: bool = False
    explicit_kill: bool = False


def route(state: BusinessState) -> dict:
    if state.explicit_kill:
        return {"route": Route.KILL.value, "reason": "EXPLICIT_KILL", "proof_promotion": False}
    if state.specialist_blocker:
        return {"route": Route.HOLD.value, "reason": "SPECIALIST_DEPENDENCY_BLOCKER", "proof_promotion": False}
    if not state.authority_restored:
        return {"route": Route.RESTORE.value, "reason": "CURRENT_AUTHORITY_NOT_RESTORED", "proof_promotion": False}
    if not state.opportunity_defined:
        return {"route": Route.DISCOVER.value, "reason": "NO_NORMALIZED_OPPORTUNITY", "proof_promotion": False}
    if not (state.micro_market_defined and state.buyer_problem_defined):
        return {"route": Route.QUALIFY.value, "reason": "BUYER_OR_MICROMARKET_INCOMPLETE", "proof_promotion": False}
    if not state.fatal_assumption_identified:
        return {"route": Route.TEST_FATAL.value, "reason": "FATAL_ASSUMPTION_NOT_IDENTIFIED", "proof_promotion": False}
    if state.fatal_test_result == "FAIL":
        return {"route": Route.KILL.value, "reason": "FATAL_ASSUMPTION_FAILED", "proof_promotion": False}
    if state.fatal_test_result in (None, "AMBIGUOUS"):
        return {"route": Route.TEST_FATAL.value, "reason": "FATAL_TEST_NOT_DECISIVE", "proof_promotion": False}
    if not state.measurable_value_hypothesis:
        return {"route": Route.BOUND_VALUE.value, "reason": "VALUE_NOT_MEASURABLE", "proof_promotion": False}
    if not state.offer_testable:
        return {"route": Route.BUILD_OFFER.value, "reason": "OFFER_NOT_TESTABLE", "proof_promotion": False}
    if not state.economics_bounded:
        return {"route": Route.BOUND_ECONOMICS.value, "reason": "UNIT_ECONOMICS_OR_CASH_UNBOUNDED", "proof_promotion": False}
    if not state.sales_test_packet_ready:
        return {"route": Route.PREPARE_SALES_TEST.value, "reason": "SALES_EXPERIMENT_NOT_READY", "proof_promotion": False}
    if not state.external_action_authorized:
        return {"route": Route.WAIT_EXTERNAL_EVIDENCE.value, "reason": "EXTERNAL_ACTION_NOT_AUTHORIZED", "proof_promotion": False}
    if not state.buyer_behavior_observed:
        return {"route": Route.WAIT_EXTERNAL_EVIDENCE.value, "reason": "NO_REAL_BUYER_BEHAVIOR", "proof_promotion": False}
    if not state.transaction_evidence:
        return {"route": Route.PROCESS_TRANSACTION.value, "reason": "BUYER_SIGNAL_WITHOUT_TRANSACTION", "proof_promotion": False}
    if not state.delivery_accepted:
        return {"route": Route.PROVE_DELIVERY.value, "reason": "TRANSACTION_WITHOUT_ACCEPTED_DELIVERY", "proof_promotion": False}
    if not state.repeatability_evidence:
        return {"route": Route.PROVE_REPEATABILITY.value, "reason": "ONE_DELIVERY_NOT_REPEATABILITY", "proof_promotion": False}
    if not state.scale_constraints_bounded:
        return {"route": Route.SCALE_GATE.value, "reason": "SCALE_CONSTRAINTS_UNBOUNDED", "proof_promotion": False}
    return {"route": Route.SCALE_GATE.value, "reason": "SCALE_REVIEW_READY", "proof_promotion": False}
