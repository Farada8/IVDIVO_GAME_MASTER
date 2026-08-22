import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def load_guard():
    p = ROOT / 'tools' / 'ivdivo_preexecution_resume_guard.py'
    spec = importlib.util.spec_from_file_location('ivdivo_preexecution_resume_guard', p)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def historical_stale_aggregate(current: dict) -> dict:
    out = copy.deepcopy(current)
    active = out['portfolio_frontier']['active_project']
    active['project_id'] = 'IVDIVO_BOOK_3_SMITH_FULL_NOVEL'
    active['mode'] = 'FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE'
    active['project_state_path'] = None
    active['next_unblocked_obligation'] = 'FRESH_AUTHORITY_RECONCILIATION_THEN_PREVIOUS_BOOK_CONSEQUENCE_CONTINUITY_CHECK_THEN_STORY_CORE_THEN_HUMAN_SCENE_DIALOGUE_CALIBRATION_THEN_CAUSAL_ARCHITECTURE_THEN_PRE_PROSE_STORY_GATE'
    return out


class RealSmithRoutingTelemetry(unittest.TestCase):
    def setUp(self):
        self.guard = load_guard()
        self.aggregate = json.loads((ROOT / 'CURRENT_IVDIVO_SYSTEM_STATE.json').read_text(encoding='utf-8'))
        self.project = json.loads((ROOT / 'PROJECT_STATES' / 'IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json').read_text(encoding='utf-8'))

    def test_historical_project_id_mismatch_remains_a_fail_closed_fixture(self):
        historical = historical_stale_aggregate(self.aggregate)
        result = self.guard.guard_resume(historical, self.project)
        self.assertEqual(result['decision'], 'PROJECT_NOT_ACTIVE', result)

    def test_historical_stale_next_action_after_id_alignment(self):
        historical = historical_stale_aggregate(self.aggregate)
        historical['portfolio_frontier']['active_project']['project_id'] = self.project['project_id']
        result = self.guard.guard_resume(historical, self.project)
        self.assertEqual(result['decision'], 'STOP_REBASE_REQUIRED', result)
        self.assertEqual(result['project_next'], self.project['next_obligation'])

    def test_current_router_executes_current_project_frontier(self):
        result = self.guard.guard_resume(self.aggregate, self.project)
        self.assertEqual(result['decision'], 'EXECUTE', result)
        self.assertEqual(result['selected_next_action'], self.project['next_obligation'])
        active = self.aggregate['portfolio_frontier']['active_project']
        self.assertEqual(active['project_id'], self.project['project_id'])
        self.assertEqual(active['next_unblocked_obligation'], self.project['next_obligation'])
        self.assertEqual(active['project_state_path'], 'PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json')

    def test_project_specific_frontier_is_authorized(self):
        self.assertTrue(self.project['manuscript_frontier']['ch25_authorized'])
        self.assertEqual(self.project['manuscript_frontier']['latest_passed'], 'CH24_GO_TO_THE_RELAY')


if __name__ == '__main__':
    unittest.main()
