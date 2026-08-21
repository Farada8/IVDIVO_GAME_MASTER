# SI-0014 — CONTROLLED REVERSIBLE GITHUB↔DRIVE PARTIAL-WRITE RECOVERY PILOT

**Date:** 2026-08-21  
**Status:** `PASS_CONTROLLED_PARTIAL_WRITE_RECOVERY`  
**Evidence class:** `PERSISTED_READBACK / CONTROLLED_REAL_INTEGRATION`  
**Story/canon effect:** NONE.

## Current authority/runtime
- `main` snapshot throughout pilot: `e5f1a50d2960941840687d16939def3b61b5fb57`.
- SI-0014 registry blob at start/end: `39cccc520dc6e8b6db3c693d5572ebf8437c063b`.
- Reconciler source: `tools/ivdivo_durable_write_reconciler.py`.
- Reconciler blob SHA: `93f1d4e8a5f44897ccb0341b1fbcafc7d1e697f2`.

## Transaction
`SI0014-CTRL-PILOT-001`

Shared exact payload SHA256:
`7c50155866b239a38fdfa5be348c9e263995557af52f92d37af91a3183c6e1ee`

Actions:
1. `A1_GITHUB` — reversible create/write, confirmed and read back first.
2. `A2_DRIVE` — intentionally left `NOT_STARTED` to create a controlled partial transaction.

GitHub readback blob:
`5651e33379d3921b8a77713ad875f119ea45bacb`.

## Partial-state decision
With GitHub confirmed/readback and Drive still NOT_STARTED, the current Run33 reconciliation contract returned:

`EXECUTE_MISSING_SAFE_ACTIONS`

with only:

`A2_DRIVE`

No GitHub replay was permitted or needed.

Idempotency keys:
- A1: `ivdtx:d4902c86e5457a4a448f605dd36bd130382b0c45112217ba47ca612dc55ecccd`
- A2: `ivdtx:3c9ef6cc15b12009f1588318d5ab2b9ebc2c9e96d42cd12f5254afad3efa3729`

## Recovery action
Drive action A2 was executed once.
Drive document ID:
`1LLVtur10_W2yD59np1Tm3jgJEmbyZE_MFMLXHrJnIp0`

Drive exact-text readback revision:
`AIroW35xgVi6I3_WUTB5VUtV-liS2t2fgy3jCOBsDkhWJigLf6rkPQ_mxby-Cz4PjO1KuoA8PDhHiKmk4JrWfJUktKwRfRMp_zUwdTDLr70`

Readback payload matched the GitHub payload exactly.

## Final-state decision
After both actions were CONFIRMED with readback and identities matched, the reconciler returned:

`TRANSACTION_COMPLETE`

Transaction SHA256:
`12ec9b484acb7b77911246b0ea5b8115f10d1db3adc25bf7a76baf1f3a673564`

A final fresh-head check confirmed `main` remained `e5f1a50d...`, so no hidden rebase condition invalidated completion.

## Acceptance consequence
SI-0014 acceptance condition `controlled reversible GitHub-Drive partial-write recovery` is now satisfied by real connector writes/readbacks.

Still NOT satisfied:
- genuine involuntary abrupt-session recovery;
- multi-incident recovery-cost trend;
- provider/paid/irreversible side-effect recovery evidence.

Therefore SI-0014 must **not** be promoted beyond its pilot boundary solely from this result. Exact next evidence gate: first genuine interruption/restart incident with persisted before/after recovery evidence.
