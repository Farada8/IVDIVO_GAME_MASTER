from __future__ import annotations

import unittest

from core.artifact_placement import PERSISTED_BUT_MISPLACED, PLACEMENT_VERIFIED
from core.artifact_placement_adapters import PlacementIntent
from core.connector_placement_capture import (
    ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW,
    POST_CLAIM_INCIDENT_NOT_PROSPECTIVE,
    REAL_PROVIDER_READBACK,
    REPLAY,
    TEST_FIXTURE,
    TEST_ONLY_NOT_LIVE_EVIDENCE,
    UNVERIFIED_ORIGIN,
    VERIFIED_PLACEMENT_OBSERVATION,
    capture_from_drive_readback,
    capture_from_github_readback,
    capture_from_receipt,
)

CAPTURED_AT = "2026-08-22T12:15:00+01:00"


def drive_intent(expected_type: str = "DOCUMENT") -> PlacementIntent:
    return PlacementIntent(
        project_root="drive:project-root",
        expected_parent="drive:canonical-folder",
        start_here_ref="drive:start-here",
        cross_store_required=False,
        expected_resource_type=expected_type,
    )


def good_receipt() -> dict:
    return {
        "artifact_id": "drive:artifact-1",
        "provider": "GOOGLE_DRIVE",
        "project_root": "drive:project-root",
        "expected_parent": "drive:canonical-folder",
        "actual_parent": "drive:canonical-folder",
        "artifact_exists": True,
        "start_here_ref": "drive:start-here",
        "start_here_readback_ok": True,
        "start_here_mentions_artifact": True,
        "legacy_conflicts": [],
        "cross_store_required": False,
        "cross_store_pointer_present": False,
        "expected_resource_type": "DOCUMENT",
        "observed_resource_type": "DOCUMENT",
    }


class ConnectorPlacementCaptureTest(unittest.TestCase):
    def test_real_drive_wrong_type_before_claim_is_live_review_candidate_not_proof(self) -> None:
        capture = capture_from_drive_readback(
            intent=drive_intent(),
            artifact_metadata={
                "id": "artifact-1",
                "parent_ids": ["canonical-folder"],
                "mime_type": "application/vnd.google-apps.folder",
            },
            start_here_readback_ok=True,
            start_here_mentions_artifact=True,
            provider_readback_ref="drive-metadata:artifact-1:rev-7",
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.receipt.status, PERSISTED_BUT_MISPLACED)
        self.assertIn("resource_type_mismatch", capture.receipt.failures())
        self.assertEqual(capture.review_status, ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW)
        self.assertFalse(capture.promotion_proof)
        self.assertTrue(capture.independent_review_required)

    def test_real_github_wrong_parent_before_claim_is_live_review_candidate_not_proof(self) -> None:
        intent = PlacementIntent(
            project_root="github:Farada8/IVDIVO_GAME_MASTER",
            expected_parent="github:Farada8/IVDIVO_GAME_MASTER:canonical/path",
            start_here_ref="github:Farada8/IVDIVO_GAME_MASTER:CURRENT.md",
            expected_resource_type="FILE",
        )
        capture = capture_from_github_readback(
            intent=intent,
            repository_full_name="Farada8/IVDIVO_GAME_MASTER",
            path="wrong/path/result.md",
            file_observed=True,
            current_index_readback_ok=True,
            current_index_mentions_artifact=True,
            provider_readback_ref="github-contents:result.md:sha123",
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.receipt.status, PERSISTED_BUT_MISPLACED)
        self.assertIn("parent_mismatch", capture.receipt.failures())
        self.assertEqual(capture.review_status, ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW)
        self.assertFalse(capture.to_dict()["promotion_proof"])

    def test_verified_real_readback_is_placement_observation_not_failure_proof(self) -> None:
        capture = capture_from_receipt(
            good_receipt(),
            evidence_origin=REAL_PROVIDER_READBACK,
            provider_readback_ref="drive-metadata:artifact-1:rev-8",
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.receipt.status, PLACEMENT_VERIFIED)
        self.assertEqual(capture.review_status, VERIFIED_PLACEMENT_OBSERVATION)
        self.assertFalse(capture.promotion_proof)

    def test_test_fixture_never_becomes_live_evidence(self) -> None:
        data = good_receipt(); data["actual_parent"] = "drive:wrong"
        capture = capture_from_receipt(
            data,
            evidence_origin=TEST_FIXTURE,
            provider_readback_ref="fixture:wrong-parent",
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.review_status, TEST_ONLY_NOT_LIVE_EVIDENCE)
        self.assertFalse(capture.promotion_proof)

    def test_replay_never_becomes_live_evidence(self) -> None:
        data = good_receipt(); data["actual_parent"] = "drive:wrong"
        capture = capture_from_receipt(
            data,
            evidence_origin=REPLAY,
            provider_readback_ref="historic:#395",
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.review_status, TEST_ONLY_NOT_LIVE_EVIDENCE)

    def test_real_mismatch_after_claim_is_retrospective_not_prospective(self) -> None:
        data = good_receipt(); data["actual_parent"] = "drive:wrong"
        capture = capture_from_receipt(
            data,
            evidence_origin=REAL_PROVIDER_READBACK,
            provider_readback_ref="drive-metadata:artifact-1:rev-9",
            captured_before_completion_claim=False,
            completion_claim_emitted=True,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.review_status, POST_CLAIM_INCIDENT_NOT_PROSPECTIVE)
        self.assertFalse(capture.promotion_proof)

    def test_real_origin_without_provider_ref_is_unverified(self) -> None:
        data = good_receipt(); data["actual_parent"] = "drive:wrong"
        capture = capture_from_receipt(
            data,
            evidence_origin=REAL_PROVIDER_READBACK,
            provider_readback_ref=None,
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.review_status, UNVERIFIED_ORIGIN)

    def test_unknown_origin_is_unverified(self) -> None:
        data = good_receipt(); data["actual_parent"] = "drive:wrong"
        capture = capture_from_receipt(
            data,
            evidence_origin="UNKNOWN",
            provider_readback_ref="some-ref",
            captured_before_completion_claim=True,
            completion_claim_emitted=False,
            captured_at=CAPTURED_AT,
        )
        self.assertEqual(capture.review_status, UNVERIFIED_ORIGIN)

    def test_invalid_origin_rejected(self) -> None:
        with self.assertRaises(ValueError):
            capture_from_receipt(
                good_receipt(),
                evidence_origin="CLAIMED_REAL",
                provider_readback_ref="x",
                captured_before_completion_claim=True,
                completion_claim_emitted=False,
                captured_at=CAPTURED_AT,
            )

    def test_capture_requires_caller_supplied_timestamp(self) -> None:
        with self.assertRaises(ValueError):
            capture_from_receipt(
                good_receipt(),
                evidence_origin=REAL_PROVIDER_READBACK,
                provider_readback_ref="x",
                captured_before_completion_claim=True,
                completion_claim_emitted=False,
                captured_at="",
            )


if __name__ == "__main__":
    unittest.main()
