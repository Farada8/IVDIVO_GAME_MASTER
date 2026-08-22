import unittest

from AUDIO_PRODUCTION.ROOM917.RU_PILOT.tools.compile_ru_selective_repair_plan import compile_plan


class SelectiveRepairCompilerTests(unittest.TestCase):
    def base_result(self):
        return {
            "episode": "E01",
            "locale": "ru-RU",
            "source_identity": {"identity_status": "VERIFIED"},
            "blind_listen": {"pass_a_notes_frozen": True},
            "defects": [],
        }

    def defect(self, **kw):
        row = {
            "defect_id": "D1",
            "start_seconds": 10.0,
            "end_seconds": 12.0,
            "question_class": "ACTOR_BELIEF",
            "severity": "MAJOR",
            "confidence": "HIGH",
            "heard": "actor sounds synthetic",
            "scene_failure": "belief breaks",
            "failure_layer": "PERFORMANCE",
            "smallest_repair_scope": "LINE",
            "minimal_fix": "rerender this line only",
            "do_not_touch": "story text",
            "regression_tests": ["local continuity"],
            "status": "REPAIR",
        }
        row.update(kw)
        return row

    def test_performance_routes_to_selective_tts_but_not_paid(self):
        r = self.base_result(); r["defects"]=[self.defect()]
        plan = compile_plan(r)
        self.assertEqual(plan["status"], "PASS_PLAN_COMPILED")
        rep = plan["repairs"][0]
        self.assertEqual(rep["action"], "SELECTIVE_DIALOGUE_RERENDER")
        self.assertTrue(rep["requires_separate_paid_canary_or_repair_authorization"])
        self.assertFalse(rep["provider_call_allowed"])
        self.assertFalse(rep["paid_synthesis_allowed"])
        self.assertFalse(plan["whole_episode_rerender_allowed"])

    def test_pronunciation_routes_to_dictionary_or_phrase(self):
        d=self.defect(heard="Лени-бёрд произношение неверное", minimal_fix="fix pronunciation only")
        r=self.base_result(); r["defects"]=[d]
        plan=compile_plan(r)
        rep=plan["repairs"][0]
        self.assertEqual(rep["performance_issue"], "PRONUNCIATION")
        self.assertEqual(rep["action"], "PRONUNCIATION_RULE_OR_MINIMUM_PHRASE_RERENDER")
        self.assertTrue(rep["requires_pronunciation_contract"])

    def test_mix_failure_does_not_rerender_dialogue(self):
        d=self.defect(failure_layer="MIX", question_class="SFX_MASKING", smallest_repair_scope="INTERVAL")
        r=self.base_result(); r["defects"]=[d]
        rep=compile_plan(r)["repairs"][0]
        self.assertEqual(rep["action"], "LOCAL_MIX_OR_AUTOMATION_PATCH")
        self.assertTrue(rep["dialogue_rerender_forbidden"])
        self.assertFalse(rep["requires_new_tts"])

    def test_sound_asset_failure_checks_shared_en_ru(self):
        d=self.defect(failure_layer="SOUND_ASSET", smallest_repair_scope="ASSET")
        r=self.base_result(); r["defects"]=[d]
        rep=compile_plan(r)["repairs"][0]
        self.assertTrue(rep["shared_en_ru_asset_check_required"])
        self.assertTrue(rep["dialogue_rerender_forbidden"])

    def test_unknown_layer_holds(self):
        d=self.defect(failure_layer="UNKNOWN", smallest_repair_scope="INTERVAL")
        r=self.base_result(); r["defects"]=[d]
        rep=compile_plan(r)["repairs"][0]
        self.assertEqual(rep["status"], "HOLD")
        self.assertEqual(rep["action"], "EVIDENCE_CLASSIFICATION_REQUIRED")

    def test_episode_scope_fails_closed(self):
        d=self.defect(smallest_repair_scope="WHOLE_EPISODE")
        r=self.base_result(); r["defects"]=[d]
        plan=compile_plan(r)
        self.assertEqual(plan["status"], "FAIL_CLOSED")
        self.assertIn("OVERBROAD_REPAIR_SCOPE_FORBIDDEN", plan["errors"][0]["errors"])

    def test_unverified_audio_identity_holds_execution(self):
        r=self.base_result(); r["source_identity"]["identity_status"]="UNVERIFIED"; r["defects"]=[self.defect()]
        plan=compile_plan(r)
        self.assertEqual(plan["status"], "HOLD_EVIDENCE_GATE")
        self.assertFalse(plan["executable_now"])
        self.assertIn("AUDIO_IDENTITY_NOT_VERIFIED", plan["hard_hold_reasons"])

    def test_pass_a_not_frozen_holds_execution(self):
        r=self.base_result(); r["blind_listen"]["pass_a_notes_frozen"] = False; r["defects"]=[self.defect()]
        plan=compile_plan(r)
        self.assertEqual(plan["status"], "HOLD_EVIDENCE_GATE")
        self.assertIn("PASS_A_NOT_FROZEN", plan["hard_hold_reasons"])


if __name__ == "__main__":
    unittest.main()
