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
`LOCAL_RUNTIME_GUARD != CHATGPT_PLATFORM_MIDDLEWARE`.

## Current merged local-runtime authority
- PR #388 — base placement convergence;
- PR #401 — resource-type/tool-route hardening;
- PR #409 — atomic completion/restart recovery;
- PR #411 — durable local-runtime interception capture;
- PR #417 — mandatory Personal AI production completion-path adoption;
- PR #441 — internal project-DONE completion-scope hardening.

The local Personal AI surface is enforced. Artifact-required tasks cannot reach DONE without placement evidence, and internal PL-08 project DONE is explicitly non-external.

## Deployment-boundary candidate — Issue #444
A new audit found that the laptop-first `personal-ai` runtime is not middleware for Google Drive/GitHub connector actions executed by ChatGPT/platform tooling in other dialogs. Therefore the prior system-wide wording `installed guard catches the next failure` is too broad when applied to CHAT_CONNECTOR writes.

The candidate splits enforcement into two surfaces:

### LOCAL_RUNTIME_ENFORCEMENT
Status: `MERGED_ENFORCED`.
Mode: executable task/agent/CLI guard inside Personal AI.

### CHAT_CONNECTOR_ENFORCEMENT
Status: `OPERATIONAL_PROTOCOL_CANDIDATE`.
Platform middleware installed: `false`.
Mode: `SYNCHRONOUS_OPERATIONAL_READBACK_GATE`.

Required Chat Connector sequence:
`WRITE -> PROVIDER READBACK -> CANONICAL INDEX/CURRENT READBACK -> CONNECTOR PLACEMENT CAPTURE -> COMPLETION CLAIM`.

New candidate components:
- `personal-ai/core/connector_placement_capture.py`;
- `personal-ai/tests/test_connector_placement_capture.py`;
- `CHAT_CONNECTOR_DEPLOYMENT_BOUNDARY_v1.md`;
- `CHAT_CONNECTOR_LIVE_INTERCEPTION_LEDGER_v1.json`.

The classifier never calls provider APIs and never claims automatic interception. It classifies evidence already obtained by synchronous connector readback. Every capture has `promotion_proof=false` and requires independent review.

A failing capture can become only `ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW` when it has real provider-readback origin, a provider readback reference, was captured before any completion claim, and no false claim was emitted. TEST_FIXTURE, REPLAY, UNKNOWN-origin and post-claim incidents cannot qualify.

Current live ledger count: `0`.

Current candidate status:
`CHAT_CONNECTOR_DEPLOYMENT_HARDENING_PENDING_CI`.

Promotion status:
`HOLD_DEPLOYMENT_BOUNDARY_PENDING_CI`.

After this bounded layer passes exact-head CI and merges, the remaining real gate must be scoped specifically to the original cross-dialog surface:
`Observe a future real CHAT_CONNECTOR provider-backed placement/resource-type failure; detect it by synchronous provider/index readback before any false completion claim; persist it in the live ledger; then independently confirm provider origin/readback.`

Tests, replays and synthetic fixtures cannot satisfy that gate. Do not manufacture a failure.

Drive mirror authority remains:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
