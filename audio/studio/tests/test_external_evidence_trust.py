import sys
import unittest
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))

from external_evidence_trust import (
    DurableArtifactReceipt,
    ReadbackStrength,
    ReviewerAttestationReceipt,
    TransactionRecoveryReceipt,
    build_external_evidence_binding,
    validate_durable_artifact_receipt,
    validate_external_evidence,
    validate_reviewer_attestation_receipt,
    validate_transaction_recovery_receipt,
)
from provider_snapshot_contract import SCHEMA_VERSION, seal_snapshot


class ExternalEvidenceTrustTests(unittest.TestCase):
    NOW = datetime(2026, 8, 21, 18, 0, tzinfo=timezone.utc)

    @staticmethod
    def h(value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    def durable(self, *, artifact_kind="RAW_AUDIO", content_hash=None, metadata=None, strength=None):
        content_hash = content_hash or self.h("artifact")
        return DurableArtifactReceipt(
            artifact_id="A1",
            artifact_kind=artifact_kind,
            storage_provider="GOOGLE_DRIVE",
            source_ref="gdrive://A1",
            content_hash=content_hash,
            size_bytes=128,
            written_at="2026-08-21T17:00:00+00:00",
            readback_at="2026-08-21T17:01:00+00:00",
            readback_hash=content_hash,
            readback_strength=strength or ReadbackStrength.CONTENT_HASH_VERIFIED.value,
            transaction_id="TX1",
            metadata=metadata or {},
        )

    def human(self, scope="PERFORMANCE", *, synthetic=False, candidate_hash=None):
        submission_hash = self.h(f"submission:{scope}")
        durable = self.durable(artifact_kind="HUMAN_ATTESTATION", content_hash=submission_hash)
        return ReviewerAttestationReceipt(
            reviewer_ref="reviewer://human-1",
            reviewer_identity_class="TRUSTED_HUMAN_REVIEWER",
            submission_ref="form://submission-1",
            submission_hash=submission_hash,
            task_pack_hash=self.h("task"),
            artifact_hash=self.h("audio"),
            candidate_hash=candidate_hash or self.h("candidate"),
            decision="PASS",
            submitted_at="2026-08-21T17:02:00+00:00",
            review_scope=scope,
            synthetic_fixture=synthetic,
            durable_receipt=durable,
        )

    def provider_payload(self):
        snapshot = seal_snapshot({
            "schema_version": SCHEMA_VERSION,
            "provider": "generic-provider",
            "status": "PASS",
            "authentication": {
                "state": "AUTHENTICATED",
                "method": "RUNTIME_AUTH",
                "credential_persisted": False,
            },
            "provenance": {
                "captured_at": "2026-08-21T17:30:00+00:00",
                "capture_method": "DIRECT_AUTHENTICATED_READ_ONLY_API",
                "capture_engine": "test-provider-acquirer/1.0",
                "source": [{"path": "/capabilities", "http_status": 200}],
            },
            "account": {"fingerprint_sha256": self.h("account")},
            "voices": {"v1": {"name": "Voice"}},
            "models": {"m1": {"name": "Model"}},
        })
        durable = self.durable(artifact_kind="PROVIDER_SNAPSHOT", content_hash=snapshot["snapshot_hash"])
        return {"snapshot": snapshot, "durable_receipt": durable}

    def test_bare_verified_flag_cannot_satisfy_external_class(self):
        out = validate_external_evidence("HUMAN_REVIEW", {"verified": True}, expected_scope="PERFORMANCE")
        self.assertFalse(out["verified"])

    def test_bare_true_cannot_satisfy_external_class(self):
        out = validate_external_evidence("AUTH_PROVIDER", True)
        self.assertEqual(out["status"], "HOLD_CLASS_SPECIFIC_RECEIPT_REQUIRED")
        self.assertFalse(out["verified"])

    def test_pointer_only_is_below_content_readback(self):
        receipt = self.durable(strength=ReadbackStrength.POINTER_READABLE.value)
        out = validate_durable_artifact_receipt(receipt)
        self.assertEqual(out["status"], "HOLD_DURABLE_READBACK_STRENGTH")
        self.assertFalse(out["verified"])

    def test_durable_hash_drift_fails(self):
        row = self.durable().__dict__.copy()
        row["readback_hash"] = self.h("other")
        out = validate_durable_artifact_receipt(row)
        self.assertEqual(out["status"], "FAIL_DURABLE_READBACK_HASH_DRIFT")

    def test_synthetic_human_cannot_satisfy_human_review(self):
        out = validate_reviewer_attestation_receipt(self.human(synthetic=True), expected_scope="PERFORMANCE")
        self.assertEqual(out["status"], "FAIL_SYNTHETIC_HUMAN_EVIDENCE")
        self.assertFalse(out["verified"])

    def test_human_scope_mismatch_fails(self):
        out = validate_reviewer_attestation_receipt(self.human(scope="PAIR"), expected_scope="PERFORMANCE")
        self.assertEqual(out["status"], "FAIL_REVIEW_SCOPE_MISMATCH")

    def test_valid_human_attestation_passes_contract(self):
        out = validate_reviewer_attestation_receipt(self.human(), expected_scope="PERFORMANCE")
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(out["verified"])

    def test_provider_snapshot_must_be_source_validated_and_durable(self):
        out = validate_external_evidence(
            "AUTH_PROVIDER",
            self.provider_payload(),
            expected_provider="generic-provider",
            max_age_seconds=3600,
            now=self.NOW,
        )
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(out["verified"])

    def test_live_audio_requires_lineage_metadata(self):
        out = validate_external_evidence("LIVE_AUDIO", self.durable(artifact_kind="RAW_AUDIO"))
        self.assertEqual(out["status"], "FAIL_LIVE_AUDIO_LINEAGE")
        self.assertFalse(out["verified"])

    def test_live_audio_passes_with_lineage_metadata(self):
        receipt = self.durable(
            artifact_kind="RAW_AUDIO",
            metadata={
                "project_id": "P1",
                "request_hash": self.h("request"),
                "provider_response_hash": self.h("response"),
            },
        )
        out = validate_external_evidence("LIVE_AUDIO", receipt)
        self.assertTrue(out["verified"])

    def test_alignment_requires_complete_coverage(self):
        receipt = self.durable(
            artifact_kind="ALIGNMENT",
            metadata={"audio_hash": self.h("audio"), "source_hash": self.h("source"), "coverage_complete": False},
        )
        out = validate_external_evidence("REAL_ALIGNMENT", receipt)
        self.assertEqual(out["status"], "HOLD_ALIGNMENT_COVERAGE")

    def test_measured_economics_requires_charge_and_human_time_provenance(self):
        receipt = self.durable(
            artifact_kind="ECONOMICS_LEDGER",
            metadata={"measured": True, "provider_charge_refs": [], "manual_minutes_source_ref": "log://human"},
        )
        out = validate_external_evidence("MEASURED_ECONOMICS", receipt)
        self.assertEqual(out["status"], "HOLD_ECONOMICS_CHARGE_PROVENANCE")

    def test_cross_project_requires_two_distinct_live_projects(self):
        receipt = self.durable(
            artifact_kind="CROSS_PROJECT_LIVE_REPORT",
            metadata={"project_ids": ["P1", "P1"], "live_evidence_hashes": [self.h("a"), self.h("b")]},
        )
        out = validate_external_evidence("CROSS_PROJECT_LIVE", receipt)
        self.assertEqual(out["status"], "HOLD_CROSS_PROJECT_REPLICATION")

    def test_recovery_fails_on_duplicate_charge(self):
        receipt = TransactionRecoveryReceipt(
            transaction_id="TX1",
            recovered_at="2026-08-21T17:10:00+00:00",
            recovered_content_hashes=[self.h("a")],
            durable_readback_strength=ReadbackStrength.TRANSACTION_RECOVERABLE.value,
            duplicate_provider_calls=0,
            duplicate_charges=1,
            unresolved_ambiguities=0,
            recovery_manifest_ref="gdrive://recovery-1",
            recovery_manifest_hash=self.h("recovery"),
            synthetic_fixture=False,
        )
        out = validate_transaction_recovery_receipt(receipt)
        self.assertEqual(out["status"], "FAIL_RECOVERY_DUPLICATE_CHARGES")

    def test_recovery_passes_only_at_transaction_recoverable_strength(self):
        receipt = TransactionRecoveryReceipt(
            transaction_id="TX1",
            recovered_at="2026-08-21T17:10:00+00:00",
            recovered_content_hashes=[self.h("a"), self.h("b")],
            durable_readback_strength=ReadbackStrength.TRANSACTION_RECOVERABLE.value,
            duplicate_provider_calls=0,
            duplicate_charges=0,
            unresolved_ambiguities=0,
            recovery_manifest_ref="gdrive://recovery-1",
            recovery_manifest_hash=self.h("recovery"),
            synthetic_fixture=False,
        )
        out = validate_transaction_recovery_receipt(receipt)
        self.assertTrue(out["verified"])

    def test_binding_hash_exists_only_after_class_validation_passes(self):
        held = build_external_evidence_binding("LIVE_AUDIO", True, claim_scope="P1")
        self.assertIsNone(held["binding_hash"])
        good = self.durable(
            artifact_kind="RAW_AUDIO",
            metadata={
                "project_id": "P1",
                "request_hash": self.h("request"),
                "provider_response_hash": self.h("response"),
            },
        )
        passed = build_external_evidence_binding("LIVE_AUDIO", good, claim_scope="P1")
        self.assertEqual(passed["status"], "PASS")
        self.assertEqual(len(passed["binding_hash"]), 64)


if __name__ == "__main__":
    unittest.main()
