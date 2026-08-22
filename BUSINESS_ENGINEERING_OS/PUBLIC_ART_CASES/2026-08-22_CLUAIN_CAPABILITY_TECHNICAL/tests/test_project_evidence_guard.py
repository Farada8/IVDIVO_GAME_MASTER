import sys
import unittest
from pathlib import Path

CASE_ROOT = Path(__file__).resolve().parents[1]
if str(CASE_ROOT) not in sys.path:
    sys.path.insert(0, str(CASE_ROOT))

from engine.project_evidence_guard import (
    archive_loss_effect,
    bind_image_to_work,
    classify_project_record,
    normalize_budget,
    three_project_gate,
)


def full_record(title="Project A"):
    return {
        "title": title,
        "context": "Named venue/client",
        "timeframe": "2019",
        "overall_budget": 10000,
        "photo_refs": ["photo.jpg"],
        "applicant_role": "artist / delivery lead",
        "relevant_delivery_context_proven": True,
    }


class ProjectEvidenceTests(unittest.TestCase):
    def test_full_record_class_a(self):
        out = classify_project_record(full_record())
        self.assertTrue(out["submission_ready"])
        self.assertEqual(out["class"], "CLASS_A_SUBMISSION_READY")

    def test_guelder_like_record_budget_missing_holds(self):
        row = full_record("Guelder Rose Paths")
        row["overall_budget"] = None
        row["relevant_delivery_context_proven"] = False
        out = classify_project_record(row)
        self.assertFalse(out["submission_ready"])
        self.assertIn("overall_budget", out["missing"])
        self.assertIn("relevant_delivery_context_proven", out["missing"])

    def test_portfolio_object_not_public_delivery_case(self):
        row = {
            "title": "Ukraine (diptych; working title)",
            "context": "RHA selected-work pack",
            "timeframe": None,
            "overall_budget": None,
            "photo_refs": ["full.jpg", "detail.jpg"],
            "applicant_role": "artist",
            "relevant_delivery_context_proven": False,
        }
        out = classify_project_record(row)
        self.assertEqual(out["status"], "HOLD_INCOMPLETE_PROJECT_RECORD")
        self.assertEqual(out["class"], "CLASS_B_DOCUMENTED_WORK_INCOMPLETE_PROJECT_FIELDS")

    def test_delivery_context_is_independently_required(self):
        row = full_record("Complete metadata but no delivery proof")
        row["relevant_delivery_context_proven"] = False
        out = classify_project_record(row)
        self.assertFalse(out["submission_ready"])
        self.assertIn("relevant_delivery_context_proven", out["missing"])

    def test_three_project_gate_needs_three_class_a(self):
        rows = [full_record("A"), full_record("B")]
        weak = full_record("C")
        weak["overall_budget"] = None
        rows.append(weak)
        out = three_project_gate(rows)
        self.assertEqual(out["status"], "HOLD_THREE_PROJECT_EVIDENCE")
        self.assertEqual(out["submission_ready_count"], 2)

    def test_three_project_gate_passes_three_complete(self):
        self.assertEqual(three_project_gate([full_record("A"), full_record("B"), full_record("C")])["status"], "PASS_THREE_PROJECT_EVIDENCE")

    def test_visual_similarity_alone_does_not_bind(self):
        self.assertEqual(bind_image_to_work(visual_match_only=True, documentary_binding=False), "HOLD_VISUAL_MATCH_ONLY")

    def test_documentary_binding_can_bind_image(self):
        self.assertEqual(bind_image_to_work(visual_match_only=True, documentary_binding=True), "BOUND")

    def test_unknown_budget_stays_null(self):
        self.assertIsNone(normalize_budget(None))
        self.assertIsNone(normalize_budget("UNKNOWN"))

    def test_not_applicable_budget_requires_authority(self):
        self.assertEqual(normalize_budget(None, authoritative_not_applicable=True), "NOT_APPLICABLE_AUTHORITY_BOUND")

    def test_archive_loss_does_not_fill_field(self):
        self.assertIsNone(archive_loss_effect(archive_loss_documented=True, missing_project_field=None))


if __name__=="__main__":
    unittest.main(verbosity=2)
