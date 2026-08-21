import sys
import unittest
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from live_evidence_escrow import compile_exact_escrow, compile_lineage, recovery_plan, verify_escrow, verify_lineage

SOURCE = "a" * 64
CAP = "b" * 64
AUDIO = "c" * 64
ALIGN = "d" * 64
REQ1 = "1" * 64
REQ2 = "2" * 64
REQ3 = "3" * 64


def lineage(block_id="RB001", request_hash=REQ1, state="ACCEPTED", source=SOURCE, audio=AUDIO, align=ALIGN, spend_state=None):
    row = {
        "project_id": "LESSON_ZERO",
        "episode_id": "CANARY",
        "block_id": block_id,
        "source_sha256": source,
        "request_hash": request_hash,
        "provider": "elevenlabs",
        "provider_state": state,
        "spend_ledger_state": spend_state or state,
        "provider_request_id": f"provider-{block_id}" if state == "ACCEPTED" else None,
        "capability_snapshot_sha256": CAP,
        "request_ref": f"drive://{block_id}/request",
        "response_ref": f"drive://{block_id}/response" if state != "AMBIGUOUS" else f"drive://{block_id}/failure",
        "audio_sha256": audio if state == "ACCEPTED" else None,
        "alignment_sha256": align if state == "ACCEPTED" else None,
        "audio_ref": f"drive://{block_id}/audio" if state == "ACCEPTED" else None,
        "alignment_ref": f"drive://{block_id}/alignment" if state == "ACCEPTED" else None,
        "spend_ledger_ref": "drive://ledger",
        "charge_ref": f"charge:{block_id}" if state == "ACCEPTED" else None,
        "canonical_asset_status": "PASS" if state == "ACCEPTED" else "HOLD",
        "created_at": "2026-08-21T18:00:00+00:00",
    }
    return compile_lineage(row)


def exact_rows():
    return [lineage("RB001", REQ1), lineage("RB002", REQ2), lineage("RB003", REQ3)]


def exact_hashes():
    return {"RB001": REQ1, "RB002": REQ2, "RB003": REQ3}


class LiveEvidenceEscrowTests(unittest.TestCase):
    def test_provider_acceptance_is_not_take_acceptance(self):
        row = lineage()
        self.assertFalse(row["take_lock"])
        self.assertEqual(row["production_take_status"], "NOT_ACCEPTED")
        self.assertEqual(row["provider_state"], row["spend_ledger_state"])
        self.assertEqual(verify_lineage(row)["status"], "PASS")

    def test_accepted_media_requires_durable_audio_ref(self):
        base = {
            "project_id": "P", "episode_id": "E", "block_id": "B", "source_sha256": SOURCE,
            "request_hash": REQ1, "provider": "elevenlabs", "provider_state": "ACCEPTED", "spend_ledger_state": "ACCEPTED",
            "provider_request_id": "req", "capability_snapshot_sha256": CAP, "audio_sha256": AUDIO,
            "request_ref": "drive://request", "response_ref": "drive://response", "spend_ledger_ref": "drive://ledger"
        }
        with self.assertRaisesRegex(ValueError, "ACCEPTED_AUDIO_DURABLE_REF_REQUIRED"):
            compile_lineage(base)

    def test_request_and_spend_refs_are_mandatory(self):
        base = {
            "project_id": "P", "episode_id": "E", "block_id": "B", "source_sha256": SOURCE,
            "request_hash": REQ1, "provider": "elevenlabs", "provider_state": "AMBIGUOUS", "spend_ledger_state": "AMBIGUOUS",
            "capability_snapshot_sha256": CAP,
        }
        with self.assertRaisesRegex(ValueError, "REQUEST_REF_REQUIRED"):
            compile_lineage(base)

    def test_provider_spend_state_mismatch_fails(self):
        with self.assertRaisesRegex(ValueError, "PROVIDER_SPEND_STATE_MISMATCH"):
            lineage(state="ACCEPTED", spend_state="AMBIGUOUS")

    def test_exact_three_lineages_pass(self):
        escrow = compile_exact_escrow(exact_rows(), expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=exact_hashes())
        self.assertEqual(escrow["status"], "PASS_EXACT_ESCROW")
        self.assertFalse(escrow["auto_retry_allowed"])
        self.assertFalse(escrow["machine_may_replay_paid_request"])
        self.assertEqual(verify_escrow(escrow)["status"], "PASS")

    def test_unknown_fourth_lineage_holds(self):
        rows = exact_rows() + [lineage("RB004", "4" * 64)]
        escrow = compile_exact_escrow(rows, expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=exact_hashes())
        self.assertEqual(escrow["status"], "HOLD")
        self.assertEqual(escrow["issues"]["unknown_block_ids"], ["RB004"])

    def test_duplicate_block_holds(self):
        rows = exact_rows() + [lineage("RB001", "4" * 64)]
        escrow = compile_exact_escrow(rows, expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=exact_hashes())
        self.assertIn("RB001", escrow["issues"]["duplicate_block_ids"])
        self.assertEqual(escrow["status"], "HOLD")

    def test_duplicate_request_hash_holds(self):
        rows = [lineage("RB001", REQ1), lineage("RB002", REQ1), lineage("RB003", REQ3)]
        escrow = compile_exact_escrow(rows, expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE)
        self.assertEqual(escrow["status"], "HOLD")
        self.assertEqual(escrow["issues"]["duplicate_request_hashes"], [REQ1])

    def test_ambiguous_provider_state_holds_without_retry(self):
        rows = [lineage("RB001", REQ1), lineage("RB002", REQ2, state="AMBIGUOUS", audio=None, align=None), lineage("RB003", REQ3)]
        escrow = compile_exact_escrow(rows, expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE)
        self.assertEqual(escrow["status"], "HOLD")
        self.assertEqual(escrow["issues"]["ambiguous_block_ids"], ["RB002"])
        self.assertFalse(escrow["auto_retry_allowed"])

    def test_source_or_request_drift_holds(self):
        rows = [lineage("RB001", REQ1), lineage("RB002", REQ2, source="e" * 64), lineage("RB003", REQ3)]
        escrow = compile_exact_escrow(rows, expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=exact_hashes())
        self.assertEqual(escrow["status"], "HOLD")
        self.assertEqual(escrow["issues"]["source_drift_block_ids"], ["RB002"])

    def test_expected_request_hash_mismatch_holds(self):
        hashes = exact_hashes(); hashes["RB002"] = "f" * 64
        escrow = compile_exact_escrow(exact_rows(), expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=hashes)
        self.assertEqual(escrow["issues"]["request_drift_block_ids"], ["RB002"])
        self.assertEqual(escrow["status"], "HOLD")

    def test_recovery_plan_never_replays_paid_request(self):
        escrow = compile_exact_escrow(exact_rows(), expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=exact_hashes())
        durable = []
        for row in escrow["lineages"]:
            durable.extend([row["request_ref"], row["response_ref"], row["audio_ref"], row["alignment_ref"], row["spend_ledger_ref"]])
        out = recovery_plan(escrow, durable_refs=durable)
        self.assertEqual(out["status"], "PASS_RECOVERABLE")
        self.assertFalse(out["auto_replay_provider"])

    def test_missing_recovery_artifact_routes_recovery_not_provider_replay(self):
        escrow = compile_exact_escrow(exact_rows(), expected_block_ids=["RB001", "RB002", "RB003"], expected_source_sha256=SOURCE, expected_request_hashes=exact_hashes())
        out = recovery_plan(escrow, durable_refs=[])
        self.assertEqual(out["status"], "RECOVER_VOLATILE_FIRST")
        self.assertGreater(len(out["missing"]), 0)
        self.assertFalse(out["auto_replay_provider"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
