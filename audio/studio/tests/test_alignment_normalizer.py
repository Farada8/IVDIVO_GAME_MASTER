import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from alignment_normalizer import normalize


class AlignmentNormalizerTests(unittest.TestCase):
    def test_voice_segments(self):
        payload = {"voice_segments": [
            {"dialogue_input_index": 0, "start_time_seconds": 0.1, "end_time_seconds": 1.2},
            {"dialogue_input_index": 1, "start_time_seconds": 1.0, "end_time_seconds": 2.0},
        ]}
        out = normalize(payload, "B1", ["u0", "u1"])
        self.assertEqual(out["source_schema"], "voice_segments")
        self.assertEqual(len(out["records"]), 2)
        self.assertEqual(out["records"][1]["unit_id"], "u1")

    def test_character_alignment(self):
        payload = {"alignment": {
            "characters": ["H", "i"],
            "character_start_times_seconds": [0.0, 0.2],
            "character_end_times_seconds": [0.2, 0.4],
        }}
        out = normalize(payload, "B2", ["u0"])
        self.assertEqual(out["source_schema"], "character_alignment")
        self.assertEqual(len(out["records"]), 1)
        self.assertEqual(out["records"][0]["end_seconds"], 0.4)

    def test_unknown_schema_fails(self):
        with self.assertRaises(ValueError):
            normalize({"foo": "bar"}, "B3")


if __name__ == "__main__":
    unittest.main()
