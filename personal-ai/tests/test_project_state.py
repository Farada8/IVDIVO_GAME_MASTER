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

from projects.manager import ProjectStateManager


class ProjectStateManagerTest(unittest.TestCase):
    def test_full_project_lifecycle_and_required_structure(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home)
            created = manager.create_project("alpha", "Alpha Project")

            project_root = home / "projects" / "alpha"
            for relative in (
                "project.yaml",
                "state.json",
                "tasks.json",
                "decisions.md",
                "artifacts",
                "references",
                "logs",
            ):
                self.assertTrue((project_root / relative).exists(), relative)
            self.assertEqual(created["state"]["status"], "NEW")
            self.assertTrue(created["required_structure_present"])

            state = manager.update_state("alpha", "READY", owner="local-user")
            self.assertEqual(state["status"], "READY")
            self.assertEqual(state["version"], 2)
            self.assertEqual(state["owner"], "local-user")

            t1 = manager.add_task("alpha", "First task", "t1")
            t2 = manager.add_task("alpha", "Second task", "t2")
            self.assertEqual(t1["status"], "READY")
            self.assertEqual(manager.get_next_task("alpha")["id"], "t1")

            completed = manager.complete_task("alpha", "t1")
            self.assertEqual(completed["status"], "DONE")
            self.assertEqual(manager.get_next_task("alpha")["id"], "t2")

            blocked = manager.block_task("alpha", "t2", "needs evidence")
            self.assertEqual(blocked["status"], "BLOCKED")
            self.assertEqual(blocked["block_reason"], "needs evidence")
            self.assertIsNone(manager.get_next_task("alpha"))

            timestamp = manager.record_decision("alpha", "Keep the project fail-closed.")
            decisions = (project_root / "decisions.md").read_text(encoding="utf-8")
            self.assertIn(timestamp, decisions)
            self.assertIn("Keep the project fail-closed.", decisions)

            loaded = manager.load_project("alpha")
            self.assertEqual(len(loaded["tasks"]), 2)

    def test_rejects_path_traversal_and_duplicate_project(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            manager = ProjectStateManager(Path(td))
            with self.assertRaises(ValueError):
                manager.create_project("../escape")
            manager.create_project("safe")
            with self.assertRaises(FileExistsError):
                manager.create_project("safe")

    def test_cli_create_status_next_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            env = os.environ.copy()
            env["PERSONAL_AI_HOME"] = td
            run_py = ROOT / "run.py"

            create = subprocess.run(
                [sys.executable, str(run_py), "project", "create", "cli-demo"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            created = json.loads(create.stdout)
            self.assertEqual(created["project_id"], "cli-demo")

            status = subprocess.run(
                [sys.executable, str(run_py), "project", "status", "cli-demo"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(json.loads(status.stdout)["state"]["status"], "NEW")

            next_result = subprocess.run(
                [sys.executable, str(run_py), "project", "next", "cli-demo"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertIsNone(json.loads(next_result.stdout)["next_task"])


if __name__ == "__main__":
    unittest.main()
