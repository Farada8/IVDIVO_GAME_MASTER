"""Saga100 semantic contracts.

WORKING integration candidate. These checks never promote story canon; they reject unsafe
inferences and return HOLD when authority/evidence is insufficient.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Sequence

CAPABILITY_STAGES = [
    "EXISTS_ELSEWHERE",
    "KNOWN",
    "CONTACT_ACCESS",
    "RESTRICTED_USE",
    "LOCAL_PROTOTYPE",
    "LEGALIZED_USE",
    "SCALABLE_MANUFACTURE",
    "ORDINARY_LIFE",
]

BOOK_INDEPENDENCE_FIELDS = (
    "hero", "want", "why_now", "opposition", "wrong_strategy", "price",
    "midpoint", "climax_choice", "resolution", "change",
)

NO_REPEAT_AXES = (
    "primary_human_problem",
    "protagonist_social_position",
    "arena",
    "genre_emphasis",
    "ivdivo_amplifier",
    "closure_type",
    "relationship_configuration",
)

AUTHORITY_PRIORITY = {
    "FOUNDER_NEWEST_DIRECT_INSTRUCTION": 100,
    "LOCKED_PROJECT_AUTHORITY": 90,
    "MASTER_SAGA_BIBLE": 80,
    "CURRENT_NARRATIVE_OS": 80,
    "CURRENT_PROJECT_ARCHITECTURE": 70,
    "SAGA100_WORKING_LAYER": 60,
    "WORKING_DRAFT": 40,
    "HISTORICAL_SEED": 20,
    "REFERENCE": 10,
}


@dataclass(frozen=True)
class ContractResult:
    status: str
    reasons: tuple[str, ...] = ()
    data: Mapping[str, Any] | None = None

    @property
    def passed(self) -> bool:
        return self.status == "PASS"


def resolve_authority(candidates: Sequence[Mapping[str, Any]]) -> ContractResult:
    """R25: choose one highest authority or HOLD on a same-rank contradiction."""
    if not candidates:
        return ContractResult("HOLD", ("NO_AUTHORITY_CANDIDATES",))
    ranked: List[tuple[int, Mapping[str, Any]]] = []
    for item in candidates:
        rank = AUTHORITY_PRIORITY.get(str(item.get("authority_class")), 0)
        ranked.append((rank, item))
    max_rank = max(rank for rank, _ in ranked)
    top = [item for rank, item in ranked if rank == max_rank]
    values = {repr(item.get("value")) for item in top}
    if len(values) > 1:
        return ContractResult(
            "HOLD",
            ("SAME_RANK_AUTHORITY_CONFLICT",),
            {"rank": max_rank, "refs": [i.get("ref") for i in top]},
        )
    return ContractResult("PASS", data={"winner": top[0], "rank": max_rank})


def continuity_substitution_gate(
    required_fields: Sequence[str],
    values: Mapping[str, Any],
    outcome_critical: Iterable[str] = (),
) -> ContractResult:
    """R26: unresolved required continuity is first-class UNKNOWN, never guessed."""
    critical = set(outcome_critical)
    missing = [f for f in required_fields if values.get(f) in (None, "", "UNKNOWN")]
    blocking = [f for f in missing if f in critical]
    if blocking:
        return ContractResult("HOLD", ("OUTCOME_CRITICAL_CONTINUITY_UNKNOWN",), {"fields": blocking})
    if missing:
        return ContractResult("PARTIAL", ("NONCRITICAL_CONTINUITY_UNKNOWN",), {"fields": missing})
    return ContractResult("PASS")


def capability_transition_gate(
    current_stage: str,
    target_stage: str,
    evidence_refs: Sequence[str],
    consequence_refs: Sequence[str],
    *,
    exception: bool = False,
    exception_reason: str | None = None,
) -> ContractResult:
    """R27: capability progression cannot silently skip civilizational stages."""
    if current_stage not in CAPABILITY_STAGES or target_stage not in CAPABILITY_STAGES:
        return ContractResult("FAIL", ("UNKNOWN_CAPABILITY_STAGE",))
    if not evidence_refs or not consequence_refs:
        return ContractResult("FAIL", ("MISSING_EVIDENCE_OR_CONSEQUENCE",))
    a, b = CAPABILITY_STAGES.index(current_stage), CAPABILITY_STAGES.index(target_stage)
    if b < a:
        return ContractResult("FAIL", ("CAPABILITY_REGRESSION_REQUIRES_EXPLICIT_EVENT_MODEL",))
    if b > a + 1 and not (exception and exception_reason and evidence_refs):
        return ContractResult("FAIL", ("UNPROVEN_CAPABILITY_STAGE_SKIP",), {"from": current_stage, "to": target_stage})
    if b > a + 1:
        return ContractResult("PASS", ("EXPLICIT_EXCEPTION_RECORDED",), {"exception_reason": exception_reason})
    return ContractResult("PASS")


def crossing_eligibility_gate(spec: Mapping[str, Any]) -> ContractResult:
    """R28: Crossing must be causally necessary, not franchise fan service."""
    failures: List[str] = []
    if not spec.get("prerequisite_line_closure"):
        failures.append("PREREQUISITE_LINE_BOOKS_NOT_LOCALLY_CLOSED")
    if not spec.get("upstream_consequences_loaded"):
        failures.append("UPSTREAM_CONSEQUENCES_NOT_LOADED")
    if int(spec.get("irreducible_line_dependencies", 0)) < 2:
        failures.append("FEWER_THAN_TWO_IRREDUCIBLE_LINE_DEPENDENCIES")
    if not spec.get("rights_or_jurisdiction_conflict"):
        failures.append("NO_RIGHTS_OR_JURISDICTION_CONFLICT")
    if spec.get("advanced_actor_auto_commands"):
        failures.append("ADVANCED_ACTOR_AUTO_COMMANDS")
    if not spec.get("shared_civilization_delta"):
        failures.append("NO_SHARED_CIVILIZATION_DELTA")
    return ContractResult("FAIL" if failures else "PASS", tuple(failures))


def book_independence_gate(book: Mapping[str, Any]) -> ContractResult:
    """R29: every book must close its own main conflict before series hook."""
    missing = [f for f in BOOK_INDEPENDENCE_FIELDS if not book.get(f)]
    if missing:
        return ContractResult("FAIL", ("MISSING_BOOK_CORE",), {"fields": missing})
    if not book.get("main_conflict_closed"):
        return ContractResult("FAIL", ("MAIN_CONFLICT_DEFERRED_TO_NEXT_BOOK",))
    if book.get("series_hook_before_resolution"):
        return ContractResult("FAIL", ("SERIES_HOOK_PRECEDES_RESOLUTION",))
    return ContractResult("PASS")


def no_repeat_gate(candidate: Mapping[str, Any], prior: Mapping[str, Any], minimum_distinct_axes: int = 4) -> ContractResult:
    """R30: require meaningful differentiation from nearby books."""
    distinct = [axis for axis in NO_REPEAT_AXES if candidate.get(axis) != prior.get(axis)]
    if len(distinct) < minimum_distinct_axes:
        return ContractResult("FAIL", ("INSUFFICIENT_DISTINCT_AXES",), {"distinct_axes": distinct, "count": len(distinct)})
    return ContractResult("PASS", data={"distinct_axes": distinct, "count": len(distinct)})


def reveal_budget_gate(reveals: Sequence[Mapping[str, Any]], allowed_ceiling: int) -> ContractResult:
    """R31: later-saga answers cannot be spent early merely to make one book feel bigger."""
    violations = []
    for r in reveals:
        if int(r.get("level", 0)) > allowed_ceiling:
            violations.append(str(r.get("id", "UNKNOWN")))
        if r.get("requires_future_founder_lock") and r.get("spent_now"):
            violations.append(str(r.get("id", "UNKNOWN")) + ":FUTURE_LOCK_SPENT")
    if violations:
        return ContractResult("FAIL", ("REVEAL_CEILING_VIOLATION",), {"violations": violations})
    return ContractResult("PASS")


def strategic_freshness_gate(request_scope: Sequence[str], loaded_layers: Sequence[str]) -> ContractResult:
    """R32: reproduce/prevent the NARR-009 omission class.

    Long-horizon sequencing is unsafe when only current execution/project state is loaded.
    """
    scope = set(request_scope)
    layers = set(loaded_layers)
    if "LONG_HORIZON_SAGA" in scope or "SAGA_SEQUENCE" in scope:
        required = {"CURRENT_EXECUTION_AUTHORITY", "LONG_HORIZON_STRATEGIC_AUTHORITY"}
        missing = sorted(required - layers)
        if missing:
            return ContractResult("FAIL", ("STRATEGIC_AUTHORITY_NOT_LOADED",), {"missing_layers": missing})
    if "ACTIVE_BOOK_EXECUTION" in scope and "CURRENT_EXECUTION_AUTHORITY" not in layers:
        return ContractResult("FAIL", ("CURRENT_EXECUTION_AUTHORITY_NOT_LOADED",))
    return ContractResult("PASS")
