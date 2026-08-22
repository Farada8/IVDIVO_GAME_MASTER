from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from agents.base import AgentRunRequest, AgentRunResult, AgentStepRecord
from memory.store import MemoryStore
from projects.manager import ProjectStateManager
from providers import ProviderRequest, ProviderUnavailableError, ProviderRegistry, default_registry

CONTINUE_PREFIX = "CONTINUE:"


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class BoundedAgentExecutor:
    """Bounded project agent runner with persisted task state, output memory and JSONL logs."""

    def __init__(
        self,
        home: Path,
        *,
        providers: ProviderRegistry | None = None,
    ) -> None:
        self.home = Path(home)
        self.projects = ProjectStateManager(self.home)
        self.memory = MemoryStore(self.home / "runtime" / "state.db")
        self.providers = providers or default_registry()

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

    def run(self, request: AgentRunRequest) -> AgentRunResult:
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
        task = self.projects.add_task(request.project_id, request.prompt, task_id)
        self.projects.start_task(request.project_id, task["id"])
        self._write_log(
            log_path,
            "RUN_START",
            run_id=run_id,
            project_id=request.project_id,
            task_id=task_id,
            provider=descriptor.name,
            max_steps=request.max_steps,
        )

        history: list[AgentStepRecord] = []
        current_prompt = request.prompt
        resolved_model: str | None = None
        try:
            for step_number in range(1, request.max_steps + 1):
                response = provider.generate(
                    ProviderRequest(prompt=current_prompt, model=request.model)
                )
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
                        },
                    )
                    self.projects.complete_task(request.project_id, task_id)
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
