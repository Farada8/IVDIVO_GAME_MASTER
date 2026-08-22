import sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from engine.applicant_fit_guard import *

class T(unittest.TestCase):
    def test_01_cluain_empty_holds(self):
        self.assertEqual(cluain_gate([])["status"],"HOLD_THREE_PROJECT_RECORDS")
    def test_02_cluain_three_complete(self):
        r={"context":"x","timeframe":"2019","overall_budget":1000,"photo_refs":["x"],"applicant_role":"artist","delivery_context":True}
        self.assertEqual(cluain_gate([r,r,r])["status"],"PASS_THREE_PROJECT_EVIDENCE")
    def test_03_cluain_missing_budget_holds(self):
        r={"context":"x","timeframe":"2019","overall_budget":None,"photo_refs":["x"],"applicant_role":"artist","delivery_context":True}
        self.assertEqual(cluain_gate([r,r,r])["ready"],0)
    def test_04_inis_complete(self):
        self.assertEqual(inis_gate(6,True,True,True,True,True)["status"],"READY_FOR_FINAL_RED_TEAM")
    def test_05_inis_concept_required(self):
        self.assertIn("CONCEPT",inis_gate(6,True,False,True,True,True)["blockers"])
    def test_06_inis_image_limit(self):
        self.assertIn("IMAGE_LIMIT",inis_gate(11,True,True,True,True,True)["blockers"])
    def test_07_inis_previous_images_do_not_require_historical_budget(self):
        self.assertFalse(inis_gate(6,True,False,False,False,False)["past_project_budget_required_for_previous_images"])
    def test_08_route_is_not_win_probability(self):
        self.assertEqual(route(cluain_gate([]),inis_gate(6,True,False,False,False,False)),"INIS_EVIDENCE_BURDEN_LOWER")

if __name__=="__main__": unittest.main(verbosity=2)
