import importlib.util
from pathlib import Path
import unittest
P=Path(__file__).resolve().parents[1]/"runtime"/"convergence_guards.py"
spec=importlib.util.spec_from_file_location("cg",P); cg=importlib.util.module_from_spec(spec); spec.loader.exec_module(cg)
class T(unittest.TestCase):
 def test_collision(self):
  o=cg.namespace_collision_gate(cg.NamespaceClaim("B81","PUBLIC","A"),[cg.NamespaceClaim("B81","SHILLELAGH","B")]); self.assertFalse(o["allocation_allowed"])
 def test_same_owner(self):
  o=cg.namespace_collision_gate(cg.NamespaceClaim("BPUB","PUBLIC","A"),[cg.NamespaceClaim("bpub","public","B")]); self.assertTrue(o["allocation_allowed"])
 def test_stale_main(self):
  o=cg.concurrent_authority_restore(expected_main_sha="a",observed_main_sha="b",expected_library_physical_files=78,observed_library_physical_files=78,expected_open_pr_heads={},observed_open_pr_heads={},drive_current_pointer="x"); self.assertFalse(o["write_allowed"])
 def test_library_drift(self):
  o=cg.concurrent_authority_restore(expected_main_sha="a",observed_main_sha="a",expected_library_physical_files=71,observed_library_physical_files=78,expected_open_pr_heads={},observed_open_pr_heads={},drive_current_pointer="x"); self.assertFalse(o["write_allowed"])
 def test_pr_drift(self):
  o=cg.concurrent_authority_restore(expected_main_sha="a",observed_main_sha="a",expected_library_physical_files=78,observed_library_physical_files=78,expected_open_pr_heads={1:"a"},observed_open_pr_heads={1:"b"},drive_current_pointer="x"); self.assertFalse(o["write_allowed"])
 def test_fresh(self):
  o=cg.concurrent_authority_restore(expected_main_sha="a",observed_main_sha="a",expected_library_physical_files=78,observed_library_physical_files=78,expected_open_pr_heads={1:"a"},observed_open_pr_heads={1:"a"},drive_current_pointer="x"); self.assertTrue(o["write_allowed"]); self.assertFalse(o["authority_promotion"])
 def test_dataset_not_engine(self):
  o=cg.dataset_neq_engine(object_count=64,persisted=True,has_unique_runtime_contract=False); self.assertEqual(o["status"],"ADAPTER_OR_EVIDENCE_PACK")
 def test_candidate_no_promotion(self):
  o=cg.dataset_neq_engine(object_count=32,persisted=True,has_unique_runtime_contract=True); self.assertFalse(o["auto_core_promotion"])
 def test_delta9(self):
  o=cg.library_delta_after_cycle_gate(prior_count=69,current_count=78,enumerated_delta_ids=[str(i) for i in range(9)]); self.assertTrue(o["closure_allowed"])
 def test_delta8_holds(self):
  o=cg.library_delta_after_cycle_gate(prior_count=69,current_count=78,enumerated_delta_ids=[str(i) for i in range(8)]); self.assertFalse(o["closure_allowed"])
if __name__=="__main__": unittest.main()
