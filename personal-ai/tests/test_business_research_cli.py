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


class BusinessResearchCliTest(unittest.TestCase):
    def test_business_research_cli_persists_registered_packet(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home"
            ProjectStateManager(home).create_project("biz", "Business Research CLI")
            request_path = Path(tmp) / "request.json"
            request_path.write_text(
                json.dumps(
                    {
                        "question": "What does the supplied evidence support?",
                        "geography": "Dublin, Ireland",
                        "industry": "painting services",
                        "as_of": "2026-08-22",
                        "freshness_max_days": 30,
                        "sources": [
                            {
                                "key": "s1",
                                "title": "Supplied source",
                                "source_as_of": "2026-08-20",
                                "document_text": "The supplied source records a value of 10.",
                                "excerpt": "records a value of 10",
                            }
                        ],
                        "claims": [
                            {
                                "key": "c1",
                                "status": "OBSERVED",
                                "text": "The supplied source records a value of 10.",
                                "source_keys": ["s1"],
                            }
                        ],
                        "calculations": [],
                        "comparison": [{"candidate": "A", "value": "10", "unknown": None}],
                        "conclusions": [
                            {
                                "status": "OBSERVED",
                                "text": "The supplied source records value 10.",
                                "claim_keys": ["c1"],
                                "calculation_ids": [],
                            }
                        ],
                        "open_questions": ["Can this observation be independently verified?"],
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
                    str(ROOT / "run.py"),
                    "--home",
                    str(home),
                    "business",
                    "research",
                    "biz",
                    str(request_path),
                ],
                capture_output=True,
                text=True,
                check=False,
                env=env,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            root = Path(result["root"])
            for name in (
                "manifest.json",
                "sources.json",
                "claims.json",
                "comparison.csv",
                "conclusions.md",
                "open_questions.md",
            ):
                self.assertTrue((root / name).is_file(), name)
            research_id = result["manifest"]["research_id"]
            outputs = MemoryStore(home / "runtime" / "state.db").search(
                research_id, kind="OUTPUT", project_id="biz", limit=20
            )
            self.assertEqual(len(outputs), 1)


if __name__ == "__main__":
    unittest.main()
