import json
import tempfile
import unittest
from pathlib import Path
import sys
from unittest.mock import patch

STUDIO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STUDIO))
sys.path.insert(0, str(STUDIO / "runtime"))

import controlled_provider_dispatch as cpd
from production_control import SpendLedger


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

    def test_default_is_dry_no_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            block = self.write(d, "block.json", ttd_block())
            with patch.object(cpd.adapter, "dispatch") as dispatch:
                out = cpd.execute(block, str(Path(d)/"out"), str(Path(d)/"ledger.json"))
            self.assertEqual(out["status"], "DRY_PASS")
            self.assertFalse(out["dispatch"])
            dispatch.assert_not_called()

    def test_capability_missing_voice_blocks(self):
        with tempfile.TemporaryDirectory() as d:
            block = self.write(d, "block.json", ttd_block())
            snap = self.write(d, "snap.json", {"status":"PASS","voices":{"v1":{}},"models":{"eleven_v3":{}}})
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
            error = RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_CONNECTIVITY"}))
            with patch.object(cpd.adapter, "dispatch", side_effect=error):
                out = cpd.execute(block_path, str(Path(d)/"out"), str(Path(d)/"ledger.json"), live=True)
            self.assertEqual(out["status"], "HOLD_AMBIGUOUS")
            ledger = SpendLedger(Path(d)/"ledger.json")
            state = next(iter(ledger.snapshot().values()))["state"]
            self.assertEqual(state, "AMBIGUOUS")

    def test_4xx_rejection_marks_rejected_not_ambiguous(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            error = RuntimeError(json.dumps({"failure":"FAIL_PROVIDER_REQUEST","http_status":400}))
            with patch.object(cpd.adapter, "dispatch", side_effect=error):
                out = cpd.execute(block_path, str(Path(d)/"out"), str(Path(d)/"ledger.json"), live=True)
            self.assertEqual(out["status"], "PROVIDER_REJECTED")
            ledger = SpendLedger(Path(d)/"ledger.json")
            state = next(iter(ledger.snapshot().values()))["state"]
            self.assertEqual(state, "REJECTED")

    def test_identity_drift_blocks_before_dispatch(self):
        with tempfile.TemporaryDirectory() as d:
            block_path = self.write(d, "block.json", ttd_block())
            manifest = self.write(d, "manifest.json", {"spoken_units":35,"blocks":{}})
            fixture = self.write(d, "fixture.json", {"scalar_fields":{"spoken_units":36},"blocks":{}})
            with self.assertRaisesRegex(ValueError, "IDENTITY_DRIFT"):
                cpd.execute(block_path, str(Path(d)/"out"), str(Path(d)/"ledger.json"), manifest_path=manifest, fixture_path=fixture)


if __name__ == "__main__":
    unittest.main(verbosity=2)
