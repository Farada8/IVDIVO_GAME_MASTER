from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from books import BookProductionCore
from projects.manager import ProjectStateManager


class ProjectCompletionScopeTest(unittest.TestCase):
    def test_book_project_state_never_asserts_external_artifact_completion(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            projects = ProjectStateManager(home)
            projects.create_project("book")
            core = BookProductionCore(home)
            core.initialize("book", "Scoped Book")

            initial = projects.load_project("book")["state"]
            self.assertEqual(initial["completion_scope"], "INTERNAL_BOOK_PRODUCTION")
            self.assertEqual(initial["external_artifact_completion"], "NOT_ASSERTED")

            result = core.load("book")
            while result["state"]["stage"] != "CONTINUITY":
                result = core.advance("book")
            core.set_continuity_gate("book", passed=True, evidence="scope fixture")
            core.advance("book")

            final_state = projects.load_project("book")["state"]
            self.assertEqual(final_state["status"], "DONE")
            self.assertEqual(final_state["book_stage"], "FINAL")
            self.assertEqual(final_state["completion_scope"], "INTERNAL_BOOK_PRODUCTION")
            self.assertEqual(final_state["external_artifact_completion"], "NOT_ASSERTED")
            self.assertNotIn("artifact_placement_receipt", final_state)

    def test_internal_book_done_does_not_complete_artifact_task(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            projects = ProjectStateManager(home)
            projects.create_project("book")
            artifact_task = projects.add_task(
                "book",
                "Export final manuscript",
                "export",
                requires_artifact_placement_receipt=True,
            )
            self.assertEqual(artifact_task["status"], "READY")

            core = BookProductionCore(home)
            core.initialize("book", "Scoped Book")
            result = core.load("book")
            while result["state"]["stage"] != "CONTINUITY":
                result = core.advance("book")
            core.set_continuity_gate("book", passed=True, evidence="scope fixture")
            core.advance("book")

            snapshot = projects.load_project("book")
            self.assertEqual(snapshot["state"]["status"], "DONE")
            persisted_task = next(task for task in snapshot["tasks"] if task["id"] == "export")
            self.assertEqual(persisted_task["status"], "READY")
            self.assertTrue(persisted_task["requires_artifact_placement_receipt"])


if __name__ == "__main__":
    unittest.main()
