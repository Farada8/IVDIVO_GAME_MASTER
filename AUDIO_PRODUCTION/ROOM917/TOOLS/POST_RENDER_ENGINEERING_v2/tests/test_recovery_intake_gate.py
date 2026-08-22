from __future__ import annotations
import hashlib
import json
import tempfile
import unittest
import wave
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import recovery_intake_gate as g


class RecoveryIntakeGateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_json(self, name, data):
        p = self.root / name
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def make_wav(self):
        p = self.root / "x.wav"
        with wave.open(str(p), "wb") as w:
            w.setnchannels(2); w.setsampwidth(3); w.setframerate(48000)
            w.writeframes(b"\x00" * (4800 * 2 * 3))
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        with wave.open(str(p), "rb") as w:
            frames = w.getnframes()
        spec = {
            "sha256": digest,
            "size_bytes": p.stat().st_size,
            "sample_rate_hz": 48000,
            "sample_width_bytes": 3,
            "channels": 2,
            "frames": frames,
            "duration_seconds": frames / 48000,
        }
        return p, spec

    def lineage(self):
        return self.write_json("lineage.json", {"blocks": [{"block_id": "B1"}, {"block_id": "B2"}]})

    def test_master_pass_and_wrong_sha_fail(self):
        p, spec = self.make_wav()
        self.assertEqual(g.validate_master(p, spec)["status"], "PASS")
        bad = dict(spec); bad["sha256"] = "0" * 64
        self.assertEqual(g.validate_master(p, bad)["status"], "FAIL")

    def test_timing_complete_pass(self):
        tm = self.write_json("tm.json", {
            "source_master_sha256": g.EXPECTED_MASTER["sha256"],
            "blocks": [
                {"block_id": "B1", "start_seconds": 0, "end_seconds": 10, "evidence_grade": "ACCEPTED_ALIGNMENT", "source": "take/a"},
                {"block_id": "B2", "start_seconds": 10, "end_seconds": 20, "evidence_grade": "LIVE_TIMELINE", "source_ref": "timeline/a"},
            ],
        })
        self.assertEqual(g.validate_timing_map(tm, self.lineage())["status"], "PASS")

    def test_timing_null_or_untrusted_fails(self):
        tm = self.write_json("tm_bad.json", {
            "source_master_sha256": g.EXPECTED_MASTER["sha256"],
            "blocks": [
                {"block_id": "B1", "start_seconds": None, "end_seconds": 10, "evidence_grade": "ACCEPTED_ALIGNMENT", "source": "x"},
                {"block_id": "B2", "start_seconds": 10, "end_seconds": 20, "evidence_grade": "SCRIPT_INFERENCE", "source": "x"},
            ],
        })
        self.assertEqual(g.validate_timing_map(tm, self.lineage())["status"], "FAIL")

    def interval_map(self):
        return self.write_json("intervals.json", {
            "schema_version": "ivdivo.room917.p003a2_interval_analysis/1.0",
            "source": {"sha256": g.EXPECTED_MASTER["sha256"], "size_bytes": g.EXPECTED_MASTER["size_bytes"]},
            "analysis_basis": {"segment_start_seconds": 0.0, "segment_end_seconds": 444.980, "window_ms": 100.0, "thresholds_dbfs": [-85, -50, -45]},
            "intervals": [{"threshold_dbfs": -85, "start_seconds": 25.0, "end_seconds": 25.3}],
        })

    def test_interval_map_requires_trusted_provenance(self):
        badp = self.write_json("prov_bad.json", {"evidence_grade": "SUMMARY_RECONSTRUCTION", "source_master_sha256": g.EXPECTED_MASTER["sha256"], "source_ref": "note", "immutable_source": True})
        self.assertEqual(g.validate_interval_map(self.interval_map(), badp)["status"], "FAIL")

    def test_interval_map_trusted_pass(self):
        prov = self.write_json("prov.json", {"evidence_grade": "P003A2_ORIGINAL_OUTPUT", "source_master_sha256": g.EXPECTED_MASTER["sha256"], "source_ref": "durable-original-output-id", "immutable_source": True})
        self.assertEqual(g.validate_interval_map(self.interval_map(), prov)["status"], "PASS")


if __name__ == "__main__":
    unittest.main()
