from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from knowledge import KnowledgeSearchError, PersonalKnowledgeSearch, SEARCH_MODE
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class PersonalKnowledgeSearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.projects = ProjectStateManager(self.home)
        self.projects.create_project("alpha", "Alpha")
        self.projects.create_project("beta", "Beta")
        self.projects.add_task("alpha", "Investigate cedar supplier", task_id="task-cedar")
        self.projects.update_state("alpha", "RUNNING", focus="cedar launch")
        self.projects.record_decision("alpha", "Use cedar only after supplier evidence is verified.")
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.alpha_doc = self.memory.store(
            "Cedar supplier document for Alpha project.",
            kind="DOCUMENT",
            source="alpha-file.md",
            project_id="alpha",
        )
        self.alpha_source = self.memory.store(
            "Cedar excerpt from supplier document.",
            kind="SOURCE",
            source="alpha-file.md excerpt",
            project_id="alpha",
            source_id=self.alpha_doc["id"],
        )
        self.alpha_decision = self.memory.store(
            "Cedar purchase requires written approval.",
            kind="DECISION",
            source="decision register",
            project_id="alpha",
        )
        self.alpha_note = self.memory.store(
            "Cedar generic working note.",
            kind="NOTE",
            source="operator note",
            project_id="alpha",
        )
        invalid = self.memory.store(
            "Cedar invalid obsolete memory must never return.",
            kind="NOTE",
            source="obsolete",
            project_id="alpha",
        )
        self.memory.invalidate(invalid["id"], "superseded")
        self.beta_doc = self.memory.store(
            "Cedar confidential Beta-only document.",
            kind="DOCUMENT",
            source="beta-file.md",
            project_id="beta",
        )
        self.search = PersonalKnowledgeSearch(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_ask_separates_project_state_documents_decisions_and_memory(self) -> None:
        result = self.search.ask("alpha", "cedar")
        self.assertEqual(result["status"], "HIT")
        self.assertEqual(result["answer_status"], "EVIDENCE_FOUND")
        self.assertEqual(result["search_mode"], SEARCH_MODE)
        self.assertFalse(result["semantic_search"])
        self.assertFalse(result["embeddings_used"])
        self.assertTrue(result["source_separation_enforced"])
        self.assertTrue(result["invalidated_memory_excluded"])
        self.assertFalse(result["cross_project_search"])

        groups = result["groups"]
        self.assertTrue(any(hit["source_type"] == "PROJECT_STATE" for hit in groups["project_state"]))
        self.assertTrue(any(hit["source_type"] == "PROJECT_TASK" for hit in groups["project_state"]))
        document_ids = {hit["record_id"] for hit in groups["documents"]}
        self.assertIn(self.alpha_doc["id"], document_ids)
        self.assertIn(self.alpha_source["id"], document_ids)
        self.assertTrue(any(hit["source_type"] == "PROJECT_DECISION_LOG" for hit in groups["decisions"]))
        self.assertIn(self.alpha_decision["id"], {hit["record_id"] for hit in groups["decisions"]})
        self.assertIn(self.alpha_note["id"], {hit["record_id"] for hit in groups["memory"]})

    def test_cross_project_and_invalidated_records_do_not_leak(self) -> None:
        result = self.search.ask("alpha", "cedar")
        all_hits = [hit for group in result["groups"].values() for hit in group]
        ids = {hit["record_id"] for hit in all_hits}
        self.assertNotIn(self.beta_doc["id"], ids)
        self.assertTrue(all(hit.get("project_id") == "alpha" for hit in all_hits))
        self.assertNotIn("obsolete memory", " ".join(hit["snippet"] for hit in all_hits).lower())

    def test_no_hit_is_unknown_not_fabricated(self) -> None:
        result = self.search.ask("alpha", "nonexistent-zebra-token")
        self.assertEqual(result["status"], "NO_HIT")
        self.assertEqual(result["answer_status"], "UNKNOWN")
        self.assertEqual(result["hit_count"], 0)
        self.assertTrue(all(not group for group in result["groups"].values()))
        self.assertIn("never converted into a fabricated answer", result["evidence_boundary"])

    def test_report_is_persisted_and_readback_matches(self) -> None:
        result = self.search.ask("alpha", "cedar")
        path = Path(result["artifact_path"])
        self.assertTrue(path.is_file())
        readback = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(readback["search_id"], result["search_id"])
        self.assertEqual(readback["project_id"], "alpha")
        self.assertEqual(readback["hit_count"], result["hit_count"])

    def test_limit_and_input_validation_fail_closed(self) -> None:
        with self.assertRaises(KnowledgeSearchError):
            self.search.ask("alpha", "")
        with self.assertRaises(KnowledgeSearchError):
            self.search.ask("alpha", "cedar", limit=0)
        with self.assertRaises(KnowledgeSearchError):
            self.search.ask("alpha", "cedar", limit=201)
        with self.assertRaises(FileNotFoundError):
            self.search.ask("missing-project", "cedar")

    def test_global_limit_is_deterministic_and_preserves_group_order(self) -> None:
        result = self.search.ask("alpha", "cedar", limit=2)
        self.assertEqual(result["hit_count"], 2)
        self.assertEqual(len(result["groups"]["project_state"]), 2)
        self.assertEqual(result["groups"]["documents"], [])
        self.assertEqual(result["groups"]["decisions"], [])
        self.assertEqual(result["groups"]["memory"], [])


if __name__ == "__main__":
    unittest.main()
