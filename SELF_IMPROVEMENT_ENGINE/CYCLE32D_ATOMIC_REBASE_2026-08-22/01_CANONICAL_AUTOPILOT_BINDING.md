# PRE_EXECUTION_RESUME_GUARD — CANONICAL AUTOPILOT BINDING

Date: 2026-08-22
Status: CANONICAL_BINDING_CANDIDATE

Parent canonical layer: `IVDIVO_NARRATIVE_OS/13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md` v1.3.
Binding amendment: `IVDIVO_NARRATIVE_OS/13A_PRE_EXECUTION_RESUME_GUARD_CANONICAL_AMENDMENT_v1.0.md`.
Runtime: `tools/ivdivo_preexecution_resume_guard.py` (already merged main through PR #271).

Required loop:
`RE-READ FRESH STATE -> LOAD ACTIVE PROJECT-SPECIFIC STATE -> PRE_EXECUTION_RESUME_GUARD -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> VERIFY READBACK -> REPEAT`

Promotion boundary:
- narrow guard binding only;
- no whole-v3 promotion;
- no whole-Cycle32D promotion;
- no new global SI ID;
- broader decision-yield/VOI/registry utilities remain candidates.

Acceptance:
1. branch freshness compatible with main;
2. canonical parent remains authoritative;
3. runtime and amendment regression PASS in GitHub CI;
4. no duplicate stronger current implementation found;
5. Drive mirror write + content readback after merge.