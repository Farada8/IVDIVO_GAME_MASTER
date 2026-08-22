# IVDIVO THREAD TOPIC CONTINUITY GUARD

**Date:** 2026-08-22  
**Lifecycle:** DEVELOPMENT CONTRACT READY -> CANARY -> REAL PILOT  
**Authority effect:** NONE until normal Self-Improvement promotion lifecycle completes.

## Why this exists
The Self-Improvement system already has project/frontier freshness and cross-lane safeguards, but a production defect showed a higher-order gap: the assistant can still change the *conversation's active project* when the user merely says `и`, `дальше`, `ок` or `продолжай`.

This guard makes conversation-topic continuity an explicit control plane.

## Control stack
`FOUNDER TURN -> THREAD TOPIC LOCK -> PROJECT FRONTIER LOCK -> SOURCE/TOOL ROUTING -> EXECUTION`

The active thread lock contains:
- active project;
- active topic/work unit;
- optional current next gate;
- latest valid switch evidence;
- optional bounded-return token.

## Switch evidence classes
- `EXPLICIT_USER_SWITCH` — may rebind thread.
- `BOUND_SWITCH_CONFIRMATION` — may rebind only to the exact pending target.
- `SAME_PROJECT_TOPIC_UPDATE` — changes topic inside project, not project.
- `SIDE_QUERY` — answer and return; no rebind.
- `REQUIRED_DEPENDENCY` — bounded detour with return token; no permanent rebind.
- `GENERIC_CONTINUATION` — inherits current topic.
- `DISCOVERED_SIBLING_CONTEXT` — supporting only.
- `ASSISTANT_INITIATED_PIVOT` — never sufficient switch evidence.

## Immediate operational rule
Until promotion, sessions may use this candidate fail-closed as a local guard, but its evidence status remains CANDIDATE/PILOT. A local use must not be described as VERIFIED_CURRENT.

## Defect learning
Observed real correction:
`GENERIC_CONTINUATION + ASSISTANT_PROJECT_PIVOT -> WRONG_PROJECT`.

Required repaired behavior:
`GENERIC_CONTINUATION -> CONTINUE_ACTIVE_THREAD_TOPIC`.

The specific human correction that triggered this candidate is retained as defect evidence, not as a successful pilot of the repaired mechanism.

## Relation to Active Frontier Hijack
The earlier Active Frontier Hijack candidate asks whether discovered cross-project material may change the causal frontier. This guard wraps that question one level higher:

1. may this turn change the conversation project at all?
2. only then, inside that project, may frontier routing be evaluated.

Therefore:
`THREAD_SWITCH_AUTHORITY PRECEDES FRONTIER_SWITCH_AUTHORITY`.

## Next gate
Run exact CI, then collect real continuation/switch/side-query telemetry without manufacturing events. Promotion requires genuine successful routing events and false-positive controls.

READBACK_MARKER: `SI-THREAD-TOPIC-CONTINUITY-GUARD-REAL-DEFECT-20260822`
