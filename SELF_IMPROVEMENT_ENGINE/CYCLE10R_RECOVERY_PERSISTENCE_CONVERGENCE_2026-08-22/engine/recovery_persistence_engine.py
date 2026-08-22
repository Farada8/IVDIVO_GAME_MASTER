"""Cycle10R recovery/persistence controls.

This module is deliberately small. It extends existing Self-Improvement v2 / SI-0014 /
SI-0015 semantics; it is not a second durable transaction engine and it cannot promote
Self-Improvement authority by itself.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping, Sequence


COMPLETE = "COMPLETE"
PARTIAL = "PARTIAL"
FAILED = "FAILED"
REBASE_FIRST = "REBASE_FIRST"
CURRENT = "CURRENT"
HOLD = "HOLD"


@dataclass(frozen=True)
class RecoverySlice:
    project_id: str
    frontier: str
    github_readback: bool
    drive_readback: bool
    false_resume: bool = False
    source_refs: tuple[str, ...] = ()

    @property
    def complete(self) -> bool:
        return bool(
            self.project_id
            and self.frontier
            and self.github_readback
            and self.drive_readback
            and not self.false_resume
        )


@dataclass(frozen=True)
class RecoveryIncident:
    incident_id: str
    real_interruption: bool
    slices: tuple[RecoverySlice, ...] = ()

    @property
    def qualifies(self) -> bool:
        if not self.incident_id or not self.real_interruption or not self.slices:
            return False
        # A qualifying incident may contain many project slices, but a false resume in
        # any claimed recovered slice invalidates the zero-false-resume requirement.
        return all(s.complete for s in self.slices)


@dataclass(frozen=True)
class CrossStoreArtifactRecord:
    logical_id: str
    github_present: bool
    github_readback: bool
    drive_present: bool
    drive_readback: bool
    expected_anchors: tuple[str, ...] = ()
    observed_text: str = ""

    def anchors_pass(self) -> bool:
        return bool(self.expected_anchors) and all(
            anchor in self.observed_text for anchor in self.expected_anchors
        )

    def persistence_state(self) -> str:
        gh_ok = self.github_present and self.github_readback
        dr_ok = self.drive_present and self.drive_readback
        if gh_ok and dr_ok and self.anchors_pass():
            return COMPLETE
        if gh_ok or dr_ok:
            return PARTIAL
        return FAILED


@dataclass(frozen=True)
class FreshnessVector:
    embedded_pointer: str | None
    latest_verified_pointer: str | None
    latest_closure_verified: bool

    def route(self) -> str:
        if not self.latest_verified_pointer or not self.latest_closure_verified:
            return HOLD
        if self.embedded_pointer != self.latest_verified_pointer:
            return REBASE_FIRST
        return CURRENT


def qualified_event_ids(events: Iterable[RecoveryIncident]) -> set[str]:
    return {event.incident_id for event in events if event.qualifies}


def qualified_event_count(events: Iterable[RecoveryIncident]) -> int:
    return len(qualified_event_ids(events))


def distinct_project_ids(events: Iterable[RecoveryIncident]) -> set[str]:
    projects: set[str] = set()
    for event in events:
        if not event.qualifies:
            continue
        for item in event.slices:
            if item.complete:
                projects.add(item.project_id)
    return projects


def si0014_promotion_state(
    events: Iterable[RecoveryIncident],
    *,
    required_events: int = 3,
    required_projects: int = 2,
) -> Mapping[str, object]:
    events = tuple(events)
    event_count = qualified_event_count(events)
    project_count = len(distinct_project_ids(events))
    eligible = event_count >= required_events and project_count >= required_projects
    return {
        "qualified_events": event_count,
        "distinct_projects": project_count,
        "required_events": required_events,
        "required_projects": required_projects,
        "promotion_authorized": False,  # machine never grants authority
        "eligible_for_promotion_review": eligible,
        "state": "ELIGIBLE_FOR_REVIEW" if eligible else "READY_FOR_PILOT",
    }


def partial_repair_plan(record: CrossStoreArtifactRecord) -> tuple[str, ...]:
    """Return only missing safe persistence actions; never replay accepted sides."""
    actions: list[str] = []
    gh_ok = record.github_present and record.github_readback
    dr_ok = record.drive_present and record.drive_readback
    if not gh_ok:
        actions.append("VERIFY_THEN_WRITE_GITHUB")
    if not dr_ok:
        actions.append("VERIFY_THEN_WRITE_DRIVE")
    if gh_ok and dr_ok and not record.anchors_pass():
        actions.append("REPAIR_SEMANTIC_CONTENT_OR_HOLD")
    return tuple(actions)


def semantic_salvage_route(
    *,
    newer_authority_exists: bool,
    delta_unique: bool,
    delta_compatible: bool,
) -> str:
    if newer_authority_exists and not delta_unique:
        return "PROVENANCE_ONLY"
    if not delta_compatible:
        return "HOLD_CONFLICT"
    if newer_authority_exists and delta_unique:
        return "SALVAGE_UNIQUE_DELTA_AFTER_REBASE"
    return "APPLY_AFTER_REGRESSION"


def normalize_evidence_families(root_ids: Sequence[str]) -> int:
    """Multiple derived reports with one root remain one evidence family."""
    return len({root for root in root_ids if root})


def candidate_id_route(candidate_id: str, committed: set[str], reserved: set[str]) -> str:
    if not candidate_id:
        return "HOLD_NO_ID"
    if candidate_id in committed or candidate_id in reserved:
        return "HOLD_ID_COLLISION"
    return "UNRESERVED_ONLY_NOT_AUTHORIZED"


def v3_mechanism_tribunal(
    *,
    existing_owner: bool,
    real_project_replications: int,
    healthy_controls: int,
    measured_net_gain: bool,
    regression_pass: bool,
) -> str:
    if existing_owner:
        return "MERGE_WITH_EXISTING_OWNER"
    if (
        real_project_replications >= 2
        and healthy_controls >= 1
        and measured_net_gain
        and regression_pass
    ):
        return "ELIGIBLE_FOR_BOUNDED_PROMOTION_REVIEW"
    return "HOLD_FOR_REAL_PRODUCTION_EVIDENCE"


def production_return_gate(target: str | None, meta_step_changes_decision: bool) -> str:
    if not target:
        return "HOLD_NO_PRODUCTION_RETURN"
    if not meta_step_changes_decision:
        return "RETURN_TO_PRODUCTION_NO_MORE_META"
    return "RETURN_TO_PRODUCTION_AFTER_PERSISTENCE"


def library_identity_state(
    *,
    physical_id: str | None,
    byte_hash: str | None,
    canonical_work_id: str | None,
) -> Mapping[str, object]:
    """Never infer hash/canonical identity from a physical file identifier."""
    return {
        "physical_present": bool(physical_id),
        "byte_hash_proven": bool(byte_hash),
        "canonical_work_proven": bool(canonical_work_id),
        "unique_work_claim_allowed": bool(byte_hash and canonical_work_id),
    }
