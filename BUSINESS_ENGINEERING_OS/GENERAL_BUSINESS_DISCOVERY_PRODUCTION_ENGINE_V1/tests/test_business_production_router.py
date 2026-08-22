from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "runtime" / "business_production_router.py"
s = spec_from_file_location("router", P)
m = module_from_spec(s); s.loader.exec_module(m)
B = m.BusinessState
R = m.route


def rr(**kw):
    return R(B(**kw))["route"]


def test_restore_first(): assert rr() == "RESTORE"
def test_discover_after_restore(): assert rr(authority_restored=True) == "DISCOVER"
def test_qualify_requires_buyer_and_market(): assert rr(authority_restored=True, opportunity_defined=True) == "QUALIFY"
def test_fatal_identification(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True) == "TEST_FATAL"
def test_fatal_fail_kills(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="FAIL") == "KILL"
def test_ambiguous_retests(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="AMBIGUOUS") == "TEST_FATAL"
def test_value_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS") == "BOUND_VALUE"
def test_offer_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True) == "BUILD_OFFER"
def test_economics_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True) == "BOUND_ECONOMICS"
def test_sales_packet_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True) == "PREPARE_SALES_TEST"
def test_external_auth_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True, sales_test_packet_ready=True) == "WAIT_EXTERNAL_EVIDENCE"
def test_buyer_behavior_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True, sales_test_packet_ready=True, external_action_authorized=True) == "WAIT_EXTERNAL_EVIDENCE"
def test_transaction_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True, sales_test_packet_ready=True, external_action_authorized=True, buyer_behavior_observed=True) == "PROCESS_TRANSACTION"
def test_delivery_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True, sales_test_packet_ready=True, external_action_authorized=True, buyer_behavior_observed=True, transaction_evidence=True) == "PROVE_DELIVERY"
def test_repeatability_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True, sales_test_packet_ready=True, external_action_authorized=True, buyer_behavior_observed=True, transaction_evidence=True, delivery_accepted=True) == "PROVE_REPEATABILITY"
def test_scale_gate(): assert rr(authority_restored=True, opportunity_defined=True, micro_market_defined=True, buyer_problem_defined=True, fatal_assumption_identified=True, fatal_test_result="PASS", measurable_value_hypothesis=True, offer_testable=True, economics_bounded=True, sales_test_packet_ready=True, external_action_authorized=True, buyer_behavior_observed=True, transaction_evidence=True, delivery_accepted=True, repeatability_evidence=True) == "SCALE_GATE"
def test_specialist_blocker_holds(): assert rr(authority_restored=True, specialist_blocker=True) == "HOLD"
def test_explicit_kill_wins(): assert rr(explicit_kill=True) == "KILL"
def test_router_never_promotes_proof(): assert R(B())["proof_promotion"] is False
