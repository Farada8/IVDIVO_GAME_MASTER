# CYCLE32D — SEMANTIC REBASE / PROMOTION GATE

Date: 2026-08-22
Status: REBASED LOCAL CANDIDATE / NO GLOBAL PROMOTION
Base: fresh `main` at branch creation time.

## Why semantic rebase
The original Cycle32D branch diverged materially from main (+27 / -205 at inspection). Blind merge/rebase was rejected because main accumulated newer self-improvement, recovery, decision-yield and business-engineering work.

## Retained unique mechanism
Only the narrow proven mechanism is carried forward:

`PRE_EXECUTION_RESUME_GUARD`

Purpose: before selecting/executing a cached aggregate-router obligation, compare it with the active project-specific current/terminal state. If the project-specific state conflicts, quarantine the aggregate pointer and require rebase.

## Existing laws reused
- Founder newest instruction remains highest authority.
- Project-specific source-of-truth outranks stale aggregate progress pointers.
- Human/provider/market evidence boundaries remain separate.
- No whole-v3 promotion.
- No new global SI identifier.
- Persistence requires write + readback/content verification.

## Candidate loop
`RE-READ FRESH STATE -> LOAD ACTIVE PROJECT STATE -> PRE_EXECUTION_RESUME_GUARD -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> READBACK -> REPEAT`

## Promotion gate
Promote only if the rebased implementation:
1. blocks stale D01-style continuation;
2. allows a matching current project frontier;
3. does not falsely quarantine non-active projects;
4. fails closed when active project state is missing;
5. passes integration regression against current main behavior.

No automatic merge to main from this artifact.