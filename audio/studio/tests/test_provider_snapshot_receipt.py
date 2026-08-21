import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
import sys

STUDIO = Path(__file__).resolve().parents[1]
RUNTIME = STUDIO / "runtime"
for path in (STUDIO, RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from provider_snapshot_contract import seal_snapshot
from provider_snapshot_receipt import build_provider_auth_receipt


class ProviderSnapshotReceiptTests(unittest.TestCase):
    def snapshot(self):
        captured = "2026-08-21T20:00:00+00:00"
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
            "account": {"fingerprint_sha256": "a" * 64, "tier": "test"},
            "models": {"eleven_v3": {"can_do_text_to_speech": True}},
            "voices": {"voice-a": {"name": "A"}},
            "volatile": {"captured_at": captured},
        })

    def write(self, root, name, value):
        path = Path(root) / name
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def test_identical_durable_readback_builds_auth_provider_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            snap = self.snapshot()
            source = self.write(d, "source.json", snap)
            readback = self.write(d, "readback.json", snap)
            now = datetime(2026, 8, 21, 20, 5, tzinfo=timezone.utc)
            out = build_provider_auth_receipt(
                source,
                readback,
                artifact_id="run-1-snapshot",
                storage_provider="GITHUB_ACTIONS_ARTIFACT",
                source_ref="https://github.com/Farada8/IVDIVO_GAME_MASTER/actions/runs/1",
                written_at="2026-08-21T20:01:00+00:00",
                transaction_id="1:1",
                artifact_digest="b" * 64,
                now=now,
            )
            self.assertTrue(out["_ivdivo_validation"]["verified"])
            self.assertEqual(out["_ivdivo_validation"]["readback_strength"], "CONTENT_HASH_VERIFIED")
            self.assertEqual(out["durable_receipt"]["content_hash"], snap["snapshot_hash"])
            self.assertEqual(
                out["durable_receipt"]["metadata"]["source_file_sha256"],
                out["durable_receipt"]["metadata"]["readback_file_sha256"],
            )

    def test_readback_mutation_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            snap = self.snapshot()
            source = self.write(d, "source.json", snap)
            mutated = json.loads(json.dumps(snap))
            mutated["voices"]["voice-b"] = {"name": "B"}
            readback = self.write(d, "readback.json", mutated)
            now = datetime(2026, 8, 21, 20, 5, tzinfo=timezone.utc)
            with self.assertRaisesRegex(ValueError, "READBACK_PROVIDER_SNAPSHOT_INVALID"):
                build_provider_auth_receipt(
                    source,
                    readback,
                    artifact_id="run-1-snapshot",
                    storage_provider="GITHUB_ACTIONS_ARTIFACT",
                    source_ref="https://github.com/Farada8/IVDIVO_GAME_MASTER/actions/runs/1",
                    written_at="2026-08-21T20:01:00+00:00",
                    now=now,
                )


if __name__ == "__main__":
    unittest.main(verbosity=2)
