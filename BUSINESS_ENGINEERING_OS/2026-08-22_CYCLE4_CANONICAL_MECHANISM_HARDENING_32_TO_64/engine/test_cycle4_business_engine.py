import unittest
from cycle4_business_engine import *

class T(unittest.TestCase):
    def test_duplicate_evidence_one_family(self):
        self.assertEqual(len(canonical_evidence_family([SourceAlias('a','LEAN','h'),SourceAlias('b','LEAN','h')])),1)
    def test_broken_never_counts(self):
        self.assertEqual(len(canonical_evidence_family([SourceAlias('bad',None,'x',True),SourceAlias('good','X','y')])),1)
    def test_replacement(self):
        self.assertEqual(resolve_broken_alias(SourceAlias('bad','AA',broken=True,replacement_file_id='good'),{'good'}),'REPLACED_BY_VALID_ALIAS')
    def test_k5_fail_closed(self):
        self.assertEqual(k5_fixture(False,True),'HOLD'); self.assertEqual(k5_fixture(True,True),'K5')
    def test_framework_conditional(self):
        self.assertEqual(route_framework(question='fatal flaw',irreversible_cost=100,uncertainty='HIGH'),'ROAD_TEST')
        self.assertEqual(route_framework(question='jobs circumstance progress',irreversible_cost=0,uncertainty='HIGH'),'JTBD')
    def test_contradiction_not_averaged(self):
        self.assertEqual(route_contradiction({'claim':'market grows','scope':'IE'},{'claim':'unit economics weak','scope':'IE'}).resolution,'PRESERVE_AND_TEST')
    def test_uncertainty(self):
        self.assertIsNone(format_uncertainty('binary',None)['value']); self.assertEqual(format_uncertainty('interval',low=1,high=2)['high'],2)
    def test_voi(self):
        self.assertTrue(voi(Measurement('go',0.5,100,10))['run']); self.assertFalse(voi(Measurement('go',0.1,10,5))['run'])
    def test_wip(self):
        out=wip_select([WorkItem('a',1),WorkItem('b',2),WorkItem('c',3),WorkItem('d',4)])
        self.assertEqual(out['primary'],['a']); self.assertEqual(out['pilots'],['b','c']); self.assertEqual(out['held'],['d'])
    def test_quick_stop(self):
        self.assertEqual(quick_stop(learning_milestone=False,customer_milestone=False,irreversible_spend=True),'STOP_NO_EVIDENCE_MILESTONE')
    def test_handoff(self):
        self.assertEqual(human_handoff(legal_material_unknown=True),'STOP_HUMAN_LEGAL_REQUIRED')
    def test_fake_precision(self):
        self.assertEqual(anti_fake_precision({'total_score':91}),'REJECT_ADDITIVE_SCORE'); self.assertEqual(anti_fake_precision({'evidence':'E2','cash_timing':None}),'PASS')
    def test_creative_opportunity_freshness(self):
        self.assertEqual(creative_opportunity_state(source_is_official=False,deadline_verified=True,eligibility_verified=True,budget_verified=True),'DISCOVERY_ONLY')
        self.assertEqual(creative_opportunity_state(source_is_official=True,deadline_verified=True,eligibility_verified=True,budget_verified=True),'APPLICATION_READY_FACTS')

if __name__=='__main__': unittest.main()
