import unittest
from engine.cycle9_engine import *

class T(unittest.TestCase):
    def test_authority(self):
        AuthoritySnapshot('a'*40,'e','VERIFIED_CURRENT','r','l','t').validate()
    def test_bad_sha(self):
        with self.assertRaises(GateError): AuthoritySnapshot('x','e','VERIFIED_CURRENT','r','l','t').validate()
    def test_library_collision(self):
        r=LibraryRegistry(); r.add(SourcePointer('x','a','GITHUB'))
        with self.assertRaises(GateError): r.add(SourcePointer('x','b','GITHUB'))
    def test_candidate_unique(self):
        f=CandidateFamily([CandidateState('SI-1','READY','U','g')])
        with self.assertRaises(GateError): f.require_unique_new_id('SI-1')
    def test_real_interruption_unqualified_without_readback(self):
        q=qualify_interruption(InterruptionObservation('e',True,('P',),False,False,False))
        self.assertFalse(q.qualifies); self.assertIn('PROJECT_SLICE_READBACK_INCOMPLETE',q.reasons)
    def test_synthetic_not_real(self):
        q=qualify_interruption(InterruptionObservation('e',True,('P',),True,True,True,synthetic=True))
        self.assertFalse(q.qualifies)
    def test_recovery_threshold(self):
        c=RecoveryEvidenceCounter()
        for i,p in enumerate(('A','B','A')):
            c.add(InterruptionObservation(str(i),True,(p,),True,True,True))
        self.assertTrue(c.promotion_ready())
    def test_slice_current(self): self.assertEqual(project_slice_freshness(ProjectSlice('p','A','A')),'CURRENT_MATCH')
    def test_slice_stale(self): self.assertEqual(project_slice_freshness(ProjectSlice('p','A','B')),'STALE_CURRENT_SLICE')
    def test_slice_historical(self): self.assertEqual(project_slice_freshness(ProjectSlice('p','A','B','HISTORICAL')),'EXEMPT_HISTORICAL_SLICE')
    def test_approval(self): self.assertEqual(project_slice_freshness(ProjectSlice('p','A','A','CURRENT',True,False)),'APPROVAL_EVENT_MISSING')
    def test_evidence_firewall(self):
        ok,missing=evidence_gate(EvidenceClaim('HUMAN_PREFERENCE',frozenset({EvidenceClass.TEST_EXECUTED})))
        self.assertFalse(ok); self.assertIn('HUMAN_VALIDATED',missing)
    def test_metric_relevance(self): self.assertEqual(metric_gate(MetricProposal('m',None,'u',1,3)),'REJECT_METRIC_WITHOUT_DECISION_RELEVANCE')
    def test_metric_voi(self): self.assertEqual(metric_gate(MetricProposal('m','d','u',1,3)),'MEASURE')
    def test_wip(self): self.assertEqual(wip_gate([WorkItem('a',True,True),WorkItem('b',True,False,True),WorkItem('c',True,False,True)]),'WIP_OK')
    def test_wip_over(self): self.assertEqual(wip_gate([WorkItem('a',True,True),WorkItem('b',True,True)]),'WIP_EXCEEDED')
    def test_causal_incomplete(self): self.assertEqual(causal_model_gate(CausalHypothesis('i','e',(),(),(),())),'INCOMPLETE_CAUSAL_MODEL')
    def test_causal_ready(self): self.assertEqual(causal_model_gate(CausalHypothesis('i','e',('f',),('d',),('g',),())),'CAUSAL_MODEL_READY')
    def test_policy_resistance(self): self.assertEqual(policy_resistance_gate(ExperimentResult('x',True,False,False)),'POLICY_RESISTANCE_DETECTED')
    def test_double_loop(self): self.assertEqual(policy_resistance_gate(ExperimentResult('x',False,None,False,True)),'DOUBLE_LOOP_REVIEW')
    def test_decision_delta(self): self.assertEqual(decision_delta_value(DecisionDelta('a','b',False)),'DECISION_CHANGED')
    def test_no_delta(self): self.assertEqual(decision_delta_value(DecisionDelta('a','a',False)),'NO_DECISION_DELTA')
    def test_duplicate_merge(self): self.assertEqual(mechanism_disposition(MechanismRecord('m','k',1,0,1,True)),Disposition.MERGE)
    def test_false_positive_narrow(self): self.assertEqual(mechanism_disposition(MechanismRecord('m','k',5,2,1)),Disposition.NARROW)
    def test_unused_hold(self): self.assertEqual(mechanism_disposition(MechanismRecord('m','k',0,0,0)),Disposition.HOLD)
    def test_store_complete(self): self.assertEqual(cross_store_closure([StoreAction('a','G','h','h','CONFIRMED')]),'TRANSACTION_COMPLETE')
    def test_store_identity_mismatch(self): self.assertEqual(cross_store_closure([StoreAction('a','G','h','x','CONFIRMED')]),'STOP_IDENTITY_MISMATCH')
    def test_irreversible_unknown(self): self.assertEqual(cross_store_closure([StoreAction('a','P','h',None,'STARTED_UNKNOWN',False)]),'QUARANTINE_AMBIGUOUS_IRREVERSIBLE')
    def test_promotion_block(self): self.assertEqual(promotion_gate(PromotionPacket('c','VERIFIED_CURRENT',(),(),(),True)),'BLOCK_DIRECT_VERIFIED_CURRENT')
    def test_universal_requires_real(self): self.assertEqual(promotion_gate(PromotionPacket('c','READY',('x',),('v',),(),True,True)),'BLOCK_UNIVERSAL_WITHOUT_REAL_PILOT')
    def test_self_reference(self): self.assertEqual(self_reference_guard(SelfReferenceMutation(True,True,True,True)),'REJECT_SELF_EXEMPTION')
    def test_ledger_order(self):
        l=SequentialLedger(['P01','P02'])
        with self.assertRaises(GateError): l.append(RunResult('P02','x','PASS','f'))
    def test_ledger_complete(self):
        l=SequentialLedger(['P01','P02']); l.append(RunResult('P01','x','PASS','f')); l.append(RunResult('P02','x','PASS','f'))
        self.assertTrue(l.complete); self.assertEqual(len(l.digest()),64)

if __name__=='__main__': unittest.main()
