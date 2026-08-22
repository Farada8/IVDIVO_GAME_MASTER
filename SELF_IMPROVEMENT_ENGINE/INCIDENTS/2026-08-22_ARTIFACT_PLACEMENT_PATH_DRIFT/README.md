# Artifact Placement Path Drift — Systemic Incident

Date: 2026-08-22
Issue: #356
Status: `BOUNDED_CANDIDATE / NO_AUTHORITY_PROMOTION`

## Failure class

`ARTIFACT_PLACEMENT_PATH_DRIFT`

A substantial artifact may physically exist while still being operationally missing because it is outside the canonical project workspace, absent from `00_START_HERE` / CURRENT index, or shadowed by a legacy/mislabeled artifact.

Core law:

`FILE_EXISTS != RESULT_IS_FINDABLE`

and therefore:

`PERSISTED != PLACEMENT_VERIFIED != DONE_VERIFIED`.

## Triggering real incident

D09 THE MAN WHO CAME BACK:
- I25 and I26 folders were successfully created but initially placed beside, not inside, the canonical `D09 — REBUILD v2.0 — STUDIO WORKSPACE`;
- an older document whose title claimed E01–E24 actually represented the early source ending at E06;
- user correctly reported that the expected files were not present in the project location.

This is not treated as a D09-only correction. It is a cross-dialog persistence/routing defect.

## Required pipeline

For every substantial artifact that is expected to persist in Drive/GitHub/project storage:

`CREATE/IMPORT`
→ `MOVE/PLACE INTO CANONICAL PROJECT LOCATION`
→ `READ BACK ACTUAL PARENT/PATH`
→ `UPDATE START_HERE/CURRENT INDEX`
→ `READ BACK INDEX`
→ `SCAN DUPLICATE/LEGACY TITLE CONFLICTS`
→ `VERIFY CROSS-STORE POINTER IF REQUIRED`
→ `PLACEMENT_VERIFIED`
→ only then `DONE_VERIFIED`.

## Fail-closed state

If the artifact exists but any placement/discoverability condition is not proven, state is:

`PERSISTED_BUT_MISPLACED`

This state MUST NOT be reported to the user as successfully saved in the correct project structure.

## Scope

Applies across dialogs and domains:
- books / audio / dramas;
- Business OS;
- Self-Improvement;
- research;
- project artifacts;
- GitHub/Drive mirrored packages.

## Authority boundary

This incident does not promote Self-Improvement v3 and does not replace v2 authority. It is an additive bounded persistence/routing candidate requiring regression and cross-project evidence before broader promotion.
