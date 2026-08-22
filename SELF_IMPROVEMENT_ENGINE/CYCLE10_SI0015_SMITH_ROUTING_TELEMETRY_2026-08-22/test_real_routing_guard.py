import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOCKED_NEXT = 'ASSEMBLE_LOCKED_CH01_CH29_MANUSCRIPT_FROM_CURRENT_AUTHORITY_FILES_THEN_RUN_FINAL_COPY_FORMAT_EXPORT_GATE'


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

    def test_current_guard_executes_only_locked_manuscript_frontier(self):
        result = self.guard.guard_resume(self.aggregate, self.project)
        self.assertEqual(result['decision'], 'EXECUTE', result)
        self.assertEqual(result['project_id'], 'IVDIVO_BOOK_3_SMITH')
        self.assertEqual(result['selected_next_action'], LOCKED_NEXT)
        self.assertNotIn('DRAFT', result['selected_next_action'])
        self.assertNotIn('CH30', result['selected_next_action'])

    def test_current_project_is_founder_locked_not_ch25_authorized(self):
        self.assertEqual(self.project['status'], 'FOUNDER_LOCKED_CH01_CH29_MANUSCRIPT_AUTHORITY')
        self.assertTrue(self.project['story_lock'])
        self.assertTrue(self.project['founder_lock'])
        self.assertFalse(self.project['manuscript_frontier']['prose_expansion_authorized'])
        self.assertFalse(self.project['manuscript_frontier']['ch30_authorized'])

    def test_current_aggregate_identity_and_frontier_match_project(self):
        active = self.aggregate['portfolio_frontier']['active_project']
        self.assertEqual(active['project_id'], self.project['project_id'])
        self.assertEqual(active['next_unblocked_obligation'], self.project['next_obligation'])
        self.assertEqual(active['mode'], 'FOUNDER_LOCKED_MANUSCRIPT_ASSEMBLY_COPY_FORMAT_EXPORT')
        self.assertEqual(active['founder_lock'], 'ISSUED')

    def test_historical_identity_and_frontier_defect_still_fails_closed(self):
        historical_project = {
            'project_id': 'IVDIVO_BOOK_3_SMITH',
            'next_obligation': 'DRAFT_CH25_CASCADE_FROM_ACTUAL_CH24_PASS_AND_FRESH_P65_P72_REBASE',
        }
        historical_aggregate = {
            'portfolio_frontier': {
                'active_project': {
                    'project_id': 'IVDIVO_BOOK_3_SMITH_FULL_NOVEL',
                    'next_unblocked_obligation': 'FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE',
                }
            }
        }
        mismatch = self.guard.guard_resume(historical_aggregate, historical_project)
        self.assertEqual(mismatch['decision'], 'PROJECT_NOT_ACTIVE', mismatch)

        aligned = copy.deepcopy(historical_aggregate)
        aligned['portfolio_frontier']['active_project']['project_id'] = historical_project['project_id']
        stale_frontier = self.guard.guard_resume(aligned, historical_project)
        self.assertEqual(stale_frontier['decision'], 'STOP_REBASE_REQUIRED', stale_frontier)
        self.assertNotEqual(stale_frontier['aggregate_next'], stale_frontier['project_next'])


if __name__ == '__main__':
    unittest.main()
