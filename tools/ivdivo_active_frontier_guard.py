from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


REQUIRED_DEPENDENCY = "REQUIRED_DEPENDENCY"
SAME_PROJECT_RELEVANT = "SAME_PROJECT_RELEVANT"
SUPPORTING = "SUPPORTING"
SIBLING = "SIBLING"
UNKNOWN = "UNKNOWN"
_ALLOWED_RELATIONS = {
    REQUIRED_DEPENDENCY,
    SAME_PROJECT_RELEVANT,
    SUPPORTING,
    SIBLING,
    UNKNOWN,
}


@dataclass(frozen=True)
class FrontierDecision:
    status: str
    active_project: Optional[str]
    active_next_gate: Optional[str]
    return_token: Optional[str] = None
    reason: str = ""


def _return_token(project: str, next_gate: str) -> str:
    return f"RETURN_FRONTIER::{project}::{next_gate}"


def decide_frontier_use(
    *,
    active_project: Optional[str],
    active_next_gate: Optional[str],
    discovered_material_project: Optional[str],
    relation_to_current_gate: str,
) -> FrontierDecision:
    """Classify discovered material after thread-level routing is already settled.

    This layer deliberately has no project-switch authority. Project switching belongs
    to the Thread Topic Continuity Guard. The frontier layer may use same-project
    evidence, permit a bounded required dependency with a return token, keep
    sibling/supporting material as context only, or fail closed.
    """
    if not active_project or not active_next_gate:
        return FrontierDecision(
            "HOLD_NO_ACTIVE_FRONTIER",
            active_project,
            active_next_gate,
            reason="Restore the active project's next gate before frontier classification.",
        )

    relation = str(relation_to_current_gate or "").strip().upper()
    if relation not in _ALLOWED_RELATIONS:
        relation = UNKNOWN

    discovered = (discovered_material_project or "").strip() or None

    if relation == REQUIRED_DEPENDENCY:
        if not discovered:
            return FrontierDecision(
                "HOLD_REQUIRED_DEPENDENCY_WITHOUT_PROJECT",
                active_project,
                active_next_gate,
                reason="A required cross-project dependency must identify the dependency project.",
            )
        if discovered == active_project:
            return FrontierDecision(
                "USE_IN_CURRENT_FRONTIER",
                active_project,
                active_next_gate,
                reason="The required material belongs to the active project; no cross-project detour is needed.",
            )
        return FrontierDecision(
            "CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN",
            active_project,
            active_next_gate,
            return_token=_return_token(active_project, active_next_gate),
            reason="The current next gate proves a bounded cross-project dependency; return to the original frontier afterward.",
        )

    if relation == SAME_PROJECT_RELEVANT:
        if discovered in (None, active_project):
            return FrontierDecision(
                "USE_IN_CURRENT_FRONTIER",
                active_project,
                active_next_gate,
                reason="Material is same-project evidence relevant to the current next gate.",
            )
        return FrontierDecision(
            "HOLD_PROJECT_RELATION_CONFLICT_KEEP_FRONTIER",
            active_project,
            active_next_gate,
            reason="Material claimed as same-project points to another project; preserve the frontier and fail closed.",
        )

    if relation in {SUPPORTING, SIBLING}:
        return FrontierDecision(
            "SUPPORTING_ONLY_KEEP_FRONTIER",
            active_project,
            active_next_gate,
            reason="Supporting or sibling material may enrich context but cannot replace the active next gate.",
        )

    return FrontierDecision(
        "HOLD_AMBIGUOUS_SCOPE_KEEP_FRONTIER",
        active_project,
        active_next_gate,
        reason="Unknown relation cannot change execution routing.",
    )


def resolve_return_token(return_token: Optional[str]) -> FrontierDecision:
    if not return_token or not return_token.startswith("RETURN_FRONTIER::"):
        return FrontierDecision(
            "HOLD_INVALID_RETURN_TOKEN",
            None,
            None,
            reason="A valid frontier return token is required.",
        )
    parts = return_token.split("::", 2)
    if len(parts) != 3 or not parts[1] or not parts[2]:
        return FrontierDecision(
            "HOLD_INVALID_RETURN_TOKEN",
            None,
            None,
            reason="Malformed frontier return token.",
        )
    return FrontierDecision(
        "RETURN_TO_ORIGINAL_FRONTIER",
        parts[1],
        parts[2],
        return_token=return_token,
        reason="Bounded dependency ended; restore the original project frontier.",
    )
