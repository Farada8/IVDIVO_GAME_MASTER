import unittest

from tools.ivdivo_evidence_adapters import (
    approval_token_matches,
    artifact_readback_evidence,
    founder_evidence,
    human_listener_evidence,
    make_approval_token,
    model_review_evidence,
    provider_response_evidence,
    resolve_conflicting_evidence,
)
from tools.ivdivo_proof_chain import validate


class EvidenceAdaptersR25R32Tests(unittest.TestCase):
    def test_r25_founder_evidence_requires_explicit_decision(self):
        hold = founder_evidence(
            evidence_id="f-d01", project_id="D01", frontier="E01-E120",
            gate_id="FOUNDER_LOCK", decision="LOCK", locator="founder:pending", explicit=False,
        )
        self.assertEqual(hold["status"], "HOLD")
        passed = founder_evidence(
            evidence_id="f-d10", project_id="D10", frontier="E01-E24",
            gate_id="FOUNDER_LOCK", decision="LOCK", locator="drive:1Fp0v", explicit=True,
        )
        self.assertEqual(passed["source_type"], "FOUNDER")
        self.assertEqual(passed["status"], "PASS")

    def test_r26_model_cannot_be_human_listener(self):
        with self.assertRaisesRegex(ValueError, "MODEL_OUTPUT_CANNOT_BE_ADAPTED_AS_HUMAN_SIGNAL"):
            human_listener_evidence(
                evidence_id="h1", project_id="D04", artifact_id="wav1",
                reviewer_id="model-x", locator="model:review", verdict="PASS",
                blind=True, model_generated=True,
            )
        human = human_listener_evidence(
            evidence_id="h2", project_id="D04", artifact_id="wav1",
            reviewer_id="participant-001", locator="response:001", verdict="PASS",
            blind=True, model_generated=False,
        )
        self.assertEqual(human["source_type"], "BLIND_LISTENER")

    def test_r27_provider_dry_run_does_not_become_live_provider(self):
        dry = provider_response_evidence(
            evidence_id="p-dry", project_id="D04", provider="tts-provider",
            request_id="req1", response_locator=None, artifact_id=None,
            verdict="PASS", live=False,
        )
        self.assertEqual(dry["source_type"], "MACHINE_TEST")
        self.assertIn("LIVE_PROVIDER_EXECUTION", dry["cannot_prove"])
        live_missing = provider_response_evidence(
            evidence_id="p-live", project_id="D04", provider="tts-provider",
            request_id="req2", response_locator=None, artifact_id=None,
            verdict="PASS", live=True,
        )
        self.assertEqual(live_missing["status"], "HOLD")

    def test_r28_external_ai_authority_ceiling(self):
        ev = model_review_evidence(
            evidence_id="m1", project_id="D01", locator="model:1",
            verdict="PASS", authority_weight=40,
        )
        self.assertEqual(ev["source_type"], "EXTERNAL_AI")
        self.assertIn("FOUNDER_APPROVAL", ev["cannot_prove"])
        with self.assertRaisesRegex(ValueError, "MODEL_REVIEW_AUTHORITY_CEILING_EXCEEDED"):
            model_review_evidence(
                evidence_id="m2", project_id="D01", locator="model:2",
                verdict="PASS", authority_weight=80,
            )

    def test_r29_conflicting_evidence_requires_reconciliation(self):
        result = resolve_conflicting_evidence([
            {"evidence_id": "a", "status": "PASS"},
            {"evidence_id": "b", "status": "FAIL"},
        ])
        self.assertEqual(result["status"], "UNRESOLVED_CONFLICT")
        self.assertIn("disposition_required", result)

    def test_r30_artifact_readback_is_exact(self):
        ok = artifact_readback_evidence(
            evidence_id="rb1", artifact_id="A", expected_sha256="abc", readback_sha256="abc"
        )
        bad = artifact_readback_evidence(
            evidence_id="rb2", artifact_id="A", expected_sha256="abc", readback_sha256="def"
        )
        self.assertEqual(ok["status"], "PASS")
        self.assertEqual(bad["status"], "FAIL")

    def test_r31_approval_token_is_scope_bound(self):
        token = make_approval_token(
            project_id="D10", frontier="E01-E24", gate_id="FOUNDER_LOCK", evidence_id="f-d10"
        )
        self.assertTrue(approval_token_matches(
            token, project_id="D10", frontier="E01-E24", gate_id="FOUNDER_LOCK", evidence_id="f-d10"
        ))
        self.assertFalse(approval_token_matches(
            token, project_id="D01", frontier="E01-E120", gate_id="FOUNDER_LOCK", evidence_id="f-d10"
        ))

    def test_r32_declared_pass_mismatch_fails_closed(self):
        payload = {
            "authority_snapshot": {"project_id": "D01", "frontier": "E01-E120"},
            "evidence": [{
                "evidence_id": "m1", "source_type": "EXTERNAL_AI",
                "authority_weight": 30, "status": "PASS"
            }],
            "claims": [{
                "claim_id": "human-ok", "evidence_ids": ["m1"],
                "requires_human_evidence": True
            }],
            "gates": [{
                "gate_id": "human-gate", "required_claim_ids": ["human-ok"],
                "declared_verdict": "PASS"
            }],
            "artifacts": [],
        }
        result = validate(payload)
        self.assertEqual(result["status"], "FAIL_CLOSED")
        self.assertTrue(any(x.startswith("GATE_VERDICT_MISMATCH:human-gate") for x in result["errors"]))


if __name__ == "__main__":
    unittest.main()
