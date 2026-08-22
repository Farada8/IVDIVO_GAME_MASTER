from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from books import BookProductionCore, ContinuityChecker
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class PL09AcceptanceFixtureTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        ProjectStateManager(self.home).create_project("fixture", "PL09 Fixture")
        self.book = BookProductionCore(self.home)
        initialized = self.book.initialize("fixture", "PL09 Fixture Book")
        self.root = Path(initialized["root"])
        (self.root / "drafts" / "chapter-01.md").write_text(
            "Deterministic PL-09 fixture manuscript.\n", encoding="utf-8"
        )
        while self.book.load("fixture")["state"]["stage"] != "CONTINUITY":
            self.book.advance("fixture")
        self.payload = json.loads(
            (ROOT / "books" / "fixtures" / "pl09_known_contradictions.json").read_text(
                encoding="utf-8"
            )
        )
        self.checker = ContinuityChecker(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_known_fixture_yields_exact_severity_counts_and_structured_pairs(self) -> None:
        report = self.checker.check("fixture", self.payload)
        self.assertEqual(
            report["summary"],
            {"FATAL": 2, "MAJOR": 3, "MINOR": 1, "STYLE": 1, "TOTAL": 7},
        )
        self.assertEqual(report["blocking_issue_count"], 5)
        self.assertEqual(report["blocking_status"], "FAIL")
        self.assertEqual(report["gate_action"], "EXPLICIT_FAIL_RECOMMENDED")
        self.assertFalse(report["automatic_pass_allowed"])

        for issue in report["issues"]:
            self.assertRegex(issue["issue_id"], r"^issue-[0-9a-f]{20}$")
            self.assertEqual(len(issue["evidence_pair"]), 2)
            for ref in issue["evidence_pair"]:
                self.assertIn("input_ref", ref)
                self.assertIn("record_id", ref)
                self.assertIsInstance(ref["chapter"], int)
                self.assertGreaterEqual(ref["chapter"], 1)
                self.assertTrue(ref["excerpt"].strip())

    def test_issue_ids_and_order_are_stable_for_same_book_and_input(self) -> None:
        first = self.checker.check("fixture", self.payload)
        second = self.checker.check("fixture", self.payload)
        self.assertEqual(first["report_id"], second["report_id"])
        self.assertEqual(
            [issue["issue_id"] for issue in first["issues"]],
            [issue["issue_id"] for issue in second["issues"]],
        )
        self.assertEqual(
            [(issue["severity"], issue["rule_id"], issue["subject"]) for issue in first["issues"]],
            [(issue["severity"], issue["rule_id"], issue["subject"]) for issue in second["issues"]],
        )

    def test_report_is_persisted_to_pl02_output_memory_with_gate_boundary(self) -> None:
        before_gate = self.book.load("fixture")["state"]["continuity_gate"]
        report = self.checker.check("fixture", self.payload)
        after_gate = self.book.load("fixture")["state"]["continuity_gate"]

        self.assertEqual(before_gate, after_gate)
        self.assertEqual(after_gate["status"], "NOT_RUN")
        self.assertIn("output_memory_id", report)
        stored = MemoryStore(self.home / "runtime" / "state.db").get(
            report["output_memory_id"]
        )
        self.assertEqual(stored["kind"], "OUTPUT")
        self.assertEqual(stored["project_id"], "fixture")
        self.assertEqual(stored["source"], "PL-09 Continuity Checker")
        self.assertEqual(stored["metadata"]["report_id"], report["report_id"])
        self.assertEqual(stored["metadata"]["blocking_status"], "FAIL")
        self.assertFalse(stored["metadata"]["automatic_pass_allowed"])

        persisted = json.loads(Path(report["artifacts"]["json"]).read_text(encoding="utf-8"))
        self.assertEqual(persisted["output_memory_id"], report["output_memory_id"])
        self.assertEqual(persisted["book_content_sha256"], report["book_content_sha256"])


if __name__ == "__main__":
    unittest.main()
