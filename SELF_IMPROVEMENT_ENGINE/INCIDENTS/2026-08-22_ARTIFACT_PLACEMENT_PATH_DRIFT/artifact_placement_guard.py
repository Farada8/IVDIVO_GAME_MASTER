from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True)
class ArtifactPlacementInput:
    artifact_id: str
    expected_project_root_id: str
    expected_parent_id: str
    actual_parent_ids: tuple[str, ...]
    start_here_updated: bool
    start_here_readback_contains_artifact: bool
    duplicate_or_legacy_conflict_resolved: bool
    cross_store_required: bool = False
    cross_store_pointer_verified: bool = False


def evaluate_artifact_placement(x: ArtifactPlacementInput) -> dict:
    failures: list[str] = []
    if not x.artifact_id:
        failures.append("ARTIFACT_ID_MISSING")
    if not x.expected_project_root_id:
        failures.append("PROJECT_ROOT_MISSING")
    if not x.expected_parent_id:
        failures.append("EXPECTED_PARENT_MISSING")
    if x.expected_parent_id and x.expected_parent_id not in set(x.actual_parent_ids):
        failures.append("PARENT_MISMATCH")
    if not x.start_here_updated:
        failures.append("START_HERE_NOT_UPDATED")
    if x.start_here_updated and not x.start_here_readback_contains_artifact:
        failures.append("START_HERE_READBACK_MISSING")
    if not x.duplicate_or_legacy_conflict_resolved:
        failures.append("DUPLICATE_OR_LEGACY_CONFLICT")
    if x.cross_store_required and not x.cross_store_pointer_verified:
        failures.append("CROSS_STORE_POINTER_MISSING")

    if not x.artifact_id:
        state = "NOT_PERSISTED"
    elif failures:
        state = "PERSISTED_BUT_MISPLACED"
    else:
        state = "PLACEMENT_VERIFIED"

    return {
        "artifact_id": x.artifact_id,
        "state": state,
        "done_verified_allowed": state == "PLACEMENT_VERIFIED",
        "failures": failures,
        "receipt_required": True,
    }


def can_transition_to_done_verified(evaluation: Mapping) -> bool:
    return bool(
        evaluation.get("state") == "PLACEMENT_VERIFIED"
        and evaluation.get("done_verified_allowed") is True
        and not evaluation.get("failures")
    )
