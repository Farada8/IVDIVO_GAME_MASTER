import importlib.util
import unittest
from pathlib import Path

ENGINE = Path(__file__).parents[2] / "2026-08-22_CYCLE7_CROSS_LANE_READINESS_32_TO_64" / "engine" / "opportunity_readiness_compiler.py"
spec = importlib.util.spec_from_file_location("readiness", ENGINE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class ProcurementExecutionDeltaTests(unittest.TestCase):
    def test_ballybunion_missing_full_pack_holds_authority(self):
        case = m.OpportunityCase("PROC-BALLYBUNION-8872468", authority=m.AuthorityState.PARTIAL, profile_complete=False)
        self.assertEqual(m.decision_state(case, []), m.DecisionState.HOLD_MISSING_AUTHORITY)

    def test_reason_graph_preserves_both_missing_authority_and_profile(self):
        case = m.OpportunityCase("PROC-BALLYBUNION-8872468", authority=m.AuthorityState.PARTIAL, profile_complete=False)
        reasons = m.reason_graph(case, [m.GapState.UNKNOWN])["reasons"]
        self.assertIn("AUTHORITY_INCOMPLETE", reasons)
        self.assertIn("CAPABILITY_PROFILE_INCOMPLETE", reasons)

    def test_next_action_is_authority_before_supplier_join(self):
        self.assertEqual(m.next_evidence_action(["CAPABILITY_PROFILE_INCOMPLETE","AUTHORITY_INCOMPLETE"]), "ACQUIRE_OR_VERIFY_AUTHORITY")

    def test_full_authority_without_verified_profile_still_holds(self):
        case = m.OpportunityCase("PROC-BALLYBUNION-8872468", authority=m.AuthorityState.FULL, profile_complete=False)
        self.assertEqual(m.decision_state(case, []), m.DecisionState.HOLD_CAPABILITY_EVIDENCE)

    def test_missing_supplier_evidence_is_unknown_not_met_or_noncurable(self):
        req = m.RequirementClaim("insurance", True, "pack:insurance", fatal_if_unmet=True)
        self.assertEqual(m.classify_gap(req, None), m.GapState.UNKNOWN)

    def test_partial_public_notice_does_not_become_full_pack(self):
        self.assertEqual(m.authority_completeness(["notice","attachments"],["notice"]), m.AuthorityState.PARTIAL)

    def test_public_evidence_cannot_launder_to_e3(self):
        out = m.proof_invariants([{"case_id":"PROC-BALLYBUNION-8872468","public_only":True,"market_grade":"E3"}])
        self.assertFalse(out["pass"])
        self.assertIn(("PROC-BALLYBUNION-8872468","PUBLIC_TO_MARKET_LEAK"), out["violations"])

    def test_no_new_admissible_blocker_returns_protect_no_change(self):
        self.assertEqual(m.next_evidence_action([]), "PROTECT_NO_CHANGE")

if __name__ == "__main__":
    unittest.main()
