# 01 — PARALLEL DEVELOPMENT + AUTHORITY RECONCILIATION

## Reused current mechanisms
The current IVDIVO Self-Improvement stack already provides the control laws required here:
- evidence contract before promotion;
- highest-information unblocked test;
- provenance and readback;
- invalidation/rollback;
- candidate → pilot → adversarial review → regression → promotion;
- separate Improvement Registry (what might improve) and Learning Ledger (what was actually observed);
- no fabricated human, provider or market evidence.

Parallel work on 2026-08-21 also established a concurrency law: when sibling dialogs advance `main`, integrate through a fresh branch/PR; do not force-overwrite stale authority.

## Duplicate suppression
This sprint therefore does **not** build another generic Self-Improvement engine, state store, transcript recovery engine, next-action resolver or asset escrow system. It builds one bounded domain adapter: `ZERO CAPITAL OPPORTUNITY ENGINE`.

## Borrowed authority order
`FOUNDER_NEWEST_DIRECT_INSTRUCTION > VERIFIED DOMAIN EVIDENCE > CURRENT SELF-IMPROVEMENT CONTRACTS > THIS SPRINT STATE > HEURISTIC SCORE`

Scores can rank hypotheses. They cannot promote evidence grade.

## New missing envelope
`SIGNAL → OPPORTUNITY → ZERO-CASH GATE → BUYER-BEFORE-BUILD → PROOF LADDER → PAID PILOT → UNIT ECONOMICS → FINANCE READINESS → SCALE → LEARNING WRITE-THROUGH`

## Concurrency / persistence protocol
1. restore latest main/Drive before a new material cycle;
2. work on bounded branch/folder;
3. write exact source/evidence IDs;
4. never overwrite central state to make the package look current;
5. use PR merge/readback before promoting any project-wide pointer;
6. if another dialog advances the same domain, reconcile diffs and preserve both provenance paths.
