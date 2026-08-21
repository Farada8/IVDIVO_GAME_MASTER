# IVDIVO — VOLATILE SESSION CHECKPOINT + RESUME PROTOCOL v1.0

**Status:** CANDIDATE FOR CANONICAL OPERATIONAL PROMOTION  
**Established:** 2026-08-21  
**Scope:** all IVDIVO writing, audio, visual, research, tooling and self-improvement workflows that may be interrupted by browser logout, tab loss, runtime termination, connector failure, model switch or abrupt conversation termination.  
**Parents:** Founder newest instruction -> current project/book authority -> `13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md` -> `17_CHAT_LOCAL_ASSET_PERSISTENCE_AND_ESCROW_v1.0.md` -> `18_SELF_IMPROVEMENT_META_ENGINE_v2.0.md`.  
**Sibling:** `18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md`.

## 1. DEFECT CLOSED

The studio already restores work from persisted project state and can ingest a pasted/exported old transcript. The 2026-08-21 logout/page-loss incident exposed a separate failure class:

`VOLATILE EXECUTION WINDOW`.

A model may have already:
- discovered a newer authority/frontier;
- executed several analytical steps;
- created material candidate outputs;
- started GitHub/Drive writes;
- identified the exact next action;

while the most recent durable workstate still points to an earlier frontier. If the page disappears before normal handoff/write-through, the next session can recover the project generally but cannot prove exactly which in-flight actions were completed.

This protocol narrows that gap.

## 2. PRIMARY LAW

A browser tab is not project memory.

For every material work block:

`FRESH BOOT -> EXECUTE SMALL ATOMIC UNIT -> VALIDATE -> WRITE/READBACK -> CHECKPOINT -> RECOMPUTE DAG -> CONTINUE`.

The checkpoint is not a transcript and not canon. It is a compact machine resume envelope.

The engine cannot guarantee recovery of the browser UI itself. It guarantees recoverable *work state* to the maximum supported by durable connectors.

## 3. WHEN TO CHECKPOINT

Create/refresh a checkpoint at these boundaries:

1. after a material GitHub/Drive/project-state write is read back;
2. before a long multi-step execution block when loss would cause meaningful rework;
3. before paid/provider/irreversible/high-impact boundaries;
4. before switching project/book/branch/model/tool family;
5. after accepting/rejecting a material system or story candidate;
6. after discovering a new blocker/frontier;
7. after creating a future-critical chat-local artifact, with the artifact explicitly marked volatile until escrow passes;
8. before final response when substantial work is still in progress across multiple systems.

Do not checkpoint after every trivial sentence. The purpose is bounded failure recovery, not ritual logging.

## 4. MINIMUM CHECKPOINT CONTRACT

The durable envelope must preserve equivalent semantics for:

- `project_id`;
- `active_line`;
- `work_unit`;
- `current_phase`;
- `authority_snapshot.repo_main_sha`;
- `authority_snapshot.state_revision`;
- active source/hash pointer when applicable;
- `last_verified_frontier`;
- `last_completed_artifact`;
- `selected_next_action`;
- blockers;
- material writes and their `readback_verified` state;
- material artifacts and whether a durable pointer exists;
- evidence boundaries;
- recovery notes;
- checksum of the checkpoint envelope.

Secrets/credentials are forbidden.

## 5. WRITE STATE CLASSIFICATION

Material writes:
- `DURABLE + readback_verified=true` -> safe to treat as persisted evidence;
- anything else -> pending/volatile and must be reconciled on resume.

Artifacts:
- `DURABLE_WORKING / APPROVED_REFERENCE / LOCKED` with valid durable pointer -> durable;
- `CHAT_LOCAL_ONLY / LOCAL_ONLY / UNPERSISTED / PENDING_WRITE` or missing pointer -> volatile.

A prior model claim such as "saved" never substitutes for readback.

## 6. RESUME DECISION STATES

On a new/recovered session, validate checksum first, then compare checkpoint authority to fresh persisted authority.

### `RESUME_EXACT`
Allowed only when:
- checkpoint hash is valid;
- no pending material write exists;
- no volatile material artifact exists;
- repo/current-state revision still matches;
- no blocker exists.

Resume from `selected_next_action`.

### `REBASE_FIRST`
Use when checkpoint is internally valid but GitHub main or controlling state revision advanced.

Process:
`FRESH READ -> COMPARE DELTA -> PRESERVE NON-CONFLICTING DURABLE WORK -> DISCARD/REBASE STALE PLAN -> RECOMPUTE DAG`.

### `RECOVER_VOLATILE_FIRST`
Use when pending writes or chat/local-only artifacts exist.

Do not rerun blindly. First determine whether the action actually completed in GitHub/Drive/provider/tool state. Then classify:
`VERIFIED_PERSISTED / PARTIAL_WRITE / CHAT_ONLY_CANDIDATE / UNRECOVERABLE / SUPERSEDED`.

### `STOP`
Use for checksum corruption, unresolved authority conflict, real blockers, secret contamination or invalid checkpoint structure.

## 7. TRANSACTION / PARTIAL-WRITE LAW

A multi-system write is not one atomic transaction. Therefore every intended write gets its own `write_id`.

Example:
- `GH-REPORT-01`;
- `DRIVE-REPORT-01`;
- `STATE-POINTER-01`.

If the session dies after GitHub succeeds but before Drive succeeds, the new session must see:
`GH-REPORT-01 = DURABLE/READBACK`, `DRIVE-REPORT-01 = PENDING`.

Recovery completes only the missing side. It does not recreate the GitHub artifact.

## 8. CONCURRENCY LAW

A checkpoint is never permission to overwrite newer work.

Immediately before any material resumed write:
- refresh GitHub main/current project state;
- compare hashes/revisions;
- if changed, route `REBASE_FIRST`;
- preserve compatible independent sibling work;
- fail closed on same-frontier conflict.

This inherits Cross-Conversation Autopilot concurrency law.

## 9. RELATION TO TRANSCRIPT RECOVERY

Use `18B` when a prior full/partial conversation transcript is actually supplied.

Use this protocol when a durable checkpoint exists or the prior page disappeared without a transcript.

If both exist:
1. checkpoint gives the machine frontier;
2. transcript may recover additional chat-only content;
3. persisted authority still outranks both.

## 10. RELATION TO ASSET ESCROW

This protocol does not replace binary/large-asset persistence.

If a future-critical WAV/image/video/ZIP/etc. exists only in chat, checkpoint state must mark it volatile and route to `17_CHAT_LOCAL_ASSET_PERSISTENCE_AND_ESCROW_v1.0.md`.

A checkpoint containing only a filename/hash is not proof that asset bytes are durable.

## 11. SELF-IMPROVEMENT SIGNAL

Every abrupt-session recovery records, when material:
- what would have been lost without persisted state;
- which state field was missing;
- which write was ambiguous;
- how much duplicate work was avoided;
- whether checkpoint cadence was too sparse or too noisy;
- any repeated connector/browser/tool failure pattern.

Reusable findings go through Self-Improvement:
`OBSERVE -> DEDUPE -> EARLIEST FAILURE -> MINIMAL PATCH -> TEST -> REGRESSION -> PROMOTE/HOLD/REJECT -> WRITE-THROUGH`.

## 12. ANTI-BLOAT / STOPPING RULE

Do not build a second project-state system.

The checkpoint is a small envelope around existing authority/state, not another canon, another archive or another full transcript store.

If current state already contains a field, reference it rather than duplicating its full contents.

Checkpoint work is complete when:
- exact restart point is recoverable;
- partial writes are distinguishable;
- volatile artifacts are exposed;
- drift forces rebase;
- secrets cannot persist;
- regression tests pass.

## 13. EXECUTABLE IMPLEMENTATION

Current candidate:
- `tools/ivdivo_session_checkpoint.py`
- `schemas/IVDIVO_SESSION_CHECKPOINT_SCHEMA_v1.json`
- `tests/test_session_checkpoint.py`

Machine decisions:
- `RESUME_EXACT`
- `REBASE_FIRST`
- `RECOVER_VOLATILE_FIRST`
- `STOP`

The tool is read/write only for local checkpoint JSON. It does not call providers, mutate canon, merge branches or spend credits.

## FINAL LAW

**THE PAGE MAY DISAPPEAR. THE FRONTIER MUST NOT.**

Persist the smallest machine-verifiable resume state often enough that the next session can prove what completed, what did not, what changed elsewhere and what action comes next.
