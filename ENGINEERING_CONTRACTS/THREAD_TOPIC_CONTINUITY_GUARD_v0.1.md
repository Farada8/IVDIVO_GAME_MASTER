# THREAD TOPIC CONTINUITY GUARD v0.1

**Date:** 2026-08-22  
**Status:** DEVELOPMENT CONTRACT / CANDIDATE / NOT VERIFIED_CURRENT  
**Parent:** IVDIVO Self-Improvement Meta Engine v2 VERIFIED_CURRENT  
**Related candidate:** ACTIVE_FRONTIER_HIJACK / PR #278 (broader thread-level extension; no automatic promotion)

## Production defect
A conversation that began in a book/project lane drifted into company/business work during generic continuation turns even though the Founder had not explicitly switched projects. The user later corrected the routing and explicitly confirmed that no company switch had been requested.

The earlier Active Frontier Hijack candidate protects the causal frontier from sibling material discovered in GitHub/Drive/Gmail/File Library. This contract adds the missing higher-level invariant: the **conversation thread itself has an active topic lock** that must not be rebound by assistant initiative, memory salience, retrieval results, a fresher sibling CURRENT file, or a generic continuation token.

## Two-level lock
1. `THREAD_TOPIC_LOCK = active_project + active_topic + optional active_next_gate`.
2. `PROJECT_FRONTIER_LOCK = current causal frontier inside that active project`.

Execution order:
`RESTORE THREAD_TOPIC_LOCK -> RESTORE PROJECT_FRONTIER_LOCK -> ROUTE USER TURN -> EXECUTE`.

A global project CURRENT may be fresher than the active thread and still remain non-controlling for that thread.

## Normative laws
`SHORT_CONTINUATION_INHERITS_THREAD_TOPIC`

`GENERIC_CONTINUATION != PROJECT_SWITCH`

`ASSISTANT_PIVOT != USER_SWITCH`

`MENTION_OF_OTHER_PROJECT != THREAD_REBIND`

`SIDE_QUERY != THREAD_REBIND`

`DISCOVERED_CONTEXT != THREAD_REBIND`

`FRESHER_SIBLING_AUTHORITY != THREAD_SWITCH_AUTHORITY`

`GLOBAL_CURRENT != THREAD_CURRENT`

`SHORT_AFFIRMATION_CAN_SWITCH_ONLY_WHEN_BOUND_TO_EXACT_PENDING_SWITCH_TARGET`

`REQUIRED_CROSS_PROJECT_DEPENDENCY_REQUIRES_RETURN_TOKEN`

`NO_ACTIVE_TOPIC + GENERIC_CONTINUATION -> RESTORE_BEFORE_EXECUTE`

`THREAD_TOPIC_LOCK -> PROJECT_FRONTIER_LOCK -> EXECUTION`

## Continuation semantics
Bare turns such as `и`, `дальше`, `продолжай`, `ок`, `да`, `continue`, `go on` inherit the current thread topic.

They do **not** authorize:
- a move to a more recently modified project;
- a move to a project surfaced by memory/search/tooling;
- a move to a project the assistant proposes on its own;
- a move to a sibling project merely because it is relevant;
- a move from a book into Business/SIL/company work without explicit switch evidence.

A short `да/ок` may confirm a project switch only if the assistant previously created an explicit, target-bound pending switch offer and the confirmation resolves that exact target. An unbound affirmative inherits the current topic.

## Side-query semantics
A question about another project may be answered without rebinding the thread. The router emits `ANSWER_SIDE_QUERY_THEN_RETURN` and a return token containing the original project/topic/gate.

Example:
- active: ORBITAL book;
- user: `а что с компанией?`;
- answer the company question;
- restore ORBITAL thread lock unless the user explicitly asks to switch.

## Required dependency semantics
Cross-project work is allowed without a permanent switch only when the current task proves the other project is a required dependency. The router must emit a return token and restore the original thread after the bounded dependency is closed.

## Explicit switch evidence
A project switch is allowed when at least one of these structured conditions is present:
1. direct Founder instruction naming/clearly selecting the new project;
2. target-bound pending switch offer followed by explicit confirmation;
3. a new user task whose structured intent explicitly requests execution in the other project and is not merely a side query.

Semantic similarity, project mention, retrieved files, assistant suggestion and generic continuation are not switch evidence.

## Fail-closed states
- `HOLD_RESTORE_THREAD_TOPIC_BEFORE_CONTINUE`
- `HOLD_NO_ACTIVE_THREAD_TOPIC`
- `HOLD_SWITCH_CONFIRMATION_TARGET_MISMATCH`
- `HOLD_EXPLICIT_SWITCH_WITHOUT_TARGET`
- `HOLD_CROSS_PROJECT_SWITCH_UNAUTHORIZED`
- `HOLD_INVALID_RETURN_TOKEN`

## Real defect fixture
Precondition:
- `active_project = ORBITAL_YOUTH_BOOK`
- `active_topic = ORBITAL_YOUTH_CURRENT_BOOK_WORK`
- user turn = `и`
- assistant proposes `SYNTHESIS_IVDIVO_BUSINESS`
- no explicit user switch

Required result:
`CONTINUE_ACTIVE_TOPIC`, `active_project` remains ORBITAL, `drift_blocked=true`.

## False-positive controls
The guard must not prevent:
- explicit user project switch;
- target-bound `да` confirming an offered switch;
- same-project topic changes;
- bounded side queries;
- required cross-project dependencies with return token.

## Evidence and promotion boundary
Current evidence includes one genuine human-reported routing defect and deterministic engineering canaries. This is enough to justify development and pilot, not VERIFIED_CURRENT promotion.

Promotion requires:
1. exact-head CI success;
2. at least 3 real continuation-routing events across at least 2 distinct project types with zero false project switches;
3. at least 2 healthy explicit-switch controls with zero false blocking;
4. at least 1 side-query-return control;
5. readback/persistence verification;
6. no regression in project/frontier authority rules.

`REAL_DEFECT_OBSERVED != PILOT_SUCCESS`

`GREEN_CANARIES != VERIFIED_CURRENT`

## Runtime
`tools/ivdivo_thread_topic_guard.py`

## Tests
`tests/test_thread_topic_guard.py`
