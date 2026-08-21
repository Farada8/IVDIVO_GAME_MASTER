import unittest
from business_opportunity_engine_v3 import *

class T(unittest.TestCase):
    def test_signal_s0(self): self.assertEqual(LiveSignal(False,False).grade(),'S0')
    def test_signal_s1(self): self.assertEqual(LiveSignal(True,False).grade(),'S1')
    def test_signal_s2(self): self.assertEqual(LiveSignal(True,True).grade(),'S2')
    def test_signal_s3(self): self.assertEqual(LiveSignal(True,True,True).grade(),'S3')
    def test_signal_s4(self): self.assertEqual(LiveSignal(True,True,True,True).grade(),'S4')
    def test_public_ceiling(self): self.assertEqual(public_evidence_ceiling(True),'E2+')
    def test_s4_not_e3(self): self.assertEqual(market_grade_from_public_signal('S4',True),'E2+')
    def test_s2_only_e1(self): self.assertEqual(market_grade_from_public_signal('S2',True),'E1')
    def test_select_zero_cost(self):
        a=Experiment('a',0,4,True,1); b=Experiment('b',2,10,True,2)
        self.assertEqual(select_experiment([a,b],0).name,'a')
    def test_no_eligible_test(self): self.assertIsNone(select_experiment([Experiment('x',1,9)],0))
    def test_cash_gap(self): self.assertEqual(cash_gap([0,100],[50,20]),50)
    def test_cash_timeline_mismatch(self):
        with self.assertRaises(ValueError): cash_gap([1],[1,2])
    def test_zero_cash_fail(self): self.assertEqual(zero_founder_cash_gate(50,False),'FAIL_ZERO_FOUNDER_CASH')
    def test_zero_cash_bridge(self): self.assertEqual(zero_founder_cash_gate(50,True),'PASS_EXTERNAL_BRIDGE_REQUIRED')
    def test_unknown_gap(self): self.assertEqual(zero_founder_cash_gate(None,False),'HOLD_UNKNOWN')
    def test_micro_gate_fail(self): self.assertEqual(micro_market_gate('seg',None,'channel'),'KILL_OR_RESHAPE')
    def test_micro_gate_pass(self): self.assertEqual(micro_market_gate('seg','benefit','channel'),'PASS')
    def test_power_benefit_only(self): self.assertEqual(strategic_power_gate(True,False),'UNPROVEN')
    def test_power_both(self): self.assertEqual(strategic_power_gate(True,True),'POWER_CANDIDATE')
    def test_v3_fail_closed(self): self.assertEqual(v3_candidate_gate(True,False),'FAIL_CLOSED')
    def test_v3_candidate(self): self.assertEqual(v3_candidate_gate(False,False),'CANDIDATE_ONLY')
    def test_v3_promotion_review(self): self.assertEqual(v3_candidate_gate(True,True),'ELIGIBLE_FOR_PROMOTION_REVIEW')
    def test_validate_e3_block(self):
        o={'proof':{'E_grade':'E3'},'buyer_workload':{'willingness_to_pay':None},'capital_topology':{'founder_cash_eur':0},'micro_market':{'segment':'s','benefit':'b','access':'a'}}
        self.assertIn('PUBLIC_EVIDENCE_CANNOT_PROMOTE_E3',validate_opportunity(o,True))
    def test_validate_wtp_block(self):
        o={'proof':{'E_grade':'E2+'},'buyer_workload':{'willingness_to_pay':100},'capital_topology':{'founder_cash_eur':0},'micro_market':{'segment':'s','benefit':'b','access':'a'}}
        self.assertIn('WTP_MUST_BE_NULL_WITHOUT_BUYER_EVIDENCE',validate_opportunity(o,True))
    def test_validate_founder_cash(self):
        o={'proof':{'E_grade':'E1'},'buyer_workload':{'willingness_to_pay':None},'capital_topology':{'founder_cash_eur':1},'micro_market':{'segment':'s','benefit':'b','access':'a'}}
        self.assertIn('FOUNDER_CASH_CONSTRAINT_BREACH',validate_opportunity(o,True))
    def test_validate_micro(self):
        o={'proof':{'E_grade':'E1'},'buyer_workload':{'willingness_to_pay':None},'capital_topology':{'founder_cash_eur':0},'micro_market':{'segment':'s','benefit':None,'access':'a'}}
        self.assertIn('MICRO_MARKET_INCOMPLETE',validate_opportunity(o,True))
    def test_route_no_magic_score(self):
        r=route_vector({'cash':0},{'cash':0},{'cash':100})
        self.assertEqual(set(r),{'CREATE','BROKER','ACQUIRE'}); self.assertNotIn('score',r)

if __name__=='__main__': unittest.main()
