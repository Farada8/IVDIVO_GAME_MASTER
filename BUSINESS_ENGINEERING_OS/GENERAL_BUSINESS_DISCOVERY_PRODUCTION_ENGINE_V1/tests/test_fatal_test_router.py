from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "runtime" / "fatal_test_router.py"
spec = importlib.util.spec_from_file_location("fatal_test_router", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
assert spec.loader is not None
spec.loader.exec_module(mod)


class FatalTestRouterTests(unittest.TestCase):
    def test_current_portfolio_ready_and_bounded(self):
        out = mod.validate_portfolio()
        self.assertTrue(out["ready"])
        self.assertEqual(out["wip_count"], 3)
        self.assertEqual(out["state"], "S3_FATAL_TEST_READY")
        self.assertFalse(out["proof_promotion"])

    def test_one_primary_two_pilots(self):
        self.assertEqual(sum(t.role == "PRIMARY" for t in mod.CURRENT_TESTS), 1)
        self.assertEqual(sum(t.role == "PILOT" for t in mod.CURRENT_TESTS), 2)

    def test_all_thresholds_predeclared(self):
        self.assertTrue(all(t.threshold_declared for t in mod.CURRENT_TESTS))

    def test_all_negative_controls_declared(self):
        self.assertTrue(all(t.negative_control for t in mod.CURRENT_TESTS))

    def test_wip_overflow_fails_closed(self):
        extra = mod.FatalTest("OPP-X", "PILOT", "X", "TEST-X", True, "CONTROL", True)
        out = mod.validate_portfolio(mod.CURRENT_TESTS + (extra,))
        self.assertFalse(out["ready"])
        self.assertEqual(out["status"], "HOLD_WIP_LIMIT_EXCEEDED")

    def test_duplicate_opportunity_fails_closed(self):
        duplicate = mod.FatalTest("OPP-33", "PILOT", "X", "TEST-X", True, "CONTROL", True)
        out = mod.validate_portfolio((mod.CURRENT_TESTS[0], duplicate))
        self.assertFalse(out["ready"])
        self.assertEqual(out["status"], "HOLD_DUPLICATE_OPPORTUNITY")

    def test_missing_threshold_fails_closed(self):
        bad = mod.FatalTest("OPP-X", "PRIMARY", "X", "TEST-X", False, "CONTROL", False)
        out = mod.validate_portfolio((bad,))
        self.assertFalse(out["ready"])
        self.assertEqual(out["status"], "HOLD_THRESHOLD_NOT_PREDECLARED")

    def test_missing_negative_control_fails_closed(self):
        bad = mod.FatalTest("OPP-X", "PRIMARY", "X", "TEST-X", True, "", False)
        out = mod.validate_portfolio((bad,))
        self.assertFalse(out["ready"])
        self.assertEqual(out["status"], "HOLD_NEGATIVE_CONTROL_MISSING")

    def test_opp33_requires_external_authorization(self):
        out = mod.route_test(mod.CURRENT_TESTS[0], external_action_authorized=False)
        self.assertEqual(out["status"], "HOLD_EXTERNAL_ACTION_AUTHORIZATION_REQUIRED")
        self.assertFalse(out["external_action"])

    def test_opp36_requires_external_authorization(self):
        out = mod.route_test(mod.CURRENT_TESTS[1], external_action_authorized=False)
        self.assertEqual(out["status"], "HOLD_EXTERNAL_ACTION_AUTHORIZATION_REQUIRED")

    def test_opp37_has_internal_negative_control(self):
        out = mod.route_test(mod.CURRENT_TESTS[2], external_action_authorized=False)
        self.assertEqual(out["status"], "RUN_INTERNAL_NEGATIVE_CONTROL_ONLY")
        self.assertFalse(out["proof_promotion"])

    def test_behavior_does_not_auto_promote(self):
        out = mod.route_test(mod.CURRENT_TESTS[0], external_action_authorized=True, new_behavior_evidence=True)
        self.assertEqual(out["status"], "BEHAVIOR_EVIDENCE_REQUIRES_REVIEW")
        self.assertFalse(out["proof_promotion"])

    def test_next_internal_action_is_opp37_only(self):
        out = mod.next_internal_action()
        self.assertEqual(out["status"], "INTERNAL_WORK_AVAILABLE")
        self.assertEqual(out["tests"], ["TEST-37"])
        self.assertEqual(out["next_block"], "P09-P16_TARGETED_TO_CURRENT_WIP")


if __name__ == "__main__":
    unittest.main()
