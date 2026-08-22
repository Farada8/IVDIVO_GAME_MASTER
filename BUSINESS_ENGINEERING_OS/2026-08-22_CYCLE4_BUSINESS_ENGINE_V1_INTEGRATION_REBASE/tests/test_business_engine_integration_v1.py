import unittest
from engine.business_engine_integration_v1 import (
    BusinessIntegrationError, SharedDependencyPassport, validate_dependency_passport,
    proof_transition, DependencyEdge, build_dependency_index, selective_invalidation,
    FounderLock, founder_lock_gate, DecisionLineage, lineage_gate, BusinessTransition,
    transition_completeness, finance_after_proof, economics_gate, mechanism_disposition,
    self_improvement_promotion, compose_profile,
)


class BusinessEngineIntegrationTests(unittest.TestCase):
    def test_dependency_passport(self):
        p=SharedDependencyPassport('book-engine','0.7','a'*64,213941,'drive',('selective_invalidation',),('story_semantics',))
        self.assertTrue(validate_dependency_passport(p))

    def test_dependency_passport_fail(self):
        with self.assertRaises(BusinessIntegrationError):
            validate_dependency_passport(SharedDependencyPassport('x','1','bad',1,'d',('a',)))

    def test_public_proof_ceiling(self):
        self.assertEqual(proof_transition('E1','E7'), 'E2_PLUS')

    def test_real_buyer_payment_events(self):
        self.assertEqual(proof_transition('E2','E7',real_buyer_event=True), 'E3')
        self.assertEqual(proof_transition('E2','E7',real_payment_event=True), 'E4')

    def test_dependency_index(self):
        idx=build_dependency_index([DependencyEdge('signal','opp','DERIVES_FROM'),DependencyEdge('opp','experiment','REQUIRES')])
        self.assertEqual(idx['signal'],('opp',))

    def test_invalid_edge(self):
        with self.assertRaises(BusinessIntegrationError):
            build_dependency_index([DependencyEdge('a','b','MAGIC')])

    def test_selective_invalidation(self):
        idx={'signal':('opp',),'opp':('experiment',),'unrelated':('x',)}
        out=selective_invalidation(idx,['signal'])
        self.assertEqual(out['dirty'],('experiment','opp','signal'))
        self.assertNotIn('x',out['dirty'])

    def test_locked_dependency(self):
        out=selective_invalidation({'signal':('locked_offer',)},['signal'],['locked_offer'])
        self.assertEqual(out['blocked_locked'],('locked_offer',))

    def test_founder_lock(self):
        lock=FounderLock('offer','FOUNDER_LOCKED','approved offer')
        with self.assertRaises(BusinessIntegrationError): founder_lock_gate(lock,'OFFER_REWRITE')
        self.assertTrue(founder_lock_gate(lock,'EVIDENCE_ONLY'))

    def test_lineage(self):
        d=DecisionLineage('d',('ev1',),'interp','alternative','KEEP','lower uncertainty')
        self.assertTrue(lineage_gate(d))

    def test_lineage_fail(self):
        with self.assertRaises(BusinessIntegrationError):
            lineage_gate(DecisionLineage('d',(),'i','h','d','e'))

    def test_transition_no_holes(self):
        t=BusinessTransition('s','o','e',None,None,None,None,None,None)
        self.assertEqual(transition_completeness(t),())

    def test_transition_hole(self):
        t=BusinessTransition('s','o',None,'offer',None,None,None,None,None)
        self.assertEqual(transition_completeness(t),('OFFER',))

    def test_finance_after_proof(self):
        self.assertEqual(finance_after_proof('E2_PLUS','loan'),'HOLD_DEMAND_PROOF_REQUIRED')
        self.assertEqual(finance_after_proof('E4','invoice_finance'),'READY_TO_ASSESS_INVOICE_FINANCE')

    def test_economics_null(self):
        self.assertIsNone(economics_gate(revenue_eur=None,direct_cost_eur=10,delivery_minutes=30))

    def test_economics_observed(self):
        out=economics_gate(revenue_eur=1000,direct_cost_eur=250,delivery_minutes=600)
        self.assertEqual(out['contribution_eur'],750)

    def test_mechanism_dispositions(self):
        self.assertEqual(mechanism_disposition(semantic_duplicate=True,current_sufficient=True,decision_delta=True),'REUSE_CURRENT')
        self.assertEqual(mechanism_disposition(semantic_duplicate=False,current_sufficient=False,decision_delta=False),'NO_OP')

    def test_self_improvement(self):
        self.assertEqual(self_improvement_promotion(observed_defect=False,regression_pass=False,provenance_bound=False,readback_pass=False),'PROTECT_NO_CHANGE')
        self.assertEqual(self_improvement_promotion(observed_defect=True,regression_pass=True,provenance_bound=True,readback_pass=True),'READY_FOR_BOUNDED_PROMOTION')

    def test_profiles(self):
        self.assertIn('PROJECT_BUDGET_NEQ_INCOME',compose_profile('CREATIVE_OPPORTUNITY'))
        self.assertIn('CASH_CONVERSION',compose_profile('CONSTRUCTION'))
        self.assertIn('DOWNSIDE_FIRST',compose_profile('ACQUISITION'))

    def test_unknown_profile(self):
        with self.assertRaises(BusinessIntegrationError): compose_profile('unknown')


if __name__ == '__main__':
    unittest.main()
