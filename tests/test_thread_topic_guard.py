import sys
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.ivdivo_thread_topic_guard import is_bare_continuation, route_turn, resolve_return_token


class ThreadTopicContinuityGuardTests(unittest.TestCase):
    def setUp(self):
        self.project = "ORBITAL_YOUTH_BOOK"
        self.topic = "ORBITAL_YOUTH_CURRENT_BOOK_WORK"
        self.gate = "CONTINUE_FROM_LAST_CONFIRMED_BOOK_FRONTIER"

    def route(self, text, **kwargs):
        return route_turn(
            active_project=self.project,
            active_topic=self.topic,
            active_next_gate=self.gate,
            user_text=text,
            **kwargs,
        )

    def test_real_defect_bare_i_does_not_switch_orbital_to_company(self):
        out = self.route(
            "и",
            proposed_project="SYNTHESIS_IVDIVO_BUSINESS",
            proposed_topic="BUSINESS_ENGINEERING",
            assistant_initiated_pivot=True,
        )
        self.assertEqual(out.status, "CONTINUE_ACTIVE_TOPIC")
        self.assertEqual(out.active_project, self.project)
        self.assertEqual(out.active_topic, self.topic)
        self.assertTrue(out.drift_blocked)

    def test_dalshe_inherits_active_topic(self):
        out = self.route("дальше", proposed_project="SIL")
        self.assertEqual(out.status, "CONTINUE_ACTIVE_TOPIC")
        self.assertEqual(out.active_project, self.project)

    def test_ok_inherits_active_topic(self):
        out = self.route("ок", proposed_project="SYNTHESIS_IVDIVO_BUSINESS")
        self.assertEqual(out.status, "CONTINUE_ACTIVE_TOPIC")

    def test_continue_inherits_active_topic(self):
        out = self.route("продолжай", discovered_context_project="BUSINESS_ENGINEERING_OS")
        self.assertEqual(out.status, "CONTINUE_ACTIVE_TOPIC")
        self.assertTrue(out.drift_blocked)

    def test_bare_yes_without_bound_switch_does_not_switch(self):
        out = self.route("да", proposed_project="SYNTHESIS_IVDIVO_BUSINESS")
        self.assertEqual(out.status, "CONTINUE_ACTIVE_TOPIC")
        self.assertEqual(out.active_project, self.project)

    def test_bound_yes_can_confirm_exact_pending_switch(self):
        out = self.route(
            "да",
            proposed_project="SYNTHESIS_IVDIVO_BUSINESS",
            proposed_topic="BUSINESS_ENGINEERING",
            pending_switch_target="SYNTHESIS_IVDIVO_BUSINESS",
            user_confirms_pending_switch=True,
        )
        self.assertEqual(out.status, "SWITCH_AUTHORIZED_BY_BOUND_CONFIRMATION")
        self.assertEqual(out.active_project, "SYNTHESIS_IVDIVO_BUSINESS")

    def test_bound_confirmation_mismatch_fails_closed(self):
        out = self.route(
            "да",
            proposed_project="SIL",
            pending_switch_target="SYNTHESIS_IVDIVO_BUSINESS",
            user_confirms_pending_switch=True,
        )
        self.assertEqual(out.status, "HOLD_SWITCH_CONFIRMATION_TARGET_MISMATCH")
        self.assertEqual(out.active_project, self.project)

    def test_explicit_switch_authorizes_new_project(self):
        out = self.route(
            "теперь переключись на компанию",
            proposed_project="SYNTHESIS_IVDIVO_BUSINESS",
            proposed_topic="BUSINESS_ENGINEERING",
            explicit_user_switch=True,
        )
        self.assertEqual(out.status, "SWITCH_AUTHORIZED")
        self.assertEqual(out.active_project, "SYNTHESIS_IVDIVO_BUSINESS")

    def test_side_query_does_not_rebind_thread(self):
        out = self.route(
            "а что с компанией?",
            proposed_project="SYNTHESIS_IVDIVO_BUSINESS",
            side_query=True,
        )
        self.assertEqual(out.status, "ANSWER_SIDE_QUERY_THEN_RETURN")
        self.assertEqual(out.active_project, self.project)
        returned = resolve_return_token(out.return_token)
        self.assertEqual(returned.status, "RETURN_TO_ORIGINAL_TOPIC")
        self.assertEqual(returned.active_project, self.project)
        self.assertEqual(returned.active_topic, self.topic)

    def test_required_dependency_gets_return_token(self):
        out = self.route(
            "проверь зависимость",
            proposed_project="SHARED_AUDIO_ENGINE",
            required_dependency=True,
        )
        self.assertEqual(out.status, "CROSS_PROJECT_DEPENDENCY_WITH_RETURN_TOKEN")
        returned = resolve_return_token(out.return_token)
        self.assertEqual(returned.active_project, self.project)

    def test_discovered_sibling_context_is_supporting_only(self):
        out = self.route(
            "проверь текущий фрагмент",
            discovered_context_project="BUSINESS_ENGINEERING_OS",
        )
        self.assertEqual(out.status, "SUPPORTING_CONTEXT_ONLY_KEEP_TOPIC")
        self.assertEqual(out.active_project, self.project)

    def test_same_project_topic_update_is_allowed(self):
        out = self.route(
            "теперь проверь главу 7",
            proposed_project=self.project,
            proposed_topic="ORBITAL_YOUTH_CH07",
        )
        self.assertEqual(out.status, "UPDATE_TOPIC_WITHIN_ACTIVE_PROJECT")
        self.assertEqual(out.active_project, self.project)
        self.assertEqual(out.active_topic, "ORBITAL_YOUTH_CH07")

    def test_cross_project_proposal_without_switch_is_blocked(self):
        out = self.route(
            "проверь это",
            proposed_project="SYNTHESIS_IVDIVO_BUSINESS",
            proposed_topic="BUSINESS_ENGINEERING",
        )
        self.assertEqual(out.status, "HOLD_CROSS_PROJECT_SWITCH_UNAUTHORIZED")
        self.assertEqual(out.active_project, self.project)
        self.assertTrue(out.drift_blocked)

    def test_missing_thread_topic_plus_continuation_requires_restore(self):
        out = route_turn(
            active_project=None,
            active_topic=None,
            user_text="и",
            proposed_project="SYNTHESIS_IVDIVO_BUSINESS",
        )
        self.assertEqual(out.status, "HOLD_RESTORE_THREAD_TOPIC_BEFORE_CONTINUE")

    def test_continuation_detector_is_narrow(self):
        self.assertTrue(is_bare_continuation("И!"))
        self.assertTrue(is_bare_continuation("continue"))
        self.assertFalse(is_bare_continuation("и теперь переключись на компанию"))
        self.assertFalse(is_bare_continuation("продолжай книгу Orbital, но проверь главу 3"))

    def test_invalid_return_token_fails_closed(self):
        out = resolve_return_token("RETURN::wrong")
        self.assertEqual(out.status, "HOLD_INVALID_RETURN_TOKEN")


if __name__ == "__main__":
    unittest.main(verbosity=2)
