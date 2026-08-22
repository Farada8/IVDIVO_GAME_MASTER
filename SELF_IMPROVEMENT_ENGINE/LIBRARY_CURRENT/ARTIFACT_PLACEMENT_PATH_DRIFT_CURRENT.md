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
- PR #417 — mandatory production completion-path adoption, merge `7f9f7c58d9febba0ac9585a81e318e9718d7454b`;
- PR #441 — internal project-DONE completion-scope hardening, merge `74ae2afc2b897baa0a65bd0ea1fd0bc099922c5f`.

## Production completion-surface audit — merged
The current `personal-ai` completion/persistence surfaces were audited after PR #417. No additional external-artifact DONE bypass was found.

One semantic ambiguity was found in registered PL-08 behavior: `BookProductionCore FINAL` intentionally sets the parent project status to `DONE`. The registered route is preserved, but its meaning is now explicit and machine-readable:
- `completion_scope = INTERNAL_BOOK_PRODUCTION`;
- `external_artifact_completion = NOT_ASSERTED`.

Therefore PL-08 `FINAL -> project DONE` means only that the internal book-production state machine completed after its continuity authorization. It does not mean that a manuscript/export/package was externally persisted, placement-verified, published or distributed. Reaching FINAL cannot complete or override a separate artifact-required task.

PR #441 validation head `b7be25a459ad2a48a8de32ea31714fb445211b15` passed 14/14 triggered workflows, including artifact-placement-runtime #37 and PL-08 Book Production Core #42. Freshness comparison through main `cca976093a4b6678cd33bf6406a1cc8b258aaaa5` found no overlap with the seven PR paths before merge.

Audit artifact:
`PRODUCTION_COMPLETION_SURFACE_AUDIT_v1.md`.

Regression:
`personal-ai/tests/test_project_completion_scope.py`.

## External artifact completion rule
Artifact-producing tasks explicitly declare `requires_artifact_placement_receipt=true`. For marked tasks, direct completion is rejected and the placement gate controls DONE. Missing receipt => BLOCKED; non-verified receipt => BLOCKED + interception evidence; PLACEMENT_VERIFIED receipt => DONE subject to normal functional gates.

## Promotion boundary
Self-Improvement v2 remains CURRENT. The bounded mechanism status is:
`LIVE_INTERCEPTION_CAPTURE_ARMED_PRODUCTION_ADOPTED_SCOPE_HARDENED`.

Promotion remains:
`HOLD_ARMED_FOR_LIVE_EVIDENCE`.

Exactly one non-simulatable requirement remains:
`Observe future real traffic where the installed and production-adopted placement/resource-type guard catches a new real persistence failure before any false DONE claim, then independently confirm provider origin/readback.`

Tests, replays and synthetic fixtures cannot satisfy that final gate. Do not manufacture a failure.

Drive mirror authority:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
