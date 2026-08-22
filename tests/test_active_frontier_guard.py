import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.ivdivo_active_frontier_guard import (
    REQUIRED_DEPENDENCY,
    SAME_PROJECT_RELEVANT,
    SIBLING,
    SUPPORTING,
    UNKNOWN,
    decide_frontier_use,
    resolve_return_token,
)


class ActiveFrontierGuardTests(unittest.TestCase):
    def setUp(self):
        self.project = "BUSINESS_ENGINEERING_OS"
        self.gate = "P225_ACQUIRE_CURRENT_OFFICIAL_TENDER_PACK"

    def route(self, relation, discovered="PUBLIC_ART_CLUAIN", switch=False):
        return decide_frontier_use(
            active_project=self.project,
            active_next_gate=self.gate,
            discovered_material_project=discovered,
            relation_to_current_gate=relation,
            explicit_user_switch=switch,
        )

    def test_real_defect_fixture_artist_cv_does_not_hijack_business_frontier(self):
        out = self.route(SIBLING)
        self.assertEqual(out.status, "SUPPORTING_ONLY_KEEP_FRONTIER")
        self.assertEqual(out.active_project, self.project)
        self.assertEqual(out.active_next_gate, self.gate)

    def test_semantic_relevance_supporting_only_does_not_switch(self):
        out = self.route(SUPPORTING)
        self.assertEqual(out.status, "SUPPORTING_ONLY_KEEP_FRONTIER")

    def test_same_project_relevant_material_is_usable(self):
        out = self.route(SAME_PROJECT_RELEVANT, discovered=self.project)
        self.assertEqual(out.status, "USE_IN_CURRENT_FRONTIER")

    def test_required_cross_lane_dependency_gets_return_token(self):
        out = self.route(REQUIRED_DEPENDENCY)
        self.assertEqual(out.status, "CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN")
        self.assertEqual(out.return_token, f"RETURN::{self.project}::{self.gate}")

    def test_dependency_return_restores_original_frontier(self):
        routed = self.route(REQUIRED_DEPENDENCY)
        returned = resolve_return_token(routed.return_token)
        self.assertEqual(returned.status, "RETURN_TO_ORIGINAL_FRONTIER")
        self.assertEqual(returned.active_project, self.project)
        self.assertEqual(returned.active_next_gate, self.gate)

    def test_explicit_user_switch_authorizes_switch(self):
        out = self.route(SIBLING, switch=True)
        self.assertEqual(out.status, "SWITCH_AUTHORIZED")
        self.assertEqual(out.active_project, "PUBLIC_ART_CLUAIN")

    def test_unknown_relation_fails_closed_and_keeps_frontier(self):
        out = self.route(UNKNOWN)
        self.assertEqual(out.status, "HOLD_AMBIGUOUS_SCOPE_KEEP_FRONTIER")
        self.assertEqual(out.active_project, self.project)

    def test_missing_active_frontier_fails_closed(self):
        out = decide_frontier_use(
            active_project=None,
            active_next_gate=None,
            discovered_material_project="PUBLIC_ART_CLUAIN",
            relation_to_current_gate=SIBLING,
        )
        self.assertEqual(out.status, "HOLD_NO_ACTIVE_FRONTIER")

    def test_conflicting_same_project_claim_does_not_switch(self):
        out = self.route(SAME_PROJECT_RELEVANT, discovered="PUBLIC_ART_CLUAIN")
        self.assertEqual(out.status, "SUPPORTING_ONLY_KEEP_FRONTIER")

    def test_invalid_return_token_fails_closed(self):
        out = resolve_return_token("bad")
        self.assertEqual(out.status, "HOLD_INVALID_RETURN_TOKEN")


if __name__ == "__main__":
    unittest.main(verbosity=2)
