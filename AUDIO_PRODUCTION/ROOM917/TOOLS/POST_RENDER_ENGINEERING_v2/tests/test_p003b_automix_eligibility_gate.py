from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve()
TOOL_DIR = HERE.parents[1]
sys.path.insert(0, str(TOOL_DIR))

from p003b_automix_eligibility_gate import HOLD, PASS, evaluate  # noqa: E402

MANIFEST_SHA = "a" * 64
RECEIPT_SHA = "b" * 64
HANDOFF_SHA = "c" * 64
AUDIO_SHA = "d" * 64
FULL_NAME = "ROOM917_E01_FULLMIX_48k24.wav"


def valid_manifest():
    return {
        "schema_version": "ivdivo.room917_render_manifest_result/1.0",
        "status": "PASS_RENDER_MANIFEST_COMPILED",
        "render_authority": True,
        "release_authority": False,
        "full_mix": {"file_name": FULL_NAME},
    }


def valid_receipt():
    return {
        "schema_version": "ivdivo.room917_render_machine_qc_result/1.0",
        "status": "PASS_RENDER_MACHINE_QC",
        "render_receipt_accepted": True,
        "release_authority": False,
        "outputs": [{"file_name": FULL_NAME, "sha256": AUDIO_SHA}],
    }


def valid_handoff():
    return {
        "schema_version": "ivdivo.room917_p003b_render_qc_handoff/1.0",
        "status": "PASS_P003B_RENDER_QC_HANDOFF",
        "handoff_authorized": True,
        "release_authority": False,
        "manifest_sha256": MANIFEST_SHA,
        "receipt_sha256": RECEIPT_SHA,
        "listener_audio_sha256": AUDIO_SHA,
        "qc_full_mix_sha256": AUDIO_SHA,
    }


class P003BAutoMixEligibilityGateTests(unittest.TestCase):
    def run_gate(self, manifest=None, receipt=None, handoff=None, audio_sha=AUDIO_SHA):
        return evaluate(
            manifest=manifest if manifest is not None else valid_manifest(),
            receipt=receipt if receipt is not None else valid_receipt(),
            handoff=handoff if handoff is not None else valid_handoff(),
            manifest_sha256=MANIFEST_SHA,
            receipt_sha256=RECEIPT_SHA,
            handoff_sha256=HANDOFF_SHA,
            audio_sha256=audio_sha,
        )

    def assert_hold(self, result, reason):
        self.assertEqual(HOLD, result["status"])
        self.assertFalse(result["eligible_for_p003b_packaging"])
        self.assertFalse(result["release_authority"])
        self.assertIn(reason, result["reasons"])

    def test_valid_automix_chain_is_eligible_but_not_released(self):
        result = self.run_gate()
        self.assertEqual(PASS, result["status"])
        self.assertTrue(result["eligible_for_p003b_packaging"])
        self.assertFalse(result["release_authority"])
        self.assertEqual("AUTOMIX_V1", result["pipeline"])

    def test_failed_render_qc_blocks(self):
        receipt = valid_receipt()
        receipt["status"] = "HOLD_RENDER_MACHINE_QC"
        self.assert_hold(self.run_gate(receipt=receipt), "render_machine_qc_not_pass")

    def test_failed_handoff_blocks(self):
        handoff = valid_handoff()
        handoff["status"] = "HOLD_P003B_RENDER_QC_HANDOFF"
        self.assert_hold(self.run_gate(handoff=handoff), "p003b_render_qc_handoff_not_pass")

    def test_different_audio_bytes_block(self):
        self.assert_hold(self.run_gate(audio_sha="e" * 64), "handoff_listener_audio_sha256_mismatch")

    def test_manifest_identity_drift_blocks(self):
        handoff = valid_handoff()
        handoff["manifest_sha256"] = "e" * 64
        self.assert_hold(self.run_gate(handoff=handoff), "handoff_manifest_sha256_mismatch")

    def test_receipt_identity_drift_blocks(self):
        handoff = valid_handoff()
        handoff["receipt_sha256"] = "e" * 64
        self.assert_hold(self.run_gate(handoff=handoff), "handoff_receipt_sha256_mismatch")

    def test_full_mix_record_missing_blocks(self):
        receipt = valid_receipt()
        receipt["outputs"] = []
        self.assert_hold(self.run_gate(receipt=receipt), "qc_full_mix_record_missing_or_ambiguous")

    def test_full_mix_record_wrong_hash_blocks(self):
        receipt = valid_receipt()
        receipt["outputs"][0]["sha256"] = "f" * 64
        self.assert_hold(self.run_gate(receipt=receipt), "qc_full_mix_record_sha256_mismatch")

    def test_invalid_manifest_schema_blocks(self):
        manifest = valid_manifest()
        manifest["schema_version"] = "legacy"
        self.assert_hold(self.run_gate(manifest=manifest), "render_manifest_schema_invalid")

    def test_authority_boundary_blocks_machine_release(self):
        receipt = valid_receipt()
        receipt["release_authority"] = True
        self.assert_hold(self.run_gate(receipt=receipt), "render_machine_qc_authority_boundary_invalid")


if __name__ == "__main__":
    unittest.main()
