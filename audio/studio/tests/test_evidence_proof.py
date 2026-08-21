import sys
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from evidence_proof import compile_proof_manifest, verify_proof_manifest

SHA = "a" * 64


def ev(cls, verified=True, ref=None):
    return {"evidence_class": cls, "ref": ref or f"github://{cls}", "sha256": SHA, "verified": verified, "observed_at": "2026-08-21T18:00:00Z"}


class EvidenceProofTests(unittest.TestCase):
    def test_code_test_proves_code_ready(self):
        p = compile_proof_manifest(claim="CODE_READY", subject="module", evidence=[ev("CODE_TEST")])
        self.assertEqual(p["status"], "PROVEN")
        self.assertEqual(verify_proof_manifest(p)["status"], "PASS")

    def test_ci_does_not_prove_human_quality(self):
        p = compile_proof_manifest(claim="HUMAN_QUALITY_PASS", subject="voice", evidence=[ev("GITHUB_CI")])
        self.assertEqual(p["status"], "HOLD_UNPROVEN")
        self.assertEqual(p["missing_evidence_classes"], ["HUMAN_REVIEW"])

    def test_provider_auth_does_not_prove_live_audio(self):
        p = compile_proof_manifest(claim="LIVE_AUDIO_ACCEPTED_AS_PROVIDER_EVIDENCE", subject="RB001", evidence=[ev("AUTH_PROVIDER")])
        self.assertEqual(p["status"], "HOLD_UNPROVEN")
        self.assertIn("LIVE_AUDIO", p["missing_evidence_classes"])

    def test_unverified_evidence_does_not_count(self):
        p = compile_proof_manifest(claim="CI_GREEN", subject="runtime", evidence=[ev("GITHUB_CI", verified=False)])
        self.assertEqual(p["status"], "HOLD_UNPROVEN")

    def test_v1_requires_all_evidence_classes(self):
        evidence = [ev("SOURCE_AUTHORITY"), ev("GITHUB_CI"), ev("AUTH_PROVIDER"), ev("LIVE_AUDIO"), ev("HUMAN_REVIEW"), ev("MEASURED_ECONOMICS")]
        p = compile_proof_manifest(claim="V1_RELEASE_EVIDENCE_COMPLETE", subject="AUDIO_NOVEL_ENGINE", evidence=evidence)
        self.assertEqual(p["status"], "HOLD_UNPROVEN")
        self.assertEqual(p["missing_evidence_classes"], ["CROSS_PROJECT_REAL"])
        evidence.append(ev("CROSS_PROJECT_REAL"))
        p2 = compile_proof_manifest(claim="V1_RELEASE_EVIDENCE_COMPLETE", subject="AUDIO_NOVEL_ENGINE", evidence=evidence)
        self.assertEqual(p2["status"], "PROVEN")

    def test_tampered_proof_fails(self):
        p = compile_proof_manifest(claim="CODE_READY", subject="module", evidence=[ev("CODE_TEST")])
        p["status"] = "HOLD_UNPROVEN"
        with self.assertRaisesRegex(ValueError, "PROOF_HASH_MISMATCH"):
            verify_proof_manifest(p)


if __name__ == "__main__":
    unittest.main(verbosity=2)
