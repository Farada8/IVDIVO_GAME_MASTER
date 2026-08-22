from pathlib import Path
import importlib.util

HERE=Path(__file__).resolve().parent.parent
SPEC=importlib.util.spec_from_file_location('cycle32d_decision_yield_utilities', HERE/'tools'/'cycle32d_decision_yield_utilities.py')
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)

extract_si_ids=MOD.extract_si_ids
registry_collision_guard=MOD.registry_collision_guard
freshness_vector=MOD.freshness_vector
dedupe_prompt_bank=MOD.dedupe_prompt_bank
evidence_yield=MOD.evidence_yield
voi_route=MOD.voi_route
proof_claim_classifier=MOD.proof_claim_classifier
rollback_plan=MOD.rollback_plan
validate_input_asset_registry=MOD.validate_input_asset_registry

def test_01_extract_si_ids(): assert extract_si_ids('SI-0015 then SI-0016')=={'SI-0015','SI-0016'}
def test_02_registry_real_collision(): assert registry_collision_guard('SI-0016',{'SI-0015'},{'SI-0016'})['verdict']=='STOP_COLLISION'
def test_03_registry_no_allocation(): assert registry_collision_guard(None,{'SI-0015'},{'SI-0016'})['verdict']=='NO_ALLOCATION'
def test_04_registry_safe_is_pending_recheck(): assert registry_collision_guard('SI-0017',{'SI-0015'},{'SI-0016'})['verdict']=='SAFE_TO_RESERVE_PENDING_RECHECK'
def test_05_freshness_pass(): assert freshness_vector(['main','drive'],{'main':{'state':'CURRENT'},'drive':{'state':'FRESH'}})['verdict']=='PASS'
def test_06_freshness_stale(): assert freshness_vector(['main'],{'main':{'state':'STALE'}})['stale']==['main']
def test_07_freshness_missing(): assert freshness_vector(['registry'],{})['missing']==['registry']
def test_08_prompt_dedupe():
    a={'id':'A','consumer':'x','evidence_class':'E1','gate':'g','action_semantics':'read','state_mutation':'none'}
    b=dict(a,id='B')
    assert dedupe_prompt_bank([a,b])['verdict']=='MERGE_DUPLICATES'
def test_09_yield_decision_change(): assert evidence_yield('A','B')['verdict']=='PASS_YIELD'
def test_10_yield_evidence_only(): assert evidence_yield('A','A',evidence_added=['readback'])['verdict']=='PASS_YIELD'
def test_11_yield_hold(): assert evidence_yield('A','A',explicit_hold='external evidence required')['verdict']=='PASS_YIELD'
def test_12_yield_no_effect(): assert evidence_yield('A','A')['verdict']=='REJECT_NO_EFFECT'
def test_13_voi_requires_consumer(): assert voi_route([{'id':'x'}])['verdict']=='HOLD_NO_DECISION_CONSUMER'
def test_14_voi_ordinal():
    tests=[{'id':'a','decision_consumer':'d','decision_flip':1,'evidence_independence':1,'burden':1,'risk':1},{'id':'b','decision_consumer':'d','decision_flip':3,'evidence_independence':2,'burden':2,'risk':2}]
    assert voi_route(tests)['selected']=='b'
def test_15_proof_ceiling(): assert proof_claim_classifier('E5','E2')['verdict']=='NOT_PROVEN_EVIDENCE_CEILING'
def test_16_proof_supported(): assert proof_claim_classifier('E1','E2')['verdict']=='SUPPORTED'
def test_17_selective_rollback():
    r=rollback_plan('A',{'A':['B','LOCK'],'B':['C']},{'LOCK'})
    assert set(r['revalidate'])=={'B','C'} and 'LOCK' not in r['revalidate']
def test_18_asset_registry_good(): assert validate_input_asset_registry([{'filename':'a.json','size_bytes':1,'sha256':'a'*64,'role':'INPUT'}])['verdict']=='PASS'
def test_19_asset_registry_bad_hash(): assert validate_input_asset_registry([{'filename':'a.json','size_bytes':1,'sha256':'bad','role':'INPUT'}])['verdict']=='FAIL'
