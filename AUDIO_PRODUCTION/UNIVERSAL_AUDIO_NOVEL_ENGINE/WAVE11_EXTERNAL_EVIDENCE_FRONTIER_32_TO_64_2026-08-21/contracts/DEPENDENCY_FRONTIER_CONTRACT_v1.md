# DEPENDENCY FRONTIER CONTRACT v1

Status: WORKING ENGINEERING CONTRACT / ROUTING ONLY

## Scope
Applies to Wave11 prompts 01–32 and any later candidate reuse only after separate promotion. It governs work ordering, not truth validation.

## Inputs
- versioned prompt graph;
- explicit set of prompt IDs already completed by their authoritative execution/evidence path.

## Outputs
For each prompt: `COMPLETED_ROUTING_INPUT`, `READY_<ACTION_CLASS>`, or `BLOCKED_DEPENDENCY`; plus dependency violations and ready IDs.

## Mandatory invariants
1. Prompt IDs are exactly 01–32 for this version.
2. Every dependency points to an earlier prompt.
3. Unknown completion IDs fail closed.
4. A completed prompt whose dependency is absent produces `HOLD_DEPENDENCY_VIOLATION`.
5. Prompt 30 paid dispatch is never READY before prompt 29 explicit pre-spend GO completion.
6. Prompt 32 paid dispatch is never READY before prompt 31 RB001 human sanity completion.
7. Routing output never authenticates external evidence.
8. Routing output never voice-locks, release-locks, auto-substitutes a voice/model, performs a provider call, performs a paid call, or creates a human review.
9. Canonical receipt validators remain authoritative for provider/human/live/alignment/economics/recovery truth.
10. Caller-supplied completion IDs are planning/routing inputs; they do not become production evidence merely by entering this evaluator.

## Failure modes
- `HOLD_UNKNOWN_COMPLETION_ID`
- `HOLD_DEPENDENCY_VIOLATION`
- static graph construction failure for unknown/non-causal dependencies.

## Non-goals
No provider SDK/API call, no secret handling, no account discovery, no audio render, no listener simulation, no artistic ranking, no cost estimate, no production readiness decision.
