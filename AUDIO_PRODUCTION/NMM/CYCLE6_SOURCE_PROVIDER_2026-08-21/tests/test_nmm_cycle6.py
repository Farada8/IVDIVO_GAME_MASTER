import sys, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
from nmm_source_authority import *
from nmm_provider_execution_gate import *
from nmm_canary_evidence import *
from nmm_cycle6_orchestrator import *
ISLA="At eleven forty-seven at night, there are three kinds of calls worth answering. Family. Police. And people who already know they have made a mistake."
LEO="Most people lower their voice before that word."
VIV="Which is precisely why I'd prefer you not to improvise in this one."
EX=ISLA+' '+LEO+' '+VIV
SL='5116067fe2571b978fecfcf8f7e80af387bc243c173cde1e50b8a1ad27f42963'
class T(unittest.TestCase):
 def test01_isla_bind(self): self.assertEqual(bind_exact_line(role='ISLA_GRANT',exact_text=ISLA,authoritative_excerpt=EX,source_locator='frozen',source_slice_sha256=SL)['status'],'PASS')
 def test02_leo_bind(self): self.assertEqual(bind_exact_line(role='LEO_HART',exact_text=LEO,authoritative_excerpt=EX,source_locator='frozen',source_slice_sha256=SL)['status'],'PASS')
 def test03_viv_bind(self): self.assertEqual(bind_exact_line(role='VIVIAN_CROSS',exact_text=VIV,authoritative_excerpt=EX,source_locator='frozen',source_slice_sha256=SL)['status'],'PASS')
 def test04_stale_calder(self): self.assertEqual(bind_exact_line(role='NATE_CALDER',exact_text='x',authoritative_excerpt='x',source_locator='old',source_slice_sha256=SL)['status'],'STALE_ROLE_BINDING')
 def test05_revision_drift(self): self.assertEqual(source_revision_gate(expected_revision='a',observed_revision='b',expected_slice_sha=SL,observed_slice_sha=SL)['status'],'REEXPORT_REQUIRED')
 def test06_provider_hold(self): self.assertEqual(resolve_provider(None)['status'],'HOLD_EXTERNAL')
 def test07_provider_stale(self): self.assertEqual(resolve_provider({'verified':True,'fresh':False})['reason'],'SNAPSHOT_STALE')
 def test08_provider_pass(self): self.assertEqual(resolve_provider({'verified':True,'fresh':True,'model_id':'m','output_format':'wav','snapshot_hash':'h'})['status'],'PASS')
 def test09_candidate_hold(self): self.assertEqual(compile_candidates(role='ISLA_GRANT',inventory=None,inventory_hash=None)['status'],'HOLD_EXTERNAL')
 def test10_candidate_cap(self): self.assertEqual(len(compile_candidates(role='LEO_HART',inventory=[{'voice_id':str(i)} for i in range(9)],inventory_hash='h')['candidates']),5)
 def test11_viv_spoiler(self): self.assertEqual(len(compile_candidates(role='VIVIAN_CROSS',inventory=[{'voice_id':'v','labels':['villain']}],inventory_hash='h')['candidates']),0)
 def test12_candidate_hash(self): self.assertTrue(compile_candidates(role='ISLA_GRANT',inventory=[{'voice_id':'v'}],inventory_hash='h')['candidate_set_hash'])
 def test13_manifest_hold(self): self.assertEqual(freeze_s0_manifest(source_binding={'status':'PASS'},provider=resolve_provider(None),candidate_set={'status':'HOLD_EXTERNAL'},settings={})['status'],'FROZEN_SOURCE_ONLY_HOLD')
 def test14_zero_paid(self): self.assertIsNone(zero_paid_plan([{},{}])['estimated_cost'])
 def test15_dispatch_hold(self): self.assertEqual(dispatch_gate(provider=resolve_provider(None),manifests=[])['status'],'HOLD_EXTERNAL')
 def test16_redteam_secret(self): self.assertEqual(red_team({'api_key':'secret'})['status'],'FAIL')
 def test17_ingest_gate(self): self.assertEqual(ingest_canary(dispatch_status='HOLD_EXTERNAL',audio_bytes=None,request_hash=None,spend_receipt=None,metadata=None)['status'],'HOLD_EXTERNAL')
 def test18_ingest_missing_audio(self): self.assertEqual(ingest_canary(dispatch_status='GO_ONE_BOUNDED_CANARY',audio_bytes=None,request_hash='h',spend_receipt={},metadata={})['reason'],'AUDIO_BYTES_MISSING')
 def test19_ingest_provenance(self): self.assertEqual(ingest_canary(dispatch_status='GO_ONE_BOUNDED_CANARY',audio_bytes=b'a',request_hash=None,spend_receipt=None,metadata={})['status'],'FAIL_CLOSED')
 def test20_ingest_pass(self): self.assertEqual(ingest_canary(dispatch_status='GO_ONE_BOUNDED_CANARY',audio_bytes=b'a',request_hash='h',spend_receipt={'amount':1},metadata={'decodable':True})['status'],'PASS')
 def test21_tech_empty(self): self.assertEqual(technical_compare([])['status'],'HOLD_EXTERNAL')
 def test22_tech_quarantine(self): self.assertEqual(technical_compare([{'status':'PASS','metadata':{'alignment_status':'QUARANTINE'}}])['status'],'FAIL_CLOSED')
 def test23_blind_hold(self): self.assertEqual(blinded_s1_map(None)['status'],'HOLD_EXTERNAL')
 def test24_blind_labels(self): self.assertEqual(blinded_s1_map(['x','y'])['labels']['x'],'A')
 def test25_eligibility_hold(self): self.assertEqual(provisional_eligibility([])['status'],'HOLD_EXTERNAL')
 def test26_no_lock(self): self.assertFalse(provisional_eligibility([{'status':'PASS'}])['voice_lock'])
 def test27_spend_null(self): self.assertIsNone(reject_taxonomy([])['measured_spend'])
 def test28_spend_measured(self): self.assertEqual(reject_taxonomy([],[{'amount':1.2},{'amount':.8}])['measured_spend'],2.0)
 def test29_packet_hold(self): self.assertEqual(evidence_packet(source_bindings=[],provider=resolve_provider(None),candidate_sets=[],canaries=[],spend={})['status'],'ENGINEERING_READY_EXTERNAL_HOLD')
 def test30_packet_no_release(self): self.assertFalse(evidence_packet(source_bindings=[],provider=resolve_provider(None),candidate_sets=[],canaries=[],spend={})['release_go'])
 def test31_orchestrator_32(self): self.assertEqual(len(execute_cycle6({})),32)
 def test32_orchestrator_source_pass(self): self.assertEqual(execute_cycle6({})[0]['status'],'PASS_REAL_SOURCE')
if __name__=='__main__': unittest.main()
