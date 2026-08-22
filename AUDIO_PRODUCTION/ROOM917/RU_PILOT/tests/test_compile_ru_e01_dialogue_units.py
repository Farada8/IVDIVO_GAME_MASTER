import tempfile
from pathlib import Path
import unittest

from AUDIO_PRODUCTION.ROOM917.RU_PILOT.tools.compile_ru_e01_dialogue_units import compile_units


class DialogueUnitCompilerTests(unittest.TestCase):
    def compile_sample(self):
        sample = """# TEST
# SCENE 1 — ЛОББИ

**ЭЛЕНА (спокойно):**  
Первая реплика.

**SFX:** звук

**МИНА:**  
Вторая реплика.

# SCENE 2 — НИША

**КЕЙТ НА ЛИНИИ — CLEAN HUMAN TAKE FIRST:**  
Лени-бёрд...

**ДЖУЛИАН:**  
Последняя реплика.
"""
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "script.md"
            p.write_text(sample, encoding="utf-8")
            return compile_units(p)

    def test_extracts_only_dialogue_roles(self):
        result = self.compile_sample()
        self.assertEqual(result["unit_count"], 4)
        self.assertEqual([u["character"] for u in result["units"]], ["ELENA", "MINA", "CATE", "JULIAN"])

    def test_scene_and_stable_ids(self):
        result = self.compile_sample()
        self.assertEqual(result["units"][0]["unit_id"], "RU_E01_DLG_S01_001_ELENA")
        self.assertEqual(result["units"][1]["unit_id"], "RU_E01_DLG_S01_002_MINA")
        self.assertEqual(result["units"][2]["unit_id"], "RU_E01_DLG_S02_001_CATE")

    def test_cate_extended_label_maps_to_cate(self):
        result = self.compile_sample()
        cate = [u for u in result["units"] if u["character"] == "CATE"]
        self.assertEqual(len(cate), 1)
        self.assertEqual(cate[0]["text"], "Лени-бёрд...")

    def test_no_provider_or_story_mutation(self):
        result = self.compile_sample()
        self.assertFalse(result["story_or_dialogue_changed"])
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["paid_synthesis_calls"], 0)
        self.assertFalse(result["estimated_seconds_are_authority"])

    def test_hashes_are_valid(self):
        result = self.compile_sample()
        self.assertEqual(len(result["source_script_sha256"]), 64)
        for unit in result["units"]:
            self.assertEqual(len(unit["text_sha256"]), 64)


if __name__ == "__main__":
    unittest.main()
