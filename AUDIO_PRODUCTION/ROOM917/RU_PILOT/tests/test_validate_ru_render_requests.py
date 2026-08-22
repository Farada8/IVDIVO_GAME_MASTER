import unittest

from AUDIO_PRODUCTION.ROOM917.RU_PILOT.tools.validate_ru_render_requests import sha256_text, validate_bundle


class RenderRequestValidatorTests(unittest.TestCase):
    def setUp(self):
        self.source = "Не трогайте. Время — один семнадцать и двенадцать секунд."
        self.manifest = {
            "audition_units": [
                {"id": "U1", "character": "ELENA", "text": self.source}
            ]
        }
        self.policy = {
            "tag_classes": {
                "ALLOW_FOR_BOUNDED_CANARY": ["[whispers]", "[sighs]"],
                "CONDITIONAL_SOURCE_ACTION_REQUIRED": ["[shouts]"],
                "ROOM917_DEFAULT_FORBIDDEN": ["[seductively]", "[terrified]"]
            }
        }

    def req(self, text=None, **overrides):
        text = self.source if text is None else text
        row = {
            "request_id": "R1",
            "unit_id": "U1",
            "character": "ELENA",
            "voice_id": "voice_current_123",
            "model_id": "eleven_v3",
            "language_code": "ru",
            "source_text_sha256": sha256_text(self.source),
            "text": text,
            "request_text_sha256": sha256_text(text),
            "text_variant_mode": "EXACT_PLUS_TAGS",
            "performance_tags": [],
            "pronunciation_dictionary_locators": []
        }
        row.update(overrides)
        return row

    def test_exact_untagged_passes(self):
        result = validate_bundle(self.manifest, self.policy, {"requests": [self.req()]})
        self.assertEqual(result["status"], "PASS_ZERO_SPEND_PRE_PROVIDER")
        self.assertEqual(result["provider_calls"], 0)
        self.assertEqual(result["paid_synthesis_calls"], 0)

    def test_approved_tag_preserves_dialogue(self):
        text = "[whispers] " + self.source
        req = self.req(text=text, performance_tags=["[whispers]"])
        result = validate_bundle(self.manifest, self.policy, {"requests": [req]})
        self.assertEqual(result["status"], "PASS_ZERO_SPEND_PRE_PROVIDER")

    def test_word_mutation_fails_exact_mode(self):
        text = self.source.replace("Не трогайте", "Не двигайтесь")
        result = validate_bundle(self.manifest, self.policy, {"requests": [self.req(text=text)]})
        self.assertEqual(result["status"], "FAIL_CLOSED")
        errors = result["errors"][0]["errors"]
        self.assertIn("DIALOGUE_MUTATION_EXACT_MODE", errors)

    def test_punctuation_only_same_words_passes(self):
        text = "Не трогайте... Время — один семнадцать и двенадцать секунд."
        req = self.req(text=text, text_variant_mode="PUNCTUATION_ONLY", variant_reason="pause canary")
        result = validate_bundle(self.manifest, self.policy, {"requests": [req]})
        self.assertEqual(result["status"], "PASS_ZERO_SPEND_PRE_PROVIDER")

    def test_forbidden_tag_fails(self):
        text = "[seductively] " + self.source
        req = self.req(text=text, performance_tags=["[seductively]"])
        result = validate_bundle(self.manifest, self.policy, {"requests": [req]})
        self.assertEqual(result["status"], "FAIL_CLOSED")
        self.assertIn("ROOM917_FORBIDDEN_TAG:[seductively]", result["errors"][0]["errors"])

    def test_conditional_tag_requires_source_action_auth(self):
        text = "[shouts] " + self.source
        req = self.req(text=text, performance_tags=["[shouts]"])
        result = validate_bundle(self.manifest, self.policy, {"requests": [req]})
        self.assertEqual(result["status"], "FAIL_CLOSED")
        self.assertIn("CONDITIONAL_TAG_REQUIRES_SOURCE_ACTION_AUTH:[shouts]", result["errors"][0]["errors"])

    def test_more_than_three_dictionary_locators_fails(self):
        locs = [
            {"pronunciation_dictionary_id": f"d{i}", "version_id": f"v{i}"}
            for i in range(4)
        ]
        result = validate_bundle(self.manifest, self.policy, {"requests": [self.req(pronunciation_dictionary_locators=locs)]})
        self.assertEqual(result["status"], "FAIL_CLOSED")
        self.assertIn("MORE_THAN_3_PRONUNCIATION_DICTIONARY_LOCATORS", result["errors"][0]["errors"])

    def test_ssml_break_fails(self):
        text = "<break time=\"500ms\"/> " + self.source
        result = validate_bundle(self.manifest, self.policy, {"requests": [self.req(text=text)]})
        self.assertEqual(result["status"], "FAIL_CLOSED")
        self.assertIn("SSML_BREAK_FORBIDDEN_IN_V3", result["errors"][0]["errors"])


if __name__ == "__main__":
    unittest.main()
