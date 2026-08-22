import unittest
import pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "engine"))
from proof_transition_engine import *

class Cycle7EngineTests(unittest.TestCase):
    def test_01_pack_non_authority_blocks(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=True,revision_inventory_complete=True,authoritative_source=False)["status"],"BLOCKED_NONAUTHORITATIVE_SOURCE")
    def test_02_pack_auth_required(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=False,attachment_inventory_complete=False,revision_inventory_complete=False,authoritative_source=True)["status"],"BLOCKED_AUTHENTICATED_OR_USER_PACK_REQUIRED")
    def test_03_pack_attachment_incomplete(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=False,revision_inventory_complete=True,authoritative_source=True)["status"],"BLOCKED_ATTACHMENT_INVENTORY_INCOMPLETE")
    def test_04_pack_revision_incomplete(self):
        self.assertEqual(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=True,revision_inventory_complete=False,authoritative_source=True)["status"],"BLOCKED_REVISION_INVENTORY_INCOMPLETE")
    def test_05_pack_complete(self):
        self.assertTrue(pack_acquisition_status(authenticated_or_user_pack=True,attachment_inventory_complete=True,revision_inventory_complete=True,authoritative_source=True)["pack_complete"])
    def test_06_supplier_missing_stays_hold(self):
        out=supplier_profile_status({}, {})
        self.assertFalse(out["verified"]); self.assertIn("insurance",out["missing"])
    def test_07_supplier_unsourced_stays_hold(self):
        fields={k:"x" for k in REQUIRED_SUPPLIER_FIELDS}; prov={}
        self.assertIn("insurance",supplier_profile_status(fields,prov)["unsourced"])
    def test_08_supplier_verified(self):
        fields={k:"x" for k in REQUIRED_SUPPLIER_FIELDS}; prov={k:"src" for k in REQUIRED_SUPPLIER_FIELDS}
        self.assertTrue(supplier_profile_status(fields,prov)["verified"])
    def test_09_join_unknown(self):
        self.assertEqual(join_requirements([{"field":"turnover"}],{})[0]["gap_state"],"UNKNOWN")
    def test_10_join_noncurable_min(self):
        self.assertEqual(join_requirements([{"field":"turnover","min":100}],{"turnover":50})[0]["gap_state"],"NONCURABLE")
    def test_11_join_not_applicable(self):
        self.assertEqual(join_requirements([{"field":"x","required":False}],{})[0]["gap_state"],"NOT_APPLICABLE")
    def test_12_decision_pack_hold(self):
        self.assertEqual(route_bid_decision(pack_complete=False,profile_verified=True,joined=[])["reason"],"INCOMPLETE_OFFICIAL_PACK")
    def test_13_decision_profile_hold(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=False,joined=[])["reason"],"UNVERIFIED_SUPPLIER_PROFILE")
    def test_14_decision_noncurable_no_bid(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[{"gap_state":"NONCURABLE"}])["decision"],"NO_BID")
    def test_15_decision_unknown_hold(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[{"gap_state":"UNKNOWN"}])["decision"],"HOLD")
    def test_16_decision_candidate_only_all_met(self):
        self.assertEqual(route_bid_decision(pack_complete=True,profile_verified=True,joined=[{"gap_state":"MET"}])["decision"],"BID_CANDIDATE")
    def test_17_clock_keeps_missing(self):
        out=critical_path_clock({"submission":"2026-09-02T17:00:00+01:00","clarification":None})
        self.assertIn("clarification",out["missing"])
    def test_18_finance_null_safe(self):
        self.assertIsNone(null_safe_finance_object(estimated_value_eur=1600000)["retention_pct"])
    def test_19_reference_matrix_incomplete(self):
        self.assertFalse(reference_matrix(["roof","insulation"],[{"id":"r1","categories":["roof"]}])["complete"])
    def test_20_hash_deterministic(self):
        self.assertEqual(public_artifact_hash("p","1",{"a":1}),public_artifact_hash("p","1",{"a":1}))
    def test_21_pa4_needs_blind_independence(self):
        self.assertFalse(blind_pa4_gate(same_packet_hash=True,reviewer_independent=False,reviewer_blinded=True,first_decision_hidden=True)["ready"])
    def test_22_pa4_ready_all_true(self):
        self.assertTrue(blind_pa4_gate(same_packet_hash=True,reviewer_independent=True,reviewer_blinded=True,first_decision_hidden=True)["ready"])
    def test_23_pa4_compare_divergence(self):
        out=pa4_compare({"decision":"HOLD","fatal_gaps":["a"],"criteria":["x","y"]},{"decision":"HOLD","fatal_gaps":["b"],"criteria":["x"]})
        self.assertEqual(out["fatal_gap_symmetric_diff"],["a","b"]); self.assertEqual(out["missed_criteria"],["y"])
    def test_24_decision_delta_requires_real_user(self):
        self.assertEqual(decision_delta("A","B",False)["status"],"HOLD_REAL_TARGET_USER_REQUIRED")
    def test_25_observed_metric_requires_real_source(self):
        self.assertIsNone(observed_metric(10,"SYNTHETIC")["value"])
    def test_26_substitute_no_residual_holds(self):
        self.assertEqual(substitute_residual_job(["alert","filter"],["alert","filter"])["status"],"HOLD_NO_PAID_RESIDUAL_JOB")
    def test_27_stale_status_revalidates(self):
        self.assertEqual(stale_status_contradiction(deadline_passed=True,portal_status="Open")["status"],"REVALIDATE")
    def test_28_refresh_idempotent(self):
        h=refresh_preserve_history([], {"status":"Open"}); h2=refresh_preserve_history(h,{"status":"Open"})
        self.assertEqual(len(h2),1)
    def test_29_wip_max_three(self):
        self.assertEqual(wip_guard("OP01",["OP03","OP19"])["status"],"PASS"); self.assertEqual(wip_guard("OP01",["OP03","OP19","X"])["status"],"FAIL")
    def test_30_si_requires_repeat_case(self):
        self.assertEqual(self_improvement_candidate(defect="x",cases=1,repair="y",evidence_hashes=["h"])["status"],"DISCOVERY_ONLY")
    def test_31_pa5_e3_e4_fail_closed_without_real(self):
        self.assertNotEqual(pa5_object(real_user_class=None,before_decision=None,after_decision=None,interaction_artifact_hash=None,observed_at=None)["pa_grade"],"PA5")
        self.assertNotEqual(e3_object(source_type="SYNTHETIC",behavioral_cost_or_commitment="yes",artifact_hash="h")["evidence_grade"],"E3")
        self.assertNotEqual(e4_object(source_type="SYNTHETIC",amount_eur=100,transaction_id="t",artifact_hash="h")["evidence_grade"],"E4")
    def test_32_cycle6_close_requires_all_surfaces(self):
        self.assertFalse(cycle_close_gate(core_merged=True,cross_lane_merged=True,drive_readback=True,current_authority_reconciled=False)["closed"])
        self.assertTrue(cycle_close_gate(core_merged=True,cross_lane_merged=True,drive_readback=True,current_authority_reconciled=True)["closed"])

if __name__ == '__main__':
    unittest.main(verbosity=2)
