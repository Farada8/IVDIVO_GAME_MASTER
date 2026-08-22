import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SYSTEM = ROOT / "CURRENT_IVDIVO_SYSTEM_STATE.json"
PORTFOLIO = ROOT / "CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json"


class D01MinimalRouterRepair(unittest.TestCase):
    def setUp(self):
        self.system_text = SYSTEM.read_text(encoding="utf-8")
        self.portfolio_text = PORTFOLIO.read_text(encoding="utf-8")
        self.system = json.loads(self.system_text)
        self.portfolio = json.loads(self.portfolio_text)

    def test_system_routes_to_smith(self):
        pf = self.system["portfolio_frontier"]
        self.assertIn(
            "D01_THE_WIFE_AT_HIS_WEDDING_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED",
            pf["text_locked_or_text_complete"],
        )
        self.assertEqual(pf["active_project"]["title"], "SMITH")
        self.assertEqual(
            pf["active_project"]["mode"],
            "FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE",
        )
        self.assertIn("NO_SMITH_PROSE", pf["active_project"]["authority_boundary"])

    def test_portfolio_routes_to_smith_and_records_d01_lock(self):
        self.assertEqual(self.portfolio["d01_founder_lock"]["status"], "FOUNDER_LOCKED")
        self.assertEqual(self.portfolio["d01_founder_lock"]["recording_authority"], "ISSUED")
        self.assertEqual(self.portfolio["active_project"]["title"], "SMITH")
        self.assertEqual(
            self.portfolio["active_project"]["mode"],
            "FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE",
        )

    def test_stale_d01_resume_tokens_are_absent(self):
        stale = [
            "ACTIVE_WORKING_FINAL_ARC",
            "E01-E96_WITH_E91_E96_CURRENT_FINAL_ARC_WORKING_COMPLETE",
            "E97_EPISTEMIC_CONTRACT_AND_SOURCE_AUTHENTICATION_THEN_DRAFT_GATE_THE_GIRL_ADRIAN_MET",
            "FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01",
        ]
        combined = self.system_text + "\n" + self.portfolio_text
        for token in stale:
            self.assertNotIn(token, combined)

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
