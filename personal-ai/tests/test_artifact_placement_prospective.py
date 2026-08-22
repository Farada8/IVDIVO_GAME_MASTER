from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.artifact_placement import ArtifactPlacementReceipt


FIXTURE = REPO_ROOT / "SELF_IMPROVEMENT_ENGINE" / "INCIDENTS" / "2026-08-22_ARTIFACT_PLACEMENT_PATH_DRIFT" / "PROSPECTIVE_CANARIES_v1.json"


class ProspectivePlacementCanaryTest(unittest.TestCase):
    def test_real_cross_project_receipts_match_expected_status(self) -> None:
        payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
        canaries = payload["canaries"]
        self.assertGreaterEqual(len(canaries), 2)
        project_roots = set()
        for case in canaries:
            receipt = ArtifactPlacementReceipt.from_mapping(case["receipt"])
            self.assertEqual(receipt.status, case["expected_status"], case["id"])
            project_roots.add(receipt.project_root)
        self.assertGreaterEqual(len(project_roots), 2)


if __name__ == "__main__":
    unittest.main()
