import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from studio_evidence import (
    AUDIO_MODES, QUALITY_DIMENSIONS, EconomicsRecord, PerformanceEvidence,
    build_benchmark_manifest, compare_benchmark, compress_human_review,
    economics_report, performance_evidence_gate, score_benchmark_variant,
    studio_release_evidence_matrix, text_hash,
)


class StudioEvidenceTests(unittest.TestCase):
    TEXT = "hello world"
    HASH = text_hash(TEXT)

    def variants(self, assets=True):
        return [
            {
                "mode": mode,
                "exact_text_hash": self.HASH,
                "source_hash": "source",
                "render_asset_hash": mode + "_hash" if assets else None,
                "duration_seconds": 60 if assets else None,
            }
            for mode in AUDIO_MODES
        ]

    def good_score(self, mode):
        return score_benchmark_variant(
            mode=mode,
            human_scores={key: 4 for key in QUALITY_DIMENSIONS},
            duration_seconds=60,
            provider_cost=1,
            manual_minutes=6,
            manual_hourly_cost=20,
        )

    def test_manifest_pass(self):
        out = build_benchmark_manifest(source_id="x", source_hash="source", exact_text=self.TEXT, variants=self.variants())
        self.assertEqual(out["status"], "READY_FOR_EVALUATION")
        self.assertEqual(len(out["variants"]), 3)

    def test_manifest_missing_mode_fails(self):
        with self.assertRaises(ValueError):
            build_benchmark_manifest(source_id="x", source_hash="source", exact_text=self.TEXT, variants=self.variants()[:2])

    def test_manifest_text_drift_fails(self):
        variants = self.variants(); variants[0]["exact_text_hash"] = "bad"
        with self.assertRaises(ValueError):
            build_benchmark_manifest(source_id="x", source_hash="source", exact_text=self.TEXT, variants=variants)

    def test_manifest_source_drift_fails(self):
        variants = self.variants(); variants[0]["source_hash"] = "other"
        with self.assertRaises(ValueError):
            build_benchmark_manifest(source_id="x", source_hash="source", exact_text=self.TEXT, variants=variants)

    def test_manifest_hold_without_assets(self):
        out = build_benchmark_manifest(source_id="x", source_hash="source", exact_text=self.TEXT, variants=self.variants(False))
        self.assertEqual(out["status"], "HOLD_FOR_RENDER_EVIDENCE")

    def test_score_complete(self):
        score = self.good_score("NARRATED")
        self.assertEqual(score["status"], "PASS_EVIDENCE_COMPLETE")
        self.assertEqual(score["cost_per_accepted_minute"], 3)

    def test_score_missing_human(self):
        score = score_benchmark_variant(mode="NARRATED", human_scores={}, duration_seconds=60,
                                        provider_cost=1, manual_minutes=1, manual_hourly_cost=1)
        self.assertEqual(score["status"], "HOLD_HUMAN_SCORES")

    def test_score_missing_cost(self):
        score = score_benchmark_variant(mode="NARRATED", human_scores={key: 4 for key in QUALITY_DIMENSIONS},
                                        duration_seconds=60, provider_cost=None, manual_minutes=1, manual_hourly_cost=1)
        self.assertEqual(score["status"], "HOLD_COST_EVIDENCE")

    def test_score_bad_range_fails(self):
        scores = {key: 4 for key in QUALITY_DIMENSIONS}; scores["clarity"] = 6
        with self.assertRaises(ValueError):
            score_benchmark_variant(mode="NARRATED", human_scores=scores, duration_seconds=60,
                                    provider_cost=1, manual_minutes=1, manual_hourly_cost=1)

    def test_compare_holds_on_incomplete_mode(self):
        scores = [self.good_score(mode) for mode in AUDIO_MODES]; scores[0]["status"] = "HOLD"
        self.assertEqual(compare_benchmark(scores)["status"], "HOLD")

    def test_compare_never_auto_selects(self):
        scores = [self.good_score(mode) for mode in AUDIO_MODES]; scores[1]["quality_mean_0_5"] = 4.5
        out = compare_benchmark(scores)
        self.assertEqual(out["status"], "REVIEW_REQUIRED")
        self.assertIsNone(out["winner"])
        self.assertFalse(out["auto_select"])

    def test_performance_hold(self):
        self.assertEqual(performance_evidence_gate(PerformanceEvidence("c", "r"))["status"], "HOLD")

    def test_performance_eligible_not_locked(self):
        evidence = PerformanceEvidence("c", "r", True, True, True, True, human_scores={"natural": 4})
        out = performance_evidence_gate(evidence)
        self.assertEqual(out["status"], "ELIGIBLE_FOR_HUMAN_LOCK_DECISION")
        self.assertFalse(out["voice_lock"])

    def test_pair_required(self):
        evidence = PerformanceEvidence("c", "r", True, True, True, True, pair=False, human_scores={"natural": 4})
        self.assertIn("pair", performance_evidence_gate(evidence, pair_required=True)["missing"])

    def test_hard_fail(self):
        evidence = PerformanceEvidence("c", "r", True, True, True, True, human_scores={"natural": 3}, hard_fails=["ROBOT"])
        self.assertEqual(performance_evidence_gate(evidence)["status"], "FAIL_HARD")

    def test_human_review_plan(self):
        flags = [{"start": 10, "end": 15, "severity": "MAJOR", "confidence": .9},
                 {"start": 50, "end": 52, "severity": "MINOR", "confidence": .5}]
        out = compress_human_review(flags, total_duration_seconds=600)
        self.assertEqual(out["status"], "PASS_REVIEW_PLAN")
        self.assertTrue(out["full_blind_listen_required_for_final_acceptance"])

    def test_fatal_always_selected(self):
        flags = [{"start": 0, "end": 100, "severity": "FATAL"}, {"start": 101, "end": 102, "severity": "MAJOR"}]
        out = compress_human_review(flags, total_duration_seconds=1000, max_fraction=.01, min_seconds=1)
        self.assertEqual(out["selected"][0]["severity"], "FATAL")

    def test_bad_interval_fails(self):
        with self.assertRaises(ValueError):
            compress_human_review([{"start": 5, "end": 2}], total_duration_seconds=10)

    def record(self, **changes):
        row = dict(render_id="r", mode="NARRATED", generated_seconds=120, accepted_seconds=60,
                   provider_cost=1, manual_minutes=6, manual_hourly_cost=20,
                   cache_reused_seconds=30, regeneration_seconds=20)
        row.update(changes)
        return EconomicsRecord(**row)

    def test_economics_pass(self):
        out = economics_report([self.record()])
        self.assertEqual(out["status"], "PASS_EVIDENCE_COMPLETE")
        self.assertEqual(out["cost_per_accepted_minute"], 3)

    def test_economics_missing(self):
        self.assertEqual(economics_report([self.record(provider_cost=None)])["status"], "HOLD_MISSING_EVIDENCE")

    def test_economics_no_accepted_fails(self):
        with self.assertRaises(ValueError):
            economics_report([self.record(accepted_seconds=0)])

    def test_economics_negative_fails(self):
        with self.assertRaises(ValueError):
            economics_report([self.record(provider_cost=-1)])

    def test_release_holds(self):
        self.assertEqual(studio_release_evidence_matrix({})["status"], "HOLD")

    def test_release_complete_still_needs_founder(self):
        keys = ("locked_source_identity", "production_control_on_main", "provider_preflight_pass",
                "live_render_provenance", "real_alignment_timeline", "performance_human_pass",
                "blind_listener_pass", "measured_economics", "durable_raw_assets",
                "cross_project_live_portability")
        out = studio_release_evidence_matrix({key: True for key in keys})
        self.assertEqual(out["status"], "GO_FOR_FOUNDER_RELEASE_DECISION")
        self.assertFalse(out["production_ready"])
        self.assertFalse(out["machine_may_declare_production_ready"])


if __name__ == "__main__":
    unittest.main()
