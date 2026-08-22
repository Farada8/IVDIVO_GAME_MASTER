from __future__ import annotations

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
A01 = "A01_GREYHAVEN_LOBBY_30S_LOOP"
A02 = "A02_SWITCHBOARD_ALCOVE_30S_LOOP"


def valid_sound_binding_report():
    requested = [A01, A02]
    return {
        "schema_version": "room917.sound_asset_binding_gate/1.1",
        "status": "PASS",
        "contract": "AUDIO_PRODUCTION/ROOM917/SOUND_DESIGN/ROOM917_E01_CURRENT_BRANCH_SOUND_ASSET_CONTRACT_v1.json",
        "requested_asset_ids": requested.copy(),
        "declared_requested_asset_ids": requested.copy(),
        "request_set_errors": [],
        "rows": [
            {"asset_id": A01, "candidate_id": "A01_TEST", "status": "PASS", "errors": []},
            {"asset_id": A02, "candidate_id": "A02_TEST", "status": "PASS", "errors": []},
        ],
        "renderer_bindings_atomic": True,
        "renderer_bindings_complete_for_requested_set": True,
        "renderer_bindings_emitted": requested.copy(),
        "renderer_bindings_suppressed_on_hold": False,
    }


def valid_timing_report():
    return {
        "schema_version": "room917.e01_sound_asset_resolved_timing/1.1",
        "status": "PASS",
        "production_timing_ready": True,
        "requested_asset_ids": [A01, A02],
        "resolved": {
            A01: {"events": [{"start_seconds": 1.0, "end_seconds": 10.0, "source_status": "LIVE_TIMELINE", "source_ref": "test"}]},
            A02: {"events": [{"start_seconds": 10.0, "end_seconds": 20.0, "source_status": "ACCEPTED_ALIGNMENT", "source_ref": "test"}]},
        },
        "production_resolved": {
            A01: {"events": [{"start_seconds": 1.0, "end_seconds": 10.0, "source_status": "LIVE_TIMELINE", "source_ref": "test"}]},
            A02: {"events": [{"start_seconds": 10.0, "end_seconds": 20.0, "source_status": "ACCEPTED_ALIGNMENT", "source_ref": "test"}]},
        },
        "holds": [],
        "errors": [],
    }


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
        "sound_binding_report": valid_sound_binding_report(),
        "timing": valid_timing_report(),
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

    def test_old_handmade_sound_summary_is_rejected(self):
        candidate = valid_candidate()
        candidate["sound_binding_report"] = {
            "status": "PASS",
            "bindings": [{"asset_id": A01, "status": "PASS"}],
        }
        self.assert_hold_gate(candidate, "SOUND_ASSET_BINDING")

    def test_missing_a02_current_patch_asset_is_rejected(self):
        candidate = valid_candidate()
        report = candidate["sound_binding_report"]
        report["requested_asset_ids"] = [A01]
        report["declared_requested_asset_ids"] = [A01]
        report["rows"] = [report["rows"][0]]
        report["renderer_bindings_emitted"] = [A01]
        self.assert_hold_gate(candidate, "SOUND_ASSET_BINDING")

    def test_partial_binding_set_is_rejected_even_if_status_says_pass(self):
        candidate = valid_candidate()
        candidate["sound_binding_report"]["renderer_bindings_emitted"] = [A01]
        self.assert_hold_gate(candidate, "SOUND_ASSET_BINDING")

    def test_hold_sound_binding_row_is_rejected_even_when_report_says_pass(self):
        candidate = valid_candidate()
        candidate["sound_binding_report"]["rows"][0]["status"] = "HOLD"
        self.assert_hold_gate(candidate, "SOUND_ASSET_BINDING")

    def test_synthetic_or_legacy_timing_summary_is_rejected(self):
        candidate = valid_candidate()
        candidate["timing"] = {
            "grade": "SYNTHETIC_ALIGNMENT",
            "fixture_only": True,
            "production_timestamps": False,
        }
        self.assert_hold_gate(candidate, "LIVE_TIMING")

    def test_partial_semantic_timing_is_rejected(self):
        candidate = valid_candidate()
        timing = candidate["timing"]
        timing["status"] = "HOLD"
        timing["production_timing_ready"] = False
        timing["production_resolved"] = {}
        timing["holds"] = [{"asset_id": A02, "reason": "ANCHOR_NOT_FOUND"}]
        self.assert_hold_gate(candidate, "LIVE_TIMING")

    def test_semantic_timing_missing_one_requested_asset_is_rejected(self):
        candidate = valid_candidate()
        del candidate["timing"]["production_resolved"][A02]
        self.assert_hold_gate(candidate, "LIVE_TIMING")

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
