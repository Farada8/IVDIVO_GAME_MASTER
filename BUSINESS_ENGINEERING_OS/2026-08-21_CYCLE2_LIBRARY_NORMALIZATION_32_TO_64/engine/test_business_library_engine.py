import unittest
from business_library_engine import *

class TestEngine(unittest.TestCase):
    def test_01_broken_zero(self): self.assertEqual(source_weight(Source("BROKEN")),0)
    def test_02_valid_one(self): self.assertEqual(source_weight(Source("VALID")),1)
    def test_03_micro_no_benefit(self): self.assertEqual(micro_market_gate(Opportunity(False,True,True)),"KILL_OR_RESHAPE")
    def test_04_micro_no_diff(self): self.assertEqual(micro_market_gate(Opportunity(True,False,True)),"KILL_OR_RESHAPE")
    def test_05_micro_pass(self): self.assertEqual(micro_market_gate(Opportunity(True,True,True)),"PASS")
    def test_06_why_now(self): self.assertEqual(why_now_gate(Opportunity(True,True,False)),"HOLD")
    def test_07_public_ceiling(self): self.assertEqual(market_proof_ceiling(True,"E4"),"E2+")
    def test_08_public_keeps_e2(self): self.assertEqual(market_proof_ceiling(True,"E2"),"E2")
    def test_09_cash_unknown(self): self.assertEqual(zero_founder_cash_gate(Opportunity(True,True,True)),"UNKNOWN")
    def test_10_cash_fail(self): self.assertEqual(zero_founder_cash_gate(Opportunity(True,True,True,founder_cash_gap=100)),"FAIL_ZERO_CASH")
    def test_11_customer_funding(self): self.assertEqual(zero_founder_cash_gate(Opportunity(True,True,True,founder_cash_gap=100,customer_funded=True)),"PASS_WITH_CUSTOMER_FUNDING")
    def test_12_constraint_hold(self): self.assertEqual(constraint_gate(Opportunity(True,True,True)),"HOLD_IDENTIFY_CONSTRAINT")
    def test_13_constraint_pass(self): self.assertEqual(constraint_gate(Opportunity(True,True,True,current_constraint="demand")),"PASS")
    def test_14_power_needs_barrier(self): self.assertEqual(power_gate(Power(True,False)),"NO_DURABLE_POWER_PROVEN")
    def test_15_power_both(self): self.assertEqual(power_gate(Power(True,True)),"POWER_POSSIBLE")
    def test_16_three_routes(self): self.assertEqual(create_broker_acquire_routes(),("CREATE","BROKER_ORCHESTRATE","ACQUIRE"))
    def test_17_sde_required(self): self.assertEqual(acquisition_target_metric(None),"SDE_CASHFLOW_REQUIRED")
    def test_18_scale_block(self): self.assertEqual(premature_scale("E2+"),"BLOCK")

if __name__=="__main__": unittest.main()
