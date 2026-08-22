from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.artifact_placement import NOT_PERSISTED, PERSISTED_BUT_MISPLACED, PLACEMENT_VERIFIED, ArtifactPlacementReceipt
from projects.artifact_completion import complete_task_with_artifact_gate
from projects.manager import ProjectStateManager


def good_receipt() -> dict:
    return {
        "artifact_id": "drive:artifact-1",
        "provider": "GOOGLE_DRIVE",
        "project_root": "drive:project-root",
        "expected_parent": "drive:canonical-child",
        "actual_parent": "drive:canonical-child",
        "artifact_exists": True,
        "start_here_ref": "drive:start-here",
        "start_here_readback_ok": True,
        "start_here_mentions_artifact": True,
        "legacy_conflicts": [],
        "cross_store_required": True,
        "cross_store_pointer_present": True,
    }


class ArtifactPlacementRuntimeTest(unittest.TestCase):
    def test_verified_receipt(self):
        self.assertEqual(ArtifactPlacementReceipt.from_mapping(good_receipt()).status, PLACEMENT_VERIFIED)

    def test_backward_compatible_receipt_without_resource_type(self):
        receipt = ArtifactPlacementReceipt.from_mapping(good_receipt())
        self.assertIsNone(receipt.expected_resource_type)
        self.assertEqual(receipt.status, PLACEMENT_VERIFIED)

    def test_expected_document_observed_folder_fails_closed(self):
        data = good_receipt(); data["expected_resource_type"] = "DOCUMENT"; data["observed_resource_type"] = "FOLDER"
        receipt = ArtifactPlacementReceipt.from_mapping(data)
        self.assertEqual(receipt.status, PERSISTED_BUT_MISPLACED)
        self.assertIn("resource_type_mismatch", receipt.failures())

    def test_expected_type_without_observation_fails_closed(self):
        data = good_receipt(); data["expected_resource_type"] = "DOCUMENT"
        receipt = ArtifactPlacementReceipt.from_mapping(data)
        self.assertEqual(receipt.status, PERSISTED_BUT_MISPLACED)
        self.assertIn("resource_type_unobserved", receipt.failures())

    def test_parent_mismatch(self):
        data = good_receipt(); data["actual_parent"] = "drive:wrong"
        receipt = ArtifactPlacementReceipt.from_mapping(data)
        self.assertEqual(receipt.status, PERSISTED_BUT_MISPLACED)
        self.assertIn("parent_mismatch", receipt.failures())

    def test_missing_start_here_pointer(self):
        data = good_receipt(); data["start_here_mentions_artifact"] = False
        self.assertEqual(ArtifactPlacementReceipt.from_mapping(data).status, PERSISTED_BUT_MISPLACED)

    def test_legacy_conflict(self):
        data = good_receipt(); data["legacy_conflicts"] = ["misleading legacy master"]
        self.assertEqual(ArtifactPlacementReceipt.from_mapping(data).status, PERSISTED_BUT_MISPLACED)

    def test_missing_cross_store_pointer(self):
        data = good_receipt(); data["cross_store_pointer_present"] = False
        self.assertEqual(ArtifactPlacementReceipt.from_mapping(data).status, PERSISTED_BUT_MISPLACED)

    def test_not_persisted_distinct(self):
        data = good_receipt(); data["artifact_exists"] = False
        self.assertEqual(ArtifactPlacementReceipt.from_mapping(data).status, NOT_PERSISTED)

    def test_completion_without_receipt_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home); manager.create_project("p"); manager.add_task("p", "Persist master", "t1")
            task = complete_task_with_artifact_gate(manager, "p", "t1", None)
            self.assertEqual(task["status"], "BLOCKED")
            self.assertEqual(task["completion_gate"], "ARTIFACT_PLACEMENT")
            reopened = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(reopened["status"], "BLOCKED")
            self.assertNotIn("artifact_placement_receipt", reopened)

    def test_bad_receipt_blocks_and_persists_receipt_across_reopen(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home); manager.create_project("p"); manager.add_task("p", "Persist master", "t1")
            data = good_receipt(); data["actual_parent"] = "drive:wrong"
            task = complete_task_with_artifact_gate(manager, "p", "t1", data)
            self.assertEqual(task["status"], "BLOCKED")
            self.assertEqual(task["artifact_placement_receipt"]["status"], PERSISTED_BUT_MISPLACED)
            reopened = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(reopened["status"], "BLOCKED")
            self.assertEqual(reopened["completion_gate"], "ARTIFACT_PLACEMENT")
            self.assertEqual(reopened["artifact_placement_receipt"]["status"], PERSISTED_BUT_MISPLACED)
            self.assertIn("parent_mismatch", reopened["artifact_placement_receipt"]["failures"])

    def test_resource_type_mismatch_blocks_completion_and_survives_reopen(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home); manager.create_project("p"); manager.add_task("p", "Persist document", "t1")
            data = good_receipt(); data["expected_resource_type"] = "DOCUMENT"; data["observed_resource_type"] = "FOLDER"
            task = complete_task_with_artifact_gate(manager, "p", "t1", data)
            self.assertEqual(task["status"], "BLOCKED")
            self.assertIn("resource_type_mismatch", task["artifact_placement_receipt"]["failures"])
            reopened = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(reopened["status"], "BLOCKED")
            self.assertEqual(reopened["artifact_placement_receipt"]["expected_resource_type"], "DOCUMENT")
            self.assertEqual(reopened["artifact_placement_receipt"]["observed_resource_type"], "FOLDER")
            self.assertIn("resource_type_mismatch", reopened["artifact_placement_receipt"]["failures"])

    def test_good_receipt_completes_and_persists_receipt_across_reopen(self):
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home); manager.create_project("p"); manager.add_task("p", "Persist master", "t1")
            task = complete_task_with_artifact_gate(manager, "p", "t1", good_receipt())
            self.assertEqual(task["status"], "DONE")
            self.assertEqual(task["artifact_placement_receipt"]["status"], PLACEMENT_VERIFIED)
            reopened = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(reopened["status"], "DONE")
            self.assertEqual(reopened["completion_gate"], "ARTIFACT_PLACEMENT")
            self.assertEqual(reopened["artifact_placement_receipt"]["status"], PLACEMENT_VERIFIED)


if __name__ == "__main__":
    unittest.main()
