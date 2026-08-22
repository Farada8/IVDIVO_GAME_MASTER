#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PROJECT_PATH = ROOT / "PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json"
SYSTEM_PATH = ROOT / "CURRENT_IVDIVO_SYSTEM_STATE.json"
PORTFOLIO_PATH = ROOT / "CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json"
GUARD_PATH = ROOT / "tools/ivdivo_preexecution_resume_guard.py"
NEXT = "ASSEMBLE_LOCKED_CH01_CH29_MANUSCRIPT_FROM_CURRENT_AUTHORITY_FILES_THEN_RUN_FINAL_COPY_FORMAT_EXPORT_GATE"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_guard():
    spec = importlib.util.spec_from_file_location("ivdivo_preexecution_resume_guard", GUARD_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


class SmithFounderLockSyncTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = load(PROJECT_PATH)
        cls.system = load(SYSTEM_PATH)
        cls.portfolio = load(PORTFOLIO_PATH)
        cls.guard = load_guard()

    def test_project_machine_state_is_founder_locked(self):
        self.assertTrue(self.project["story_lock"])
        self.assertTrue(self.project["founder_lock"])
        self.assertEqual(self.project["status"], "FOUNDER_LOCKED_CH01_CH29_MANUSCRIPT_AUTHORITY")
        self.assertEqual(self.project["founder_lock_decision"]["decision"], "GRANTED")
        self.assertEqual(self.project["founder_lock_decision"]["locked_scope"], "CH01_CH29")
        self.assertFalse(self.project["founder_lock_decision"]["ch30_authorized"])

    def test_project_frontier_is_post_lock_not_prose(self):
        self.assertEqual(self.project["next_obligation"], NEXT)
        self.assertTrue(self.project["manuscript_frontier"]["founder_locked"])
        self.assertFalse(self.project["manuscript_frontier"]["prose_expansion_authorized"])
        self.assertFalse(self.project["manuscript_frontier"]["ch30_authorized"])
        self.assertIn("DO_NOT_WRITE_CH30", self.project["do_not"])

    def test_historical_p72_fact_is_preserved(self):
        self.assertFalse(self.project["verified_block_state"]["p72_full_novel_gate_v0_2"]["founder_lock_implied"])
        self.assertEqual(self.project["verified_block_state"]["medical_factual_hold"]["status"], "PASS_BLOCKER_CLOSED")
        self.assertEqual(self.project["verified_block_state"]["network_relay_factual_hold"]["status"], "PASS_AFTER_MINIMAL_TERMINOLOGY_REPAIR_BLOCKER_CLOSED")

    def test_central_router_matches_project(self):
        active = self.system["portfolio_frontier"]["active_project"]
        self.assertEqual(active["project_id"], self.project["project_id"])
        self.assertEqual(active["mode"], "FOUNDER_LOCKED_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT")
        self.assertEqual(active["founder_lock"], "ISSUED")
        self.assertEqual(active["next_unblocked_obligation"], NEXT)
        self.assertNotIn("SMITH_CH01_CH29_FACTUAL_LINE_LOCK_PENDING", self.system["portfolio_frontier"].get("development_complete_not_locked", []))

    def test_portfolio_router_matches_project(self):
        active = self.portfolio["active_project"]
        self.assertEqual(active["project_id"], self.project["project_id"])
        self.assertEqual(active["founder_lock"], "ISSUED")
        self.assertEqual(active["next_unblocked_obligation"], NEXT)
        self.assertEqual(self.portfolio["b03_founder_lock"]["status"], "FOUNDER_LOCKED")

    def test_preexecution_guard_selects_only_post_lock_work(self):
        result = self.guard.guard_resume(self.system, self.project)
        self.assertEqual(result["decision"], "EXECUTE")
        self.assertEqual(result["selected_next_action"], NEXT)
        self.assertNotIn("CH30", result["selected_next_action"])
        self.assertNotIn("DRAFT", result["selected_next_action"])

    def test_no_router_reopens_story_development(self):
        serialized = json.dumps({"system": self.system["portfolio_frontier"], "portfolio": self.portfolio}, ensure_ascii=False)
        forbidden = [
            "DEVELOPMENT_COMPLETE_FACTUAL_LINE_LOCK_PENDING",
            "FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE",
            "FOUNDER_LOCK_REQUIRED_BEFORE_DOWNSTREAM_AUDIO_PACKAGING",
        ]
        for token in forbidden:
            self.assertNotIn(token, serialized)


if __name__ == "__main__":
    unittest.main(verbosity=2)
