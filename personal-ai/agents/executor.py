from __future__ import annotations

import json
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Mapping

from agents.base import AgentAction, AgentDefinition, AgentRunRequest, AgentRunResult, AgentStepRecord
from agents.tools import ToolContext, ToolRegistry
from memory.store import MemoryStore
from projects.artifact_completion import complete_task_with_artifact_gate
from projects.manager import ProjectStateManager
from providers import ProviderRequest, ProviderUnavailableError, ProviderRegistry, default_registry

CONTINUE_PREFIX = "CONTINUE:"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _type_matches(value: Any, expected: str) -> bool:
    normalized = expected.strip().lower()
    if normalized == "any":
        return True
    if normalized == "string":
        return isinstance(value, str)
    if normalized == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if normalized == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if normalized == "boolean":
        return isinstance(value, bool)
    if normalized == "object":
        return isinstance(value, dict)
    if normalized == "array":
        return isinstance(value, list)
    if normalized == "null":
        return value is None
    if normalized.endswith("|null"):
        return value is None or _type_matches(value, normalized[:-5])
    raise ValueError(f"unsupported OUTPUT_SCHEMA type: {expected}")


def validate_output(output: Any, schema: Mapping[str, str]) -> None:
    if not schema:
        json.dumps(output)
        return
    if not isinstance(output, dict):
        raise ValueError("OUTPUT_SCHEMA requires an object output")
    for key, expected in schema.items():
        if key not in output:
            raise ValueError(f"missing output field: {key}")
        if not _type_matches(output[key], expected):
            raise ValueError(f"output field {key} does not match {expected}")
    json.dumps(output)


class BoundedAgentExecutor:
    """Bounded project agent runner with persistence and a strict PL-05 tool/observation path."""

    def __init__(
        self,
        home: Path,
        *,
        providers: ProviderRegistry | None = None,
        tools: ToolRegistry | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.providers = providers or default_registry()
        self.tools = tools or ToolRegistry.core()
        self.clock = clock

    def _write_log(self, path: Path, event: str, **fields: Any) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {"timestamp": _utc_now(), "event": event, **fields}
        with path.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(record, sort_keys=True) + "\n")

    @staticmethod
    def _next_prompt(response_text: str) -> tuple[bool, str | None]:
        stripped = response_text.strip()
        if stripped.upper().startswith(CONTINUE_PREFIX):
            next_prompt = stripped[len(CONTINUE_PREFIX) :].strip()
            if not next_prompt:
                raise RuntimeError("provider requested CONTINUE without a next prompt")
            return False, next_prompt
        return True, None

    def _check_timeout(self, deadline: float) -> None:
        if self.clock() >= deadline:
            raise TimeoutError("agent timeout exceeded")

    def _complete_task(
        self,
        project_id: str,
        task_id: str,
        *,
        requires_artifact_placement_receipt: bool,
        artifact_placement_receipt: Mapping[str, Any] | None,
    ) -> dict[str, Any]:
        if requires_artifact_placement_receipt:
            return complete_task_with_artifact_gate(
                self.projects,
                project_id,
                task_id,
                artifact_placement_receipt,
            )
        return self.projects.complete_task(project_id, task_id)

    def run(self, request: AgentRunRequest) -> AgentRunResult:
        """Compatibility provider-only bounded path retained from the PL-05 baseline."""
        self.projects.load_project(request.project_id)
        provider = self.providers.get(request.provider)
        descriptor = provider.describe()
        if descriptor.network_required and not request.allow_network:
            raise ProviderUnavailableError(
                f"{descriptor.name} requires explicit network authorization for agent execution"
            )

        run_id = f"run-{uuid.uuid4().hex}"
        task_id = request.task_id or f"agent-{uuid.uuid4().hex[:12]}"
        log_path = self.projects.paths(request.project_id).root / "logs" / f"{run_id}.jsonl"
        task = self.projects.add_task(
            request.project_id,
            request.prompt,
            task_id,
            requires_artifact_placement_receipt=request.requires_artifact_placement_receipt,
        )
        self.projects.start_task(request.project_id, task["id"])
        deadline = self.clock() + request.timeout_seconds
        self._write_log(
            log_path,
            "RUN_START",
            run_id=run_id,
            project_id=request.project_id,
            task_id=task_id,
            provider=descriptor.name,
            max_steps=request.max_steps,
            timeout_seconds=request.timeout_seconds,
            mode="compatibility",
            requires_artifact_placement_receipt=request.requires_artifact_placement_receipt,
        )

        history: list[AgentStepRecord] = []
        current_prompt = request.prompt
        resolved_model: str | None = None
        try:
            for step_number in range(1, request.max_steps + 1):
                self._check_timeout(deadline)
                response = provider.generate(
                    ProviderRequest(prompt=current_prompt, model=request.model)
                )
                self._check_timeout(deadline)
                resolved_model = response.model
                done, next_prompt = self._next_prompt(response.text)
                step = AgentStepRecord(
                    step=step_number,
                    prompt=current_prompt,
                    response_text=response.text,
                    provider=response.provider,
                    model=response.model,
                    done=done,
                )
                history.append(step)
                self._write_log(log_path, "STEP", **step.to_dict())
                if done:
                    output_id = f"agent-output-{run_id}"
                    self.memory.store(
                        response.text,
                        kind="OUTPUT",
                        source=f"agent:{descriptor.name}",
                        record_id=output_id,
                        project_id=request.project_id,
                        confidence=None,
                        metadata={
                            "run_id": run_id,
                            "task_id": task_id,
                            "provider": response.provider,
                            "model": response.model,
                            "steps": step_number,
                            "mode": "compatibility",
                        },
                    )
                    completion = self._complete_task(
                        request.project_id,
                        task_id,
                        requires_artifact_placement_receipt=request.requires_artifact_placement_receipt,
                        artifact_placement_receipt=request.artifact_placement_receipt,
                    )
                    if completion["status"] != "DONE":
                        reason = completion.get("block_reason") or "artifact placement gate blocked DONE"
                        self._write_log(
                            log_path,
                            "RUN_BLOCKED",
                            run_id=run_id,
                            task_id=task_id,
                            output_memory_id=output_id,
                            reason=reason,
                            steps=step_number,
                        )
                        return AgentRunResult(
                            run_id=run_id,
                            project_id=request.project_id,
                            task_id=task_id,
                            status="BLOCKED",
                            provider=descriptor.name,
                            model=resolved_model,
                            steps=tuple(history),
                            output_memory_id=output_id,
                            log_path=str(log_path),
                            error=reason,
                        )
                    self._write_log(
                        log_path,
                        "RUN_DONE",
                        run_id=run_id,
                        task_id=task_id,
                        output_memory_id=output_id,
                        steps=step_number,
                    )
                    return AgentRunResult(
                        run_id=run_id,
                        project_id=request.project_id,
                        task_id=task_id,
                        status="DONE",
                        provider=descriptor.name,
                        model=resolved_model,
                        steps=tuple(history),
                        output_memory_id=output_id,
                        log_path=str(log_path),
                    )
                current_prompt = next_prompt or current_prompt

            reason = f"max_steps_exceeded:{request.max_steps}"
            self.projects.fail_task(request.project_id, task_id, reason)
            self._write_log(
                log_path,
                "RUN_FAILED",
                run_id=run_id,
                task_id=task_id,
                reason=reason,
                steps=len(history),
            )
            return AgentRunResult(
                run_id=run_id,
                project_id=request.project_id,
                task_id=task_id,
                status="FAILED",
                provider=descriptor.name,
                model=resolved_model,
                steps=tuple(history),
                log_path=str(log_path),
                error=reason,
            )
        except Exception as exc:
            reason = f"{type(exc).__name__}: {exc}"
            self.projects.fail_task(request.project_id, task_id, reason[:1000])
            self._write_log(
                log_path,
                "RUN_FAILED",
                run_id=run_id,
                task_id=task_id,
                reason=reason[:1000],
                steps=len(history),
            )
            return AgentRunResult(
                run_id=run_id,
                project_id=request.project_id,
                task_id=task_id,
                status="FAILED",
                provider=descriptor.name,
                model=resolved_model,
                steps=tuple(history),
                log_path=str(log_path),
                error=reason,
            )

    def _memory_context(self, definition: AgentDefinition, project_id: str) -> list[dict[str, Any]]:
        if definition.memory is None:
            return []
        rows = self.memory.search(definition.memory, project_id=project_id, limit=10)
        return [
            {
                "id": row["id"],
                "kind": row["kind"],
                "content": row["content"],
                "source": row.get("source"),
                "content_hash": row.get("content_hash"),
            }
            for row in rows
        ]

    @staticmethod
    def _strict_prompt(
        definition: AgentDefinition,
        *,
        task_id: str,
        memory_context: list[dict[str, Any]],
        observations: list[dict[str, Any]],
        step: int,
    ) -> str:
        context = {
            "agent": definition.to_contract_dict(),
            "task_id": task_id,
            "memory_context": memory_context,
            "observations": observations,
            "step": step,
        }
        return (
            "You are a bounded agent planner. Return exactly one JSON object and no prose. "
            "Use either {\"action\":\"TOOL\",\"tool\":\"allowed_name\",\"arguments\":{...}} "
            "or {\"action\":\"FINISH\",\"output\":{...}}. "
            "Never name a tool outside TOOLS. Unknown evidence must remain null.\nCONTEXT:\n"
            + json.dumps(context, sort_keys=True, ensure_ascii=False)
        )

    def execute(
        self,
        definition: AgentDefinition,
        *,
        project_id: str,
        provider_name: str = "mock",
        model: str | None = None,
        task_id: str | None = None,
        allow_network: bool = False,
        timeout_seconds: float = 30.0,
        requires_artifact_placement_receipt: bool = False,
        artifact_placement_receipt: Mapping[str, Any] | None = None,
    ) -> AgentRunResult:
        """Canonical strict PL-05 path: load -> propose -> call tool -> observe -> update -> stop."""
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if artifact_placement_receipt is not None and not requires_artifact_placement_receipt:
            raise ValueError(
                "artifact_placement_receipt requires requires_artifact_placement_receipt=true"
            )
        self.projects.load_project(project_id)
        provider = self.providers.get(provider_name)
        descriptor = provider.describe()
        if descriptor.network_required and not allow_network:
            raise ProviderUnavailableError(
                f"{descriptor.name} requires explicit network authorization for agent execution"
            )

        run_id = f"run-{uuid.uuid4().hex}"
        task_id = task_id or f"agent-{uuid.uuid4().hex[:12]}"
        log_path = self.projects.paths(project_id).root / "logs" / f"{run_id}.jsonl"
        task = self.projects.add_task(
            project_id,
            definition.goal,
            task_id,
            requires_artifact_placement_receipt=requires_artifact_placement_receipt,
        )
        self.projects.start_task(project_id, task["id"])
        self.projects.update_state(
            project_id,
            "RUNNING",
            agent_run_id=run_id,
            agent_task_id=task_id,
            agent_mode="strict",
            agent_steps=0,
        )
        deadline = self.clock() + timeout_seconds
        memory_context = self._memory_context(definition, project_id)
        self._write_log(
            log_path,
            "RUN_START",
            run_id=run_id,
            project_id=project_id,
            task_id=task_id,
            provider=descriptor.name,
            max_steps=definition.max_steps,
            timeout_seconds=timeout_seconds,
            mode="strict",
            requires_artifact_placement_receipt=requires_artifact_placement_receipt,
        )
        self._write_log(log_path, "LOAD_TASK", task_id=task_id, goal=definition.goal)
        self._write_log(log_path, "LOAD_CONTEXT", memory_count=len(memory_context))
        self.memory.store(
            f"Strict agent run {run_id} started for task {task_id}",
            kind="EVENT",
            source=f"agent:{descriptor.name}",
            project_id=project_id,
            metadata={"run_id": run_id, "task_id": task_id, "status": "RUNNING"},
        )

        history: list[AgentStepRecord] = []
        observations: list[dict[str, Any]] = []
        allowed_tools = set(definition.tools)
        tool_context = ToolContext(project_id=project_id, task_id=task_id, memory=self.memory)
        resolved_model: str | None = None

        def fail(reason: str) -> AgentRunResult:
            self.projects.fail_task(project_id, task_id, reason[:1000])
            self.projects.update_state(
                project_id,
                "FAILED",
                agent_run_id=run_id,
                agent_task_id=task_id,
                agent_mode="strict",
                agent_steps=len(history),
                agent_error=reason[:1000],
            )
            self._write_log(
                log_path,
                "RUN_FAILED",
                run_id=run_id,
                task_id=task_id,
                reason=reason[:1000],
                steps=len(history),
            )
            self.memory.store(
                reason[:1000],
                kind="EVENT",
                source=f"agent:{descriptor.name}",
                project_id=project_id,
                metadata={"run_id": run_id, "task_id": task_id, "status": "FAILED"},
            )
            return AgentRunResult(
                run_id=run_id,
                project_id=project_id,
                task_id=task_id,
                status="FAILED",
                provider=descriptor.name,
                model=resolved_model,
                steps=tuple(history),
                log_path=str(log_path),
                error=reason,
            )

        try:
            for step_number in range(1, definition.max_steps + 1):
                self._check_timeout(deadline)
                prompt = self._strict_prompt(
                    definition,
                    task_id=task_id,
                    memory_context=memory_context,
                    observations=observations,
                    step=step_number,
                )
                self._write_log(log_path, "PROPOSE_ACTION", step=step_number, provider=descriptor.name)
                response = provider.generate(ProviderRequest(prompt=prompt, model=model))
                self._check_timeout(deadline)
                resolved_model = response.model
                action = AgentAction.parse(response.text)
                done = action.action == "FINISH"
                history.append(
                    AgentStepRecord(
                        step=step_number,
                        prompt=prompt,
                        response_text=response.text,
                        provider=response.provider,
                        model=response.model,
                        done=done,
                    )
                )
                self._write_log(
                    log_path,
                    "ACTION",
                    step=step_number,
                    action=action.action,
                    tool=action.tool,
                    arguments=action.arguments,
                )

                if done:
                    validate_output(action.output, definition.output_schema)
                    content = json.dumps(action.output, sort_keys=True, ensure_ascii=False)
                    output_id = f"agent-output-{run_id}"
                    self.memory.store(
                        content,
                        kind="OUTPUT",
                        source=f"agent:{descriptor.name}",
                        record_id=output_id,
                        project_id=project_id,
                        metadata={
                            "run_id": run_id,
                            "task_id": task_id,
                            "provider": response.provider,
                            "model": response.model,
                            "steps": step_number,
                            "mode": "strict",
                            "output_schema": dict(definition.output_schema),
                        },
                    )
                    completion = self._complete_task(
                        project_id,
                        task_id,
                        requires_artifact_placement_receipt=requires_artifact_placement_receipt,
                        artifact_placement_receipt=artifact_placement_receipt,
                    )
                    if completion["status"] != "DONE":
                        reason = completion.get("block_reason") or "artifact placement gate blocked DONE"
                        self.projects.update_state(
                            project_id,
                            "BLOCKED",
                            agent_run_id=run_id,
                            agent_task_id=task_id,
                            agent_mode="strict",
                            agent_steps=step_number,
                            agent_error=reason,
                            agent_output_memory_id=output_id,
                        )
                        self._write_log(
                            log_path,
                            "UPDATE_STATE",
                            step=step_number,
                            project_status="BLOCKED",
                        )
                        self._write_log(
                            log_path,
                            "RUN_BLOCKED",
                            run_id=run_id,
                            task_id=task_id,
                            output_memory_id=output_id,
                            reason=reason,
                            steps=step_number,
                        )
                        self.memory.store(
                            reason,
                            kind="EVENT",
                            source=f"agent:{descriptor.name}",
                            project_id=project_id,
                            metadata={"run_id": run_id, "task_id": task_id, "status": "BLOCKED"},
                        )
                        return AgentRunResult(
                            run_id=run_id,
                            project_id=project_id,
                            task_id=task_id,
                            status="BLOCKED",
                            provider=descriptor.name,
                            model=resolved_model,
                            steps=tuple(history),
                            output_memory_id=output_id,
                            log_path=str(log_path),
                            error=reason,
                        )

                    next_task = self.projects.get_next_task(project_id)
                    project_status = "READY" if next_task is not None else "DONE"
                    self.projects.update_state(
                        project_id,
                        project_status,
                        agent_run_id=run_id,
                        agent_task_id=task_id,
                        agent_mode="strict",
                        agent_steps=step_number,
                        agent_error=None,
                        agent_output_memory_id=output_id,
                    )
                    self._write_log(
                        log_path,
                        "UPDATE_STATE",
                        step=step_number,
                        project_status=project_status,
                    )
                    self._write_log(
                        log_path,
                        "RUN_DONE",
                        run_id=run_id,
                        task_id=task_id,
                        output_memory_id=output_id,
                        steps=step_number,
                    )
                    return AgentRunResult(
                        run_id=run_id,
                        project_id=project_id,
                        task_id=task_id,
                        status="DONE",
                        provider=descriptor.name,
                        model=resolved_model,
                        steps=tuple(history),
                        output_memory_id=output_id,
                        log_path=str(log_path),
                    )

                if action.tool not in allowed_tools:
                    return fail(f"tool_not_allowlisted:{action.tool}")
                self._write_log(log_path, "CALL_TOOL", step=step_number, tool=action.tool)
                observation = self.tools.call(action.tool or "", action.arguments, tool_context)
                observations.append({"step": step_number, "tool": action.tool, "result": observation})
                self._write_log(
                    log_path,
                    "OBSERVE",
                    step=step_number,
                    tool=action.tool,
                    result=observation,
                )
                self.projects.update_state(
                    project_id,
                    "RUNNING",
                    agent_run_id=run_id,
                    agent_task_id=task_id,
                    agent_mode="strict",
                    agent_steps=step_number,
                    agent_last_tool=action.tool,
                )

            return fail(f"max_steps_exceeded:{definition.max_steps}")
        except Exception as exc:
            return fail(f"{type(exc).__name__}: {exc}")
