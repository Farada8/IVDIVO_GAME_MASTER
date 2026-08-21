#!/usr/bin/env python3
"""Wave11 dependency-aware external-evidence frontier evaluator.

Routing-only helper for Wave11 prompts 01-32. It does not validate provider,
human, live-audio, economics, or release truth. Those claims remain owned by the
canonical Audio Studio receipt validators. This module only answers which prompt
can be attempted next given an explicitly supplied set of already completed
prompt IDs, and fails closed on impossible completion ordering.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


class ActionClass(str, Enum):
    ENGINEERING = "ENGINEERING"
    PROVIDER_READ = "PROVIDER_READ"
    REAL_AUDIO = "REAL_AUDIO"
    HUMAN_REVIEW = "HUMAN_REVIEW"
    HUMAN_LOCK = "HUMAN_LOCK"
    PAID_DISPATCH = "PAID_DISPATCH"


@dataclass(frozen=True)
class PromptSpec:
    prompt_id: int
    stage: str
    depends_on: tuple[int, ...]
    action_class: ActionClass


PROMPTS: tuple[PromptSpec, ...] = (
    PromptSpec(1, "AUTH_PROVIDER", (), ActionClass.PROVIDER_READ),
    PromptSpec(2, "AUTH_PROVIDER", (1,), ActionClass.ENGINEERING),
    PromptSpec(3, "AUTH_PROVIDER", (2,), ActionClass.PROVIDER_READ),
    PromptSpec(4, "AUTH_PROVIDER", (3,), ActionClass.ENGINEERING),
    PromptSpec(5, "AUTH_PROVIDER", (3,), ActionClass.ENGINEERING),
    PromptSpec(6, "AUTH_PROVIDER", (3,), ActionClass.ENGINEERING),
    PromptSpec(7, "AUTH_PROVIDER", (1,), ActionClass.ENGINEERING),
    PromptSpec(8, "AUTH_PROVIDER", (2, 3, 4, 5, 6, 7), ActionClass.ENGINEERING),
    PromptSpec(9, "INVENTORY_CAST", (8,), ActionClass.ENGINEERING),
    PromptSpec(10, "INVENTORY_CAST", (9,), ActionClass.ENGINEERING),
    PromptSpec(11, "INVENTORY_CAST", (9, 10), ActionClass.ENGINEERING),
    PromptSpec(12, "INVENTORY_CAST", (9, 10), ActionClass.ENGINEERING),
    PromptSpec(13, "INVENTORY_CAST", (9, 10), ActionClass.ENGINEERING),
    PromptSpec(14, "INVENTORY_CAST", (11, 12, 13), ActionClass.ENGINEERING),
    PromptSpec(15, "INVENTORY_CAST", (14,), ActionClass.ENGINEERING),
    PromptSpec(16, "INVENTORY_CAST", (15,), ActionClass.ENGINEERING),
    PromptSpec(17, "PERFORMANCE", (16,), ActionClass.REAL_AUDIO),
    PromptSpec(18, "PERFORMANCE", (16,), ActionClass.REAL_AUDIO),
    PromptSpec(19, "PERFORMANCE", (17,), ActionClass.HUMAN_REVIEW),
    PromptSpec(20, "PERFORMANCE", (17, 18), ActionClass.HUMAN_REVIEW),
    PromptSpec(21, "PERFORMANCE", (16,), ActionClass.REAL_AUDIO),
    PromptSpec(22, "PERFORMANCE", (16,), ActionClass.REAL_AUDIO),
    PromptSpec(23, "PERFORMANCE", (16,), ActionClass.HUMAN_REVIEW),
    PromptSpec(24, "PERFORMANCE", (19, 20, 21, 22, 23), ActionClass.ENGINEERING),
    PromptSpec(25, "LOCK_CANARY", (24,), ActionClass.HUMAN_LOCK),
    PromptSpec(26, "LOCK_CANARY", (25,), ActionClass.ENGINEERING),
    PromptSpec(27, "LOCK_CANARY", (26,), ActionClass.PROVIDER_READ),
    PromptSpec(28, "LOCK_CANARY", (26, 27), ActionClass.ENGINEERING),
    PromptSpec(29, "LOCK_CANARY", (28,), ActionClass.HUMAN_LOCK),
    PromptSpec(30, "LOCK_CANARY", (29,), ActionClass.PAID_DISPATCH),
    PromptSpec(31, "LOCK_CANARY", (30,), ActionClass.HUMAN_REVIEW),
    PromptSpec(32, "LOCK_CANARY", (31,), ActionClass.PAID_DISPATCH),
)

PROMPT_BY_ID = {row.prompt_id: row for row in PROMPTS}


def _validate_static_graph() -> None:
    if tuple(row.prompt_id for row in PROMPTS) != tuple(range(1, 33)):
        raise RuntimeError("WAVE11_PROMPT_SET_MUST_BE_EXACT_01_32")
    for row in PROMPTS:
        for dependency in row.depends_on:
            if dependency not in PROMPT_BY_ID:
                raise RuntimeError(f"UNKNOWN_STATIC_DEPENDENCY:{row.prompt_id}:{dependency}")
            if dependency >= row.prompt_id:
                raise RuntimeError(f"NON_CAUSAL_STATIC_DEPENDENCY:{row.prompt_id}:{dependency}")


_validate_static_graph()


def evaluate_frontier(completed_ids: Iterable[int]) -> dict:
    """Return deterministic routing status without asserting external truth.

    `completed_ids` is routing input supplied by a caller after its own evidence
    validation. This evaluator does not authenticate those completions. If the
    supplied completion set violates the dependency graph, the result is HOLD.
    """
    completed = {int(value) for value in completed_ids}
    unknown = sorted(completed - set(PROMPT_BY_ID))
    if unknown:
        return _base_result(
            status="HOLD_UNKNOWN_COMPLETION_ID",
            completed=completed,
            violations=[{"prompt_id": None, "missing_dependencies": [], "unknown_ids": unknown}],
            rows=[],
        )

    violations = []
    for prompt_id in sorted(completed):
        row = PROMPT_BY_ID[prompt_id]
        missing = sorted(set(row.depends_on) - completed)
        if missing:
            violations.append({"prompt_id": prompt_id, "missing_dependencies": missing})

    rows = []
    ready_ids = []
    for row in PROMPTS:
        if row.prompt_id in completed:
            state = "COMPLETED_ROUTING_INPUT"
            missing = []
        else:
            missing = sorted(set(row.depends_on) - completed)
            if not missing:
                state = f"READY_{row.action_class.value}"
                ready_ids.append(row.prompt_id)
            else:
                state = "BLOCKED_DEPENDENCY"
        rows.append(
            {
                "prompt_id": row.prompt_id,
                "stage": row.stage,
                "action_class": row.action_class.value,
                "depends_on": list(row.depends_on),
                "missing_dependencies": missing,
                "routing_state": state,
            }
        )

    status = "HOLD_DEPENDENCY_VIOLATION" if violations else "PASS_ROUTING_GRAPH"
    result = _base_result(status=status, completed=completed, violations=violations, rows=rows)
    result["next_ready_ids"] = [] if violations else ready_ids
    return result


def _base_result(*, status: str, completed: set[int], violations: list[dict], rows: list[dict]) -> dict:
    return {
        "schema": "ivdivo.audio.wave11_dependency_frontier/1.0",
        "status": status,
        "authority_scope": "ROUTING_ONLY_NOT_EXTERNAL_EVIDENCE",
        "completed_routing_inputs": sorted(completed),
        "dependency_violations": violations,
        "rows": rows,
        "provider_calls_performed": 0,
        "paid_calls_performed": 0,
        "human_reviews_performed": 0,
        "voice_lock": False,
        "release_go": False,
        "provider_dispatch_authorized": False,
        "external_truth_validated": False,
        "law": "External completion must be validated by canonical class-specific receipt validators before a caller supplies it here.",
    }
