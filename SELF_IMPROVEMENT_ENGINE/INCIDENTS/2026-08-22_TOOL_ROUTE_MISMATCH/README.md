# Tool Route / Resource Type Mismatch — Real Incident

Date: 2026-08-22
GitHub issue: #395
Status: `BOUNDED_REPAIR_CANDIDATE / NO_AUTHORITY_PROMOTION`

## Failure class
`TOOL_ROUTE_MISMATCH / RESOURCE_TYPE_MISMATCH`

A persistence operation can create a real provider object of the wrong type. Existence and even parent placement therefore do not prove that the requested artifact was created.

Core law:
`WRITE_INTENT != PROVIDER_RESOURCE_TYPE`
`RESOURCE_EXISTS != REQUEST_FULFILLED`

## Real observed incident
During Cycle10 post-merge Drive closure, write operations intended to create/persist documents produced a sequence of Google Drive folders instead. Provider readback of the archived subtree `__EMPTY_TOOL_ROUTE_MISMATCH_ARCHIVE_DO_NOT_USE` (Drive folder ID `1Z8bJ1ilv09uA1CHzLcJGFrKyNx3K51xp`) shows 18 children named `00_RECEIPTS` through `18_READBACK_OK`, all with MIME type `application/vnd.google-apps.folder`.

The valid post-merge receipt had to be created later as a native Google Doc and read back separately. Therefore the incorrect folder objects are not treated as successful document persistence.

## Root cause class
Provider/tool route selection allowed the operation shape to drift from expected artifact type. The existing placement runtime verified existence, parent/index/discoverability, but had no explicit expected-vs-observed resource-type invariant.

## Bounded repair
Extend `ArtifactPlacementReceipt` / `PlacementIntent` with optional expected and observed resource types.

When expected type is declared:
- no observed type -> `resource_type_unobserved` -> `PERSISTED_BUT_MISPLACED`;
- observed type differs -> `resource_type_mismatch` -> `PERSISTED_BUT_MISPLACED`;
- task completion remains BLOCKED.

Google Drive MIME observations normalize to DOCUMENT / SPREADSHEET / PRESENTATION / FOLDER / FILE. GitHub observed repository artifacts normalize to FILE.

Backward compatibility: receipts without an expected type preserve the pre-existing placement contract.

## Evidence boundary
This incident proves a persistence-integrity failure class and a concrete negative control. It does not prove content correctness, provider reliability rate, Human Signal, market evidence or global Self-Improvement promotion.

## Promotion law
No new SI ID. Self-Improvement v2 remains current. This repair must pass current artifact-placement + Personal AI regressions and survive future real traffic before any broader promotion claim.
