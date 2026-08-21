from dataclasses import dataclass, field
from typing import Tuple


EXEMPT_SLICE_KINDS = {"HISTORICAL", "SUPERSEDED", "REFERENCE"}


@dataclass(frozen=True)
class ProjectSlice:
    slice_kind: str
    embedded_frontier: str
    controlling_frontiers: Tuple[str, ...]
    pointer_resolved: bool = True
    required_approval_event: str | None = None
    observed_events: Tuple[str, ...] = field(default_factory=tuple)


def classify_slice(project_slice: ProjectSlice) -> str:
    """Return one SI-0015 contract output without mutating project state."""
    if project_slice.slice_kind in EXEMPT_SLICE_KINDS:
        return "EXEMPT_HISTORICAL_SLICE"

    if not project_slice.pointer_resolved or len(project_slice.controlling_frontiers) != 1:
        return "UNRESOLVED_POINTER"

    if (
        project_slice.required_approval_event
        and project_slice.required_approval_event not in set(project_slice.observed_events)
    ):
        return "APPROVAL_EVENT_MISSING"

    if project_slice.embedded_frontier != project_slice.controlling_frontiers[0]:
        return "STALE_CURRENT_SLICE"

    return "CURRENT_MATCH"
