from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from projects.manager import ProjectStateManager
from research import BusinessResearchService, ResearchInputError


class BusinessResearchEvidenceCeilingTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name) / "home"
        ProjectStateManager(self.home).create_project("biz", "PL07 Evidence Ceiling")
        self.service = BusinessResearchService(self.home)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    @staticmethod
    def base_request() -> dict:
        return {
            "question": "What does supplied evidence support?",
            "geography": "Dublin, Ireland",
            "industry": "painting services",
            "as_of": "2026-08-22",
            "freshness_max_days": 30,
            "sources": [
                {
                    "key": "s1",
                    "title": "Current supplied source",
                    "source_as_of": "2026-08-20",
                    "document_text": "Current supplied source records ten inquiries.",
                    "excerpt": "records ten inquiries",
                }
            ],
            "calculations": [],
            "claims": [
                {
                    "key": "obs",
                    "status": "OBSERVED",
                    "text": "The supplied source records ten inquiries.",
                    "source_keys": ["s1"],
                }
            ],
            "comparison": [],
            "conclusions": [
                {
                    "status": "OBSERVED",
                    "text": "The supplied source records ten inquiries.",
                    "claim_keys": ["obs"],
                    "calculation_ids": [],
                }
            ],
            "open_questions": [],
        }

    def test_inferred_claim_cannot_be_laundered_to_observed_conclusion(self) -> None:
        request = self.base_request()
        request["claims"][0]["status"] = "INFERRED"
        request["conclusions"][0]["status"] = "OBSERVED"
        with self.assertRaisesRegex(ResearchInputError, "OBSERVED cannot be supported"):
            self.service.create_research("biz", request)

    def test_unknown_claim_cannot_be_laundered_to_inferred_conclusion(self) -> None:
        request = self.base_request()
        request["claims"][0]["status"] = "UNKNOWN"
        request["claims"][0]["source_keys"] = []
        request["conclusions"][0]["status"] = "INFERRED"
        with self.assertRaisesRegex(ResearchInputError, "INFERRED requires at least one non-UNKNOWN"):
            self.service.create_research("biz", request)

    def test_unknown_calculation_cannot_be_laundered_to_calculated_conclusion(self) -> None:
        request = self.base_request()
        request["calculations"] = [
            {
                "id": "missing",
                "operation": "SUM",
                "operands": [None, "10"],
                "source_keys": ["s1"],
            }
        ]
        request["claims"] = [
            {
                "key": "calc",
                "status": "CALCULATED",
                "text": "This result remains unknown because an operand is missing.",
                "source_keys": [],
                "calculation_id": "missing",
            }
        ]
        request["conclusions"] = [
            {
                "status": "CALCULATED",
                "text": "The total is calculated.",
                "claim_keys": ["calc"],
                "calculation_ids": ["missing"],
            }
        ]
        with self.assertRaisesRegex(ResearchInputError, "CALCULATED cannot exceed"):
            self.service.create_research("biz", request)

    def test_future_source_may_be_recorded_but_cannot_support_claim(self) -> None:
        request = self.base_request()
        request["sources"][0]["source_as_of"] = "2026-09-01"
        with self.assertRaisesRegex(ResearchInputError, "future-dated source"):
            self.service.create_research("biz", request)

    def test_future_source_cannot_support_calculation(self) -> None:
        request = self.base_request()
        request["sources"][0]["source_as_of"] = "2026-09-01"
        request["claims"] = []
        request["conclusions"] = []
        request["calculations"] = [
            {
                "id": "bad-future",
                "operation": "SUM",
                "operands": ["10", "5"],
                "source_keys": ["s1"],
            }
        ]
        with self.assertRaisesRegex(ResearchInputError, "future-dated source"):
            self.service.create_research("biz", request)

    def test_calculated_conclusion_may_use_observed_plus_successful_calculation(self) -> None:
        request = self.base_request()
        request["calculations"] = [
            {
                "id": "sum",
                "operation": "SUM",
                "operands": ["10", "5"],
                "source_keys": ["s1"],
            }
        ]
        request["claims"].append(
            {
                "key": "calc",
                "status": "CALCULATED",
                "text": "The bounded sum is fifteen.",
                "source_keys": [],
                "calculation_id": "sum",
            }
        )
        request["conclusions"] = [
            {
                "status": "CALCULATED",
                "text": "The bounded sum is fifteen using the supplied source context.",
                "claim_keys": ["obs", "calc"],
                "calculation_ids": ["sum"],
            }
        ]
        result = self.service.create_research("biz", request)
        self.assertIn("[CALCULATED]", result["conclusions_md"])


if __name__ == "__main__":
    unittest.main()
