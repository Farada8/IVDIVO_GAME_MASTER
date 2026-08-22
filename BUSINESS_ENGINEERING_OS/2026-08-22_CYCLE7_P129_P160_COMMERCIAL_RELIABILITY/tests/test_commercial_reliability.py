import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from engine.commercial_reliability import *


class CommercialReliabilityTests(unittest.TestCase):
    def test_01_zero_residual_job_holds(self):
        r = residual_job({"alert"}, [{"available": True, "class": "PUBLIC", "jobs": ["alert"]}])
        self.assertEqual(r["status"], "HOLD_ZERO_RESIDUAL_JOB")
        self.assertFalse(r["paid_residual_proven"])

    def test_02_residual_is_not_paid_proof(self):
        r = residual_job({"alert", "evidence_gap"}, [{"available": True, "class": "PUBLIC", "jobs": ["alert"]}])
        self.assertEqual(r["residual"], ["evidence_gap"])
        self.assertFalse(r["paid_residual_proven"])

    def test_03_decision_utility_requires_real_user(self):
        self.assertIsNone(decision_utility("A", "B", real_user=False)["decision_delta"])

    def test_04_real_decision_delta_can_be_observed(self):
        self.assertTrue(decision_utility("A", "B", real_user=True)["decision_delta"])

    def test_05_internal_price_guess_fails(self):
        self.assertIsNone(external_price_gate(100, external_signal=False)["price"])

    def test_06_external_price_signal_can_bind(self):
        self.assertEqual(external_price_gate(100, external_signal=True)["price"], 100)

    def test_07_hypothetical_discovery_fails(self):
        self.assertFalse(behavior_first_record(past_event="bid", actual_spend=20, hypothetical=True)["valid_for_discovery"])

    def test_08_past_behavior_is_valid_discovery_input(self):
        self.assertTrue(behavior_first_record(past_event="missed bid", actual_spend=300)["valid_for_discovery"])

    def test_09_ambiguity_routes_to_human(self):
        self.assertTrue(legal_handoff("exclusion", "pack:p3", "ambiguous")["human_review_required"])

    def test_10_missing_credential_source_unknown(self):
        self.assertEqual(credential_state(source=None, issuer="x", verified_at="t", expires_at="e"), "UNKNOWN")

    def test_11_missing_expiry_revalidates(self):
        self.assertEqual(credential_state(source="doc", issuer="x", verified_at="t", expires_at=None), "REVALIDATE_HOLD")

    def test_12_identity_is_not_capability(self):
        self.assertEqual(supplier_identity_state(True, 0), "PARTIAL_IDENTITY_ONLY")

    def test_13_positive_relevance_is_not_eligibility(self):
        self.assertEqual(negative_relevance_filter(category_match=True, scope_match=True, geography_match=True), "PASS_TO_FULL_QUALIFICATION_NOT_ELIGIBILITY")

    def test_14_negative_relevance_can_reject(self):
        self.assertEqual(negative_relevance_filter(category_match=False, scope_match=True, geography_match=True), "REJECT_OBVIOUS_IRRELEVANCE")

    def test_15_stale_open_status_revalidates(self):
        self.assertEqual(stale_status_guard(label="Open", deadline_passed=True), "REVALIDATE_STATUS")

    def test_16_real_input_gate_holds(self):
        self.assertEqual(lane_unlock(None), "HOLD_REAL_INPUT")

    def test_17_minimization_drops_unneeded_fields(self):
        r = minimize_private_record({"name": "x", "tax": "secret", "favorite": "unused"}, {"name", "tax"})
        self.assertNotIn("favorite", r)

    def test_18_public_derivative_redacts_secret(self):
        r = public_safe_derivative({"tax": "abc", "country": "IE"}, {"tax"}, {"tax"})
        self.assertEqual(r["tax"], "PRIVATE_VERIFIED")
        self.assertEqual(r["country"], "IE")

    def test_19_value_vector_has_no_total(self):
        self.assertIsNone(decision_value_vector(decision_delta=None, human_minutes=None, observed_errors=None, next_action_clear=True)["total_score"])

    def test_20_cash_gap_is_null_without_terms(self):
        self.assertIsNone(cash_gap(required_outflow=1000, payment_received_before_outflow=None))

    def test_21_margin_requires_observed_delivery_basis(self):
        self.assertIsNone(contribution_margin(external_price=1000, variable_cost=100, observed_delivery_hours=None, labor_rate=20))

    def test_22_capacity_requires_observed_time(self):
        self.assertIsNone(service_capacity(available_human_hours=40, observed_hours_per_delivery=None))

    def test_23_provenance_path_required(self):
        edges = [Edge("source", "field", "extract"), Edge("field", "artifact", "compile"), Edge("artifact", "decision", "use")]
        self.assertTrue(provenance_path(edges, "source", "decision"))
        self.assertFalse(provenance_path(edges, "source", "proof"))

    def test_24_cross_store_and_promotion_fail_closed(self):
        self.assertEqual(persistence_state(github_written=True, drive_written=False, readback_verified=False), "PARTIAL_FAILURE")
        self.assertEqual(authority_promotion_gate(ci_green=True, unresolved_review_threads=0, drive_readback=False, fresh_main_reconciled=True), "STOP_RECONCILE")

    def test_25_full_persistence_can_verify(self):
        self.assertEqual(persistence_state(github_written=True, drive_written=True, readback_verified=True), "READBACK_VERIFIED")

    def test_26_promotion_requires_all_gates(self):
        self.assertEqual(authority_promotion_gate(ci_green=True, unresolved_review_threads=0, drive_readback=True, fresh_main_reconciled=True), "PROMOTION_ELIGIBLE")

    def test_27_next_frontier_pack_first(self):
        self.assertEqual(next_frontier(full_target_pack=False, verified_supplier_packet=False, independent_pa4=False, real_user_interaction=False), "ACQUIRE_CURRENT_TARGET_PACK")

    def test_28_next_frontier_supplier_second(self):
        self.assertEqual(next_frontier(full_target_pack=True, verified_supplier_packet=False, independent_pa4=False, real_user_interaction=False), "ACQUIRE_VERIFIED_SUPPLIER_PACKET")


if __name__ == "__main__":
    unittest.main()
