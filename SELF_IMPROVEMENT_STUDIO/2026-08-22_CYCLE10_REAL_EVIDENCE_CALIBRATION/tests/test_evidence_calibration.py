import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
P = ROOT / "runtime" / "evidence_calibration.py"
spec = importlib.util.spec_from_file_location("ec", P)
ec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ec)


class EvidenceCalibrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.event = json.loads((ROOT / "01_IMPROVEMENT_EVENT_001.json").read_text())
        cls.receipt = json.loads((ROOT / "02_AVOIDED_FAILURE_RECEIPT_001.json").read_text())

    def test_real_event_contract(self):
        self.assertTrue(ec.validate_improvement_event(self.event)["valid"])

    def test_receipt_contract(self):
        self.assertTrue(ec.validate_avoided_failure_receipt(self.receipt)["valid"])

    def test_one_interruption_two_slices_still_one_event(self):
        self.assertEqual(self.event["genuine_interruption_event_count"], 1)
        self.assertEqual(self.event["distinct_project_recoveries"], 2)

    def test_operator_minutes_stays_null_without_measurement(self):
        self.assertIsNone(self.event["measurement"]["operator_minutes"])

    def test_money_saved_stays_null_without_measurement(self):
        self.assertIsNone(self.receipt["economic_metrics"]["money_saved"])

    def test_hypothetical_time_saved_is_blocked(self):
        out = ec.reject_hypothetical_benefit_laundering(observed=True, measured_value=None, claim_type="TIME_SAVED")
        self.assertFalse(out["allowed"])

    def test_unobserved_failure_claim_is_blocked(self):
        out = ec.reject_hypothetical_benefit_laundering(observed=False, measured_value=1, claim_type="FAILURE_AVOIDED")
        self.assertFalse(out["allowed"])

    def test_current_recovery_progress_holds(self):
        out = ec.recovery_progress(
            genuine_event_ids=[self.event["event_id"]],
            project_ids=[x["project_id"] for x in self.event["project_slices"]],
            false_resume_count=0,
        )
        self.assertEqual(out["status"], "HOLD_RECOVERY_EVIDENCE_GATE")
        self.assertFalse(out["auto_promote"])

    def test_three_genuine_events_two_projects_zero_false_resume_only_review_eligible(self):
        out = ec.recovery_progress(
            genuine_event_ids=["e1", "e2", "e3"],
            project_ids=["p1", "p2"],
            false_resume_count=0,
        )
        self.assertEqual(out["status"], "ELIGIBLE_FOR_REVIEW")
        self.assertTrue(out["eligible_for_promotion_review"])
        self.assertFalse(out["auto_promote"])

    def test_false_resume_blocks_review_even_at_counts(self):
        out = ec.recovery_progress(
            genuine_event_ids=["e1", "e2", "e3"],
            project_ids=["p1", "p2"],
            false_resume_count=1,
        )
        self.assertFalse(out["eligible_for_promotion_review"])

    def test_wrong_resume_paths_not_event_count(self):
        self.assertEqual(self.receipt["recovery_quality"]["genuine_event_count"], 1)
        self.assertEqual(self.receipt["rejected_wrong_resume_paths"]["count"], 4)


if __name__ == "__main__":
    unittest.main()
