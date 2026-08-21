import json
import tempfile
import unittest
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from post_render_engineering import (
    PatchLedger,
    file_sha256,
    stage_router,
    validate_patch_plan,
    validate_regression_ranges,
    verify_json_artifact,
)

SHA_A = "a" * 64
SHA_B = "b" * 64


class PostRenderEngineeringTests(unittest.TestCase):
    def write_json(self, root, name, obj):
        path = Path(root) / name
        path.write_text(json.dumps(obj), encoding="utf-8")
        return path

    def test_file_existence_without_semantic_pass_is_not_evidence(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.write_json(d, "artifact.json", {"schema_version": "x/1", "status": "HOLD"})
            out = verify_json_artifact(path, expected_schema_prefix="x/")
            self.assertFalse(out["verified"])
            self.assertEqual(out["status"], "HOLD_SEMANTIC_STATUS")

    def test_verified_artifact_checks_schema_and_hash(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.write_json(d, "artifact.json", {"schema_version": "x/1", "status": "PASS"})
            sha = file_sha256(path)
            out = verify_json_artifact(path, expected_schema_prefix="x/", expected_sha256=sha)
            self.assertTrue(out["verified"])
            self.assertEqual(out["sha256"], sha)

    def test_artifact_hash_drift_fails(self):
        with tempfile.TemporaryDirectory() as d:
            path = self.write_json(d, "artifact.json", {"schema_version": "x/1", "status": "PASS"})
            out = verify_json_artifact(path, expected_sha256=SHA_A)
            self.assertEqual(out["status"], "FAIL_HASH_DRIFT")

    def test_patch_ledger_reuses_regression_pass(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = PatchLedger(Path(d) / "ledger.json")
            self.assertEqual(ledger.plan(patch_id="P1", authorization_hash=SHA_A, source_master_sha256=SHA_B), "PLANNED")
            ledger.transition("P1", "AUTHORIZED")
            ledger.transition("P1", "RENDERED", rendered_sha256="c" * 64)
            ledger.transition("P1", "REGRESSION_PASS", regression_sha256="d" * 64)
            reopened = PatchLedger(Path(d) / "ledger.json")
            self.assertEqual(reopened.plan(patch_id="P1", authorization_hash=SHA_A, source_master_sha256=SHA_B), "REUSE_REGRESSION_PASS")

    def test_patch_identity_drift_holds(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = PatchLedger(Path(d) / "ledger.json")
            ledger.plan(patch_id="P1", authorization_hash=SHA_A, source_master_sha256=SHA_B)
            self.assertEqual(ledger.plan(patch_id="P1", authorization_hash="c" * 64, source_master_sha256=SHA_B), "HOLD_IDENTITY_DRIFT")

    def test_terminal_human_pass_is_immutable(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = PatchLedger(Path(d) / "ledger.json")
            ledger.plan(patch_id="P1", authorization_hash=SHA_A, source_master_sha256=SHA_B)
            ledger.transition("P1", "AUTHORIZED")
            ledger.transition("P1", "RENDERED")
            ledger.transition("P1", "REGRESSION_PASS")
            ledger.transition("P1", "HUMAN_PASS", human_evidence_sha256="e" * 64)
            with self.assertRaisesRegex(ValueError, "TERMINAL_PATCH_ATTEMPT_IMMUTABLE"):
                ledger.transition("P1", "REJECTED")

    def test_invalid_patch_lifecycle_transition_fails(self):
        with tempfile.TemporaryDirectory() as d:
            ledger = PatchLedger(Path(d) / "ledger.json")
            ledger.plan(patch_id="P1", authorization_hash=SHA_A, source_master_sha256=SHA_B)
            with self.assertRaisesRegex(ValueError, "PATCH_TRANSITION_INVALID"):
                ledger.transition("P1", "REGRESSION_PASS")

    def test_patch_plan_requires_authorization_hash(self):
        with self.assertRaisesRegex(ValueError, "PATCH_AUTHORIZATION_HASH_MISSING"):
            validate_patch_plan({"patches": [{
                "patch_id": "P1", "interval_start_seconds": 0, "interval_end_seconds": 1,
                "source_master_sha256": SHA_A,
            }]})

    def test_project_neutral_regression_passes_authorized_change(self):
        out = validate_regression_ranges(
            SHA_A, SHA_B,
            authorized_ranges=[{"start_seconds": 1, "end_seconds": 2}],
            protected_ranges=[{"start_seconds": 3, "end_seconds": 4}],
            changed_ranges=[{"start_seconds": 1.1, "end_seconds": 1.8}],
        )
        self.assertEqual(out["status"], "PASS")

    def test_regression_rejects_unauthorized_change(self):
        out = validate_regression_ranges(
            SHA_A, SHA_B,
            authorized_ranges=[{"start_seconds": 1, "end_seconds": 2}],
            protected_ranges=[],
            changed_ranges=[{"start_seconds": 2.2, "end_seconds": 2.4}],
        )
        self.assertEqual(out["status"], "FAIL")
        self.assertEqual(out["violations"][0]["type"], "UNAUTHORIZED_CHANGE")

    def test_regression_rejects_protected_change_even_if_authorized(self):
        out = validate_regression_ranges(
            SHA_A, SHA_B,
            authorized_ranges=[{"start_seconds": 1, "end_seconds": 4}],
            protected_ranges=[{"start_seconds": 2, "end_seconds": 3}],
            changed_ranges=[{"start_seconds": 2.2, "end_seconds": 2.4}],
        )
        types = {row["type"] for row in out["violations"]}
        self.assertIn("PROTECTED_RANGE_CHANGED", types)

    def test_router_advances_only_verified_semantic_evidence(self):
        evidence = {
            "master": {"verified": True, "status": "PASS", "sha256": SHA_A},
            "lineage": {"verified": True, "status": "PASS", "sha256": SHA_B},
            "timing": {"verified": False, "status": "FILE_EXISTS_ONLY"},
        }
        out = stage_router(evidence)
        self.assertEqual(out["next_stage"], "ACCEPTED_TIMING")
        self.assertEqual(out["stages"][2]["status"], "READY_OR_HOLD")
        self.assertEqual(out["stages"][3]["status"], "BLOCKED_UPSTREAM")


if __name__ == "__main__":
    unittest.main(verbosity=2)
