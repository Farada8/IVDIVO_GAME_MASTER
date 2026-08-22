from __future__ import annotations

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.bootstrap import bootstrap


class BootstrapSmokeTest(unittest.TestCase):
    def test_bootstrap_persists_and_reads_back(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            first = bootstrap(home)
            second = bootstrap(home)

            self.assertTrue(first["persisted"])
            self.assertEqual(first["project"]["id"], "demo-project")
            self.assertEqual(first["task"]["id"], "demo-task")
            self.assertEqual(second["counts"], {"projects": 1, "tasks": 1})
            self.assertTrue((home / "runtime" / "state.db").exists())
            self.assertTrue((home / "logs" / "bootstrap.log").exists())

            with sqlite3.connect(home / "runtime" / "state.db") as conn:
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM projects").fetchone()[0], 1)
                self.assertEqual(conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0], 1)

            lines = (home / "logs" / "bootstrap.log").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)


if __name__ == "__main__":
    unittest.main()
