import hashlib
import unittest

from AUDIO_PRODUCTION.ROOM917.RU_PILOT.tools.plan_ru_e01_controlled_blocks import plan_blocks


def unit(uid, scene, ordinal, text, seconds, char="ELENA"):
    return {
        "unit_id": uid,
        "scene": scene,
        "scene_title": f"Scene {scene}",
        "global_dialogue_ordinal": ordinal,
        "character": char,
        "text": text,
        "text_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "estimated_seconds_reference_only": seconds,
    }


class BlockPlannerTests(unittest.TestCase):
    def policy(self):
        return {
            "duration_reference": {"target_seconds_min": 30.0, "target_seconds_max": 80.0},
            "protected_exact_text_units": ["PROTECTED"],
        }

    def doc(self, units):
        return {
            "status": "COMPILED_FROM_AUTHORITATIVE_SCRIPT",
            "story_or_dialogue_changed": False,
            "source_script_sha256": "a" * 64,
            "units": units,
        }

    def test_preserves_order_and_never_crosses_scene(self):
        units = [
            unit("U1",1,1,"A",20), unit("U2",1,2,"B",15,"JULIAN"),
            unit("U3",2,3,"C",20), unit("U4",2,4,"D",15,"MINA")
        ]
        plan=plan_blocks(self.doc(units),self.policy())
        flat=[x for b in plan["blocks"] for x in b["unit_ids"]]
        self.assertEqual(flat,["U1","U2","U3","U4"])
        for b in plan["blocks"]:
            scene=b["scene"]
            self.assertTrue(all(next(u for u in units if u["unit_id"]==uid)["scene"]==scene for uid in b["unit_ids"]))

    def test_protected_unit_is_isolated(self):
        units=[unit("U1",1,1,"A",20),unit("U2",1,2,"PROTECTED",2),unit("U3",1,3,"C",20)]
        plan=plan_blocks(self.doc(units),self.policy())
        p=[b for b in plan["blocks"] if b["protected"]]
        self.assertEqual(len(p),1)
        self.assertEqual(p[0]["unit_ids"],["U2"])
        self.assertEqual(p[0]["status"],"PROTECTED_SHORT_BLOCK")

    def test_rebalances_short_final_edge_when_possible(self):
        units=[
            unit("U1",1,1,"A",20),unit("U2",1,2,"B",20),unit("U3",1,3,"C",20),
            unit("U4",1,4,"D",20),unit("U5",1,5,"E",20)
        ]
        plan=plan_blocks(self.doc(units),self.policy())
        durations=[b["estimated_seconds_reference_only"] for b in plan["blocks"]]
        self.assertEqual(len(durations),2)
        self.assertTrue(all(30 <= d <= 80 for d in durations))
        self.assertEqual(plan["ordinary_short_edge_block_count"],0)

    def test_multi_character_block_is_editorial_not_single_tts(self):
        units=[unit("U1",1,1,"A",18,"ELENA"),unit("U2",1,2,"B",18,"JULIAN")]
        plan=plan_blocks(self.doc(units),self.policy())
        self.assertEqual(plan["blocks"][0]["render_mode"],"MULTI_CHARACTER_EDITORIAL_BLOCK_SPLIT_TO_ORDERED_REQUESTS")

    def test_single_character_block_can_be_isolated_tts_after_lock(self):
        units=[unit("U1",1,1,"A",18,"ELENA"),unit("U2",1,2,"B",18,"ELENA")]
        plan=plan_blocks(self.doc(units),self.policy())
        self.assertEqual(plan["blocks"][0]["render_mode"],"ISOLATED_TTS_BLOCK_ALLOWED_AFTER_CAST_LOCK")

    def test_no_provider_or_spend_authority(self):
        units=[unit("U1",1,1,"A",35)]
        plan=plan_blocks(self.doc(units),self.policy())
        self.assertEqual(plan["provider_calls"],0)
        self.assertEqual(plan["paid_synthesis_calls"],0)
        self.assertFalse(plan["full_episode_single_pass_allowed"])
        self.assertFalse(plan["story_or_dialogue_changed"])

    def test_oversize_unit_fails_closed(self):
        units=[unit("U1",1,1,"A",81)]
        with self.assertRaisesRegex(ValueError,"exceeds max duration"):
            plan_blocks(self.doc(units),self.policy())


if __name__ == "__main__":
    unittest.main()
