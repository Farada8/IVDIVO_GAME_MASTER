import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
READY = ROOT / "PROJECTS" / "THE_WIFE_AT_HIS_WEDDING" / "DOWNSTREAM_READINESS_PRELOCK" / "D01_DOWNSTREAM_READINESS_PRELOCK_v1.json"
STATE = ROOT / "PROJECTS" / "THE_WIFE_AT_HIS_WEDDING" / "CURRENT_STATE.md"


class D01DownstreamReadinessR41R48Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = json.loads(READY.read_text(encoding="utf-8"))
        cls.s = STATE.read_text(encoding="utf-8")

    def test_r41_parity_does_not_self_lock(self):
        self.assertEqual(self.r["R41_lock_decision_parity"]["status"], "PASS")
        self.assertFalse(self.r["R41_lock_decision_parity"]["self_lock_allowed"])
        self.assertEqual(self.r["founder_lock"], "NOT_YET_ISSUED")
        self.assertIn("NOT YET FOUNDER-LOCKED", self.s)

    def test_r42_no_change_gate(self):
        x = self.r["R42_no_change_validation"]
        self.assertEqual(x["status"], "PASS_NO_CHANGE")
        self.assertFalse(x["new_fatal_major_evidence_found"])
        self.assertFalse(x["story_repair_authorized"])
        self.assertIn("E121", x["prohibited"])

    def test_r43_ingest_plan_is_not_recording_authority(self):
        x = self.r["R43_locked_source_audio_ingest_plan"]
        self.assertEqual(x["status"], "READY_CONDITIONAL_ON_FOUNDER_LOCK")
        self.assertFalse(x["recording_authority_issued_by_this_plan"])
        self.assertIn("FOUNDER_LOCK_D01", x["required_before_ingest"])

    def test_r44_runtime_normalization_is_mechanical(self):
        x = self.r["R44_whole_season_runtime_normalization"]
        self.assertEqual(x["scope"], "E01-E120_MECHANICAL_ONLY")
        self.assertFalse(x["story_rewrite_on_format_failure"])
        self.assertIn("E01-E60_NOT_FRESHLY_MECHANICALLY_RECOUNTED", x["known_gap"])

    def test_r45_legal_packet_does_not_simulate_specialist(self):
        x = self.r["R45_legal_specialist_review_packet"]
        self.assertEqual(x["human_expert_evidence"], "NOT_RUN")
        self.assertGreaterEqual(len(x["questions"]), 5)

    def test_r46_listener_packet_does_not_simulate_human(self):
        x = self.r["R46_human_listener_packet"]
        self.assertEqual(x["human_signal"], "NOT_RUN")
        self.assertFalse(x["model_substitution_allowed"])
        self.assertGreaterEqual(len(x["target_questions"]), 8)

    def test_r47_firewall_protects_ending_and_identity_solution(self):
        p = self.r["R47_story_protection_firewall"]["protected_story_elements"]
        self.assertIn("SEPARATE_LATE_BIRTH_REGISTRATION_REMEDY", p)
        self.assertIn("E120_COMPLETE_ORDINARY_LIFE_ENDING_NO_NEW_CONSPIRACY_HOOK", p)

    def test_r48_holds_and_smith_is_prohibited(self):
        x = self.r["R48_downstream_handoff"]
        self.assertEqual(x["status"], "HOLD_FOUNDER_LOCK_REQUIRED")
        self.assertEqual(x["recording_authority"], "NOT_ISSUED")
        self.assertEqual(x["smith_activation"], "PROHIBITED_UNTIL_D01_FOUNDER_LOCK")


if __name__ == "__main__":
    unittest.main()
