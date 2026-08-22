import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / "CURRENT_IVDIVO_SYSTEM_STATE.json"
PORTFOLIO = ROOT / "CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json"
LOCKED_NEXT = "ASSEMBLE_LOCKED_CH01_CH29_MANUSCRIPT_FROM_CURRENT_AUTHORITY_FILES_THEN_RUN_FINAL_COPY_FORMAT_EXPORT_GATE"


class D01MinimalRouterRepair(unittest.TestCase):
    def setUp(self):
        self.system_text = SYSTEM.read_text(encoding="utf-8")
        self.portfolio_text = PORTFOLIO.read_text(encoding="utf-8")
        self.system = json.loads(self.system_text)
        self.portfolio = json.loads(self.portfolio_text)

    def test_system_preserves_d01_lock_and_routes_current_smith_frontier(self):
        pf = self.system["portfolio_frontier"]
        self.assertIn(
            "D01_THE_WIFE_AT_HIS_WEDDING_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED",
            pf["text_locked_or_text_complete"],
        )
        active = pf["active_project"]
        self.assertEqual(active["project_id"], "IVDIVO_BOOK_3_SMITH")
        self.assertTrue(active["title"].startswith("SMITH"))
        self.assertEqual(active["mode"], "FOUNDER_LOCKED_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT")
        self.assertEqual(active["founder_lock"], "ISSUED")
        self.assertEqual(active["next_unblocked_obligation"], LOCKED_NEXT)
        self.assertIn("NO_CH30", active["authority_boundary"])
        self.assertIn("NO_STORY_DEVELOPMENT", active["authority_boundary"])

    def test_portfolio_preserves_d01_lock_and_current_smith_frontier(self):
        self.assertEqual(self.portfolio["d01_founder_lock"]["status"], "FOUNDER_LOCKED")
        self.assertEqual(self.portfolio["d01_founder_lock"]["recording_authority"], "ISSUED")
        active = self.portfolio["active_project"]
        self.assertEqual(active["project_id"], "IVDIVO_BOOK_3_SMITH")
        self.assertTrue(active["title"].startswith("SMITH"))
        self.assertEqual(active["mode"], "FOUNDER_LOCKED_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT")
        self.assertEqual(active["next_unblocked_obligation"], LOCKED_NEXT)
        self.assertEqual(self.portfolio["b03_founder_lock"]["status"], "FOUNDER_LOCKED")

    def test_stale_d01_resume_tokens_are_absent_from_current_routing_surfaces(self):
        stale = [
            "ACTIVE_WORKING_FINAL_ARC",
            "E01-E96_WITH_E91_E96_CURRENT_FINAL_ARC_WORKING_COMPLETE",
            "E97_EPISTEMIC_CONTRACT_AND_SOURCE_AUTHENTICATION_THEN_DRAFT_GATE_THE_GIRL_ADRIAN_MET",
            "FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01",
        ]
        current = json.dumps(
            {
                "system_portfolio_frontier": self.system["portfolio_frontier"],
                "portfolio_active": self.portfolio["active_project"],
                "portfolio_state_status": self.portfolio["state_status"],
            },
            ensure_ascii=False,
        )
        for token in stale:
            self.assertNotIn(token, current)

    def test_prelock_smith_tokens_are_absent_from_current_active_routing(self):
        stale = [
            "DEVELOPMENT_COMPLETE_FACTUAL_LINE_LOCK_PENDING",
            "FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE",
            "FOUNDER_LOCK_REQUIRED_BEFORE_DOWNSTREAM_AUDIO_PACKAGING",
        ]
        current = json.dumps(
            {
                "system_active": self.system["portfolio_frontier"]["active_project"],
                "system_development_complete_not_locked": self.system["portfolio_frontier"].get("development_complete_not_locked", []),
                "portfolio_active": self.portfolio["active_project"],
            },
            ensure_ascii=False,
        )
        for token in stale:
            self.assertNotIn(token, current)

    def test_historical_provenance_may_retain_old_smith_labels(self):
        # Old labels are valid evidence of what the earlier routing state was;
        # only CURRENT routing surfaces must be free of them.
        self.assertIn("B03_STATE_RECONCILED_TO_CH01_CH29_DEVELOPMENT_COMPLETE_FACTUAL_LINE_LOCK_PENDING", self.system_text)

    def test_d09_gate_is_preserved(self):
        sys_d09 = self.system["portfolio_frontier"]["pending_founder_decision_gates"][0]
        port_d09 = self.portfolio["parallel_founder_decision_gates"][0]
        self.assertEqual(sys_d09["project_id"], "D09")
        self.assertEqual(sys_d09["founder_lock"], "NOT_YET_ISSUED")
        self.assertEqual(port_d09["project_id"], "D09")
        self.assertEqual(port_d09["founder_lock"], "NOT_YET_ISSUED")

    def test_representation_remains_reviewable(self):
        self.assertGreater(self.system_text.count("\n"), 150)
        self.assertGreater(self.portfolio_text.count("\n"), 70)
        self.assertFalse(self.system_text.startswith('{"schema_version"'))
        self.assertFalse(self.portfolio_text.startswith('{"schema_version"'))


if __name__ == "__main__":
    unittest.main()
