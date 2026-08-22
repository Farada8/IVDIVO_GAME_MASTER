import unittest
from engine.business_engine_integration_v1 import *

class IntegrationTests(unittest.TestCase):
    def test_signal_primary(self):
        self.assertEqual(signal_state(PublicSignal('s','u',True,'p','e','a','IE')),'CURRENT_PRIMARY_SIGNAL')
    def test_signal_discovery(self):
        self.assertEqual(signal_state(PublicSignal('s','u',False,None,None,None,'IE')),'DISCOVERY_ONLY')
    def test_signal_superseded(self):
        self.assertEqual(signal_state(PublicSignal('s','u',True,None,None,None,'IE',True)),'SUPERSEDED_ZERO_CURRENT_WEIGHT')
    def test_date_triad(self):
        self.assertEqual(date_triad(PublicSignal('s','u',True,'p','e','a','IE')),('p','e','a'))
    def test_public_cap(self):
        self.assertEqual(cap_market_proof('E7'),'E2_PLUS')
    def test_proof_firewall(self):
        self.assertEqual(proof_plane_firewall(knowledge_level='K5',signal_level='S4',requested_market_level='E4'),'E2_PLUS')
    def test_real_events(self):
        self.assertEqual(cap_market_proof('E7',buyer_event=True),'E3'); self.assertEqual(cap_market_proof('E7',payment_event=True),'E4')
    def test_no_outreach(self):
        with self.assertRaises(IntegrationGateError): action_gate('SEND_EMAIL')
    def test_creative_discovery(self):
        self.assertEqual(creative_state(CreativeOpportunity('o',None,False,None,None,55000,None)),'DISCOVERY_ONLY')
    def test_creative_eligibility_hold(self):
        self.assertEqual(creative_state(CreativeOpportunity('o','u',True,None,'d',55000,None)),'HOLD_ELIGIBILITY_UNKNOWN')
    def test_budget_not_income(self):
        self.assertFalse(project_budget_is_artist_income(CreativeOpportunity('o','u',True,True,'d',55000,None)))
    def test_opportunity_fatal_assumption(self):
        with self.assertRaises(IntegrationGateError): opportunity_gate(OpportunityObject('o','buyer','work',None))
    def test_economics_null(self):
        self.assertIsNone(observed_economics(OpportunityObject('o','b','w','f')))
    def test_economics_observed(self):
        self.assertEqual(observed_economics(OpportunityObject('o','b','w','f',price_eur=1000,delivery_cost_eur=300,delivery_minutes=600))['contribution_eur'],700)
    def test_finance_after_e4(self):
        self.assertEqual(finance_gate('E2_PLUS','loan'),'HOLD_DEMAND_PROOF_REQUIRED'); self.assertEqual(finance_gate('E4','loan'),'READY_TO_ASSESS_LOAN')
    def test_lineage(self):
        with self.assertRaises(IntegrationGateError): lineage_gate(DecisionLineage((),'i','h','d','e'))
    def test_selective_invalidation(self):
        out=selective_invalidation({'signal':['opp'],'opp':['test'],'other':['x']},['signal']); self.assertEqual(out['dirty'],('opp','signal','test')); self.assertNotIn('x',out['dirty'])
    def test_locked_invalidation(self):
        self.assertEqual(selective_invalidation({'s':['locked']},['s'],['locked'])['blocked_locked'],('locked',))
    def test_reuse(self):
        self.assertEqual(shared_mechanism_disposition(semantic_duplicate=True,current_sufficient=True,new_decision_delta=True),'REUSE_CURRENT')
    def test_noop(self):
        self.assertEqual(shared_mechanism_disposition(semantic_duplicate=False,current_sufficient=False,new_decision_delta=False),'NO_OP')
    def test_si_promotion(self):
        self.assertEqual(self_improvement_gate(observed_defect=True,regression_pass=True,provenance_bound=True,readback_pass=True),'READY_FOR_BOUNDED_PROMOTION')
    def test_si_protect(self):
        self.assertEqual(self_improvement_gate(observed_defect=False,regression_pass=False,provenance_bound=False,readback_pass=False),'PROTECT_NO_CHANGE')
    def test_founder_lock(self):
        with self.assertRaises(IntegrationGateError): protected_project_gate('FOUNDER_LOCKED','BUSINESS_MODEL_REWRITE')
        self.assertTrue(protected_project_gate('FOUNDER_LOCKED','EVIDENCE_ONLY'))
    def test_cross_store(self):
        self.assertEqual(cross_store_identity('a','a',10,10),'BINARY_EXTERNAL_PARITY'); self.assertEqual(cross_store_identity('a','b',10,10),'IDENTITY_MISMATCH')
    def test_profiles(self):
        self.assertIn('BUYER_BEFORE_BUILD',business_profile('ZERO_CAPITAL')); self.assertIn('BUDGET_NEQ_INCOME',business_profile('CREATIVE_OPPORTUNITY')); self.assertIn('CASH_CONVERSION',business_profile('CONSTRUCTION'))

if __name__=='__main__': unittest.main()
