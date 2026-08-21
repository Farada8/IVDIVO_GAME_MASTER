import json, os, tempfile, unittest, sys, pathlib, hashlib
ROOT=pathlib.Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'runtime'))
from nmm_trust_anchor import classify_anchor
from nmm_provider_snapshot_guard import validate_snapshot,credential_environment_state
from nmm_listener_provenance import validate_human_record
from nmm_blind_whistle_scoring import seal_protocol,verify_protocol_seal,score_rows
from nmm_escrow_content_readback import verify_escrow
from nmm_evidence_progress_vector import compile_vector
from nmm_experiment_governor import choose
from nmm_replication_bridge_v2 import sanitize_record,classify_replication
H='a'*64
class T(unittest.TestCase):
 def test_hash_only_internal(self):
  r=classify_anchor({'evidence_class':'INTERNAL_ENGINEERING','artifact_sha256':H,'protocol_sha256':H,'captured_at':'2026-08-21T19:00:00Z','producer_declaration':'machine'}); self.assertEqual(r['gate'],'INTERNAL_ONLY')
 def test_external_provider_needs_auth(self):
  r=classify_anchor({'evidence_class':'AUTHENTICATED_PROVIDER','artifact_sha256':H,'protocol_sha256':H,'captured_at':'2026-08-21T19:00:00Z','producer_declaration':'tool','authenticated_source':False}); self.assertEqual(r['gate'],'INTERNAL_ONLY')
 def test_no_credential_hold(self): self.assertEqual(credential_environment_state({})['gate'],'HOLD_NO_CREDENTIAL')
 def test_provider_missing(self): self.assertEqual(validate_snapshot({},now_iso='2026-08-21T20:00:00+00:00')['gate'],'FAIL_CLOSED')
 def test_provider_unauthenticated(self):
  s={'provider':'x','provider_model':'m','output_format':'wav','captured_at':'2026-08-21T19:00:00Z','authenticated':False,'preflight_artifact_sha256':H,'capabilities':{'tts':True}}; self.assertEqual(validate_snapshot(s,now_iso='2026-08-21T20:00:00+00:00')['reason'],'NOT_AUTHENTICATED')
 def test_provider_stale(self):
  s={'provider':'x','provider_model':'m','output_format':'wav','captured_at':'2026-08-19T00:00:00Z','authenticated':True,'preflight_artifact_sha256':H,'capabilities':{'tts':True}}; self.assertEqual(validate_snapshot(s,now_iso='2026-08-21T20:00:00+00:00')['gate'],'STALE_REVALIDATE')
 def test_human_missing_declaration(self): self.assertEqual(validate_human_record({'listener_id':'L'})['gate'],'FAIL')
 def test_human_complete(self):
  r={'listener_id':'L1','listener_declaration':'I_LISTENED_ONCE','captured_at':'x','artifact_sha256':H,'protocol_sha256':H,'device':'PHONE','methodology':'one listen','raw_response_hash':H}; self.assertEqual(validate_human_record(r)['gate'],'PROVENANCE_COMPLETE')
 def test_protocol_mutation(self):
  p=seal_protocol({'min_accuracy':.75,'min_mean_realism':3.5}); self.assertTrue(verify_protocol_seal(p)); p['min_accuracy']=.5; self.assertFalse(verify_protocol_seal(p))
 def test_scoring_mutated_protocol_fails(self):
  p=seal_protocol({'min_accuracy':.75,'min_mean_realism':3.5}); p['min_accuracy']=.1; self.assertEqual(score_rows([],{},p)['gate'],'FAIL_PROTOCOL_MUTATED')
 def test_scoring_pass_fixture(self):
  p=seal_protocol({'min_accuracy':.75,'min_mean_realism':3.5}); rows=[{'device_pass':'HEADPHONES','trial':'01','shorter_sound_guess_FIRST_SECOND_CANNOT_TELL':'FIRST','realism_1_5':'4'}]; self.assertEqual(score_rows(rows,{'HEADPHONES:01':'FIRST'},p)['gate'],'PASS')
 def test_escrow_locator_only(self): self.assertEqual(verify_escrow({'locator':'x','expected_sha256':H})['gate'],'METADATA_ONLY')
 def test_escrow_content_pass(self):
  with tempfile.NamedTemporaryFile(delete=False) as f: f.write(b'abc'); p=f.name
  h=hashlib.sha256(b'abc').hexdigest(); self.assertEqual(verify_escrow({'locator':'x','expected_sha256':h},p)['gate'],'CONTENT_READBACK_PASS'); os.unlink(p)
 def test_progress_internal_not_release(self):
  x=compile_vector({'source_integrity':'PASS','deterministic_regression':'PASS'}); self.assertTrue(x['internal_engineering_ready']); self.assertFalse(x['release_ready'])
 def test_progress_release_requires_all(self):
  x=compile_vector({k:'PASS' for k in ('source_integrity','deterministic_regression','cross_storage_parity','provider_truth','human_truth','specialist_truth','economics_truth')}); self.assertTrue(x['release_ready'])
 def test_governor_prefers_real_human(self):
  r=choose([{'id':'schema','class':'NEW_SCHEMA','info_gain':5,'cost':1},{'id':'listen','class':'REAL_HUMAN','info_gain':5,'cost':1}]); self.assertEqual(r['selected']['id'],'listen')
 def test_governor_refuses_generic_gapless(self):
  r=choose([{'id':'arch','class':'GENERIC_ARCHITECTURE','info_gain':100,'cost':0,'demonstrated_gap':False}]); self.assertEqual(r['gate'],'REFUSE_META_WORK')
 def test_sanitize_leakage(self):
  r=sanitize_record({'root_cause':'Leo C17 whistle in NMM','exact_text':'Harbour Copper Lantern','asset_id':'C17'}); self.assertNotIn('Leo',json.dumps(r)); self.assertNotIn('exact_text',r); self.assertNotIn('asset_id',r)
 def test_one_project_discovery(self): self.assertEqual(classify_replication([{'project_id':'NMM','result':'PASS','human_evidence':True}])['status'],'DISCOVERY_ONLY')
 def test_two_projects_candidate_at_most(self):
  x=classify_replication([{'project_id':'A','result':'PASS','human_evidence':True},{'project_id':'B','result':'PASS','human_evidence':True}]); self.assertEqual(x['status'],'CANDIDATE_FOR_REVIEW'); self.assertFalse(x['auto_promote'])
if __name__=='__main__': unittest.main()
