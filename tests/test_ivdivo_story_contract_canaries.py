import unittest
from tools.ivdivo_story_contract_canaries import *

class StoryContractCanaries(unittest.TestCase):
    def core(self): return dict(hero='H',want='W',why_now='N',opposition='O',wrong_strategy='S',price='P',midpoint='M',climax_choice='C',resolution='R',series_hook_status='AFTER_CLOSURE')
    def test_approval(self):
        self.assertEqual(approval_event_gate({'type':'FOUNDER_LOCK','target':'D01'},{'type':'RESUME','target':'D01','authority_source':'chat'}),'APPROVAL_EVENT_MISSING'); self.assertEqual(approval_event_gate({'type':'FOUNDER_LOCK','target':'D01'},{'type':'FOUNDER_LOCK','target':'D01','authority_source':'founder'}),'PASS')
    def test_story_core(self):
        self.assertEqual(story_core_gate(self.core())['status'],'STORY_CORE_READY'); d=self.core(); d['midpoint']='UNKNOWN'; self.assertEqual(story_core_gate(d)['status'],'PROSE_NO_GO')
    def test_character_unknown(self): self.assertEqual(character_continuity_gate('CANON'),'USE'); self.assertEqual(character_continuity_gate('OPTION'),'OPTION_ONLY'); self.assertEqual(character_continuity_gate('UNKNOWN'),'UNKNOWN_HOLD')
    def test_ordinary_life(self): self.assertEqual(ordinary_life_pressure_gate([]),'COMPETENCE_ONLY_RISK'); self.assertEqual(ordinary_life_pressure_gate([{'present':1}]),'CHECKLIST_EXPOSITION_RISK'); self.assertEqual(ordinary_life_pressure_gate([{'present':1,'causal_pressure':1,'choice_or_price':1}]),'FUNCTIONAL_COVERAGE')
    def test_opposition(self): self.assertEqual(opposition_legitimacy_gate({'goal':'x'}),'CARDBOARD_OPPOSITION'); self.assertEqual(opposition_legitimacy_gate(dict(goal=1,competence=1,legitimate_interest=1,cost_of_yielding=1)),'LEGITIMATE_RESISTANCE')
    def test_wrong_strategy(self): self.assertEqual(wrong_strategy_gate(dict(strategy=1,action=1,resistance=1,consequence=1,price=1,deletion_changes_chain=0)),'DECORATIVE_FLAW'); self.assertEqual(wrong_strategy_gate(dict(strategy=1,action=1,resistance=1,consequence=1,price=1,deletion_changes_chain=1)),'CAUSALLY_PROVEN')
    def test_midpoint(self): self.assertEqual(midpoint_gate(dict(earned_evidence=1,pre_model='a',post_model='a',strategy_delta=1)),'ESCALATION_ONLY'); self.assertEqual(midpoint_gate(dict(earned_evidence=1,pre_model='a',post_model='b',strategy_delta=1)),'MIDPOINT_RECLASSIFICATION')
    def test_climax(self): self.assertEqual(climax_ownership_gate(dict(protagonist_choice=1,pressure=1,price=1,resolution_dependency=0)),'PASSIVE_CLIMAX'); self.assertEqual(climax_ownership_gate(dict(protagonist_choice=1,pressure=1,price=1,resolution_dependency=1)),'OWNED_CLIMAX')
    def test_resolution_hook(self): self.assertEqual(resolution_hook_gate(False,True),'HOOK_QUARANTINED'); self.assertEqual(resolution_hook_gate(True,True),'CLOSED_THEN_HOOK')
    def test_scene(self): self.assertEqual(scene_state_change_gate(dict(who=1,want=1,why_now=1,resistance=1,start_state='a',end_state='a')),'CUT_COMPRESS_REDESIGN'); self.assertEqual(scene_state_change_gate(dict(who=1,want=1,why_now=1,resistance=1,start_state='a',end_state='b')),'SCENE_EARNS_EXISTENCE')
    def test_dialogue(self): self.assertEqual(dialogue_action_gate(dict(objective=1,resistance=0)),'INFO_EXCHANGE_RISK'); self.assertEqual(dialogue_action_gate(dict(objective=1,resistance=1,listening_reaction=1,change=1)),'DIALOGUE_ACTION')
    def test_voice(self): self.assertEqual(voice_separation_gate({'a':{'question_style':'q'},'b':{'question_style':'q'}}),'COLLISION_WATCH'); self.assertEqual(voice_separation_gate({'a':{'question_style':'q1'},'b':{'question_style':'q2'}}),'SEPARATED')
    def test_world(self): self.assertEqual(world_through_life_gate({'lived_domain':'lecture','plot_pressure':1}),'LORE_ONLY_RISK'); self.assertEqual(world_through_life_gate({'lived_domain':'job','plot_pressure':1}),'EARNED_WORLD_REVEAL')
    def test_institutions(self):
        r=dict(jurisdiction='x',knowledge='y',incentive='z',constraint='c',internal_disagreement='d'); self.assertEqual(institution_differentiation_gate([r,r.copy()]),'MORALIZED_DUPLICATE')
    def test_jurisdiction(self): self.assertEqual(knowledge_jurisdiction_gate('SCIENCE','NONE','ADVICE'),'ADVISORY_ONLY'); self.assertEqual(knowledge_jurisdiction_gate('SCIENCE','NONE','COMMAND'),'OVERREACH'); self.assertEqual(knowledge_jurisdiction_gate('SCIENCE','LOCAL','COMMAND',True),'AUTHORIZED')
    def test_mystery(self):
        c=dict(source='s',observation='o',interpretation='i',confidence=.7,alternatives=['a'],disclosure_time=5,non_proof='n'); self.assertEqual(mystery_epistemic_gate(c),'FAIR_CLUE_RECORD'); c['evidence_available_time']=6; self.assertEqual(mystery_epistemic_gate(c),'RETROACTIVE_EVIDENCE_RISK')
    def test_reference(self): self.assertEqual(reference_firewall_gate({'distinctive_sequence':1}),'COPY_RISK'); self.assertEqual(reference_firewall_gate({'abstract_mechanism':'pressure','transformed_application':'new'}),'SAFE_TRANSFORM')
    def test_cross_ai(self): self.assertEqual(cross_ai_evidence_dedupe([{'root_source':'x'},{'root_source':'x'},{'root_source':'y'}])['evidence_families'],2)
    def test_evidence(self): self.assertEqual(evidence_class_gate('HUMAN','MODEL'),'EVIDENCE_CLASS_MISMATCH')
    def test_human_signal(self): self.assertEqual(human_signal_gate(None,True),'HOLD_REAL_HUMAN'); self.assertEqual(human_signal_gate('r',True),'HUMAN_SIGNAL_AVAILABLE')
    def test_metric(self): self.assertEqual(metric_gate(None,False),'UNKNOWN_NULL'); self.assertEqual(metric_gate(0,False),'FAIL_FALSE_ZERO'); self.assertEqual(metric_gate(0,True,'src'),'MEASURED_ZERO')
    def test_persistence(self): self.assertEqual(persistence_closure_gate({'github_write':1}),'SYNC_PENDING'); self.assertEqual(persistence_closure_gate({k:1 for k in ('github_write','drive_write','github_readback','drive_readback','pointer_reconciled','stale_scan','final_readback')}),'PERSISTENCE_CLOSURE_PASS')
    def test_concurrency(self): self.assertEqual(concurrent_delta_gate(True,False,True),'REBASE_SALVAGE'); self.assertEqual(concurrent_delta_gate(True,True,True),'FRONTIER_CONFLICT')
    def test_registry(self): self.assertEqual(registry_id_gate('SI-0015',['SI-0015'],[]),'COLLISION'); self.assertEqual(registry_id_gate('SI-0020',[],[],False),'PARTIAL_VISIBILITY_HOLD')
    def test_promotion(self): self.assertEqual(promotion_tribunal({'contract':1,'canary':1,'requested_scope':'UNIVERSAL'}),'HOLD'); self.assertEqual(promotion_tribunal({'contract':1,'canary':1,'project_pilot':1,'requested_scope':'UNIVERSAL'}),'ACCEPT_WITH_SCOPE')
    def test_engine(self): self.assertEqual(engine_worthiness_gate({'semantic_duplicate':1}),'REJECT_DUPLICATE'); self.assertEqual(engine_worthiness_gate({'recurrent':1,'state_need':1,'coordination_need':1}),'BUILD')
    def test_audio(self): self.assertEqual(story_to_audio_handoff_gate({'story_lock':1}),'SOURCE_HOLD'); self.assertEqual(story_to_audio_handoff_gate({'story_lock':1,'source_version':'v','source_hash':'h','text_protection':1}),'AUDIO_INGEST_READY')
    def test_governor(self): self.assertEqual(portfolio_governor([{'id':'meta','admissible':1,'authority_priority':1,'dependency_priority':1,'information_value':9},{'id':'founder','admissible':1,'authority_priority':3,'dependency_priority':3,'information_value':5}]),'founder')

if __name__=='__main__': unittest.main()
