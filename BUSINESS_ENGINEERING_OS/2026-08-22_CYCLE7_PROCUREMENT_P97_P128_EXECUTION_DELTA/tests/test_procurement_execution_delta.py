import importlib.util
import unittest
from pathlib import Path
ENGINE=Path(__file__).parents[2]/"2026-08-22_CYCLE7_CROSS_LANE_READINESS_32_TO_64"/"engine"/"opportunity_readiness_compiler.py"
spec=importlib.util.spec_from_file_location("readiness",ENGINE); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
class T(unittest.TestCase):
 def test_01(self):
  case=m.OpportunityCase("PROC-BALLYBUNION-8872468",authority=m.AuthorityState.PARTIAL,profile_complete=False); self.assertEqual(m.decision_state(case,[]),m.DecisionState.HOLD_MISSING_AUTHORITY)
 def test_02(self):
  case=m.OpportunityCase("PROC-BALLYBUNION-8872468",authority=m.AuthorityState.PARTIAL,profile_complete=False); r=m.reason_graph(case,[m.GapState.UNKNOWN])["reasons"]; self.assertIn("AUTHORITY_INCOMPLETE",r); self.assertIn("CAPABILITY_PROFILE_INCOMPLETE",r)
 def test_03(self): self.assertEqual(m.next_evidence_action(["CAPABILITY_PROFILE_INCOMPLETE","AUTHORITY_INCOMPLETE"]),"ACQUIRE_OR_VERIFY_AUTHORITY")
 def test_04(self):
  case=m.OpportunityCase("PROC-BALLYBUNION-8872468",authority=m.AuthorityState.FULL,profile_complete=False); self.assertEqual(m.decision_state(case,[]),m.DecisionState.HOLD_CAPABILITY_EVIDENCE)
 def test_05(self):
  req=m.RequirementClaim("insurance",True,"pack:insurance",fatal_if_unmet=True); self.assertEqual(m.classify_gap(req,None),m.GapState.UNKNOWN)
 def test_06(self): self.assertEqual(m.authority_completeness(["notice","attachments"],["notice"]),m.AuthorityState.PARTIAL)
 def test_07(self):
  out=m.proof_invariants([{"case_id":"PROC-BALLYBUNION-8872468","public_only":True,"market_grade":"E3"}]); self.assertFalse(out["pass"])
 def test_08(self): self.assertEqual(m.next_evidence_action([]),"PROTECT_NO_CHANGE")
if __name__=="__main__": unittest.main()
