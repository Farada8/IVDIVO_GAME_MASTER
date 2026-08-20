import hashlib
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
import adaptation_plan_validator as apv


def h(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class AdaptationPlanValidatorTests(unittest.TestCase):
    def source_units(self):
        return {
            "source_hash": "SOURCEHASH",
            "units": [
                {"unit_id": "CH001_U0001", "global_ordinal": 1, "text_sha256": h("A")},
                {"unit_id": "CH001_U0002", "global_ordinal": 2, "text_sha256": h("B")},
            ],
        }

    def valid_plan(self):
        return {
            "project_id": "P",
            "source_hash": "SOURCEHASH",
            "delivery_mode": "DRAMATIZED",
            "text_protection": "EXACT_SOURCE",
            "scenes": [
                {
                    "scene_id": "S01",
                    "chapter_id": "CH001",
                    "scene_objective": "Establish conflict",
                    "dramatic_function": "OPENING",
                    "listener_contract_seed": {"must_understand": ["A happens"]},
                    "decisions": [
                        {"source_unit_id": "CH001_U0001", "source_text_sha256": h("A"), "decision_type": "NARRATE"},
                        {"source_unit_id": "CH001_U0002", "source_text_sha256": h("B"), "decision_type": "ACTOR_DIALOGUE", "speaker_ids": ["C1"]},
                    ],
                }
            ],
        }

    def test_valid_exact_plan_passes(self):
        r = apv.validate(self.valid_plan(), self.source_units())
        self.assertEqual(r["gate"], "PASS")
        self.assertEqual(r["mapped_source_unit_count"], 2)

    def test_unmapped_source_fails(self):
        p = self.valid_plan()
        p["scenes"][0]["decisions"].pop()
        r = apv.validate(p, self.source_units())
        self.assertEqual(r["gate"], "FAIL")
        self.assertTrue(any(i["code"] == "SOURCE_UNIT_UNMAPPED" for i in r["issues"]))

    def test_omit_forbidden_under_exact(self):
        p = self.valid_plan()
        p["scenes"][0]["decisions"][1]["decision_type"] = "OMIT"
        p["scenes"][0]["decisions"][1]["adaptation_diff"] = {"approved": True, "source": "B", "performance_version": "", "reason": "x", "meaning_change": "NO"}
        r = apv.validate(p, self.source_units())
        self.assertEqual(r["gate"], "FAIL")
        self.assertTrue(any(i["code"] == "UNAUTHORIZED_TEXT_CHANGE" for i in r["issues"]))

    def test_authorized_adaptation_requires_approved_diff(self):
        p = self.valid_plan()
        p["text_protection"] = "AUTHORIZED_ADAPTATION"
        p["delivery_mode"] = "FULL_AUDIO_DRAMA"
        p["scenes"][0]["decisions"][1]["decision_type"] = "ADAPT"
        r = apv.validate(p, self.source_units())
        self.assertEqual(r["gate"], "FAIL")
        self.assertTrue(any(i["code"] == "ADAPTATION_DIFF_NOT_APPROVED" for i in r["issues"]))


if __name__ == "__main__":
    unittest.main()
