from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from books import BookProductionCore
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class BookProductionCoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        ProjectStateManager(self.home).create_project("bookproj", "Book Project")
        self.core = BookProductionCore(self.home)
        self.core.create_book("bookproj", "b01", "Book One")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _write(self, text: str = "Chapter one.\n\nChapter two.\n") -> dict:
        return self.core.update_manuscript("bookproj", "b01", text)

    def test_final_is_blocked_until_continuity_passes(self) -> None:
        self._write()
        with self.assertRaisesRegex(RuntimeError, "continuity gate passes"):
            self.core.finalize("bookproj", "b01")
        submitted = self.core.submit_for_continuity("bookproj", "b01")
        self.assertEqual(submitted["state"], "CONTINUITY_REVIEW")
        with self.assertRaisesRegex(RuntimeError, "continuity gate passes"):
            self.core.finalize("bookproj", "b01")

    def test_pass_allows_final_and_persists_exact_output(self) -> None:
        text = "Exact manuscript text.\nSecond line.\n"
        state = self._write(text)
        digest = state["manuscript"]["sha256"]
        self.core.submit_for_continuity("bookproj", "b01")
        reviewed = self.core.record_continuity_result(
            "bookproj", "b01", passed=True, source="manual fixture", findings=[]
        )
        self.assertEqual(reviewed["state"], "READY_FOR_FINAL")
        self.assertEqual(reviewed["continuity_gate"]["status"], "PASS")
        self.assertEqual(reviewed["continuity_gate"]["manuscript_sha256"], digest)

        final = self.core.finalize("bookproj", "b01")
        self.assertEqual(final["state"], "FINAL")
        self.assertEqual(final["final"]["sha256"], digest)
        final_path = Path(final["final"]["path"])
        self.assertEqual(final_path.read_text(encoding="utf-8"), text)
        memory = MemoryStore(self.home / "runtime" / "state.db").get(
            final["final"]["output_memory_id"]
        )
        self.assertEqual(memory["kind"], "OUTPUT")
        self.assertEqual(memory["content"], text)
        self.assertEqual(memory["metadata"]["manuscript_sha256"], digest)
        self.assertEqual(memory["metadata"]["continuity_source"], "manual fixture")

    def test_failed_continuity_blocks_final_and_requires_finding(self) -> None:
        self._write()
        self.core.submit_for_continuity("bookproj", "b01")
        with self.assertRaises(ValueError):
            self.core.record_continuity_result(
                "bookproj", "b01", passed=False, source="review", findings=[]
            )
        failed = self.core.record_continuity_result(
            "bookproj",
            "b01",
            passed=False,
            source="review",
            findings=[{"severity": "MAJOR", "message": "timeline conflict"}],
        )
        self.assertEqual(failed["state"], "CONTINUITY_REVIEW")
        self.assertEqual(failed["continuity_gate"]["status"], "FAIL")
        with self.assertRaisesRegex(RuntimeError, "continuity gate passes"):
            self.core.finalize("bookproj", "b01")

    def test_manuscript_update_invalidates_previous_pass(self) -> None:
        self._write("Version A")
        self.core.submit_for_continuity("bookproj", "b01")
        passed = self.core.record_continuity_result(
            "bookproj", "b01", passed=True, source="review A"
        )
        old_hash = passed["continuity_gate"]["manuscript_sha256"]
        changed = self.core.update_manuscript("bookproj", "b01", "Version B")
        self.assertEqual(changed["state"], "DRAFT")
        self.assertEqual(changed["continuity_gate"]["status"], "NOT_RUN")
        self.assertNotEqual(changed["manuscript"]["sha256"], old_hash)
        with self.assertRaisesRegex(RuntimeError, "continuity gate passes"):
            self.core.finalize("bookproj", "b01")

    def test_direct_file_edit_is_detected(self) -> None:
        state = self._write("Known text")
        manuscript = Path(state["manuscript"]["path"])
        manuscript.write_text("tampered", encoding="utf-8")
        with self.assertRaisesRegex(RuntimeError, "hash mismatch"):
            self.core.submit_for_continuity("bookproj", "b01")

    def test_final_is_immutable_through_core(self) -> None:
        self._write("Locked final")
        self.core.submit_for_continuity("bookproj", "b01")
        self.core.record_continuity_result(
            "bookproj", "b01", passed=True, source="review"
        )
        self.core.finalize("bookproj", "b01")
        with self.assertRaisesRegex(RuntimeError, "immutable"):
            self.core.update_manuscript("bookproj", "b01", "rewrite")

    def test_invalid_transitions_fail_closed(self) -> None:
        with self.assertRaises(RuntimeError):
            self.core.submit_for_continuity("bookproj", "b01")
        with self.assertRaises(RuntimeError):
            self.core.record_continuity_result(
                "bookproj", "b01", passed=True, source="premature"
            )
        self._write()
        self.core.submit_for_continuity("bookproj", "b01")
        with self.assertRaises(ValueError):
            self.core.record_continuity_result(
                "bookproj", "b01", passed=True, source="   "
            )

    def test_cli_round_trip_to_final(self) -> None:
        run_py = ROOT / "run.py"
        cli_home = self.home / "cli-home"
        manuscript = self.home / "cli-manuscript.md"
        manuscript.write_text("CLI manuscript\n", encoding="utf-8")
        continuity = self.home / "continuity.json"
        continuity.write_text(
            json.dumps({"passed": True, "source": "CLI review", "findings": []}),
            encoding="utf-8",
        )

        commands = [
            [sys.executable, str(run_py), "--home", str(cli_home), "project", "create", "cli-book"],
            [sys.executable, str(run_py), "--home", str(cli_home), "book", "create", "cli-book", "b1", "CLI Book"],
            [sys.executable, str(run_py), "--home", str(cli_home), "book", "manuscript", "cli-book", "b1", str(manuscript)],
            [sys.executable, str(run_py), "--home", str(cli_home), "book", "submit", "cli-book", "b1"],
            [sys.executable, str(run_py), "--home", str(cli_home), "book", "continuity", "cli-book", "b1", str(continuity)],
            [sys.executable, str(run_py), "--home", str(cli_home), "book", "finalize", "cli-book", "b1"],
        ]
        last = None
        for command in commands:
            last = subprocess.run(command, check=False, capture_output=True, text=True)
            self.assertEqual(last.returncode, 0, last.stderr)
        result = json.loads(last.stdout)
        self.assertEqual(result["state"], "FINAL")
        self.assertTrue(Path(result["final"]["path"]).is_file())


if __name__ == "__main__":
    unittest.main()
