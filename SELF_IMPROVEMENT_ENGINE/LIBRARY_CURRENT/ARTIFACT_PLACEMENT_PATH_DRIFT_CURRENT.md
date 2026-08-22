# CURRENT Pointer — Artifact Placement Path Drift Pilot

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains `VERIFIED_CURRENT`.

Bounded incident package:
`SELF_IMPROVEMENT_ENGINE/INCIDENTS/2026-08-22_ARTIFACT_PLACEMENT_PATH_DRIFT/`

Failure class:
`ARTIFACT_PLACEMENT_PATH_DRIFT`

Fail-closed state:
`PERSISTED_BUT_MISPLACED`

Execution law:
`FILE_EXISTS != RESULT_IS_FINDABLE`.
A substantial artifact may not transition toward `DONE_VERIFIED` until canonical placement, provider parent/path readback, project START_HERE/CURRENT update and readback, legacy/duplicate-title scan, and required cross-store pointer checks have passed.

GitHub issue: #356.
Drive mirror: `06_SELF_IMPROVEMENT/INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.

Do not infer promotion from recency. This remains a bounded pilot until prospective cross-project evidence and regression gates pass.
