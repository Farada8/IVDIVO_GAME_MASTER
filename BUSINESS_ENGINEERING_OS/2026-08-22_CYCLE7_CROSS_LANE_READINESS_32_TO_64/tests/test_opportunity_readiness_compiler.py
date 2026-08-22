import sys
import unittest
from pathlib import Path

CYCLE_ROOT = Path(__file__).resolve().parents[1]
if str(CYCLE_ROOT) not in sys.path:
    sys.path.insert(0, str(CYCLE_ROOT))

from engine.opportunity_readiness_compiler import *

class Cycle7ReadinessTests(unittest.TestCase):
    def test_authority_full(self):
        self.assertEqual(authority_completeness(["a","b"],["a","b"]), AuthorityState.FULL)
    def test_authority_partial(self):
        self.assertEqual(authority_completeness(["a","b"],["a"]), AuthorityState.PARTIAL)
    def test_authority_intentional_partial(self):
        self.assertEqual(authority_completeness(["site"],[], intentionally_partial=True), AuthorityState.PARTIAL)
    def test_authority_missing(self):
        self.assertEqual(authority_completeness(["a"],[]), AuthorityState.MISSING)
    def test_profile_verified_only(self):
        claims=[CapabilityClaim("insurance","yes","src",True),CapabilityClaim("tax","yes",None,True)]
        self.assertEqual(profile_completeness(["insurance","tax"],claims)["missing"],["tax"])
    def test_join_preserves_unmatched(self):
        r=[RequirementClaim("insurance",True,"brief")]
        self.assertTrue(join_requirements(r,[])[0]["unmatched"])
    def test_unknown_not_fail(self):
        req=RequirementClaim("insurance",True,"brief",True)
        self.assertEqual(classify_gap(req,None),GapState.UNKNOWN)
    def test_curable_requires_deadline(self):
        req=RequirementClaim("insurance",True,"brief",True)
        self.assertEqual(classify_gap(req,None,can_cure=True,deadline_proven=False),GapState.UNKNOWN)
        self.assertEqual(classify_gap(req,None,can_cure=True,deadline_proven=True),GapState.CURABLE_BEFORE_DEADLINE)
    def test_noncurable_requires_proven_mismatch(self):
        req=RequirementClaim("license",True,"brief",True)
        cap=CapabilityClaim("license",False,"registry",True)
        self.assertEqual(classify_gap(req,cap,can_cure=False),GapState.NONCURABLE)
    def test_not_applicable(self):
        req=RequirementClaim("el",True,"brief")
        self.assertEqual(classify_gap(req,None,not_applicable=True),GapState.NOT_APPLICABLE)
    def test_irrelevant_reject(self):
        case=OpportunityCase("x",relevant=False)
        self.assertEqual(decision_state(case,[]),DecisionState.REJECT_IRRELEVANT)
    def test_missing_authority_holds(self):
        case=OpportunityCase("x",authority=AuthorityState.PARTIAL,profile_complete=True,technical_package_ready=True)
        self.assertEqual(decision_state(case,[]),DecisionState.HOLD_MISSING_AUTHORITY)
    def test_missing_profile_holds_after_full_authority(self):
        case=OpportunityCase("x",authority=AuthorityState.FULL,profile_complete=False)
        self.assertEqual(decision_state(case,[]),DecisionState.HOLD_CAPABILITY_EVIDENCE)
    def test_unknown_gap_holds(self):
        case=OpportunityCase("x",authority=AuthorityState.FULL,profile_complete=True,technical_package_ready=True)
        self.assertEqual(decision_state(case,[GapState.UNKNOWN]),DecisionState.HOLD_REQUIREMENT_GAPS)
    def test_technical_package_gate(self):
        case=OpportunityCase("x",authority=AuthorityState.FULL,profile_complete=True,technical_package_ready=False)
        self.assertEqual(decision_state(case,[GapState.MET]),DecisionState.HOLD_TECHNICAL_PACKAGE)
    def test_ready_for_independent_review(self):
        case=OpportunityCase("x",authority=AuthorityState.FULL,profile_complete=True,technical_package_ready=True,independent_review_ready=False)
        self.assertEqual(decision_state(case,[GapState.MET]),DecisionState.READY_FOR_INDEPENDENT_REVIEW)
    def test_reason_graph(self):
        case=OpportunityCase("x",authority=AuthorityState.PARTIAL,profile_complete=False)
        result=reason_graph(case,[GapState.UNKNOWN])
        self.assertIn("AUTHORITY_INCOMPLETE",result["reasons"])
        self.assertIn("CAPABILITY_PROFILE_INCOMPLETE",result["reasons"])
    def test_next_action_authority_first(self):
        self.assertEqual(next_evidence_action(["TECHNICAL_OR_PROPOSAL_PACKAGE_INCOMPLETE","AUTHORITY_INCOMPLETE"]),"ACQUIRE_OR_VERIFY_AUTHORITY")
    def test_repeated_missing_authority_candidate(self):
        result=recurring_missing_authority([{"case_id":"proc","missing_required_authority":True},{"case_id":"art","missing_required_authority":True}])
        self.assertTrue(result["candidate"])
        self.assertEqual(result["scope"],"BUSINESS_ENGINEERING")
    def test_public_to_market_leak(self):
        self.assertFalse(proof_invariants([{"case_id":"x","public_only":True,"market_grade":"E3"}])["pass"])
    def test_official_brief_not_applicant_ready(self):
        rec={"case_id":"art","public_only":True,"market_grade":"E2+","official_brief_validated":True,"applicant_ready":True,"applicant_evidence":False}
        self.assertFalse(proof_invariants([rec])["pass"])
    def test_unknown_neither_pass_nor_fail(self):
        self.assertFalse(proof_invariants([{"case_id":"x","unknown_treated_as_pass":True}])["pass"])
        self.assertFalse(proof_invariants([{"case_id":"x","unknown_treated_as_fail":True}])["pass"])

if __name__ == "__main__": unittest.main()
