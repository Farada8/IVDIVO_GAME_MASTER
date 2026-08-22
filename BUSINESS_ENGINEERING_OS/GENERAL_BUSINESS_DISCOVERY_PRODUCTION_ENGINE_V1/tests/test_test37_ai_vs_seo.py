from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "runtime" / "test37_ai_vs_seo.py"
spec = importlib.util.spec_from_file_location("test37_ai_vs_seo", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
assert spec.loader is not None
spec.loader.exec_module(mod)


class Test37AiVsSeoTests(unittest.TestCase):
    def test_current_result_is_exactly_two_of_three(self):
        out = mod.current_result()
        self.assertTrue(out["pass"])
        self.assertEqual(out["count"], 2)
        self.assertEqual(out["sample"], 3)
        self.assertEqual(out["status"], "PASS_INTERNAL_DIFFERENTIAL_2_OF_3_OR_BETTER")

    def test_no_buyer_or_market_promotion(self):
        out = mod.current_result()
        self.assertFalse(out["buyer_behavior"])
        self.assertIsNone(out["willingness_to_pay"])
        self.assertIsNone(out["transaction"])
        self.assertFalse(out["proof_promotion"])
        self.assertEqual(out["next64_increment"], 0)

    def test_exactly_three_sites_required(self):
        out = mod.evaluate(mod.CURRENT_OBSERVATIONS[:2])
        self.assertFalse(out["pass"])
        self.assertEqual(out["status"], "HOLD_EXACTLY_THREE_SITES_REQUIRED")

    def test_duplicate_site_fails_closed(self):
        p = mod.CURRENT_OBSERVATIONS[0]
        out = mod.evaluate((p, p, mod.CURRENT_OBSERVATIONS[2]))
        self.assertFalse(out["pass"])
        self.assertEqual(out["status"], "HOLD_DUPLICATE_SITE")

    def test_ordinary_seo_problem_cannot_count_as_ai_defect(self):
        obs = mod.SiteObservation("SEO_ONLY", False, True, True, True)
        out = mod.classify(obs)
        self.assertFalse(out["counts"])

    def test_unreproduced_defect_cannot_count(self):
        obs = mod.SiteObservation("UNREPRODUCED", True, True, False, True)
        self.assertFalse(mod.classify(obs)["counts"])

    def test_unactionable_defect_cannot_count(self):
        obs = mod.SiteObservation("UNACTIONABLE", True, True, True, False)
        self.assertFalse(mod.classify(obs)["counts"])

    def test_one_of_three_is_ambiguous_not_pass(self):
        rows = (
            mod.SiteObservation("A", True, True, True, True),
            mod.SiteObservation("B", True, False, False, False),
            mod.SiteObservation("C", True, False, False, False),
        )
        out = mod.evaluate(rows)
        self.assertFalse(out["pass"])
        self.assertEqual(out["status"], "AMBIGUOUS_INTERNAL_DIFFERENTIAL_1_OF_3")

    def test_zero_of_three_is_fail(self):
        rows = tuple(mod.SiteObservation(str(i), True, False, False, False) for i in range(3))
        out = mod.evaluate(rows)
        self.assertFalse(out["pass"])
        self.assertEqual(out["status"], "FAIL_INTERNAL_DIFFERENTIAL_0_OF_3")


if __name__ == "__main__":
    unittest.main()
