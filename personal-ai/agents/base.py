from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentRunRequest:
    project_id: str
    prompt: str
    provider: str = "mock"
    model: str | None = None
    max_steps: int = 3
    allow_network: bool = False
    task_id: str | None = None

    def __post_init__(self) -> None:
        if not self.project_id.strip():
            raise ValueError("project_id cannot be empty")
        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty")
        if not self.provider.strip():
            raise ValueError("provider cannot be empty")
        if self.max_steps < 1 or self.max_steps > 20:
            raise ValueError("max_steps must be between 1 and 20")


@dataclass(frozen=True)
class AgentStepRecord:
    step: int
    prompt: str
    response_text: str
    provider: str
    model: str
    done: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class AgentRunResult:
    run_id: str
    project_id: str
    task_id: str
    status: str
    provider: str
    model: str | None
    steps: tuple[AgentStepRecord, ...] = field(default_factory=tuple)
    output_memory_id: str | None = None
    log_path: str | None = None
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["steps"] = [step.to_dict() for step in self.steps]
        return value
