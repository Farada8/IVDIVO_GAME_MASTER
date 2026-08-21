import importlib.util
import pathlib
import unittest

from tools.ivdivo_story_crossdomain_guards import *

ROOT=pathlib.Path(__file__).resolve().parents[1]
PILOT=ROOT/'SELF_IMPROVEMENT_STUDIO'/'2026-08-21_CYCLE8_STORY_ADAPTER_REAL_PILOT'/'story_adapters.py'
spec=importlib.util.spec_from_file_location('story_adapters',PILOT)
story=importlib.util.module_from_spec(spec)
spec.loader.exec_module(story)

class IntegratedStoryContracts(unittest.TestCase):
    def test_source_adequacy(self): self.assertEqual(story.story_core_compiler({},'ROUTING_STATE')['status'],'INSUFFICIENT_SOURCE_NOT_STORY_DEFECT')
    def test_character_unknown(self): self.assertEqual(story.character_continuity_unknown_gate('WORKING','MANUSCRIPT_DEPENDENCY',True)['status'],'FOUNDER_DECISION_REQUIRED')
    def test_resolution(self): self.assertEqual(story.resolution_closure_hook_quarantine(True,True,False)['status'],'CLOSED_THEN_HOOK')
    def test_jurisdiction(self): self.assertEqual(story.knowledge_jurisdiction_separation_gate('SCIENCE',None,'COMMAND')['status'],'OVERREACH')
    def test_approval(self): self.assertEqual(approval_event_gate({'type':'FOUNDER_LOCK','target':'D01'},{'type':'RESUME','target':'D01','authority_source':'chat'}),'APPROVAL_EVENT_MISSING')
    def test_scene(self): self.assertEqual(scene_state_change_gate(dict(who=1,want=1,why_now=1,resistance=1,start_state='a',end_state='b')),'SCENE_EARNS_EXISTENCE')
    def test_dialogue(self): self.assertEqual(dialogue_action_gate(dict(objective=1,resistance=1,listening_reaction=1,change=1)),'DIALOGUE_ACTION')
    def test_voice(self): self.assertEqual(voice_separation_gate({'a':{'question_style':'x'},'b':{'question_style':'x'}}),'COLLISION_WATCH')
    def test_reference(self): self.assertEqual(reference_firewall_gate({'distinctive_sequence':1}),'COPY_RISK')
    def test_cross_ai(self): self.assertEqual(cross_ai_evidence_dedupe([{'root_source':'x'},{'root_source':'x'}])['evidence_families'],1)
    def test_evidence(self): self.assertEqual(evidence_class_gate('HUMAN','MODEL'),'EVIDENCE_CLASS_MISMATCH')
    def test_human(self): self.assertEqual(human_signal_gate(None,True),'HOLD_REAL_HUMAN')
    def test_metric(self): self.assertEqual(metric_gate(0,False),'FAIL_FALSE_ZERO')
    def test_persistence(self): self.assertEqual(persistence_closure_gate({'github_write':1}),'SYNC_PENDING')
    def test_concurrency(self): self.assertEqual(concurrent_delta_gate(True,False,True),'REBASE_SALVAGE')
    def test_registry(self): self.assertEqual(registry_id_gate('SI-0015',['SI-0015'],[]),'COLLISION')
    def test_promotion(self): self.assertEqual(promotion_tribunal({'contract':1,'canary':1,'project_pilot':1,'requested_scope':'UNIVERSAL'}),'ACCEPT_WITH_SCOPE')
    def test_engine(self): self.assertEqual(engine_worthiness_gate({'semantic_duplicate':1}),'REJECT_DUPLICATE')
    def test_audio(self): self.assertEqual(story_to_audio_handoff_gate({'story_lock':1}),'SOURCE_HOLD')
    def test_governor(self): self.assertEqual(portfolio_governor([{'id':'meta','admissible':1,'authority_priority':1},{'id':'founder','admissible':1,'authority_priority':3}]),'founder')

if __name__=='__main__': unittest.main()
