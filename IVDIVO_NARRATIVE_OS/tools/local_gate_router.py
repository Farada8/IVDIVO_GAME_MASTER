from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

GLOBAL_GATE_TYPES = {
    "AUTHORITY_UNRESOLVED",
    "FRONTIER_CONFLICT",
    "CANON_APPROVAL_REQUIRED",
    "SAFETY_LEGAL",
    "EXPLICIT_FOUNDER_STOP",
}

LOCAL_GATE_TYPES = {
    "HUMAN_EVIDENCE_REQUIRED",
    "EXTERNAL_PROVIDER_REQUIRED",
    "TOOL_RUNTIME_LIMITATION",
    "MISSING_INPUT",
    "DEPENDENCY_BLOCKED",
    "UNRESOLVED_FATAL_MAJOR_LOCAL",
}


@dataclass(frozen=True)
class Obligation:
    id: str
    priority: int
    status: str = "READY"
    gate_type: str | None = None
    dependencies: tuple[str, ...] = ()
    scope: str = "PROJECT"


@dataclass(frozen=True)
class RouteDecision:
    action: str
    selected_id: str | None
    blocked_local: tuple[str, ...]
    blocked_global: tuple[str, ...]
    reason: str


def _dependency_map(obligations: Sequence[Obligation]) -> dict[str, Obligation]:
    return {o.id: o for o in obligations}


def _deps_ready(o: Obligation, by_id: dict[str, Obligation]) -> bool:
    for dep_id in o.dependencies:
        dep = by_id.get(dep_id)
        if dep is None or dep.status != "DONE":
            return False
    return True


def route(obligations: Iterable[Obligation]) -> RouteDecision:
    items = list(obligations)
    by_id = _dependency_map(items)

    blocked_global = tuple(
        o.id
        for o in items
        if o.status == "BLOCKED" and o.gate_type in GLOBAL_GATE_TYPES
    )
    if blocked_global:
        return RouteDecision(
            action="GLOBAL_STOP",
            selected_id=None,
            blocked_local=(),
            blocked_global=blocked_global,
            reason="At least one authoritative global gate blocks safe continuation.",
        )

    blocked_local = tuple(
        o.id
        for o in items
        if o.status == "BLOCKED"
        and (o.gate_type in LOCAL_GATE_TYPES or o.gate_type not in GLOBAL_GATE_TYPES)
    )

    ready = [
        o
        for o in items
        if o.status == "READY" and _deps_ready(o, by_id)
    ]
    if ready:
        selected = sorted(ready, key=lambda o: (o.priority, o.id))[0]
        return RouteDecision(
            action="CONTINUE",
            selected_id=selected.id,
            blocked_local=blocked_local,
            blocked_global=(),
            reason="Local gates do not stop independent executable work.",
        )

    if blocked_local:
        return RouteDecision(
            action="LOCAL_GATE_ONLY_NO_READY_SIBLING",
            selected_id=None,
            blocked_local=blocked_local,
            blocked_global=(),
            reason="Current executable queue is exhausted; blocked branches remain local.",
        )

    return RouteDecision(
        action="QUEUE_EMPTY",
        selected_id=None,
        blocked_local=(),
        blocked_global=(),
        reason="No READY obligations remain.",
    )
