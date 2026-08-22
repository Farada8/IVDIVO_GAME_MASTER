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

from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class PersonalKnowledgeSearchCliTest(unittest.TestCase):
    def test_ask_cli_returns_project_local_evidence_and_persists_report(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            manager = ProjectStateManager(home)
            manager.create_project("alpha", "Alpha")
            manager.add_task("alpha", "Check cedar supplier", task_id="cedar-task")
            MemoryStore(home / "runtime" / "state.db").store(
                "Cedar supplier document.",
                kind="DOCUMENT",
                source="cedar.md",
                project_id="alpha",
            )
            env = dict(os.environ)
            env["PYTHONPATH"] = str(ROOT)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "ask.py"),
                    "--home",
                    str(home),
                    "alpha",
                    "cedar",
                ],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["project_id"], "alpha")
            self.assertEqual(result["status"], "HIT")
            self.assertGreaterEqual(result["hit_count"], 2)
            self.assertTrue(Path(result["artifact_path"]).is_file())
            self.assertFalse(result["semantic_search"])
            self.assertEqual(result["search_mode"], "LITERAL_CASE_INSENSITIVE_SUBSTRING")


if __name__ == "__main__":
    unittest.main()
