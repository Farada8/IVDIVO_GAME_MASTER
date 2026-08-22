import unittest, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from engine.cycle5_business_engine import *

class TestCycle5(unittest.TestCase):
    def test_age(self):
        self.assertEqual(expiry_state('2026-08-01T00:00:00+00:00','2026-08-10T00:00:00+00:00',10),'FRESH')
        self.assertEqual(expiry_state(None,'2026-08-10T00:00:00+00:00',10),'UNKNOWN')
    def test_url(self):
        self.assertEqual(canonical_url('HTTPS://Example.COM/a/?utm_source=x&b=2'),'https://example.com/a?b=2')
    def test_notice(self):
        self.assertEqual(verify_notice_state('OPEN_TENDER_SUBMISSION','2026-09-01T00:00:00+00:00','2026-08-22T00:00:00+00:00')['status'],'OPEN_TENDER_SUBMISSION')
        self.assertEqual(verify_notice_state('OPEN_TENDER_SUBMISSION','2026-08-01T00:00:00+00:00','2026-08-22T00:00:00+00:00')['status'],'STALE_OPEN_CONTRADICTION')
    def test_budget(self): self.assertEqual(budget_buyer_guard(100000,False)['status'],'BUDGET_NOT_BUYER_PROOF')
    def test_access(self): self.assertEqual(access_path_guard('official',True,False)['status'],'PUBLIC_ACCESS_PATH_ONLY')
    def test_market_state(self):
        self.assertEqual(market_state(nonconsumer=True),'NONCONSUMPTION')
        self.assertEqual(market_state(nonconsumer=True,overshot=True),'CONFLICT')
    def test_falsifier(self): self.assertEqual(why_now_falsifier('rule','rule withdrawn'),'FALSIFIABLE_WHY_NOW')
    def test_assumption(self): self.assertAlmostEqual(fatal_assumption_score(.5,.8,.9),.36)
    def test_artifact(self): self.assertEqual(artifact_gate(3,'2026-08-22',True,True,True),'PASS_PUBLIC_ARTIFACT')
    def test_human_time(self): self.assertIsNone(human_delivery_time(0.1,'MODEL')['human_minutes'])
    def test_interview(self):
        self.assertEqual(anti_fluff_question('Would you pay?',hypothetical=True),'REJECT_LEADING_OR_HYPOTHETICAL')
        self.assertEqual(anti_fluff_question('What happened last time?',asks_past_behavior=True),'KEEP_BEHAVIOR_EVIDENCE')
    def test_e3(self):
        self.assertEqual(e3_capture('quote','owner','spreadsheet','missed deadline')['status'],'E3_CONVERSATION_EVIDENCE')
        self.assertEqual(e3_capture('x','x','x','x',True)['status'],'NOT_E3')
    def test_e4(self):
        self.assertEqual(e4_payment_proof('PAID_PILOT',100,'2026-08-22','inv1')['status'],'E4_TRANSACTION_EVIDENCE')
        self.assertEqual(e4_payment_proof('PROMISE',100,'2026-08-22','x')['status'],'NOT_E4')
    def test_price(self): self.assertIsNone(pricing_schema(None,[50,100])['price'])
    def test_cash(self):
        r=cash_timeline(100,[{'date':'2026-01-01','amount':-150},{'date':'2026-01-02','amount':200}])
        self.assertEqual(r['min_cash'],-50)
    def test_bridge(self): self.assertEqual(reimbursement_bridge('UPFRONT_COST','POST_WORK_REIMBURSEMENT'),'BRIDGE_REQUIRED')
    def test_funding(self):
        self.assertEqual(funding_topology(),['UNKNOWN'])
        self.assertIn('CUSTOMER_FUNDED', funding_topology(customer_prepay=True))
    def test_margin(self):
        self.assertIsNone(contribution_margin(None,10)['contribution_margin'])
        self.assertEqual(contribution_margin(100,30,20,10)['contribution_margin'],40)
    def test_queue(self):
        self.assertEqual(queue_state(9,10)['status'],'HIGH_UTILIZATION')
        self.assertEqual(queue_state(10,10)['status'],'OVERLOAD')

if __name__=='__main__': unittest.main()
