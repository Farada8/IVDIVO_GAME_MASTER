import sys
import unittest
from pathlib import Path

CYCLE_ROOT = Path(__file__).resolve().parents[1]
if str(CYCLE_ROOT) not in sys.path:
    sys.path.insert(0, str(CYCLE_ROOT))

from engine.cross_lane_safeguards import *

class CrossLaneCycle6Tests(unittest.TestCase):
    def test_p81_decision_delta(self):
        self.assertEqual(decision_delta("A","A")["status"],"ZERO_DELTA_HOLD")
        self.assertIsNone(decision_delta(None,"B")["delta"])
    def test_p82_time_null_safe(self):
        self.assertIsNone(time_saved_null_safe(30,10)["minutes_saved"])
        self.assertEqual(time_saved_null_safe(30,10,measured=True)["minutes_saved"],20)
    def test_p83_error_avoidance(self):
        self.assertIsNone(error_avoidance(None,1)["errors_avoided"])
        self.assertIsNone(error_avoidance(5,3)["monetized_value"])
    def test_p84_vector_rubric(self):
        self.assertIsNone(artifact_rubric(completeness=1,freshness=1)["total_score"])
    def test_p85_fail_closed_completeness(self):
        self.assertEqual(completeness_gate(["deadline","source"],{"deadline":None,"source":"x"})["status"],"FAIL_CLOSED_MISSING_INPUT")
    def test_p86_half_life(self):
        self.assertLess(field_revalidation("PROCUREMENT_DEADLINE")["revalidate_days"],field_revalidation("POLICY")["revalidate_days"])
    def test_p87_substitution(self):
        r=substitution_matrix([{"available":True,"price_type":"FREE","jobs":["diagnosis"]}],{"diagnosis","implementation"})
        self.assertEqual(r["residual_unsolved_job"],["implementation"])
    def test_p88_false_confidence(self):
        self.assertFalse(false_confidence_guard(polished=True,proof_grade="PA3",unknown_fields=["eligibility"])["proof_upgrade_from_polish"])
    def test_p89_wip(self):
        self.assertEqual(wip_gate("OP01",["OP03","OP19"])["status"],"PASS")
        self.assertEqual(wip_gate("OP01",["OP03","OP19","OP20"])["status"],"FREEZE_EXCESS")
    def test_p90_pareto(self):
        cs=[{"id":"a","decision_utility":2,"evidence_accessibility":2,"kill_power":2},{"id":"b","decision_utility":1,"evidence_accessibility":1,"kill_power":1}]
        self.assertEqual(pareto_front(cs),["a"])
    def test_p91_si_repeat_rule(self):
        r=self_improvement_candidate([{"defect":"x","case_id":"a"},{"defect":"x","case_id":"b"},{"defect":"y","case_id":"a"}])
        self.assertEqual(r["candidates"],["x"])
    def test_p92_invariants(self):
        self.assertTrue(invariants([{"id":"a","public_only":True,"market_grade":"E2+","price":None}])["pass"])
        self.assertFalse(invariants([{"id":"a","public_only":True,"market_grade":"E3","price":None}])["pass"])
    def test_p93_independent_pa4(self):
        self.assertEqual(pa4_gate(same_source_packet=True,independent_reviewer=False,blinded_to_first_output=True),"HOLD_NOT_INDEPENDENT_PA4")
    def test_p94_test_designs(self):
        self.assertEqual(set(smallest_safe_decision_use_tests()),{"PROCUREMENT","RETROFIT","SME_AI"})
    def test_p95_pa5_e3(self):
        e={"target_user_class":"SME","decision_before":"x","decision_after":"y","interaction_artifact":"z","timestamp":"t","what_changed":"c","compliment_only":True}
        self.assertEqual(pa5_e3_gate(e),"HOLD_COMPLIMENT_NOT_BEHAVIOR")
    def test_p96_cycle_gate(self):
        lanes=[{"id":"PROC","pa_grade_num":3},{"id":"RETRO","pa_grade_num":3},{"id":"AI","pa_grade_num":3}]
        self.assertEqual(cycle6_eligibility(lanes)["status"],"HOLD_NO_PA4")

if __name__=="__main__": unittest.main()
