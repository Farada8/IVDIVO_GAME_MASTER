import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pew06_proof", ROOT / "proof.py")
MOD = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MOD)


class TestPEW06Proof(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = json.loads((ROOT / "01_FIXTURES.json").read_text(encoding="utf-8"))
        cls.result = MOD.compute(cls.payload)

    def test_fixture_is_explicitly_synthetic(self):
        self.assertTrue(self.payload["synthetic"])
        self.assertFalse(self.payload["real_provider_prices_used"])

    def test_total_cost(self):
        self.assertEqual(self.result["total_cost_eur"], 100.0)

    def test_work_unit_coverage(self):
        self.assertEqual(self.result["work_unit_cost_coverage_pct"], 95.0)

    def test_outcome_coverage(self):
        self.assertEqual(self.result["outcome_cost_coverage_pct"], 78.0)

    def test_unattributed_cost(self):
        self.assertEqual(self.result["unattributed_outcome_cost_eur"], 22.0)

    def test_target_costs(self):
        self.assertEqual(self.result["observed_target_ai_cost_eur"], 13.0)
        self.assertEqual(self.result["ground_truth_target_ai_cost_eur"], 35.0)

    def test_margin_flip(self):
        self.assertEqual(self.result["reported_margin_eur"], 7.0)
        self.assertEqual(self.result["corrected_margin_eur"], -15.0)
        self.assertTrue(self.result["decision_error_detected"])

    def test_threshold_holds(self):
        self.assertFalse(self.result["decision_ready_by_threshold"])
        self.assertEqual(self.result["technical_result"], "PASS_TECHNICAL_GAP_ONLY")

    def test_commercial_boundary(self):
        self.assertEqual(self.result["commercial_result"], "HOLD_COMMERCIAL_DIFFERENTIATION_UNPROVEN")
        self.assertFalse(self.result["wip_promotion"])
        self.assertEqual(self.result["buyer_demand"], "UNPROVEN")
        self.assertEqual(self.result["wtp"], "UNKNOWN")
        self.assertIsNone(self.result["price"])
        self.assertEqual(self.result["transactions"], 0)
        self.assertEqual(self.result["profitability"], "UNPROVEN")
        self.assertFalse(self.result["external_action_authorized"])


if __name__ == "__main__":
    unittest.main()
