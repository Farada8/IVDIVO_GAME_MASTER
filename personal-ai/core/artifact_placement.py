from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping

NOT_PERSISTED = "NOT_PERSISTED"
PERSISTED_BUT_MISPLACED = "PERSISTED_BUT_MISPLACED"
PLACEMENT_VERIFIED = "PLACEMENT_VERIFIED"


@dataclass(frozen=True)
class ArtifactPlacementReceipt:
    artifact_id: str
    project_root: str
    expected_parent: str
    actual_parent: str | None
    artifact_exists: bool
    start_here_ref: str | None
    start_here_readback_ok: bool
    start_here_mentions_artifact: bool
    legacy_conflicts: tuple[str, ...] = ()
    cross_store_required: bool = False
    cross_store_pointer_present: bool = False
    provider: str = "UNKNOWN"

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ArtifactPlacementReceipt":
        legacy = value.get("legacy_conflicts", ())
        if legacy is None:
            legacy = ()
        if not isinstance(legacy, (list, tuple)):
            raise TypeError("legacy_conflicts must be a list/tuple")
        return cls(
            artifact_id=str(value.get("artifact_id", "")).strip(),
            project_root=str(value.get("project_root", "")).strip(),
            expected_parent=str(value.get("expected_parent", "")).strip(),
            actual_parent=None if value.get("actual_parent") is None else str(value.get("actual_parent")).strip(),
            artifact_exists=bool(value.get("artifact_exists", False)),
            start_here_ref=None if value.get("start_here_ref") is None else str(value.get("start_here_ref")).strip(),
            start_here_readback_ok=bool(value.get("start_here_readback_ok", False)),
            start_here_mentions_artifact=bool(value.get("start_here_mentions_artifact", False)),
            legacy_conflicts=tuple(str(item).strip() for item in legacy if str(item).strip()),
            cross_store_required=bool(value.get("cross_store_required", False)),
            cross_store_pointer_present=bool(value.get("cross_store_pointer_present", False)),
            provider=str(value.get("provider", "UNKNOWN")).strip() or "UNKNOWN",
        )

    def failures(self) -> list[str]:
        failures: list[str] = []
        if not self.artifact_exists or not self.artifact_id:
            failures.append("artifact_not_persisted")
            return failures
        if not self.project_root:
            failures.append("project_root_unresolved")
        if not self.expected_parent:
            failures.append("expected_parent_unresolved")
        if self.actual_parent != self.expected_parent:
            failures.append("parent_mismatch")
        if not self.start_here_ref:
            failures.append("start_here_missing")
        if not self.start_here_readback_ok:
            failures.append("start_here_readback_failed")
        if not self.start_here_mentions_artifact:
            failures.append("artifact_missing_from_start_here")
        if self.legacy_conflicts:
            failures.append("legacy_or_duplicate_conflict")
        if self.cross_store_required and not self.cross_store_pointer_present:
            failures.append("cross_store_pointer_missing")
        return failures

    @property
    def status(self) -> str:
        failures = self.failures()
        if "artifact_not_persisted" in failures:
            return NOT_PERSISTED
        if failures:
            return PERSISTED_BUT_MISPLACED
        return PLACEMENT_VERIFIED

    @property
    def placement_verified(self) -> bool:
        return self.status == PLACEMENT_VERIFIED

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["legacy_conflicts"] = list(self.legacy_conflicts)
        data["status"] = self.status
        data["failures"] = self.failures()
        return data


def require_placement_verified(receipt: ArtifactPlacementReceipt | Mapping[str, Any]) -> ArtifactPlacementReceipt:
    if not isinstance(receipt, ArtifactPlacementReceipt):
        receipt = ArtifactPlacementReceipt.from_mapping(receipt)
    if not receipt.placement_verified:
        reasons = ", ".join(receipt.failures()) or receipt.status
        raise RuntimeError(f"artifact placement is not verified: {reasons}")
    return receipt
