import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engine.evidence_economics_guards import *

class TestAdditiveGuards(unittest.TestCase):
    def test_expiry(self):
        self.assertEqual(expiry_state('2026-08-01T00:00:00+00:00','2026-08-10T00:00:00+00:00',10),'FRESH')
        self.assertEqual(expiry_state(None,'2026-08-10T00:00:00+00:00',10),'UNKNOWN')
    def test_canonical(self): self.assertEqual(canonical_url('HTTPS://Example.COM/a/?utm_source=x&b=2'),'https://example.com/a?b=2')
    def test_correlation(self): self.assertEqual(correlation_key('OPW',' A  B ','https://x.ie/a?utm_source=z'),('opw','a b','https://x.ie/a'))
    def test_notice(self):
        self.assertEqual(notice_state('OPEN_TENDER_SUBMISSION','2026-08-01T00:00:00+00:00','2026-08-22T00:00:00+00:00'),'STALE_OPEN_CONTRADICTION')
    def test_supersession(self): self.assertEqual(supersession_status('v1','v2'),'SUPERSEDED')
    def test_budget(self): self.assertEqual(budget_buyer_boundary(100000,False),'BUDGET_NOT_BUYER_PROOF')
    def test_access(self): self.assertEqual(access_intent_boundary('portal',True,False),'PUBLIC_ACCESS_PATH_ONLY')
    def test_consumption(self):
        self.assertEqual(market_consumption_state(nonconsumer=True),'NONCONSUMPTION')
        self.assertEqual(market_consumption_state(nonconsumer=True,overshot=True),'CONFLICT')
    def test_motivation_ability(self): self.assertEqual(motivation_ability_delta(True,None)['status'],'HOLD_UNKNOWN')
    def test_incumbent(self): self.assertEqual(incumbent_asymmetry(True,None),'PRESSURE_NOT_INCUMBENT_WEAKNESS_PROOF')
    def test_falsifier(self): self.assertEqual(why_now_falsifier('law','law withdrawn'),'FALSIFIABLE_WHY_NOW')
    def test_assumption(self): self.assertAlmostEqual(fatal_assumption_priority(.5,.8,.9),.36)
    def test_shared(self):
        r=shared_assumption_update(['OP03','OP01','OP03'],'E1')
        self.assertEqual(r['affected_opportunities'],['OP01','OP03']); self.assertTrue(r['count_once'])
    def test_human_time(self): self.assertEqual(human_delivery_time(.1,'MODEL')['status'],'HOLD_NO_HUMAN_TIMING')
    def test_antifluff(self): self.assertEqual(anti_fluff_question(hypothetical=True),'REJECT_LEADING_OR_HYPOTHETICAL')
    def test_e3(self):
        self.assertEqual(e3_capture('q','owner','sheet','missed bid'),'E3_CONVERSATION_EVIDENCE')
        self.assertEqual(e3_capture('q','owner','sheet','missed bid',True),'NOT_E3')
    def test_e4(self):
        self.assertEqual(e4_payment_proof('PAID_PILOT',100,'2026-08-22','inv-1'),'E4_TRANSACTION_EVIDENCE')
        self.assertEqual(e4_payment_proof('PROMISE',100,'2026-08-22','x'),'NOT_E4')
    def test_price(self): self.assertIsNone(pricing_state(None,[50,100])['price'])
    def test_cash(self): self.assertEqual(cash_timeline(100,[{'date':'2026-01-01','amount':-150},{'date':'2026-01-02','amount':200}])['min_cash'],-50)
    def test_bridge(self): self.assertEqual(reimbursement_bridge('UPFRONT_COST','POST_WORK_REIMBURSEMENT'),'BRIDGE_REQUIRED')
    def test_funding(self): self.assertEqual(funding_topology(),['UNKNOWN'])
    def test_margin(self):
        self.assertEqual(contribution_margin(None,10,2,1)['status'],'HOLD_NO_REVENUE_EVIDENCE')
        self.assertEqual(contribution_margin(100,30,20,10)['value'],40)
    def test_capacity(self):
        self.assertEqual(capacity_state(9,10)['status'],'HIGH_UTILIZATION')
        self.assertEqual(capacity_state(10,10)['status'],'OVERLOAD')

if __name__=='__main__': unittest.main()
