# Cycle32D — v2 Resume-Gate Integration Candidate

Status: LOCAL CANDIDATE / NO MAIN AUTHORITY PROMOTION
Date: 2026-08-22

## Integration point
Existing canonical loop:
`RE-READ FRESH STATE -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> VERIFY READBACK -> REPEAT`

Candidate guarded loop:
`RE-READ FRESH STATE -> LOAD PROJECT-SPECIFIC STATE -> RESUME_GUARD -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> VERIFY READBACK -> REPEAT`

## RESUME_GUARD outcomes
- `EXECUTE`: project-specific frontier agrees and supplies the selected next action.
- `STOP_REBASE_REQUIRED`: aggregate router conflicts with project-specific frontier; quarantine cached plan and rebase.
- `STOP_NO_PROJECT_FRONTIER`: active project lacks an executable persisted frontier; fail closed.
- `PROJECT_NOT_ACTIVE`: inspected project is not the active portfolio project; no false quarantine.

## Protected invariants
1. Founder newest instruction remains highest authority.
2. Project-specific source-of-truth outranks stale aggregate progress pointers.
3. Universal router law remains reusable even if its cached frontier is stale.
4. No locked story layer is reopened by router convenience.
5. Human/provider/market evidence is never simulated.
6. Candidate integration may not promote itself or v3.

## Executable implementation
- `tools/ivdivo_resume_guard.py`
- `SELF_IMPROVEMENT_DELTAS/CYCLE32D_2026-08-22/tools/cycle32d_stale_router_validator.py`
- `tests/test_ivdivo_resume_guard_cycle32d.py`

## Current proof
Local regression: 5/5 PASS.
Real-project evidence: D01 true-positive stale pointer; D10 regression; D09 founder-decision boundary; D04 human/audio evidence boundary.

## Promotion gate
Do not modify canonical main autopilot until branch review confirms no false block on additional active-project patterns and the integration regression remains green.
