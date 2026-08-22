# Artifact Placement Contract v1

## Truth conditions

1. `CREATE_SUCCESS != CORRECT_PLACEMENT`.
2. `FILE_ID_EXISTS != USER_CAN_FIND_RESULT`.
3. `CORRECT_PARENT != DISCOVERABLE` unless the canonical project index points to the artifact.
4. `START_HERE_UPDATED != START_HERE_VERIFIED` until readback confirms the pointer/state.
5. A misleading legacy title is a routing defect even when the underlying historical file is valid.
6. `DONE_VERIFIED` is forbidden until placement and discoverability are proven.

## Mandatory receipt fields

Every substantial persisted artifact must produce an `ArtifactPlacementReceipt` containing:

- `artifact_id`
- `artifact_title`
- `project_id` / project key
- `expected_project_root_id`
- `expected_parent_id`
- `actual_parent_ids_readback`
- `start_here_id`
- `start_here_updated`
- `start_here_readback_contains_artifact`
- `duplicate_or_legacy_conflict_scan`
- `duplicate_or_legacy_conflict_resolved`
- `cross_store_required`
- `cross_store_pointer_verified`
- `placement_state`
- `timestamp`
- `source_dialog_or_run` when available

## States

- `NOT_PERSISTED`
- `PERSISTED_BUT_MISPLACED`
- `PLACEMENT_VERIFIED`
- `DONE_VERIFIED`

The guard may emit `PLACEMENT_VERIFIED`; the calling workflow may transition to `DONE_VERIFIED` only if its other functional/evidence gates also pass.

## Canonical algorithm

1. Resolve the canonical project root from CURRENT authority, never from a guessed title.
2. Resolve or create the intended child folder.
3. Create/import the artifact.
4. Move the artifact/folder into the intended child folder when the provider created it elsewhere.
5. Read back provider metadata and verify `expected_parent_id ∈ actual_parent_ids`.
6. Update project `00_START_HERE` / CURRENT index with artifact name, ID/URL, status and next action.
7. Read back START_HERE and confirm the artifact pointer and state are present.
8. Scan the canonical project tree for misleading same/similar titles and legacy files.
9. Rename/label historical sources explicitly (`LEGACY`, `SUPERSEDED`, `ACTUAL ... ONLY`) instead of deleting provenance.
10. If GitHub/Drive mirroring is required, verify the cross-store pointer or manifest.
11. Emit receipt. If any check fails, set `PERSISTED_BUT_MISPLACED` and do not claim successful project persistence.

## Cross-dialog law

A new dialog must not trust a prior assistant sentence such as “saved to Drive.” It must restore from CURRENT authority and verify the provider parent/path/index receipt before relying on the artifact.

## Negative controls

The system must reject `DONE_VERIFIED` for at least:

- artifact in Drive root while expected parent is a project folder;
- artifact beside project root rather than inside it;
- START_HERE not updated;
- START_HERE updated but readback does not contain artifact;
- legacy file with a stronger/misleading title not explicitly marked;
- required Drive/GitHub mirror missing.
