from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents import AgentDefinition, AgentRunRequest, BoundedAgentExecutor
from projects.manager import ProjectStateManager
from providers import MockProvider, ProviderRequest, ProviderResponse, ProviderRegistry


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
        "cross_store_required": False,
        "cross_store_pointer_present": False,
        "expected_resource_type": "DOCUMENT",
        "observed_resource_type": "DOCUMENT",
    }


def bad_type_receipt() -> dict:
    value = good_receipt()
    value["observed_resource_type"] = "FOLDER"
    return value


class StrictFinishProvider(MockProvider):
    def generate(self, request: ProviderRequest) -> ProviderResponse:
        return ProviderResponse(
            provider=self.name,
            model=request.model or "mock-v1",
            text=json.dumps({"action": "FINISH", "output": {"ok": True}}),
            request_id="strict-finish-1",
            metadata={"network_used": False, "deterministic": True},
        )


def strict_registry() -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(StrictFinishProvider())
    return registry


class ArtifactGateProductionAdoptionTest(unittest.TestCase):
    def test_manager_direct_done_rejects_artifact_task(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home)
            manager.create_project("p")
            task = manager.add_task(
                "p",
                "Create Drive document",
                "artifact-task",
                requires_artifact_placement_receipt=True,
            )
            self.assertTrue(task["requires_artifact_placement_receipt"])
            with self.assertRaisesRegex(RuntimeError, "complete_task_with_artifact_gate"):
                manager.complete_task("p", "artifact-task")
            reopened = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(reopened["status"], "READY")

    def test_manager_non_artifact_task_keeps_backward_compatible_done(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            manager = ProjectStateManager(home)
            manager.create_project("p")
            task = manager.add_task("p", "Internal reasoning", "plain-task")
            self.assertFalse(task["requires_artifact_placement_receipt"])
            self.assertEqual(manager.complete_task("p", "plain-task")["status"], "DONE")

    def test_compatibility_agent_artifact_task_without_receipt_blocks(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("p")
            result = BoundedAgentExecutor(home).run(
                AgentRunRequest(
                    project_id="p",
                    prompt="create external artifact",
                    provider="mock",
                    task_id="artifact-task",
                    requires_artifact_placement_receipt=True,
                )
            )
            self.assertEqual(result.status, "BLOCKED")
            task = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(task["status"], "BLOCKED")
            self.assertTrue(task["requires_artifact_placement_receipt"])
            self.assertEqual(task["completion_gate"], "ARTIFACT_PLACEMENT")
            self.assertNotIn("artifact_placement_interceptions", task)

    def test_compatibility_agent_bad_receipt_blocks_and_captures_interception(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("p")
            result = BoundedAgentExecutor(home).run(
                AgentRunRequest(
                    project_id="p",
                    prompt="create external artifact",
                    provider="mock",
                    requires_artifact_placement_receipt=True,
                    artifact_placement_receipt=bad_type_receipt(),
                )
            )
            self.assertEqual(result.status, "BLOCKED")
            task = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(task["artifact_placement_receipt"]["status"], "PERSISTED_BUT_MISPLACED")
            self.assertIn("resource_type_mismatch", task["artifact_placement_interceptions"][0]["failures"])
            self.assertTrue(task["artifact_placement_interceptions"][0]["caught_before_done"])
            self.assertFalse(task["artifact_placement_interceptions"][0]["promotion_proof"])

    def test_compatibility_agent_verified_receipt_completes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("p")
            result = BoundedAgentExecutor(home).run(
                AgentRunRequest(
                    project_id="p",
                    prompt="create external artifact",
                    provider="mock",
                    requires_artifact_placement_receipt=True,
                    artifact_placement_receipt=good_receipt(),
                )
            )
            self.assertEqual(result.status, "DONE")
            task = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(task["status"], "DONE")
            self.assertEqual(task["artifact_placement_receipt"]["status"], "PLACEMENT_VERIFIED")

    def test_strict_agent_artifact_finish_without_receipt_blocks_project(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("p")
            executor = BoundedAgentExecutor(home, providers=strict_registry())
            definition = AgentDefinition(
                role="writer",
                goal="persist deliverable",
                input={},
                tools=(),
                memory=None,
                max_steps=1,
                output_schema={"ok": "boolean"},
            )
            result = executor.execute(
                definition,
                project_id="p",
                provider_name="mock",
                requires_artifact_placement_receipt=True,
            )
            self.assertEqual(result.status, "BLOCKED")
            snapshot = ProjectStateManager(home).load_project("p")
            self.assertEqual(snapshot["state"]["status"], "BLOCKED")
            task = snapshot["tasks"][0]
            self.assertEqual(task["status"], "BLOCKED")
            self.assertEqual(task["completion_gate"], "ARTIFACT_PLACEMENT")

    def test_strict_agent_bad_receipt_blocks_with_interception(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("p")
            executor = BoundedAgentExecutor(home, providers=strict_registry())
            definition = AgentDefinition(
                role="writer",
                goal="persist deliverable",
                input={},
                tools=(),
                memory=None,
                max_steps=1,
                output_schema={"ok": "boolean"},
            )
            result = executor.execute(
                definition,
                project_id="p",
                provider_name="mock",
                requires_artifact_placement_receipt=True,
                artifact_placement_receipt=bad_type_receipt(),
            )
            self.assertEqual(result.status, "BLOCKED")
            task = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertIn("resource_type_mismatch", task["artifact_placement_interceptions"][0]["failures"])

    def test_strict_agent_verified_receipt_completes(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("p")
            executor = BoundedAgentExecutor(home, providers=strict_registry())
            definition = AgentDefinition(
                role="writer",
                goal="persist deliverable",
                input={},
                tools=(),
                memory=None,
                max_steps=1,
                output_schema={"ok": "boolean"},
            )
            result = executor.execute(
                definition,
                project_id="p",
                provider_name="mock",
                requires_artifact_placement_receipt=True,
                artifact_placement_receipt=good_receipt(),
            )
            self.assertEqual(result.status, "DONE")
            snapshot = ProjectStateManager(home).load_project("p")
            self.assertEqual(snapshot["state"]["status"], "DONE")
            self.assertEqual(snapshot["tasks"][0]["artifact_placement_receipt"]["status"], "PLACEMENT_VERIFIED")

    def test_cli_block_then_complete_with_provider_receipt(self) -> None:
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            env = os.environ.copy()
            env.pop("OPENAI_API_KEY", None)
            env.pop("ANTHROPIC_API_KEY", None)
            run_py = ROOT / "run.py"
            subprocess.run(
                [sys.executable, str(run_py), "--home", str(home), "project", "create", "p"],
                check=True,
                capture_output=True,
                text=True,
                env=env,
            )
            blocked = subprocess.run(
                [
                    sys.executable,
                    str(run_py),
                    "--home",
                    str(home),
                    "agent",
                    "run",
                    "p",
                    "create Drive document",
                    "--provider",
                    "mock",
                    "--task-id",
                    "artifact-task",
                    "--require-artifact-placement-receipt",
                ],
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(blocked.returncode, 2)
            self.assertEqual(json.loads(blocked.stdout)["status"], "BLOCKED")

            receipt_path = home / "receipt.json"
            receipt_path.write_text(json.dumps(good_receipt()), encoding="utf-8")
            completed = subprocess.run(
                [
                    sys.executable,
                    str(run_py),
                    "--home",
                    str(home),
                    "project",
                    "complete-artifact",
                    "p",
                    "artifact-task",
                    str(receipt_path),
                ],
                check=False,
                capture_output=True,
                text=True,
                env=env,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            task = json.loads(completed.stdout)
            self.assertEqual(task["status"], "DONE")
            self.assertEqual(task["artifact_placement_receipt"]["status"], "PLACEMENT_VERIFIED")
            reopened = ProjectStateManager(home).load_project("p")["tasks"][0]
            self.assertEqual(reopened["status"], "DONE")
            self.assertTrue(reopened["requires_artifact_placement_receipt"])


if __name__ == "__main__":
    unittest.main()
