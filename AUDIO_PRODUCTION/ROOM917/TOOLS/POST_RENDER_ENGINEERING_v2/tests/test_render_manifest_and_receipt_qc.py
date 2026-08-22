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

from render_manifest_and_receipt_qc import (  # noqa: E402
    MANIFEST_HOLD,
    MANIFEST_PASS,
    QC_HOLD,
    QC_PASS,
    compile_manifest,
    validate_receipt,
)

CONTRACT_PATH = ROOM917_DIR / "AUTOMIX" / "ROOM917_E01_RENDER_MANIFEST_AND_RECEIPT_QC_CONTRACT_v1.json"
MASTER_SHA = "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
PLAN_SHA = "a" * 64
MANIFEST_SHA = "b" * 64


def valid_plan():
    return {
        "status": "PASS_AUTOMATION_PLAN_COMPILED",
        "render_authority": True,
        "release_authority": False,
    }


def valid_source_master():
    return {"sha256": MASTER_SHA, "exact_bytes_verified": True}


def valid_receipt(manifest):
    sample_count = 480000
    outputs = []
    all_entries = [manifest["full_mix"]] + list(manifest["stems"])
    for index, entry in enumerate(all_entries):
        outputs.append({
            "file_name": entry["file_name"],
            "exists": True,
            "sha256": f"{index + 1:064x}",
            "sample_rate_hz": entry["sample_rate_hz"],
            "bit_depth": entry["bit_depth"],
            "channels": entry["channels"],
            "sample_count": sample_count,
            "start_offset_samples": 0,
        })
    return {
        "manifest_sha256": MANIFEST_SHA,
        "source_master_sha256": manifest["source_master_sha256"],
        "compiled_plan_sha256": manifest["compiled_plan_sha256"],
        "measurement_source": "REAL_RENDER_BYTES",
        "outputs": outputs,
        "stem_sum_null": {
            "max_abs_lsb": 1,
            "sample_offset": 0,
            "compared_samples": sample_count,
        },
        "protected_silence_post_fx_sample_exact_pass": True,
        "clue_sfx_survival_pass": True,
        "scene3_lineage_preserved": True,
        "mono_survival_pass": True,
        "phone_proxy_survival_pass": True,
        "full_mix_metrics": {
            "integrated_lufs": -16.0,
            "true_peak_dbtp": -1.2,
            "lra_lu": 8.0,
        },
    }


class RenderManifestAndReceiptQCTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def compile_valid(self):
        result = compile_manifest(
            self.contract,
            valid_plan(),
            valid_source_master(),
            plan_sha256=PLAN_SHA,
            output_root="render/e01",
        )
        self.assertEqual(MANIFEST_PASS, result["status"])
        return result

    def validate(self, receipt_mutator=None, manifest_mutator=None):
        manifest = self.compile_valid()
        if manifest_mutator:
            manifest_mutator(manifest)
        receipt = valid_receipt(manifest)
        if receipt_mutator:
            receipt_mutator(receipt)
        return validate_receipt(self.contract, manifest, receipt, manifest_sha256=MANIFEST_SHA)

    def assert_qc_hold(self, reason, receipt_mutator=None, manifest_mutator=None):
        result = self.validate(receipt_mutator, manifest_mutator)
        self.assertEqual(QC_HOLD, result["status"])
        self.assertFalse(result["render_receipt_accepted"])
        self.assertFalse(result["release_authority"])
        self.assertIn(reason, result["reasons"])

    def test_manifest_compiles_exact_full_mix_and_six_stems(self):
        result = self.compile_valid()
        self.assertEqual(6, len(result["stems"]))
        self.assertEqual("ROOM917_E01_FULLMIX_48k24.wav", result["full_mix"]["file_name"])
        self.assertFalse(result["release_authority"])

    def test_manifest_rejects_unpassed_plan(self):
        plan = valid_plan()
        plan["status"] = "HOLD_AUTOMATION_PLAN"
        result = compile_manifest(self.contract, plan, valid_source_master(), plan_sha256=PLAN_SHA, output_root="render/e01")
        self.assertEqual(MANIFEST_HOLD, result["status"])
        self.assertIn("compiled_plan_status_not_pass", result["reasons"])

    def test_manifest_rejects_wrong_master_sha(self):
        source = valid_source_master()
        source["sha256"] = "f" * 64
        result = compile_manifest(self.contract, valid_plan(), source, plan_sha256=PLAN_SHA, output_root="render/e01")
        self.assertEqual(MANIFEST_HOLD, result["status"])
        self.assertIn("source_master_sha256_mismatch", result["reasons"])

    def test_manifest_rejects_unverified_master_bytes(self):
        source = valid_source_master()
        source["exact_bytes_verified"] = False
        result = compile_manifest(self.contract, valid_plan(), source, plan_sha256=PLAN_SHA, output_root="render/e01")
        self.assertEqual(MANIFEST_HOLD, result["status"])
        self.assertIn("source_master_exact_bytes_not_verified", result["reasons"])

    def test_valid_real_receipt_passes_machine_qc_only(self):
        result = self.validate()
        self.assertEqual(QC_PASS, result["status"])
        self.assertTrue(result["render_receipt_accepted"])
        self.assertFalse(result["release_authority"])
        self.assertIn("P003B", result["next"])

    def test_missing_stem_fails(self):
        self.assert_qc_hold("render_output_set_mismatch", lambda r: r["outputs"].pop())

    def test_extra_output_fails(self):
        self.assert_qc_hold("render_output_set_mismatch", lambda r: r["outputs"].append({"file_name": "EXTRA.wav"}))

    def test_hashless_output_fails(self):
        self.assert_qc_hold("one_or_more_outputs_invalid", lambda r: r["outputs"][0].update({"sha256": ""}))

    def test_output_format_mismatch_fails(self):
        self.assert_qc_hold("one_or_more_outputs_invalid", lambda r: r["outputs"][0].update({"sample_rate_hz": 44100}))

    def test_stem_sample_count_mismatch_fails(self):
        self.assert_qc_hold("stem_sample_count_mismatch", lambda r: r["outputs"][1].update({"sample_count": 479999}))

    def test_nonzero_output_offset_fails(self):
        self.assert_qc_hold("one_or_more_outputs_invalid", lambda r: r["outputs"][2].update({"start_offset_samples": 1}))

    def test_stem_sum_above_one_lsb_fails(self):
        self.assert_qc_hold("stem_sum_null_exceeds_one_lsb", lambda r: r["stem_sum_null"].update({"max_abs_lsb": 2}))

    def test_stem_sum_offset_fails(self):
        self.assert_qc_hold("stem_sum_null_sample_offset_nonzero", lambda r: r["stem_sum_null"].update({"sample_offset": 1}))

    def test_protected_silence_failure_blocks(self):
        self.assert_qc_hold("protected_silence_post_fx_sample_exact_failed", lambda r: r.update({"protected_silence_post_fx_sample_exact_pass": False}))

    def test_clue_survival_failure_blocks(self):
        self.assert_qc_hold("clue_sfx_survival_failed", lambda r: r.update({"clue_sfx_survival_pass": False}))

    def test_scene3_lineage_failure_blocks(self):
        self.assert_qc_hold("scene3_lineage_not_preserved", lambda r: r.update({"scene3_lineage_preserved": False}))

    def test_mono_failure_blocks(self):
        self.assert_qc_hold("mono_survival_failed", lambda r: r.update({"mono_survival_pass": False}))

    def test_phone_proxy_failure_blocks(self):
        self.assert_qc_hold("phone_proxy_survival_failed", lambda r: r.update({"phone_proxy_survival_pass": False}))

    def test_loudness_outside_tolerance_blocks(self):
        self.assert_qc_hold("integrated_lufs_out_of_profile", lambda r: r["full_mix_metrics"].update({"integrated_lufs": -17.0}))

    def test_true_peak_above_limit_blocks(self):
        self.assert_qc_hold("true_peak_out_of_profile", lambda r: r["full_mix_metrics"].update({"true_peak_dbtp": -0.9}))

    def test_lra_above_limit_blocks(self):
        self.assert_qc_hold("lra_out_of_profile", lambda r: r["full_mix_metrics"].update({"lra_lu": 12.0}))

    def test_non_real_measurement_source_blocks(self):
        self.assert_qc_hold("machine_qc_not_measured_from_real_render_bytes", lambda r: r.update({"measurement_source": "FIXTURE"}))

    def test_manifest_identity_mismatch_blocks(self):
        self.assert_qc_hold("receipt_manifest_sha256_mismatch", lambda r: r.update({"manifest_sha256": "c" * 64}))

    def test_compiled_plan_identity_mismatch_blocks(self):
        self.assert_qc_hold("receipt_compiled_plan_sha256_mismatch", lambda r: r.update({"compiled_plan_sha256": "d" * 64}))


if __name__ == "__main__":
    unittest.main()
