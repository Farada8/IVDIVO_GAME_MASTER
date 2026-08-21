import json
import sys
import tempfile
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from human_review_evidence import HumanReviewLedger, ReviewEvent, compile_event, lock_eligibility, verify_event

SHA_A = "a" * 64
SHA_B = "b" * 64
BINDING_A = "c" * 64
BINDING_B = "d" * 64


def event(family="PRONUNCIATION", decision="PASS", hard_fails=(), candidate="V1", role="NARRATOR", reviewer="LANGUAGE_REVIEWER", binding=BINDING_A):
    return compile_event(ReviewEvent(
        candidate_id=candidate,
        role_id=role,
        candidate_binding_sha256=binding,
        evidence_family=family,
        reviewer_type=reviewer,
        reviewer_ref="reviewer:001",
        artifact_sha256=SHA_A,
        source_sha256=SHA_B,
        reviewed_at="2026-08-21T18:00:00+00:00",
        decision=decision,
        scores={"naturalness": 4.2},
        hard_fails=tuple(hard_fails),
    ))


def eligibility(events, families, *, pair=False, binding=BINDING_A):
    return lock_eligibility(events, candidate_id="V1", role_id="NARRATOR", candidate_binding_sha256=binding, required_families=families, pair_required=pair)


class HumanReviewEvidenceTests(unittest.TestCase):
    def test_event_hash_verifies(self):
        out = event()
        self.assertEqual(verify_event(out)["status"], "PASS")
        self.assertEqual(out["candidate_binding_sha256"], BINDING_A)
        self.assertFalse(out["machine_generated"])

    def test_tampered_event_fails(self):
        out = event(); out["scores"]["naturalness"] = 1.0
        with self.assertRaisesRegex(ValueError, "HUMAN_REVIEW_EVENT_HASH_MISMATCH"):
            verify_event(out)

    def test_machine_reviewer_type_is_forbidden(self):
        with self.assertRaisesRegex(ValueError, "HUMAN_REVIEWER_TYPE_INVALID"):
            event(reviewer="MACHINE")

    def test_append_only_ledger_reuses_identical_event(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.json"; ledger = HumanReviewLedger(path)
            first = ledger.append(event()); second = ledger.append(event())
            self.assertEqual(first["status"], "APPENDED")
            self.assertEqual(second["status"], "REUSE_EXISTING_EVENT")
            self.assertEqual(ledger.verify_chain()["entries"], 1)

    def test_ledger_tamper_is_detected_on_restart(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "ledger.json"; ledger = HumanReviewLedger(path); ledger.append(event())
            data = json.loads(path.read_text()); data["events"][0]["event"]["decision"] = "FAIL"; path.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "HUMAN_REVIEW_EVENT_HASH_MISMATCH"):
                HumanReviewLedger(path)

    def test_missing_required_family_holds(self):
        out = eligibility([event("PRONUNCIATION"), event("MULTI_STATE")], ["PRONUNCIATION", "MULTI_STATE", "FATIGUE"])
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("FATIGUE", out["missing"])
        self.assertFalse(out["machine_may_auto_lock"])

    def test_pair_required_holds_without_pair(self):
        out = eligibility([event("PRONUNCIATION"), event("MULTI_STATE"), event("FATIGUE")], ["PRONUNCIATION", "MULTI_STATE", "FATIGUE"], pair=True)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("PAIR", out["missing"])

    def test_full_evidence_only_creates_human_lock_eligibility(self):
        events = [event("PRONUNCIATION"), event("MULTI_STATE"), event("FATIGUE"), event("PAIR")]
        out = eligibility(events, ["PRONUNCIATION", "MULTI_STATE", "FATIGUE"], pair=True)
        self.assertEqual(out["status"], "ELIGIBLE_FOR_HUMAN_LOCK_DECISION")
        self.assertFalse(out["voice_lock"])
        self.assertFalse(out["machine_may_auto_lock"])
        self.assertEqual(out["next_authority"], "FOUNDER_OR_AUTHORIZED_HUMAN_LOCK_DECISION")

    def test_hard_fail_blocks_even_with_coverage(self):
        events = [event("PRONUNCIATION", hard_fails=("AGE_DRIFT",)), event("MULTI_STATE"), event("FATIGUE")]
        out = eligibility(events, ["PRONUNCIATION", "MULTI_STATE", "FATIGUE"])
        self.assertEqual(out["status"], "FAIL_HARD")
        self.assertIn("AGE_DRIFT", out["hard_fails"])

    def test_fail_event_in_required_family_holds_conflicting_evidence(self):
        events = [event("PRONUNCIATION", decision="PASS"), event("PRONUNCIATION", decision="FAIL"), event("MULTI_STATE"), event("FATIGUE")]
        self.assertEqual(eligibility(events, ["PRONUNCIATION", "MULTI_STATE", "FATIGUE"])["status"], "HOLD")

    def test_different_binding_evidence_cannot_be_combined(self):
        events = [event("PRONUNCIATION", binding=BINDING_A), event("MULTI_STATE", binding=BINDING_B), event("FATIGUE", binding=BINDING_A)]
        out = eligibility(events, ["PRONUNCIATION", "MULTI_STATE", "FATIGUE"], binding=BINDING_A)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("MULTI_STATE", out["missing"])
        self.assertEqual(out["foreign_binding_events_ignored"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
