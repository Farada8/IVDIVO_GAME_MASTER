import copy, json, unittest
from pathlib import Path
from SELF_IMPROVEMENT_ENGINE.CYCLE10_SI0015_D01_ROUTER_REPAIR_2026_08_22.apply_repair import patch_system, patch_portfolio

ROOT=Path(__file__).resolve().parents[2]


def flatten(x,p=''):
    out={}
    if isinstance(x,dict):
        for k,v in x.items(): out.update(flatten(v,f'{p}.{k}' if p else k))
    elif isinstance(x,list):
        out[p]=x
    else: out[p]=x
    return out

class Repair(unittest.TestCase):
    def test_system_patch_is_bounded_and_removes_d01_stale_resume(self):
        src=json.loads((ROOT/'CURRENT_IVDIVO_SYSTEM_STATE.json').read_text())
        before=copy.deepcopy(src); after=patch_system(src)
        self.assertEqual(after['portfolio_frontier']['active_project']['project_id'],'IVDIVO_BOOK_3_SMITH_FULL_NOVEL')
        self.assertIn('D01_THE_WIFE_AT_HIS_WEDDING_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED',after['portfolio_frontier']['text_locked_or_text_complete'])
        self.assertNotIn('D01_ACTIVE_E96',after['state_status'])
        b,a=flatten(before),flatten(after)
        changed={k for k in set(b)|set(a) if b.get(k)!=a.get(k)}
        allowed=(
          'portfolio_frontier.active_project',
          'portfolio_frontier.text_locked_or_text_complete',
          'recent_verified_main_integration',
          'state_status',
        )
        self.assertTrue(all(any(k==x or k.startswith(x+'.') for x in allowed) for k in changed),changed)

    def test_portfolio_patch_is_bounded_and_records_d01_lock(self):
        src=json.loads((ROOT/'CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json').read_text())
        before=copy.deepcopy(src); after=patch_portfolio(src)
        self.assertEqual(after['d01_founder_lock']['status'],'FOUNDER_LOCKED')
        self.assertEqual(after['active_project']['project_id'],'IVDIVO_BOOK_3_SMITH_FULL_NOVEL')
        self.assertIn('D01_THE_WIFE_AT_HIS_WEDDING_FOUNDER_LOCKED_E01_E120_RECORDING_AUTHORITY_ISSUED',after['text_complete_or_locked'])
        b,a=flatten(before),flatten(after)
        changed={k for k in set(b)|set(a) if b.get(k)!=a.get(k)}
        allowed=('purpose','text_complete_or_locked','d01_founder_lock','active_project','queue_after_d01_founder_lock','state_status')
        self.assertTrue(all(any(k==x or k.startswith(x+'.') for x in allowed) for k in changed),changed)

if __name__=='__main__': unittest.main()
