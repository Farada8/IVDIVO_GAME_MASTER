# Artifact Placement Path Drift — Systemic Incident

Date: 2026-08-22
Issue: #356
Status: `BOUNDED_CANDIDATE / NO_AUTHORITY_PROMOTION`

## Failure class
`ARTIFACT_PLACEMENT_PATH_DRIFT`

A substantial artifact may physically exist while still being operationally missing because it is outside the canonical project workspace, absent from `00_START_HERE` / CURRENT index, or shadowed by a legacy/mislabeled artifact.

Core law:
`FILE_EXISTS != RESULT_IS_FINDABLE`
`PERSISTED != PLACEMENT_VERIFIED != DONE_VERIFIED`.

## Triggering real incident
D09 THE MAN WHO CAME BACK:
- I25 and I26 folders were successfully created but initially placed beside, not inside, the canonical `D09 — REBUILD v2.0 — STUDIO WORKSPACE`;
- an older document whose title claimed E01–E24 actually represented the early source ending at E06;
- user correctly reported that the expected files were not present in the project location.

This is a cross-dialog persistence/routing defect, not a D09-only correction.

## Required pipeline
`CREATE/IMPORT -> CANONICAL PROJECT PLACEMENT -> PARENT/PATH READBACK -> START_HERE/CURRENT UPDATE -> INDEX READBACK -> DUPLICATE/LEGACY SCAN -> CROSS-STORE POINTER IF REQUIRED -> PLACEMENT_VERIFIED -> DONE_VERIFIED only after all other gates`.

If any placement/discoverability condition is unproven, state is `PERSISTED_BUT_MISPLACED` and the workflow must not claim correct persistence.

## Scope
Books, audio, dramas, business, Self-Improvement, research, project artifacts, and GitHub/Drive mirrored packages across dialogs.

## Authority boundary
Self-Improvement v2 remains CURRENT. This is a bounded candidate requiring prospective cross-project evidence before promotion.
