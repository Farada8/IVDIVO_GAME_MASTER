from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


REQUIRED_DEPENDENCY = "REQUIRED_DEPENDENCY"
SAME_PROJECT_RELEVANT = "SAME_PROJECT_RELEVANT"
SUPPORTING = "SUPPORTING"
SIBLING = "SIBLING"
UNKNOWN = "UNKNOWN"


@dataclass(frozen=True)
class FrontierDecision:
    status: str
    active_project: Optional[str]
    active_next_gate: Optional[str]
    return_token: Optional[str] = None
    reason: str = ""


def decide_frontier_use(
    *,
    active_project: Optional[str],
    active_next_gate: Optional[str],
    discovered_material_project: Optional[str],
    relation_to_current_gate: str,
    explicit_user_switch: bool = False,
) -> FrontierDecision:
    """Fail-closed router for discovered cross-project material.

    Semantic relevance is never enough to authorize a frontier switch.
    """
    if not active_project or not active_next_gate:
        return FrontierDecision(
            "HOLD_NO_ACTIVE_FRONTIER",
            active_project,
            active_next_gate,
            reason="Current frontier must be restored before discovered material can route execution.",
        )

    if explicit_user_switch:
        return FrontierDecision(
            "SWITCH_AUTHORIZED",
            discovered_material_project or active_project,
            active_next_gate,
            reason="Explicit user switch event outranks the existing frontier.",
        )

    if relation_to_current_gate == REQUIRED_DEPENDENCY:
        token = f"RETURN::{active_project}::{active_next_gate}"
        return FrontierDecision(
            "CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN",
            active_project,
            active_next_gate,
            return_token=token,
            reason="Material is a proven dependency of the current next gate; bounded cross-lane work is allowed.",
        )

    if relation_to_current_gate == SAME_PROJECT_RELEVANT:
        if discovered_material_project in (None, active_project):
            return FrontierDecision(
                "USE_IN_CURRENT_FRONTIER",
                active_project,
                active_next_gate,
                reason="Material belongs to the active project and is relevant to the current gate.",
            )
        return FrontierDecision(
            "SUPPORTING_ONLY_KEEP_FRONTIER",
            active_project,
            active_next_gate,
            reason="Claimed same-project relevance conflicts with a different project identity; keep frontier.",
        )

    if relation_to_current_gate in (SUPPORTING, SIBLING):
        return FrontierDecision(
            "SUPPORTING_ONLY_KEEP_FRONTIER",
            active_project,
            active_next_gate,
            reason="Sibling/supporting evidence may enrich context but may not change the active frontier.",
        )

    return FrontierDecision(
        "HOLD_AMBIGUOUS_SCOPE_KEEP_FRONTIER",
        active_project,
        active_next_gate,
        reason="Unknown or unsupported relation fails closed; preserve current frontier.",
    )


def resolve_return_token(return_token: Optional[str]) -> FrontierDecision:
    if not return_token or not return_token.startswith("RETURN::"):
        return FrontierDecision(
            "HOLD_INVALID_RETURN_TOKEN", None, None, reason="A valid return token is required."
        )
    parts = return_token.split("::", 2)
    if len(parts) != 3 or not parts[1] or not parts[2]:
        return FrontierDecision(
            "HOLD_INVALID_RETURN_TOKEN", None, None, reason="Malformed return token."
        )
    return FrontierDecision(
        "RETURN_TO_ORIGINAL_FRONTIER",
        parts[1],
        parts[2],
        return_token=return_token,
        reason="Bounded dependency ended; restore the original causal frontier.",
    )
