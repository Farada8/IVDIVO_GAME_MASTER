import math
import unittest
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from post_render_contracts import (
    authorize_patch,
    canonical_interval,
    promotion_gate,
    protected_timing_coverage,
    validate_asset_binding,
    validate_headroom,
    validate_human_listen_evidence,
    validate_master_identity,
    validate_timing_evidence,
)

SHA_A = "a" * 64
SHA_B = "b" * 64


def block(block_id="B1", start=0.0, end=2.0, bed="ROOM_A", protected=False):
    return {
        "block_id": block_id,
        "scene_id": "S1",
        "room_id": "R1",
        "required_bed": bed,
        "required_cues": [],
        "prohibited": [],
        "evidence_grade": "ACCEPTED_ALIGNMENT",
        "timing_source": "alignment.json",
        "start_seconds": start,
        "end_seconds": end,
        "protected_pause": protected,
    }


def lineage(blocks=None, protected_global=None):
    return {"blocks": blocks or [block()], "protected_global": protected_global or []}


def binding(**overrides):
    obj = {
        "asset_id": "BED_A",
        "sha256": "c" * 64,
        "sample_rate_hz": 48000,
        "channels": 2,
        "gain_db": -18.0,
        "rights_status": "OWNED",
    }
    obj.update(overrides)
    return obj


def classification(start=0.25, end=1.25):
    return {
        "classification": "MISSING_ROOM_OR_AMBIENCE_SUPPORT",
        "patch_candidate": True,
        "start_seconds": start,
        "end_seconds": end,
    }


def authorize(**overrides):
    kwargs = {
        "classification": classification(),
        "lineage": lineage(),
        "source_master_expected_sha256": SHA_A,
        "source_master_actual_sha256": SHA_A,
        "asset_binding": binding(),
        "patch_id": "P1",
        "source_peak_dbfs": -8.0,
        "added_signal_peak_dbfs": -24.0,
    }
    kwargs.update(overrides)
    return authorize_patch(**kwargs)


class PostRenderContractTests(unittest.TestCase):
    def test_legacy_interval_read_alias_normalizes(self):
        out = canonical_interval({"start_s": 1, "end_s": 2.5})
        self.assertEqual(out["start_seconds"], 1.0)
        self.assertEqual(out["duration_seconds"], 1.5)

    def test_invalid_interval_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "INTERVAL_ORDER_INVALID"):
            canonical_interval({"start_seconds": 2, "end_seconds": 1})

    def test_directorial_timing_is_not_accepted_absolute_timing(self):
        with self.assertRaisesRegex(ValueError, "TIMING_EVIDENCE_NOT_ACCEPTED"):
            validate_timing_evidence({
                "evidence_grade": "DIRECTORIAL_INFERENCE", "source": "notes", "start_seconds": 0, "end_seconds": 1,
            })

    def test_protected_semantic_pause_without_timing_holds(self):
        b = block(protected=True)
        b.pop("start_seconds"); b.pop("end_seconds"); b["evidence_grade"] = "ROOM_CONTRACT_REQUIRED"
        out = protected_timing_coverage(lineage([b]))
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("B1", out["unresolved"])

    def test_master_hash_mismatch_blocks(self):
        with self.assertRaisesRegex(ValueError, "MASTER_IDENTITY_MISMATCH"):
            validate_master_identity(SHA_A, SHA_B)

    def test_asset_rights_required(self):
        with self.assertRaisesRegex(ValueError, "ASSET_RIGHTS_NOT_CLEARED"):
            validate_asset_binding(binding(rights_status="UNKNOWN"))

    def test_positive_gain_is_not_universal_failure(self):
        out = validate_asset_binding(binding(gain_db=2.0))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["gain_db"], 2.0)

    def test_nonfinite_gain_fails(self):
        with self.assertRaisesRegex(ValueError, "INVALID_NUMBER:gain_db"):
            validate_asset_binding(binding(gain_db=math.nan))

    def test_noncanonical_asset_sample_rate_holds(self):
        with self.assertRaisesRegex(ValueError, "ASSET_SAMPLE_RATE_NOT_CANONICAL"):
            validate_asset_binding(binding(sample_rate_hz=44100))

    def test_headroom_uses_amplitude_sum_not_db_addition(self):
        out = validate_headroom(source_peak_dbfs=-8.0, added_signal_peak_dbfs=-24.0)
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["prediction_model"], "WORST_CASE_COHERENT_AMPLITUDE_SUM")

    def test_headroom_preflight_holds_possible_clipping(self):
        out = validate_headroom(source_peak_dbfs=-1.2, added_signal_peak_dbfs=-10.0)
        self.assertEqual(out["status"], "HOLD_HEADROOM")
        self.assertGreater(out["predicted_peak_dbfs"], -1.0)

    def test_patch_authorization_passes_with_complete_evidence(self):
        out = authorize()
        self.assertEqual(out.status, "AUTHORIZED")
        self.assertEqual(len(out.authorization_hash), 64)

    def test_classifier_nomination_does_not_override_master_identity(self):
        out = authorize(source_master_actual_sha256=SHA_B)
        self.assertEqual(out.status, "HOLD")
        self.assertIn("MASTER_IDENTITY_MISMATCH", out.reasons)

    def test_unsafe_headroom_blocks_even_with_valid_classifier(self):
        out = authorize(source_peak_dbfs=-1.2, added_signal_peak_dbfs=-10.0)
        self.assertEqual(out.status, "HOLD")
        self.assertIn("HEADROOM_NOT_PROVEN", out.reasons)

    def test_unresolved_protected_pause_blocks_unrelated_auto_patch(self):
        protected = block("PB", protected=True)
        protected.pop("start_seconds"); protected.pop("end_seconds"); protected["evidence_grade"] = "ROOM_CONTRACT_REQUIRED"
        out = authorize(lineage=lineage([block(), protected]))
        self.assertIn("PROTECTED_TIMING_INCOMPLETE", out.reasons)

    def test_patch_overlapping_protected_range_blocks(self):
        protected = {
            "id": "SIL1", "evidence_grade": "LIVE_TIMELINE", "source": "timeline",
            "start_seconds": 0.5, "end_seconds": 0.8,
        }
        out = authorize(lineage=lineage(protected_global=[protected]))
        self.assertIn("PATCH_OVERLAPS_PROTECTED_RANGE", out.reasons)

    def test_cross_bed_domain_patch_blocks(self):
        out = authorize(
            classification=classification(0.5, 2.5),
            lineage=lineage([block("B1", 0, 2, "ROOM_A"), block("B2", 2, 4, "ROOM_B")]),
        )
        self.assertIn("PATCH_CROSSES_BED_DOMAINS", out.reasons)

    def test_human_listen_requires_real_provenance_fields(self):
        with self.assertRaisesRegex(ValueError, "HUMAN_LISTEN_PROVENANCE_MISSING"):
            validate_human_listen_evidence({"status": "PASS", "reviewer_type": "HUMAN_LISTENER"})

    def test_synthetic_project_cannot_promote_domain(self):
        out = promotion_gate([{
            "project_id": "P1", "synthetic_only": True, "locked_source": True,
            "real_audio_bytes": True, "real_defect_caught": True,
            "selective_repair_regression_pass": True, "human_listen_pass": True,
        }])
        self.assertEqual(out["status"], "HOLD")

    def test_two_independent_real_projects_only_create_promotion_eligibility(self):
        common = {
            "synthetic_only": False, "locked_source": True, "real_audio_bytes": True,
            "real_defect_caught": True, "selective_repair_regression_pass": True,
            "human_listen_pass": True,
        }
        out = promotion_gate([{"project_id": "P1", **common}, {"project_id": "P2", **common}])
        self.assertEqual(out["status"], "DOMAIN_PROMOTION_ELIGIBLE")
        self.assertEqual(out["qualified_projects"], ["P1", "P2"])
        self.assertFalse(out["machine_may_change_current_authority"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
