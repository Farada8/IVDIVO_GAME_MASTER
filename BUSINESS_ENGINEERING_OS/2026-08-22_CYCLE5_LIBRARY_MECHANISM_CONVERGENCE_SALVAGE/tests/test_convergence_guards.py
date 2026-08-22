import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / "runtime" / "convergence_guards.py"
spec = importlib.util.spec_from_file_location("cg", P)
cg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cg)


class ConvergenceGuardTests(unittest.TestCase):
    def test_namespace_collision_blocks_different_owner(self):
        out = cg.namespace_collision_gate(
            cg.NamespaceClaim("B81", "PUBLIC_REGULATORY", "A"),
            [cg.NamespaceClaim("B81", "SHILLELAGH_VERTICAL", "B")],
        )
        self.assertEqual(out["status"], "HOLD_NAMESPACE_COLLISION")
        self.assertFalse(out["allocation_allowed"])
        self.assertFalse(out["auto_rename"])

    def test_namespace_same_owner_reuse_passes(self):
        out = cg.namespace_collision_gate(
            cg.NamespaceClaim("BPUB", "PUBLIC_REGULATORY", "A2"),
            [cg.NamespaceClaim("bpub", "public_regulatory", "A1")],
        )
        self.assertTrue(out["allocation_allowed"])

    def test_stale_main_blocks_write(self):
        out = cg.concurrent_authority_restore(
            expected_main_sha="old", observed_main_sha="new",
            expected_library_physical_files=78, observed_library_physical_files=78,
            expected_open_pr_heads={}, observed_open_pr_heads={},
            drive_current_pointer="drive://current",
        )
        self.assertFalse(out["write_allowed"])
        self.assertIn("main_sha", out["drift"])

    def test_library_count_drift_blocks_write(self):
        out = cg.concurrent_authority_restore(
            expected_main_sha="same", observed_main_sha="same",
            expected_library_physical_files=71, observed_library_physical_files=78,
            expected_open_pr_heads={}, observed_open_pr_heads={},
            drive_current_pointer="drive://current",
        )
        self.assertFalse(out["write_allowed"])

    def test_relevant_pr_head_drift_blocks_write(self):
        out = cg.concurrent_authority_restore(
            expected_main_sha="same", observed_main_sha="same",
            expected_library_physical_files=78, observed_library_physical_files=78,
            expected_open_pr_heads={190: "a"}, observed_open_pr_heads={190: "b"},
            drive_current_pointer="drive://current",
        )
        self.assertFalse(out["write_allowed"])

    def test_fresh_authority_pass_never_promotes(self):
        out = cg.concurrent_authority_restore(
            expected_main_sha="same", observed_main_sha="same",
            expected_library_physical_files=78, observed_library_physical_files=78,
            expected_open_pr_heads={190: "a"}, observed_open_pr_heads={190: "a"},
            drive_current_pointer="drive://current",
        )
        self.assertTrue(out["write_allowed"])
        self.assertFalse(out["authority_promotion"])

    def test_persisted_dataset_is_not_engine(self):
        out = cg.dataset_neq_engine(object_count=64, persisted=True, has_unique_runtime_contract=False)
        self.assertEqual(out["status"], "ADAPTER_OR_EVIDENCE_PACK")
        self.assertFalse(out["auto_core_promotion"])

    def test_engine_candidate_still_not_auto_promoted(self):
        out = cg.dataset_neq_engine(object_count=32, persisted=True, has_unique_runtime_contract=True)
        self.assertEqual(out["status"], "ENGINE_REVIEW_CANDIDATE")
        self.assertFalse(out["auto_core_promotion"])

    def test_69_to_78_requires_nine_unique_ids(self):
        out = cg.library_delta_after_cycle_gate(
            prior_count=69, current_count=78,
            enumerated_delta_ids=[f"d{i}" for i in range(9)],
        )
        self.assertTrue(out["closure_allowed"])

    def test_incomplete_delta_holds(self):
        out = cg.library_delta_after_cycle_gate(
            prior_count=69, current_count=78,
            enumerated_delta_ids=[f"d{i}" for i in range(8)],
        )
        self.assertFalse(out["closure_allowed"])


if __name__ == "__main__":
    unittest.main()
