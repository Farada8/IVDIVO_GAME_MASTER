# Chat Connector Deployment Boundary v1

Date: 2026-08-22
Parent incident: #356
Deployment-boundary issue: #444
Authority effect: NONE until exact-head CI + merge.
Self-Improvement v2 remains VERIFIED_CURRENT.

## Problem

The Artifact Placement runtime is executable and production-adopted inside the laptop-first `personal-ai` process. ChatGPT platform connector calls to Google Drive/GitHub do not execute inside that Python process. Therefore:

`LOCAL_RUNTIME_GUARD != CHATGPT_PLATFORM_MIDDLEWARE`.

A local task interceptor cannot honestly be described as automatically intercepting every Drive/GitHub write made in other ChatGPT dialogs.

## Two execution surfaces

### 1. LOCAL_RUNTIME_ENFORCEMENT

Surface: `personal-ai` task/agent/CLI runtime.

Enforcement: executable/automatic when the work is routed through that runtime.

Relevant merged controls:
- artifact-required task policy;
- provider-normalized placement receipts;
- atomic status + receipt persistence;
- durable interception candidates;
- compatibility + strict Agent Executor adoption;
- CLI delayed artifact completion;
- internal project-DONE scope separation.

### 2. CHAT_CONNECTOR_ENFORCEMENT

Surface: Google Drive/GitHub connector actions executed by ChatGPT/platform tooling outside the local Python runtime.

Current enforcement mode:
`SYNCHRONOUS_OPERATIONAL_READBACK_GATE`.

It is **not** platform middleware and must never be described as one.

Required sequence for a substantial connector artifact:

`WRITE -> PROVIDER READBACK -> CANONICAL INDEX/CURRENT READBACK -> CONNECTOR PLACEMENT CAPTURE -> COMPLETION CLAIM`

If provider/index readback does not verify the requested placement/resource type:
- do not emit a completion claim;
- classify the capture;
- persist it in `CHAT_CONNECTOR_LIVE_INTERCEPTION_LEDGER_v1.json` using a concurrency-safe update;
- if it is real provider evidence captured before any completion claim, it may be marked `ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW`;
- eligibility is not promotion proof.

## Executable classifier

`personal-ai/core/connector_placement_capture.py`

It reuses provider-normalized Artifact Placement receipts but does not call external APIs and does not intercept ChatGPT tools. It classifies evidence already obtained from connector/provider readback.

Evidence origins:
- `REAL_PROVIDER_READBACK`
- `TEST_FIXTURE`
- `REPLAY`
- `UNKNOWN`

Review statuses:
- `ELIGIBLE_FOR_INDEPENDENT_LIVE_REVIEW`
- `VERIFIED_PLACEMENT_OBSERVATION`
- `TEST_ONLY_NOT_LIVE_EVIDENCE`
- `POST_CLAIM_INCIDENT_NOT_PROSPECTIVE`
- `UNVERIFIED_ORIGIN`

Invariant:
`promotion_proof = false` for every runtime capture.

Only a later independent authority pass may determine whether a real eligible event satisfies the remaining promotion gate.

## Live-event eligibility

A failing connector capture is eligible for independent live review only when all are true:
1. execution surface is CHAT_CONNECTOR;
2. evidence origin is REAL_PROVIDER_READBACK;
3. provider_readback_ref is present;
4. receipt is NOT_PERSISTED or PERSISTED_BUT_MISPLACED;
5. capture occurred before a completion claim;
6. no completion claim had been emitted;
7. event is durably persisted with provider/readback details.

Tests, synthetic fixtures, replay of issue #395, remembered chat text without provider evidence, and post-claim incident discovery do not qualify.

## Promotion boundary

The original systemic incident is cross-dialog and provider-facing. Therefore the remaining real-evidence gate must be evaluated on the CHAT_CONNECTOR surface, not inferred from local deterministic tests.

Correct remaining gate after this boundary is merged:

`Observe a future real CHAT_CONNECTOR provider-backed placement/resource-type failure; detect it via synchronous provider/index readback before any false completion claim; persist the capture in the live ledger; then independently confirm provider origin/readback.`

Do not manufacture a failure.
