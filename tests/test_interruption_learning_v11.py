import unittest

from tools.ivdivo_interruption_learning import summarize_events, validate_event


class InterruptionLearningV11Tests(unittest.TestCase):
    def test_one_incident_two_projects_counts_once(self):
        events = [
            {
                "event_id": "I1",
                "incident_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
                "project_slice_readback_complete": True,
            },
            {
                "event_id": "I1",
                "incident_id": "I1",
                "project_id": "P2",
                "work_unit": "W2",
                "recovery_decision": "RECOVER_PERSISTED_AUTHORITY_FIRST",
                "real_interruption": True,
                "project_slice_readback_complete": True,
            },
        ]
        result = summarize_events(events)
        self.assertEqual(result["promotion_progress"]["genuine_incidents"], 1)
        self.assertEqual(result["promotion_progress"]["distinct_projects"], 2)
        self.assertEqual(result["promotion_recommendation"], "CONTINUE_PILOT")

    def test_same_incident_three_projects_still_counts_once(self):
        events = [
            {
                "event_id": "I1",
                "incident_id": "I1",
                "project_id": f"P{i}",
                "work_unit": f"W{i}",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            }
            for i in range(3)
        ]
        result = summarize_events(events)
        self.assertEqual(result["metrics"]["qualified_real_incident_count"], 1)
        self.assertEqual(result["metrics"]["real_project_count"], 3)

    def test_legacy_three_independent_incidents_still_reach_review(self):
        events = [
            {
                "event_id": "1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            },
            {
                "event_id": "2",
                "project_id": "P2",
                "work_unit": "W2",
                "recovery_decision": "RECOVER_VOLATILE_FIRST",
                "real_interruption": True,
            },
            {
                "event_id": "3",
                "project_id": "P1",
                "work_unit": "W3",
                "recovery_decision": "RESUME_EXACT",
                "real_interruption": True,
            },
        ]
        result = summarize_events(events)
        self.assertEqual(result["promotion_recommendation"], "ELIGIBLE_FOR_PROMOTION_REVIEW")
        self.assertFalse(result["promotion_progress"]["promotion_authorized"])

    def test_duplicate_recovery_id_rejected(self):
        first = {
            "event_id": "I1",
            "incident_id": "I1",
            "recovery_id": "R1",
            "project_id": "P1",
            "work_unit": "W1",
            "recovery_decision": "REBASE_FIRST",
            "real_interruption": True,
        }
        second = dict(first)
        second["project_id"] = "P2"
        with self.assertRaises(ValueError):
            summarize_events([first, second])

    def test_same_incident_may_not_mix_real_and_synthetic(self):
        events = [
            {
                "event_id": "I1",
                "incident_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            },
            {
                "event_id": "I1",
                "incident_id": "I1",
                "project_id": "P2",
                "work_unit": "W2",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": False,
            },
        ]
        with self.assertRaises(ValueError):
            summarize_events(events)

    def test_incomplete_readback_does_not_qualify_real_incident(self):
        result = summarize_events([
            {
                "event_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
                "project_slice_readback_complete": False,
            }
        ])
        self.assertEqual(result["promotion_progress"]["genuine_incidents"], 0)
        self.assertEqual(result["promotion_recommendation"], "HOLD")

    def test_false_resume_always_blocks(self):
        result = summarize_events([
            {
                "event_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "RESUME_EXACT",
                "real_interruption": True,
                "false_resume": True,
            }
        ])
        self.assertEqual(result["reason"], "FALSE_RESUME_PRESENT")

    def test_synthetic_rows_cannot_satisfy_threshold(self):
        events = [
            {
                "event_id": f"S{i}",
                "project_id": "P1" if i % 2 else "P2",
                "work_unit": f"W{i}",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": False,
            }
            for i in range(5)
        ]
        result = summarize_events(events)
        self.assertEqual(result["promotion_progress"]["genuine_incidents"], 0)
        self.assertEqual(result["promotion_recommendation"], "HOLD")

    def test_synthetic_false_resume_can_block_for_safety(self):
        events = [
            {
                "event_id": "R1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            },
            {
                "event_id": "S1",
                "project_id": "P2",
                "work_unit": "W2",
                "recovery_decision": "RESUME_EXACT",
                "real_interruption": False,
                "false_resume": True,
            },
        ]
        result = summarize_events(events)
        self.assertEqual(result["promotion_recommendation"], "HOLD")
        self.assertEqual(result["reason"], "FALSE_RESUME_PRESENT")

    def test_project_slice_id_alias_is_supported(self):
        normalized = validate_event({
            "event_id": "I1",
            "project_slice_id": "BUSINESS_ENGINEERING",
            "work_unit": "W1",
            "recovery_decision": "REBASE_FIRST",
            "real_interruption": True,
        })
        self.assertEqual(normalized["project_id"], "BUSINESS_ENGINEERING")

    def test_explicit_qualification_cannot_override_missing_readback(self):
        result = summarize_events([
            {
                "event_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
                "project_slice_readback_complete": False,
                "qualifying_recovery": True,
            }
        ])
        self.assertEqual(result["promotion_progress"]["genuine_incidents"], 0)

    def test_three_incidents_same_project_do_not_meet_project_diversity(self):
        events = [
            {
                "event_id": f"I{i}",
                "project_id": "P1",
                "work_unit": f"W{i}",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            }
            for i in range(3)
        ]
        result = summarize_events(events)
        self.assertEqual(result["promotion_progress"]["genuine_incidents"], 3)
        self.assertEqual(result["promotion_progress"]["distinct_projects"], 1)
        self.assertEqual(result["promotion_recommendation"], "CONTINUE_PILOT")


if __name__ == "__main__":
    unittest.main()
