import importlib.util
from pathlib import Path
import unittest

P = Path(__file__).resolve().parents[1] / "runtime" / "cycle9_control.py"
spec = importlib.util.spec_from_file_location("c9", P)
c9 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(c9)


class Cycle9ControlTests(unittest.TestCase):
    def test_same_root_models_count_one_family(self):
        out = c9.evidence_family_count([
            {"raw_root_id": "r1", "model": "A"},
            {"raw_root_id": "r1", "model": "B"},
            {"raw_root_id": "r1", "model": "C"},
        ])
        self.assertEqual(out["independent_families"], 1)

    def test_missing_root_holds(self):
        self.assertEqual(c9.evidence_family_count([{"model": "A"}])["status"], "HOLD_MISSING_RAW_ROOT")

    def test_machine_cannot_claim_human(self):
        self.assertFalse(c9.evidence_class_firewall(claimed="HUMAN", evidence_class="MACHINE")["allowed"])

    def test_source_cannot_claim_provider(self):
        self.assertFalse(c9.evidence_class_firewall(claimed="PROVIDER", evidence_class="SOURCE")["allowed"])

    def test_promotion_missing_fields_holds(self):
        out = c9.promotion_eligibility({"scope": "DOMAIN"})
        self.assertFalse(out["eligible_for_review"])
        self.assertIn("pilot_evidence", out["blockers"])

    def test_full_machine_packet_only_review_eligible(self):
        packet = {
            "development_contract": True,
            "pilot_evidence": ["p"],
            "adversarial_review": ["a"],
            "regression_evidence": ["r"],
            "evaluation_matrix_result": "PASS",
            "scope": "DOMAIN",
            "application_targets": ["x"],
            "rollback_plan": "rb",
            "readback_plan": "rd",
        }
        out = c9.promotion_eligibility(packet)
        self.assertEqual(out["status"], "ELIGIBLE_FOR_REVIEW")
        self.assertFalse(out["auto_promote"])

    def test_required_human_blocks_without_human(self):
        packet = {
            "development_contract": True, "pilot_evidence": ["p"], "adversarial_review": ["a"],
            "regression_evidence": ["r"], "evaluation_matrix_result": "PASS", "scope": "DOMAIN",
            "application_targets": ["x"], "rollback_plan": "rb", "readback_plan": "rd",
            "requires_human": True,
        }
        self.assertIn("human_evidence", c9.promotion_eligibility(packet)["blockers"])

    def test_negative_evidence_cannot_disappear(self):
        out = c9.negative_evidence_retention(existing_negative_ids=["n1"], proposed_retained_ids=[], supersession_map={})
        self.assertFalse(out["allowed"])

    def test_negative_evidence_explicit_supersession_allowed(self):
        out = c9.negative_evidence_retention(existing_negative_ids=["n1"], proposed_retained_ids=[], supersession_map={"n1": "n2"})
        self.assertTrue(out["allowed"])

    def test_current_owner_prevents_new_engine(self):
        out = c9.engine_worthiness(recurrence=True, stateful_coordination=True, unique_runtime_contract=True, current_owner_can_absorb=True)
        self.assertEqual(out["status"], "REUSE_OR_ADAPTER")
        self.assertFalse(out["new_engine_allowed"])

    def test_even_engine_candidate_requires_review(self):
        out = c9.engine_worthiness(recurrence=True, stateful_coordination=True, unique_runtime_contract=True, current_owner_can_absorb=False)
        self.assertEqual(out["status"], "ENGINE_REVIEW_CANDIDATE")
        self.assertFalse(out["new_engine_allowed"])

    def test_meta_wip_overflow_holds(self):
        out = c9.meta_work_budget_governor(founder_selected_meta=False, meta_direct_prerequisite=False, higher_priority_product_task_unblocked=False, active_meta_primary=2, active_meta_pilots=0)
        self.assertEqual(out["route"], "REDUCE_META_WIP")

    def test_product_wins_when_meta_not_prerequisite(self):
        out = c9.meta_work_budget_governor(founder_selected_meta=False, meta_direct_prerequisite=False, higher_priority_product_task_unblocked=True, active_meta_primary=1, active_meta_pilots=1)
        self.assertEqual(out["route"], "PRODUCT")

    def test_founder_meta_focus_allows_bounded_meta(self):
        out = c9.meta_work_budget_governor(founder_selected_meta=True, meta_direct_prerequisite=False, higher_priority_product_task_unblocked=True, active_meta_primary=1, active_meta_pilots=2)
        self.assertEqual(out["route"], "META")

    def test_self_reference_cannot_waive_evidence(self):
        self.assertFalse(c9.self_reference_guard(modifies_self_improvement_gate=True, waives_required_evidence=True, externalized_review=True)["allowed"])

    def test_self_reference_needs_externalized_review(self):
        self.assertFalse(c9.self_reference_guard(modifies_self_improvement_gate=True, waives_required_evidence=False, externalized_review=False)["allowed"])

    def test_normal_non_self_change_passes(self):
        self.assertTrue(c9.self_reference_guard(modifies_self_improvement_gate=False, waives_required_evidence=False, externalized_review=False)["allowed"])


if __name__ == "__main__":
    unittest.main()
