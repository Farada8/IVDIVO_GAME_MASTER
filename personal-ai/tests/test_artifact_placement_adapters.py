from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.artifact_placement import PERSISTED_BUT_MISPLACED, PLACEMENT_VERIFIED
from core.artifact_placement_adapters import PlacementIntent, receipt_from_drive_observation, receipt_from_github_observation


class ArtifactPlacementAdapterTest(unittest.TestCase):
    def test_drive_provider_observation_passes_with_raw_ids(self):
        intent = PlacementIntent("drive:ROOT", "drive:PARENT", "drive:START")
        receipt = receipt_from_drive_observation(
            intent=intent,
            artifact_metadata={"id": "FILE", "parent_ids": ["PARENT"]},
            start_here_readback_ok=True,
            start_here_mentions_artifact=True,
        )
        self.assertEqual(receipt.status, PLACEMENT_VERIFIED)
        self.assertEqual(receipt.artifact_id, "drive:FILE")
        self.assertEqual(receipt.actual_parent, "drive:PARENT")
        self.assertEqual(receipt.provider, "GOOGLE_DRIVE")

    def test_drive_prefixed_ids_do_not_double_prefix(self):
        intent = PlacementIntent("drive:ROOT", "drive:PARENT", "drive:START")
        receipt = receipt_from_drive_observation(
            intent=intent,
            artifact_metadata={"id": "drive:FILE", "parent_ids": ["drive:PARENT"]},
            start_here_readback_ok=True,
            start_here_mentions_artifact=True,
        )
        self.assertEqual(receipt.artifact_id, "drive:FILE")
        self.assertEqual(receipt.actual_parent, "drive:PARENT")
        self.assertEqual(receipt.status, PLACEMENT_VERIFIED)

    def test_drive_wrong_parent_fails_closed(self):
        intent = PlacementIntent("drive:ROOT", "drive:PARENT", "drive:START")
        receipt = receipt_from_drive_observation(
            intent=intent,
            artifact_metadata={"id": "FILE", "parent_ids": ["WRONG"]},
            start_here_readback_ok=True,
            start_here_mentions_artifact=True,
        )
        self.assertEqual(receipt.status, PERSISTED_BUT_MISPLACED)
        self.assertIn("parent_mismatch", receipt.failures())

    def test_drive_multiple_parents_fail_closed(self):
        intent = PlacementIntent("drive:ROOT", "drive:PARENT", "drive:START")
        receipt = receipt_from_drive_observation(
            intent=intent,
            artifact_metadata={"id": "FILE", "parent_ids": ["PARENT", "OTHER"]},
            start_here_readback_ok=True,
            start_here_mentions_artifact=True,
        )
        self.assertEqual(receipt.status, PERSISTED_BUT_MISPLACED)

    def test_github_provider_observation_passes(self):
        intent = PlacementIntent(
            "github:Farada8/IVDIVO_GAME_MASTER:PROJECTS/D09",
            "github:Farada8/IVDIVO_GAME_MASTER:PROJECTS/D09/current",
            "github:Farada8/IVDIVO_GAME_MASTER:PROJECTS/D09/README.md",
        )
        receipt = receipt_from_github_observation(
            intent=intent,
            repository_full_name="Farada8/IVDIVO_GAME_MASTER",
            path="PROJECTS/D09/current/master.md",
            file_observed=True,
            current_index_readback_ok=True,
            current_index_mentions_artifact=True,
        )
        self.assertEqual(receipt.status, PLACEMENT_VERIFIED)
        self.assertEqual(receipt.provider, "GITHUB")

    def test_github_missing_file_is_not_persisted(self):
        intent = PlacementIntent("github:repo:root", "github:repo:root/current", "github:repo:root/README.md")
        receipt = receipt_from_github_observation(
            intent=intent,
            repository_full_name="repo",
            path="root/current/master.md",
            file_observed=False,
            current_index_readback_ok=True,
            current_index_mentions_artifact=True,
        )
        self.assertFalse(receipt.artifact_exists)


if __name__ == "__main__":
    unittest.main()
