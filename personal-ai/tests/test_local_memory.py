from __future__ import annotations

import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from memory.store import LocalMemory, REQUIRED_TABLES


class LocalMemoryTest(unittest.TestCase):
    def test_required_tables_and_store_search(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "state.db"
            memory = LocalMemory(db_path)
            memory.initialize()

            with sqlite3.connect(db_path) as conn:
                tables = {
                    row[0]
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ).fetchall()
                }
            self.assertTrue(set(REQUIRED_TABLES).issubset(tables))

            stored = memory.store(
                "documents",
                "doc-1",
                "Supplier quote for insulation materials",
                project_id="business-demo",
                source="drive",
                confidence=0.95,
            )
            self.assertEqual(stored["version"], 1)
            self.assertEqual(stored["status"], "ACTIVE")
            self.assertEqual(
                stored["content_hash"],
                hashlib.sha256(stored["content"].encode("utf-8")).hexdigest(),
            )
            results = memory.search("insulation", project_id="business-demo")
            self.assertEqual([r["id"] for r in results], ["doc-1"])

    def test_update_preserves_old_version_instead_of_overwriting(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = LocalMemory(Path(td) / "state.db")
            memory.initialize()
            memory.store(
                "facts",
                "fact-1",
                "Initial estimate is provisional",
                source="quote-1",
                confidence=0.60,
            )
            updated = memory.update(
                "facts",
                "fact-1",
                content="Estimate verified against supplier quote",
                confidence=0.90,
                source="quote-2",
            )
            self.assertEqual(updated["version"], 2)
            self.assertTrue(updated["is_current"])

            versions = memory.get_versions("facts", "fact-1")
            self.assertEqual(len(versions), 2)
            self.assertEqual(versions[0]["content"], "Initial estimate is provisional")
            self.assertFalse(versions[0]["is_current"])
            self.assertEqual(
                versions[1]["content"], "Estimate verified against supplier quote"
            )
            self.assertNotEqual(versions[0]["content_hash"], versions[1]["content_hash"])

    def test_invalidate_is_versioned_and_hidden_from_normal_search(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = LocalMemory(Path(td) / "state.db")
            memory.initialize()
            memory.store("facts", "fact-x", "Old supplier price", source="email")
            invalid = memory.invalidate(
                "facts", "fact-x", reason="supplier issued corrected price"
            )
            self.assertEqual(invalid["version"], 2)
            self.assertEqual(invalid["status"], "INVALIDATED")
            self.assertEqual(
                invalid["invalidation_reason"], "supplier issued corrected price"
            )
            self.assertEqual(memory.search("supplier price"), [])
            included = memory.search("supplier price", include_invalid=True)
            self.assertEqual(len(included), 1)
            self.assertEqual(included[0]["status"], "INVALIDATED")
            self.assertEqual(len(memory.get_versions("facts", "fact-x")), 2)

    def test_trace_source_chain_and_missing_source_are_explicit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = LocalMemory(Path(td) / "state.db")
            memory.initialize()
            memory.store("sources", "book", "Systems book", source="library")
            memory.store(
                "sources",
                "chapter",
                "Chapter on feedback",
                source="book",
                source_id="book",
            )
            memory.store(
                "facts",
                "claim",
                "Feedback delay can destabilize a loop",
                source="chapter",
                source_id="chapter",
                confidence=0.80,
            )
            trace = memory.trace_source("facts", "claim")
            self.assertEqual([item["id"] for item in trace["chain"]], ["claim", "chapter", "book"])
            self.assertFalse(trace["cycle_detected"])
            self.assertFalse(trace["truncated"])

            memory.store(
                "facts",
                "orphan",
                "Unresolved claim",
                source="missing",
                source_id="not-present",
            )
            orphan_trace = memory.trace_source("facts", "orphan")
            self.assertEqual(orphan_trace["missing_source_id"], "not-present")

    def test_confidence_range_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = LocalMemory(Path(td) / "state.db")
            memory.initialize()
            with self.assertRaises(ValueError):
                memory.store("facts", "bad", "bad confidence", confidence=1.1)

    def test_cli_store_search_update_versions_trace_and_invalidate(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            env = os.environ.copy()
            env["PERSONAL_AI_HOME"] = td
            run_py = ROOT / "run.py"

            def run(*args: str) -> dict:
                completed = subprocess.run(
                    [sys.executable, str(run_py), *args],
                    check=True,
                    capture_output=True,
                    text=True,
                    env=env,
                )
                return json.loads(completed.stdout)

            run("memory", "store", "sources", "src-1", "Client interview", "--source", "user")
            stored = run(
                "memory",
                "store",
                "facts",
                "pref-1",
                "Client prefers written quotes",
                "--source",
                "interview",
                "--source-id",
                "src-1",
                "--confidence",
                "0.9",
            )
            self.assertEqual(stored["version"], 1)

            searched = run("memory", "search", "written quotes", "--entity", "facts")
            self.assertEqual(searched["results"][0]["id"], "pref-1")

            updated = run(
                "memory",
                "update",
                "facts",
                "pref-1",
                "--content",
                "Client prefers itemized written quotes",
            )
            self.assertEqual(updated["version"], 2)

            versions = run("memory", "versions", "facts", "pref-1")
            self.assertEqual(len(versions["versions"]), 2)

            trace = run("memory", "trace", "facts", "pref-1")
            self.assertEqual([item["id"] for item in trace["chain"]], ["pref-1", "src-1"])

            invalid = run(
                "memory",
                "invalidate",
                "facts",
                "pref-1",
                "--reason",
                "client changed preference",
            )
            self.assertEqual(invalid["status"], "INVALIDATED")
            hidden = run("memory", "search", "itemized", "--entity", "facts")
            self.assertEqual(hidden["results"], [])


if __name__ == "__main__":
    unittest.main()
