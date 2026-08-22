from __future__ import annotations

import copy
import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
TOOL_DIR = HERE.parents[1]
ROOM917_DIR = HERE.parents[3]
sys.path.insert(0, str(TOOL_DIR))

from automix_postproduction_preflight import HOLD, PASS, evaluate  # noqa: E402

CONTRACT_PATH = ROOM917_DIR / "AUTOMIX" / "ROOM917_E01_AUTOMIX_POSTPRODUCTION_EXECUTION_CONTRACT_v1.json"


def valid_candidate():
    return {
        "locale": "EN",
        "mode": "POST_RENDER_PATCH",
        "voice_manifest": {
            "status": "LOCKED",
            "fixture_only": False,
            "production_sources": True,
            "sources": [
                {"role": "ELENA", "approval_status": "LOCKED", "sha256": "a" * 64},
                {"role": "JULIAN", "approval_status": "PASS", "sha256": "b" * 64},
                {"role": "CATE", "approval_status": "LOCKED", "sha256": "c" * 64},
            ],
        },
        "sound_binding_report": {
            "status": "PASS",
            "bindings": [
                {"asset_id": "A01_LOBBY_BED", "status": "PASS"},
                {"asset_id": "A02_SWITCHBOARD_ALCOVE_BED", "status": "PASS"},
                {"asset_id": "S13_INTERNAL_DOUBLE_RING_OLD", "status": "PASS"},
            ],
        },
        "timing": {
            "grade": "LIVE_TIMELINE",
            "fixture_only": False,
            "production_timestamps": True,
        },
        "protected_silence": {
            "resolved_from_same_live_timing": True,
            "post_fx_sample_exact_mask": True,
            "silence_removal": False,
            "reverb_tail_invasion": False,
        },
        "buses": ["DIALOGUE", "CLUE_SFX", "SFX", "FOLEY", "AMBIENCE", "MUSIC"],
        "ducking": {
            "targets": ["AMBIENCE", "MUSIC"],
            "immune": ["DIALOGUE", "CLUE_SFX"],
            "event_aware": True,
        },
        "telephone_events": [
            {
                "speaker": "CATE",
                "clean_human_source": True,
                "hpf_hz": 300,
                "lpf_hz": 3400,
                "reverb": "NONE",
                "mono_core": True,
                "pitch_shift": False,
                "stereo_widening": False,
                "ghost_processing": False,
            }
        ],
        "master": {
            "verified_bytes": True,
            "sha256": "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8",
        },
    }


class AutoMixPostproductionPreflightTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def assert_hold_gate(self, candidate, gate):
        result = evaluate(self.contract, candidate)
        self.assertEqual(HOLD, result["status"])
        self.assertFalse(result["render_authorized"])
        self.assertFalse(result["release_authority"])
        self.assertIn(gate, result["failed_gates"])

    def test_valid_en_production_candidate_passes_machine_preflight(self):
        result = evaluate(self.contract, valid_candidate())
        self.assertEqual(PASS, result["status"])
        self.assertTrue(result["render_authorized"])
        self.assertFalse(result["release_authority"])
        self.assertEqual([], result["failed_gates"])

    def test_synthetic_or_fixture_timing_is_rejected(self):
        candidate = valid_candidate()
        candidate["timing"] = {
            "grade": "SYNTHETIC_ALIGNMENT",
            "fixture_only": True,
            "production_timestamps": False,
        }
        self.assert_hold_gate(candidate, "LIVE_TIMING")

    def test_hold_sound_binding_is_rejected_even_when_report_says_pass(self):
        candidate = valid_candidate()
        candidate["sound_binding_report"]["bindings"][0]["status"] = "HOLD"
        self.assert_hold_gate(candidate, "SOUND_ASSET_BINDING")

    def test_unlocked_voice_source_is_rejected(self):
        candidate = valid_candidate()
        candidate["voice_manifest"]["sources"][0]["approval_status"] = "CANDIDATE"
        self.assert_hold_gate(candidate, "VOICE_PROVENANCE")

    def test_voice_without_hash_is_rejected(self):
        candidate = valid_candidate()
        candidate["voice_manifest"]["sources"][0]["sha256"] = ""
        self.assert_hold_gate(candidate, "VOICE_PROVENANCE")

    def test_non_cate_telephone_processing_is_rejected(self):
        candidate = valid_candidate()
        candidate["telephone_events"][0]["speaker"] = "ELENA"
        self.assert_hold_gate(candidate, "CATE_TELEPHONE_CHAIN")

    def test_cate_ghost_or_spatial_processing_is_rejected(self):
        candidate = valid_candidate()
        candidate["telephone_events"][0]["stereo_widening"] = True
        candidate["telephone_events"][0]["reverb"] = "ROOM"
        self.assert_hold_gate(candidate, "CATE_TELEPHONE_CHAIN")

    def test_missing_cate_telephone_event_is_rejected_for_e01(self):
        candidate = valid_candidate()
        candidate["telephone_events"] = []
        self.assert_hold_gate(candidate, "CATE_TELEPHONE_CHAIN")

    def test_unresolved_protected_silence_is_rejected(self):
        candidate = valid_candidate()
        candidate["protected_silence"]["resolved_from_same_live_timing"] = False
        self.assert_hold_gate(candidate, "PROTECTED_SILENCE")

    def test_ducking_dialogue_or_clue_bus_is_rejected(self):
        candidate = valid_candidate()
        candidate["ducking"]["targets"] = ["AMBIENCE", "MUSIC", "DIALOGUE"]
        candidate["ducking"]["immune"] = ["CLUE_SFX"]
        self.assert_hold_gate(candidate, "DUCKING")

    def test_wrong_bus_topology_is_rejected(self):
        candidate = valid_candidate()
        candidate["buses"] = ["DIALOGUE", "SFX", "FOLEY", "AMBIENCE", "MUSIC"]
        self.assert_hold_gate(candidate, "BUS_TOPOLOGY")

    def test_ru_is_held_until_current_cast_policy_unlocks_automix(self):
        candidate = valid_candidate()
        candidate["locale"] = "RU"
        self.assert_hold_gate(candidate, "LOCALE_AUTHORITY")

    def test_wrong_master_hash_is_rejected(self):
        candidate = valid_candidate()
        candidate["master"]["sha256"] = "d" * 64
        self.assert_hold_gate(candidate, "MASTER_IDENTITY")

    def test_missing_verified_master_bytes_is_rejected(self):
        candidate = valid_candidate()
        candidate["master"]["verified_bytes"] = False
        self.assert_hold_gate(candidate, "MASTER_IDENTITY")

    def test_unsupported_mode_is_rejected(self):
        candidate = valid_candidate()
        candidate["mode"] = "STEM_ASSEMBLY"
        self.assert_hold_gate(candidate, "MODE")


if __name__ == "__main__":
    unittest.main()
