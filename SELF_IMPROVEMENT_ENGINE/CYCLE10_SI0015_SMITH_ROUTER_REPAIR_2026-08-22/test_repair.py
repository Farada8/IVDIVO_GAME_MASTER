import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIR = Path(__file__).resolve().parent


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def flatten(x, p=''):
    out = {}
    if isinstance(x, dict):
        for k, v in x.items():
            out.update(flatten(v, f'{p}.{k}' if p else k))
    elif isinstance(x, list):
        out[p] = x
    else:
        out[p] = x
    return out


def historical_stale_system(current: dict) -> dict:
    out = copy.deepcopy(current)
    out['portfolio_frontier']['active_project'] = {
        'project_id': 'IVDIVO_BOOK_3_SMITH_FULL_NOVEL',
        'title': 'SMITH',
        'mode': 'FRESH_AUTHORITY_AND_CONTINUITY_RECONCILIATION_BEFORE_PROSE',
        'project_state_path': None,
        'source_transition_from': 'PROJECTS/THE_WIFE_AT_HIS_WEDDING/CURRENT_STATE.md',
        'next_unblocked_obligation': 'FRESH_AUTHORITY_RECONCILIATION_THEN_PREVIOUS_BOOK_CONSEQUENCE_CONTINUITY_CHECK_THEN_STORY_CORE_THEN_HUMAN_SCENE_DIALOGUE_CALIBRATION_THEN_CAUSAL_ARCHITECTURE_THEN_PRE_PROSE_STORY_GATE',
        'authority_boundary': 'NO_SMITH_PROSE_UNTIL_FRESH_AUTHORITY_AND_PRE_PROSE_STORY_GATE',
        'do_not_repeat': [],
    }
    return out


class SmithRouterRepair(unittest.TestCase):
    def setUp(self):
        self.repair = load_module(DIR / 'apply_repair.py', 'smith_router_repair')
        self.guard = load_module(ROOT / 'tools' / 'ivdivo_preexecution_resume_guard.py', 'resume_guard')
        self.system = json.loads((ROOT / 'CURRENT_IVDIVO_SYSTEM_STATE.json').read_text(encoding='utf-8'))
        self.portfolio = json.loads((ROOT / 'CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json').read_text(encoding='utf-8'))
        self.project = json.loads((ROOT / 'PROJECT_STATES' / 'IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json').read_text(encoding='utf-8'))

    def test_historical_pre_repair_fixture_fails_closed(self):
        historical = historical_stale_system(self.system)
        self.assertEqual(self.guard.guard_resume(historical, self.project)['decision'], 'PROJECT_NOT_ACTIVE')
        historical['portfolio_frontier']['active_project']['project_id'] = self.project['project_id']
        self.assertEqual(self.guard.guard_resume(historical, self.project)['decision'], 'STOP_REBASE_REQUIRED')

    def test_current_router_executes_exact_project_frontier(self):
        result = self.guard.guard_resume(self.system, self.project)
        self.assertEqual(result['decision'], 'EXECUTE', result)
        self.assertEqual(result['project_id'], self.project['project_id'])
        self.assertEqual(result['selected_next_action'], self.project['next_obligation'])

    def test_repair_is_idempotent_on_current_router(self):
        patched = self.repair.patch_system(self.system, self.project)
        result = self.guard.guard_resume(patched, self.project)
        self.assertEqual(result['decision'], 'EXECUTE', result)
        self.assertEqual(patched['portfolio_frontier']['active_project'], self.system['portfolio_frontier']['active_project'])

    def test_system_patch_is_bounded(self):
        after = self.repair.patch_system(self.system, self.project)
        b, a = flatten(self.system), flatten(after)
        changed = {k for k in set(b) | set(a) if b.get(k) != a.get(k)}
        allowed = ('portfolio_frontier.active_project', 'recent_verified_main_integration', 'state_status')
        self.assertTrue(all(any(k == x or k.startswith(x + '.') for x in allowed) for k in changed), changed)
        self.assertEqual(after['portfolio_frontier']['active_project']['project_state_path'], 'PROJECT_STATES/IVDIVO_BOOK_3_SMITH_CURRENT_STATE.json')

    def test_portfolio_patch_is_bounded(self):
        after = self.repair.patch_portfolio(self.portfolio, self.project)
        b, a = flatten(self.portfolio), flatten(after)
        changed = {k for k in set(b) | set(a) if b.get(k) != a.get(k)}
        allowed = ('purpose', 'active_project', 'queue_after_d01_founder_lock', 'state_status')
        self.assertTrue(all(any(k == x or k.startswith(x + '.') for x in allowed) for k in changed), changed)

    def test_d01_d09_d10_authority_surfaces_unchanged(self):
        s = self.repair.patch_system(self.system, self.project)
        p = self.repair.patch_portfolio(self.portfolio, self.project)
        self.assertEqual(s['portfolio_frontier']['text_locked_or_text_complete'], self.system['portfolio_frontier']['text_locked_or_text_complete'])
        self.assertEqual(s['portfolio_frontier']['pending_founder_decision_gates'], self.system['portfolio_frontier']['pending_founder_decision_gates'])
        self.assertEqual(p['d01_founder_lock'], self.portfolio['d01_founder_lock'])
        self.assertEqual(p['d10_founder_lock'], self.portfolio['d10_founder_lock'])
        self.assertEqual(p['parallel_founder_decision_gates'], self.portfolio['parallel_founder_decision_gates'])


if __name__ == '__main__':
    unittest.main()
