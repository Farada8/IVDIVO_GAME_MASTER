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

from agents import AgentRunRequest, BoundedAgentExecutor
from memory.store import MemoryStore
from projects.manager import ProjectStateManager
from providers.base import AIProvider, ProviderDescriptor, ProviderRequest, ProviderResponse
from providers.registry import ProviderRegistry


class SequenceProvider(AIProvider):
    def __init__(
        self,
        responses: list[str],
        *,
        name: str = "sequence",
        network_required: bool = False,
        fail_at: int | None = None,
    ) -> None:
        self.name = name
        self.responses = list(responses)
        self.network_required = network_required
        self.fail_at = fail_at
        self.calls: list[str] = []

    def describe(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            name=self.name,
            configured=True,
            network_required=self.network_required,
            endpoint="https://example.invalid" if self.network_required else None,
            default_model="sequence-v1",
            contract="test.sequence/0.1",
        )

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        self.calls.append(request.prompt)
        call_number = len(self.calls)
        if self.fail_at == call_number:
            raise RuntimeError("synthetic provider failure")
        if not self.responses:
            raise RuntimeError("no synthetic response left")
        return ProviderResponse(
            provider=self.name,
            model=request.model or "sequence-v1",
            text=self.responses.pop(0),
            metadata={"network_used": self.network_required},
        )


def registry_with(provider: AIProvider) -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(provider)
    return registry


class AgentExecutorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.home = Path(self.tmp.name)
        self.projects = ProjectStateManager(self.home)
        self.projects.create_project("demo", "Demo")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_one_step_success_persists_task_output_and_log(self) -> None:
        provider = SequenceProvider(["final answer"])
        executor = BoundedAgentExecutor(self.home, providers=registry_with(provider))
        result = executor.run(
            AgentRunRequest(project_id="demo", prompt="do work", provider="sequence", max_steps=3)
        )

        self.assertEqual(result.status, "DONE")
        self.assertEqual(len(result.steps), 1)
        self.assertEqual(provider.calls, ["do work"])
        self.assertIsNotNone(result.output_memory_id)

        project = self.projects.load_project("demo")
        task = next(item for item in project["tasks"] if item["id"] == result.task_id)
        self.assertEqual(task["status"], "DONE")

        memory = MemoryStore(self.home / "runtime" / "state.db")
        output = memory.get(result.output_memory_id or "")
        self.assertEqual(output["kind"], "OUTPUT")
        self.assertEqual(output["content"], "final answer")
        self.assertEqual(output["project_id"], "demo")
        self.assertEqual(output["metadata"]["task_id"], result.task_id)

        log_path = Path(result.log_path or "")
        events = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([item["event"] for item in events], ["RUN_START", "STEP", "RUN_DONE"])

    def test_continue_protocol_is_bounded_and_persists_final_only(self) -> None:
        provider = SequenceProvider(["CONTINUE: inspect evidence", "final synthesis"])
        executor = BoundedAgentExecutor(self.home, providers=registry_with(provider))
        result = executor.run(
            AgentRunRequest(project_id="demo", prompt="start", provider="sequence", max_steps=3)
        )

        self.assertEqual(result.status, "DONE")
        self.assertEqual(provider.calls, ["start", "inspect evidence"])
        self.assertEqual(len(result.steps), 2)
        self.assertFalse(result.steps[0].done)
        self.assertTrue(result.steps[1].done)
        memory = MemoryStore(self.home / "runtime" / "state.db")
        outputs = memory.search("final synthesis", kind="OUTPUT", project_id="demo")
        self.assertEqual(len(outputs), 1)
        self.assertEqual(outputs[0]["id"], result.output_memory_id)

    def test_max_steps_marks_task_failed_and_does_not_create_output(self) -> None:
        provider = SequenceProvider(["CONTINUE: two", "CONTINUE: three", "CONTINUE: four"])
        executor = BoundedAgentExecutor(self.home, providers=registry_with(provider))
        result = executor.run(
            AgentRunRequest(project_id="demo", prompt="one", provider="sequence", max_steps=2)
        )

        self.assertEqual(result.status, "FAILED")
        self.assertEqual(result.error, "max_steps_exceeded:2")
        self.assertEqual(provider.calls, ["one", "two"])
        project = self.projects.load_project("demo")
        task = next(item for item in project["tasks"] if item["id"] == result.task_id)
        self.assertEqual(task["status"], "FAILED")
        self.assertEqual(task["block_reason"], "max_steps_exceeded:2")
        memory = MemoryStore(self.home / "runtime" / "state.db")
        self.assertEqual(memory.search("agent-output-", kind="OUTPUT", project_id="demo"), [])

    def test_provider_failure_is_persisted_as_failed_task_and_log(self) -> None:
        provider = SequenceProvider(["unused"], fail_at=1)
        executor = BoundedAgentExecutor(self.home, providers=registry_with(provider))
        result = executor.run(
            AgentRunRequest(project_id="demo", prompt="explode", provider="sequence")
        )

        self.assertEqual(result.status, "FAILED")
        self.assertIn("synthetic provider failure", result.error or "")
        project = self.projects.load_project("demo")
        task = next(item for item in project["tasks"] if item["id"] == result.task_id)
        self.assertEqual(task["status"], "FAILED")
        log_events = [
            json.loads(line)["event"]
            for line in Path(result.log_path or "").read_text(encoding="utf-8").splitlines()
        ]
        self.assertEqual(log_events, ["RUN_START", "RUN_FAILED"])

    def test_network_provider_requires_explicit_authorization_before_task_creation(self) -> None:
        provider = SequenceProvider(["never"], name="networked", network_required=True)
        executor = BoundedAgentExecutor(self.home, providers=registry_with(provider))
        with self.assertRaisesRegex(RuntimeError, "explicit network authorization"):
            executor.run(
                AgentRunRequest(project_id="demo", prompt="do not send", provider="networked")
            )
        self.assertEqual(self.projects.load_project("demo")["tasks"], [])
        self.assertEqual(provider.calls, [])

    def test_request_rejects_unbounded_step_count(self) -> None:
        with self.assertRaises(ValueError):
            AgentRunRequest(project_id="demo", prompt="x", max_steps=0)
        with self.assertRaises(ValueError):
            AgentRunRequest(project_id="demo", prompt="x", max_steps=21)

    def test_cli_mock_round_trip_persists_state_memory_and_log(self) -> None:
        cli_home = self.home / "cli-home"
        run_py = ROOT / "run.py"
        env = os.environ.copy()
        env.pop("OPENAI_API_KEY", None)
        env.pop("ANTHROPIC_API_KEY", None)

        subprocess.run(
            [sys.executable, str(run_py), "--home", str(cli_home), "project", "create", "cli-demo"],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        completed = subprocess.run(
            [
                sys.executable,
                str(run_py),
                "--home",
                str(cli_home),
                "agent",
                "run",
                "cli-demo",
                "hello agent",
                "--provider",
                "mock",
                "--max-steps",
                "2",
            ],
            check=True,
            capture_output=True,
            text=True,
            env=env,
        )
        result = json.loads(completed.stdout)
        self.assertEqual(result["status"], "DONE")
        self.assertEqual(result["steps"][0]["response_text"], "MOCK_RESPONSE: hello agent")
        self.assertTrue(Path(result["log_path"]).is_file())

        manager = ProjectStateManager(cli_home)
        task = next(item for item in manager.load_project("cli-demo")["tasks"] if item["id"] == result["task_id"])
        self.assertEqual(task["status"], "DONE")
        output = MemoryStore(cli_home / "runtime" / "state.db").get(result["output_memory_id"])
        self.assertEqual(output["content"], "MOCK_RESPONSE: hello agent")


if __name__ == "__main__":
    unittest.main()
