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
            manager = ProjectStateManager(Path(td)); manager.create_project("p"); manager.add_task("p", "Persist master", "t1")
            task = complete_task_with_artifact_gate(manager, "p", "t1", None)
            self.assertEqual(task["status"], "BLOCKED")

    def test_bad_receipt_blocks_and_persists_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            manager = ProjectStateManager(Path(td)); manager.create_project("p"); manager.add_task("p", "Persist master", "t1")
            data = good_receipt(); data["actual_parent"] = "drive:wrong"
            task = complete_task_with_artifact_gate(manager, "p", "t1", data)
            self.assertEqual(task["status"], "BLOCKED")
            self.assertEqual(task["artifact_placement_receipt"]["status"], PERSISTED_BUT_MISPLACED)

    def test_good_receipt_completes_and_persists_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            manager = ProjectStateManager(Path(td)); manager.create_project("p"); manager.add_task("p", "Persist master", "t1")
            task = complete_task_with_artifact_gate(manager, "p", "t1", good_receipt())
            self.assertEqual(task["status"], "DONE")
            self.assertEqual(task["artifact_placement_receipt"]["status"], PLACEMENT_VERIFIED)


if __name__ == "__main__":
    unittest.main()
