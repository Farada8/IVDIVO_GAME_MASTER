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

from books import BOOK_STAGES, BookProductionCore, BookProductionError, ContinuityGateError
from projects.manager import ProjectStateManager


class BookProductionCoreTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.projects = ProjectStateManager(self.home)
        self.projects.create_project("demo", "Demo")
        self.core = BookProductionCore(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def init(self) -> dict:
        return self.core.initialize("demo", "Demo Book")

    def advance_to_continuity(self) -> dict:
        if not (self.home / "projects" / "demo" / "book").exists():
            self.init()
        result = self.core.load("demo")
        while result["state"]["stage"] != "CONTINUITY":
            result = self.core.advance("demo")
        return result

    def test_initialize_creates_registered_structure(self) -> None:
        result = self.init()
        root = Path(result["root"])
        for filename in (
            "book.yaml",
            "state.json",
            "canon.md",
            "characters.json",
            "locations.json",
            "timeline.json",
            "plot.json",
        ):
            self.assertTrue((root / filename).is_file(), filename)
        for dirname in ("chapters", "drafts", "critique", "continuity", "final"):
            self.assertTrue((root / dirname).is_dir(), dirname)
        self.assertEqual(result["state"]["stage"], "IDEA")
        self.assertEqual(result["next_stage"], "CANON")
        self.assertTrue(result["required_structure_present"])

    def test_initialize_updates_parent_project_state(self) -> None:
        self.init()
        state = self.projects.load_project("demo")["state"]
        self.assertEqual(state["status"], "READY")
        self.assertEqual(state["domain"], "BOOK")
        self.assertEqual(state["book_stage"], "IDEA")
        self.assertEqual(state["continuity_gate_status"], "NOT_RUN")

    def test_registered_route_advances_exactly_one_stage(self) -> None:
        result = self.init()
        observed = [result["state"]["stage"]]
        for expected in BOOK_STAGES[1:-1]:
            result = self.core.advance("demo")
            observed.append(result["state"]["stage"])
            self.assertEqual(result["state"]["stage"], expected)
        self.assertEqual(tuple(observed), BOOK_STAGES[:-1])
        self.assertEqual(result["state"]["stage"], "CONTINUITY")

    def test_stage_skip_is_rejected_without_state_mutation(self) -> None:
        before = self.init()["state"]
        with self.assertRaises(BookProductionError):
            self.core.advance("demo", "OUTLINE")
        after = self.core.load("demo")["state"]
        self.assertEqual(after["stage"], "IDEA")
        self.assertEqual(after["version"], before["version"])
        self.assertEqual(after["history"], before["history"])

    def test_final_is_blocked_without_continuity_pass_and_state_does_not_move(self) -> None:
        before = self.advance_to_continuity()["state"]
        self.assertEqual(before["continuity_gate"]["status"], "NOT_RUN")
        with self.assertRaises(ContinuityGateError):
            self.core.advance("demo")
        after = self.core.load("demo")["state"]
        self.assertEqual(after["stage"], "CONTINUITY")
        self.assertEqual(after["version"], before["version"])
        self.assertEqual(after["continuity_gate"]["status"], "NOT_RUN")

    def test_continuity_gate_cannot_be_recorded_before_continuity_stage(self) -> None:
        self.init()
        with self.assertRaises(ContinuityGateError):
            self.core.set_continuity_gate(
                "demo", passed=True, evidence="fixture check"
            )
        self.assertEqual(self.core.load("demo")["state"]["stage"], "IDEA")

    def test_failed_continuity_gate_blocks_project_and_final(self) -> None:
        self.advance_to_continuity()
        failed = self.core.set_continuity_gate(
            "demo", passed=False, evidence="fixture contradiction remains"
        )
        self.assertEqual(failed["state"]["continuity_gate"]["status"], "FAIL")
        project_state = self.projects.load_project("demo")["state"]
        self.assertEqual(project_state["status"], "BLOCKED")
        self.assertEqual(project_state["continuity_gate_status"], "FAIL")
        with self.assertRaises(ContinuityGateError):
            self.core.advance("demo")
        self.assertEqual(self.core.load("demo")["state"]["stage"], "CONTINUITY")

    def test_passed_continuity_gate_allows_final_and_marks_project_done(self) -> None:
        self.advance_to_continuity()
        passed = self.core.set_continuity_gate(
            "demo", passed=True, evidence="deterministic fixture continuity PASS"
        )
        self.assertEqual(passed["state"]["continuity_gate"]["status"], "PASS")
        final = self.core.advance("demo")
        self.assertEqual(final["state"]["stage"], "FINAL")
        self.assertIsNone(final["next_stage"])
        project_state = self.projects.load_project("demo")["state"]
        self.assertEqual(project_state["status"], "DONE")
        self.assertEqual(project_state["book_stage"], "FINAL")
        self.assertEqual(project_state["continuity_gate_status"], "PASS")

    def test_failed_gate_can_be_repaired_only_by_explicit_pass(self) -> None:
        self.advance_to_continuity()
        self.core.set_continuity_gate("demo", passed=False, evidence="fixture fail")
        repaired = self.core.set_continuity_gate("demo", passed=True, evidence="fixture recheck pass")
        self.assertEqual(repaired["state"]["continuity_gate"]["status"], "PASS")
        self.assertEqual(self.projects.load_project("demo")["state"]["status"], "RUNNING")
        self.assertEqual(self.core.advance("demo")["state"]["stage"], "FINAL")

    def test_reopen_preserves_stage_gate_and_history(self) -> None:
        self.advance_to_continuity()
        first = self.core.set_continuity_gate("demo", passed=True, evidence="fixture pass")
        reopened = BookProductionCore(self.home).load("demo")
        self.assertEqual(reopened["state"]["stage"], "CONTINUITY")
        self.assertEqual(reopened["state"]["continuity_gate"], first["state"]["continuity_gate"])
        self.assertEqual(reopened["state"]["history"], first["state"]["history"])

    def test_cli_roundtrip_and_fail_closed_final(self) -> None:
        run_py = ROOT / "run.py"
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT)

        init = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(self.home),
                "book",
                "init",
                "demo",
                "--title",
                "CLI Book",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(json.loads(init.stdout)["state"]["stage"], "IDEA")

        for target in BOOK_STAGES[1:-1]:
            step = subprocess.run(
                [
                    sys.executable,
                    str(run_py),
                    "--home",
                    str(self.home),
                    "book",
                    "advance",
                    "demo",
                    "--to",
                    target,
                ],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(json.loads(step.stdout)["state"]["stage"], target)

        blocked = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(self.home),
                "book",
                "advance",
                "demo",
            ],
            check=False,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertNotEqual(blocked.returncode, 0)
        self.assertEqual(self.core.load("demo")["state"]["stage"], "CONTINUITY")

        gate = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(self.home),
                "book",
                "continuity",
                "demo",
                "--pass-gate",
                "--evidence",
                "CLI fixture pass",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(json.loads(gate.stdout)["state"]["continuity_gate"]["status"], "PASS")

        final = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(self.home),
                "book",
                "advance",
                "demo",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        self.assertEqual(json.loads(final.stdout)["state"]["stage"], "FINAL")


if __name__ == "__main__":
    unittest.main()
