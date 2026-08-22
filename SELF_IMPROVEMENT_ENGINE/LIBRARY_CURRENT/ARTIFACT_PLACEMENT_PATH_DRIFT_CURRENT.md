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

Runtime candidate:
- `personal-ai/core/artifact_placement.py`
- `personal-ai/projects/artifact_completion.py`
- `.github/workflows/artifact-placement-runtime.yml`

Evidence:
- GitHub issue #356;
- exact-head CI run 32561883676 = PASS;
- two real cross-project placement canaries = 2/2 PLACEMENT_VERIFIED;
- Drive mirror: `06_SELF_IMPROVEMENT/INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.

Do not infer Self-Improvement promotion from this pointer. Provider-adapter integration and a prospective newly-caught real placement failure remain required before broader promotion.
