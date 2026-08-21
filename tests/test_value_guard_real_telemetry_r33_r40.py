import json
import pathlib
import unittest

from tools.ivdivo_value_guard import evaluate

ROOT = pathlib.Path(__file__).resolve().parents[1]
PAYLOAD = ROOT / "SELF_IMPROVEMENT_STUDIO" / "2026-08-21_PRODUCTION_PROOF_CONVERGENCE_RUN32" / "evidence" / "R33_R40_PRODUCTION_PROOF_VALUE_TELEMETRY_v1.json"


class ValueGuardRealTelemetryR33R40Tests(unittest.TestCase):
    def test_partial_real_telemetry_holds_for_measurement(self):
        payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
        result = evaluate(payload)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["disposition"], "HOLD_FOR_MEASUREMENT")
        self.assertEqual(result["metrics"]["measurement_state"], "PARTIAL")
        self.assertEqual(result["metrics"]["real_project_pilots"], 6.0)
        self.assertEqual(result["metrics"]["independent_human_evidence_count"], 0.0)
        self.assertEqual(result["metrics"]["precision"], 1.0)
        self.assertIn("VALUE_TELEMETRY_NOT_COMPLETE", result["reasons"])

    def test_unknown_time_values_remain_null_in_source(self):
        payload = json.loads(PAYLOAD.read_text(encoding="utf-8"))
        t = payload["telemetry"]
        self.assertIsNone(t["measured_minutes_saved"])
        self.assertIsNone(t["measured_overhead_minutes"])
        self.assertIsNone(payload["evidence_boundaries"]["false_negative_rate"])
        self.assertFalse(payload["evidence_boundaries"]["promotion_allowed"])


if __name__ == "__main__":
    unittest.main()
