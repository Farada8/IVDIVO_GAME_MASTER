from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from agents import AgentDefinition, AgentRunRequest, BoundedAgentExecutor, ToolRegistry
from memory.store import MemoryStore
from projects.manager import ProjectStateManager
from providers import MockProvider, ProviderRequest, ProviderResponse, ProviderRegistry


class SequenceMockProvider(MockProvider):
    def __init__(self, responses: list[str], clock=None) -> None:
        super().__init__()
        self.responses = list(responses)
        self.clock = clock
        self.calls = 0

    def generate(self, request: ProviderRequest) -> ProviderResponse:
        self.calls += 1
        if self.clock is not None:
            self.clock.advance(1.0)
        if not self.responses:
            raise RuntimeError("no scripted response")
        text = self.responses.pop(0)
        return ProviderResponse(
            provider=self.name,
            model=request.model or "mock-v1",
            text=text,
            request_id=f"mock-{self.calls}",
            metadata={"network_used": False, "deterministic": True},
        )


class FakeClock:
    def __init__(self) -> None:
        self.value = 0.0

    def __call__(self) -> float:
        return self.value

    def advance(self, delta: float) -> None:
        self.value += delta


def registry_with(provider: MockProvider) -> ProviderRegistry:
    registry = ProviderRegistry()
    registry.register(provider)
    return registry


class StrictAgentContractTest(unittest.TestCase):
    def test_definition_has_exact_registered_fields(self) -> None:
        definition = AgentDefinition(
            role="researcher",
            goal="bounded goal",
            input={"question": "q"},
            tools=("memory_search",),
            memory="brief",
            max_steps=3,
            output_schema={"summary": "string"},
        )
        self.assertEqual(
            set(definition.to_contract_dict()),
            {"ROLE", "GOAL", "INPUT", "TOOLS", "MEMORY", "MAX_STEPS", "OUTPUT_SCHEMA"},
        )

    def test_strict_demo_calls_allowlisted_tool_observes_and_persists(self) -> None:
        provider = SequenceMockProvider([
            json.dumps({"action": "TOOL", "tool": "memory_search", "arguments": {"query": "brief"}}),
            json.dumps({"action": "FINISH", "output": {"summary": "bounded result", "status": "ok"}}),
        ])
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            projects = ProjectStateManager(home)
            projects.create_project("strict")
            memory = MemoryStore(home / "runtime" / "state.db")
            memory.store(
                "brief: use source-backed output",
                kind="DOCUMENT",
                source="fixture",
                project_id="strict",
                record_id="brief-1",
            )
            executor = BoundedAgentExecutor(home, providers=registry_with(provider), tools=ToolRegistry.core())
            definition = AgentDefinition(
                role="bounded researcher",
                goal="use stored brief and finish",
                input={"question": "what matters"},
                tools=("memory_search",),
                memory="brief",
                max_steps=4,
                output_schema={"summary": "string", "status": "string"},
            )
            result = executor.execute(definition, project_id="strict", provider_name="mock")
            self.assertEqual(result.status, "DONE")
            self.assertEqual(len(result.steps), 2)
            events = [
                json.loads(line)["event"]
                for line in Path(result.log_path or "").read_text(encoding="utf-8").splitlines()
            ]
            for event in ("LOAD_TASK", "LOAD_CONTEXT", "PROPOSE_ACTION", "CALL_TOOL", "OBSERVE", "UPDATE_STATE", "RUN_DONE"):
                self.assertIn(event, events)

            reopened_projects = ProjectStateManager(home).load_project("strict")
            self.assertEqual(reopened_projects["state"]["status"], "DONE")
            task = next(item for item in reopened_projects["tasks"] if item["id"] == result.task_id)
            self.assertEqual(task["status"], "DONE")
            output = MemoryStore(home / "runtime" / "state.db").get(result.output_memory_id or "")
            self.assertEqual(output["kind"], "OUTPUT")
            self.assertEqual(json.loads(output["content"])["summary"], "bounded result")

    def test_non_allowlisted_tool_fails_before_tool_call(self) -> None:
        provider = SequenceMockProvider([
            json.dumps({"action": "TOOL", "tool": "echo", "arguments": {"x": 1}})
        ])
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            projects = ProjectStateManager(home)
            projects.create_project("deny")
            executor = BoundedAgentExecutor(home, providers=registry_with(provider), tools=ToolRegistry.core())
            result = executor.execute(
                AgentDefinition(
                    role="tester", goal="deny", input={}, tools=("memory_search",), memory=None,
                    max_steps=2, output_schema={"ok": "boolean"},
                ),
                project_id="deny",
                provider_name="mock",
            )
            self.assertEqual(result.status, "FAILED")
            self.assertIn("tool_not_allowlisted:echo", result.error or "")
            snapshot = projects.load_project("deny")
            task = next(item for item in snapshot["tasks"] if item["id"] == result.task_id)
            self.assertEqual(task["status"], "FAILED")
            self.assertEqual(snapshot["state"]["status"], "FAILED")

    def test_strict_max_steps_prevents_infinite_loop(self) -> None:
        provider = SequenceMockProvider([
            json.dumps({"action": "TOOL", "tool": "echo", "arguments": {"x": 1}}),
            json.dumps({"action": "TOOL", "tool": "echo", "arguments": {"x": 2}}),
        ])
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("limit")
            executor = BoundedAgentExecutor(home, providers=registry_with(provider), tools=ToolRegistry.core())
            result = executor.execute(
                AgentDefinition(
                    role="tester", goal="bounded loop", input={}, tools=("echo",), memory=None,
                    max_steps=2, output_schema={"ok": "boolean"},
                ),
                project_id="limit",
                provider_name="mock",
            )
            self.assertEqual(result.status, "FAILED")
            self.assertEqual(result.error, "max_steps_exceeded:2")
            self.assertEqual(provider.calls, 2)

    def test_strict_timeout_is_hard_bound(self) -> None:
        clock = FakeClock()
        provider = SequenceMockProvider([
            json.dumps({"action": "FINISH", "output": {"ok": True}})
        ], clock=clock)
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("timeout")
            executor = BoundedAgentExecutor(home, providers=registry_with(provider), clock=clock)
            result = executor.execute(
                AgentDefinition(
                    role="tester", goal="timeout", input={}, tools=(), memory=None,
                    max_steps=2, output_schema={"ok": "boolean"},
                ),
                project_id="timeout",
                provider_name="mock",
                timeout_seconds=0.5,
            )
            self.assertEqual(result.status, "FAILED")
            self.assertIn("TimeoutError", result.error or "")

    def test_output_schema_fails_closed(self) -> None:
        provider = SequenceMockProvider([
            json.dumps({"action": "FINISH", "output": {"wrong": "field"}})
        ])
        with tempfile.TemporaryDirectory() as td:
            home = Path(td)
            ProjectStateManager(home).create_project("schema")
            executor = BoundedAgentExecutor(home, providers=registry_with(provider))
            result = executor.execute(
                AgentDefinition(
                    role="tester", goal="schema", input={}, tools=(), memory=None,
                    max_steps=1, output_schema={"summary": "string"},
                ),
                project_id="schema",
                provider_name="mock",
            )
            self.assertEqual(result.status, "FAILED")
            self.assertIn("missing output field", result.error or "")
            self.assertIsNone(result.output_memory_id)

    def test_compatibility_request_has_timeout_guard(self) -> None:
        with self.assertRaises(ValueError):
            AgentRunRequest(project_id="demo", prompt="x", timeout_seconds=0)


if __name__ == "__main__":
    unittest.main()
