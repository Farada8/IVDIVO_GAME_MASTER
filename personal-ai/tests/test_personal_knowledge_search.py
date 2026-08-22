from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PERSONAL_AI = Path(__file__).resolve().parents[1]
if str(PERSONAL_AI) not in sys.path:
    sys.path.insert(0, str(PERSONAL_AI))

from evidence import EvidenceStore
from ingestion import FileIngestionService
from knowledge import KnowledgeSearchError, PersonalKnowledgeSearch
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class PersonalKnowledgeSearchTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        self.manager = ProjectStateManager(self.home)
        self.manager.create_project("p1", "Primary Project")
        self.manager.create_project("p2", "Other Project")
        self.manager.add_task("p1", "Alpha delivery task")
        self.manager.record_decision("p1", "Choose Alpha supplier after review")

        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        obsolete = self.memory.store(
            "Alpha obsolete memory that must not return",
            kind="NOTE",
            project_id="p1",
            source="fixture",
        )
        self.memory.invalidate(obsolete["id"], "superseded fixture")
        self.memory.store(
            "Alpha confidential record from another project",
            kind="NOTE",
            project_id="p2",
            source="fixture",
        )

        evidence = EvidenceStore(self.home)
        doc = evidence.create_document("p1", "Alpha source document body")
        source = evidence.create_source("p1", doc["id"], "Alpha source excerpt")
        self.inference = evidence.create_claim(
            "p1",
            "Alpha inferred opportunity",
            "AI_INFERENCE",
            source_ids=[source["id"]],
            confidence=0.6,
        )
        candidate = evidence.create_claim(
            "p1",
            "Alpha externally checked statement",
            "SOURCE_CLAIM",
            source_ids=[source["id"]],
            confidence=0.9,
        )
        evidence.verify_claim(
            candidate["id"],
            verifier="fixture-reviewer",
            evidence="Fixture verification event",
            verification_source_ids=[source["id"]],
        )
        self.fact = evidence.emit_verified_fact(candidate["id"])

        source_file = Path(self.tmp.name) / "alpha_notes.txt"
        source_file.write_text("Alpha ingestion record for project p1", encoding="utf-8")
        self.ingestion = FileIngestionService(self.home).ingest("p1", source_file)
        self.search = PersonalKnowledgeSearch(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_project_scoped_search_keeps_source_types_and_authority_separate(self) -> None:
        result = self.search.ask("what have we already done about alpha", project_id="p1", limit=100)
        self.assertEqual(result["status"], "FOUND")
        self.assertEqual(result["search_mode"], "LEXICAL_ONLY")
        self.assertTrue(result["results"])
        self.assertTrue(all(item.get("project_id") == "p1" for item in result["results"]))

        source_types = {item["source_type"] for item in result["results"]}
        self.assertIn("PROJECT_STATE", source_types)
        self.assertIn("DECISION_FILE", source_types)
        self.assertIn("DOCUMENT", source_types)
        self.assertIn("CLAIM", source_types)
        self.assertIn("FACT", source_types)

        by_id = {item.get("memory_id"): item for item in result["results"] if item.get("memory_id")}
        self.assertEqual(by_id[self.inference["id"]]["authority"], "AI_INFERENCE_UNVERIFIED")
        self.assertEqual(by_id[self.fact["id"]]["authority"], "VERIFIED_FACT")
        self.assertGreaterEqual(len(by_id[self.fact["id"]]["provenance_chain"]), 2)

    def test_invalidated_memory_is_not_returned(self) -> None:
        result = self.search.ask("obsolete", project_id="p1", limit=100)
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["results"], [])

    def test_project_scope_blocks_cross_project_leakage(self) -> None:
        scoped = self.search.ask("confidential", project_id="p1", limit=100)
        self.assertEqual(scoped["status"], "UNKNOWN")
        global_result = self.search.ask("confidential", limit=100)
        self.assertEqual(global_result["status"], "FOUND")
        self.assertEqual({item["project_id"] for item in global_result["results"]}, {"p2"})

    def test_no_hit_returns_unknown_not_fabricated_answer(self) -> None:
        result = self.search.ask("nonexistent-knowledge-token", project_id="p1")
        self.assertEqual(result["status"], "UNKNOWN")
        self.assertEqual(result["result_count"], 0)
        self.assertEqual(result["results"], [])
        self.assertTrue(result["answer"].startswith("UNKNOWN:"))

    def test_ingested_document_is_retrieved_with_memory_source_reference(self) -> None:
        result = self.search.ask("ingestion", project_id="p1", limit=100)
        docs = [item for item in result["results"] if item["source_type"] == "DOCUMENT"]
        self.assertTrue(any(item.get("memory_id") == self.ingestion["document_memory_id"] for item in docs))
        hit = next(item for item in docs if item.get("memory_id") == self.ingestion["document_memory_id"])
        self.assertEqual(hit["authority"], "SOURCE_MATERIAL_NOT_TRUTH_VERIFIED")
        self.assertGreaterEqual(len(hit["provenance_chain"]), 2)

    def test_result_is_persisted_outside_searchable_memory_and_is_stable(self) -> None:
        first = self.search.ask("alpha", project_id="p1", limit=100)
        second = self.search.ask("alpha", project_id="p1", limit=100)
        self.assertEqual(first["result_id"], second["result_id"])
        self.assertEqual(first["result_count"], second["result_count"])
        persisted = self.home / first["persisted_result"]
        self.assertTrue(persisted.is_file())
        stored = json.loads(persisted.read_text(encoding="utf-8"))
        self.assertEqual(stored["result_id"], first["result_id"])
        self.assertEqual(
            self.memory.search("Traceable stored matches found", project_id="p1", include_invalid=False),
            [],
        )

    def test_verified_claim_does_not_masquerade_as_verified_fact(self) -> None:
        result = self.search.ask("externally checked", project_id="p1", limit=100)
        claims = [item for item in result["results"] if item["source_type"] == "CLAIM"]
        facts = [item for item in result["results"] if item["source_type"] == "FACT"]
        self.assertTrue(any(item["authority"] == "SOURCE_CLAIM_VERIFIED" for item in claims))
        self.assertTrue(any(item["authority"] == "VERIFIED_FACT" for item in facts))

    def test_invalid_query_and_limit_fail_closed(self) -> None:
        with self.assertRaises(KnowledgeSearchError):
            self.search.ask("   ", project_id="p1")
        with self.assertRaises(KnowledgeSearchError):
            self.search.ask("alpha", project_id="p1", limit=0)
        with self.assertRaises(KnowledgeSearchError):
            self.search.ask("alpha", project_id="p1", limit=201)

    def test_unknown_project_fails_closed(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.search.ask("alpha", project_id="missing")

    def test_cli_roundtrip(self) -> None:
        run_py = PERSONAL_AI / "run.py"
        proc = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(self.home),
                "ask",
                "what have we already done about alpha",
                "--project",
                "p1",
                "--limit",
                "100",
            ],
            cwd=PERSONAL_AI,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stderr)
        payload = json.loads(proc.stdout)
        self.assertEqual(payload["status"], "FOUND")
        self.assertEqual(payload["scope"]["project_id"], "p1")
        self.assertEqual(payload["search_mode"], "LEXICAL_ONLY")


if __name__ == "__main__":
    unittest.main()
