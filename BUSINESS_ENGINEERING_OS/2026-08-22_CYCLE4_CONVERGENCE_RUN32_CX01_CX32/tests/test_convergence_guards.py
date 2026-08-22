import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / "engine" / "convergence_guards.py"
spec = importlib.util.spec_from_file_location("cg", P)
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)


class ConvergenceGuardTests(unittest.TestCase):
    def test_namespace_collision_blocks_different_owner(self):
        result = cg.namespace_collision_gate(
            cg.NamespaceClaim("B81", "PUBLIC_REGULATORY", "A"),
            [cg.NamespaceClaim("B81", "SHILLELAGH_VERTICAL", "B")],
        )
        self.assertEqual(result["status"], "HOLD_NAMESPACE_COLLISION")
        self.assertFalse(result["allocation_allowed"])
        self.assertFalse(result["auto_rename"])

    def test_namespace_same_owner_can_reuse(self):
        result = cg.namespace_collision_gate(
            cg.NamespaceClaim("BPUB", "PUBLIC_REGULATORY", "A2"),
            [cg.NamespaceClaim("bpub", "public_regulatory", "A1")],
        )
        self.assertTrue(result["allocation_allowed"])

    def test_authority_main_drift_blocks_write(self):
        result = cg.concurrent_authority_restore(
            expected_main_sha="old", observed_main_sha="new",
            expected_library_physical_files=78, observed_library_physical_files=78,
            expected_open_pr_heads={172: "x"}, observed_open_pr_heads={172: "x"},
            drive_current_pointer="drive://current",
        )
        self.assertFalse(result["write_allowed"])
        self.assertIn("main_sha", result["drift"])

    def test_authority_library_delta_blocks_write(self):
        result = cg.concurrent_authority_restore(
            expected_main_sha="same", observed_main_sha="same",
            expected_library_physical_files=71, observed_library_physical_files=78,
            expected_open_pr_heads={}, observed_open_pr_heads={},
            drive_current_pointer="drive://current",
        )
        self.assertFalse(result["write_allowed"])

    def test_authority_pr_head_drift_blocks_write(self):
        result = cg.concurrent_authority_restore(
            expected_main_sha="same", observed_main_sha="same",
            expected_library_physical_files=78, observed_library_physical_files=78,
            expected_open_pr_heads={172: "a"}, observed_open_pr_heads={172: "b"},
            drive_current_pointer="drive://current",
        )
        self.assertFalse(result["write_allowed"])

    def test_fresh_authority_passes_without_promotion(self):
        result = cg.concurrent_authority_restore(
            expected_main_sha="same", observed_main_sha="same",
            expected_library_physical_files=78, observed_library_physical_files=78,
            expected_open_pr_heads={172: "a"}, observed_open_pr_heads={172: "a"},
            drive_current_pointer="drive://current",
        )
        self.assertTrue(result["write_allowed"])
        self.assertFalse(result["authority_promotion"])

    def test_dataset_persistence_is_not_engine(self):
        result = cg.dataset_neq_engine(object_count=64, persisted=True, has_unique_runtime_contract=False)
        self.assertEqual(result["status"], "ADAPTER_OR_EVIDENCE_PACK")
        self.assertFalse(result["auto_core_promotion"])

    def test_dataset_engine_candidate_still_not_promoted(self):
        result = cg.dataset_neq_engine(object_count=32, persisted=True, has_unique_runtime_contract=True)
        self.assertEqual(result["status"], "ENGINE_REVIEW_CANDIDATE")
        self.assertFalse(result["auto_core_promotion"])

    def test_library_delta_69_to_78_passes_with_nine_ids(self):
        result = cg.library_delta_after_cycle_gate(
            prior_count=69, current_count=78,
            enumerated_delta_ids=[f"d{i}" for i in range(9)],
        )
        self.assertEqual(result["status"], "PASS_LIBRARY_DELTA_ENUMERATED")
        self.assertTrue(result["closure_allowed"])

    def test_library_delta_incomplete_holds(self):
        result = cg.library_delta_after_cycle_gate(
            prior_count=69, current_count=78,
            enumerated_delta_ids=[f"d{i}" for i in range(8)],
        )
        self.assertFalse(result["closure_allowed"])


if __name__ == "__main__":
    unittest.main()
