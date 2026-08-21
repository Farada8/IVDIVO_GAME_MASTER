import unittest
from hashlib import sha256
from wave4_studio_intelligence import *

TEXT = "Locked exact text."
TH = sha256(TEXT.encode()).hexdigest()

class BenchmarkTests(unittest.TestCase):
    def variants(self, hashes=True):
        return [
            {"mode":m, "exact_text_hash":TH, "render_asset_hash": (m+"hash" if hashes else None)}
            for m in AUDIO_MODES
        ]
    def test_manifest_complete(self):
        x=build_benchmark_manifest(source_id="S", source_hash="H", exact_text=TEXT, variants=self.variants())
        self.assertEqual(x["status"],"READY_FOR_RENDER_EVIDENCE")
    def test_manifest_hold_without_render(self):
        x=build_benchmark_manifest(source_id="S", source_hash="H", exact_text=TEXT, variants=self.variants(False))
        self.assertEqual(x["status"],"HOLD_FOR_RENDER_EVIDENCE")
    def test_manifest_rejects_missing_mode(self):
        with self.assertRaises(ValueError): build_benchmark_manifest(source_id="S",source_hash="H",exact_text=TEXT,variants=self.variants()[:2])
    def test_manifest_rejects_text_drift(self):
        v=self.variants(); v[0]["exact_text_hash"]="bad"
        with self.assertRaises(ValueError): build_benchmark_manifest(source_id="S",source_hash="H",exact_text=TEXT,variants=v)
    def test_score_complete(self):
        x=score_benchmark_variant(mode="NARRATED",human_scores={"believability":4,"clarity":4,"want_more":3,"fatigue_resistance":5},cost={"provider_cost":1,"manual_cost":1},duration_seconds=120)
        self.assertEqual(x["status"],"PASS_EVIDENCE_COMPLETE")
    def test_score_holds_missing_human(self):
        x=score_benchmark_variant(mode="NARRATED",human_scores={},cost={"provider_cost":1,"manual_cost":1},duration_seconds=120)
        self.assertEqual(x["status"],"HOLD_HUMAN_SCORES")
    def test_score_holds_missing_cost(self):
        x=score_benchmark_variant(mode="NARRATED",human_scores={"believability":4,"clarity":4,"want_more":3,"fatigue_resistance":5},cost={"provider_cost":None,"manual_cost":1},duration_seconds=120)
        self.assertEqual(x["status"],"HOLD_COST_EVIDENCE")
    def test_compare_holds_blocked(self):
        s=[{"mode":m,"status":"HOLD","composite":None} for m in AUDIO_MODES]
        self.assertEqual(compare_benchmark(s)["status"],"HOLD")

class DirectorTests(unittest.TestCase):
    def scene(self):
        return {"scene_id":"SC1","source_text_hash":"H","spoken_units":[
            {"unit_id":"U1","objective":"get an answer","listener_state":"LISTENING","mic_perspective":"CLOSE"},
            {"unit_id":"U2","objective":"hide fear","listener_state":"HESITATION","mic_perspective":"NORMAL"},
        ],"declared_events":[
            {"kind":"FOLEY","anchor_unit_id":"U1","source_fact_id":"PROP_PHONE","function":"OBJECT_ACTION","instruction":"phone set down"},
            {"kind":"AMBIENCE","anchor_unit_id":"U1","function":"LOCATION","instruction":"room tone"},
            {"kind":"SILENCE","anchor_unit_id":"U2","function":"PROTECTED_WAIT","instruction":"do not fill"},
        ]}
    def test_compile(self):
        x=compile_automatic_director(self.scene()); self.assertFalse(x["story_mutation"]); self.assertGreater(len(x["cues"]),3)
    def test_validate(self):
        self.assertEqual(validate_director_score(compile_automatic_director(self.scene()))["status"],"PASS")
    def test_no_absolute_time(self):
        x=compile_automatic_director(self.scene()); self.assertTrue(all(c["absolute_time_seconds"] is None for c in x["cues"]))
    def test_unknown_event_anchor(self):
        s=self.scene(); s["declared_events"][0]["anchor_unit_id"]="BAD"
        with self.assertRaises(ValueError): compile_automatic_director(s)
    def test_foley_requires_source_fact(self):
        s=self.scene(); s["declared_events"][0].pop("source_fact_id")
        with self.assertRaises(ValueError): compile_automatic_director(s)
    def test_invalid_mic(self):
        s=self.scene(); s["spoken_units"][0]["mic_perspective"]="MAGIC"
        with self.assertRaises(ValueError): compile_automatic_director(s)
    def test_duplicate_units(self):
        s=self.scene(); s["spoken_units"][1]["unit_id"]="U1"
        with self.assertRaises(ValueError): compile_automatic_director(s)

class PerformanceTests(unittest.TestCase):
    def test_hold(self):
        x=performance_intelligence(PerformanceEvidence("C","R")); self.assertEqual(x["lock_status"],"HOLD")
    def test_eligible(self):
        e=PerformanceEvidence("C","R",True,True,True,True,True,["PAUSE_REGULARITY"],{"believability":4})
        x=performance_intelligence(e,pair_required=True); self.assertEqual(x["lock_status"],"PROVISIONAL_PILOT_LOCK_ELIGIBLE")
    def test_machine_never_locks(self):
        e=PerformanceEvidence("C","R",True,True,True,True,True)
        self.assertFalse(performance_intelligence(e,pair_required=True)["machine_may_auto_lock"])
    def test_pair_required(self):
        e=PerformanceEvidence("C","R",True,True,True,True,None)
        self.assertIn("pair",performance_intelligence(e,pair_required=True)["missing_evidence"])
    def test_compare_candidate_recommendation_only(self):
        e1=PerformanceEvidence("C1","R",True,True,True,True,True,human_scores={"believability":4.0,"direction":4.0})
        e2=PerformanceEvidence("C2","R",True,True,True,True,True,human_scores={"believability":3.0,"direction":3.5})
        rows=[performance_intelligence(e1,pair_required=True),performance_intelligence(e2,pair_required=True)]
        x=compare_cast_candidates(rows); self.assertEqual(x["winner"],"C1"); self.assertFalse(x["auto_lock"])
    def test_compare_candidate_holds_without_eligible(self):
        self.assertEqual(compare_cast_candidates([performance_intelligence(PerformanceEvidence("C","R"))])["status"],"HOLD")

class ReviewCompressorTests(unittest.TestCase):
    def flags(self): return [
        {"id":"a","start":10,"end":20,"severity":"MAJOR","confidence":0.9},
        {"id":"b","start":30,"end":35,"severity":"MINOR","confidence":0.7},
        {"id":"c","start":50,"end":55,"severity":"FATAL","confidence":0.8},
    ]
    def test_selects_fatal(self):
        x=compress_human_review(self.flags(),total_duration_seconds=600,max_fraction=.05,min_seconds=10)
        self.assertIn("c",[i["id"] for i in x["selected"]])
    def test_no_release_clear(self):
        x=compress_human_review(self.flags(),total_duration_seconds=600)
        self.assertFalse(x["machine_may_clear_release"])
    def test_final_full_listen_required(self):
        x=compress_human_review(self.flags(),total_duration_seconds=600)
        self.assertTrue(x["full_listen_still_required_for_final_blind_acceptance"])
    def test_invalid_interval(self):
        with self.assertRaises(ValueError): compress_human_review([{"start":2,"end":1}],total_duration_seconds=10)

class EconomicsTests(unittest.TestCase):
    def good(self):
        return [EconomicsRecord("r1","NARRATED",120,100,2,10,30,20,10)]
    def test_complete(self):
        x=economics_report(self.good()); self.assertEqual(x["status"],"PASS_EVIDENCE_COMPLETE")
    def test_missing_evidence(self):
        r=EconomicsRecord("r","NARRATED",60,60,None,5,30)
        self.assertEqual(economics_report([r])["status"],"HOLD_MISSING_EVIDENCE")
    def test_unknown_mode(self):
        with self.assertRaises(ValueError): economics_report([EconomicsRecord("r","BAD",60,60,1,1,1)])
    def test_no_accepted(self):
        with self.assertRaises(ValueError): economics_report([EconomicsRecord("r","NARRATED",60,0,1,1,1)])
    def test_acceptance_yield(self):
        self.assertEqual(economics_report(self.good())["acceptance_yield"],round(100/120,4))

class RepairAndReleaseTests(unittest.TestCase):
    def test_selective_repair(self):
        x=selective_repair_plan([{"defect_id":"D1","earliest_layer":"PRONUNCIATION","asset_id":"RB1"}],{"RB1":["MIX1","MASTER"]})
        self.assertFalse(x["actions"][0]["full_chapter_rerender"])
    def test_repair_no_story_rewrite(self):
        x=selective_repair_plan([{"defect_id":"D1","earliest_layer":"MIX","asset_id":"SFX1"}],{})
        self.assertFalse(x["actions"][0]["rewrite_story"])
    def test_release_hold_without_live(self):
        p=[{"lock_status":"PROVISIONAL_PILOT_LOCK_ELIGIBLE"}]
        x=studio_release_gate(benchmark={"status":"PASS"},performance=p,economics={"status":"PASS_EVIDENCE_COMPLETE"},blind_human_review=True,live_provider_evidence=False)
        self.assertEqual(x["status"],"HOLD")
    def test_release_go(self):
        p=[{"lock_status":"PROVISIONAL_PILOT_LOCK_ELIGIBLE"}]
        x=studio_release_gate(benchmark={"status":"PASS"},performance=p,economics={"status":"PASS_EVIDENCE_COMPLETE"},blind_human_review=True,live_provider_evidence=True)
        self.assertEqual(x["status"],"GO_STUDIO_V1")
    def test_machine_no_override(self):
        x=studio_release_gate(benchmark={"status":"HOLD"},performance=[],economics={"status":"HOLD"},blind_human_review=False,live_provider_evidence=False)
        self.assertFalse(x["machine_may_override"])

if __name__ == '__main__':
    unittest.main(verbosity=2)
