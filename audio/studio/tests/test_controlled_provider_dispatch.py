import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
import sys
from unittest.mock import patch

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))
sys.path.insert(0, str(STUDIO / "runtime"))

import controlled_provider_dispatch as cpd
from production_control import SpendLedger
from provider_snapshot_contract import seal_snapshot


def ttd_block():
    return {
        "block_id": "RB001",
        "block_type": "TTD_BLOCK",
        "model_id": "eleven_v3",
        "turns": [
            {"unit_id": "u1", "exact_text": "Привет.", "voice_id": "v1"},
            {"unit_id": "u2", "exact_text": "Да.", "voice_id": "v2"},
        ],
    }


class ControlledProviderDispatchTests(unittest.TestCase):
    def write(self, root, name, obj):
        path = Path(root) / name
        path.write_text(json.dumps(obj, ensure_ascii=False), encoding="utf-8")
        return str(path)

    def provider_snapshot(self, *, voices=None, models=None):
        payload = {
            "schema_version": "ivdivo.provider_snapshot/1.0",
            "provider": "elevenlabs",
            "status": "PASS",
            "authentication": {
                "state": "AUTHENTICATED",
                "method": "TEST_AUTHENTICATED_FIXTURE",
                "credential_persisted": False,
            },
            "provenance": {
                "captured_at": datetime.now(timezone.utc).isoformat(),
                "capture_method": "TEST_FIXTURE",
                "capture_engine": "test_controlled_provider_dispatch",
                "source": [{"path": "fixture", "http_status": 200}],
            },
            "account": {"fingerprint_sha256": "a" * 64},
            "voices": voices if voices is not None else {"v1": {}, "v2": {}},
            "models": models if models is not None else {"eleven_v3": {}},
            "volatile": {},
        }
        return seal_snapshot(payload)

    def live_gates(self, root):
        # Minimal generic identity fixture for wrapper tests. Project fixtures such
        # as Lesson Zero freeze much richer scalar/block identity.
        manifest = self.write(root, "manifest.json", {"blocks": {}})
        fixture = self.write(root, "fixture.json", {"scalar_fields": {}, "blocks": {}})
        snap = self.write(root, "snap.json", self.provider_snapshot())
        return manifest, fixture, snap

    def test_default_is_dry_no_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            block = self.write(d, "block.json", ttd_block())
            with patch.object(cpd.adapter, "dispatch") as dispatch:
                out = cpd.execute(block, str(Path(d)/"out"), str(Path(d)/"ledger.json"))
            self.assertEqual(out["status"], "DRY_PASS")
            self.assertFalse(out["dispatch"])
            dispatch.assert_not_called()

    def test_new_live_dispatch_requires_identity_and_authenticated_capability(self):
        with tempfile.TemporaryDirectory() as d:
            block = self.write(d, "block.json", ttd_block())
            with patch.object(cpd.adapter, "dispatch") as dispatch:
                out = cpd.execute(block, str(Path(d)/"out"), str(Path(d)/"ledger.json"), live=True)
            self.assertEqual(out["status"], "NO_DISPATCH_LIVE_GATES")
            self.assertIn("IDENTITY_FIXTURE", out["missing"])
            self.assertIn("AUTHENTICATED_CAPABILITY_SNAPSHOT", out["missing"])
            dispatch.assert_not_called()

    def test_legacy_status_pass_snapshot_no_longer_authorizes_capability(self):
        with tempfile.TemporaryDirectory() as d:
            block = self.write(d, "block.json", ttd_block())
            snap = self.write(d, "snap.json", {
                "status": "PASS",
                "voices": {"v1": {}, "v2": {}},
                "models": {"eleven_v3": {}},
            })
            out = cpd.execute(block, str(Path(d)/"out"), str(Path(d)/"ledger.json"), capability_snapshot_path=snap)
            self.assertEqual(out["status"], "NO_DISPATCH_CAPABILITY")
            self.assertEqual(out["capability_gate"]["status"], "FAIL_SNAPSHOT_CONTRACT")
            self.assertEqual(out["capability_gate"]["snapshot_contract"]["status"], "FAIL_SCHEMA")

    def test_capability_missing_voice_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            block = self.write(d, "block.json", ttd_block())
            snap = self.write(d, "snap.json", self.provider_snapshot(voices={"v1": {}}))
            out = cpd.execute(block, str(Path(d)/"out"), str(Path(d)/"ledger.json"), capability_snapshot_path=snap)
            self.assertEqual(out["status"], "NO_DISPATCH_CAPABILITY")
            self.assertIn("v2", out["capability_gate"]["missing_voices"])

    def test_accepted_hash_is_not_resent_after_restart(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            block = ttd_block(); compiled = cpd.adapter.compile_block(block)
            ledger_path = Path(d)/"ledger.json"
            ledger = SpendLedger(ledger_path)
            ledger.plan(compiled["request_hash"], "RB001")
            ledger.transition(compiled["request_hash"], "ACCEPTED", response_hash="audio")
            with patch.object(cpd.adapter, "dispatch") as dispatch:
                out = cpd.execute(block_path, str(Path(d)/"out"), str(ledger_path), live=True)
            self.assertEqual(out["status"], "REUSE_ACCEPTED")
            dispatch.assert_not_called()

    def test_connectivity_after_post_quarantines_ambiguous(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            manifest, fixture, snap = self.live_gates(d)
            error = RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_CONNECTIVITY"}))
            with patch.object(cpd.adapter, "dispatch", side_effect=error):
                out = cpd.execute(
                    block_path, str(Path(d)/"out"), str(Path(d)/"ledger.json"), live=True,
                    manifest_path=manifest, fixture_path=fixture, capability_snapshot_path=snap,
                )
            self.assertEqual(out["status"], "HOLD_AMBIGUOUS")
            ledger = SpendLedger(Path(d)/"ledger.json")
            state = next(iter(ledger.snapshot().values()))["state"]
            self.assertEqual(state, "AMBIGUOUS")

    def test_4xx_rejection_marks_rejected_not_ambiguous(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            manifest, fixture, snap = self.live_gates(d)
            error = RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_REQUEST","http_status":400}))
            with patch.object(cpd.adapter, "dispatch", side_effect=error):
                out = cpd.execute(
                    block_path, str(Path(d)/"out"), str(Path(d)/"ledger.json"), live=True,
                    manifest_path=manifest, fixture_path=fixture, capability_snapshot_path=snap,
                )
            self.assertEqual(out["status"], "PROVIDER_REJECTED")
            ledger = SpendLedger(Path(d)/"ledger.json")
            state = next(iter(ledger.snapshot().values()))["state"]
            self.assertEqual(state, "REJECTED")

    def test_provider_acceptance_is_not_take_lock_and_mp3_holds_canonical_ingest(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            manifest, fixture, snap = self.live_gates(d)
            out_dir = Path(d) / "out"
            out_dir.mkdir()
            audio_path = out_dir / "RB001__audio.mp3"
            audio_path.write_bytes(b"fake-mp3-provider-evidence")
            evidence = {"audio_artifact": str(audio_path), "audio_sha256": "abc"}
            with patch.object(cpd.adapter, "dispatch", return_value=({"audio_base64":"unused"},{"provider_request_id":"p1"})), \
                 patch.object(cpd.adapter, "persist", return_value=evidence):
                out = cpd.execute(
                    block_path, str(out_dir), str(Path(d)/"ledger.json"), live=True,
                    manifest_path=manifest, fixture_path=fixture, capability_snapshot_path=snap,
                )
            self.assertEqual(out["status"], "LIVE_PROVIDER_ACCEPTED")
            self.assertFalse(out["take_lock"])
            self.assertEqual(out["production_asset_gate"]["status"], "HOLD_EXPLICIT_UPSTREAM_CONVERSION_REQUIRED")
            ledger = SpendLedger(Path(d)/"ledger.json")
            state = next(iter(ledger.snapshot().values()))["state"]
            self.assertEqual(state, "ACCEPTED")

    def test_identity_drift_blocks_before_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            manifest = self.write(d, "manifest.json", {"spoken_units":35,"blocks":{}})
            fixture = self.write(d, "fixture.json", {"scalar_fields":{"spoken_units":36},"blocks":{}})
            with self.assertRaisesRegex(ValueError, "IDENTITY_DRIFT"):
                cpd.execute(block_path, str(Path(d)/"out"), str(Path(d)/"ledger.json"), manifest_path=manifest, fixture_path=fixture)


if __name__ == "__main__":
    unittest.main(verbosity=2)
