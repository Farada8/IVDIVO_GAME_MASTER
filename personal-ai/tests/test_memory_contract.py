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

from memory.store import MemoryStore, REQUIRED_TABLES


class MemoryContractHardeningTest(unittest.TestCase):
    def test_required_named_tables_hash_confidence_and_typed_mirror(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "runtime" / "state.db"
            store = MemoryStore(db_path)
            created = store.store(
                "Verified supplier quotation",
                kind="FACT",
                source="quote.pdf",
                record_id="fact-1",
                project_id="business-1",
                confidence=0.9,
            )
            expected_hash = hashlib.sha256(created["content"].encode("utf-8")).hexdigest()
            self.assertEqual(created["content_hash"], expected_hash)
            self.assertEqual(created["confidence"], 0.9)
            self.assertEqual(created["project_id"], "business-1")
            self.assertEqual(created["version"], 1)

            with store.base.connect() as conn:
                tables = {
                    row[0]
                    for row in conn.execute(
                        "SELECT name FROM sqlite_master WHERE type='table'"
                    ).fetchall()
                }
                fact = conn.execute(
                    "SELECT id,version,project_id,confidence,content_hash,is_current FROM facts WHERE id='fact-1'"
                ).fetchone()
            self.assertTrue(set(REQUIRED_TABLES).issubset(tables))
            self.assertEqual(fact["version"], 1)
            self.assertEqual(fact["project_id"], "business-1")
            self.assertEqual(fact["content_hash"], expected_hash)
            self.assertEqual(fact["is_current"], 1)

    def test_update_and_invalidate_preserve_full_old_content_versions(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store = MemoryStore(Path(td) / "state.db")
            store.store(
                "Estimate is provisional",
                kind="FACT",
                record_id="estimate",
                source="draft",
                confidence=0.5,
            )
            updated = store.update(
                "estimate",
                content="Estimate verified against quote",
                source="supplier-quote",
                confidence=0.95,
            )
            self.assertEqual(updated["version"], 2)
            versions = store.versions("estimate")
            self.assertEqual([v["version"] for v in versions], [1, 2])
            self.assertEqual(versions[0]["content"], "Estimate is provisional")
            self.assertEqual(versions[1]["content"], "Estimate verified against quote")
            self.assertNotEqual(versions[0]["content_hash"], versions[1]["content_hash"])

            invalid = store.invalidate("estimate", "superseded by signed contract")
            self.assertEqual(invalid["version"], 3)
            self.assertEqual(invalid["status"], "INVALID")
            versions = store.versions("estimate")
            self.assertEqual(len(versions), 3)
            self.assertEqual(versions[-1]["action"], "INVALIDATE")
            self.assertEqual(versions[-1]["invalid_reason"], "superseded by signed contract")

            with store.base.connect() as conn:
                rows = conn.execute(
                    "SELECT version,content,status,is_current FROM facts WHERE id='estimate' ORDER BY version"
                ).fetchall()
            self.assertEqual([row["version"] for row in rows], [1, 2, 3])
            self.assertEqual(rows[0]["content"], "Estimate is provisional")
            self.assertEqual(rows[1]["content"], "Estimate verified against quote")
            self.assertEqual([row["is_current"] for row in rows], [0, 0, 1])
            self.assertEqual(rows[-1]["status"], "INVALID")

    def test_source_trace_chain_missing_source_and_confidence_guard(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store = MemoryStore(Path(td) / "state.db")
            store.store("Book", kind="SOURCE", record_id="src-root", source="library")
            store.store(
                "Chapter",
                kind="SOURCE",
                record_id="src-chapter",
                source="book",
                source_id="src-root",
            )
            store.store(
                "Feedback delay matters",
                kind="FACT",
                record_id="claim",
                source="chapter",
                source_id="src-chapter",
                confidence=0.8,
            )
            trace = store.trace_source("claim")
            self.assertEqual(
                [item["id"] for item in trace["chain"]],
                ["claim", "src-chapter", "src-root"],
            )
            self.assertFalse(trace["cycle_detected"])

            store.store(
                "Unresolved",
                kind="FACT",
                record_id="orphan",
                source="unknown",
                source_id="missing-source",
            )
            orphan = store.trace_source("orphan")
            self.assertEqual(orphan["missing_source_id"], "missing-source")
            with self.assertRaises(ValueError):
                store.store("bad", kind="FACT", record_id="bad", confidence=1.1)

    def test_legacy_memory_record_is_migrated_without_content_loss(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "state.db"
            conn = sqlite3.connect(db_path)
            conn.executescript(
                """
                CREATE TABLE memory_records (
                    id TEXT PRIMARY KEY,
                    kind TEXT NOT NULL,
                    content TEXT NOT NULL,
                    status TEXT NOT NULL,
                    source TEXT,
                    metadata_json TEXT NOT NULL,
                    invalid_reason TEXT,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                );
                CREATE TABLE memory_events (
                    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    memory_id TEXT NOT NULL,
                    action TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    detail_json TEXT NOT NULL
                );
                """
            )
            conn.execute(
                "INSERT INTO memory_records VALUES(?,?,?,?,?,?,?,?,?)",
                (
                    "legacy-1",
                    "DECISION",
                    "Keep original content",
                    "ACTIVE",
                    "old-system",
                    json.dumps({"project": "legacy-project"}),
                    None,
                    "2026-08-21T00:00:00+00:00",
                    "2026-08-21T00:00:00+00:00",
                ),
            )
            conn.commit()
            conn.close()

            store = MemoryStore(db_path)
            migrated = store.get("legacy-1")
            self.assertEqual(migrated["content"], "Keep original content")
            self.assertEqual(migrated["project_id"], "legacy-project")
            self.assertEqual(migrated["version"], 1)
            versions = store.versions("legacy-1")
            self.assertEqual(versions[0]["action"], "LEGACY_SNAPSHOT")
            self.assertEqual(versions[0]["content"], "Keep original content")
            with store.base.connect() as conn2:
                typed = conn2.execute(
                    "SELECT content FROM decisions WHERE id='legacy-1' AND version=1"
                ).fetchone()
            self.assertEqual(typed["content"], "Keep original content")

    def test_extended_cli_preserves_existing_commands_and_exposes_versions(self) -> None:
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

            run(
                "memory",
                "put",
                "Source interview",
                "--kind",
                "source",
                "--id",
                "src-cli",
                "--source",
                "user",
            )
            fact = run(
                "memory",
                "put",
                "Client prefers written quote",
                "--kind",
                "fact",
                "--id",
                "fact-cli",
                "--source",
                "interview",
                "--source-id",
                "src-cli",
                "--project-id",
                "business-cli",
                "--confidence",
                "0.9",
            )
            self.assertEqual(fact["version"], 1)
            run("memory", "update", "fact-cli", "Client prefers itemized written quote")
            versions = run("memory", "versions", "fact-cli")
            self.assertEqual(len(versions["versions"]), 2)
            provenance = run("memory", "source-trace", "fact-cli")
            self.assertEqual(
                [item["id"] for item in provenance["chain"]],
                ["fact-cli", "src-cli"],
            )
            filtered = run(
                "memory",
                "search",
                "itemized",
                "--kind",
                "fact",
                "--project-id",
                "business-cli",
            )
            self.assertEqual(filtered["results"][0]["id"], "fact-cli")


if __name__ == "__main__":
    unittest.main()
