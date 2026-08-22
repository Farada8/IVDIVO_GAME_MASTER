# Artifact Placement Contract v1

## Truth conditions
1. `CREATE_SUCCESS != CORRECT_PLACEMENT`.
2. `FILE_ID_EXISTS != USER_CAN_FIND_RESULT`.
3. `RESOURCE_EXISTS != RESOURCE_TYPE_MATCHES_WRITE_INTENT`.
4. `CORRECT_PARENT != DISCOVERABLE` unless canonical `00_START_HERE` / CURRENT points to it.
5. `START_HERE_UPDATED != START_HERE_VERIFIED` until readback confirms the pointer.
6. A misleading legacy title is a routing defect even when the historical file is valid.
7. `DONE_VERIFIED` is forbidden until placement/discoverability are proven.

## ArtifactPlacementReceipt fields
Runtime fields include:
- artifact_id
- project_root
- expected_parent
- actual_parent
- artifact_exists
- start_here_ref
- start_here_readback_ok
- start_here_mentions_artifact
- duplicate/legacy conflicts
- cross_store_required
- cross_store_pointer_present
- provider
- optional `expected_resource_type`
- provider-observed `observed_resource_type`

When `expected_resource_type` is declared, provider readback MUST yield a matching observed type. Missing observation => `resource_type_unobserved`; mismatch => `resource_type_mismatch`. Either failure keeps the state `PERSISTED_BUT_MISPLACED` and forbids DONE.

Current normalized resource types:
- Google Drive native folder -> `FOLDER`
- Google Drive native Doc -> `DOCUMENT`
- Google Drive native Sheet -> `SPREADSHEET`
- Google Drive native Slides -> `PRESENTATION`
- other Drive file -> `FILE`
- observed GitHub repository file -> `FILE`

Receipts that predate this extension and do not declare an expected type preserve existing semantics. Backward compatibility is intentional; type validation becomes mandatory when the write intent knows the expected resource type.

## States
`NOT_PERSISTED`
`PERSISTED_BUT_MISPLACED`
`PLACEMENT_VERIFIED`
`DONE_VERIFIED`

## Canonical algorithm
1. Resolve canonical project root from CURRENT authority, not guessed titles.
2. Resolve intended child folder.
3. Resolve expected provider resource type when the operation knows it.
4. Create/import artifact.
5. Read back provider metadata.
6. Verify artifact existence, expected parent/path, and expected resource type when declared.
7. Update project `00_START_HERE` / CURRENT index with artifact ID/URL/status/next action.
8. Read back the index and confirm pointer/state.
9. Scan same/similar titles and legacy artifacts.
10. Explicitly relabel historical misleading sources (`LEGACY`, `SUPERSEDED`, `ACTUAL ... ONLY`) rather than deleting provenance.
11. Verify Drive/GitHub cross-store pointer when mirroring is required.
12. Emit receipt. Any failed check => `PERSISTED_BUT_MISPLACED`.

## Cross-dialog law
A new dialog must not trust a prior sentence such as “saved to Drive.” Restore CURRENT authority and verify provider resource type + parent/path/index evidence before using the artifact when type is known.

## Negative controls
- expected DOCUMENT but provider returns FOLDER => reject DONE_VERIFIED.
- expected type declared but provider metadata omits type => reject.
- Drive-root artifact while a project folder is expected => reject.
- sibling folder rather than project child => reject.
- START_HERE missing or unreadable => reject.
- misleading legacy title unresolved => reject.
- required mirror pointer missing => reject.
