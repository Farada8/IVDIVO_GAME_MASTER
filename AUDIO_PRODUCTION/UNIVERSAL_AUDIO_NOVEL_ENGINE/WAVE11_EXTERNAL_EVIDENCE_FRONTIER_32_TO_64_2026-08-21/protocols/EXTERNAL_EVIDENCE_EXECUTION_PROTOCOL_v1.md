# EXTERNAL EVIDENCE EXECUTION PROTOCOL v1

## Objective
Advance Audio Novel Engine work until the first unavailable external evidence boundary, then persist a precise causal HOLD rather than substitute synthetic evidence.

## Procedure
1. Re-read latest GitHub `main`, relevant merged Audio authority, open overlapping PRs, and Drive current state.
2. Dedupe the requested work against current modules and previous prompt cycles.
3. Load the dependency frontier for the active prompt range.
4. Attempt only READY work.
5. For an external action, require its canonical evidence class and acquisition path before downstream execution.
6. When evidence is absent, record `HOLD_EXTERNAL_*` at that prompt and `BLOCKED_*` for descendants with exact dependencies.
7. Internal engineering may continue only when it does not pretend the blocked external event occurred.
8. Before paid work, require explicit human pre-spend GO, immutable request identity, current provider revalidation, idempotency and quarantine.
9. After any real provider result, persist durable request/result/spend/raw lineage before the next paid request.
10. Human review may enter authority only via trusted attestation bound to actual artifact/candidate/task hashes.
11. Feed only observed defects/repairs/retests into Self-Improvement; no single engineering cycle can auto-promote a universal rule.
12. Persist GitHub + Drive state, read it back, re-check fresh main, and resume the highest unblocked obligation.

## Evidence classes
- AUTH_PROVIDER
- HUMAN_REVIEW
- LIVE_AUDIO
- REAL_ALIGNMENT
- MEASURED_ECONOMICS
- DURABLE_RAW_ASSET
- DURABLE_RECOVERY
- CROSS_PROJECT_LIVE

## Forbidden shortcuts
- caller boolean as external truth;
- public provider docs as account inventory;
- remembered voice/model ID as current capability;
- synthetic/model review as human evidence;
- provider acceptance as take acceptance;
- CI success as production readiness;
- downstream execution past missing upstream proof;
- automatic paid replay after ambiguous outcome;
- force-merging stale branches over newer trust state.

## Completion semantics
`PASS_ENGINEERING` proves a deterministic internal mechanism.
`HOLD_EXTERNAL` proves only that the real external precondition has not been durably observed in the current evidence set.
`BLOCKED_DEPENDENCY` is a completed causal disposition, not a failure to work.
`PRODUCTION_READY` is forbidden until cross-bound real evidence exists and the authorized final decision is recorded.
