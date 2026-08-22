import unittest, importlib.util, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("c10",ROOT/"runtime/cycle10_governance.py")
m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)

class T(unittest.TestCase):
    def test01_decision_pass(self): self.assertEqual(m.decision_yield("d","u","t","p")["status"],"PASS_BOUNDED_META_ACTION")
    def test02_decision_hold(self): self.assertIn("decision",m.decision_yield(None,"u","t","p")["missing"])
    def test03_dup_merge(self): self.assertEqual(m.existing_mechanism_gate("A_B",["a b"]),"MERGE_WITH_EXISTING")
    def test04_new_candidate(self): self.assertEqual(m.existing_mechanism_gate("new",["old"]),"ALLOW_BOUNDED_CANDIDATE")
    def test05_si0016_collision(self): self.assertEqual(m.reservation_view(["SI-0015"],["SI-0016"],"SI-0016")["status"],"HOLD_ID_COLLISION")
    def test06_free_id_conditional(self): self.assertIn("AVAILABLE",m.reservation_view(["SI-0015"],["SI-0016"],"SI-0017")["status"])
    def test07_merge_collision_false(self): self.assertFalse(m.merge_time_collision(["SI-0017"],[],"SI-0017"))
    def test08_merge_free_true(self): self.assertTrue(m.merge_time_collision(["SI-0015"],["SI-0016"],"SI-0017"))
    def test09_family_collapse(self): self.assertEqual(m.evidence_family_counter([{"root":"x"},{"root":"x"},{"root":"y"}]),2)
    def test10_independent_families(self): self.assertEqual(m.independent_families([{"project":"A","root_evidence_family":"r","mechanism_identity":"m"},{"project":"A","root_evidence_family":"r","mechanism_identity":"m"},{"project":"B","root_evidence_family":"r2","mechanism_identity":"m"}]),2)
    def test11_replication_hold_one(self): self.assertEqual(m.replication_diversity([{"project":"A","outcome":"PASS","healthy_control":True}])["status"],"HOLD_REPLICATION_DIVERSITY")
    def test12_replication_pass_two(self): self.assertEqual(m.replication_diversity([{"project":"A","outcome":"PASS","healthy_control":True},{"project":"B","outcome":"PASS","healthy_control":True}])["status"],"PASS_DIVERSE_REPLICATION")
    def test13_false_positive(self): self.assertEqual(m.false_positive_control(True),"FAIL_FALSE_POSITIVE")
    def test14_control_pass(self): self.assertEqual(m.false_positive_control(False),"PASS_FALSE_POSITIVE_CONTROL")
    def test15_promotion_missing(self): self.assertEqual(m.promotion_tribunal({})["status"],"HOLD_INCOMPLETE_PROMOTION_BUNDLE")
    def test16_promotion_external_hold(self):
        b={k:True for k in ["application_target","rollback","readback","regression","source_provenance","evidence_boundary"]}; b.update(external_gate_required=True,external_gate_satisfied=False,independent_projects=2,required_independent_projects=2)
        self.assertEqual(m.promotion_tribunal(b)["status"],"HOLD_EXTERNAL_EVIDENCE")
    def test17_promotion_replication_hold(self):
        b={k:True for k in ["application_target","rollback","readback","regression","source_provenance","evidence_boundary"]}; b.update(external_gate_required=False,external_gate_satisfied=False,independent_projects=1,required_independent_projects=2)
        self.assertEqual(m.promotion_tribunal(b)["status"],"HOLD_REPLICATION_DIVERSITY")
    def test18_promotion_review_not_auto(self):
        b={k:True for k in ["application_target","rollback","readback","regression","source_provenance","evidence_boundary"]}; b.update(external_gate_required=False,external_gate_satisfied=False,independent_projects=2,required_independent_projects=2)
        self.assertEqual(m.promotion_tribunal(b)["status"],"PROMOTION_REVIEW_NOT_AUTO_PROMOTION")
    def test19_prune_duplicate(self): self.assertEqual(m.candidate_utility(True,True,True),"MERGE")
    def test20_prune_no_delta(self): self.assertEqual(m.candidate_utility(False,False,True),"PRUNE_LOW_INFORMATION")
    def test21_prune_expired(self): self.assertEqual(m.candidate_utility(True,False,False),"PRUNE_OR_HOLD_EXPIRED")
    def test22_prune_overhead(self): self.assertEqual(m.candidate_utility(True,False,True,10,5),"PRUNE_OVERHEAD_DOMINATES")
    def test23_keep_bounded(self): self.assertEqual(m.candidate_utility(True,False,True,5,10),"KEEP_BOUNDED")
    def test24_return_no_meta(self): self.assertEqual(m.production_return(False,"book"),"RETURN_TO_PRODUCTION")
    def test25_return_target_required(self): self.assertEqual(m.production_return(True,None),"HOLD_NO_RETURN_TARGET")
    def test26_return_bounded(self): self.assertEqual(m.production_return(True,"audio"),"META_BOUNDED_THEN_RETURN")
    def test27_rollback_pass(self): self.assertTrue(m.rollback_witness("a","b","a"))
    def test28_rollback_fail(self): self.assertFalse(m.rollback_witness("a","b","c"))
    def test29_private_drive(self): self.assertEqual(m.private_raw_policy("USER_UPLOAD_PRIVATE_REFERENCE"),"DRIVE_ONLY_POINTER_IN_GITHUB")
    def test30_gap_vector(self): self.assertEqual(m.evidence_gap_vector(["a"],["b"],["h"])["unknown"],["b"])
    def test31_overhead_null(self): self.assertIsNone(m.meta_overhead_ratio(None,10))
    def test32_overhead_ratio(self): self.assertEqual(m.meta_overhead_ratio(5,10),0.5)
    def test33_prompt_fingerprint_same_function(self):
        a={"consumer":"book","evidence_class":"E2","gate":"G","action_semantics":"repair","state_mutation":"none"}
        b={"consumer":" BOOK ","evidence_class":"e2","gate":"g","action_semantics":"REPAIR","state_mutation":"NONE"}
        self.assertEqual(m.prompt_functional_fingerprint(a),m.prompt_functional_fingerprint(b))
    def test34_prompt_dedupe_detects_functional_duplicate(self):
        base={"consumer":"book","evidence_class":"E2","gate":"G","action_semantics":"repair","state_mutation":"none"}
        cards=[dict(base,id="A"),dict(base,id="B")]
        self.assertEqual(m.dedupe_prompt_bank(cards)["status"],"MERGE_FUNCTIONAL_DUPLICATES")
    def test35_prompt_dedupe_unique(self):
        a={"id":"A","consumer":"book","evidence_class":"E2","gate":"G1","action_semantics":"repair","state_mutation":"none"}
        b={"id":"B","consumer":"book","evidence_class":"E2","gate":"G2","action_semantics":"repair","state_mutation":"none"}
        self.assertEqual(m.dedupe_prompt_bank([a,b])["unique"],2)
    def test36_voi_requires_decision_consumer(self):
        self.assertEqual(m.ordinal_voi_route([{"id":"x"}])["status"],"HOLD_NO_DECISION_CONSUMER")
    def test37_voi_prefers_information_then_burden(self):
        tests=[{"id":"a","decision_consumer":"D","decision_flip":1,"evidence_independence":1,"burden":3,"risk":1},{"id":"b","decision_consumer":"D","decision_flip":1,"evidence_independence":1,"burden":1,"risk":1}]
        self.assertEqual(m.ordinal_voi_route(tests)["selected"],"b")
    def test38_cost_of_delay_high(self): self.assertEqual(m.cost_of_delay_band("authority corruption risk"),"HIGH")
    def test39_cost_of_delay_medium(self): self.assertEqual(m.cost_of_delay_band("deadline causes rework"),"MEDIUM")
    def test40_selective_rollback_preserves_locked(self):
        graph={"A":["B","LOCK"],"B":["C"],"LOCK":["X"]}
        out=m.selective_rollback_plan("A",graph,{"LOCK"})
        self.assertEqual(set(out["revalidate"]),{"B","C"}); self.assertEqual(out["locked_preserved"],["LOCK"])
    def test41_asset_registry_pass(self):
        x={"filename":"a.bin","sha256":"a"*64,"size_bytes":1,"role":"fixture"}
        self.assertEqual(m.validate_asset_registry([x])["status"],"PASS")
    def test42_asset_registry_fail_hash(self):
        x={"filename":"a.bin","sha256":"bad","size_bytes":1,"role":"fixture"}
        self.assertEqual(m.validate_asset_registry([x])["status"],"FAIL_ASSET_REGISTRY")

if __name__=="__main__": unittest.main(verbosity=2)
