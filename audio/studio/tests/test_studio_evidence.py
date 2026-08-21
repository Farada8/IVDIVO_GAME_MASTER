import unittest
import sys
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "runtime"))
from external_evidence_trust import (
    DurableArtifactReceipt, ReadbackStrength, ReviewerAttestationReceipt,
    TransactionRecoveryReceipt,
)
from provider_snapshot_contract import SCHEMA_VERSION, seal_snapshot
from studio_evidence import (
    AUDIO_MODES, QUALITY_DIMENSIONS, EconomicsRecord, PerformanceEvidence,
    build_benchmark_manifest, compare_benchmark, compress_human_review,
    economics_report, performance_evidence_gate, score_benchmark_variant,
    studio_release_evidence_matrix, text_hash,
)


class StudioEvidenceTests(unittest.TestCase):
    TEXT = "hello world"
    HASH = text_hash(TEXT)
    NOW = datetime(2026, 8, 21, 18, 0, tzinfo=timezone.utc)

    @staticmethod
    def h(value):
        return sha256(value.encode("utf-8")).hexdigest()

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

    def durable(self, *, kind="RAW_AUDIO", content_hash=None, metadata=None, strength=None, artifact_id="A1", transaction_id="TX1"):
        content_hash = content_hash or self.h(artifact_id)
        return DurableArtifactReceipt(
            artifact_id=artifact_id,
            artifact_kind=kind,
            storage_provider="GOOGLE_DRIVE",
            source_ref=f"gdrive://{artifact_id}",
            content_hash=content_hash,
            size_bytes=128,
            written_at="2026-08-21T17:00:00+00:00",
            readback_at="2026-08-21T17:01:00+00:00",
            readback_hash=content_hash,
            readback_strength=strength or ReadbackStrength.CONTENT_HASH_VERIFIED.value,
            transaction_id=transaction_id,
            metadata=metadata or {},
        )

    def human_receipt(self, scope, *, candidate_hash=None, suffix="1"):
        submission_hash = self.h(f"submission:{scope}:{suffix}")
        return ReviewerAttestationReceipt(
            reviewer_ref=f"reviewer://human-{suffix}",
            reviewer_identity_class="TRUSTED_HUMAN_REVIEWER",
            submission_ref=f"form://submission-{scope}-{suffix}",
            submission_hash=submission_hash,
            task_pack_hash=self.h(f"task:{scope}"),
            artifact_hash=self.h("audio"),
            candidate_hash=candidate_hash or self.h("candidate"),
            decision="PASS",
            submitted_at="2026-08-21T17:02:00+00:00",
            review_scope=scope,
            synthetic_fixture=False,
            durable_receipt=self.durable(
                kind="HUMAN_ATTESTATION",
                content_hash=submission_hash,
                artifact_id=f"H-{scope}-{suffix}",
            ),
        )

    def provider_payload(self):
        snapshot = seal_snapshot({
            "schema_version": SCHEMA_VERSION,
            "provider": "generic-provider",
            "status": "PASS",
            "authentication": {"state": "AUTHENTICATED", "method": "RUNTIME_AUTH", "credential_persisted": False},
            "provenance": {
                "captured_at": "2026-08-21T17:30:00+00:00",
                "capture_method": "DIRECT_AUTHENTICATED_READ_ONLY_API",
                "capture_engine": "test-provider-acquirer/1.0",
                "source": [{"path": "/capabilities", "http_status": 200}],
            },
            "account": {"fingerprint_sha256": self.h("account")},
            "voices": {"v1": {"name": "Voice"}},
            "models": {"m1": {"name": "Model"}},
        })
        return {
            "snapshot": snapshot,
            "durable_receipt": self.durable(
                kind="PROVIDER_SNAPSHOT", content_hash=snapshot["snapshot_hash"], artifact_id="PROVIDER"
            ),
        }

    def valid_release_evidence(self):
        live = self.durable(
            kind="RAW_AUDIO",
            artifact_id="LIVE",
            metadata={
                "project_id": "P1",
                "request_hash": self.h("request"),
                "provider_response_hash": self.h("response"),
            },
        )
        alignment = self.durable(
            kind="ALIGNMENT",
            artifact_id="ALIGN",
            metadata={"audio_hash": live.content_hash, "source_hash": self.h("source"), "coverage_complete": True},
        )
        economics = self.durable(
            kind="ECONOMICS_LEDGER",
            artifact_id="ECON",
            metadata={
                "measured": True,
                "provider_charge_refs": ["provider://charge-1"],
                "manual_minutes_source_ref": "log://human-minutes",
            },
        )
        cross = self.durable(
            kind="CROSS_PROJECT_LIVE_REPORT",
            artifact_id="CROSS",
            metadata={
                "project_ids": ["P1", "P2"],
                "live_evidence_hashes": [live.content_hash, self.h("live-p2")],
            },
        )
        recovery = TransactionRecoveryReceipt(
            transaction_id="TX1",
            recovered_at="2026-08-21T17:10:00+00:00",
            recovered_content_hashes=[live.content_hash, alignment.content_hash],
            durable_readback_strength=ReadbackStrength.TRANSACTION_RECOVERABLE.value,
            duplicate_provider_calls=0,
            duplicate_charges=0,
            unresolved_ambiguities=0,
            recovery_manifest_ref="gdrive://recovery-1",
            recovery_manifest_hash=self.h("recovery"),
            synthetic_fixture=False,
        )
        return {
            "locked_source_identity": True,
            "production_control_on_main": True,
            "provider_preflight_pass": self.provider_payload(),
            "live_render_provenance": live,
            "real_alignment_timeline": alignment,
            "performance_human_pass": self.human_receipt("PERFORMANCE"),
            "blind_listener_pass": self.human_receipt("BLIND_LISTENER", suffix="2"),
            "measured_economics": economics,
            "durable_raw_assets": live,
            "durable_recovery": recovery,
            "cross_project_live_portability": cross,
        }

    def release(self, evidence):
        return studio_release_evidence_matrix(
            evidence,
            expected_provider="generic-provider",
            provider_max_age_seconds=3600,
            now=self.NOW,
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

    def test_performance_booleans_alone_do_not_authorize(self):
        evidence = PerformanceEvidence("c", "r", True, True, True, True, human_scores={"natural": 4})
        out = performance_evidence_gate(evidence)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("trusted_human_review_evidence", out["missing"])
        self.assertFalse(out["production_authoritative"])

    def test_performance_trusted_receipts_make_candidate_eligible_not_locked(self):
        candidate_hash = text_hash("r:c")
        receipts = {
            "multi_state": self.human_receipt("MULTI_STATE", candidate_hash=candidate_hash, suffix="ms"),
            "pronunciation": self.human_receipt("PRONUNCIATION", candidate_hash=candidate_hash, suffix="pr"),
            "fatigue": self.human_receipt("FATIGUE", candidate_hash=candidate_hash, suffix="ft"),
            "human_review": self.human_receipt("PERFORMANCE", candidate_hash=candidate_hash, suffix="hr"),
        }
        evidence = PerformanceEvidence(
            "c", "r", True, True, True, True,
            human_scores={"natural": 4}, trusted_human_evidence=receipts,
        )
        out = performance_evidence_gate(evidence)
        self.assertEqual(out["status"], "ELIGIBLE_FOR_HUMAN_LOCK_DECISION")
        self.assertTrue(out["production_authoritative"])
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

    def test_release_all_true_booleans_are_not_external_evidence(self):
        keys = ("locked_source_identity", "production_control_on_main", "provider_preflight_pass",
                "live_render_provenance", "real_alignment_timeline", "performance_human_pass",
                "blind_listener_pass", "measured_economics", "durable_raw_assets", "durable_recovery",
                "cross_project_live_portability")
        out = studio_release_evidence_matrix({key: True for key in keys})
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("provider_preflight_pass", out["missing"])
        self.assertFalse(out["production_ready"])

    def test_release_complete_receipts_still_need_founder(self):
        out = self.release(self.valid_release_evidence())
        self.assertEqual(out["status"], "GO_FOR_FOUNDER_RELEASE_DECISION")
        self.assertEqual(out["missing"], [])
        self.assertEqual(out["lineage_validation"]["status"], "PASS")
        self.assertFalse(out["production_ready"])
        self.assertFalse(out["machine_may_declare_production_ready"])

    def test_release_holds_if_alignment_belongs_to_other_live_audio(self):
        evidence = self.valid_release_evidence()
        alignment = evidence["real_alignment_timeline"]
        evidence["real_alignment_timeline"] = self.durable(
            kind="ALIGNMENT",
            artifact_id="ALIGN2",
            metadata={"audio_hash": self.h("other-live"), "source_hash": self.h("source"), "coverage_complete": True},
        )
        recovery = evidence["durable_recovery"]
        evidence["durable_recovery"] = TransactionRecoveryReceipt(
            transaction_id=recovery.transaction_id,
            recovered_at=recovery.recovered_at,
            recovered_content_hashes=[evidence["live_render_provenance"].content_hash, evidence["real_alignment_timeline"].content_hash],
            durable_readback_strength=recovery.durable_readback_strength,
            duplicate_provider_calls=0,
            duplicate_charges=0,
            unresolved_ambiguities=0,
            recovery_manifest_ref=recovery.recovery_manifest_ref,
            recovery_manifest_hash=recovery.recovery_manifest_hash,
            synthetic_fixture=False,
        )
        out = self.release(evidence)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("cross_class_lineage", out["missing"])
        self.assertIn("ALIGNMENT_NOT_BOUND_TO_CURRENT_LIVE_AUDIO", out["lineage_validation"]["issues"])
        self.assertNotEqual(alignment.content_hash, evidence["real_alignment_timeline"].content_hash)

    def test_release_holds_if_recovery_omits_current_alignment(self):
        evidence = self.valid_release_evidence()
        recovery = evidence["durable_recovery"]
        evidence["durable_recovery"] = TransactionRecoveryReceipt(
            transaction_id=recovery.transaction_id,
            recovered_at=recovery.recovered_at,
            recovered_content_hashes=[evidence["live_render_provenance"].content_hash, self.h("other-alignment")],
            durable_readback_strength=recovery.durable_readback_strength,
            duplicate_provider_calls=0,
            duplicate_charges=0,
            unresolved_ambiguities=0,
            recovery_manifest_ref=recovery.recovery_manifest_ref,
            recovery_manifest_hash=recovery.recovery_manifest_hash,
            synthetic_fixture=False,
        )
        out = self.release(evidence)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("RECOVERY_MISSING_CURRENT_ALIGNMENT", out["lineage_validation"]["issues"])

    def test_release_holds_if_recovery_transaction_is_unrelated(self):
        evidence = self.valid_release_evidence()
        recovery = evidence["durable_recovery"]
        evidence["durable_recovery"] = TransactionRecoveryReceipt(
            transaction_id="TX-OTHER",
            recovered_at=recovery.recovered_at,
            recovered_content_hashes=recovery.recovered_content_hashes,
            durable_readback_strength=recovery.durable_readback_strength,
            duplicate_provider_calls=0,
            duplicate_charges=0,
            unresolved_ambiguities=0,
            recovery_manifest_ref=recovery.recovery_manifest_ref,
            recovery_manifest_hash=recovery.recovery_manifest_hash,
            synthetic_fixture=False,
        )
        out = self.release(evidence)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("RECOVERY_TRANSACTION_NOT_CURRENT_LIVE_TRANSACTION", out["lineage_validation"]["issues"])

    def test_release_holds_if_cross_project_report_omits_current_lineage(self):
        evidence = self.valid_release_evidence()
        evidence["cross_project_live_portability"] = self.durable(
            kind="CROSS_PROJECT_LIVE_REPORT",
            artifact_id="CROSS2",
            metadata={
                "project_ids": ["P2", "P3"],
                "live_evidence_hashes": [self.h("live-p2"), self.h("live-p3")],
            },
        )
        out = self.release(evidence)
        self.assertEqual(out["status"], "HOLD")
        self.assertIn("CROSS_PROJECT_REPORT_MISSING_CURRENT_PROJECT", out["lineage_validation"]["issues"])
        self.assertIn("CROSS_PROJECT_REPORT_MISSING_CURRENT_LIVE_HASH", out["lineage_validation"]["issues"])


if __name__ == "__main__":
    unittest.main()
