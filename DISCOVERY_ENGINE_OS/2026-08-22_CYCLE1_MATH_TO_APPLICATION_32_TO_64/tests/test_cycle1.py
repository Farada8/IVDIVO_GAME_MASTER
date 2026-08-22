import unittest, json, sys
from pathlib import Path
ROOT=Path(__file__).parents[1]
sys.path.insert(0,str(ROOT/"engine"))
from discovery_engine import *

class DiscoveryCycle1Tests(unittest.TestCase):
    def test_01_absence_gate(self):
        self.assertEqual(bounded_absence_gate(0,100),"NOVELTY_UNVERIFIED")
    def test_02_prior_art_found(self):
        self.assertEqual(bounded_absence_gate(1,100),"PRIOR_ART_FOUND")
    def test_03_claim_atomization(self):
        self.assertEqual(len(atomize_claim("A and B; C")),3)
    def test_04_novelty_planes(self):
        self.assertEqual(set(novelty_planes()),set(PLANES))
    def test_05_square_recovery(self):
        r=sequence_discovery([n*n for n in range(12)])
        self.assertLess(r["rmse"],1e-12); self.assertAlmostEqual(r["coefficients"][2],1.0,places=12)
    def test_06_forest_control(self):
        candidate=lambda n,e:(cyclomatic(n,e)!=0) or (len(e)==n-graph_components(n,e))
        r=exhaustive_graph_counterexample(candidate,5)
        self.assertFalse(r["found"]); self.assertEqual(r["checked"],1099)
    def test_07_false_graph_conjecture(self):
        r=exhaustive_graph_counterexample(lambda n,e:graph_triangles(n,e)<=max(0,cyclomatic(n,e)),5)
        self.assertTrue(r["found"]); self.assertEqual(r["n"],4)
    def test_08_k4_violation(self):
        edges=list(itertools.combinations(range(4),2))
        self.assertGreater(graph_triangles(4,edges),cyclomatic(4,edges))
    def test_09_logistic_recovery(self):
        r=logistic_symbolic_regression(3.2,180,.173)
        self.assertLess(r["rmse"],1e-12)
    def test_10_logistic_linear(self):
        r=logistic_symbolic_regression(3.2,180,.173)
        self.assertAlmostEqual(r["coefficients"][1],3.2,places=10)
    def test_11_logistic_quadratic(self):
        r=logistic_symbolic_regression(3.2,180,.173)
        self.assertAlmostEqual(r["coefficients"][2],-3.2,places=10)
    def test_12_binpack_hidden_failure(self):
        self.assertFalse(binpack_policy_benchmark()["generalizes"])
    def test_13_binpack_train_winner(self):
        self.assertEqual(binpack_policy_benchmark()["train_selected"]["policy"],"TIGHT_OR_SPREAD")
    def test_14_context_c1(self):
        self.assertEqual(context_refinement_fixture()["c1_classes"],2)
    def test_15_context_combined(self):
        self.assertEqual(context_refinement_fixture()["combined_classes"],4)
    def test_16_transfer_requires_negative(self):
        self.assertEqual(transfer_certificate("m","a","b",True,False)["status"],"INCONCLUSIVE")
    def test_17_transfer_candidate(self):
        self.assertEqual(transfer_certificate("m","a","b",True,True)["status"],"APPLICATION_CANDIDATE")
    def test_18_patent_exact(self):
        r=patent_triage(["sensor","threshold","alarm"],{"R1":["sensor","threshold","alarm"]})
        self.assertEqual(r["novelty_triage"],"NOT_NOVEL_SINGLE_REFERENCE")
    def test_19_patent_combo_hold(self):
        r=patent_triage(["sensor","adaptive","dashboard"],{"R1":["sensor","adaptive"],"R2":["dashboard"]})
        self.assertEqual(r["status"],"PATENT_TRIAGE_HOLD")
    def test_20_patent_inventive_unresolved(self):
        r=patent_triage(["sensor","adaptive","dashboard"],{"R1":["sensor","adaptive"],"R2":["dashboard"]})
        self.assertEqual(r["inventive_step"],"UNRESOLVED")
    def test_21_no_legal_opinion(self):
        r=patent_triage(["a"],{"R1":["a"]}); self.assertFalse(r["legal_opinion"])
    def test_22_observational_firewall(self):
        self.assertEqual(causal_claim_gate("OBSERVATIONAL"),"ASSOCIATIONAL_ONLY")
    def test_23_intervention_gate(self):
        self.assertEqual(causal_claim_gate("RANDOMIZED_INTERVENTION"),"CAUSAL_CLAIM_POSSIBLE_WITH_ASSUMPTIONS")
    def test_24_trl_concept(self):
        self.assertEqual(trl_gate(False,False,False),"TRL0_CONCEPT")
    def test_25_trl_lab(self):
        self.assertEqual(trl_gate(True,True,False),"TRL3_4_LAB_PROTOTYPE")
    def test_26_portfolio_excludes_rediscovery(self):
        c=[{"id":"A","status":"REDISCOVERY","falsifiability":9,"application_breadth":9},{"id":"B","status":"APPLICATION_CANDIDATE","falsifiability":1,"application_breadth":1}]
        self.assertEqual(discovery_portfolio(c,1)[0]["id"],"B")
    def test_27_naive_false_new(self):
        self.assertEqual(self_improvement_fixture()["naive_false_new"],5)
    def test_28_evidence_false_new(self):
        self.assertEqual(self_improvement_fixture()["evidence_false_new"],0)
    def test_29_local_keep(self):
        self.assertEqual(self_improvement_fixture()["candidate_status"],"LOCAL_KEEP")
    def test_30_no_global_promotion(self):
        self.assertFalse(self_improvement_fixture()["global_authority_promotion"])
    def test_31_closure_accepts_no_new(self):
        self.assertTrue(close_discovery([{"status":"REDISCOVERY"},{"status":"NOVELTY_UNVERIFIED"}])["can_close"])
    def test_32_closure_blocks_new(self):
        self.assertFalse(close_discovery([{"status":"NEW"}])["can_close"])

if __name__=="__main__": unittest.main()
