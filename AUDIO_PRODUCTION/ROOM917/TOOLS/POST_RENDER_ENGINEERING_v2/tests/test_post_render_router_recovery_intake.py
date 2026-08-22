import json
import tempfile
import unittest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import post_render_router as r


class PostRenderRouterRecoveryIntakeTests(unittest.TestCase):
    def setUp(self):
        self.t = tempfile.TemporaryDirectory()
        self.root = Path(self.t.name)

    def tearDown(self):
        self.t.cleanup()

    def j(self, name, data):
        p = self.root / name
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def test_raw_paths_do_not_count_without_intake(self):
        master = self.root / "master.wav"
        master.write_bytes(b"x")
        timing = self.j("timing.json", {"blocks": []})
        flags = r.recovery_flags(None)
        self.assertFalse(master.exists() and flags["master_pass"])
        self.assertFalse(timing.exists() and flags["timing_pass"])

    def test_intake_flags_only_explicit_pass(self):
        p = self.j("intake.json", {
            "schema_version": "room917.recovery_intake_gate/1.0",
            "route": "P003A2_SIGNAL_INTERVALS",
            "results": {
                "master_bytes": {"status": "PASS"},
                "accepted_timing": {"status": "FAIL"}
            }
        })
        flags = r.recovery_flags(p)
        self.assertTrue(flags["master_pass"])
        self.assertFalse(flags["timing_pass"])

    def test_bad_schema_fails_closed(self):
        p = self.j("intake.json", {
            "schema_version": "wrong",
            "results": {"master_bytes": {"status": "PASS"}}
        })
        self.assertFalse(r.recovery_flags(p)["master_pass"])

    def test_interval_identity_rejects_foreign_sha(self):
        p = self.j("iv.json", {
            "schema_version": "ivdivo.room917.p003a2_interval_analysis/1.0",
            "source": {"sha256": "0" * 64, "size_bytes": r.EXPECTED_MASTER["size_bytes"]},
            "analysis_basis": {
                "segment_start_seconds": 0,
                "segment_end_seconds": 444.98,
                "window_ms": 100,
                "thresholds_dbfs": [-85, -50, -45]
            }
        })
        self.assertFalse(r.exact_interval_analysis_ok(p))

    def test_pick_frontier_requires_recovery_intake_before_raw_recovery(self):
        ctx = {
            "mainline_ready": False,
            "authority_ok": True,
            "asset_contract_exists": True,
            "asset_canary_receipt_exists": True,
            "asset_audition_contract_exists": True,
            "release_qc_profile_exists": True,
            "provenance_contract_exists": True,
            "recovery_intake_supplied": False,
            "master_ok": False,
            "timing_ok": False,
            "secondary_safe_work_remaining": True,
        }
        self.assertEqual(r.pick_frontier(ctx)["frontier"], "PROVENANCE_AND_ESCROW_HARDENING")


if __name__ == "__main__":
    unittest.main()
