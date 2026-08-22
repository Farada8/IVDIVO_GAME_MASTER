import unittest
from engine.business_design_engine import *

class T(unittest.TestCase):
    def test01_source_planned(self): self.assertEqual(source_state(False),"PLANNED_NOT_CONFIRMED_UPLOADED")
    def test02_source_raw(self): self.assertEqual(source_state(True),"CONFIRMED_RAW")
    def test03_source_quarantine(self): self.assertEqual(source_state(False,False,True),"QUARANTINED")
    def test04_site_summary_missing(self):
        self.assertEqual(site_context_gate({"site_id":"x","source_role":"EARLY_BRIEF"})["status"],"INSUFFICIENT_SOURCE_NOT_PROJECT_DEFECT")
    def test05_site_ready(self):
        p={"site_id":"x","location":"Galway","site_type":"wall","dimensions_state":"CONFIRMED","ownership_or_access_state":"PERMISSION_PENDING","climate_exposure":"COASTAL","heritage_state":"NOT_LISTED_CONFIRMED","public_access":"PUBLIC","stakeholders":["owner"],"source_role":"SITE_SURVEY"}
        self.assertEqual(site_context_gate(p)["status"],"SITE_CONTEXT_READY")
    def test06_brief_ready(self):
        p={"objective":"o","users":["u"],"site_ref":"s","programme":["p"],"constraints":["c"],"deliverables":["d"],"exclusions":["e"],"unknowns":[]}
        self.assertEqual(design_brief_gate(p)["status"],"BRIEF_READY")
    def test07_composition_flat(self):
        p={"dominant":"same","subordinate":"same","focal_path":"x","value_structure":"x","distance":"x"}
        self.assertEqual(composition_gate(p)["status"],"FLAT_HIERARCHY_RISK")
    def test08_readability_unknown(self): self.assertEqual(distance_readability({})["status"],"DISTANCE_DATA_REQUIRED")
    def test09_readability_proxy(self): self.assertEqual(distance_readability({"distance_m":10,"critical_feature_size_mm":30})["status"],"READABILITY_PROXY_PASS")
    def test10_prompt_protects_unknown(self):
        r=prompt_compile({"objective":"mural","protected_unknowns":["exact_dimensions"]})
        self.assertIn("DO_NOT_INVENT:exact_dimensions",r["prompt"])
    def test11_mural_missing(self): self.assertEqual(mural_surface_gate({"substrate":"render","source_role":"TECHNICAL_SURVEY"})["status"],"MISSING_REQUIRED_PROJECT_DATA")
    def test12_mural_moisture_hold(self):
        p={"substrate":"render","moisture_state":"UNRESOLVED","uv_exposure":"HIGH","wind_exposure":"HIGH","prep_system":"mineral-compatible prep","access_method":"scaffold","coating_system":"specified exterior system","maintenance_plan":"annual inspection","source_role":"TECHNICAL_SURVEY"}
        self.assertEqual(mural_surface_gate(p)["status"],"MURAL_TECHNICAL_HOLD")
    def test13_sculpture_structural_hold(self):
        p={"material":"steel","height_or_mass_state":"ESTIMATE","foundation_state":"concept defined","structural_review_state":"NOT_RUN","public_contact":True,"maintenance_plan":"annual inspection","source_role":"TECHNICAL_SURVEY"}
        self.assertEqual(sculpture_gate(p)["status"],"STRUCTURAL_REVIEW_REQUIRED")
    def test14_hospitality_conflict(self):
        p={"guest_path":["door","corridor"],"service_path":["yard","corridor"],"delivery_path":["yard"],"waste_path":["yard"],"accessible_path":["door","corridor"],"capacity_state":"KNOWN"}
        self.assertEqual(hospitality_flow(p)["status"],"FLOW_CONFLICT")
    def test15_hospitality_shared_allowed(self):
        p={"guest_path":["door","corridor"],"service_path":["yard","corridor"],"delivery_path":["yard"],"waste_path":["yard"],"accessible_path":["door","corridor"],"capacity_state":"KNOWN","shared_allowed":["corridor"]}
        self.assertEqual(hospitality_flow(p)["status"],"FLOW_READY")
    def test16_material_lifecycle(self):
        p={"material":"mosaic","environment":"exterior","maintenance_interval":"annual","replacement_method":"local repair","failure_modes":["grout loss"]}
        self.assertEqual(material_lifecycle(p)["status"],"LIFECYCLE_REGISTERED")
    def test17_buildability_missing(self): self.assertEqual(buildability_gate({"fabrication":"shop","source_role":"TECHNICAL_PACKAGE"})["status"],"MISSING_REQUIRED_PROJECT_DATA")
    def test18_buildability_ready(self):
        p={"fabrication":"shop","transport":"van","site_access":"scaffold","installation":"bolted","inspection":"engineer","maintenance_access":"MEWP"}
        self.assertEqual(buildability_gate(p)["status"],"BUILDABILITY_READY_FOR_SPECIALIST_REVIEW")
    def test19_cost_missing(self): self.assertEqual(cost_band({"quantity_basis":10})["status"],"MISSING_REQUIRED_PROJECT_DATA")
    def test20_cost_range(self):
        r=cost_band({"quantity_basis":10,"unit_cost_low":100,"unit_cost_high":200,"contingency_pct":10})
        self.assertEqual((r["low"],r["high"]),(1100.0,2200.0))
    def test21_commission_map(self):
        p={"buyer_class":"hotel","procurement_route":"direct","approval_chain":["owner"],"required_evidence":["site","cost"]}
        self.assertFalse(commission_route(p)["buyer_intent_claimed"])
    def test22_public_signal_no_launder(self): self.assertEqual(public_signal_gate({"e_grade":"E4","direct_buyer_or_money_evidence":False})["status"],"EVIDENCE_LAUNDERING_BLOCKED")
    def test23_public_signal_e2(self): self.assertEqual(public_signal_gate({"e_grade":"E2","direct_buyer_or_money_evidence":False})["status"],"PUBLIC_SIGNAL_ACCEPTED")
    def test24_offer_ready(self):
        p={"scope":"concept","deliverables":["render"],"assumptions":["site TBD"],"exclusions":["engineering"],"price_basis_state":"RANGE","evidence_state":"E2"}
        self.assertEqual(offer_package(p)["status"],"OFFER_READY_FOR_REVIEW")
    def test25_redteam_site_fatal(self): self.assertEqual(red_team({"site_authority":False})["status"],"NO_GO")
    def test26_redteam_fake_cost(self):
        r=red_team({"site_authority":True,"cost_point_estimate":1000,"maintenance_path":True})
        self.assertIn("FAKE_COST_PRECISION",r["major"])
    def test27_redteam_buyer_overclaim(self):
        r=red_team({"site_authority":True,"buyer_demand_claimed":True,"buyer_evidence":False,"maintenance_path":True})
        self.assertIn("BUYER_EVIDENCE_MISSING",r["major"])
    def test28_redteam_pass(self):
        r=red_team({"site_authority":True,"technical_maturity_claimed":False,"buyer_demand_claimed":False,"maintenance_path":True})
        self.assertEqual(r["status"],"PASS_WITH_WATCHES")
    def test29_si_capture_only(self):
        p={"project_id":"p","defect_or_success":"x","root_cause":"y","evidence_ref":"z","repeat_count":1,"proposed_mechanism":"m"}
        self.assertEqual(self_improvement_observation(p)["status"],"CAPTURE_ONLY_NOT_ENGINE_CANDIDATE")
    def test30_si_candidate(self):
        p={"project_id":"p","defect_or_success":"x","root_cause":"y","evidence_ref":"z","repeat_count":2,"proposed_mechanism":"m"}
        self.assertEqual(self_improvement_observation(p)["status"],"CANDIDATE_FOR_SELF_IMPROVEMENT_REVIEW")
    def test31_si_no_auto_promote(self):
        p={"project_id":"p","defect_or_success":"x","root_cause":"y","evidence_ref":"z","repeat_count":2,"proposed_mechanism":"m"}
        self.assertFalse(self_improvement_observation(p)["auto_promote"])
    def test32_unknown_cost_not_zero(self): self.assertNotEqual(cost_band({"quantity_basis":0})["status"],"ASSUMPTION_BANDED_COST")

if __name__=="__main__": unittest.main()
