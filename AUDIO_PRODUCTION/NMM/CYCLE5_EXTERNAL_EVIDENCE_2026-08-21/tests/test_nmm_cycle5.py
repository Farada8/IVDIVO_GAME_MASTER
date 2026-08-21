import unittest, sys, pathlib
ROOT=pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'runtime'))
from nmm_cycle5_frontier_orchestrator import classify
from nmm_provider_gate_adapter import credential_state, admit_verified_snapshot
from nmm_cast_candidate_filter import filter_candidates
from nmm_s0_manifest_freezer import freeze, verify
from nmm_alignment_shape_normalizer import normalize
from nmm_human_session_sealer import seal
from nmm_human_answer_capture import capture
from nmm_device_evidence_aggregator import aggregate
from nmm_association_coder import code
from nmm_finalist_selector import select
from nmm_asset_evidence_ledger import append
from nmm_external_evidence_vector import compile
H='a'*64
class T(unittest.TestCase):
 def test01_no_credential_hold(self): self.assertEqual(classify(1,credential_present=False,provider_snapshot_present=False,real_human_rows=0)['status'],'HOLD_EXTERNAL_CREDENTIAL')
 def test02_snapshot_dependency(self): self.assertEqual(classify(2,credential_present=False,provider_snapshot_present=False,real_human_rows=0)['status'],'HOLD_DEP_PROVIDER_SNAPSHOT')
 def test03_provider_adapter_no_secret(self): self.assertFalse(credential_state({})['secret_persisted'])
 def test04_provider_unverified_fails(self): self.assertTrue(admit_verified_snapshot({'status':'FAIL'})['status'].startswith('FAIL_CLOSED'))
 def test05_provider_verified_no_lock(self): self.assertFalse(admit_verified_snapshot({'status':'PASS','verified':True,'snapshot_hash':H})['voice_lock'])
 def test06_cast_cap(self): self.assertEqual(len(filter_candidates([{'voice_id':str(i),'name':str(i)} for i in range(9)])['accepted']),5)
 def test07_vivian_spoiler_filter(self): self.assertEqual(len(filter_candidates([{'voice_id':'x','name':'killer voice'}],role='VIVIAN')['accepted']),0)
 def test08_filter_no_paid(self): self.assertEqual(filter_candidates([])['paid_audio_calls'],0)
 def test09_s0_missing_hold(self): self.assertEqual(freeze({})['status'],'HOLD_SOURCE_OR_SETTINGS_BINDING')
 def test10_s0_seal(self):
  m=freeze({'exact_text':'x','role':'ISLA','provider':'elevenlabs','model_id':'m','output_format':'wav','settings':{'a':1}}); self.assertTrue(verify(m))
 def test11_s0_mutation_detected(self):
  m=freeze({'exact_text':'x','role':'ISLA','provider':'elevenlabs','model_id':'m','output_format':'wav','settings':{'a':1}}); m['exact_text']='y'; self.assertFalse(verify(m))
 def test12_alignment_missing_quarantine(self): self.assertEqual(normalize({})['status'],'QUARANTINE')
 def test13_alignment_nonmonotonic(self): self.assertEqual(normalize({'words':[{'text':'a','start':1,'end':2},{'text':'b','start':1.5,'end':2.2}]})['status'],'QUARANTINE')
 def test14_alignment_normal(self): self.assertEqual(normalize({'words':[{'text':'a','start':0,'end':1}]})['status'],'NORMALIZED')
 def test15_alignment_no_sample_lock(self): self.assertFalse(normalize({'words':[{'text':'a','start':0,'end':1}]})['sample_lock'])
 def test16_human_gate(self): self.assertEqual(classify(17,credential_present=False,provider_snapshot_present=False,real_human_rows=0)['status'],'HOLD_EXTERNAL_HUMAN')
 def test17_session_missing_fail(self): self.assertEqual(seal({})['status'],'FAIL_PREDECLARATION')
 def test18_session_sealed(self): self.assertEqual(seal({'listener_id':'L1','protocol_sha256':H,'artifact_set_sha256':H,'device':'HEADPHONES','one_listen_rule':True})['status'],'SEALED_BEFORE_PLAYBACK')
 def test19_capture_requires_seal(self): self.assertEqual(capture({},[{'x':1}])['status'],'FAIL_SESSION_NOT_SEALED')
 def test20_capture_empty_hold(self):
  s=seal({'listener_id':'L1','protocol_sha256':H,'artifact_set_sha256':H,'device':'HEADPHONES','one_listen_rule':True}); self.assertEqual(capture(s,[])['status'],'HOLD_NO_REAL_ANSWERS')
 def test21_capture_hash(self):
  s=seal({'listener_id':'L1','protocol_sha256':H,'artifact_set_sha256':H,'device':'HEADPHONES','one_listen_rule':True}); self.assertEqual(len(capture(s,[{'trial':'1'}])['raw_response_sha256']),64)
 def test22_aggregate_empty(self): self.assertEqual(aggregate([])['status'],'NO_REAL_DATA')
 def test23_aggregate_preserves_fail(self): self.assertEqual(len(aggregate([{'listener_id':'L1','device':'PHONE','trial':'1','correct':False,'realism':2}])['individual_failures']),1)
 def test24_association_police(self): self.assertIn('POLICE',code('sounds like a police whistle'))
 def test25_association_default(self): self.assertEqual(code('neutral tone'),['OTHER_OR_NONE'])
 def test26_no_finalists_without_humans(self): self.assertEqual(select([{'human_listeners':1,'phone_accuracy':1,'headphone_accuracy':1,'mean_realism':5}])['status'],'NO_FINALISTS')
 def test27_max_two_finalists(self):
  x=[{'id':str(i),'human_listeners':3,'phone_accuracy':.9,'headphone_accuracy':.9,'mean_realism':4} for i in range(5)]; self.assertEqual(len(select(x)['finalists']),2)
 def test28_ledger_missing_rejects(self):
  with self.assertRaises(ValueError): append([],{})
 def test29_human_ledger_requires_response_hash(self):
  with self.assertRaises(ValueError): append([],{'asset_id':'a','decision':'ACCEPT','artifact_sha256':H,'evidence_class':'HUMAN'})
 def test30_ledger_hash_chain(self):
  x=append([],{'asset_id':'a','decision':'HOLD','artifact_sha256':H,'evidence_class':'ENGINEERING'}); y=append(x,{'asset_id':'b','decision':'REJECT','artifact_sha256':H,'evidence_class':'ENGINEERING'}); self.assertEqual(y[1]['previous_record_sha256'],y[0]['record_sha256'])
 def test31_vector_unknown_not_ready(self): self.assertFalse(compile({})['cycle5_external_ready'])
 def test32_release_never_auto(self): self.assertFalse(compile({k:'PASS' for k in ('provider_snapshot','cast_metadata','s0_manifest','provider_canaries','alignment','human_headphones','human_phone','multi_listener','finalists','asset_ledger')})['release_ready'])
if __name__=='__main__': unittest.main()
