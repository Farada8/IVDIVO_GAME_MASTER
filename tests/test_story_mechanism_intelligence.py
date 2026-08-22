import importlib.util
from pathlib import Path

PATH = Path(__file__).parents[1] / 'tools' / 'ivdivo_story_mechanism_intelligence.py'
spec = importlib.util.spec_from_file_location('smi', PATH)
smi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(smi)

def sig(**kw):
    d={'project_id':'P1','stage':'ARCHITECTURE','genre_tags':['mystery'],'problem_tags':['weak opposition','information asymmetry'],'desired_effects':['pressure','reader pull'],'hard_constraints':['canon protected'],'available_conditions':['source verified'],'forbidden_moves':['copy plot'],'max_mechanisms':3}
    d.update(kw); return d

def card(mid,**kw):
    d={'mechanism_id':mid,'statement':f'mechanism {mid}','disposition':'LOCAL_TEST','problem_tags':['weak opposition'],'effect_vector':['pressure'],'genre_tags':['mystery'],'prerequisites':[],'contraindications':[],'required_moves':[],'incompatible_with':[],'forbids_effects':[],'source_ids':[f'S-{mid}'],'independent_source_groups':[f'G-{mid}'],'evidence_locators':[f'L-{mid}'],'failure_modes':['overuse'],'project_specific_expression_removed':True,'portability':'PROJECT_NEUTRAL','requires_text_mutation':False}
    d.update(kw); return d

def test_signature_validation_passes(): assert smi.validate_problem_signature(sig())==[]
def test_signature_max_three_is_hard_cap(): assert 'invalid:max_mechanisms' in smi.validate_problem_signature(sig(max_mechanisms=4))
def test_relevant_mechanism_outranks_irrelevant():
    good=card('GOOD',problem_tags=['weak opposition','information asymmetry'],effect_vector=['pressure','reader pull']); bad=card('BAD',problem_tags=['world texture'],effect_vector=['humor'],genre_tags=['general'])
    assert smi.rank_mechanisms(sig(),[bad,good])[0]['card']['mechanism_id']=='GOOD'
def test_hard_contraindication_excludes():
    v=smi.mechanism_match_vector(sig(),card('C',contraindications=['canon protected'])); assert not v['eligible'] and any(x.startswith('contraindication:') for x in v['rejection_reasons'])
def test_hold_and_reject_are_excluded(): assert smi.rank_mechanisms(sig(),[card('H',disposition='HOLD'),card('R',disposition='REJECT')])==[]
def test_distinctive_expression_not_removed_excludes():
    v=smi.mechanism_match_vector(sig(),card('COPY',project_specific_expression_removed=False)); assert not v['eligible'] and 'distinctive_expression_not_confirmed_removed' in v['rejection_reasons']
def test_project_only_cross_project_transfer_excluded(): assert not smi.mechanism_match_vector(sig(),card('PO',portability='PROJECT_ONLY',project_id='OTHER'))['eligible']
def test_missing_prerequisite_excludes():
    v=smi.mechanism_match_vector(sig(),card('REQ',prerequisites=['human signal'])); assert not v['eligible'] and any(x.startswith('missing_prerequisites:') for x in v['rejection_reasons'])
def test_forbidden_required_move_excludes(): assert not smi.mechanism_match_vector(sig(),card('MOVE',required_moves=['copy plot']))['eligible']
def test_explicit_incompatible_pair_never_composes():
    out=smi.compose_mechanism_set(sig(),[card('A',incompatible_with=['B']),card('B',effect_vector=['reader pull'])]); ids={x['mechanism_id'] for x in out['selected']}; assert not {'A','B'}<=ids
def test_complementary_effects_are_preferred():
    out=smi.compose_mechanism_set(sig(max_mechanisms=2),[card('A',effect_vector=['pressure']),card('B',effect_vector=['reader pull'],problem_tags=['information asymmetry']),card('C',effect_vector=['pressure'])]); ids={x['mechanism_id'] for x in out['selected']}; assert 'B' in ids and len(ids)==2 and out['selection_vector']['desired_effect_coverage']==2
def test_packet_never_selects_more_than_three(): assert len(smi.build_story_mechanism_packet(sig(),[card(str(i),effect_vector=['pressure','reader pull']) for i in range(6)])['mechanisms'])<=3
def test_locked_project_is_shadow_only():
    p=smi.build_story_mechanism_packet(sig(locked=True),[card('A')]); assert p['status']=='SHADOW_ONLY' and 'LOCKED_TEXT_SHADOW_EVALUATION_ONLY_NO_MUTATION' in p['constraints']
def test_locked_project_rejects_mutating_mechanism(): assert smi.build_story_mechanism_packet(sig(locked=True),[card('A',requires_text_mutation=True)])['status']=='HOLD'
def test_duplicate_source_group_does_not_inflate_group_count(): assert smi.mechanism_match_vector(sig(),card('D',independent_source_groups=['G1','G1','G1']))['source_group_count']==1
def test_packet_marks_prediction_not_observation():
    p=smi.build_story_mechanism_packet(sig(),[card('A')]); assert p['prediction_status']=='PREDICTION_ONLY_NOT_OBSERVED_RESULT' and 'MATCH_VECTOR_IS_NOT_STORY_QUALITY_PROOF' in p['constraints']
def test_baseline_missing_dimension_holds(): assert smi.evaluate_baseline_candidate(baseline={'a':1},candidate={'a':2,'b':1},directions={'a':'HIGHER','b':'HIGHER'})['status']=='EVIDENCE_HOLD'
def test_observed_gain_requires_actual_improvement(): assert smi.evaluate_baseline_candidate(baseline={'causality':2,'clarity':2},candidate={'causality':3,'clarity':2},directions={'causality':'HIGHER','clarity':'HIGHER'})['status']=='OBSERVED_NET_GAIN'
def test_protected_regression_blocks_even_with_other_gain(): assert smi.evaluate_baseline_candidate(baseline={'causality':3,'reader_pull':2},candidate={'causality':2,'reader_pull':4},directions={'causality':'HIGHER','reader_pull':'HIGHER'},protected_dimensions=['causality'])['status']=='REGRESSION'
def test_major_regression_blocks(): assert smi.evaluate_baseline_candidate(baseline={'voice':3,'pressure':2},candidate={'voice':2,'pressure':4},directions={'voice':'HIGHER','pressure':'HIGHER'},severity_by_dimension={'voice':'MAJOR'})['status']=='REGRESSION'
def test_one_project_feedback_requires_second_project(): assert smi.record_outcome_feedback(card('A'),project_id='P1',packet_hash='x',result='PASS',measurable_gain=True,evidence_locator='e1')['application_readiness']=='SECOND_PROJECT_REQUIRED'
def test_two_project_feedback_reaches_promotion_review_not_auto_promotion():
    c=smi.record_outcome_feedback(card('A'),project_id='P1',packet_hash='x',result='PASS',measurable_gain=True,evidence_locator='e1'); c=smi.record_outcome_feedback(c,project_id='P2',packet_hash='y',result='PASS',measurable_gain=True,evidence_locator='e2'); assert c['application_readiness']=='PROMOTION_REVIEW_READY' and c['disposition']=='LOCAL_TEST'
def test_fatal_feedback_holds_future_application(): assert smi.record_outcome_feedback(card('A'),project_id='P1',packet_hash='x',result='REGRESSION',measurable_gain=False,severity='FATAL',evidence_locator='e1')['application_readiness']=='HOLD_APPLICATION'
def test_feedback_does_not_mutate_source_claim_fields():
    o=card('A',statement='keep',source_ids=['S1'],evidence_locators=['L1']); c=smi.record_outcome_feedback(o,project_id='P1',packet_hash='x',result='PASS',measurable_gain=True,evidence_locator='e1'); assert c['statement']=='keep' and c['source_ids']==['S1'] and c['evidence_locators']==['L1']
