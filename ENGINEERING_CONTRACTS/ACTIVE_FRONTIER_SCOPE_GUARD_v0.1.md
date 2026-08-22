# ACTIVE FRONTIER SCOPE GUARD v0.1

**Status:** DEVELOPMENT CONTRACT / NOT CURRENT AUTHORITY  
**Owner:** Self-Improvement v2 routing governor  
**Defect:** `ACTIVE_FRONTIER_HIJACK`

## Question
How can connected-source discovery enrich the active task without silently changing the active project or causal frontier when the discovered material is not a proven dependency of the current next gate?

## Contract
Before any discovered GitHub/Drive/Gmail/File-Library material changes execution routing, the system MUST hold:

- `ACTIVE_PROJECT_ID`
- `ACTIVE_NEXT_GATE`
- `DISCOVERED_MATERIAL_PROJECT_ID`
- `RELATION_TO_CURRENT_GATE`
- `EXPLICIT_USER_SWITCH_EVENT`

Allowed relation values:
- `SAME_PROJECT_RELEVANT`
- `REQUIRED_DEPENDENCY`
- `SUPPORTING`
- `SIBLING`
- `UNKNOWN`

## Routing law
1. Explicit user switch -> `SWITCH_AUTHORIZED`.
2. Proven required dependency -> `CROSS_LANE_DEPENDENCY_WITH_RETURN_TOKEN`.
3. Same-project relevant evidence -> `USE_IN_CURRENT_FRONTIER`.
4. Supporting/sibling evidence -> `SUPPORTING_ONLY_KEEP_FRONTIER`.
5. Unknown/conflicting scope -> `HOLD_AMBIGUOUS_SCOPE_KEEP_FRONTIER`.
6. Missing active frontier -> `HOLD_NO_ACTIVE_FRONTIER`.

## Non-negotiable invariants
`DISCOVERED_RELEVANCE != FRONTIER_SWITCH_AUTHORITY`.

`SOURCE_DISCOVERY != USER_INTENT_CHANGE`.

`SIBLING_PROJECT_EVIDENCE != ACTIVE_PROJECT_DEPENDENCY`.

`CROSS_LANE_DEPENDENCY -> RETURN_TOKEN -> ORIGINAL_FRONTIER`.

A search result may enrich context. It may not rewrite `ACTIVE_NEXT_GATE` merely because it is interesting, recent, detailed or personally relevant.

## Real defect fixture
Active authority: Business Engineering Cycle8.  
Active frontier: P225/P235 evidence-acquisition chain.  
Discovered material: artist CV / Clúain public-art application evidence.  
Actual relation: sibling/supporting, not a proven P225/P235 dependency.  
Required decision: `SUPPORTING_ONLY_KEEP_FRONTIER`.

## Promotion evidence required
- executable canaries pass;
- at least one real cross-project pilot passes;
- healthy same-project material is not incorrectly blocked;
- explicit user switch remains possible;
- required cross-lane dependency returns to the original frontier;
- false-positive review completed.

No global SI ID is assigned while SI-0016 is reserved by open PR #147.
