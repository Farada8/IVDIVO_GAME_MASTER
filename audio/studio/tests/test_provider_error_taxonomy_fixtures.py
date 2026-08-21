import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "audio" / "studio" / "runtime"))
from production_control import normalize_provider_error

FIXTURE = ROOT / "AUDIO_PRODUCTION" / "UNIVERSAL_AUDIO_NOVEL_ENGINE" / "WAVE4_INTEGRATION_2026-08-21" / "fixtures" / "PROVIDER_ERROR_TAXONOMY_FIXTURES_v1.json"


class ProviderErrorFixtureTests(unittest.TestCase):
    def test_all_sanitized_error_shapes_map_stably(self):
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(payload["cases"]), 10)
        for case in payload["cases"]:
            with self.subTest(case=case["id"]):
                out = normalize_provider_error(case.get("status"), case.get("code"), case.get("message", ""))
                self.assertEqual(out["category"], case["expected_category"])
                self.assertEqual(out["retryable"], case["expected_retryable"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
