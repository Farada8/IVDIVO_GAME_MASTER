import unittest

from tools.ivdivo_interruption_learning import summarize_events


class InterruptionLearningNullTelemetryTests(unittest.TestCase):
    def test_unknown_optional_telemetry_remains_null(self):
        result = summarize_events([
            {
                "event_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            }
        ])
        metrics = result["metrics"]
        self.assertIsNone(metrics["duplicate_work_units_avoided"])
        self.assertIsNone(metrics["writes_reconciled"])
        self.assertIsNone(metrics["checkpoint_tool_calls"])
        self.assertIsNone(metrics["recovery_tool_calls"])
        self.assertIsNone(metrics["checkpoint_bytes_total"])
        self.assertIsNone(metrics["checkpoint_bytes_mean"])

    def test_known_zero_remains_real_zero(self):
        result = summarize_events([
            {
                "event_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
                "checkpoint_bytes": 0,
                "recovery_tool_calls": 0,
            }
        ])
        metrics = result["metrics"]
        self.assertEqual(metrics["checkpoint_bytes_total"], 0)
        self.assertEqual(metrics["checkpoint_bytes_mean"], 0.0)
        self.assertEqual(metrics["recovery_tool_calls"], 0)
        self.assertEqual(metrics["telemetry_known_rows"]["checkpoint_bytes"], 1)
        self.assertEqual(metrics["telemetry_known_rows"]["recovery_tool_calls"], 1)

    def test_partial_known_telemetry_sums_only_known_rows(self):
        result = summarize_events([
            {
                "event_id": "I1",
                "project_id": "P1",
                "work_unit": "W1",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
                "writes_reconciled": 2,
            },
            {
                "event_id": "I2",
                "project_id": "P2",
                "work_unit": "W2",
                "recovery_decision": "REBASE_FIRST",
                "real_interruption": True,
            },
        ])
        metrics = result["metrics"]
        self.assertEqual(metrics["writes_reconciled"], 2)
        self.assertEqual(metrics["telemetry_known_rows"]["writes_reconciled"], 1)
        self.assertIsNone(metrics["checkpoint_bytes_total"])


if __name__ == "__main__":
    unittest.main()
