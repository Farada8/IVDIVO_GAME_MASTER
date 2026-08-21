import unittest
from tools.ivdivo_value_guard import evaluate

def p(**telemetry):
    base={"measurement_state":"COMPLETE","true_positive_findings":3,"false_positive_findings":1,"accepted_repairs":2,
          "avoided_rework_cycles":1,"measured_minutes_saved":60,"measured_overhead_minutes":20,
          "new_artifacts":2,"new_prompts":2,"real_project_pilots":1,
          "independent_human_evidence_count":0,"regressions_introduced":0,
          "unsafe_or_unauthorized_actions_blocked":1}
    base.update(telemetry)
    return {"candidate_id":"SI-X","telemetry":base}

class ValueTests(unittest.TestCase):
    def test_keep_candidate(self):
        self.assertEqual(evaluate(p())["disposition"],"KEEP_CANDIDATE")
    def test_hold_without_real_pilot(self):
        self.assertEqual(evaluate(p(real_project_pilots=0))["disposition"],"HOLD_FOR_REAL_PILOT")
    def test_promotion_review_requires_multi_project_human(self):
        self.assertEqual(evaluate(p(real_project_pilots=2,independent_human_evidence_count=1))["disposition"],"PROMOTION_REVIEW_ELIGIBLE")
    def test_low_precision_prune(self):
        self.assertEqual(evaluate(p(true_positive_findings=1,false_positive_findings=5))["disposition"],"PRUNE_OR_REVISE")
    def test_regression_forces_revise(self):
        self.assertEqual(evaluate(p(regressions_introduced=1))["disposition"],"REVISE_OR_ROLLBACK")
    def test_negative_value_prune(self):
        self.assertEqual(evaluate(p(measured_overhead_minutes=1000,new_artifacts=50,new_prompts=50))["disposition"],"PRUNE_OR_REVISE")
    def test_no_alert_precision_is_none(self):
        self.assertIsNone(evaluate(p(true_positive_findings=0,false_positive_findings=0))["metrics"]["precision"])
    def test_unmeasured_value_holds_without_fake_precision(self):
        result=evaluate(p(measurement_state="UNMEASURED",real_project_pilots=1))
        self.assertEqual(result["disposition"],"HOLD_FOR_MEASUREMENT")
    def test_partial_null_measurements_hold_not_fake_zero(self):
        result=evaluate({"candidate_id":"SI-X","telemetry":{
            "measurement_state":"PARTIAL","real_project_pilots":2,
            "measured_minutes_saved":None,"measured_overhead_minutes":None,
            "independent_human_evidence_count":None
        }})
        self.assertEqual(result["disposition"],"HOLD_FOR_MEASUREMENT")
        self.assertEqual(result["metrics"]["measurement_state"],"PARTIAL")
    def test_complete_label_with_missing_fields_holds(self):
        result=evaluate({"candidate_id":"SI-X","telemetry":{
            "measurement_state":"COMPLETE","real_project_pilots":2
        }})
        self.assertEqual(result["disposition"],"HOLD_FOR_MEASUREMENT")
        self.assertEqual(result["metrics"]["measurement_state"],"COMPLETE_INVALID")
        self.assertIn("COMPLETE_LABEL_WITH_MISSING_OR_UNKNOWN_MEASUREMENTS",result["reasons"])
    def test_negative_telemetry_fails_closed(self):
        result=evaluate(p(measured_overhead_minutes=-1))
        self.assertEqual(result["status"],"FAIL_CLOSED")
        self.assertEqual(result["disposition"],"STOP")
    def test_missing_input_fails_closed(self):
        self.assertEqual(evaluate({})["status"],"FAIL_CLOSED")

if __name__=="__main__": unittest.main()
