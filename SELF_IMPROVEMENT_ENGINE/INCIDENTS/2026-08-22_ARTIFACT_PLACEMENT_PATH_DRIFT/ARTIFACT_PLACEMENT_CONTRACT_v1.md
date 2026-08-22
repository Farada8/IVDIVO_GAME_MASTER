# Artifact Placement Contract v1

## Truth conditions
1. `CREATE_SUCCESS != CORRECT_PLACEMENT`.
2. `FILE_ID_EXISTS != USER_CAN_FIND_RESULT`.
3. `CORRECT_PARENT != DISCOVERABLE` unless canonical `00_START_HERE` / CURRENT points to it.
4. `START_HERE_UPDATED != START_HERE_VERIFIED` until readback confirms the pointer.
5. A misleading legacy title is a routing defect even when the historical file is valid.
6. `DONE_VERIFIED` is forbidden until placement/discoverability are proven.

## Required ArtifactPlacementReceipt
- artifact_id
- artifact_title
- project_key
- expected_project_root_id
- expected_parent_id
- actual_parent_ids_readback
- start_here_id
- start_here_updated
- start_here_readback_contains_artifact
- duplicate_or_legacy_conflict_scan
- duplicate_or_legacy_conflict_resolved
- cross_store_required
- cross_store_pointer_verified
- placement_state
- timestamp
- source_dialog_or_run

## States
`NOT_PERSISTED`
`PERSISTED_BUT_MISPLACED`
`PLACEMENT_VERIFIED`
`DONE_VERIFIED`

## Canonical algorithm
1. Resolve canonical project root from CURRENT authority, not guessed titles.
2. Resolve intended child folder.
3. Create/import artifact.
4. Move/place artifact into intended child folder.
5. Read back provider metadata and verify expected parent.
6. Update project `00_START_HERE` / CURRENT index with artifact ID/URL/status/next action.
7. Read back the index and confirm pointer/state.
8. Scan same/similar titles and legacy artifacts.
9. Explicitly relabel historical misleading sources (`LEGACY`, `SUPERSEDED`, `ACTUAL ... ONLY`) rather than deleting provenance.
10. Verify Drive/GitHub cross-store pointer when mirroring is required.
11. Emit receipt. Any failed check => `PERSISTED_BUT_MISPLACED`.

## Cross-dialog law
A new dialog must not trust a prior sentence such as “saved to Drive.” Restore CURRENT authority and verify provider parent/path/index evidence before using the artifact.

## Negative controls
- Drive-root artifact while a project folder is expected => reject DONE_VERIFIED.
- sibling folder rather than project child => reject.
- START_HERE missing or unreadable => reject.
- misleading legacy title unresolved => reject.
- required mirror pointer missing => reject.
