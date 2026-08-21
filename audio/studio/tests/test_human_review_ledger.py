import json
import sys
import tempfile
import unittest
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))

from external_evidence_trust import DurableArtifactReceipt, ReadbackStrength, ReviewerAttestationReceipt
from human_review_ledger import (
    HumanReviewLedger,
    candidate_review_state,
    compile_review_record,
    verify_review_record,
)


class HumanReviewLedgerTests(unittest.TestCase):
    @staticmethod
    def h(value: str) -> str:
        return sha256(value.encode("utf-8")).hexdigest()

    def durable(self, submission_hash: str):
        return DurableArtifactReceipt(
            artifact_id=f"H-{submission_hash[:8]}",
            artifact_kind="HUMAN_ATTESTATION",
            storage_provider="GOOGLE_DRIVE",
            source_ref=f"gdrive://human/{submission_hash[:8]}",
            content_hash=submission_hash,
            size_bytes=256,
            written_at="2026-08-21T17:00:00+00:00",
            readback_at="2026-08-21T17:01:00+00:00",
            readback_hash=submission_hash,
            readback_strength=ReadbackStrength.CONTENT_HASH_VERIFIED.value,
            transaction_id=f"HUM-{submission_hash[:8]}",
            metadata={},
        )

    def human(self, scope="PERFORMANCE", *, decision="PASS", candidate=None, synthetic=False, reviewer="human-1"):
        candidate_hash = candidate or self.h("candidate-a")
        submission_hash = self.h(f"submission:{scope}:{decision}:{candidate_hash}:{reviewer}")
        return ReviewerAttestationReceipt(
            reviewer_ref=f"reviewer://{reviewer}",
            reviewer_identity_class="TRUSTED_HUMAN_REVIEWER",
            submission_ref=f"form://{submission_hash[:12]}",
            submission_hash=submission_hash,
            task_pack_hash=self.h(f"task:{scope}"),
            artifact_hash=self.h(f"audio:{scope}"),
            candidate_hash=candidate_hash,
            decision=decision,
            submitted_at="2026-08-21T17:02:00+00:00",
            review_scope=scope,
            synthetic_fixture=synthetic,
            durable_receipt=self.durable(submission_hash),
        )

    def record(self, scope="PERFORMANCE", **kwargs):
        return compile_review_record(self.human(scope, **kwargs), expected_scope=scope)

    def test_pass_fail_hold_are_preserved_as_attested_history(self):
        for decision in ("PASS", "FAIL", "HOLD"):
            record = self.record("PERFORMANCE", decision=decision)
            self.assertEqual(record["decision"], decision)
            self.assertEqual(verify_review_record(record)["status"], "PASS")

    def test_synthetic_review_cannot_enter_ledger(self):
        with self.assertRaisesRegex(ValueError, "HUMAN_ATTESTATION_INVALID:FAIL_SYNTHETIC_HUMAN_EVIDENCE"):
            compile_review_record(self.human(synthetic=True), expected_scope="PERFORMANCE")

    def test_append_only_ledger_reuses_exact_record(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = HumanReviewLedger(Path(td) / "reviews.json")
            record = self.record("PRONUNCIATION")
            first = ledger.append(record)
            second = ledger.append(record)
            self.assertEqual(first["status"], "APPENDED")
            self.assertEqual(second["status"], "REUSE_EXISTING_RECORD")
            self.assertEqual(ledger.verify_chain()["entries"], 1)

    def test_chain_tamper_is_detected_on_restart(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "reviews.json"
            ledger = HumanReviewLedger(path)
            ledger.append(self.record("PRONUNCIATION"))
            data = json.loads(path.read_text(encoding="utf-8"))
            data["entries"][0]["record"]["decision"] = "FAIL"
            path.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "HUMAN_REVIEW_RECORD_HASH_MISMATCH"):
                HumanReviewLedger(path)

    def test_complete_pass_coverage_only_creates_human_lock_eligibility(self):
        candidate = self.h("candidate-a")
        records = [
            self.record("PRONUNCIATION", candidate=candidate),
            self.record("MULTI_STATE", candidate=candidate),
            self.record("FATIGUE", candidate=candidate),
            self.record("PAIR", candidate=candidate),
        ]
        out = candidate_review_state(
            records,
            candidate_hash=candidate,
            required_scopes=["PRONUNCIATION", "MULTI_STATE", "FATIGUE", "PAIR"],
        )
        self.assertEqual(out["status"], "ELIGIBLE_FOR_HUMAN_LOCK_DECISION")
        self.assertFalse(out["machine_may_auto_lock"])
        self.assertFalse(out["voice_lock"])

    def test_pass_fail_conflict_holds_instead_of_overwriting_history(self):
        candidate = self.h("candidate-a")
        records = [
            self.record("PRONUNCIATION", candidate=candidate, decision="PASS", reviewer="human-1"),
            self.record("PRONUNCIATION", candidate=candidate, decision="FAIL", reviewer="human-2"),
        ]
        out = candidate_review_state(records, candidate_hash=candidate, required_scopes=["PRONUNCIATION"])
        self.assertEqual(out["status"], "HOLD_CONFLICT")
        self.assertEqual(out["conflicting_scopes"], ["PRONUNCIATION"])

    def test_other_candidate_evidence_cannot_fill_required_scope(self):
        candidate_a = self.h("candidate-a")
        candidate_b = self.h("candidate-b")
        records = [
            self.record("PRONUNCIATION", candidate=candidate_a),
            self.record("MULTI_STATE", candidate=candidate_b),
        ]
        out = candidate_review_state(
            records,
            candidate_hash=candidate_a,
            required_scopes=["PRONUNCIATION", "MULTI_STATE"],
        )
        self.assertEqual(out["status"], "HOLD")
        self.assertEqual(out["missing_scopes"], ["MULTI_STATE"])
        self.assertEqual(out["ignored_other_candidate_records"], 1)


if __name__ == "__main__":
    unittest.main()
