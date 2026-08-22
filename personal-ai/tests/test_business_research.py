from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from evidence import EvidenceStore
from memory.store import MemoryStore
from projects.manager import ProjectStateManager
from research import BusinessResearchService, ResearchInputError


class BusinessResearchTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        ProjectStateManager(self.home).create_project("biz", "Business Research")
        self.service = BusinessResearchService(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def request() -> dict:
        return {
            "question": "Which local service offer has the stronger supplied evidence?",
            "geography": "Dublin, Ireland",
            "industry": "local painting services",
            "as_of": "2026-08-22",
            "freshness_max_days": 30,
            "sources": [
                {
                    "key": "fresh",
                    "title": "Fresh supplied source",
                    "url": "https://example.test/fresh",
                    "source_as_of": "2026-08-10",
                    "retrieved_at": "2026-08-22",
                    "document_text": "Supplied source says observed demand count is 12 and unit value is 100.",
                    "excerpt": "observed demand count is 12",
                },
                {
                    "key": "stale",
                    "title": "Old supplied source",
                    "url": "https://example.test/old",
                    "source_as_of": "2026-01-01",
                    "retrieved_at": "2026-08-22",
                    "document_text": "Older supplied source reports a historical value of 80.",
                    "excerpt": "historical value of 80",
                },
                {
                    "key": "undated",
                    "title": "Undated supplied source",
                    "document_text": "Undated note says supplier lead time is not known.",
                    "excerpt": "supplier lead time is not known",
                },
            ],
            "calculations": [
                {
                    "id": "known-sum",
                    "operation": "SUM",
                    "operands": ["100", "20"],
                    "source_keys": ["fresh"],
                    "text": "Known supplied operands total 120.",
                },
                {
                    "id": "missing-sum",
                    "operation": "SUM",
                    "operands": [None, "20"],
                    "source_keys": ["undated"],
                    "text": "One required operand is missing.",
                },
            ],
            "claims": [
                {
                    "key": "observed-demand",
                    "status": "OBSERVED",
                    "text": "The supplied fresh source records demand count 12.",
                    "source_keys": ["fresh"],
                    "confidence": 0.8,
                },
                {
                    "key": "calculated-total",
                    "status": "CALCULATED",
                    "text": "The bounded arithmetic result is 120.",
                    "source_keys": [],
                    "calculation_id": "known-sum",
                },
                {
                    "key": "inference",
                    "status": "INFERRED",
                    "text": "The supplied evidence may favor the first offer.",
                    "source_keys": ["fresh"],
                    "confidence": 0.5,
                },
                {
                    "key": "missing-value",
                    "status": "CALCULATED",
                    "text": "The missing-operand result remains unknown.",
                    "source_keys": [],
                    "calculation_id": "missing-sum",
                },
            ],
            "comparison": [
                {"offer": "A", "observed_value": "100", "missing_metric": None},
                {"offer": "B", "observed_value": "80", "missing_metric": None},
            ],
            "conclusions": [
                {
                    "status": "OBSERVED",
                    "text": "A supplied source records demand count 12.",
                    "claim_keys": ["observed-demand"],
                    "calculation_ids": [],
                },
                {
                    "status": "CALCULATED",
                    "text": "The supplied operands total 120.",
                    "claim_keys": ["calculated-total"],
                    "calculation_ids": ["known-sum"],
                },
                {
                    "status": "INFERRED",
                    "text": "Offer A may warrant further validation.",
                    "claim_keys": ["inference"],
                    "calculation_ids": [],
                },
                {
                    "status": "UNKNOWN",
                    "text": "A conclusion requiring the missing operand remains unknown.",
                    "claim_keys": ["missing-value"],
                    "calculation_ids": ["missing-sum"],
                },
            ],
            "open_questions": [
                "Can the observed demand count be independently verified?",
                "What is the missing operand?",
            ],
        }

    def test_packet_persists_registered_outputs_and_provenance(self) -> None:
        result = self.service.create_research("biz", self.request())
        manifest = result["manifest"]
        self.assertEqual(manifest["question"], self.request()["question"])
        self.assertEqual(manifest["geography"], "Dublin, Ireland")
        self.assertEqual(manifest["industry"], "local painting services")
        self.assertEqual(manifest["as_of"], "2026-08-22")
        self.assertEqual(
            set(manifest["files"]),
            {"sources.json", "claims.json", "comparison.csv", "conclusions.md", "open_questions.md"},
        )

        source_rows = {item["key"]: item for item in result["sources"]["sources"]}
        self.assertEqual(source_rows["fresh"]["freshness_status"], "FRESH")
        self.assertEqual(source_rows["fresh"]["age_days"], 12)
        self.assertEqual(source_rows["stale"]["freshness_status"], "STALE")
        self.assertEqual(source_rows["undated"]["freshness_status"], "UNKNOWN")
        self.assertIsNone(source_rows["undated"]["age_days"])

        evidence = EvidenceStore(self.home)
        claims = {item["key"]: item for item in result["claims"]["claims"]}
        observed_trace = evidence.trace_claim(claims["observed-demand"]["claim_id"])
        self.assertEqual(len(observed_trace["sources"]), 1)
        self.assertEqual(len(observed_trace["documents"]), 1)
        self.assertEqual(observed_trace["project_id"], "biz")
        self.assertEqual(claims["observed-demand"]["claim_type"], "SOURCE_CLAIM")
        self.assertEqual(claims["observed-demand"]["verified_state"], "UNVERIFIED")
        self.assertEqual(claims["inference"]["claim_type"], "AI_INFERENCE")
        self.assertEqual(claims["inference"]["verified_state"], "UNVERIFIED")

    def test_calculated_and_unknown_are_not_conflated(self) -> None:
        result = self.service.create_research("biz", self.request())
        calculations = {item["id"]: item for item in result["claims"]["calculations"]}
        claims = {item["key"]: item for item in result["claims"]["claims"]}

        self.assertEqual(calculations["known-sum"]["status"], "CALCULATED")
        self.assertEqual(calculations["known-sum"]["result"], "120")
        self.assertEqual(calculations["missing-sum"]["status"], "UNKNOWN")
        self.assertIsNone(calculations["missing-sum"]["result"])
        self.assertIn("missing", calculations["missing-sum"]["unknown_reason"])
        self.assertEqual(claims["missing-value"]["status"], "UNKNOWN")
        self.assertEqual(claims["missing-value"]["claim_type"], "HYPOTHESIS")

        rows = list(csv.DictReader(io.StringIO(result["comparison_csv"])))
        self.assertEqual(rows[0]["missing_metric"], "")
        self.assertNotEqual(rows[0]["missing_metric"], "0")
        self.assertIn("UNKNOWN remains unknown", result["conclusions_md"])

    def test_every_conclusion_contains_resolved_evidence_route(self) -> None:
        result = self.service.create_research("biz", self.request())
        text = result["conclusions_md"]
        self.assertIn("Claim IDs:", text)
        self.assertIn("Source IDs:", text)
        self.assertIn("Calculation IDs:", text)
        self.assertNotIn("Source IDs: none\n\n## 1.", text)

    def test_identical_request_reopens_same_packet_without_new_output_memory(self) -> None:
        first = self.service.create_research("biz", self.request())
        memory = MemoryStore(self.home / "runtime" / "state.db")
        before = memory.search(first["manifest"]["research_id"], kind="OUTPUT", project_id="biz", limit=20)
        second = self.service.create_research("biz", self.request())
        after = memory.search(first["manifest"]["research_id"], kind="OUTPUT", project_id="biz", limit=20)
        self.assertEqual(first["manifest"]["research_id"], second["manifest"]["research_id"])
        self.assertEqual(first["manifest"]["input_sha256"], second["manifest"]["input_sha256"])
        self.assertEqual(len(before), 1)
        self.assertEqual(len(after), 1)

    def test_observed_claim_without_source_fails_closed(self) -> None:
        request = self.request()
        request["claims"][0]["source_keys"] = []
        with self.assertRaisesRegex(ResearchInputError, "OBSERVED claim requires"):
            self.service.create_research("biz", request)

    def test_conclusion_without_claim_or_calculation_fails_closed(self) -> None:
        request = self.request()
        request["conclusions"][0]["claim_keys"] = []
        request["conclusions"][0]["calculation_ids"] = []
        with self.assertRaisesRegex(ResearchInputError, "every conclusion must trace"):
            self.service.create_research("biz", request)

    def test_unknown_source_and_calculation_references_fail_closed(self) -> None:
        request = self.request()
        request["claims"][0]["source_keys"] = ["missing-source"]
        with self.assertRaisesRegex(ResearchInputError, "unknown source key"):
            self.service.create_research("biz", request)

        other_home = Path(self.tmp.name) / "other-home"
        ProjectStateManager(other_home).create_project("biz", "Other")
        other = BusinessResearchService(other_home)
        request = self.request()
        request["claims"][1]["calculation_id"] = "missing-calculation"
        with self.assertRaisesRegex(ResearchInputError, "unknown calculation_id"):
            other.create_research("biz", request)

    def test_division_by_zero_and_future_source_are_explicit(self) -> None:
        request = self.request()
        request["sources"].append(
            {
                "key": "future",
                "title": "Future-dated supplied source",
                "source_as_of": "2026-09-01",
                "document_text": "Future-dated source text.",
                "excerpt": "Future-dated source text.",
            }
        )
        result = self.service.create_research("biz", request)
        future = next(item for item in result["sources"]["sources"] if item["key"] == "future")
        self.assertEqual(future["freshness_status"], "FUTURE")
        self.assertLess(future["age_days"], 0)

        other_home = Path(self.tmp.name) / "division-home"
        ProjectStateManager(other_home).create_project("biz", "Division")
        request = self.request()
        request["calculations"] = [
            {"id": "bad-div", "operation": "DIVIDE", "operands": ["1", "0"], "source_keys": []}
        ]
        request["claims"] = []
        request["conclusions"] = []
        with self.assertRaisesRegex(ResearchInputError, "denominator cannot be zero"):
            BusinessResearchService(other_home).create_research("biz", request)


if __name__ == "__main__":
    unittest.main()
