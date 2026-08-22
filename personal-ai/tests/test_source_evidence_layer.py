from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence import CLAIM_TYPES, EvidenceError, EvidenceStore, VerificationRequiredError
from memory.store import MemoryStore
from projects.manager import ProjectStateManager


class SourceEvidenceLayerTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.projects = ProjectStateManager(self.home)
        self.projects.create_project("alpha", "Alpha")
        self.projects.create_project("beta", "Beta")
        self.store = EvidenceStore(self.home)

        self.document = self.store.create_document(
            "alpha",
            "Official fixture document says the roof area is 120 square metres.",
            source_label="fixture.pdf",
            metadata={"document_path": "fixtures/fixture.pdf"},
        )
        self.source = self.store.create_source(
            "alpha",
            self.document["id"],
            "Page 2: roof area = 120 m2.",
            source_label="fixture.pdf#page=2",
            metadata={"page": 2},
        )

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_unverified_ai_inference_cannot_emit_verified_fact(self) -> None:
        claim = self.store.create_claim(
            "alpha",
            "The roof probably needs full replacement.",
            "AI_INFERENCE",
            source_ids=[self.source["id"]],
            confidence=0.62,
        )

        with self.assertRaises(VerificationRequiredError):
            self.store.emit_verified_fact(claim["id"])

        facts = MemoryStore(self.home / "runtime" / "state.db").search(
            "roof probably needs full replacement", kind="FACT", project_id="alpha"
        )
        self.assertEqual(facts, [])
        persisted = self.store.memory.get(claim["id"])
        self.assertEqual(persisted["kind"], "CLAIM")
        self.assertEqual(persisted["metadata"]["claim_type"], "AI_INFERENCE")
        self.assertEqual(persisted["metadata"]["verified_state"], "UNVERIFIED")

    def test_explicit_verification_event_allows_derived_verified_fact(self) -> None:
        claim = self.store.create_claim(
            "alpha",
            "The measured roof area is 120 square metres.",
            "AI_INFERENCE",
            source_ids=[self.source["id"]],
            confidence=0.8,
        )
        verified = self.store.verify_claim(
            claim["id"],
            verifier="fixture-human-reviewer",
            evidence="Reviewer checked the cited page against the fixture document.",
            verification_source_ids=[self.source["id"]],
        )
        fact = self.store.emit_verified_fact(claim["id"])

        self.assertEqual(verified["claim"]["metadata"]["verified_state"], "VERIFIED")
        self.assertEqual(verified["verification_event"]["kind"], "EVENT")
        self.assertEqual(
            verified["verification_event"]["metadata"]["event_type"],
            "CLAIM_VERIFICATION",
        )
        self.assertEqual(fact["kind"], "FACT")
        self.assertEqual(fact["metadata"]["record_role"], "VERIFIED_FACT")
        self.assertEqual(fact["metadata"]["derived_from_claim_id"], claim["id"])
        self.assertEqual(
            fact["metadata"]["verification_event_id"],
            verified["verification_event"]["id"],
        )

        original = self.store.memory.get(claim["id"])
        self.assertEqual(original["kind"], "CLAIM")
        self.assertEqual(original["metadata"]["claim_type"], "AI_INFERENCE")

    def test_trace_claim_returns_claim_sources_documents_and_project(self) -> None:
        source2 = self.store.create_source(
            "alpha",
            self.document["id"],
            "Appendix measurement repeats 120 m2.",
            source_label="fixture.pdf#appendix",
        )
        claim = self.store.create_claim(
            "alpha",
            "Roof area is 120 m2.",
            "SOURCE_CLAIM",
            source_ids=[self.source["id"], source2["id"]],
            confidence=0.95,
        )
        trace = self.store.trace_claim(claim["id"])

        self.assertEqual(trace["claim"]["id"], claim["id"])
        self.assertEqual([s["id"] for s in trace["sources"]], [self.source["id"], source2["id"]])
        self.assertEqual([d["id"] for d in trace["documents"]], [self.document["id"]])
        self.assertEqual(trace["project_id"], "alpha")
        self.assertEqual(trace["provenance_route"], "claim <- source <- document <- project")

    def test_all_registered_claim_types_persist_without_silent_verification(self) -> None:
        for claim_type in CLAIM_TYPES:
            claim = self.store.create_claim(
                "alpha",
                f"fixture claim for {claim_type}",
                claim_type,
                source_ids=[self.source["id"]],
                confidence=0.5,
            )
            self.assertEqual(claim["metadata"]["claim_type"], claim_type)
            self.assertEqual(claim["metadata"]["verified_state"], "UNVERIFIED")

    def test_verification_preserves_immutable_claim_versions(self) -> None:
        claim = self.store.create_claim(
            "alpha",
            "Versioned claim.",
            "HYPOTHESIS",
            source_ids=[self.source["id"]],
        )
        self.store.verify_claim(
            claim["id"], verifier="reviewer", evidence="Explicit verification event."
        )
        self.store.emit_verified_fact(claim["id"])
        versions = self.store.memory.versions(claim["id"])

        self.assertGreaterEqual(len(versions), 3)
        self.assertEqual(versions[0]["metadata"]["verified_state"], "UNVERIFIED")
        self.assertEqual(versions[1]["metadata"]["verified_state"], "VERIFIED")
        self.assertIsNotNone(versions[-1]["metadata"]["emitted_fact_id"])
        self.assertEqual(versions[0]["content"], versions[-1]["content"])

    def test_repeated_emit_is_idempotent(self) -> None:
        claim = self.store.create_claim("alpha", "Stable fact.", "FACT")
        self.store.verify_claim(claim["id"], verifier="reviewer", evidence="Checked.")
        first = self.store.emit_verified_fact(claim["id"])
        second = self.store.emit_verified_fact(claim["id"])
        self.assertEqual(first["id"], second["id"])

    def test_cross_project_source_is_rejected(self) -> None:
        beta_doc = self.store.create_document("beta", "Beta document")
        beta_source = self.store.create_source("beta", beta_doc["id"], "Beta source")
        with self.assertRaises(EvidenceError):
            self.store.create_claim(
                "alpha", "Cross project claim", "SOURCE_CLAIM", source_ids=[beta_source["id"]]
            )

    def test_non_source_record_cannot_be_used_as_claim_source(self) -> None:
        with self.assertRaises(EvidenceError):
            self.store.create_claim(
                "alpha", "Bad provenance", "SOURCE_CLAIM", source_ids=[self.document["id"]]
            )

    def test_rejected_claim_cannot_emit_or_be_silently_reverified(self) -> None:
        claim = self.store.create_claim("alpha", "Rejected inference.", "AI_INFERENCE")
        rejected = self.store.reject_claim(
            claim["id"], verifier="reviewer", evidence="Contradicted by source review."
        )
        self.assertEqual(rejected["claim"]["metadata"]["verified_state"], "REJECTED")
        with self.assertRaises(VerificationRequiredError):
            self.store.emit_verified_fact(claim["id"])
        with self.assertRaises(EvidenceError):
            self.store.verify_claim(claim["id"], verifier="reviewer", evidence="Try again")

    def test_invalid_claim_type_and_confidence_fail_closed(self) -> None:
        with self.assertRaises(EvidenceError):
            self.store.create_claim("alpha", "x", "MAGIC_FACT")
        with self.assertRaises(EvidenceError):
            self.store.create_claim("alpha", "x", "FACT", confidence=1.5)

    def test_trace_includes_verification_and_emitted_fact(self) -> None:
        claim = self.store.create_claim(
            "alpha", "Traceable verified claim", "TEST_RESULT", source_ids=[self.source["id"]]
        )
        verified = self.store.verify_claim(
            claim["id"], verifier="test-runner", evidence="Deterministic fixture passed."
        )
        fact = self.store.emit_verified_fact(claim["id"])
        trace = self.store.trace_claim(claim["id"])
        self.assertEqual(trace["verification_event"]["id"], verified["verification_event"]["id"])
        self.assertEqual(trace["emitted_fact"]["id"], fact["id"])


if __name__ == "__main__":
    unittest.main()
