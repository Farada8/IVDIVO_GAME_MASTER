"""State machine for Saga100 slot capacity grid.

A slot is a planning coordinate, never permission to invent/renumber a PROJECT_ID.
"""
from __future__ import annotations

from dataclasses import dataclass

STATES = (
    "EMPTY",
    "FUNCTION_ONLY",
    "CANDIDATE_MAPPED",
    "AUTHORITY_HOLD",
    "DISCOVERY",
    "ARCHITECTURE",
    "STORY_GATE",
    "PROSE",
    "DEVELOPMENT",
    "FINAL_GATE",
    "LOCKED",
    "DOWNSTREAM",
    "DEFERRED",
    "RETIRED_UNUSED",
)

ALLOWED = {
    "EMPTY": {"FUNCTION_ONLY", "RETIRED_UNUSED"},
    "FUNCTION_ONLY": {"CANDIDATE_MAPPED", "AUTHORITY_HOLD", "DEFERRED", "RETIRED_UNUSED"},
    "CANDIDATE_MAPPED": {"AUTHORITY_HOLD", "DISCOVERY", "DEFERRED"},
    "AUTHORITY_HOLD": {"CANDIDATE_MAPPED", "DISCOVERY", "DEFERRED", "RETIRED_UNUSED"},
    "DISCOVERY": {"AUTHORITY_HOLD", "ARCHITECTURE", "DEFERRED"},
    "ARCHITECTURE": {"AUTHORITY_HOLD", "STORY_GATE", "DEFERRED"},
    "STORY_GATE": {"AUTHORITY_HOLD", "ARCHITECTURE", "PROSE", "DEFERRED"},
    "PROSE": {"AUTHORITY_HOLD", "DEVELOPMENT"},
    "DEVELOPMENT": {"AUTHORITY_HOLD", "FINAL_GATE", "PROSE"},
    "FINAL_GATE": {"AUTHORITY_HOLD", "DEVELOPMENT", "LOCKED"},
    "LOCKED": {"DOWNSTREAM"},
    "DOWNSTREAM": set(),
    "DEFERRED": {"FUNCTION_ONLY", "CANDIDATE_MAPPED", "AUTHORITY_HOLD", "RETIRED_UNUSED"},
    "RETIRED_UNUSED": set(),
}

@dataclass(frozen=True)
class TransitionResult:
    allowed: bool
    reason: str


def validate_slot_id(slot_id: str) -> bool:
    if not slot_id.startswith("S100-C") or len(slot_id) < 11:
        return False
    try:
        cycle = int(slot_id[6:8])
    except ValueError:
        return False
    return 1 <= cycle <= 25 and slot_id[-1] in {"S", "O", "C", "X"}


def transition(current: str, target: str, *, project_id: str | None = None, authority_clear: bool = True, crossing_eligible: bool | None = None) -> TransitionResult:
    if current not in STATES or target not in STATES:
        return TransitionResult(False, "UNKNOWN_STATE")
    if target not in ALLOWED[current]:
        return TransitionResult(False, "FORBIDDEN_TRANSITION")
    if target in {"DISCOVERY","ARCHITECTURE","STORY_GATE","PROSE","DEVELOPMENT","FINAL_GATE","LOCKED"} and not project_id:
        return TransitionResult(False, "NO_DURABLE_PROJECT_ID")
    if not authority_clear and target not in {"AUTHORITY_HOLD","DEFERRED","RETIRED_UNUSED"}:
        return TransitionResult(False, "AUTHORITY_NOT_CLEAR")
    if target == "PROSE" and current != "STORY_GATE":
        return TransitionResult(False, "PROSE_REQUIRES_STORY_GATE")
    if target == "LOCKED" and current != "FINAL_GATE":
        return TransitionResult(False, "LOCK_REQUIRES_FINAL_GATE")
    if crossing_eligible is False and target in {"PROSE","DEVELOPMENT","FINAL_GATE","LOCKED"}:
        return TransitionResult(False, "CROSSING_NOT_ELIGIBLE")
    return TransitionResult(True, "PASS")


def cycle_slot_ids() -> list[str]:
    return [f"S100-C{cycle:02d}-{role}" for cycle in range(1,26) for role in ("S","O","C","X")]
