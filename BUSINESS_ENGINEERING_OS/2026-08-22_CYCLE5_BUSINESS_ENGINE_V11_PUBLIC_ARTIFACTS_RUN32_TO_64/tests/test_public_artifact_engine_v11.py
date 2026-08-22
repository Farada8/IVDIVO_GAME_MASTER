import unittest
from engine.public_artifact_engine_v11 import *

class PublicArtifactEngineV11Tests(unittest.TestCase):
    def source(self, sid="S", current=True):
        return SourceEvidence(sid,"title","https://example.com","authority","2026-08-20","2026-08-22",current)
    def req(self, verified=True, fatal=False):
        return Requirement("R","x",RequirementClass.MUST,"S",verified,fatal)
    def artifact(self, **kw):
        base=dict(artifact_id="A",opportunity_id="O",artifact_type="BRIEF",source_ids=("S",),requirements=(self.req(),),explicit_unknowns=("price",),hard_exclusions=("late",),buyer_role_public=None,budget_owner_public=None)
        base.update(kw); return PublicArtifact(**base)
    def test_public_source_valid(self): self.source().validate()
    def test_public_source_cannot_claim_market_plane(self):
        s=SourceEvidence("S","t","u","a",None,"r",True,evidence_plane=EvidencePlane.E)
        with self.assertRaises(BusinessArtifactError): s.validate()
    def test_lineage_rejects_old_value(self):
        old=TenderSnapshot("t","OLD","x","a","2026-08-20",None,245000,"Open",(),"x","SUPERSEDED")
        cur=TenderSnapshot("t","CUR","x","a","2026-09-10",None,None,"Open",(),"x","CURRENT")
        d=resolve_signal_lineage([old,cur]); self.assertEqual(d.rejected_inheritance["estimated_value_eur"],"OLD_VALUE_NOT_PROMOTED_TO_CURRENT")
    def test_lineage_one_current(self):
        s=TenderSnapshot("t","A","x","a",None,None,None,None,(),"x","CURRENT")
        with self.assertRaises(BusinessArtifactError): resolve_signal_lineage([s,s])
    def test_artifact_valid(self): self.artifact().validate()
    def test_artifact_requires_source(self):
        with self.assertRaises(BusinessArtifactError): self.artifact(source_ids=()).validate()
    def test_artifact_public_ceiling(self):
        with self.assertRaises(BusinessArtifactError): self.artifact(proof_level="E3").validate()
    def test_fatal_requirement_blocks(self):
        with self.assertRaises(BusinessArtifactError): self.artifact(requirements=(self.req(False,True),)).validate()
    def test_artifact_digest_stable(self): self.assertEqual(self.artifact().digest(),self.artifact().digest())
    def test_assessment_decision_change(self): self.assertEqual(assess_experiment(ArtifactExperiment("E","A","HOLD","KEEP",None,None,None,None,True)).verdict,ExperimentVerdict.KEEP)
    def test_assessment_missing_measurement_holds(self): self.assertEqual(assess_experiment(ArtifactExperiment("E","A","HOLD","HOLD",None,None,None,None,False)).verdict,ExperimentVerdict.HOLD)
    def test_assessment_no_delta_reshapes(self): self.assertEqual(assess_experiment(ArtifactExperiment("E","A","HOLD","HOLD",10,10,1,1,False)).verdict,ExperimentVerdict.RESHAPE)
    def test_time_saving_only_if_measured(self):
        x=assess_experiment(ArtifactExperiment("E","A","A","B",20,8,3,1,True)); self.assertEqual(x.time_saved_minutes,12); self.assertEqual(x.errors_reduced,2)
    def test_public_proof_ceiling(self): self.assertEqual(public_proof_level(),"E2_PLUS")
    def test_real_buyer_e3(self): self.assertEqual(public_proof_level(real_buyer_event=True),"E3")
    def test_real_payment_e4(self): self.assertEqual(public_proof_level(real_payment_event=True),"E4")
    def test_economics_null_without_actuals(self): self.assertIsNone(monetary_economics(actual_revenue_eur=None,actual_direct_cost_eur=1,measured_delivery_minutes=1))
    def test_economics_actuals(self): self.assertEqual(monetary_economics(actual_revenue_eur=100,actual_direct_cost_eur=20,measured_delivery_minutes=10)["actual_contribution_eur"],80)
    def test_buyer_role_unknown(self): self.assertEqual(buyer_role_gate(None,True)["grade"],"UNKNOWN")
    def test_buyer_role_public(self): self.assertEqual(buyer_role_gate("Procurement Officer",True)["grade"],"PUBLIC_ROLE")
    def test_payment_requires_evidence(self): self.assertEqual(payment_proof_gate({"event_type":"PURCHASE_ORDER"}),"NOT_E4")
    def test_payment_with_evidence(self): self.assertEqual(payment_proof_gate({"event_type":"PURCHASE_ORDER","evidence_ref":"po.pdf"}),"E4")
    def test_dependency_graph_semantic_only(self): self.assertEqual(build_artifact_dependency_graph([ArtifactDependency("deadline","brief",True),ArtifactDependency("a","b",False)]),{"deadline":("brief",)})
    def test_selective_invalidation(self): self.assertEqual(artifact_selective_invalidation({"deadline":("brief",),"brief":("decision",)},["deadline"])["dirty"],("brief","deadline","decision"))
    def test_selective_invalidation_locked(self): self.assertEqual(artifact_selective_invalidation({"deadline":("signed_bid",)},["deadline"],["signed_bid"])["blocked_locked"],("signed_bid",))
    def test_decision_value_changed(self): self.assertEqual(decision_value(DecisionLedgerEntry("e","o","s","HOLD","KEEP","r")),"DECISION_CHANGED")
    def test_decision_value_no_delta(self): self.assertEqual(decision_value(DecisionLedgerEntry("e","o","s","HOLD","HOLD","r")),"NO_DECISION_DELTA")
    def test_stop_gate(self):
        h=[ExperimentAssessment(ExperimentVerdict.HOLD,False,None,None,"x"),ExperimentAssessment(ExperimentVerdict.RESHAPE,False,0,0,"x")]
        self.assertEqual(artifact_stop_gate(h),"STOP_OR_CHANGE_HYPOTHESIS")
    def test_portfolio_independent_information(self):
        c=[PortfolioCandidate("A","tender",True,True,1),PortfolioCandidate("B","tender",True,True,2),PortfolioCandidate("C","retrofit",True,True,3),PortfolioCandidate("D","ai",True,True,4)]
        out=information_gain_portfolio(c); self.assertEqual(out["primary"],("A",)); self.assertEqual(out["pilots"],("C","D")); self.assertIn("B",out["held"])
    def test_si_observe_more(self): self.assertEqual(self_improvement_disposition(SelfImprovementObservation("O","p",("e",),1,True,True,True)),"OBSERVE_MORE")
    def test_si_protect_no_change(self): self.assertEqual(self_improvement_disposition(SelfImprovementObservation("O","p",("e",),2,True,True,False)),"PROTECT_NO_CHANGE")
    def test_si_candidate_review(self): self.assertEqual(self_improvement_disposition(SelfImprovementObservation("O","p",("e",),2,True,True,True)),"READY_FOR_BOUNDED_CANDIDATE_REVIEW")
    def test_prune_duplicate(self): self.assertEqual(mechanism_prune(duplicate=True,used_in_real_decision=True,false_positive_rate=0),"MERGE")
    def test_prune_false_positive(self): self.assertEqual(mechanism_prune(duplicate=False,used_in_real_decision=True,false_positive_rate=.5),"NARROW")
    def test_prune_unmeasured(self): self.assertEqual(mechanism_prune(duplicate=False,used_in_real_decision=False,false_positive_rate=None),"HOLD_TELEMETRY")
    def test_manifest_duplicate_blocks(self):
        with self.assertRaises(BusinessArtifactError): build_artifact_manifest([self.artifact(),self.artifact()])

if __name__ == "__main__": unittest.main()
