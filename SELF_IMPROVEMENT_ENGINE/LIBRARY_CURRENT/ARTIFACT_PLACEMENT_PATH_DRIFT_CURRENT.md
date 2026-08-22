# CURRENT Pointer — Artifact Placement Path Drift Pilot

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains `VERIFIED_CURRENT`.

Bounded incident/runtime package:
`SELF_IMPROVEMENT_ENGINE/INCIDENTS/2026-08-22_ARTIFACT_PLACEMENT_PATH_DRIFT/`

Failure classes covered:
- `ARTIFACT_PLACEMENT_PATH_DRIFT`;
- `TOOL_ROUTE_MISMATCH / RESOURCE_TYPE_MISMATCH`.

Execution laws:
`FILE_EXISTS != RESULT_IS_FINDABLE`.
`RESOURCE_EXISTS != REQUEST_FULFILLED`.
`DONE_WITHOUT_DURABLE_RECEIPT = INVALID_STATE`.
`INTERCEPTION_CANDIDATE != REAL_PROVIDER_INTERCEPTION_PROOF`.
`GUARD_IMPLEMENTED != GUARD_ADOPTED_BY_PRODUCTION_COMPLETION_PATHS`.
`PROJECT_DONE != EXTERNAL_ARTIFACT_DONE`.

## Current merged authority
- PR #388 — base placement convergence;
- PR #401 — resource-type/tool-route hardening;
- PR #409 — atomic completion/restart recovery;
- PR #411 — durable live-interception evidence capture;
- PR #417 — mandatory production completion-path adoption, merge `7f9f7c58d9febba0ac9585a81e318e9718d7454b`.

## Production completion-surface audit candidate
A repository-wide audit of current `personal-ai` completion/persistence surfaces found no additional external-artifact DONE bypass after PR #417.

One semantic ambiguity remains in registered PL-08 behavior: `BookProductionCore FINAL` intentionally sets the parent project status to `DONE`. Existing tests make that state route authoritative, so it is not renamed.

The bounded candidate instead makes its meaning machine-readable:
- `completion_scope = INTERNAL_BOOK_PRODUCTION`;
- `external_artifact_completion = NOT_ASSERTED`.

Reaching PL-08 FINAL therefore never means that a manuscript/export/package was externally persisted, placement-verified, published or distributed, and it never completes a separate artifact-required task.

Current audit artifact:
`PRODUCTION_COMPLETION_SURFACE_AUDIT_v1.md`.

Candidate regression:
`personal-ai/tests/test_project_completion_scope.py`.

Current candidate status:
`PROJECT_DONE_SCOPE_HARDENING_PENDING_CI`.

## External artifact completion rule
Artifact-producing tasks explicitly declare `requires_artifact_placement_receipt=true`. For marked tasks, direct completion is rejected and the placement gate controls DONE. Missing receipt => BLOCKED; non-verified receipt => BLOCKED + interception evidence; PLACEMENT_VERIFIED receipt => DONE subject to normal gates.

## Promotion boundary
Self-Improvement v2 remains CURRENT. No broader promotion is claimed.

Before returning to `HOLD_ARMED_FOR_LIVE_EVIDENCE`, the bounded scope-hardening candidate must pass its own exact-head CI and merge without changing the registered PL-08 route.

After that, exactly one non-simulatable requirement remains: observe future real traffic where the installed and production-adopted placement/resource-type guard catches a new real persistence failure before any false DONE claim, then independently confirm provider origin/readback.

Tests, replays and synthetic fixtures cannot satisfy that final gate. Do not manufacture a failure.

Drive mirror authority:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
