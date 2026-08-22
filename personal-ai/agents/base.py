from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class AgentRunRequest:
    project_id: str
    prompt: str
    provider: str = "mock"
    model: str | None = None
    max_steps: int = 3
    allow_network: bool = False
    task_id: str | None = None
    timeout_seconds: float = 30.0
    requires_artifact_placement_receipt: bool = False
    artifact_placement_receipt: Mapping[str, Any] | None = None

    def __post_init__(self) -> None:
        if not self.project_id.strip():
            raise ValueError("project_id cannot be empty")
        if not self.prompt.strip():
            raise ValueError("prompt cannot be empty")
        if not self.provider.strip():
            raise ValueError("provider cannot be empty")
        if self.max_steps < 1 or self.max_steps > 20:
            raise ValueError("max_steps must be between 1 and 20")
        if self.timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        if self.artifact_placement_receipt is not None and not self.requires_artifact_placement_receipt:
            raise ValueError(
                "artifact_placement_receipt requires requires_artifact_placement_receipt=true"
            )


@dataclass(frozen=True)
class AgentDefinition:
    role: str
    goal: str
    input: Any
    tools: tuple[str, ...]
    memory: str | None
    max_steps: int
    output_schema: Mapping[str, str]

    def __post_init__(self) -> None:
        if not self.role.strip():
            raise ValueError("ROLE cannot be empty")
        if not self.goal.strip():
            raise ValueError("GOAL cannot be empty")
        if self.max_steps < 1 or self.max_steps > 20:
            raise ValueError("MAX_STEPS must be between 1 and 20")
        normalized = tuple(name.strip() for name in self.tools)
        if any(not name for name in normalized):
            raise ValueError("TOOLS cannot contain blank names")
        if len(set(normalized)) != len(normalized):
            raise ValueError("TOOLS cannot contain duplicates")
        object.__setattr__(self, "tools", normalized)
        if self.memory is not None and not self.memory.strip():
            raise ValueError("MEMORY query cannot be blank")

    def to_contract_dict(self) -> dict[str, Any]:
        return {
            "ROLE": self.role,
            "GOAL": self.goal,
            "INPUT": self.input,
            "TOOLS": list(self.tools),
            "MEMORY": self.memory,
            "MAX_STEPS": self.max_steps,
            "OUTPUT_SCHEMA": dict(self.output_schema),
        }


@dataclass(frozen=True)
class AgentAction:
    action: str
    tool: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)
    output: Any = None

    @classmethod
    def parse(cls, response_text: str) -> "AgentAction":
        try:
            value = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise ValueError("strict agent response must be one JSON object") from exc
        if not isinstance(value, dict):
            raise ValueError("strict agent response must be one JSON object")
        action = str(value.get("action", "")).strip().upper()
        if action == "TOOL":
            tool = value.get("tool")
            arguments = value.get("arguments", {})
            if not isinstance(tool, str) or not tool.strip():
                raise ValueError("TOOL action requires a tool name")
            if not isinstance(arguments, dict):
                raise ValueError("TOOL arguments must be an object")
            return cls(action="TOOL", tool=tool.strip(), arguments=arguments)
        if action == "FINISH":
            return cls(action="FINISH", output=value.get("output"))
        raise ValueError("strict agent action must be TOOL or FINISH")


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
