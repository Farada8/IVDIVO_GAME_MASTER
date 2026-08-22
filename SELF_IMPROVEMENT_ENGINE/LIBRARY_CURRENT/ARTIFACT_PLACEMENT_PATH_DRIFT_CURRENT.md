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

Merged runtime authority on `main` before this candidate:
- #388 base placement convergence;
- #401 resource-type/tool-route hardening;
- #409 atomic completion/restart recovery;
- #411 durable live-interception evidence capture.

## Current adoption finding
Post-#411 audit found a MAJOR integration gap: both `BoundedAgentExecutor.run()` and canonical strict `execute()` directly called `ProjectStateManager.complete_task()`, and the CLI exposed no artifact-gated completion route. Therefore live evidence capture was implemented but not yet mandatory across canonical agent completion traffic.

Current candidate branch:
`self-improvement/artifact-gate-production-adoption-20260822`

Candidate changes:
- task field `requires_artifact_placement_receipt`;
- direct `complete_task()` refuses marked artifact tasks;
- compatibility Agent Executor routes marked FINISH through placement gate;
- strict Agent Executor routes marked FINISH through placement gate;
- missing receipt => BLOCKED, never DONE;
- failing receipt => BLOCKED + durable interception candidate;
- verified receipt => DONE;
- CLI `agent run --require-artifact-placement-receipt [--artifact-placement-receipt receipt.json]`;
- CLI `project complete-artifact <project> <task> <receipt.json>` for later provider-backed completion;
- placement CI now watches manager/agent/CLI call-sites and runs production-adoption + Agent Executor regressions.

Contract:
`PRODUCTION_ADOPTION_CONTRACT_v1.md`.

Promotion boundary:
Self-Improvement v2 remains CURRENT. Candidate status is `HOLD_ADOPTION_HARDENING` until exact-head CI and merge prove mandatory adoption. Only after that may the mechanism return to `HOLD_ARMED_FOR_LIVE_EVIDENCE`; the future real provider-confirmed interception remains required and cannot be simulated.

Issue #395 does not satisfy that final live gate because it triggered the resource-type repair. Tests/replays also cannot satisfy it.

Drive mirror authority remains:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
