import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
import timeline_assembler as ta


class TimelineAssemblerTests(unittest.TestCase):
    def align(self, block_id, unit_id, start, end):
        return {
            "schema_version": "1.0",
            "provider": "test",
            "source_schema": "voice_segments",
            "block_id": block_id,
            "records": [
                {
                    "provider": "test",
                    "endpoint_profile": "test",
                    "source_schema": "voice_segments",
                    "block_id": block_id,
                    "unit_id": unit_id,
                    "unit_index": 0,
                    "start_seconds": start,
                    "end_seconds": end,
                    "text_ref": unit_id,
                    "raw_evidence_ref": "raw.json",
                }
            ],
        }

    def test_resolves_blocks_and_semantic_cue(self):
        assembly = {
            "project_id": "P",
            "scene_id": "S",
            "source_hash": "H",
            "blocks": [
                {"block_id": "B1", "gap_before_ms": 0},
                {"block_id": "B2", "gap_before_ms": 500},
            ],
        }
        a1 = self.align("B1", "U1", 0.0, 1.0)
        a2 = self.align("B2", "U2", 0.1, 1.1)
        cues = {
            "cues": [
                {
                    "cue_id": "F1",
                    "event_type": "FOLEY",
                    "stem": "FOLEY",
                    "anchor": {"unit_id": "U2", "edge": "START", "offset_ms": -50},
                    "duration_ms": 200,
                }
            ]
        }
        r = ta.assemble(assembly, [a1, a2], cues)
        self.assertEqual(r["gate"], "PASS")
        b2 = next(x for x in r["blocks"] if x["block_id"] == "B2")
        self.assertAlmostEqual(b2["start_seconds"], 1.5)
        u2 = next(x for x in r["events"] if x.get("unit_id") == "U2")
        self.assertAlmostEqual(u2["start_seconds"], 1.6)
        f1 = next(x for x in r["events"] if x.get("cue_id") == "F1")
        self.assertAlmostEqual(f1["start_seconds"], 1.55)

    def test_unresolved_anchor_fails(self):
        assembly = {"blocks": [{"block_id": "B1"}]}
        cues = {"cues": [{"cue_id": "X", "anchor": {"unit_id": "MISSING", "edge": "END"}}]}
        r = ta.assemble(assembly, [self.align("B1", "U1", 0, 1)], cues)
        self.assertEqual(r["gate"], "FAIL")
        self.assertEqual(len(r["unresolved_anchors"]), 1)

    def test_missing_alignment_block_raises(self):
        assembly = {"blocks": [{"block_id": "B2"}]}
        with self.assertRaises(ValueError):
            ta.assemble(assembly, [self.align("B1", "U1", 0, 1)], None)

    def test_gap_and_overlap_together_forbidden(self):
        assembly = {"blocks": [{"block_id": "B1", "gap_before_ms": 100, "overlap_previous_ms": 50}]}
        with self.assertRaises(ValueError):
            ta.assemble(assembly, [self.align("B1", "U1", 0, 1)], None)


if __name__ == "__main__":
    unittest.main()
