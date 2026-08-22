# IVDIVO — LOCAL GATE REROUTE ADDENDUM v1.0

**Status:** CANONICAL OPERATIONAL ADDENDUM  
**Established:** 2026-08-22  
**Authority:** Founder direct instruction — engine must not stop merely because one branch is blocked.  
**Parent:** `13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md`  
**Scope:** all IVDIVO project, writing, engineering, audio, research and production workflows.

## PRIMARY CORRECTION

A gate blocks only the dependency descendants that actually require it.

`LOCAL GATE != GLOBAL STOP`.

The earlier shorthand in section 5 of the parent Autopilot file must therefore be read with scope semantics: `HUMAN_EVIDENCE_REQUIRED`, `EXTERNAL_PROVIDER_REQUIRED`, `TOOL_RUNTIME_LIMITATION`, missing local input, or a local unresolved FATAL/MAJOR stop only the affected branch unless every remaining executable obligation depends on that gate.

The system must not end a work block merely because the current highest-priority branch is waiting on a human, provider, file, byte object, payment, permission, or other local dependency.

## GATE CLASSES

### GLOBAL STOP

A gate is global only when safe continuation anywhere in the active project is impossible or unauthorized. Examples:

- `AUTHORITY_UNRESOLVED` affecting the project authority itself;
- `FRONTIER_CONFLICT` where competing current states cannot be reconciled;
- `CANON_APPROVAL_REQUIRED` for a change required by every remaining branch;
- safety/legal constraint that prohibits further execution;
- explicit Founder `STOP / HOLD`;
- irreversible/high-impact action when all remaining work depends on that approval.

### LOCAL BLOCK

The following are local by default:

- `HUMAN_EVIDENCE_REQUIRED`;
- human blind listen / Human Signal;
- `EXTERNAL_PROVIDER_REQUIRED`;
- missing provider authentication;
- missing local asset/file/bytes;
- inaccessible single tool/runtime;
- local permission limitation;
- one unresolved branch-specific FATAL/MAJOR;
- one missing upstream dependency whose descendants can be isolated.

A local block is promoted to global only if the recomputed dependency DAG proves that no independent executable obligation remains.

## MANDATORY REROUTE LOOP

When any obligation becomes blocked:

`REGISTER BLOCKER -> CLASSIFY LOCAL/GLOBAL -> MARK TRUE DESCENDANTS BLOCKED -> RECOMPUTE DAG -> SEARCH READY SIBLINGS -> EXECUTE HIGHEST PRIORITY READY SIBLING -> VALIDATE -> PERSIST -> VERIFY -> RECOMPUTE AGAIN`

Do not ask the Founder for another `и / дальше` merely to traverse this loop.

## WORK QUEUE CONTRACT

Every obligation should expose, where practical:

- `id`;
- `priority`;
- `status = READY / RUNNING / DONE / BLOCKED / REJECTED`;
- `dependencies[]`;
- `gate_type` if blocked;
- `gate_scope = LOCAL / GLOBAL`;
- `affected_descendants[]` or computable DAG links;
- `required_inputs[]`;
- `owner/module`;
- `reversible`;
- `cost_or_spend_gate` where relevant;
- `next_consumer`;
- `evidence_required`;
- `persistence_target`.

## SELECTION LAW

The scheduler selects the lowest priority-number READY obligation whose dependencies are DONE.

A blocked obligation is skipped; its true descendants are not eligible; independent siblings remain eligible.

If a global gate exists, return `GLOBAL_STOP`.

If only local gates remain and no READY sibling exists, return `LOCAL_GATE_ONLY_NO_READY_SIBLING`. This means the current executable queue is exhausted, not that the project has no future work.

If the queue is genuinely empty, return `QUEUE_EMPTY`.

## ANTI-BUSYWORK LAW

Continuous work does not authorize filler.

When a branch is blocked, the engine may continue only with real obligations that:

- already exist in the dependency DAG; or
- are required infrastructure, validation, persistence, regression, recovery, provenance, safety, or self-improvement work created by an observed production failure.

Do not invent speculative architecture merely to appear active.

Do not redo a PASS artifact because a different branch is blocked.

## HUMAN-EVIDENCE FIREWALL

Rerouting must never fake completion of a human gate.

The engine may prepare blind packages, scorecards, deterministic machine preflight, provenance, routing, regression harnesses and repair contracts, but may not fabricate:

- a human listen;
- actor belief;
- market preference;
- blind X/Y selection;
- publisher/editor feedback;
- Founder preference not actually given.

The human-blocked node remains BLOCKED while independent work proceeds.

## CONCURRENT-DIALOG LAW

Before any material write after rerouting, re-read the current project pointer and rebase against newer compatible sibling-dialog state. A local reroute is not permission to overwrite a newer frontier.

## ROOM 917 REFERENCE CASE

Current E01 examples:

- `P003B_HUMAN_LISTEN` — LOCAL BLOCK while identifiable assembled audio/human listen is missing;
- `FULL_MASTER_BYTE_RECOVERY` — LOCAL BLOCK while exact full-master bytes are unavailable;
- `RU_PROVIDER_AUTH` — LOCAL BLOCK while provider authentication is missing;
- independent engineering, validation, provenance, queue/routing, non-spend deterministic tests, and other READY siblings may continue if they are not descendants of those gates.

The presence of these gates must not produce a generic session stop.

## EXECUTABLE REFERENCE

Canonical implementation:

`IVDIVO_NARRATIVE_OS/tools/local_gate_router.py`

Regression tests:

`IVDIVO_NARRATIVE_OS/tests/test_local_gate_router.py`

## FINAL LAW

**STOP THE BRANCH, NOT THE ENGINE.**

**A PROJECT STOPS ONLY WHEN A GLOBAL GATE EXISTS OR THE RECOMPUTED EXECUTABLE QUEUE HAS NO READY INDEPENDENT OBLIGATION.**
