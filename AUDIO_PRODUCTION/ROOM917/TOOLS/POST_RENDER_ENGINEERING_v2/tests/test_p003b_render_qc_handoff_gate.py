from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
TOOL_DIR = HERE.parents[1]
ROOM917_DIR = HERE.parents[3]
sys.path.insert(0, str(TOOL_DIR))

from p003b_render_qc_handoff_gate import HOLD, PASS, evaluate_handoff  # noqa: E402
from render_manifest_and_receipt_qc import compile_manifest  # noqa: E402

CONTRACT_PATH = ROOM917_DIR / "AUTOMIX" / "ROOM917_E01_RENDER_MANIFEST_AND_RECEIPT_QC_CONTRACT_v1.json"
MASTER_SHA = "231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8"
PLAN_SHA = "a" * 64
MANIFEST_SHA = "b" * 64
RECEIPT_SHA = "c" * 64
AUDIO_SHA = "d" * 64


def valid_plan():
    return {"status": "PASS_AUTOMATION_PLAN_COMPILED", "render_authority": True, "release_authority": False}


def valid_manifest(contract):
    return compile_manifest(
        contract,
        valid_plan(),
        {"sha256": MASTER_SHA, "exact_bytes_verified": True},
        plan_sha256=PLAN_SHA,
        output_root="render/e01",
    )


def valid_receipt(manifest):
    sample_count = 480000
    outputs = []
    entries = [manifest["full_mix"]] + list(manifest["stems"])
    for index, entry in enumerate(entries):
        outputs.append({
            "file_name": entry["file_name"],
            "exists": True,
            "sha256": AUDIO_SHA if entry["kind"] == "FULL_MIX" else f"{index + 10:064x}",
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
        "stem_sum_null": {"max_abs_lsb": 1, "sample_offset": 0, "compared_samples": sample_count},
        "protected_silence_post_fx_sample_exact_pass": True,
        "clue_sfx_survival_pass": True,
        "scene3_lineage_preserved": True,
        "mono_survival_pass": True,
        "phone_proxy_survival_pass": True,
        "full_mix_metrics": {"integrated_lufs": -16.0, "true_peak_dbtp": -1.2, "lra_lu": 8.0},
    }


class P003BRenderQCHandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.contract = json.loads(CONTRACT_PATH.read_text(encoding="utf-8"))

    def run_gate(self, audio_sha=AUDIO_SHA, receipt_mutator=None):
        manifest = valid_manifest(self.contract)
        receipt = valid_receipt(manifest)
        if receipt_mutator:
            receipt_mutator(receipt, manifest)
        return evaluate_handoff(
            self.contract,
            manifest,
            receipt,
            audio_sha256=audio_sha,
            manifest_sha256=MANIFEST_SHA,
            receipt_sha256=RECEIPT_SHA,
        )

    def test_exact_qc_full_mix_identity_passes_handoff_only(self):
        result = self.run_gate()
        self.assertEqual(PASS, result["status"])
        self.assertTrue(result["handoff_authorized"])
        self.assertFalse(result["release_authority"])
        self.assertEqual(AUDIO_SHA, result["listener_audio_sha256"])
        self.assertEqual(AUDIO_SHA, result["qc_full_mix_sha256"])

    def test_different_listener_audio_bytes_are_rejected(self):
        result = self.run_gate(audio_sha="e" * 64)
        self.assertEqual(HOLD, result["status"])
        self.assertIn("listener_audio_not_same_bytes_as_qc_full_mix", result["reasons"])

    def test_machine_qc_failure_blocks_handoff(self):
        def mutate(receipt, manifest):
            receipt["full_mix_metrics"]["integrated_lufs"] = -18.0
        result = self.run_gate(receipt_mutator=mutate)
        self.assertEqual(HOLD, result["status"])
        self.assertIn("render_machine_qc_not_pass", result["reasons"])
        self.assertIn("integrated_lufs_out_of_profile", result["machine_qc_reasons"])

    def test_missing_full_mix_receipt_record_blocks(self):
        def mutate(receipt, manifest):
            target = manifest["full_mix"]["file_name"]
            receipt["outputs"] = [o for o in receipt["outputs"] if o["file_name"] != target]
        result = self.run_gate(receipt_mutator=mutate)
        self.assertEqual(HOLD, result["status"])
        self.assertIn("receipt_full_mix_record_missing_or_ambiguous", result["reasons"])

    def test_invalid_listener_audio_hash_blocks(self):
        result = self.run_gate(audio_sha="not-a-hash")
        self.assertEqual(HOLD, result["status"])
        self.assertIn("listener_audio_sha256_invalid", result["reasons"])

    def test_non_real_measurement_blocks(self):
        def mutate(receipt, manifest):
            receipt["measurement_source"] = "FIXTURE"
        result = self.run_gate(receipt_mutator=mutate)
        self.assertEqual(HOLD, result["status"])
        self.assertIn("render_machine_qc_not_pass", result["reasons"])


if __name__ == "__main__":
    unittest.main()
