# IVDIVO — SELF-IMPROVEMENT v2 RUNTIME VERIFICATION

**Status:** VERIFIED RUNTIME EVIDENCE
**Date:** 2026-08-21
**Scope:** `tools/ivdivo_self_improvement.py` against the live `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json` snapshot verified below.

## Exact source identity

The execution environment could not resolve `raw.githubusercontent.com`, so ordinary clone/curl remained unavailable. The current blobs were retrieved through the authenticated GitHub connector, reconstructed byte-for-byte locally, and verified using Git blob SHA-1 before execution.

- Utility GitHub blob SHA: `0805fd0596a05c2b1f9cdd14bf6f2ce03a6cf358`
- Local reconstructed utility Git blob SHA: `0805fd0596a05c2b1f9cdd14bf6f2ce03a6cf358`
- Live registry GitHub blob SHA: `fe1605a13da9d3b83e9005971f79bb99d6a39999`
- Local reconstructed live registry Git blob SHA: `fe1605a13da9d3b83e9005971f79bb99d6a39999`

Therefore the smoke executed the exact current utility bytes against the exact current registry bytes represented by those blobs.

## Smoke results

### 1. Registry audit

Command:
`python3 tools/ivdivo_self_improvement.py audit`

Result:
`PASS: 7 candidates; anti-loss and promotion-integrity checks green`

### 2. Book/audio priority routing

Command:
`python3 tools/ivdivo_self_improvement.py queue --query 'book audio production' --limit 5`

Top result:
`SI-0007 — Self-Improvement Meta Engine v2 — books first, audio second, whole factory learning`

Command:
`python3 tools/ivdivo_self_improvement.py next --query 'book audio production'`

Result selected `SI-0007`, preserving the guard that active story/project production outranks meta-improvement unless a system FATAL/MAJOR blocks production.

### 3. Negative lifecycle fixture

A temporary copy of the live registry was used. A new candidate `SI-0008` was captured and then intentionally advanced directly to `VERIFIED_CURRENT` without `application_targets` or `verification_evidence`.

The current utility correctly failed closed with:
- `BLOCK PROMOTED_WITHOUT_TARGET`
- `BLOCK VERIFIED_WITHOUT_EVIDENCE`
- exit code `1`

The invalid state was not saved.

## Verdict

**RUNTIME SMOKE: PASS**

The previous blocker `EXACT_EXECUTABLE_UTILITY_RUNTIME_SMOKE_WHEN_RUNNABLE_CHECKOUT_AVAILABLE` is satisfied by exact blob-identity execution. The DNS/clone limitation remains an environment limitation but no longer blocks runtime verification because exact source identity was independently proven before execution.

Promotion consequence:
- `SI-0007` is eligible for `VERIFIED_CURRENT` after normal concurrent-state re-read/rebase.
- `SI-0006` may be marked `SUPERSEDED` as historical/base implementation.

This evidence does not claim literary quality, Human Signal, provider performance, or market performance. It verifies only the registry utility runtime/lifecycle behavior tested above.
