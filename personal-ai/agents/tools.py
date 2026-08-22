from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Callable

from memory.store import MemoryStore


@dataclass(frozen=True)
class ToolContext:
    project_id: str
    task_id: str
    memory: MemoryStore


ToolCallable = Callable[[dict[str, Any], ToolContext], Any]


class ToolRegistry:
    """Explicit named tool registry. Only registered + agent-allowlisted tools may run."""

    def __init__(self) -> None:
        self._tools: dict[str, ToolCallable] = {}

    def register(self, name: str, fn: ToolCallable) -> None:
        key = name.strip()
        if not key:
            raise ValueError("tool name cannot be empty")
        if key in self._tools:
            raise ValueError(f"tool already registered: {key}")
        self._tools[key] = fn

    def call(self, name: str, arguments: dict[str, Any], context: ToolContext) -> Any:
        try:
            fn = self._tools[name]
        except KeyError as exc:
            raise PermissionError(f"tool is not registered: {name}") from exc
        result = fn(arguments, context)
        json.dumps(result)
        return result

    @classmethod
    def core(cls) -> "ToolRegistry":
        registry = cls()

        def memory_search(arguments: dict[str, Any], context: ToolContext) -> Any:
            query = str(arguments.get("query", "")).strip()
            if not query:
                raise ValueError("memory_search requires query")
            limit = int(arguments.get("limit", 10))
            if limit < 1 or limit > 50:
                raise ValueError("memory_search limit must be between 1 and 50")
            kind = arguments.get("kind")
            rows = context.memory.search(
                query,
                kind=str(kind) if kind is not None else None,
                project_id=context.project_id,
                limit=limit,
            )
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

        def echo(arguments: dict[str, Any], context: ToolContext) -> Any:
            del context
            return arguments

        registry.register("memory_search", memory_search)
        registry.register("echo", echo)
        return registry
