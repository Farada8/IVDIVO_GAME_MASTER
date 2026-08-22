import unittest
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "engine"))
from proof_transition_engine import *

class Cycle7AProofTests(unittest.TestCase):
    def test_01_non_authoritative_pack_blocks(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=True,revision_inventory_complete=True,authoritative_source=False)["status"],"BLOCKED_NONAUTHORITATIVE_SOURCE")
    def test_02_authenticated_pack_required(self):
        self.assertFalse(pack_acquisition_status(authenticated_or_user_pack=False,attachment_inventory_complete=False,revision_inventory_complete=False,authoritative_source=True)["pack_complete"])
    def test_03_attachment_inventory_required(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=False,revision_inventory_complete=True,authoritative_source=True)["status"],"BLOCKED_ATTACHMENT_INVENTORY_INCOMPLETE")
    def test_04_revision_inventory_required(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=True,revision_inventory_complete=False,authoritative_source=True)["status"],"BLOCKED_REVISION_INVENTORY_INCOMPLETE")
    def test_05_complete_pack_passes(self):
        self.assertTrue(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=True,revision_inventory_complete=True,authoritative_source=True)["pack_complete"])
    def test_06_supplier_missing_holds(self):
        self.assertFalse(supplier_profile_status({}, {})["verified"])
    def test_07_supplier_unsourced_holds(self):
        fields={k:"x" for k in REQUIRED_SUPPLIER_FIELDS}
        self.assertTrue(supplier_profile_status(fields,{})["unsourced"])
    def test_08_supplier_verified_needs_all_sources(self):
        fields={k:"x" for k in REQUIRED_SUPPLIER_FIELDS}; p={k:"s" for k in REQUIRED_SUPPLIER_FIELDS}
        self.assertTrue(supplier_profile_status(fields,p)["verified"])
    def test_09_join_unknown(self):
        self.assertEqual(join_requirements([{"field":"turnover"}],{})[0]["gap_state"],"UNKNOWN")
    def test_10_join_min_noncurable(self):
        self.assertEqual(join_requirements([{"field":"turnover","min":100}],{"turnover":50})[0]["gap_state"],"NONCURABLE")
    def test_11_join_allowed_noncurable(self):
        self.assertEqual(join_requirements([{"field":"cert","allowed":["A"]}],{"cert":"B"})[0]["gap_state"],"NONCURABLE")
    def test_12_join_met(self):
        self.assertEqual(join_requirements([{"field":"cert","allowed":["A"]}],{"cert":"A"})[0]["gap_state"],"MET")
    def test_13_decision_pack_hold(self):
        self.assertEqual(route_bid_decision(pack_complete=False,profile_verified=True,joined=[])["decision"],"HOLD")
    def test_14_decision_profile_hold(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=False,joined=[])["reason"],"UNVERIFIED_SUPPLIER_PROFILE")
    def test_15_decision_unknown_hold(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[{"gap_state":"UNKNOWN"}])["decision"],"HOLD")
    def test_16_decision_noncurable_no_bid(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[{"gap_state":"NONCURABLE"}])["decision"],"NO_BID")
    def test_17_decision_all_met_is_candidate_not_eligibility(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[{"gap_state":"MET"}])["decision"],"BID_CANDIDATE")
    def test_18_closed_deadline_no_bid(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[],deadline_open=False)["reason"],"DEADLINE_CLOSED")
    def test_19_clock_exposes_missing(self):
        self.assertIn("clarification",critical_path_clock({"submission":"2026-09-02","clarification":None})["missing"])
    def test_20_clock_orders_known(self):
        self.assertEqual(critical_path_clock({"b":"2026-09-02","a":"2026-09-01"})["ordered"][0][0],"a")
    def test_21_finance_unknown_is_null(self):
        self.assertIsNone(null_safe_finance_object(estimated_value_eur=1600000)["retention_pct"])
    def test_22_finance_preserves_sourced_value(self):
        self.assertEqual(null_safe_finance_object(payment_days=30)["payment_days"],30)
    def test_23_reference_matrix_incomplete(self):
        self.assertFalse(reference_matrix(["roof","insulation"],[{"id":"r1","categories":["roof"]}])["complete"])
    def test_24_reference_matrix_complete(self):
        self.assertTrue(reference_matrix(["roof"],[{"id":"r1","categories":["roof"]}])["complete"])
    def test_25_pa4_requires_independence(self):
        self.assertFalse(blind_pa4_gate(same_packet_hash=True,reviewer_independent=False,reviewer_blinded=True,first_decision_hidden=True)["ready"])
    def test_26_pa4_all_conditions_ready(self):
        self.assertTrue(blind_pa4_gate(same_packet_hash=True,reviewer_independent=True,reviewer_blinded=True,first_decision_hidden=True)["ready"])
    def test_27_pa4_divergence_preserved(self):
        out=pa4_compare({"decision":"HOLD","fatal_gaps":["a"],"criteria":["x","y"]},{"decision":"HOLD","fatal_gaps":["b"],"criteria":["x"]})
        self.assertEqual(out["fatal_gap_symmetric_diff"],["a","b"])
    def test_28_decision_delta_requires_real_user(self):
        self.assertEqual(decision_delta("A","B",False)["status"],"HOLD_REAL_TARGET_USER_REQUIRED")
    def test_29_synthetic_metric_rejected(self):
        self.assertIsNone(observed_metric(10,"SYNTHETIC")["value"])
    def test_30_free_substitute_zero_residual_holds(self):
        self.assertEqual(substitute_residual_job(["alert","filter"],["alert","filter"])["status"],"HOLD_NO_PAID_RESIDUAL_JOB")
    def test_31_proof_receipts_fail_closed_without_real_evidence(self):
        self.assertNotEqual(pa5_object(real_user_class=None,before_decision=None,after_decision=None,interaction_artifact_hash=None,observed_at=None)["pa_grade"],"PA5")
        self.assertNotEqual(e3_object(source_type="SYNTHETIC",behavioral_cost_or_commitment="yes",artifact_hash="h")["evidence_grade"],"E3")
        self.assertNotEqual(e4_object(source_type="SYNTHETIC",amount_eur=100,transaction_id="t",artifact_hash="h")["evidence_grade"],"E4")
    def test_32_refresh_idempotent_and_stale_status_guard(self):
        h=refresh_preserve_history([], {"status":"Open"}); h2=refresh_preserve_history(h,{"status":"Open"})
        self.assertEqual(len(h2),1)
        self.assertEqual(stale_status_contradiction(deadline_passed=True,portal_status="Open")["status"],"REVALIDATE")

if __name__ == '__main__':
    unittest.main(verbosity=2)
