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


class MultiModelReviewCliTest(unittest.TestCase):
    def test_offline_mock_run_persists_independent_results_and_aggregate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ProjectStateManager(home).create_project("demo", "Demo")
            request_path = Path(tmp) / "review.json"
            request_path.write_text(
                json.dumps(
                    {
                        "content": "Review this frozen offline fixture.",
                        "critics": [
                            {
                                "id": "logic",
                                "provider": "mock",
                                "model": "mock-logic",
                                "instruction": "Find logical contradictions.",
                                "required": True,
                            },
                            {
                                "id": "evidence",
                                "provider": "mock",
                                "model": "mock-evidence",
                                "instruction": "Audit unsupported evidence claims.",
                                "required": True,
                            },
                        ],
                    },
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            env = dict(os.environ)
            env["PYTHONPATH"] = str(ROOT)
            completed = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "review_cli.py"),
                    "--home",
                    str(home),
                    "run",
                    "demo",
                    str(request_path),
                ],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            aggregate = json.loads(completed.stdout)
            self.assertEqual(aggregate["status"], "COMPLETE")
            self.assertEqual(aggregate["critic_count"], 2)
            self.assertEqual(aggregate["completed_count"], 2)
            self.assertEqual(aggregate["agreement"], "DISAGREEMENT")
            self.assertFalse(aggregate["truth_claimed"])
            self.assertFalse(aggregate["consensus_claimed"])
            self.assertEqual(len(aggregate["critic_results"]), 2)
            output = MemoryStore(home / "runtime" / "state.db").get(aggregate["output_memory_id"])
            self.assertEqual(output["kind"], "OUTPUT")
            self.assertEqual(output["project_id"], "demo")


if __name__ == "__main__":
    unittest.main()
