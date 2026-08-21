# AUDIO WAVE9 — UNIQUE SALVAGE FROM WAVE8

**Date:** 2026-08-21  
**Base main:** `9a3467ef798b2cce840fbb37df6d8a9130d2c66a`  
**Status:** WORKING / CI REQUIRED / NO EXTERNAL EVIDENCE CLAIMS

## Why this branch exists

The old Wave8 PR #111 was overtaken by stronger current-main work:

- merged PR #122 owns authenticated, provenance-bound provider snapshot validation;
- merged PR #132 owns class-specific external evidence trust and prevents caller booleans / `verified=true` / pointer-only evidence from satisfying provider, human, live-audio, alignment, economics or recovery claims;
- Self-Improvement Cycle6 and SI-0014/transaction-recovery work now own broader cross-surface recovery semantics.

Therefore PR #111 must not be merged as a package.

A function-by-function review found only two useful Wave8 mechanisms still missing from current main:

1. append-only human review history with conflict-preserving candidate coverage;
2. exact-N paid live lineage escrow with no-replay recovery coverage.

This branch salvages only those two functions and binds them to the newer trust receipts.

## New bounded runtime modules

### `audio/studio/runtime/human_review_ledger.py`

Pipeline:

`ReviewerAttestationReceipt -> external trust validation -> immutable review record -> hash-chain ledger -> candidate/scope aggregation -> human lock eligibility`

Laws:
- PASS, FAIL and HOLD are preserved as historical human decisions;
- synthetic or structurally invalid human evidence cannot enter the ledger;
- a FAIL is never overwritten by a later PASS;
- PASS+FAIL in one required scope yields `HOLD_CONFLICT`;
- evidence for a different candidate hash cannot fill the current candidate's required scope;
- terminal machine result is at most `ELIGIBLE_FOR_HUMAN_LOCK_DECISION`;
- `voice_lock=false`; `machine_may_auto_lock=false`.

### `audio/studio/runtime/live_lineage_escrow.py`

Pipeline:

`provider auth receipt + durable request + provider result + spend receipt + live audio + optional real alignment -> immutable lineage -> exact-N escrow -> transaction recovery receipts`

Laws:
- accepted provider response is not a production take;
- request/result/spend/audio/alignment are content-hash bound;
- live audio must bind the exact request hash and exact provider-result content hash;
- alignment must bind the accepted audio hash and source hash;
- accepted spend requires a non-synthetic charge reference;
- request/result/spend/audio/alignment for one lineage must share one transaction ID;
- missing/duplicate/unknown/nonaccepted/source-drift/request-drift lineage => escrow HOLD;
- `auto_retry_allowed=false` and `machine_may_replay_paid_request=false`;
- recovery requires a real `TransactionRecoveryReceipt` for every lineage and complete recovered-content-hash coverage;
- duplicate provider calls, duplicate charges or unresolved ambiguity invalidate recovery evidence.

## Explicit non-transfer from old Wave8

Do **not** port:
- old `provider_snapshot.py` — superseded by merged provider snapshot contract;
- old `evidence_proof.py` — superseded by merged external-evidence trust boundary;
- old self-asserted human review event model;
- old pointer-presence recovery semantics;
- any Lesson Zero / ROOM917 / BODYGUARD project facts into generic runtime.

## Acceptance gate

This branch may only advance if:
1. dedicated new tests pass;
2. full `audio/studio/tests` regression passes on the PR merge result;
3. fresh-main delta shows no newer equivalent implementation;
4. Red Team confirms receipt validators cannot be bypassed by booleans or pointer-only artifacts;
5. no provider/human/live/economics claims are inferred from CI.

Even after merge, real production remains externally gated on authenticated provider access, real human review, live audio, alignment, measured economics and actual recovery evidence.
