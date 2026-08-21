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
from provider_inventory_compiler import compile_provider_inventory
from provider_snapshot_contract import seal_snapshot
from provider_snapshot_diff import compare_provider_snapshots

NOW = datetime(2026, 8, 21, 20, 45, tzinfo=timezone.utc)


def snapshot(*, fingerprint="a" * 64, voice_b=False, usage=10):
    voices = {
        "voice-n": {"name": "Narrator Candidate", "category": "premade", "labels": {"language": "en"}},
        "voice-e": {"name": "Ethan Candidate", "category": "premade", "labels": {"language": "en"}},
        "voice-a": {"name": "Aoife Candidate", "category": "premade", "labels": {"language": "en"}},
    }
    if voice_b:
        voices["voice-b"] = {"name": "Additional Candidate", "category": "premade", "labels": {"language": "en"}}
    captured = "2026-08-21T20:40:00+00:00"
    return seal_snapshot({
        "schema_version": "ivdivo.provider_snapshot/1.0",
        "provider": "elevenlabs",
        "status": "PASS",
        "authentication": {
            "state": "AUTHENTICATED",
            "method": "XI_API_KEY_RUNTIME_ENV",
            "credential_persisted": False,
        },
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
        "models": {
            "eleven_v3": {
                "name": "fixture",
                "can_do_text_to_speech": True,
                "can_use_style": True,
                "maximum_text_length_per_request": 5000,
            }
        },
        "voices": voices,
        "volatile": {"captured_at": captured, "character_count": usage},
    })


class ProviderSnapshotDiffTests(unittest.TestCase):
    def test_volatile_change_does_not_become_capability_drift(self):
        first = snapshot(usage=10)
        second = snapshot(usage=20)
        result = compare_provider_snapshots(first, second, max_age_seconds=21600, now=NOW)
        self.assertEqual(result["status"], "PASS_REPEATABLE_CAPABILITY_SET")
        self.assertFalse(result["capability_drift"])
        self.assertTrue(result["volatile_usage_changed"])
        self.assertFalse(result["auto_substitution"])

    def test_voice_inventory_change_requires_revalidation(self):
        result = compare_provider_snapshots(snapshot(), snapshot(voice_b=True), max_age_seconds=21600, now=NOW)
        self.assertEqual(result["status"], "PASS_CAPABILITY_DRIFT_OBSERVED")
        self.assertIn("voice-b", result["voices"]["added"])
        self.assertTrue(result["dispatch_revalidation_required"])

    def test_account_identity_drift_fails_closed(self):
        result = compare_provider_snapshots(
            snapshot(fingerprint="a" * 64),
            snapshot(fingerprint="b" * 64),
            max_age_seconds=21600,
            now=NOW,
        )
        self.assertEqual(result["status"], "FAIL_ACCOUNT_IDENTITY_DRIFT")
        self.assertFalse(result["verified"])


class ProviderInventoryCompilerTests(unittest.TestCase):
    def test_valid_snapshot_compiles_tts_inventory(self):
        out = compile_provider_inventory(snapshot(), now=NOW)
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["voice_count"], 3)
        self.assertEqual(out["tts_model_ids"], ["eleven_v3"])
        self.assertFalse(out["voice_lock"])
        self.assertEqual(out["provider_calls_performed"], 0)

    def test_invalid_snapshot_holds(self):
        bad = snapshot()
        bad["authentication"]["credential_persisted"] = True
        out = compile_provider_inventory(bad, now=NOW)
        self.assertEqual(out["status"], "HOLD_PROVIDER_SNAPSHOT")
        self.assertFalse(out["verified"])


class CastReadinessTests(unittest.TestCase):
    def inventory(self):
        return compile_provider_inventory(snapshot(), now=NOW)

    def test_missing_role_holds(self):
        out = build_cast_readiness(
            self.inventory(),
            candidate_voice_ids={"NARRATOR": ["voice-n"], "ETHAN": ["voice-e"]},
            model_id="eleven_v3",
        )
        self.assertEqual(out["status"], "HOLD_CAST_CANDIDATES")
        self.assertEqual(out["missing_roles"], ["AOIFE"])
        self.assertFalse(out["voice_lock"])

    def test_unknown_voice_id_fails_closed(self):
        out = build_cast_readiness(
            self.inventory(),
            candidate_voice_ids={
                "NARRATOR": ["voice-n"],
                "ETHAN": ["voice-missing"],
                "AOIFE": ["voice-a"],
            },
            model_id="eleven_v3",
        )
        self.assertEqual(out["status"], "FAIL_UNKNOWN_PROVIDER_VOICE_ID")
        self.assertFalse(out["machine_may_auto_lock"])

    def test_missing_model_holds(self):
        out = build_cast_readiness(
            self.inventory(),
            candidate_voice_ids={
                "NARRATOR": ["voice-n"], "ETHAN": ["voice-e"], "AOIFE": ["voice-a"]
            },
            model_id="missing-model",
        )
        self.assertEqual(out["status"], "HOLD_MODEL_BINDING")

    def test_complete_candidate_binding_is_audition_ready_not_locked(self):
        candidates = {"NARRATOR": ["voice-n"], "ETHAN": ["voice-e"], "AOIFE": ["voice-a"]}
        out = build_cast_readiness(self.inventory(), candidate_voice_ids=candidates, model_id="eleven_v3")
        self.assertEqual(out["status"], "READY_FOR_REAL_AUDITION")
        self.assertEqual(out["audition"]["pronunciation"]["terms"], ["Ифа", "Контакт"])
        self.assertEqual(out["audition"]["pair"]["roles"], ["ETHAN", "AOIFE"])
        self.assertEqual(out["audition"]["fatigue"]["minimum_seconds"], 480)
        self.assertFalse(out["provider_dispatch_allowed"])
        self.assertFalse(out["voice_lock"])
        self.assertTrue(out["human_evidence_required"])

    def test_manifest_is_deterministic(self):
        candidates = {"NARRATOR": ["voice-n"], "ETHAN": ["voice-e"], "AOIFE": ["voice-a"]}
        a = build_cast_readiness(self.inventory(), candidate_voice_ids=candidates, model_id="eleven_v3")
        b = build_cast_readiness(self.inventory(), candidate_voice_ids=copy.deepcopy(candidates), model_id="eleven_v3")
        self.assertEqual(a["manifest_hash"], b["manifest_hash"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
