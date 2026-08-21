import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from audio_repair_router import route_issue, choose_edit_vs_regen


class AudioRepairRouterTests(unittest.TestCase):
    def issue(self, symptom, **extra):
        base = {
            "issue_id": "D1",
            "severity": "MAJOR",
            "symptom_class": symptom,
            "evidence_ref": "listen@00:01",
        }
        base.update(extra)
        return base

    def test_room_dropout_routes_before_music_and_mix(self):
        route = route_issue(self.issue("ROOM_OR_WEATHER_DROPS_OUT"))
        self.assertEqual(route["earliest_layer"], "AMBIENCE_ROOM_IDENTITY")
        self.assertIn("MUSIC_DRAMATURGY", route["invalidates"])
        self.assertIn("SPATIAL_MIX", route["invalidates"])
        self.assertFalse(route["automatic_patch_allowed"])

    def test_physical_action_routes_to_foley(self):
        route = route_issue(self.issue("PHYSICAL_ACTION_NOT_AUDIBLE"))
        self.assertEqual(route["earliest_layer"], "FOLEY_OBJECT_CAUSALITY")
        action = choose_edit_vs_regen(route)
        self.assertEqual(action["action"], "EDIT_OR_LOCAL_REMIX_FIRST")
        self.assertFalse(action["whole_episode_rerender"])

    def test_performance_failure_routes_selective_regen(self):
        route = route_issue(self.issue("VOICE_IDENTITY_OR_ACTING_FAILURE"))
        self.assertEqual(route["earliest_layer"], "VOICE_TAKE")
        self.assertEqual(choose_edit_vs_regen(route)["action"], "SELECTIVE_VOICE_REGEN_OR_RETAKE")

    def test_loudness_only_routes_to_mastering(self):
        route = route_issue(self.issue("LOUDNESS_TRUEPEAK_DELIVERY_ONLY"))
        self.assertEqual(route["earliest_layer"], "MASTERING")
        self.assertEqual(route["invalidates"], [])

    def test_locked_story_does_not_auto_rewrite(self):
        route = route_issue(self.issue("WRONG_WORDS_OR_MEANING", story_locked=True))
        self.assertEqual(route["status"], "ESCALATE_STORY_AUTHORITY")
        self.assertFalse(route["automatic_patch_allowed"])
        self.assertEqual(choose_edit_vs_regen(route)["action"], "AUTHORITY_ESCALATION")

    def test_unknown_symptom_holds(self):
        route = route_issue(self.issue("SOUNDS_WEIRD"))
        self.assertEqual(route["status"], "HOLD_UNKNOWN_CAUSE")
        self.assertIsNone(route["earliest_layer"])

    def test_protected_fields_preserved_in_route(self):
        route = route_issue(self.issue("PAN_WIDTH_OCCLUSION_REVERB_FAILURE", protected_fields=["clue_order", "exact_text"]))
        self.assertEqual(route["protected_fields"], ["clue_order", "exact_text"])

    def test_missing_evidence_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "FIELDS_MISSING"):
            route_issue({"issue_id": "D1", "severity": "MAJOR", "symptom_class": "PHYSICAL_ACTION_NOT_AUDIBLE"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
