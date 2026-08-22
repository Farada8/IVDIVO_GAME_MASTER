# Cycle32D Rebased2 — Promotion Gate
Date: 2026-08-22
Status: CANDIDATE / SECOND SEMANTIC REBASE

## Why
The first rebased branch passed CI but main advanced by 57 commits before promotion review. A second semantic rebase was required.

## Retained mechanism
PRE_EXECUTION_RESUME_GUARD only.

## Candidate law
RE-READ FRESH STATE -> LOAD ACTIVE PROJECT STATE -> PRE_EXECUTION_RESUME_GUARD -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> READBACK -> REPEAT

## Required outcomes
EXECUTE / STOP_REBASE_REQUIRED / STOP_NO_PROJECT_STATE / STOP_NO_PROJECT_FRONTIER / PROJECT_NOT_ACTIVE

## Evidence carried forward
- D01 true-positive stale aggregate frontier prevented duplicate production.
- D10/D09/D04 negative/regression boundaries preserved.
- First rebased CI run #1 failed on import path; failure was not waived.
- Workflow was repaired with PYTHONPATH and run #2 passed.

## Promotion rule
Do not promote whole v3 or whole Cycle32D.
Promote only this narrow guard if:
1. rebased2 CI passes;
2. fresh-main comparison shows no material semantic collision;
3. no equivalent stronger mechanism already exists in newest main;
4. project-specific source-of-truth precedence remains intact.
