# Atomic Artifact Completion + Recovery Contract v1

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains VERIFIED_CURRENT.

## Problem
`complete_task_with_artifact_gate()` previously persisted task status and `artifact_placement_receipt` in two separate writes. A process interruption after the status write but before the receipt write could leave a durable `DONE` task without the evidence that authorized DONE.

Core law:
`DONE_WITHOUT_DURABLE_RECEIPT = INVALID_STATE`.

## Atomic persistence invariant
For artifact-gated tasks, these fields form one persistence unit and MUST be committed through one atomic temporary-file replace:
- `status`;
- `block_reason`;
- `completion_gate`;
- `artifact_placement_receipt` when present;
- `updated_at`.

The runtime MUST NOT first persist DONE/BLOCKED and then attach the receipt in a second write.

## Recovery invariant
After constructing a new `ProjectStateManager` against the same persisted home and reopening the project:
- missing receipt remains BLOCKED;
- `PERSISTED_BUT_MISPLACED` remains BLOCKED with its failure reasons intact;
- resource-type mismatch remains BLOCKED with expected/observed resource type intact;
- `PLACEMENT_VERIFIED` DONE remains DONE with the receipt intact.

## Real failure evidence boundary
Issue #395 recorded a real Drive failure after the original placement runtime merge: document persistence intent created 18 provider objects of type FOLDER. The incorrect objects were not accepted as successful document persistence; a valid Google Doc had to be created and read back separately. PR #401 merged the resource-type guard and negative canary.

This proves the failure class is real and that provider type readback is necessary. It does NOT satisfy the separate prospective promotion gate, because #395 triggered the resource-type repair. The canonical PR401 receipt still requires observing future real traffic where the installed guard catches the next persistence/resource-type failure before a false DONE claim.

## Promotion boundary
This atomic persistence/reopen repair may satisfy only the persistence/recovery regression requirement after exact-head CI passes against the current ProjectState and Personal AI compatibility contracts. Self-Improvement promotion remains HOLD until a future real failure is intercepted prospectively by the installed guard.
