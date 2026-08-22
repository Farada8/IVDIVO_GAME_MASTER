import pytest
from cycle32d_engine import *

def test_01_extract_ids(): assert extract_si_ids('x SI-0015 y SI-0016')=={'SI-0015','SI-0016'}
def test_02_collision_real_case(): assert registry_collision_guard('SI-0016', {'SI-0015'}, {'SI-0016'})['verdict']=='STOP_COLLISION'
def test_03_no_allocation(): assert registry_collision_guard(None, {'SI-0015'}, {'SI-0016'})['verdict']=='NO_ALLOCATION'
def test_04_safe_pending_recheck(): assert registry_collision_guard('SI-0017', {'SI-0015'}, {'SI-0016'})['verdict']=='SAFE_TO_RESERVE_PENDING_RECHECK'
def test_05_authority_pass(): assert authority_stack_resolver([{'id':'v2','status':'VERIFIED_CURRENT','role':'CONTROLLING','priority':1},{'id':'v3','status':'CANDIDATE','role':'COMPATIBLE','priority':2}])['ordered'][0]=='v2'
def test_06_authority_conflict(): assert authority_stack_resolver([{'id':'a','status':'CURRENT','role':'CONTROLLING','priority':1},{'id':'b','status':'CURRENT','role':'CONTROLLING','priority':1}])['verdict'].startswith('HOLD')
def test_07_fresh_vector(): assert freshness_vector(['main','drive'],{'main':{'state':'CURRENT'},'drive':{'state':'FRESH'}})['verdict']=='PASS'
def test_08_stale_vector(): assert 'main' in freshness_vector(['main'],{'main':{'state':'STALE'}})['stale']
def test_09_missing_vector(): assert 'registry' in freshness_vector(['registry'],{})['missing']
def test_10_wip_normal(): assert meta_wip_limiter(1,2)['verdict']=='PASS'
def test_11_wip_stop(): assert meta_wip_limiter(2,3)['verdict']=='STOP_WIP_LIMIT'
def test_12_wip_founder_switch(): assert meta_wip_limiter(2,3,founder_switched=True)['verdict']=='PASS_FOUNDER_SWITCH'
def test_13_return_guard(): assert production_return_guard('resume product')=='PASS'
def test_14_return_missing(): assert production_return_guard(None)=='STOP_NO_RETURN_TARGET'
def test_15_fingerprint_equal():
 a={'consumer':'x','evidence_class':'E1','gate':'g','action_semantics':'read','state_mutation':'none'}; assert prompt_fingerprint(a)==prompt_fingerprint(dict(a))
def test_16_dedupe_detects():
 a={'id':'1','consumer':'x','evidence_class':'E1','gate':'g','action_semantics':'read','state_mutation':'none'}; b=dict(a,id='2'); assert dedupe_prompt_bank([a,b])['duplicates']
def test_17_yield_decision(): assert evidence_yield('A','B')['verdict']=='PASS_YIELD'
def test_18_yield_evidence(): assert evidence_yield('A','A',['source readback'])['verdict']=='PASS_YIELD'
def test_19_yield_hold(): assert evidence_yield('A','A',explicit_hold='external evidence')['verdict']=='PASS_YIELD'
def test_20_yield_no_effect(): assert evidence_yield('A','A')['verdict']=='REJECT_NO_EFFECT'
def test_21_voi_selects():
 x=[{'id':'a','decision_consumer':'d','decision_flip':1,'evidence_independence':1,'burden':1,'risk':1},{'id':'b','decision_consumer':'d','decision_flip':3,'evidence_independence':2,'burden':2,'risk':2}]; assert voi_route(x)['selected']=='b'
def test_22_voi_no_consumer(): assert voi_route([{'id':'a'}])['verdict']=='HOLD_NO_DECISION_CONSUMER'
def test_23_cod_high(): assert cost_of_delay_band('authority corruption')=='HIGH'
def test_24_cod_medium(): assert cost_of_delay_band('blocks production deadline')=='MEDIUM'
def test_25_proof_ceiling(): assert proof_claim_classifier('E5','E2')['verdict']=='NOT_PROVEN_EVIDENCE_CEILING'
def test_26_proof_supported(): assert proof_claim_classifier('E1','E2')['verdict']=='SUPPORTED'
def test_27_external_firewall(): assert external_evidence_firewall('HUMAN_SIGNAL','MODEL_REVIEW')=='STOP_EVIDENCE_SUBSTITUTION'
def test_28_fail_closed_registry(): assert fail_closed_router('REGISTRY_ID_COLLISION_RISK')=='NO_ID_ALLOCATION'
def test_29_observability_no_score():
 o=observability([{'type':'decision_changed'},{'type':'decision_changed'},{'type':'no_effect'}]); assert o['decision_changed']==2 and o['no_effect']==1 and 'score' not in o
def test_30_rollback_selective():
 r=rollback_plan('A',{'A':['B','LOCK'],'B':['C']},{'LOCK'}); assert set(r['revalidate'])=={'B','C'} and 'LOCK' not in r['revalidate']
def test_31_promotion_hold(): assert promotion_disposition(prospective_cross_project=False,registry_race_guard=True,application_readback=True,evidence_ceiling='E2')['verdict']=='HOLD_LOCAL_PILOT'
def test_32_asset_registry(): assert validate_input_asset_registry([{'filename':'a','size_bytes':1,'sha256':'a'*64,'role':'INPUT'}])['verdict']=='PASS'
