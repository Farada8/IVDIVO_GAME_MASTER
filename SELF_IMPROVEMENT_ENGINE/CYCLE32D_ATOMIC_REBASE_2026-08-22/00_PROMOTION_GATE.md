# Cycle32D Atomic Semantic Rebase — Promotion Gate
Date: 2026-08-22
Status: CANDIDATE / ATOMIC TRANSPLANT

## Why
Sequential rebases repeatedly became stale while main advanced. This transplant is constructed as one commit whose parent is an exact fresh main SHA.

## Retained mechanism
PRE_EXECUTION_RESUME_GUARD only.

## Candidate law
RE-READ FRESH STATE -> LOAD ACTIVE PROJECT STATE -> PRE_EXECUTION_RESUME_GUARD -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> READBACK -> REPEAT

## Evidence
- D01 true-positive stale router catch prevented duplicate E97-E120 continuation.
- D10/D09/D04 negative/regression boundaries preserved.
- First rebased CI failed on import path and was not waived.
- Import path repaired; second CI run passed.
- Freshness gate still blocked promotion when main advanced.

## Promotion criteria
1. CI PASS on atomic branch.
2. Fresh comparison against main.
3. No stronger equivalent mechanism in newest main.
4. No weakening of source-of-truth precedence, Founder gates, human evidence gates or locked story layers.

No whole-v3 promotion. No new global SI ID.
