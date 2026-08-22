from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE = ROOT / "runtime" / "opp37_offer_router.py"
spec = importlib.util.spec_from_file_location("opp37_offer_router", MODULE)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
assert spec.loader is not None
spec.loader.exec_module(mod)


FULL = mod.REQUIRED_ARTIFACT_COMPONENTS


class Opp37OfferRouterTests(unittest.TestCase):
    def evidence(self, **overrides):
        data = dict(test37_internal_pass=True, artifact_components=FULL)
        data.update(overrides)
        return mod.OfferEvidence(**data)

    def test_narrow_offer_is_internal_testable(self):
        out = mod.validate_offer(self.evidence(), offer_name="First Party Fact Consistency Answerability Decision Pack")
        self.assertTrue(out["testable"])
        self.assertEqual(out["status"], "INTERNAL_OFFER_TESTABLE_NO_MARKET_PROOF")
        self.assertIsNone(out["willingness_to_pay"])
        self.assertIsNone(out["profitability"])
        self.assertFalse(out["proof_promotion"])

    def test_generic_ai_seo_audit_is_killed(self):
        out = mod.validate_offer(self.evidence(), offer_name="Generic AI SEO Audit")
        self.assertFalse(out["testable"])
        self.assertEqual(out["status"], "KILL_GENERIC_COMMODITY_CORE")

    def test_test37_dependency_is_required(self):
        out = mod.validate_offer(self.evidence(test37_internal_pass=False), offer_name="Decision Pack")
        self.assertFalse(out["testable"])
        self.assertEqual(out["status"], "HOLD_TEST37_NOT_PASSED")

    def test_incomplete_artifact_fails_closed(self):
        out = mod.validate_offer(self.evidence(artifact_components=FULL[:-1]), offer_name="Decision Pack")
        self.assertFalse(out["testable"])
        self.assertIn("IMPLEMENTATION_HANDOFF_CHECKLIST", out["missing"])

    def test_provenance_is_mandatory(self):
        out = mod.validate_offer(self.evidence(source_provenance_required=False), offer_name="Decision Pack")
        self.assertEqual(out["status"], "HOLD_PROVENANCE_REQUIRED")

    def test_ordinary_control_is_mandatory(self):
        out = mod.validate_offer(self.evidence(ordinary_control_separated=False), offer_name="Decision Pack")
        self.assertEqual(out["status"], "HOLD_NO_ORDINARY_CONTROL")

    def test_negative_findings_must_be_allowed(self):
        out = mod.validate_offer(self.evidence(negative_findings_allowed=False), offer_name="Decision Pack")
        self.assertEqual(out["status"], "HOLD_UPSELL_BIAS_NEGATIVE_CONTROL_REQUIRED")

    def test_unproven_revenue_claim_fails_closed(self):
        out = mod.validate_offer(self.evidence(claims_revenue_uplift=True), offer_name="Decision Pack")
        self.assertEqual(out["status"], "HOLD_UNPROVEN_MARKET_OR_ECONOMIC_CLAIM")

    def test_unproven_wtp_claim_fails_closed(self):
        out = mod.validate_offer(self.evidence(claims_wtp=True), offer_name="Decision Pack")
        self.assertEqual(out["status"], "HOLD_UNPROVEN_MARKET_OR_ECONOMIC_CLAIM")

    def test_pricing_hypothesis_is_not_wtp_or_profit(self):
        out = mod.pricing_hypothesis()
        self.assertEqual(out["test_points_ex_vat"], (249, 349, 490))
        self.assertEqual(out["central_hypothesis"], 349)
        self.assertIsNone(out["minimum_viable_price"])
        self.assertIsNone(out["willingness_to_pay"])
        self.assertIsNone(out["profitability"])

    def test_internal_decision_fixture_passes_with_negative_control(self):
        out = mod.internal_decision_test(specific_decisions=2, protected_negative_controls=1)
        self.assertTrue(out["pass"])
        self.assertFalse(out["buyer_value_proven"])
        self.assertFalse(out["proof_promotion"])

    def test_decision_test_fails_without_negative_control(self):
        out = mod.internal_decision_test(specific_decisions=3, protected_negative_controls=0)
        self.assertFalse(out["pass"])

    def test_saas_is_held_without_repeated_manual_need(self):
        out = mod.architecture_route("SAAS_TOOL_HOLD")
        self.assertFalse(out["build"])
        self.assertEqual(out["status"], "HOLD_REPEATED_MANUAL_NEED_REQUIRED")

    def test_coordinator_is_held_without_buyer_behavior(self):
        out = mod.architecture_route("IMPLEMENTATION_COORDINATOR_CONDITIONAL")
        self.assertFalse(out["build"])
        self.assertEqual(out["status"], "HOLD_BUYER_BEHAVIOR_REQUIRED")

    def test_final_route_opens_p33_p40_but_not_external_action(self):
        out = mod.next_route(p25_p32_complete=True, ci_verified=True)
        self.assertEqual(out["state"], "S5_OFFER_TESTABLE_INTERNAL_ONLY")
        self.assertEqual(out["executed_next64"], 32)
        self.assertEqual(out["remaining_next64"], 32)
        self.assertFalse(out["external_action"])
        self.assertIsNone(out["unit_economics"])
        self.assertFalse(out["proof_promotion"])


if __name__ == "__main__":
    unittest.main()
