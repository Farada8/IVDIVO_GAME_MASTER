# CURRENT Pointer — Artifact Placement Path Drift Pilot

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains `VERIFIED_CURRENT`.

Bounded incident/runtime package:
`SELF_IMPROVEMENT_ENGINE/INCIDENTS/2026-08-22_ARTIFACT_PLACEMENT_PATH_DRIFT/`

Failure class: `ARTIFACT_PLACEMENT_PATH_DRIFT`
Fail-closed state: `PERSISTED_BUT_MISPLACED`

Execution law:
`FILE_EXISTS != RESULT_IS_FINDABLE`.
A substantial external artifact may not transition toward verified completion until canonical placement, provider parent/path readback, project START_HERE/CURRENT update and readback, legacy/duplicate-title scan, and required cross-store pointer checks have passed.

Runtime now present on `main`:
- `personal-ai/core/artifact_placement.py`
- `personal-ai/core/artifact_placement_adapters.py`
- `personal-ai/projects/artifact_completion.py`
- `.github/workflows/artifact-placement-runtime.yml`

Merge authority:
- merged PR #388;
- merge commit `b8265fe897a29147844591919fa4853aa3ba5a2c`;
- 11/11 related workflow runs passed before merge;
- provider adapters for Google Drive and GitHub are implemented with fail-closed regression coverage;
- two real cross-project placement canaries = 2/2 `PLACEMENT_VERIFIED`;
- Drive mirror: `06_SELF_IMPROVEMENT/INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.

Promotion boundary:
Self-Improvement v2 remains CURRENT. Do not infer broader promotion from the merge. Remaining gates are:
1. prospectively catch at least one new real placement failure before any false completion claim;
2. pass regression against future current persistence/recovery contracts.

Older PRs #362, #372, #377 and replacement attempt #389 are provenance-only after #388 and must not be treated as current implementation authority.
