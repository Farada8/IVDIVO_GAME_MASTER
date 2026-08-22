import unittest
from runtime.cycle5_control import *

class Cycle5ControlTests(unittest.TestCase):
    def test_explicit_supersession(self):
        old=SurfaceRecord('old','writing',1,'1','aaa'); new=SurfaceRecord('new','writing',1,'2','bbb',('old',))
        self.assertEqual(resolve_current_surface([old,new],'writing').surface_id,'new')
    def test_split_brain(self):
        with self.assertRaises(SplitBrainError): resolve_current_surface([SurfaceRecord('a','writing',1,'1','a'),SurfaceRecord('b','writing',1,'2','b')],'writing')
    def test_scope_separation(self):
        rv=ReadinessVector(story_gate=True); self.assertTrue(rv.invariant_ok()); self.assertFalse(rv.founder_lock or rv.provider or rv.human)
    def test_false_progress_machine_not_human(self):
        self.assertTrue(claim_allowed(EvidenceClass.MACHINE,'MACHINE_GATE_PASS')); self.assertFalse(claim_allowed(EvidenceClass.MACHINE,'HUMAN_PASS'))
    def test_false_progress_human_not_founder(self):
        self.assertFalse(claim_allowed(EvidenceClass.HUMAN,'FOUNDER_LOCK')); self.assertTrue(claim_allowed(EvidenceClass.FOUNDER,'FOUNDER_LOCK'))
    def test_fact_lock_stale(self):
        with self.assertRaises(StaleFactLockError): FactLock('F','h1',3,'a').commit('h0',2,'h2')
    def test_fact_lock_fresh(self):
        n=FactLock('F','h1',3,'a').commit('h1',3,'h2'); self.assertEqual((n.version,n.value_hash),(4,'h2'))
    def test_one_evidence_family(self):
        rs=[EvidenceRecord('g','A',EvidenceClass.MODEL,'A'),EvidenceRecord('c','A',EvidenceClass.MODEL,'A'),EvidenceRecord('r','A',EvidenceClass.MODEL,'A')]
        self.assertEqual(independent_family_count(rs),1)
    def test_two_evidence_families(self):
        rs=[EvidenceRecord('m','A',EvidenceClass.MODEL,'A'),EvidenceRecord('p','B',EvidenceClass.PROVIDER,'B')]; self.assertEqual(independent_family_count(rs),2)
    def test_mutation_stale(self):
        with self.assertRaises(MutationGuardError): MutationIntent('f','old','new').preflight('other')
    def test_mutation_approval(self):
        with self.assertRaises(MutationGuardError): MutationIntent('r','old','new',False,True).preflight('old',False)
    def test_partial_repair_required(self):
        tx=TransactionJournal('T',('github','drive','state')); tx.record_write('github','gh'); tx.mark_failure('drive'); self.assertEqual(tx.status,'REPAIR_REQUIRED'); self.assertEqual(tx.next_unapplied(),['drive','state'])
    def test_ack_idempotent(self):
        tx=TransactionJournal('T',('github','drive')); tx.record_write('github','gh'); tx.record_write('github','gh'); self.assertEqual(tx.applied,['github']); tx.record_write('drive','d'); self.assertEqual(tx.status,'COMMITTED')
    def test_state_missing_field(self):
        with self.assertRaises(StateDriftError): validate_state_shape({'schema_version':'2.1','status':'CURRENT','authority_order':['A']})
    def test_state_minimum(self):
        validate_state_shape({'schema_version':'2.1','status':'CURRENT','authority_order':['A'],'resume_algorithm':['FRESHNESS_SWEEP']})
    def test_governor_p1_preempts_meta(self):
        ts=[RoutedTask('meta',0,.9,False,True),RoutedTask('book',1,.7,False,False)]; self.assertEqual(select_next_task(ts).task_id,'book')
    def test_governor_meta_when_p1p2_blocked(self):
        ts=[RoutedTask('meta',0,.9,False,True),RoutedTask('book',1,1,True,False),RoutedTask('provider',2,1,True,False)]; self.assertEqual(select_next_task(ts).task_id,'meta')

if __name__=='__main__': unittest.main()
