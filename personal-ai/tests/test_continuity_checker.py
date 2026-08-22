from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from books import BOOK_STAGES, BookProductionCore, ContinuityChecker, ContinuityInputError
from books.core import _continuity_content_sha256
from projects.manager import ProjectStateManager


class ContinuityCheckerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        ProjectStateManager(self.home).create_project("demo", "Demo")
        self.core = BookProductionCore(self.home)
        initialized = self.core.initialize("demo", "Continuity Fixture")
        self.root = Path(initialized["root"])
        (self.root / "drafts" / "chapter-01.md").write_text(
            "Fixture manuscript A\n", encoding="utf-8"
        )
        while self.core.load("demo")["state"]["stage"] != "CONTINUITY":
            self.core.advance("demo")
        self.checker = ContinuityChecker(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def contradiction_payload(self) -> dict:
        return {
            "observations": [
                {
                    "id": "name-a",
                    "category": "NAME",
                    "subject": "char:ava",
                    "field": "canonical_name",
                    "scope": "GLOBAL",
                    "value": "Ava Stone",
                    "chapter": 1,
                    "evidence": "The dossier names her Ava Stone.",
                },
                {
                    "id": "name-b",
                    "category": "NAME",
                    "subject": "char:ava",
                    "field": "canonical_name",
                    "scope": "GLOBAL",
                    "value": "Eva Stone",
                    "chapter": 2,
                    "evidence": "The narrator calls the same character Eva Stone.",
                },
                {
                    "id": "name-style-a",
                    "category": "NAME",
                    "subject": "char:leo",
                    "field": "canonical_name",
                    "scope": "GLOBAL",
                    "value": "Leo Hart",
                    "chapter": 1,
                    "evidence": "Character sheet: Leo Hart.",
                },
                {
                    "id": "name-style-b",
                    "category": "NAME",
                    "subject": "char:leo",
                    "field": "canonical_name",
                    "scope": "GLOBAL",
                    "value": " leo   hart ",
                    "chapter": 4,
                    "evidence": "A later label uses irregular spacing/case.",
                },
                {
                    "id": "age-a",
                    "category": "AGE",
                    "subject": "char:ava",
                    "field": "age",
                    "scope": "story-date:2026-08-22",
                    "value": 30,
                    "chapter": 1,
                    "evidence": "Ava says she is thirty today.",
                },
                {
                    "id": "age-b",
                    "category": "AGE",
                    "subject": "char:ava",
                    "field": "age",
                    "scope": "story-date:2026-08-22",
                    "value": 31,
                    "chapter": 6,
                    "evidence": "On the same story date the file lists age thirty-one.",
                },
                {
                    "id": "appearance-a",
                    "category": "APPEARANCE",
                    "subject": "char:ava",
                    "field": "eye_color",
                    "scope": "GLOBAL",
                    "value": "green",
                    "chapter": 1,
                    "evidence": "Her eyes are described as green.",
                },
                {
                    "id": "appearance-b",
                    "category": "APPEARANCE",
                    "subject": "char:ava",
                    "field": "eye_color",
                    "scope": "GLOBAL",
                    "value": "blue",
                    "chapter": 7,
                    "evidence": "Later the same stable eye colour is described as blue.",
                },
                {
                    "id": "relationship-a",
                    "category": "RELATIONSHIP",
                    "subject": "char:ava|char:leo",
                    "field": "status",
                    "scope": "day:3",
                    "value": "estranged",
                    "chapter": 3,
                    "evidence": "They remain estranged on day three.",
                },
                {
                    "id": "relationship-b",
                    "category": "RELATIONSHIP",
                    "subject": "char:ava|char:leo",
                    "field": "status",
                    "scope": "day:3",
                    "value": "married-and-reconciled",
                    "chapter": 5,
                    "evidence": "Another scene on day three says they already reconciled.",
                },
                {
                    "id": "time-a",
                    "category": "DATE_TIME",
                    "subject": "event:meeting",
                    "field": "timestamp",
                    "scope": "event:meeting",
                    "value": "2026-08-22T10:00",
                    "chapter": 2,
                    "evidence": "The meeting begins at 10:00.",
                },
                {
                    "id": "time-b",
                    "category": "DATE_TIME",
                    "subject": "event:meeting",
                    "field": "timestamp",
                    "scope": "event:meeting",
                    "value": "2026-08-22T12:00",
                    "chapter": 4,
                    "evidence": "The same meeting is stated to begin at noon.",
                },
                {
                    "id": "location-a",
                    "category": "LOCATION",
                    "subject": "char:ava",
                    "field": "location",
                    "scope": "time:2026-08-22T10:15",
                    "value": "Dublin",
                    "chapter": 4,
                    "evidence": "At 10:15 Ava is physically in Dublin.",
                },
                {
                    "id": "location-b",
                    "category": "LOCATION",
                    "subject": "char:ava",
                    "field": "location",
                    "scope": "time:2026-08-22T10:15",
                    "value": "Cork",
                    "chapter": 4,
                    "evidence": "At the same time Ava is physically placed in Cork.",
                },
                {
                    "id": "prop-a",
                    "category": "PROP",
                    "subject": "prop:brass-key",
                    "field": "holder",
                    "scope": "scene:lift-landing",
                    "value": "char:ava",
                    "chapter": 5,
                    "evidence": "Ava keeps the brass key in her hand.",
                },
                {
                    "id": "prop-b",
                    "category": "PROP",
                    "subject": "prop:brass-key",
                    "field": "holder",
                    "scope": "scene:lift-landing",
                    "value": "char:leo",
                    "chapter": 5,
                    "evidence": "Without a transfer, Leo is said to hold the same key.",
                },
            ],
            "event_order": [
                {
                    "before": "event:blackout",
                    "after": "event:hatch-open",
                    "chapter": 8,
                    "evidence": "The blackout happens before the hatch opens.",
                },
                {
                    "before": "event:hatch-open",
                    "after": "event:blackout",
                    "chapter": 9,
                    "evidence": "A later chronology says the hatch opens before the blackout.",
                },
            ],
            "knowledge": [
                {
                    "character": "char:ava",
                    "fact": "fact:service-code",
                    "chapter": 3,
                    "evidence": "Ava uses the service code without explanation.",
                }
            ],
            "reveals": [
                {
                    "fact": "fact:service-code",
                    "chapter": 6,
                    "evidence": "Leo first tells Ava the service code here.",
                }
            ],
            "completions": [
                {
                    "event": "event:seal-hatch",
                    "chapter": 7,
                    "evidence": "The hatch is permanently sealed.",
                    "repeatable": False,
                },
                {
                    "event": "event:seal-hatch",
                    "chapter": 10,
                    "evidence": "The same non-repeatable sealing is performed again.",
                    "repeatable": False,
                },
            ],
        }

    def test_known_fixture_detects_all_registered_domains_with_evidence_pairs(self) -> None:
        report = self.checker.check("demo", self.contradiction_payload())
        categories = {issue["category"] for issue in report["issues"]}
        self.assertEqual(
            categories,
            {
                "NAME",
                "AGE",
                "APPEARANCE",
                "RELATIONSHIP",
                "DATE_TIME",
                "LOCATION",
                "PROP",
                "EVENT_ORDER",
                "KNOWLEDGE",
                "COMPLETED_EVENT",
            },
        )
        required = {
            "severity",
            "chapter",
            "issue",
            "evidence_a",
            "evidence_b",
            "suggested_fix",
        }
        for issue in report["issues"]:
            self.assertTrue(required.issubset(issue))
            self.assertTrue(issue["evidence_a"].startswith("CH"))
            self.assertTrue(issue["evidence_b"].startswith("CH"))
            self.assertIn(issue["severity"], {"FATAL", "MAJOR", "MINOR", "STYLE"})

        self.assertEqual(report["summary"]["FATAL"], 3)
        self.assertEqual(report["summary"]["MAJOR"], 6)
        self.assertEqual(report["summary"]["MINOR"], 1)
        self.assertEqual(report["summary"]["STYLE"], 1)
        self.assertEqual(report["summary"]["TOTAL"], 11)
        self.assertEqual(report["blocking_issue_count"], 9)
        self.assertEqual(report["blocking_status"], "FAIL")
        self.assertEqual(report["gate_action"], "EXPLICIT_FAIL_RECOMMENDED")
        self.assertFalse(report["automatic_pass_allowed"])

    def test_report_persists_json_and_markdown_without_mutating_book_gate(self) -> None:
        before_state = self.core.load("demo")["state"]
        before_hash = _continuity_content_sha256(self.root)
        report = self.checker.check("demo", self.contradiction_payload())
        after_state = self.core.load("demo")["state"]
        after_hash = _continuity_content_sha256(self.root)

        self.assertEqual(before_state, after_state)
        self.assertEqual(before_hash, after_hash)
        self.assertEqual(report["book_content_sha256"], before_hash)
        json_path = Path(report["artifacts"]["json"])
        md_path = Path(report["artifacts"]["markdown"])
        self.assertTrue(json_path.is_file())
        self.assertTrue(md_path.is_file())
        persisted = json.loads(json_path.read_text(encoding="utf-8"))
        self.assertEqual(persisted["report_id"], report["report_id"])
        self.assertIn("Evidence A", md_path.read_text(encoding="utf-8"))

    def test_clean_supported_input_never_auto_passes(self) -> None:
        payload = {
            "observations": [
                {
                    "category": "LOCATION",
                    "subject": "char:ava",
                    "field": "location",
                    "scope": "scene:one",
                    "value": "Dublin",
                    "chapter": 1,
                    "evidence": "Ava is in Dublin.",
                },
                {
                    "category": "LOCATION",
                    "subject": "char:ava",
                    "field": "location",
                    "scope": "scene:two",
                    "value": "Cork",
                    "chapter": 2,
                    "evidence": "Later Ava is in Cork.",
                },
            ],
            "event_order": [],
            "knowledge": [],
            "reveals": [],
            "completions": [],
        }
        before = self.core.load("demo")["state"]
        report = self.checker.check("demo", payload)
        after = self.core.load("demo")["state"]
        self.assertEqual(report["summary"]["TOTAL"], 0)
        self.assertEqual(report["blocking_status"], "NO_BLOCKING_ISSUES_DETECTED")
        self.assertEqual(report["gate_action"], "MANUAL_REVIEW_REQUIRED")
        self.assertFalse(report["automatic_pass_allowed"])
        self.assertEqual(before, after)
        self.assertEqual(after["continuity_gate"]["status"], "NOT_RUN")

    def test_same_scope_identical_values_are_not_issues(self) -> None:
        payload = {
            "observations": [
                {
                    "category": "AGE",
                    "subject": "char:ava",
                    "field": "age",
                    "scope": "day:1",
                    "value": 30,
                    "chapter": 1,
                    "evidence": "Age is thirty.",
                },
                {
                    "category": "AGE",
                    "subject": "char:ava",
                    "field": "age",
                    "scope": "day:1",
                    "value": 30,
                    "chapter": 2,
                    "evidence": "The same age is repeated.",
                },
            ]
        }
        report = self.checker.check("demo", payload)
        self.assertEqual(report["issues"], [])

    def test_repeatable_completion_is_not_flagged(self) -> None:
        payload = {
            "completions": [
                {
                    "event": "event:knock",
                    "chapter": 1,
                    "evidence": "She knocks once.",
                    "repeatable": True,
                },
                {
                    "event": "event:knock",
                    "chapter": 2,
                    "evidence": "She knocks again.",
                    "repeatable": True,
                },
            ]
        }
        self.assertEqual(self.checker.check("demo", payload)["issues"], [])

    def test_report_id_changes_when_reviewed_manuscript_changes(self) -> None:
        payload = {"observations": []}
        first = self.checker.check("demo", payload)
        (self.root / "drafts" / "chapter-01.md").write_text(
            "Fixture manuscript B\n", encoding="utf-8"
        )
        second = self.checker.check("demo", payload)
        self.assertNotEqual(first["book_content_sha256"], second["book_content_sha256"])
        self.assertNotEqual(first["report_id"], second["report_id"])

    def test_checker_rejects_wrong_book_stage(self) -> None:
        other = tempfile.TemporaryDirectory()
        try:
            home = Path(other.name)
            ProjectStateManager(home).create_project("early", "Early")
            BookProductionCore(home).initialize("early", "Early Book")
            with self.assertRaisesRegex(ContinuityInputError, "stage == CONTINUITY"):
                ContinuityChecker(home).check("early", {"observations": []})
        finally:
            other.cleanup()

    def test_unknown_category_fails_closed(self) -> None:
        payload = {
            "observations": [
                {
                    "category": "MAGIC_INTUITION",
                    "subject": "char:ava",
                    "field": "state",
                    "value": "x",
                    "chapter": 1,
                    "evidence": "Unsupported rule.",
                }
            ]
        }
        with self.assertRaisesRegex(ContinuityInputError, "unsupported"):
            self.checker.check("demo", payload)

    def test_inverse_event_order_emits_one_pair_issue(self) -> None:
        payload = {
            "event_order": [
                {"before": "a", "after": "b", "chapter": 1, "evidence": "a then b"},
                {"before": "b", "after": "a", "chapter": 2, "evidence": "b then a"},
                {"before": "a", "after": "b", "chapter": 3, "evidence": "a then b repeated"},
            ]
        }
        issues = self.checker.check("demo", payload)["issues"]
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]["rule_id"], "EVENT_ORDER_INVERSE")
        self.assertEqual(issues[0]["severity"], "FATAL")

    def test_cli_enforce_returns_two_for_blocking_issue_and_persists_report(self) -> None:
        input_path = self.home / "continuity-input.json"
        input_path.write_text(
            json.dumps(
                {
                    "observations": [
                        {
                            "category": "LOCATION",
                            "subject": "char:ava",
                            "field": "location",
                            "scope": "time:1",
                            "value": "Dublin",
                            "chapter": 1,
                            "evidence": "Ava is in Dublin.",
                        },
                        {
                            "category": "LOCATION",
                            "subject": "char:ava",
                            "field": "location",
                            "scope": "time:1",
                            "value": "Cork",
                            "chapter": 1,
                            "evidence": "At the same time Ava is in Cork.",
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )
        run_py = ROOT / "run.py"
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)
        completed = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(self.home),
                "book",
                "check-continuity",
                "demo",
                str(input_path),
                "--enforce",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(completed.returncode, 2, completed.stderr)
        report = json.loads(completed.stdout)
        self.assertEqual(report["summary"]["FATAL"], 1)
        self.assertTrue(Path(report["artifacts"]["json"]).is_file())
        self.assertEqual(self.core.load("demo")["state"]["continuity_gate"]["status"], "NOT_RUN")

    def test_all_registered_stages_constant_is_unchanged(self) -> None:
        self.assertEqual(
            BOOK_STAGES,
            (
                "IDEA",
                "CANON",
                "STORY_BIBLE",
                "OUTLINE",
                "CHAPTER_PLAN",
                "DRAFT",
                "CRITIQUE",
                "REWRITE",
                "CONTINUITY",
                "FINAL",
            ),
        )


if __name__ == "__main__":
    unittest.main()
