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


class RealSmithRoutingTelemetry(unittest.TestCase):
    def setUp(self):
        self.guard = load_guard()
        self.aggregate = json.loads((ROOT / 'CURRENT_IVDIVO_SYSTEM_STATE.json').read_text(encoding='utf-8'))
        self.project = json.loads((ROOT / 'PROJECT_STATES' / 'IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json').read_text(encoding='utf-8'))

    def test_real_guard_fails_closed_if_aggregate_lags_project(self):
        result = self.guard.guard_resume(self.aggregate, self.project)
        self.assertEqual(result['decision'], 'STOP_REBASE_REQUIRED', result)
        self.assertEqual(result['project_id'], 'IVDIVO_BOOK_3_SMITH_FULL_NOVEL')
        self.assertEqual(result['project_next'], 'DRAFT_CH25_CASCADE_FROM_ACTUAL_CH24_PASS_AND_FRESH_P65_P72_REBASE')

    def test_project_specific_frontier_is_authorized_ch25(self):
        self.assertEqual(self.project['status'], 'ACTIVE_WORKING_PROSE_CH24_PASS_CH25_AUTHORIZED')
        self.assertTrue(self.project['manuscript_frontier']['ch25_authorized'])
        self.assertEqual(self.project['manuscript_frontier']['latest_passed'], 'CH24_GO_TO_THE_RELAY')

    def test_aggregate_selects_smith_but_next_action_lags(self):
        active = self.aggregate['portfolio_frontier']['active_project']
        self.assertEqual(active['project_id'], 'IVDIVO_BOOK_3_SMITH_FULL_NOVEL')
        self.assertNotEqual(active['next_unblocked_obligation'], self.project['next_obligation'])


if __name__ == '__main__':
    unittest.main()
