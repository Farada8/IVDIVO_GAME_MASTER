# CURRENT Pointer — Artifact Placement Path Drift Pilot

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains `VERIFIED_CURRENT`.

Bounded incident/runtime package:
`SELF_IMPROVEMENT_ENGINE/INCIDENTS/2026-08-22_ARTIFACT_PLACEMENT_PATH_DRIFT/`

Failure classes covered:
- `ARTIFACT_PLACEMENT_PATH_DRIFT`;
- `TOOL_ROUTE_MISMATCH / RESOURCE_TYPE_MISMATCH`.

Fail-closed state: `PERSISTED_BUT_MISPLACED`.

Execution laws:
`FILE_EXISTS != RESULT_IS_FINDABLE`.
`RESOURCE_EXISTS != REQUEST_FULFILLED`.
`DONE_WITHOUT_DURABLE_RECEIPT = INVALID_STATE`.
`INTERCEPTION_CANDIDATE != REAL_PROVIDER_INTERCEPTION_PROOF`.
`GUARD_IMPLEMENTED != GUARD_ADOPTED_BY_PRODUCTION_COMPLETION_PATHS`.

## Current merged authority
- PR #388 — base placement convergence;
- PR #401 — resource-type/tool-route hardening;
- PR #409 — atomic completion/restart recovery;
- PR #411 — durable live-interception evidence capture;
- PR #417 — mandatory production completion-path adoption, merge `7f9f7c58d9febba0ac9585a81e318e9718d7454b`.

PR #417 was reconciled against fresh main before merge. Reconciled head `5cd4c1493069b5da26e6df169e67a810a83f88cd` passed 14/14 triggered workflows, including artifact-placement-runtime #30, PL-05 Agent Executor, PL-01 Project State, PL-03 Source Evidence and PL-13 File Ingestion. Freshness check after reconciliation found no overlap with subsequent main changes.

## Production adoption now verified
Artifact-producing tasks explicitly declare:
`requires_artifact_placement_receipt = true`.

For marked tasks:
- direct `ProjectStateManager.complete_task()` refuses DONE;
- compatibility `BoundedAgentExecutor.run()` routes FINISH through the artifact placement gate;
- canonical strict `BoundedAgentExecutor.execute()` routes FINISH through the artifact placement gate;
- missing receipt => BLOCKED, never DONE;
- non-verified receipt => BLOCKED + durable append-only interception candidate;
- PLACEMENT_VERIFIED receipt => DONE subject to normal functional gates;
- CLI supports `agent run --require-artifact-placement-receipt` and later provider-backed `project complete-artifact <project> <task> <receipt.json>`;
- PL-13 `ingest file` and PL-03 evidence functionality were preserved during run.py reconciliation.

Internal model/agent output existence does not authorize external artifact DONE. Placement receipts are provider-backed evidence and cannot be self-certified by an agent.

Contract:
`PRODUCTION_ADOPTION_CONTRACT_v1.md`.

## Promotion boundary
Self-Improvement v2 remains CURRENT. The bounded mechanism status is now:
`HOLD_ARMED_FOR_LIVE_EVIDENCE`.

Exactly one non-simulatable requirement remains:
`Observe future real traffic where the already-installed and production-adopted placement/resource-type guard catches a new real persistence failure before any false DONE claim, then independently confirm provider origin/readback.`

Issue #395 does not satisfy this final gate because it triggered the resource-type repair. Tests, replays and synthetic fixtures cannot satisfy it. Do not manufacture a failure.

Drive mirror authority:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
