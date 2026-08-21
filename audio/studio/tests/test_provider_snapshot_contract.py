import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from provider_snapshot_contract import seal_snapshot, validate_provider_snapshot


class ProviderSnapshotContractTests(unittest.TestCase):
    def payload(self):
        return {
            "schema_version": "ivdivo.provider_snapshot/1.0",
            "provider": "elevenlabs",
            "status": "PASS",
            "authentication": {
                "state": "AUTHENTICATED",
                "method": "XI_API_KEY_RUNTIME_ENV",
                "credential_persisted": False,
            },
            "provenance": {
                "captured_at": "2026-08-21T18:00:00+00:00",
                "capture_method": "DIRECT_AUTHENTICATED_READ_ONLY_API",
                "capture_engine": "ivdivo.elevenlabs_snapshot_acquirer/1.0",
                "source": [
                    {"path": "/v1/user", "http_status": 200},
                    {"path": "/v1/user/subscription", "http_status": 200},
                    {"path": "/v1/models", "http_status": 200},
                    {"path": "/v2/voices", "http_status": 200},
                ],
            },
            "account": {"fingerprint_sha256": "a" * 64, "tier": "creator"},
            "models": {"eleven_v3": {"can_do_text_to_speech": True}},
            "voices": {"voice-A": {"name": "A"}},
            "volatile": {"captured_at": "2026-08-21T18:00:00+00:00"},
        }

    def test_valid_sealed_snapshot_passes(self):
        out = validate_provider_snapshot(seal_snapshot(self.payload()), expected_provider="elevenlabs")
        self.assertEqual(out["status"], "PASS")
        self.assertTrue(out["verified"])
        self.assertTrue(out["production_capture_contract"])

    def test_plain_status_pass_without_authentication_fails(self):
        payload = self.payload(); payload["authentication"]["state"] = "UNKNOWN"
        out = validate_provider_snapshot(seal_snapshot(payload), expected_provider="elevenlabs")
        self.assertEqual(out["status"], "FAIL_NOT_AUTHENTICATED")

    def test_secret_bearing_field_is_rejected(self):
        payload = self.payload(); payload["api_key"] = "never-persist-this"
        with self.assertRaisesRegex(ValueError, "SECRET_FIELD_FORBIDDEN"):
            seal_snapshot(payload)

    def test_hash_drift_fails(self):
        snapshot = seal_snapshot(self.payload()); snapshot["voices"]["voice-B"] = {"name": "B"}
        out = validate_provider_snapshot(snapshot, expected_provider="elevenlabs")
        self.assertEqual(out["status"], "FAIL_HASH_DRIFT")

    def test_provider_mismatch_fails(self):
        out = validate_provider_snapshot(seal_snapshot(self.payload()), expected_provider="other")
        self.assertEqual(out["status"], "FAIL_PROVIDER_MISMATCH")

    def test_stale_snapshot_fails_when_freshness_gate_requested(self):
        payload = self.payload(); captured = datetime(2026, 8, 21, 18, 0, tzinfo=timezone.utc)
        payload["provenance"]["captured_at"] = captured.isoformat()
        out = validate_provider_snapshot(
            seal_snapshot(payload), expected_provider="elevenlabs",
            max_age_seconds=3600, now=captured + timedelta(hours=2),
        )
        self.assertEqual(out["status"], "FAIL_STALE")

    def test_wrong_capture_engine_fails(self):
        payload = self.payload(); payload["provenance"]["capture_engine"] = "manual-json"
        out = validate_provider_snapshot(seal_snapshot(payload), expected_provider="elevenlabs")
        self.assertEqual(out["status"], "FAIL_CAPTURE_ENGINE")

    def test_missing_required_provider_source_fails(self):
        payload = self.payload()
        payload["provenance"]["source"] = [
            {"path": "/v1/user", "http_status": 200},
            {"path": "/v1/models", "http_status": 200},
            {"path": "/v2/voices", "http_status": 200},
        ]
        out = validate_provider_snapshot(seal_snapshot(payload), expected_provider="elevenlabs")
        self.assertEqual(out["status"], "FAIL_SOURCE_COVERAGE")
        self.assertIn("/v1/user/subscription", out["missing_paths"])

    def test_credential_persistence_must_be_explicitly_false(self):
        payload = self.payload(); payload["authentication"]["credential_persisted"] = None
        out = validate_provider_snapshot(seal_snapshot(payload), expected_provider="elevenlabs")
        self.assertEqual(out["status"], "FAIL_CREDENTIAL_PERSISTENCE_UNPROVEN")


if __name__ == "__main__":
    unittest.main(verbosity=2)
