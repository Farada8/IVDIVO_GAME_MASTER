import importlib.util
from pathlib import Path
import sys
import unittest

ENGINE = Path(__file__).resolve().parents[1] / "engine" / "recovery_persistence_engine.py"
spec = importlib.util.spec_from_file_location("c10r_engine", ENGINE)
assert spec and spec.loader
mod = importlib.util.module_from_spec(spec)
# Python 3.12 dataclasses resolve postponed annotations through sys.modules.
# Register the dynamically loaded module before executing it.
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


class Cycle10RCanaries(unittest.TestCase):
    def good_slice(self, project="P1"):
        return mod.RecoverySlice(project, "frontier", True, True, False, ("gh", "dr"))

    def record(self, gh=True, ghr=True, dr=True, drr=True, anchors=("A",), text="A"):
        return mod.CrossStoreArtifactRecord("X", gh, ghr, dr, drr, anchors, text)

    def test_01_complete_slice(self):
        self.assertTrue(self.good_slice().complete)

    def test_02_false_resume_slice_fails(self):
        s = mod.RecoverySlice("P1", "frontier", True, True, True)
        self.assertFalse(s.complete)

    def test_03_real_incident_qualifies(self):
        e = mod.RecoveryIncident("E1", True, (self.good_slice(),))
        self.assertTrue(e.qualifies)

    def test_04_controlled_or_synthetic_incident_does_not_qualify(self):
        e = mod.RecoveryIncident("E1", False, (self.good_slice(),))
        self.assertFalse(e.qualifies)

    def test_05_duplicate_incident_id_counts_once(self):
        e1 = mod.RecoveryIncident("E1", True, (self.good_slice(),))
        e2 = mod.RecoveryIncident("E1", True, (self.good_slice("P2"),))
        self.assertEqual(mod.qualified_event_count((e1, e2)), 1)

    def test_06_two_projects_in_one_incident_still_one_event(self):
        e = mod.RecoveryIncident("E1", True, (self.good_slice("P1"), self.good_slice("P2")))
        self.assertEqual(mod.qualified_event_count((e,)), 1)
        self.assertEqual(len(mod.distinct_project_ids((e,))), 2)

    def test_07_two_unique_real_incidents_count_two(self):
        e1 = mod.RecoveryIncident("E1", True, (self.good_slice("P1"),))
        e2 = mod.RecoveryIncident("E2", True, (self.good_slice("P2"),))
        self.assertEqual(mod.qualified_event_count((e1, e2)), 2)

    def test_08_si0014_one_of_three_not_eligible(self):
        e = mod.RecoveryIncident("E1", True, (self.good_slice("P1"), self.good_slice("P2")))
        state = mod.si0014_promotion_state((e,))
        self.assertFalse(state["eligible_for_promotion_review"])
        self.assertEqual(state["state"], "READY_FOR_PILOT")

    def test_09_si0014_three_events_two_projects_review_only(self):
        events = (
            mod.RecoveryIncident("E1", True, (self.good_slice("P1"),)),
            mod.RecoveryIncident("E2", True, (self.good_slice("P2"),)),
            mod.RecoveryIncident("E3", True, (self.good_slice("P1"),)),
        )
        state = mod.si0014_promotion_state(events)
        self.assertTrue(state["eligible_for_promotion_review"])
        self.assertFalse(state["promotion_authorized"])

    def test_10_three_events_one_project_fails_diversity(self):
        events = tuple(mod.RecoveryIncident(f"E{i}", True, (self.good_slice("P1"),)) for i in range(3))
        self.assertFalse(mod.si0014_promotion_state(events)["eligible_for_promotion_review"])

    def test_11_fresh_pointer_is_current(self):
        self.assertEqual(mod.FreshnessVector("A", "A", True).route(), mod.CURRENT)

    def test_12_stale_pointer_routes_rebase_first(self):
        self.assertEqual(mod.FreshnessVector("OLD", "NEW", True).route(), mod.REBASE_FIRST)

    def test_13_missing_verified_closure_holds(self):
        self.assertEqual(mod.FreshnessVector("A", "B", False).route(), mod.HOLD)

    def test_14_cross_store_complete_requires_both_and_anchor(self):
        self.assertEqual(self.record().persistence_state(), mod.COMPLETE)

    def test_15_github_only_is_partial(self):
        self.assertEqual(self.record(dr=False, drr=False).persistence_state(), mod.PARTIAL)

    def test_16_drive_only_is_partial_not_absent(self):
        self.assertEqual(self.record(gh=False, ghr=False).persistence_state(), mod.PARTIAL)

    def test_17_no_store_is_failed(self):
        self.assertEqual(self.record(gh=False, ghr=False, dr=False, drr=False).persistence_state(), mod.FAILED)

    def test_18_wrong_semantic_anchor_blocks_complete(self):
        self.assertEqual(self.record(anchors=("EXPECTED",), text="OTHER").persistence_state(), mod.PARTIAL)

    def test_19_github_only_repair_writes_drive_only(self):
        plan = mod.partial_repair_plan(self.record(dr=False, drr=False))
        self.assertEqual(plan, ("VERIFY_THEN_WRITE_DRIVE",))

    def test_20_drive_only_repair_writes_github_only(self):
        plan = mod.partial_repair_plan(self.record(gh=False, ghr=False))
        self.assertEqual(plan, ("VERIFY_THEN_WRITE_GITHUB",))

    def test_21_bad_anchor_repairs_content_not_duplicate_store(self):
        plan = mod.partial_repair_plan(self.record(anchors=("EXPECTED",), text="OTHER"))
        self.assertEqual(plan, ("REPAIR_SEMANTIC_CONTENT_OR_HOLD",))

    def test_22_duplicate_parallel_delta_becomes_provenance_only(self):
        self.assertEqual(
            mod.semantic_salvage_route(newer_authority_exists=True, delta_unique=False, delta_compatible=True),
            "PROVENANCE_ONLY",
        )

    def test_23_unique_compatible_delta_salvages_after_rebase(self):
        self.assertEqual(
            mod.semantic_salvage_route(newer_authority_exists=True, delta_unique=True, delta_compatible=True),
            "SALVAGE_UNIQUE_DELTA_AFTER_REBASE",
        )

    def test_24_incompatible_delta_holds(self):
        self.assertEqual(
            mod.semantic_salvage_route(newer_authority_exists=True, delta_unique=True, delta_compatible=False),
            "HOLD_CONFLICT",
        )

    def test_25_same_raw_evidence_root_counts_once(self):
        self.assertEqual(mod.normalize_evidence_families(("ROOT1", "ROOT1", "ROOT1")), 1)

    def test_26_independent_roots_count_independently(self):
        self.assertEqual(mod.normalize_evidence_families(("A", "B", "A", "")), 2)

    def test_27_committed_candidate_id_collides(self):
        self.assertEqual(mod.candidate_id_route("SI-0016", {"SI-0016"}, set()), "HOLD_ID_COLLISION")

    def test_28_reserved_candidate_id_collides(self):
        self.assertEqual(mod.candidate_id_route("SI-0016", set(), {"SI-0016"}), "HOLD_ID_COLLISION")

    def test_29_v3_mechanism_with_existing_owner_merges(self):
        self.assertEqual(
            mod.v3_mechanism_tribunal(existing_owner=True, real_project_replications=0, healthy_controls=0, measured_net_gain=False, regression_pass=False),
            "MERGE_WITH_EXISTING_OWNER",
        )

    def test_30_v3_mechanism_without_real_evidence_holds(self):
        self.assertEqual(
            mod.v3_mechanism_tribunal(existing_owner=False, real_project_replications=1, healthy_controls=1, measured_net_gain=False, regression_pass=True),
            "HOLD_FOR_REAL_PRODUCTION_EVIDENCE",
        )

    def test_31_v3_mechanism_can_only_become_review_eligible(self):
        self.assertEqual(
            mod.v3_mechanism_tribunal(existing_owner=False, real_project_replications=2, healthy_controls=1, measured_net_gain=True, regression_pass=True),
            "ELIGIBLE_FOR_BOUNDED_PROMOTION_REVIEW",
        )

    def test_32_production_return_and_library_identity_fail_closed(self):
        self.assertEqual(mod.production_return_gate(None, True), "HOLD_NO_PRODUCTION_RETURN")
        self.assertEqual(mod.production_return_gate("BOOK_PRODUCTION", False), "RETURN_TO_PRODUCTION_NO_MORE_META")
        identity = mod.library_identity_state(physical_id="file1", byte_hash=None, canonical_work_id=None)
        self.assertTrue(identity["physical_present"])
        self.assertFalse(identity["unique_work_claim_allowed"])


if __name__ == "__main__":
    unittest.main()
