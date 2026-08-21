import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
OVERLAY_PATH = ROOT / "PROJECT_STATES" / "CURRENT_TERMINAL_ROUTING_OVERLAY.json"
COVERAGE_PATH = ROOT / "PROJECT_STATES" / "00_PROJECT_STATE_COVERAGE_INDEX.json"
D01_PATH = ROOT / "PROJECTS" / "THE_WIFE_AT_HIS_WEDDING" / "CURRENT_STATE.md"
B02_GATE_PATH = ROOT / "IVDIVO_NARRATIVE_OS" / "BOOKS" / "B02_ORBITAL_YOUTH" / "GATES" / "BOOK2_FINAL_STORY_GATE_v1.0.md"
D10_PATH = ROOT / "PROJECT_STATES" / "D10_BLOODBOUND_CURRENT_STATE.json"
D09_PATH = ROOT / "PROJECT_STATES" / "D09_THE_MAN_WHO_CAME_BACK_CURRENT_STATE.json"
D04_PATH = ROOT / "PROJECT_STATES" / "D04_SEVEN_NIGHTS_BEFORE_CODE_BLUE_CURRENT_STATE.json"
ROOM917_PATH = ROOT / "AUDIO_PRODUCTION" / "ROOM917" / "CURRENT_EXECUTION_STATE.json"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


class RoutingWriteThroughR17R24Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.overlay = load_json(OVERLAY_PATH)
        cls.coverage = load_json(COVERAGE_PATH)

    def test_r17_d01_routes_to_terminal_founder_decision(self):
        d01 = self.overlay["projects"]["D01"]
        self.assertEqual(d01["route"], "FOUNDER_EXPLICIT_LOCK_DECISION")
        self.assertIn("E01-E120", d01["frontier"])
        self.assertEqual(d01["founder_lock"], "NOT_YET_ISSUED")
        self.assertIn("GENERATE_E121", d01["prohibited"])
        self.assertNotIn("E97", d01["route"])
        source = D01_PATH.read_text(encoding="utf-8")
        self.assertIn("E01–E120", source)
        self.assertIn("NOT YET FOUNDER-LOCKED", source)

    def test_r18_founder_lock_is_project_bound(self):
        d10 = self.overlay["projects"]["D10"]
        d01 = self.overlay["projects"]["D01"]
        d09 = self.overlay["projects"]["D09"]
        self.assertEqual(d10["founder_lock"], "ISSUED")
        self.assertEqual(d01["founder_lock"], "NOT_YET_ISSUED")
        self.assertEqual(d09["founder_lock"], "NOT_YET_ISSUED")
        d10_state = load_json(D10_PATH)
        self.assertEqual(d10_state["founder_lock"]["status"], "ISSUED")

    def test_r19_b02_final_gate_stops_internal_rewrite_route(self):
        b02 = self.overlay["projects"]["IVDIVO_BOOK_2"]
        self.assertEqual(b02["route"], "EXTERNAL_FEEDBACK_PUBLISHER_READER_EVIDENCE")
        self.assertIn("PASS_C_READER_ADVOCATE_AS_NEXT_ACTION", b02["prohibited"])
        gate = B02_GATE_PATH.read_text(encoding="utf-8")
        self.assertIn("EXTERNAL-FEEDBACK READY", gate)
        self.assertIn("NOT LOCKED", gate)

    def test_r20_provider_gate_propagates_without_fake_result(self):
        d04 = self.overlay["projects"]["D04"]
        self.assertIn("EXTERNAL_PROVIDER_REQUIRED", d04["evidence_gates"])
        self.assertIn("FAKE_PROVIDER_RESULT", d04["prohibited"])
        state = load_json(D04_PATH)
        self.assertEqual(state["live_audio_status"], "NOT_CLAIMED_NOT_YET_PROVEN")

    def test_r21_human_gate_propagates_without_model_substitution(self):
        d04 = self.overlay["projects"]["D04"]
        self.assertIn("HUMAN_SIGNAL_REQUIRED", d04["evidence_gates"])
        self.assertIn("MODEL_AS_HUMAN_SIGNAL", d04["prohibited"])
        state = load_json(D04_PATH)
        self.assertEqual(state["current_blocker"], "HUMAN_SIGNAL_REQUIRED_FOR_G4_PERCEPTUAL_PASS")

    def test_r22_stale_routes_are_explicitly_quarantined(self):
        quarantined = self.coverage.get("quarantined_stale_routes", [])
        scopes = {(x["surface"], x["scope"]) for x in quarantined}
        self.assertIn(("CURRENT_IVDIVO_SYSTEM_STATE.json", "D01 portfolio_frontier.active_project"), scopes)
        self.assertIn(("IVDIVO_NARRATIVE_OS/BOOKS/B02_ORBITAL_YOUTH/DRAFT_STATUS.md", "IVDIVO_BOOK_2 next action"), scopes)
        self.assertIn(("Google Drive CURRENT_WORKSTATE_v2.8", "IVDIVO_BOOK_2 earlier section"), scopes)

    def test_r23_next_project_queue_does_not_bypass_d01_lock(self):
        d01 = self.overlay["projects"]["D01"]
        self.assertEqual(d01["route"], "FOUNDER_EXPLICIT_LOCK_DECISION")
        self.assertNotEqual(d01["route"], "SMITH")
        d10 = self.overlay["projects"]["D10"]
        self.assertEqual(d10["route"], "DOWNSTREAM_PRODUCTION_ONLY")

    def test_r24_locked_or_terminal_prose_routes_fail_closed_by_contract(self):
        law = self.overlay["propagation_laws"]["LOCKED_OR_TERMINAL_PROSE"]
        self.assertIn("fails closed", law)
        self.assertIn("GENERATE_E25", self.overlay["projects"]["D10"]["prohibited"])
        self.assertIn("GENERATE_E25", self.overlay["projects"]["D09"]["prohibited"])
        self.assertIn("GENERATE_E121", self.overlay["projects"]["D01"]["prohibited"])
        room = self.overlay["projects"]["D02_ROOM917"]
        self.assertIn("RESTART_S0_S1", room["prohibited"])
        state = load_json(ROOM917_PATH)
        self.assertIn("P003A2_PRE_SCENE3_INTERVAL_LOCALIZATION", state["next_action"]["stage"])


if __name__ == "__main__":
    unittest.main()
