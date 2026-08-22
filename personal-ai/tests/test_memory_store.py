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


class LocalMemoryTest(unittest.TestCase):
    def test_store_search_update_invalidate_trace_and_reopen(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            db_path = Path(td) / "runtime" / "state.db"
            store = MemoryStore(db_path)

            created = store.store(
                "Client prefers lime render on the south facade",
                kind="DECISION",
                source="meeting-note",
                metadata={"project": "demo", "confidence": "observed"},
                record_id="mem-demo",
            )
            self.assertEqual(created["status"], "ACTIVE")
            self.assertEqual(created["metadata"]["project"], "demo")

            found = store.search("lime render")
            self.assertEqual([row["id"] for row in found], ["mem-demo"])

            updated = store.update("mem-demo", content="Client prefers mineral render on the south facade")
            self.assertIn("mineral render", updated["content"])
            self.assertEqual(store.search("lime render"), [])
            self.assertEqual(store.search("mineral render")[0]["id"], "mem-demo")

            invalid = store.invalidate("mem-demo", "superseded by signed specification")
            self.assertEqual(invalid["status"], "INVALID")
            self.assertEqual(store.search("mineral render"), [])
            self.assertEqual(store.search("mineral render", include_invalid=True)[0]["id"], "mem-demo")

            trace = store.trace("mem-demo")
            self.assertEqual([event["action"] for event in trace], ["STORE", "UPDATE", "INVALIDATE"])
            self.assertEqual(trace[-1]["detail"]["reason"], "superseded by signed specification")

            with self.assertRaises(RuntimeError):
                store.update("mem-demo", content="must not mutate invalid record")

            reopened = MemoryStore(db_path)
            persisted = reopened.get("mem-demo")
            self.assertEqual(persisted["status"], "INVALID")
            self.assertEqual(len(reopened.trace("mem-demo")), 3)

    def test_search_kind_and_limit(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            store = MemoryStore(Path(td) / "state.db")
            store.store("alpha evidence", kind="EVIDENCE", record_id="m1")
            store.store("alpha note", kind="NOTE", record_id="m2")
            store.store("alpha second note", kind="NOTE", record_id="m3")
            notes = store.search("alpha", kind="note", limit=1)
            self.assertEqual(len(notes), 1)
            self.assertEqual(notes[0]["kind"], "NOTE")
            with self.assertRaises(ValueError):
                store.search("alpha", limit=0)

    def test_cli_memory_round_trip(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            env = os.environ.copy()
            env["PERSONAL_AI_HOME"] = td
            run_py = ROOT / "run.py"

            put = subprocess.run(
                [
                    sys.executable,
                    str(run_py),
                    "memory",
                    "put",
                    "Persistent CLI memory",
                    "--kind",
                    "note",
                    "--source",
                    "cli-test",
                    "--id",
                    "cli-memory",
                    "--metadata",
                    '{"project":"cli-demo"}',
                ],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(json.loads(put.stdout)["id"], "cli-memory")

            search = subprocess.run(
                [sys.executable, str(run_py), "memory", "search", "Persistent CLI"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(json.loads(search.stdout)["results"][0]["id"], "cli-memory")

            subprocess.run(
                [sys.executable, str(run_py), "memory", "update", "cli-memory", "Updated CLI memory"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            subprocess.run(
                [sys.executable, str(run_py), "memory", "invalidate", "cli-memory", "--reason", "obsolete"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            trace = subprocess.run(
                [sys.executable, str(run_py), "memory", "trace", "cli-memory"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(
                [event["action"] for event in json.loads(trace.stdout)["events"]],
                ["STORE", "UPDATE", "INVALIDATE"],
            )


if __name__ == "__main__":
    unittest.main()
