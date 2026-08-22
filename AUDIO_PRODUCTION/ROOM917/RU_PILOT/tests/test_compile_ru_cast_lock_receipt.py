import unittest

from AUDIO_PRODUCTION.ROOM917.RU_PILOT.tools.compile_ru_cast_lock_receipt import compile_receipt


ROLES = ("ELENA", "JULIAN", "MINA", "CATE")
PAIR = {
    "RU_PAIR_01_ELENA_MINA_LOBBY": "PASS",
    "RU_PAIR_02_ELENA_JULIAN_DOORS": "PASS",
    "RU_PAIR_03_ELENA_JULIAN_STATUS": "PASS",
    "RU_PAIR_04_CATE_LINE_VS_CASSETTE": "PASS",
}


class CastLockCompilerTests(unittest.TestCase):
    def snapshot(self):
        return {
            "status": "PASS_CANDIDATES_FOUND",
            "generated_at": "2026-08-22T17:00:00Z",
            "candidates": [
                {"voice_id": f"voice_{role.lower()}", "name": role.title(), "ru_verified": True, "category": "professional", "notice_period": 365, "disable_at_unix": None}
                for role in ROLES
            ],
        }

    def review(self):
        roles = {}
        for role in ROLES:
            roles[role] = {
                "selected_voice_id": f"voice_{role.lower()}",
                "provider_name": role.title(),
                "preview_listen": "PASS",
                "provider_identity_check": "PASS",
                "native_ru_pronunciation": "PASS",
                "age_character_fit": "PASS",
                "naturalism": "PASS",
                "microemotion_subtext": "PASS",
                "precision_under_pressure": "PASS",
                "repeat_take_identity_consistency": "PASS",
                "founder_credibility": "PASS",
                "score_0_30": 27,
                "naturalism_score_0_5": 4.5,
                "pronunciation_score_0_5": 4.5,
                "hard_reject": False,
            }
        return {
            "status": "REVIEW_COMPLETE",
            "pronunciation_gate": "PASS",
            "all_selected_voice_ids_unique": "PASS",
            "paid_s0_authorized": False,
            "cast_lock": False,
            "pair_tests": dict(PAIR),
            "roles": roles,
        }

    def registry(self):
        records = []
        for role in ROLES:
            for n in (1, 2):
                records.append({
                    "take_id": f"{role}_{n}",
                    "unit_id": f"RU_{role}_{n}",
                    "character": role,
                    "voice_id": f"voice_{role.lower()}",
                    "model_id": "eleven_v3",
                    "language_code": "ru",
                    "voice_settings": {"stability": 0.45},
                    "output_sha256": ("a" if n == 1 else "b") * 64,
                    "selected": True,
                    "qc": {"pronunciation": "PASS", "technical_artifact": "PASS"},
                })
        return {"records": records}

    def test_complete_evidence_locks(self):
        receipt = compile_receipt(self.snapshot(), self.review(), self.registry())
        self.assertEqual(receipt["status"], "LOCKED")
        self.assertTrue(receipt["global_lock_gate"]["all_four_roles_locked"])
        self.assertEqual(receipt["execution_boundary"]["provider_calls_made_by_compiler"], 0)
        self.assertEqual(receipt["execution_boundary"]["paid_synthesis_calls_made_by_compiler"], 0)
        for role in ROLES:
            self.assertEqual(receipt["roles"][role]["founder_credibility"], "YES")
            self.assertEqual(len(receipt["roles"][role]["accepted_canary_ids"]), 2)

    def test_missing_explicit_naturalism_score_fails(self):
        review = self.review()
        review["roles"]["ELENA"]["naturalism_score_0_5"] = None
        with self.assertRaisesRegex(ValueError, "naturalism_score_0_5 missing"):
            compile_receipt(self.snapshot(), review, self.registry())

    def test_low_pronunciation_score_fails(self):
        review = self.review()
        review["roles"]["JULIAN"]["pronunciation_score_0_5"] = 3.9
        with self.assertRaisesRegex(ValueError, "pronunciation_score_0_5 must be 4.0..5.0"):
            compile_receipt(self.snapshot(), review, self.registry())

    def test_single_selected_take_fails(self):
        registry = self.registry()
        registry["records"] = [r for r in registry["records"] if not (r["character"] == "MINA" and r["take_id"] == "MINA_2")]
        with self.assertRaisesRegex(ValueError, "MINA: fewer than two selected accepted takes"):
            compile_receipt(self.snapshot(), self.review(), registry)

    def test_same_unit_twice_fails(self):
        registry = self.registry()
        mina = [r for r in registry["records"] if r["character"] == "MINA"]
        mina[1]["unit_id"] = mina[0]["unit_id"]
        with self.assertRaisesRegex(ValueError, "MINA: selected evidence must cover at least two distinct canary units"):
            compile_receipt(self.snapshot(), self.review(), registry)

    def test_voice_settings_drift_fails(self):
        registry = self.registry()
        julian = [r for r in registry["records"] if r["character"] == "JULIAN"]
        julian[1]["voice_settings"] = {"stability": 0.60}
        with self.assertRaisesRegex(ValueError, "JULIAN: selected take voice_settings drift"):
            compile_receipt(self.snapshot(), self.review(), registry)

    def test_metadata_only_cannot_lock(self):
        review = self.review()
        review["roles"]["CATE"]["founder_credibility"] = "PENDING"
        with self.assertRaisesRegex(ValueError, "CATE: founder_credibility must PASS"):
            compile_receipt(self.snapshot(), review, self.registry())

    def test_duplicate_voice_ids_fail(self):
        snapshot = self.snapshot()
        review = self.review()
        registry = self.registry()
        review["roles"]["MINA"]["selected_voice_id"] = "voice_elena"
        for r in registry["records"]:
            if r["character"] == "MINA":
                r["voice_id"] = "voice_elena"
        with self.assertRaisesRegex(ValueError, "voice IDs must be unique across roles"):
            compile_receipt(snapshot, review, registry)


if __name__ == "__main__":
    unittest.main()
