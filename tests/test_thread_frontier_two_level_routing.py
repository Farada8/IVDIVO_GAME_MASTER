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
    decide_frontier_use,
    resolve_return_token as resolve_frontier_return,
)
from tools.ivdivo_thread_topic_guard import route_turn, resolve_return_token as resolve_topic_return


class ThreadFrontierTwoLevelRoutingTests(unittest.TestCase):
    def setUp(self):
        self.project = "BUSINESS_ENGINEERING_OS"
        self.topic = "BUSINESS_ENGINEERING_CURRENT_WORK"
        self.gate = "P225_ACQUIRE_CURRENT_OFFICIAL_TENDER_PACK"

    def test_generic_continuation_then_sibling_discovery_keeps_both_locks(self):
        topic = route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text="и",
            proposed_project="PUBLIC_ART_CLUAIN",
            discovered_context_project="PUBLIC_ART_CLUAIN",
            assistant_initiated_pivot=True,
        )
        self.assertEqual(topic.status, "CONTINUE_ACTIVE_TOPIC")
        self.assertEqual(topic.active_project, self.project)
        self.assertEqual(topic.active_next_gate, self.gate)
        self.assertTrue(topic.drift_blocked)

        frontier = decide_frontier_use(
            active_project=topic.active_project,
            active_next_gate=topic.active_next_gate,
            discovered_material_project="PUBLIC_ART_CLUAIN",
            relation_to_current_gate=SIBLING,
        )
        self.assertEqual(frontier.status, "SUPPORTING_ONLY_KEEP_FRONTIER")
        self.assertEqual(frontier.active_project, self.project)
        self.assertEqual(frontier.active_next_gate, self.gate)

    def test_same_project_relevant_material_passes_after_thread_lock(self):
        topic = route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text="continue",
        )
        frontier = decide_frontier_use(
            active_project=topic.active_project,
            active_next_gate=topic.active_next_gate,
            discovered_material_project=self.project,
            relation_to_current_gate=SAME_PROJECT_RELEVANT,
        )
        self.assertEqual(frontier.status, "USE_IN_CURRENT_FRONTIER")

    def test_required_dependency_has_topic_and_frontier_return_paths(self):
        topic = route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text="need external dependency",
            required_dependency=True,
        )
        self.assertEqual(topic.status, "CROSS_PROJECT_DEPENDENCY_WITH_RETURN_TOKEN")
        self.assertEqual(resolve_topic_return(topic.return_token).active_project, self.project)

        frontier = decide_frontier_use(
            active_project=self.project,
            active_next_gate=self.gate,
            discovered_material_project="DEPENDENCY_PROJECT",
            relation_to_current_gate=REQUIRED_DEPENDENCY,
        )
        self.assertEqual(frontier.status, "CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN")
        restored = resolve_frontier_return(frontier.return_token)
        self.assertEqual(restored.active_project, self.project)
        self.assertEqual(restored.active_next_gate, self.gate)

    def test_explicit_project_switch_does_not_authorize_old_frontier_reuse(self):
        topic = route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text="switch to public art",
            proposed_project="PUBLIC_ART_CLUAIN",
            proposed_topic="PUBLIC_ART_APPLICATION",
            explicit_user_switch=True,
        )
        self.assertEqual(topic.status, "SWITCH_AUTHORIZED")
        self.assertEqual(topic.active_project, "PUBLIC_ART_CLUAIN")

        # The old BUSINESS next gate is not valid merely because topic switching was authorized.
        frontier = decide_frontier_use(
            active_project=topic.active_project,
            active_next_gate=None,
            discovered_material_project="PUBLIC_ART_CLUAIN",
            relation_to_current_gate=SAME_PROJECT_RELEVANT,
        )
        self.assertEqual(frontier.status, "HOLD_NO_ACTIVE_FRONTIER")

    def test_bound_switch_confirmation_also_requires_target_frontier_restore(self):
        topic = route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text="да",
            proposed_project="PUBLIC_ART_CLUAIN",
            proposed_topic="PUBLIC_ART_APPLICATION",
            pending_switch_target="PUBLIC_ART_CLUAIN",
            user_confirms_pending_switch=True,
        )
        self.assertEqual(topic.status, "SWITCH_AUTHORIZED_BY_BOUND_CONFIRMATION")
        frontier = decide_frontier_use(
            active_project=topic.active_project,
            active_next_gate=None,
            discovered_material_project=topic.active_project,
            relation_to_current_gate=SAME_PROJECT_RELEVANT,
        )
        self.assertEqual(frontier.status, "HOLD_NO_ACTIVE_FRONTIER")

    def test_side_query_returns_to_same_thread_and_frontier(self):
        topic = route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text="а что с публичным артом?",
            side_query=True,
        )
        self.assertEqual(topic.status, "ANSWER_SIDE_QUERY_THEN_RETURN")
        restored = resolve_topic_return(topic.return_token)
        self.assertEqual(restored.active_project, self.project)
        self.assertEqual(restored.active_topic, self.topic)
        self.assertEqual(restored.active_next_gate, self.gate)


if __name__ == "__main__":
    unittest.main(verbosity=2)
