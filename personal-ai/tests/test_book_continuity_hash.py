from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from books import BOOK_STAGES, BookProductionCore, ContinuityGateError
from projects.manager import ProjectStateManager


class BookContinuityHashTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        ProjectStateManager(self.home).create_project("demo", "Demo")
        self.core = BookProductionCore(self.home)
        self.core.initialize("demo", "Hash-Gated Book")
        loaded = self.core.load("demo")
        self.root = Path(loaded["root"])
        (self.root / "drafts" / "chapter-01.md").write_text(
            "Version A\n", encoding="utf-8"
        )
        while self.core.load("demo")["state"]["stage"] != "CONTINUITY":
            self.core.advance("demo")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_pass_records_exact_content_digest(self) -> None:
        passed = self.core.set_continuity_gate(
            "demo", passed=True, evidence="deterministic fixture pass"
        )
        digest = passed["state"]["continuity_gate"]["content_sha256"]
        self.assertIsInstance(digest, str)
        self.assertEqual(len(digest), 64)
        self.assertTrue(all(char in "0123456789abcdef" for char in digest))
        self.assertEqual(self.core.advance("demo")["state"]["stage"], "FINAL")

    def test_content_change_after_pass_blocks_final_without_state_mutation(self) -> None:
        passed = self.core.set_continuity_gate(
            "demo", passed=True, evidence="reviewed Version A"
        )
        version_before = passed["state"]["version"]
        history_before = list(passed["state"]["history"])
        old_hash = passed["state"]["continuity_gate"]["content_sha256"]

        (self.root / "drafts" / "chapter-01.md").write_text(
            "Version B\n", encoding="utf-8"
        )
        with self.assertRaisesRegex(ContinuityGateError, "PASS is stale"):
            self.core.advance("demo")

        after = self.core.load("demo")["state"]
        self.assertEqual(after["stage"], "CONTINUITY")
        self.assertEqual(after["version"], version_before)
        self.assertEqual(after["history"], history_before)
        self.assertEqual(after["continuity_gate"]["status"], "PASS")
        self.assertEqual(after["continuity_gate"]["content_sha256"], old_hash)

    def test_recheck_after_content_change_refreshes_digest_and_allows_final(self) -> None:
        first = self.core.set_continuity_gate(
            "demo", passed=True, evidence="reviewed Version A"
        )
        first_hash = first["state"]["continuity_gate"]["content_sha256"]
        (self.root / "chapters" / "chapter-02.md").write_text(
            "New chapter\n", encoding="utf-8"
        )
        with self.assertRaises(ContinuityGateError):
            self.core.advance("demo")

        second = self.core.set_continuity_gate(
            "demo", passed=True, evidence="reviewed Version A plus chapter two"
        )
        second_hash = second["state"]["continuity_gate"]["content_sha256"]
        self.assertNotEqual(first_hash, second_hash)
        self.assertEqual(self.core.advance("demo")["state"]["stage"], "FINAL")


if __name__ == "__main__":
    unittest.main()
