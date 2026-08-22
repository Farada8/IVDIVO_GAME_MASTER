from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping, Sequence

from core.artifact_placement import ArtifactPlacementReceipt


@dataclass(frozen=True)
class PlacementIntent:
    project_root: str
    expected_parent: str
    start_here_ref: str
    cross_store_required: bool = False


def _single_parent(parents: Sequence[str] | None) -> str | None:
    if not parents:
        return None
    normalized = [str(x).strip() for x in parents if str(x).strip()]
    if len(normalized) != 1:
        return None
    return normalized[0]


def _drive_locator(value: str | None) -> str | None:
    if value is None:
        return None
    value = str(value).strip()
    if not value:
        return None
    return value if value.startswith("drive:") else f"drive:{value}"


def receipt_from_drive_observation(
    *,
    intent: PlacementIntent,
    artifact_metadata: Mapping[str, Any],
    start_here_readback_ok: bool,
    start_here_mentions_artifact: bool,
    legacy_conflicts: Sequence[str] = (),
    cross_store_pointer_present: bool = False,
) -> ArtifactPlacementReceipt:
    """Compile provider-observed Google Drive metadata into the common receipt.

    Drive connector/API observations normally return raw file IDs in `id` and
    `parent_ids`/`parents`. This adapter normalizes them to `drive:<id>` locators
    before comparing with the canonical PlacementIntent. Multiple parents fail
    closed by producing `actual_parent=None`.
    """
    artifact_raw_id = str(artifact_metadata.get("id", "")).strip()
    parents = artifact_metadata.get("parent_ids")
    if parents is None:
        parents = artifact_metadata.get("parents")
    raw_parent = _single_parent(parents if isinstance(parents, (list, tuple)) else None)
    return ArtifactPlacementReceipt(
        artifact_id=_drive_locator(artifact_raw_id) or "",
        provider="GOOGLE_DRIVE",
        project_root=intent.project_root,
        expected_parent=intent.expected_parent,
        actual_parent=_drive_locator(raw_parent),
        artifact_exists=bool(artifact_raw_id),
        start_here_ref=intent.start_here_ref,
        start_here_readback_ok=start_here_readback_ok,
        start_here_mentions_artifact=start_here_mentions_artifact,
        legacy_conflicts=tuple(str(x) for x in legacy_conflicts if str(x).strip()),
        cross_store_required=intent.cross_store_required,
        cross_store_pointer_present=cross_store_pointer_present,
    )


def receipt_from_github_observation(
    *,
    intent: PlacementIntent,
    repository_full_name: str,
    path: str,
    file_observed: bool,
    current_index_readback_ok: bool,
    current_index_mentions_artifact: bool,
    legacy_conflicts: Sequence[str] = (),
    cross_store_pointer_present: bool = False,
) -> ArtifactPlacementReceipt:
    """Compile a GitHub file/path observation into the common receipt.

    GitHub uses repository paths rather than Drive parents. The parent is the
    dirname of the provider-observed path; expected_parent should use the same
    `github:owner/repo:path/to/dir` convention.
    """
    repo = repository_full_name.strip()
    clean_path = path.strip().strip("/")
    artifact_id = f"github:{repo}:{clean_path}" if repo and clean_path and file_observed else ""
    parent_path = clean_path.rsplit("/", 1)[0] if "/" in clean_path else ""
    actual_parent = f"github:{repo}:{parent_path}" if repo and file_observed else None
    return ArtifactPlacementReceipt(
        artifact_id=artifact_id,
        provider="GITHUB",
        project_root=intent.project_root,
        expected_parent=intent.expected_parent,
        actual_parent=actual_parent,
        artifact_exists=bool(artifact_id),
        start_here_ref=intent.start_here_ref,
        start_here_readback_ok=current_index_readback_ok,
        start_here_mentions_artifact=current_index_mentions_artifact,
        legacy_conflicts=tuple(str(x) for x in legacy_conflicts if str(x).strip()),
        cross_store_required=intent.cross_store_required,
        cross_store_pointer_present=cross_store_pointer_present,
    )
