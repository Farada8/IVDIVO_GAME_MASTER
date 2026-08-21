import unittest
from pathlib import Path
import sys

RUNTIME = Path(__file__).resolve().parents[1] / "runtime"
sys.path.insert(0, str(RUNTIME))

from post_render_learning import (
    build_improvement_event,
    domain_promotion_review,
    normalize_metrics,
    project_leakage_scan,
    reconcile_learning_events,
)


class PostRenderLearningTests(unittest.TestCase):
    def event(self, **overrides):
        kwargs = {
            "event_id": "E1",
            "project_id": "PROJECT_A",
            "mechanism_id": "POST_RENDER_AUTHORIZATION",
            "problem_class": "PATCH_AUTHORITY_TOO_WEAK",
            "earliest_failure_layer": "AUTHORIZATION",
            "evidence_refs": [{"evidence_class": "STATIC_CODE", "ref": "commit:abc"}],
            "candidate_delta": "Separate classifier nomination from byte-touch authorization.",
            "regression_results": [{"id": "T1", "status": "PASS"}],
            "metrics": {"rework_cycles": 1, "human_minutes": 0},
            "synthetic_only": True,
            "forbidden_project_tokens": ["greyhaven", "cate reed"],
        }
        kwargs.update(overrides)
        return build_improvement_event(**kwargs)

    def test_negative_metrics_fail(self):
        with self.assertRaisesRegex(ValueError, "NEGATIVE_METRIC"):
            normalize_metrics({"provider_spend": -1})

    def test_project_leakage_scan_detects_token(self):
        out = project_leakage_scan("Never transfer Greyhaven cue facts", ["Greyhaven"])
        self.assertEqual(out["status"], "FAIL_PROJECT_LEAKAGE")

    def test_event_rejects_story_fact_leakage(self):
        with self.assertRaisesRegex(ValueError, "PROJECT_STORY_CONTENT_LEAKAGE"):
            self.event(candidate_delta="Copy Greyhaven Scene3 timing into universal runtime.")

    def test_event_requires_evidence(self):
        with self.assertRaisesRegex(ValueError, "IMPROVEMENT_EVENT_EVIDENCE_REQUIRED"):
            self.event(evidence_refs=[])

    def test_event_has_deterministic_hash_and_no_promotion_claim(self):
        event = self.event()
        self.assertEqual(event["promotion_claim"], "NONE")
        self.assertEqual(len(event["event_hash"]), 64)
        event2 = self.event()
        self.assertEqual(event["event_hash"], event2["event_hash"])

    def test_regression_failure_holds_learning_event(self):
        event = self.event(regression_results=[{"id": "T1", "status": "FAIL"}])
        self.assertEqual(event["regression_gate"], "HOLD")

    def test_duplicate_evidence_family_counts_once(self):
        a = self.event(event_id="E1")
        b = self.event(event_id="E2")
        for item in (a, b):
            item["evidence_family"] = "ROOM917_E01"
        out = reconcile_learning_events([a, b])
        self.assertEqual(out["independent_count"], 1)
        self.assertEqual(out["duplicates_collapsed"][0]["count"], 2)

    def test_one_real_project_remains_hold(self):
        common = {
            "synthetic_only": False,
            "locked_source": True,
            "real_audio_bytes": True,
            "real_defect_caught": True,
            "selective_repair_regression_pass": True,
            "human_listen_pass": True,
        }
        out = domain_promotion_review([{"project_id": "P1", **common}])
        self.assertEqual(out["status"], "HOLD")
        self.assertFalse(out["machine_may_change_current_authority"])

    def test_two_real_projects_create_founder_review_candidate_not_auto_authority(self):
        common = {
            "synthetic_only": False,
            "locked_source": True,
            "real_audio_bytes": True,
            "real_defect_caught": True,
            "selective_repair_regression_pass": True,
            "human_listen_pass": True,
        }
        out = domain_promotion_review([
            {"project_id": "P1", **common},
            {"project_id": "P2", **common},
        ])
        self.assertEqual(out["status"], "DOMAIN_PROMOTION_ELIGIBLE")
        self.assertEqual(out["self_improvement_decision"], "ACCEPT_DOMAIN_MECHANISM_CANDIDATE_FOR_FOUNDER_REVIEW")
        self.assertFalse(out["machine_may_change_current_authority"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
