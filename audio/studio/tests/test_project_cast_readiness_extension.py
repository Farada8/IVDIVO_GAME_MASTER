import copy
import sys
import unittest
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[1]
RUNTIME = STUDIO / "runtime"
for path in (STUDIO, RUNTIME):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cast_readiness import build_cast_readiness


def inventory():
    voices = ["voice-n", "voice-e", "voice-a", "voice-m", "voice-ad", "voice-l", "voice-c"]
    return {
        "status": "PASS",
        "verified": True,
        "provider": "elevenlabs",
        "source_snapshot_hash": "fixture-snapshot",
        "account_fingerprint_sha256": "a" * 64,
        "tts_model_ids": ["eleven_v3"],
        "voices": [{"voice_id": voice_id, "metadata_hash": voice_id + "-hash"} for voice_id in voices],
    }


class CompatibilityTests(unittest.TestCase):
    def test_lesson_zero_defaults_are_semantically_preserved(self):
        out = build_cast_readiness(
            inventory(),
            candidate_voice_ids={"NARRATOR": ["voice-n"], "ETHAN": ["voice-e"], "AOIFE": ["voice-a"]},
            model_id="eleven_v3",
        )
        self.assertEqual(out["status"], "READY_FOR_REAL_AUDITION")
        self.assertEqual(out["roles"], ["NARRATOR", "ETHAN", "AOIFE"])
        self.assertEqual(out["audition"]["pronunciation"]["terms"], ["Ифа", "Контакт"])
        self.assertEqual(out["audition"]["pair"]["roles"], ["ETHAN", "AOIFE"])
        self.assertEqual(out["audition"]["fatigue"]["minimum_seconds"], 480)
        self.assertFalse(out["voice_lock"])

    def test_manifest_remains_deterministic(self):
        candidates = {"NARRATOR": ["voice-n"], "ETHAN": ["voice-e"], "AOIFE": ["voice-a"]}
        first = build_cast_readiness(inventory(), candidate_voice_ids=candidates, model_id="eleven_v3")
        second = build_cast_readiness(
            inventory(), candidate_voice_ids=copy.deepcopy(candidates), model_id="eleven_v3"
        )
        self.assertEqual(first["manifest_hash"], second["manifest_hash"])


class D01ProjectSpecTests(unittest.TestCase):
    ROLES = ["NARRATOR", "MARA", "ADRIAN", "LILY", "CELESTE"]
    TERMS = ["Mara Quinn", "Adrian Vale", "Evelyn Vale", "Celeste Arden", "Vale Meridian", "Ravenmere"]

    def candidates(self):
        return {
            "NARRATOR": ["voice-n"],
            "MARA": ["voice-m"],
            "ADRIAN": ["voice-ad"],
            "LILY": ["voice-l"],
            "CELESTE": ["voice-c"],
        }

    def test_d01_project_spec_is_supported(self):
        out = build_cast_readiness(
            inventory(),
            candidate_voice_ids=self.candidates(),
            model_id="eleven_v3",
            required_roles=self.ROLES,
            pronunciation_terms=self.TERMS,
            pair_roles=["MARA", "ADRIAN"],
        )
        self.assertEqual(out["status"], "READY_FOR_REAL_AUDITION")
        self.assertEqual(out["roles"], self.ROLES)
        self.assertEqual(out["audition"]["pair"]["roles"], ["MARA", "ADRIAN"])
        self.assertEqual(out["audition"]["pronunciation"]["terms"], self.TERMS)
        self.assertFalse(out["provider_dispatch_allowed"])
        self.assertFalse(out["machine_may_auto_lock"])

    def test_d01_missing_role_holds(self):
        candidates = self.candidates()
        candidates.pop("LILY")
        out = build_cast_readiness(
            inventory(),
            candidate_voice_ids=candidates,
            model_id="eleven_v3",
            required_roles=self.ROLES,
            pronunciation_terms=self.TERMS,
            pair_roles=["MARA", "ADRIAN"],
        )
        self.assertEqual(out["status"], "HOLD_CAST_CANDIDATES")
        self.assertEqual(out["missing_roles"], ["LILY"])

    def test_invalid_project_pair_fails_closed(self):
        out = build_cast_readiness(
            inventory(),
            candidate_voice_ids=self.candidates(),
            model_id="eleven_v3",
            required_roles=self.ROLES,
            pair_roles=["MARA", "ETHAN"],
        )
        self.assertEqual(out["status"], "FAIL_CAST_SPEC")
        self.assertEqual(out["reason"], "PAIR_ROLES_INVALID")

    def test_missing_provider_inventory_holds_and_keeps_project_roles(self):
        out = build_cast_readiness(
            {"status": "HOLD", "verified": False},
            candidate_voice_ids={},
            model_id="eleven_v3",
            required_roles=self.ROLES,
            pair_roles=["MARA", "ADRIAN"],
        )
        self.assertEqual(out["status"], "HOLD_PROVIDER_INVENTORY")
        self.assertEqual(out["required_roles"], self.ROLES)
        self.assertFalse(out["provider_dispatch_allowed"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
