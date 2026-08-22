from __future__ import annotations

import hashlib
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from memory.store import REQUIRED_PL02_TABLES, VersionedMemory


class VersionedMemoryTest(unittest.TestCase):
    def test_required_physical_tables_exist(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "state.db"
            VersionedMemory(db_path)
            with sqlite3.connect(db_path) as conn:
                tables = {
                    row[0]
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ).fetchall()
                }
            self.assertTrue(set(REQUIRED_PL02_TABLES).issubset(tables))

    def test_store_hash_search_and_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "state.db"
            memory = VersionedMemory(db_path)
            stored = memory.store(
                "documents",
                "doc-1",
                "Supplier quote for insulation materials",
                project_id="demo",
                source="drive",
                confidence=0.95,
            )
            self.assertEqual(stored["version"], 1)
            self.assertEqual(
                stored["content_hash"],
                hashlib.sha256(stored["content"].encode("utf-8")).hexdigest(),
            )
            self.assertEqual(memory.search("insulation")[0]["id"], "doc-1")

            reopened = VersionedMemory(db_path)
            self.assertEqual(reopened.get("documents", "doc-1")["content"], stored["content"])

    def test_update_preserves_immutable_versions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = VersionedMemory(Path(td) / "state.db")
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
                source="quote-2",
                confidence=0.90,
            )
            self.assertEqual(updated["version"], 2)
            versions = memory.versions("facts", "fact-1")
            self.assertEqual(len(versions), 2)
            self.assertEqual(versions[0]["content"], "Initial estimate is provisional")
            self.assertFalse(versions[0]["is_current"])
            self.assertTrue(versions[1]["is_current"])
            self.assertNotEqual(versions[0]["content_hash"], versions[1]["content_hash"])

    def test_invalidate_is_versioned_and_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = VersionedMemory(Path(td) / "state.db")
            memory.store("facts", "fact-x", "Old supplier price", source="email")
            invalid = memory.invalidate(
                "facts", "fact-x", reason="supplier issued corrected price"
            )
            self.assertEqual(invalid["status"], "INVALIDATED")
            self.assertEqual(invalid["version"], 2)
            self.assertEqual(memory.search("supplier price"), [])
            self.assertEqual(
                memory.search("supplier price", include_invalid=True)[0]["status"],
                "INVALIDATED",
            )
            with self.assertRaises(RuntimeError):
                memory.update("facts", "fact-x", content="must not mutate")

    def test_trace_source_chain_and_missing_source(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = VersionedMemory(Path(td) / "state.db")
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
            self.assertEqual([row["id"] for row in trace["chain"]], ["claim", "chapter", "book"])
            self.assertFalse(trace["cycle_detected"])
            self.assertFalse(trace["truncated"])

            memory.store(
                "facts",
                "orphan",
                "Unresolved claim",
                source="missing",
                source_id="not-present",
            )
            orphan = memory.trace_source("facts", "orphan")
            self.assertEqual(orphan["missing_source_id"], "not-present")

    def test_confidence_is_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = VersionedMemory(Path(td) / "state.db")
            with self.assertRaises(ValueError):
                memory.store("facts", "bad-high", "bad", confidence=1.1)
            with self.assertRaises(ValueError):
                memory.store("facts", "bad-low", "bad", confidence=-0.1)

    def test_duplicate_store_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            memory = VersionedMemory(Path(td) / "state.db")
            memory.store("outputs", "out-1", "first", source="system")
            with self.assertRaises(ValueError):
                memory.store("outputs", "out-1", "second", source="system")


if __name__ == "__main__":
    unittest.main()
