# SI-0014 — CONTROLLED REVERSIBLE GITHUB↔DRIVE PARTIAL-WRITE RECOVERY PILOT

**Date:** 2026-08-21  
**Status:** `PASS_CONTROLLED_PARTIAL_WRITE_RECOVERY`  
**Evidence class:** `PERSISTED_READBACK / CONTROLLED_REAL_INTEGRATION`  
**Story/canon effect:** NONE.

## Current authority/runtime used by the pilot
- `main` snapshot during the actual transaction: `e5f1a50d2960941840687d16939def3b61b5fb57`.
- SI-0014 registry blob during the actual transaction: `39cccc520dc6e8b6db3c693d5572ebf8437c063b`.
- Reconciler source: `tools/ivdivo_durable_write_reconciler.py`.
- Reconciler blob SHA: `93f1d4e8a5f44897ccb0341b1fbcafc7d1e697f2`.

## Transaction
`SI0014-CTRL-PILOT-001`

Shared exact payload SHA256: `7c50155866b239a38fdfa5be348c9e263995557af52f92d37af91a3183c6e1ee`.

A1_GITHUB was executed first and read back. GitHub payload blob: `5651e33379d3921b8a77713ad875f119ea45bacb`.
A2_DRIVE was deliberately left `NOT_STARTED` to create a controlled partial transaction.

## Partial reconciliation
Current Run33 logic returned `EXECUTE_MISSING_SAFE_ACTIONS` with only `A2_DRIVE`; no GitHub replay was permitted or needed.

Idempotency keys:
- A1: `ivdtx:d4902c86e5457a4a448f605dd36bd130382b0c45112217ba47ca612dc55ecccd`
- A2: `ivdtx:3c9ef6cc15b12009f1588318d5ab2b9ebc2c9e96d42cd12f5254afad3efa3729`

## Recovery
Drive A2 executed once.
Drive document ID: `1LLVtur10_W2yD59np1Tm3jgJEmbyZE_MFMLXHrJnIp0`.
Exact readback revision: `AIroW35xgVi6I3_WUTB5VUtV-liS2t2fgy3jCOBsDkhWJigLf6rkPQ_mxby-Cz4PjO1KuoA8PDhHiKmk4JrWfJUktKwRfRMp_zUwdTDLr70`.
The Drive text matched the GitHub payload exactly.

## Final reconciliation
Decision: `TRANSACTION_COMPLETE`.
Reason: `ALL_ACTIONS_TERMINAL_AND_READBACK_VERIFIED`.
Transaction SHA256: `12ec9b484acb7b77911246b0ea5b8115f10d1db3adc25bf7a76baf1f3a673564`.
A final fresh-head check immediately after the transaction still returned `e5f1a50d...`, so the transaction itself was not invalidated by authority drift.

## Post-pilot rebase
`main` subsequently advanced. This evidence package is re-created on a clean branch from later current main rather than force-updating the original pilot branch. The underlying pilot evidence remains bound to its actual transaction snapshot and is not rewritten as if it happened at the later head.

## Acceptance consequence
The SI-0014 controlled reversible GitHub–Drive partial-write recovery gate is satisfied with real connector write/readback evidence.

Still open:
- genuine involuntary abrupt-session recovery;
- multi-incident recovery-cost baseline;
- paid/provider/irreversible recovery evidence.

Exact next gate: `REAL_INTERRUPTION_EVIDENCE_THEN_RECOVERY_COST_BASELINE_AND_SCOPE_PROMOTION_REVIEW`.
