import importlib.util
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / 'tools' / 'ivdivo_speaker_attribution.py'
spec = importlib.util.spec_from_file_location('ivdivo_speaker_attribution', MODULE_PATH)
sa = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = sa
spec.loader.exec_module(sa)

ALIASES={'JANA':['Jana'],'SMITH':['Smith'],'TINA':['Tina'],'ANDREJ':['Andrej'],'HYDRO_CONTROL':['hydro control']}
G={'JANA':'F','TINA':'F','SMITH':'M','ANDREJ':'M'}
def seg(sid,kind,text): return {'segment_id':sid,'kind':kind,'exact_text':text}

def test_pre_direct_tag():
    xs=[seg('n1','NARRATION','Jana said, '),seg('d1','DIALOGUE','“Go.”'),seg('n2','NARRATION','\n\n')]
    r=sa.classify_and_attribute(xs,ALIASES,G); assert [(x.segment_id,x.speaker,x.method) for x in r]==[('d1','JANA','PRE_DIRECT_TAG')]

def test_post_direct_same_paragraph():
    xs=[seg('n1','NARRATION',''),seg('d1','DIALOGUE','“Go.”'),seg('n2','NARRATION',' Smith said.\n\nTina moved.')]
    r=sa.classify_and_attribute(xs,ALIASES,G); assert r[0].speaker=='SMITH' and r[0].method=='POST_DIRECT_TAG'

def test_paragraph_start_not_back_attached():
    xs=[seg('n1','NARRATION',''),seg('d1','DIALOGUE','“Thirty seconds.”'),seg('n2','NARRATION','\n\nTina watched.\n\nJana said, '),seg('d2','DIALOGUE','“Header?”')]
    r=sa.classify_and_attribute(xs,ALIASES,G); assert all(x.segment_id!='d1' for x in r); assert any(x.segment_id=='d2' and x.speaker=='JANA' for x in r)

def test_pronoun_post_requires_unique_gender_antecedent():
    xs=[seg('n1','NARRATION','Jana looked at Smith. '),seg('d1','DIALOGUE','“Go.”'),seg('n2','NARRATION',' she said.')]
    r=sa.classify_and_attribute(xs,ALIASES,G); assert r[0].speaker=='JANA'

def test_pronoun_post_uses_last_nonempty_prior_paragraph():
    xs=[seg('n1','NARRATION','\n\nJana stood behind Nika.\n\n'),seg('d1','DIALOGUE','“Go.”'),seg('n2','NARRATION',' she said.\n\n')]
    r=sa.classify_and_attribute(xs,{'JANA':['Jana'],'SMITH':['Smith']},{'JANA':'F','SMITH':'M'}); assert r[0].speaker=='JANA' and r[0].method=='POST_PRONOUN_RESOLVED_REVIEW_CANDIDATE'

def test_possessive_name_counts_as_antecedent_and_can_create_ambiguity():
    xs=[seg('n1','NARRATION','Jana came to Nika’s desk.\n\n'),seg('d1','DIALOGUE','“What?”'),seg('n2','NARRATION',' she asked.')]
    aliases={'JANA':['Jana'],'NIKA':['Nika']}; genders={'JANA':'F','NIKA':'F'}
    assert sa.classify_and_attribute(xs,aliases,genders)==[]

def test_pronoun_post_conflict_fails_closed():
    xs=[seg('n1','NARRATION','Jana looked at Tina. '),seg('d1','DIALOGUE','“Go.”'),seg('n2','NARRATION',' she said.')]
    assert sa.classify_and_attribute(xs,ALIASES,G)==[]

def test_standalone_pre_paragraph_exact_review_helper():
    aps=sa.compile_aliases(ALIASES); r=sa.standalone_pre_tag('\n\nSmith answered.\n\n',aps); assert r and r[0]=='SMITH'

def test_standalone_pre_with_adverb_review_helper():
    aps=sa.compile_aliases(ALIASES); r=sa.standalone_pre_tag('\n\nHydro control answered immediately.\n\n',aps); assert r and r[0]=='HYDRO_CONTROL'

def test_non_spoken_override():
    xs=[seg('n1','NARRATION','He did not add '),seg('d1','DIALOGUE','“second hit”'),seg('n2','NARRATION',' to the instruction.')]
    assert sa.classify_and_attribute(xs,ALIASES,G,{'d1'})==[]

def test_same_paragraph_propagation():
    xs=[seg('d1','DIALOGUE','“A,”'),seg('n1','NARRATION',' Jana said. '),seg('d2','DIALOGUE','“B.”'),seg('n2','NARRATION','\n\n')]
    seed=[sa.Evidence('d1','JANA','POST_DIRECT_TAG',' Jana said')]
    r=sa.propagate_same_paragraph(xs,seed); assert len(r)==1 and r[0].segment_id=='d2' and r[0].speaker=='JANA'

def test_same_paragraph_conflicting_anchors_fail_closed():
    xs=[seg('d1','DIALOGUE','“A.”'),seg('n1','NARRATION',' x '),seg('d2','DIALOGUE','“B.”')]
    seed=[sa.Evidence('d1','JANA','M','x'),sa.Evidence('d2','SMITH','M','x')]
    assert sa.propagate_same_paragraph(xs,seed)==[]

def test_small_perfect_sample_not_promoted():
    assert not sa.rule_auto_promotable(2,2); assert not sa.rule_auto_promotable(17,17)

def test_high_precision_large_sample_can_promote():
    assert sa.rule_auto_promotable(100,100)

def test_low_precision_rejected():
    assert not sa.rule_auto_promotable(29,49); assert not sa.rule_auto_promotable(5,27)

def test_subject_tracker_prefers_grammatical_subject_over_object_name():
    aliases={'JANA':['Jana'],'NIKA':['Nika']}; genders={'JANA':'F','NIKA':'F'}
    xs=[seg('n1','NARRATION','\n\nJana stood behind Nika now, arms folded.\n\n'),seg('d1','DIALOGUE','“Walk the gallery,”'),seg('n2','NARRATION',' she said.\n\n')]
    r=sa.classify_and_attribute(xs,aliases,genders,project_pronoun_subject_tracker_promoted=True)
    assert r[0].speaker=='JANA' and r[0].method=='AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER'

def test_subject_tracker_role_gender_from_local_possessive():
    aliases={'TECH':['the technician']}; genders={}
    xs=[seg('n1','NARRATION','\n\nThe technician connected his maintenance terminal.\n\n'),seg('d1','DIALOGUE','“Cleaner.”'),seg('n2','NARRATION',' he said.\n\n')]
    r=sa.classify_and_attribute(xs,aliases,genders,project_pronoun_subject_tracker_promoted=True); assert r[0].speaker=='TECH'

def test_subject_tracker_does_not_cross_post_quote_paragraph_break():
    aliases={'SMITH':['Smith']}; genders={'SMITH':'M'}
    xs=[seg('n1','NARRATION','\n\nSmith turned back. '),seg('d1','DIALOGUE','“Field.”'),seg('n2','NARRATION','\n\nHe added a short line.')]
    assert sa.classify_and_attribute(xs,aliases,genders,project_pronoun_subject_tracker_promoted=True)==[]
