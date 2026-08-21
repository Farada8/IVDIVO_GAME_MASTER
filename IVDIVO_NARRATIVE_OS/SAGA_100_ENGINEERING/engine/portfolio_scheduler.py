"""Gate-aware Saga100 portfolio scheduler.

Scores prioritize work but can never bypass Founder/authority/human gates.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

WEIGHTS = {
    "dependency_readiness": 0.25,
    "asset_maturity": 0.20,
    "civilization_need": 0.15,
    "line_balance": 0.10,
    "diversity": 0.10,
    "evidence_need": 0.10,
    "production_capacity_fit": 0.10,
}

HARD_GATES = {
    "FOUNDER_DECISION_REQUIRED",
    "AUTHORITY_CONFLICT",
    "UPSTREAM_CONTINUITY_REQUIRED",
    "HUMAN_EXTERNAL_EVIDENCE_REQUIRED",
    "UNRESOLVED_FATAL_OR_MAJOR",
}

@dataclass(frozen=True)
class ScheduleResult:
    score: float
    executable_now: bool
    gate: str | None
    lane: str


def schedule_score(item: Mapping[str, object]) -> ScheduleResult:
    raw = 0.0
    for key, weight in WEIGHTS.items():
        value = float(item.get(key, 0.0))
        if not 0.0 <= value <= 100.0:
            raise ValueError(f"{key} must be 0..100")
        raw += value * weight
    gate = item.get("gate")
    executable = gate not in HARD_GATES and not bool(item.get("blocked", False))
    lane = str(item.get("lane", "STORY_PRODUCTION"))
    return ScheduleResult(round(raw, 2), executable, str(gate) if gate else None, lane)


def compare(a: Mapping[str, object], b: Mapping[str, object]) -> int:
    """Executable work always ranks above blocked work; score orders within same gate class."""
    ra, rb = schedule_score(a), schedule_score(b)
    if ra.executable_now != rb.executable_now:
        return -1 if ra.executable_now else 1
    if ra.score == rb.score:
        return 0
    return -1 if ra.score > rb.score else 1
