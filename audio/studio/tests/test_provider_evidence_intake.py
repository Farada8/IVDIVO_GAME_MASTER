import copy
import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[1]
RUNTIME = STUDIO / "runtime"
for path in (STUDIO, RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cast_readiness import build_cast_readiness
from provider_evidence_intake import intake_provider_evidence
from provider_execution_state import resolve_provider_execution_state
from provider_snapshot_contract import seal_snapshot

NOW = datetime(2026, 8, 21, 22, 0, tzinfo=timezone.utc)
REPO = "Farada8/IVDIVO_GAME_MASTER"
RUN_ID = 12345
ATTEMPT = 2
SOURCE_REF = f"https://github.com/{REPO}/actions/runs/{RUN_ID}"


def snapshot(*, fingerprint="a" * 64, captured="2026-08-21T21:55:00+00:00", extra_voice=False):
    voices = {
        "voice-n": {"name": "Narrator Candidate", "category": "premade", "labels": {"language": "en"}},
        "voice-e": {"name": "Ethan Candidate", "category": "premade", "labels": {"language": "en"}},
        "voice-a": {"name": "Aoife Candidate", "category": "premade", "labels": {"language": "en"}},
    }
    if extra_voice:
        voices["voice-x"] = {"name": "New Candidate", "category": "premade", "labels": {"language": "en"}}
    return seal_snapshot({
        "schema_version": "ivdivo.provider_snapshot/1.0",
        "provider": "elevenlabs",
        "status": "PASS",
        "authentication": {"state": "AUTHENTICATED", "method": "XI_API_KEY_RUNTIME_ENV", "credential_persisted": False},
        "provenance": {
            "captured_at": captured,
            "capture_method": "DIRECT_AUTHENTICATED_READ_ONLY_API",
            "capture_engine": "ivdivo.elevenlabs_snapshot_acquirer/1.0",
            "source": [
                {"path": "/v1/user", "http_status": 200},
                {"path": "/v1/user/subscription", "http_status": 200},
                {"path": "/v1/models", "http_status": 200},
                {"path": "/v2/voices", "http_status": 200},
            ],
        },
        "account": {"fingerprint_sha256": fingerprint, "tier": "fixture"},
        "models": {"eleven_v3": {"name": "fixture", "can_do_text_to_speech": True, "can_use_style": True, "maximum_text_length_per_request": 5000}},
        "voices": voices,
        "volatile": {"captured_at": captured, "character_count": 10},
    })


def packet(snap=None, *, transaction=f"{RUN_ID}:{ATTEMPT}", source_ref=SOURCE_REF):
    snap = snap or snapshot()
    h = snap["snapshot_hash"]
    durable = {
        "artifact_id": f"elevenlabs-provider-snapshot-{RUN_ID}-{ATTEMPT}",
        "artifact_kind": "PROVIDER_SNAPSHOT",
        "storage_provider": "GITHUB_ACTIONS_ARTIFACT",
        "source_ref": source_ref,
        "content_hash": h,
        "size_bytes": 1000,
        "written_at": "2026-08-21T21:55:01+00:00",
        "readback_at": "2026-08-21T21:55:02+00:00",
        "readback_hash": h,
        "readback_strength": "CONTENT_HASH_VERIFIED",
        "transaction_id": transaction,
        "metadata": {"provider": "elevenlabs", "source_file_sha256": "b" * 64, "readback_file_sha256": "b" * 64},
    }
    return {"snapshot": snap, "durable_receipt": durable}


class ProviderEvidenceIntakeTests(unittest.TestCase):
    def test_valid_packet_binds_exact_run_and_compiles_inventory(self):
        out = intake_provider_evidence(packet(), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, snapshot_file=snapshot(), now=NOW)
        self.assertEqual(out["status"], "PASS_AUTH_PROVIDER_INTAKE")
        self.assertTrue(out["verified"])
        self.assertEqual(out["next_state"], "REPEATABILITY_REQUIRED")
        self.assertEqual(out["inventory"]["voice_count"], 3)
        self.assertFalse(out["provider_dispatch_allowed"])
        self.assertFalse(out["voice_lock"])

    def test_non_numeric_or_zero_run_identity_fails_before_trust(self):
        for run_id, attempt in (("abc", 1), (0, 1), (1, 0), (1, "2x")):
            with self.subTest(run_id=run_id, attempt=attempt):
                out = intake_provider_evidence(packet(), repository=REPO, run_id=run_id, run_attempt=attempt, now=NOW)
                self.assertEqual(out["status"], "FAIL_WORKFLOW_RUN_IDENTITY_SHAPE")
                self.assertFalse(out["verified"])

    def test_malformed_repository_identity_fails_before_trust(self):
        for repository in ("owneronly", "/repo", "owner/", "a/b/c"):
            with self.subTest(repository=repository):
                out = intake_provider_evidence(packet(), repository=repository, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
                self.assertEqual(out["status"], "FAIL_REPOSITORY_IDENTITY_SHAPE")
                self.assertFalse(out["verified"])

    def test_wrong_transaction_lineage_fails(self):
        out = intake_provider_evidence(packet(transaction="999:1"), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
        self.assertEqual(out["status"], "FAIL_WORKFLOW_TRANSACTION_LINEAGE")

    def test_wrong_source_ref_lineage_fails(self):
        out = intake_provider_evidence(packet(source_ref="https://github.com/x/y/actions/runs/1"), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
        self.assertEqual(out["status"], "FAIL_WORKFLOW_SOURCE_REF_LINEAGE")

    def test_artifact_snapshot_drift_fails(self):
        out = intake_provider_evidence(packet(), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, snapshot_file=snapshot(extra_voice=True), now=NOW)
        self.assertEqual(out["status"], "FAIL_ARTIFACT_PACKET_SNAPSHOT_DRIFT")

    def test_stale_packet_holds(self):
        stale = snapshot(captured="2026-08-20T00:00:00+00:00")
        out = intake_provider_evidence(packet(stale), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
        self.assertEqual(out["status"], "HOLD_AUTH_PROVIDER_INVALID")
        self.assertFalse(out["verified"])

    def test_secret_bearing_key_fails_before_intake(self):
        bad = packet()
        bad["debug"] = {"api_key": "must-never-be-present"}
        out = intake_provider_evidence(bad, repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
        self.assertEqual(out["status"], "FAIL_SECRET_BEARING_FIELD")

    def test_repeatability_same_account_advances_to_cast_binding(self):
        old = snapshot(captured="2026-08-21T21:50:00+00:00")
        current = snapshot(captured="2026-08-21T21:55:00+00:00")
        out = intake_provider_evidence(packet(current), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, prior_snapshot=old, now=NOW)
        self.assertEqual(out["next_state"], "CAST_BINDING_REQUIRED")
        self.assertFalse(out["repeatability"]["capability_drift"])

    def test_repeatability_capability_drift_forces_revalidation(self):
        old = snapshot(captured="2026-08-21T21:50:00+00:00")
        current = snapshot(captured="2026-08-21T21:55:00+00:00", extra_voice=True)
        out = intake_provider_evidence(packet(current), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, prior_snapshot=old, now=NOW)
        self.assertEqual(out["next_state"], "CAPABILITY_DRIFT_REVALIDATION_REQUIRED")
        self.assertTrue(out["repeatability"]["capability_drift"])

    def test_repeatability_different_account_fails(self):
        old = snapshot(fingerprint="c" * 64, captured="2026-08-21T21:50:00+00:00")
        current = snapshot(fingerprint="d" * 64)
        out = intake_provider_evidence(packet(current), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, prior_snapshot=old, now=NOW)
        self.assertEqual(out["status"], "FAIL_PROVIDER_REPEATABILITY")

    def test_intake_is_deterministic_for_same_inputs(self):
        p = packet()
        a = intake_provider_evidence(copy.deepcopy(p), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
        b = intake_provider_evidence(copy.deepcopy(p), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, now=NOW)
        self.assertEqual(a["intake_hash"], b["intake_hash"])


class ProviderExecutionStateTests(unittest.TestCase):
    def valid_intake_with_prior(self):
        return intake_provider_evidence(packet(), repository=REPO, run_id=RUN_ID, run_attempt=ATTEMPT, prior_snapshot=snapshot(captured="2026-08-21T21:50:00+00:00"), now=NOW)

    def test_no_evidence_routes_to_provider_workflow(self):
        out = resolve_provider_execution_state(None)
        self.assertEqual(out["status"], "NO_ADMISSIBLE_PROVIDER_EVIDENCE")
        self.assertFalse(out["provider_dispatch_allowed"])

    def test_inventory_routes_to_provisional_cast_not_lock(self):
        out = resolve_provider_execution_state(self.valid_intake_with_prior())
        self.assertEqual(out["status"], "INVENTORY_READY")
        self.assertFalse(out["voice_lock"])

    def test_cast_ready_routes_only_to_real_audition(self):
        intake = self.valid_intake_with_prior()
        inventory = intake["inventory"]
        cast = build_cast_readiness(
            inventory,
            candidate_voice_ids={"NARRATOR": ["voice-n"], "ETHAN": ["voice-e"], "AOIFE": ["voice-a"]},
            model_id="eleven_v3",
        )
        out = resolve_provider_execution_state(intake, cast_readiness=cast)
        self.assertEqual(out["status"], "AUDITION_REQUIRED")
        self.assertFalse(out["provider_dispatch_allowed"])
        self.assertFalse(out["machine_may_auto_lock"])
        self.assertFalse(out["voice_lock"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
