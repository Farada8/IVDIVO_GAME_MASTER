import unittest
from story_adapters import *

class T(unittest.TestCase):
 def test01(self):self.assertEqual(source_adequacy(['hero','midpoint'],{'hero':'x'},'ROUTING_STATE')['status'],'INSUFFICIENT_SOURCE_NOT_STORY_DEFECT')
 def test02(self):self.assertEqual(story_core_compiler({k:'x' for k in STORY_CORE_FIELDS},'STORY_CORE')['status'],'STORY_CORE_READY')
 def test03(self):self.assertEqual(story_core_compiler({'hero':'x'},'STORY_CORE')['status'],'MISSING_REQUIRED_STORY_DATA')
 def test04(self):self.assertEqual(character_continuity_unknown_gate('CANON','MANUSCRIPT_DEPENDENCY',True)['status'],'USE')
 def test05(self):self.assertEqual(character_continuity_unknown_gate('WORKING_OPTION','MANUSCRIPT_DEPENDENCY',True)['status'],'FOUNDER_DECISION_REQUIRED')
 def test06(self):self.assertEqual(character_continuity_unknown_gate('OPTION','REFERENCE_ONLY',True)['status'],'OPTION_ONLY')
 def test07(self):self.assertEqual(ordinary_life_pressure_coverage({'major_character':'A','ordinary_life_domains':['work'],'plot_pressure_links':['money blocks choice']},'CHARACTER_BIBLE')['status'],'FUNCTIONAL_COVERAGE')
 def test08(self):self.assertEqual(ordinary_life_pressure_coverage({'major_character':'A'},'ROUTING_STATE')['status'],'INSUFFICIENT_SOURCE_NOT_STORY_DEFECT')
 def test09(self):self.assertEqual(opposition_legitimacy_matrix({'opponent_goal':'g','evidence':'e','competence':True,'legitimate_interest':'l','cost_of_yielding':'c','right_domain':'r'},'ARCHITECTURE')['status'],'LEGITIMATE_RESISTANCE')
 def test10(self):self.assertEqual(wrong_strategy_causality_proof({'hero_strategy':'s','actions':['a'],'resistance':['r'],'consequences':['c'],'price':'p','deletion_changes_chain':True},'ARCHITECTURE')['status'],'CAUSALLY_PROVEN')
 def test11(self):self.assertEqual(wrong_strategy_causality_proof({'hero_strategy':'s','actions':['a'],'resistance':['r'],'consequences':['c'],'price':'p','deletion_changes_chain':False},'ARCHITECTURE')['status'],'DECORATIVE_FLAW')
 def test12(self):self.assertEqual(midpoint_reclassification_validator({'pre_midpoint_model':'A','evidence_event':'E','post_midpoint_model':'B','strategy_delta':'S','stakes_delta':'T'},'ARCHITECTURE')['status'],'MIDPOINT_RECLASSIFICATION')
 def test13(self):self.assertEqual(midpoint_reclassification_validator({'pre_midpoint_model':'A','evidence_event':'E','post_midpoint_model':'A','strategy_delta':[],'stakes_delta':'T'},'ARCHITECTURE')['status'],'ESCALATION_ONLY')
 def test14(self):self.assertEqual(climax_ownership_gate({'protagonist_choice':'x','pressure':'p','price':'cost','resolution_dependency':True,'ensemble_mode':False},'ARCHITECTURE')['status'],'OWNED_CLIMAX')
 def test15(self):self.assertEqual(resolution_closure_hook_quarantine(True,False,False)['status'],'CLOSED_NO_HOOK')
 def test16(self):self.assertEqual(resolution_closure_hook_quarantine(True,True,False)['status'],'CLOSED_THEN_HOOK')
 def test17(self):self.assertEqual(resolution_closure_hook_quarantine(False,True,False)['status'],'HOOK_QUARANTINED')
 def test18(self):self.assertEqual(world_through_life_validator({'world_fact':'f','delivery_scene':'s','lived_domain':'job','plot_pressure':'deadline'},'SCENE')['status'],'EARNED_WORLD_REVEAL')
 def test19(self):
  rows=[{'jurisdiction':'A','knowledge':'A','incentives':'A','constraints':'A'},{'jurisdiction':'B','knowledge':'B','incentives':'B','constraints':'B'}]
  x={'institutions':rows,'jurisdiction':'x','knowledge':'x','incentives':'x','successes':'x','crimes':'x','constraints':'x','internal_disagreement':'x'}
  self.assertEqual(institutional_conflict_differentiator(x,'WORLD_BIBLE')['status'],'DIFFERENTIATED')
 def test20(self):self.assertEqual(knowledge_jurisdiction_separation_gate('science',None,'COMMAND',False)['status'],'OVERREACH')
 def test21(self):self.assertEqual(knowledge_jurisdiction_separation_gate('science',None,'ADVICE',False)['status'],'ADVISORY_ONLY')
 def test22(self):self.assertEqual(mystery_epistemic_ladder({'clue_source':'s','observation':'o','interpretation':'i','confidence':'LOW','alternatives':['a'],'disclosure_time':'t','non_proof':['not guilt']},'CLUE_LEDGER')['status'],'FAIR_CLUE_RECORD')
 def test23(self):self.assertEqual(mystery_epistemic_ladder({'clue_source':'s','observation':'o','interpretation':'i','confidence':'LOW','alternatives':['a'],'disclosure_time':'t','non_proof':['n'],'retroactive_unavailable_evidence':True},'CLUE_LEDGER')['status'],'RETROACTIVE_EVIDENCE_RISK')
 def test24(self):self.assertEqual(mystery_epistemic_ladder({'clue_source':'s'},'ROUTING_STATE')['status'],'INSUFFICIENT_SOURCE_NOT_STORY_DEFECT')

if __name__=='__main__':unittest.main()
