# IVDIVO — PRE-EXECUTION RESUME GUARD CANONICAL AMENDMENT

**Status:** CANONICAL AMENDMENT CANDIDATE TO `13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md`  
**Version:** 1.0  
**Date:** 2026-08-22  
**Runtime implementation:** `tools/ivdivo_preexecution_resume_guard.py`  
**Scope:** Sections 2, 5 and 16 of the canonical Cross-Conversation State & Autopilot control layer only.

## 1. PURPOSE

This amendment does not create a second router or a new self-improvement engine. It binds the already merged `PRE_EXECUTION_RESUME_GUARD` runtime to the existing canonical continuation law.

The aggregate/portfolio router is a discovery and prioritization surface. It MUST NOT override a fresher, provenance-valid project-specific persisted frontier.

`ROUTER_POINTER != PROJECT_FRONTIER`

## 2. UNIVERSAL BOOT INSERTION

After resolving the active project and current project-specific state, but before selecting or executing the next obligation, evaluate the merged runtime guard.

Required control sequence:

`RE-READ FRESH STATE -> LOAD ACTIVE PROJECT-SPECIFIC STATE -> PRE_EXECUTION_RESUME_GUARD -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> VERIFY READBACK -> REPEAT`

The guard compares:
- active project identity;
- aggregate/portfolio proposed next action;
- project-specific persisted next action/frontier;
- terminal/decision-gate status when present.

## 3. FAIL-CLOSED OUTCOMES

The runtime outcomes are canonical control states:

- `EXECUTE` — project-specific frontier is present and compatible with the aggregate pointer, or no aggregate pointer exists to conflict with it;
- `STOP_REBASE_REQUIRED` — aggregate pointer conflicts with the project-specific frontier;
- `STOP_NO_PROJECT_STATE` — no project-specific persisted state is available for a consequential continuation;
- `STOP_NO_PROJECT_FRONTIER` — project state exists but has no usable next frontier;
- `PROJECT_NOT_ACTIVE` — loaded state is for a different project and cannot authorize execution.

Only `EXECUTE` permits the normal DAG-selection/execution path. All other outcomes stop the cached/aggregate continuation path until state is corrected or the appropriate project state is loaded.

## 4. SOURCE-OF-TRUTH PRECEDENCE

When a fresher provenance-valid project state conflicts with a stale aggregate pointer:

`PROJECT-SPECIFIC PERSISTED FRONTIER > STALE AGGREGATE ROUTER POINTER`

This precedence does not permit project state to override higher canon/Founder authority. It only prevents an obsolete aggregate progress pointer from reopening completed, locked, terminal or decision-gated work.

A conflict is a synchronization defect to repair, not permission to infer a compromise frontier.

## 5. CONTINUATION COMMAND AMENDMENT

For Founder continuation shorthand (`и / дальше / продолжай / делай / работай`), canonical continuation becomes:

1. restore persisted authority/state;
2. resolve the active project;
3. load its current project-specific persisted state;
4. delta-scan material concurrent changes;
5. run `PRE_EXECUTION_RESUME_GUARD`;
6. if and only if result is `EXECUTE`, recompute open gates/DAG and select the highest unblocked obligation;
7. execute, validate, persist and verify readback;
8. re-read state and repeat;
9. stop on a mandatory stop state or non-`EXECUTE` guard outcome.

## 6. EVIDENCE / PROMOTION BOUNDARY

The guard was promoted narrowly after:
- a real D01 stale-router positive canary prevented duplicate continuation into an already completed frontier;
- D10/D09/D04 negative/regression canaries preserved terminal, Founder-decision and human/provider evidence boundaries;
- CI regression passed on an atomic fresh-main transplant;
- duplicate/stale wider Cycle32D merge surfaces were rejected rather than merged wholesale.

This amendment DOES NOT promote whole Self-Improvement v3, whole Cycle32D, broader decision-yield utilities, or any new global SI identifier.

## 7. REGRESSION CONTRACT

Canonical integration is valid only while all are true:
- the runtime module remains importable;
- stale aggregate/project mismatch returns `STOP_REBASE_REQUIRED`;
- matching frontier returns `EXECUTE`;
- absent project state fails closed;
- this amendment names the guard before `SELECT HIGHEST UNBLOCKED OBLIGATION`;
- `13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md` remains the parent canonical control layer.

If a later canonical Autopilot version incorporates these clauses directly, this amendment may be marked `SUPERSEDED_BY_INTEGRATED_PARENT` rather than maintained as a parallel router.