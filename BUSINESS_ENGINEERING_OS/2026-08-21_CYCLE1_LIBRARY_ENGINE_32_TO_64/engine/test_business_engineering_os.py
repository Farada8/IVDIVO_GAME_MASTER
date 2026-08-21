import unittest
from business_engineering_os import Opportunity, route, clamp_evidence

class EngineTests(unittest.TestCase):
    def test_public_evidence_ceiling(self): self.assertEqual(clamp_evidence(Opportunity('x',evidence_level='E6')),'E2+')
    def test_buyer_interaction_ceiling(self): self.assertEqual(clamp_evidence(Opportunity('x',evidence_level='E6',external_buyer_interaction=True)),'E3')
    def test_payment_promotes_to_at_least_e4(self): self.assertEqual(clamp_evidence(Opportunity('x',payment_proof=True)),'E4')
    def test_micro_market_fails_without_benefit(self): self.assertEqual(route(Opportunity('x',target_segment='SME',differentiated=True))['micro_market'],'KILL_OR_RESHAPE')
    def test_micro_market_pass(self): self.assertEqual(route(Opportunity('x',target_segment='SME',clear_benefit=True,differentiated=True))['micro_market'],'PASS')
    def test_zero_cash_fail(self): self.assertEqual(route(Opportunity('x',founder_cash_required=100))['zero_cash'],'FAIL_ZERO_CASH')
    def test_customer_funded_mutation(self): self.assertEqual(route(Opportunity('x',founder_cash_required=100,customer_funding_available=True))['zero_cash'],'MUTATE_TO_CUSTOMER_FUNDED')
    def test_no_premature_scale(self): self.assertEqual(route(Opportunity('x',evidence_level='E2+'))['scale'],'BLOCK_PREMATURE_SCALE')
    def test_unknown_economics_stays_unknown(self): self.assertEqual(route(Opportunity('x',economics={'price':149}))['economics'],'UNKNOWN_KEEP_NULL')
    def test_measured_economics(self): self.assertEqual(route(Opportunity('x',economics={'price':149,'gross_margin':0.7,'conversion':0.1,'cash_cycle_days':-5}))['economics'],'MEASURED')
    def test_constraint_required(self): self.assertEqual(route(Opportunity('x'))['constraint'],'IDENTIFY_CONSTRAINT_FIRST')
    def test_three_entry_modes(self): self.assertEqual(route(Opportunity('x'))['entry_modes'],['CREATE','BROKER','ACQUIRE'])

if __name__=='__main__': unittest.main()
