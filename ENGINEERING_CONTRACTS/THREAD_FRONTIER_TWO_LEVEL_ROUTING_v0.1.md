# THREAD + FRONTIER TWO-LEVEL ROUTING v0.1

**Date:** 2026-08-22  
**Status:** DEVELOPMENT CONTRACT / BOUNDED CANDIDATE / NOT VERIFIED_CURRENT  
**Parent authority:** Self-Improvement v2 VERIFIED_CURRENT  
**Thread guard:** PR #448 / `tools/ivdivo_thread_topic_guard.py`  
**Predecessor frontier candidate:** draft PR #278

## Problem
The merged Thread Topic Continuity Guard correctly protects the conversation-level project/topic lock, but its contract also requires a lower `PROJECT_FRONTIER_LOCK`. Draft PR #278 contains useful frontier classification logic, yet it also duplicates project-switch authority and can pair a newly switched project with the old project's `active_next_gate`.

That state is invalid:

`NEW_PROJECT + OLD_PROJECT_GATE = ROUTING_CORRUPTION`.

A project switch and a frontier change are related but not the same authorization.

## Architecture
Execution order is mandatory:

`THREAD_TOPIC_LOCK -> PROJECT_FRONTIER_LOCK -> EXECUTION`

### Level 1 — Thread Topic Guard
Only the Thread Topic Guard may authorize a cross-project topic switch from user intent.

It decides:
- generic continuation;
- explicit project switch;
- target-bound short confirmation;
- side query;
- required cross-project dependency;
- unauthorized assistant/retrieval-driven pivot.

### Level 2 — Active Frontier Guard
The Active Frontier Guard has **no project-switch authority**.

It receives an already-established `active_project` and `active_next_gate` and classifies discovered material only as:
- `SAME_PROJECT_RELEVANT`;
- `REQUIRED_DEPENDENCY`;
- `SUPPORTING`;
- `SIBLING`;
- `UNKNOWN`.

It may output:
- `USE_IN_CURRENT_FRONTIER`;
- `CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN`;
- `SUPPORTING_ONLY_KEEP_FRONTIER`;
- fail-closed HOLD states.

## Switch boundary
After Level 1 authorizes a project switch, the old next gate must not be inherited into the new project.

Required sequence:

`SWITCH_AUTHORIZED -> SET_NEW_THREAD_PROJECT/TOPIC -> RESTORE_TARGET_PROJECT_FRONTIER -> EXECUTE`

Until a target-project frontier is restored:

`HOLD_NO_ACTIVE_FRONTIER`.

The Frontier Guard may never infer the new next gate from the old project, discovered context, semantic similarity, or assistant preference.

## Discovery boundary
`DISCOVERED_RELEVANCE != FRONTIER_SWITCH_AUTHORITY`.

`SIBLING_PROJECT_EVIDENCE != ACTIVE_PROJECT_DEPENDENCY`.

`UNKNOWN_RELATION -> HOLD_AMBIGUOUS_SCOPE_KEEP_FRONTIER`.

`SAME_PROJECT_RELEVANT` with a conflicting project identity fails closed.

## Dependency boundary
A proven required dependency may temporarily cross lanes but must preserve a return token:

`CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN -> bounded work -> RETURN_TO_ORIGINAL_FRONTIER`.

Required-dependency status without an identified dependency project fails closed.

## Side query boundary
Side-query routing remains owned by the Thread Topic Guard. The thread return token restores project + topic + next gate after the bounded answer. The side query does not rebind either lock.

## Real defects covered
1. ORBITAL / generic continuation drift into Business without user switch — covered by Thread Topic Guard.
2. Business P225/P235 frontier displaced by artist-CV/public-art discovery — covered by Active Frontier Guard.
3. Draft #278 explicit switch carrying the old project gate into the new project — blocked by this convergence contract.

## Evidence boundary
This integration closes an engineering inconsistency; it does not promote Thread Topic Continuity to VERIFIED_CURRENT.

The existing real pilot requirements remain unchanged:
- 3 real continuation events across at least 2 project types;
- zero false project switches;
- 2 healthy explicit-switch controls;
- 1 side-query-return control;
- persistence/readback verification.

Current pilot evidence remains 2/3 continuation events, 1/2 project types, 0 false switches.

## Runtime
- `tools/ivdivo_thread_topic_guard.py`
- `tools/ivdivo_active_frontier_guard.py`

## Tests
- `tests/test_thread_topic_guard.py`
- `tests/test_active_frontier_guard.py`
- `tests/test_thread_frontier_two_level_routing.py`

## Supersession rule
Draft PR #278 must not be merged after this safer two-level implementation becomes merged authority. Its production-defect provenance is preserved, but its duplicated `explicit_user_switch` runtime path is rejected.
