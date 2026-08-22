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

from compile_automix_automation_plan import HOLD, PASS, evaluate  # noqa: E402

CONTRACT_PATH = ROOM917_DIR / "AUTOMIX" / "ROOM917_E01_AUTOMIX_AUTOMATION_PLAN_CONTRACT_v1.json"


def preflight_pass():
    return {
        "status": "PASS_AUTOMIX_EXECUTION_READY",
        "render_authorized": True,
        "release_authority": False,
    }


def valid_source():
    return {
        "buses": ["DIALOGUE", "CLUE_SFX", "SFX", "FOLEY", "AMBIENCE", "MUSIC"],
        "timing_fixture_only": False,
        "production_timestamps": True,
        "operations": [
            {
                "operation_id": "bed_a01_001",
                "type": "PLACE_ASSET",
                "bus": "AMBIENCE",
                "start_sample": 0,
                "end_sample": 48000,
                "source_sha256": "a" * 64,
                "binding_status": "PASS",
                "timing_grade": "LIVE_TIMELINE",
            },
            {
                "operation_id": "duck_music_001",
                "type": "DUCK_WINDOW",
                "bus": "MUSIC",
                "start_sample": 48000,
                "end_sample": 72000,
                "gain_db": -4.0,
                "trigger": "ELENA_DIALOGUE",
                "timing_grade": "LIVE_TIMELINE",
            },
            {
                "operation_id": "cate_tel_001",
                "type": "CATE_TELEPHONE_CHAIN",
                "bus": "DIALOGUE",
                "start_sample": 96000,
                "end_sample": 120000,
                "speaker": "CATE",
                "hpf_hz": 300,
                "lpf_hz": 3400,
                "reverb": "NONE",
                "mono_core": True,
                "pitch_shift": False,
                "stereo_widening": False,
                "ghost_processing": False,
                "timing_grade": "ACCEPTED_ALIGNMENT",
            },
            {
                "operation_id": "julian_move_001",
                "type": "SPATIAL_EVENT",
                "bus": "DIALOGUE",
                "start_sample": 120000,
                "end_sample": 144000,
                "speaker_or_source": "JULIAN",
                "pan_start": -0.35,
                "pan_end": 0.15,
                "timing_grade": "LIVE_TIMELINE",
            },
            {
                "operation_id": "silence_001",
                "type": "PROTECTED_SILENCE",
                "start_sample": 150000,
                "end_sample": 156000,
                "timing_grade": "LIVE_TIMELINE",
                "post_fx_sample_exact_mask": True,
            },
        ],
    }


class CompileAutoMixAutomationPlanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def run_eval(self, source=None, preflight=None):
        return evaluate(
            self.contract,
            preflight if preflight is not None else preflight_pass(),
            source if source is not None else valid_source(),
            source_sha256="1" * 64,
            preflight_sha256="2" * 64,
        )

    def assert_hold(self, source=None, preflight=None, reason=None):
        result = self.run_eval(source, preflight)
        self.assertEqual(HOLD, result["status"])
        self.assertFalse(result["render_authority"])
        self.assertFalse(result["release_authority"])
        if reason:
            text = json.dumps(result)
            self.assertIn(reason, text)

    def test_valid_plan_compiles_and_never_grants_release(self):
        result = self.run_eval()
        self.assertEqual(PASS, result["status"])
        self.assertTrue(result["render_authority"])
        self.assertFalse(result["release_authority"])
        self.assertEqual(5, result["operation_count"])

    def test_output_is_sorted_deterministically(self):
        source = valid_source()
        source["operations"] = list(reversed(source["operations"]))
        result = self.run_eval(source)
        self.assertEqual(PASS, result["status"])
        starts = [x["start_sample"] for x in result["operations"]]
        self.assertEqual(starts, sorted(starts))

    def test_failed_preflight_blocks_compilation(self):
        p = preflight_pass()
        p["status"] = "HOLD_AUTOMIX_EXECUTION"
        p["render_authorized"] = False
        self.assert_hold(preflight=p, reason="preflight_status_not_PASS_AUTOMIX_EXECUTION_READY")

    def test_synthetic_timing_is_rejected(self):
        source = valid_source()
        source["operations"][0]["timing_grade"] = "SYNTHETIC_ALIGNMENT"
        self.assert_hold(source=source, reason="timing_grade_must_be_ACCEPTED_ALIGNMENT_or_LIVE_TIMELINE")

    def test_fixture_source_timing_is_rejected(self):
        source = valid_source()
        source["timing_fixture_only"] = True
        self.assert_hold(source=source, reason="source_timing_is_fixture_or_unproven")

    def test_hold_asset_is_rejected(self):
        source = valid_source()
        source["operations"][0]["binding_status"] = "HOLD"
        self.assert_hold(source=source, reason="asset_binding_status_not_PASS")

    def test_asset_without_hash_is_rejected(self):
        source = valid_source()
        source["operations"][0]["source_sha256"] = ""
        self.assert_hold(source=source, reason="asset_source_sha256_missing_or_invalid")

    def test_dialogue_ducking_is_rejected(self):
        source = valid_source()
        source["operations"][1]["bus"] = "DIALOGUE"
        self.assert_hold(source=source, reason="duck_bus_forbidden")

    def test_non_cate_telephone_chain_is_rejected(self):
        source = valid_source()
        source["operations"][2]["speaker"] = "ELENA"
        self.assert_hold(source=source, reason="cate_chain_speaker_mismatch")

    def test_ghost_processing_on_cate_is_rejected(self):
        source = valid_source()
        source["operations"][2]["ghost_processing"] = True
        self.assert_hold(source=source, reason="cate_chain_ghost_processing_mismatch")

    def test_spatial_pan_out_of_range_is_rejected(self):
        source = valid_source()
        source["operations"][3]["pan_end"] = 1.5
        self.assert_hold(source=source, reason="pan_end_out_of_range")

    def test_protected_silence_overlap_is_rejected(self):
        source = valid_source()
        source["operations"].append({
            "operation_id": "foley_bad_overlap",
            "type": "PLACE_ASSET",
            "bus": "FOLEY",
            "start_sample": 152000,
            "end_sample": 154000,
            "source_sha256": "f" * 64,
            "binding_status": "PASS",
            "timing_grade": "LIVE_TIMELINE",
        })
        self.assert_hold(source=source, reason="overlaps_protected_silence:silence_001")

    def test_duplicate_operation_id_is_rejected(self):
        source = valid_source()
        duplicate = copy.deepcopy(source["operations"][0])
        duplicate["start_sample"] = 200000
        duplicate["end_sample"] = 210000
        source["operations"].append(duplicate)
        self.assert_hold(source=source, reason="operation_id_duplicate")

    def test_missing_timestamp_is_not_inferred(self):
        source = valid_source()
        del source["operations"][0]["start_sample"]
        self.assert_hold(source=source, reason="missing_required_field:start_sample")

    def test_bus_set_must_remain_exact(self):
        source = valid_source()
        source["buses"].remove("CLUE_SFX")
        self.assert_hold(source=source, reason="source_bus_set_does_not_match_required_exact_set")


if __name__ == "__main__":
    unittest.main()
