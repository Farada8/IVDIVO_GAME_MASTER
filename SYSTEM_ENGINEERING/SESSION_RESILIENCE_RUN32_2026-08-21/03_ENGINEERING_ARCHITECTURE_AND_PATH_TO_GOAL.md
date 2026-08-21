# SESSION RESILIENCE — ENGINEERING ARCHITECTURE + PATH TO GOAL

Date: 2026-08-21
Status: WORKING INTEGRATION PACKAGE
Fresh-main baseline: `43b1e4db0af9d43563bf244d83bf948781eb3bce`

## 1. Problem being solved

The page/logout incident exposed a failure not fully covered by existing IVDIVO controls.

Existing layers already solve:
- **13 Cross-Conversation Autopilot** — restore durable project state and continue;
- **18B Transcript Recovery** — ingest a pasted/exported prior conversation;
- **17 Asset Escrow** — prevent future-critical binary assets from remaining chat-local;
- **Self-Improvement v2** — learn from recurring production failures.

Missing layer:
`VOLATILE_EXECUTION_WINDOW` — the period in which a session has already done useful work, perhaps written one store but not another, while the durable project frontier has not yet captured enough information to resume safely after abrupt logout/crash.

The browser page itself cannot be guaranteed or recreated by the IVDIVO project engine. The engineering target is stronger: **the work frontier survives even if the page disappears.**

## 2. Architecture

`PROJECT STATE + AUTHORITY SNAPSHOT -> ATOMIC WORK UNIT -> VALIDATE -> DURABLE WRITE/READBACK -> CHECKPOINT -> RECOMPUTE DAG`

Checkpoint is a compact recovery envelope, not another canon/state database.

### Core module
`tools/ivdivo_session_checkpoint.py`

Functions:
- compile normalized checkpoint;
- reject credential-like fields;
- checksum canonical payload;
- verify envelope;
- classify restart.

### Schema
`schemas/IVDIVO_SESSION_CHECKPOINT_SCHEMA_v1.json`

Schema version:
`ivdivo.session_checkpoint/1.0`

### Resume state machine
- `RESUME_EXACT` — authority/state unchanged; no pending writes/artifacts/blockers;
- `REBASE_FIRST` — repo main or project-state revision advanced;
- `RECOVER_VOLATILE_FIRST` — pending write or volatile artifact exists;
- `STOP` — corruption, blocker, invalid state, or security failure.

## 3. Durable write transaction semantics

Each material multi-store mutation should have a stable `write_id`.

Example:
`W123 GitHub branch write = VERIFIED_DURABLE`
`W124 Drive mirror = PENDING_WRITE`

If the page disappears after W123:
- restart does not repeat W123 blindly;
- checkpoint returns `RECOVER_VOLATILE_FIRST`;
- Drive state is re-read;
- only missing W124 is executed;
- readback is verified;
- checkpoint is advanced.

This makes partial GitHub/Drive completion recoverable.

## 4. Concurrency law

Checkpoint includes:
- `repo_main_sha`;
- `state_revision`.

A restart compares them against current persisted truth.

Drift does **not** mean failure. It means sibling work happened.

`DRIFT -> REBASE_FIRST -> READ FRESH DELTA -> DEDUPE -> PRESERVE COMPATIBLE NEWER WORK -> RECOMPUTE NEXT ACTION`.

No force overwrite.

## 5. Relation to transcript recovery

If a full/partial old transcript exists:
`18B -> verify/recover transcript -> project state -> checkpoint/resume`.

If no transcript exists:
`checkpoint -> persisted state -> store readback -> resume/rebase`.

If neither transcript nor checkpoint contains an unpersisted result, the exact lost chat reasoning is not recoverable; only persisted frontier can be trusted. The new mechanism reduces that loss window.

## 6. Relation to asset escrow

Checkpoint may point to artifacts but does not replace byte escrow.

Any future-critical artifact with state:
`CHAT_LOCAL_ONLY / LOCAL_ONLY / UNPERSISTED / PENDING_WRITE`
forces:
`RECOVER_VOLATILE_FIRST`.

Then v17 persistence law owns actual durable-byte escrow.

## 7. Self-improvement integration

New candidate:
`SI-0010 — Volatile Session Checkpoint + Resume Extension`.

Proposed lifecycle:
`PILOT_CODE -> CI -> DIFF RED TEAM -> MERGE/APPLY -> DRIVE READBACK -> REAL INTERRUPTION/RESTART OBSERVATION -> PROMOTION REVIEW`.

The mechanism should record future abrupt-session incidents as learning signals:
- pending write recovered?
- duplicated work avoided?
- stale overwrite prevented?
- volatile artifact caught?
- checkpoint overhead?
- recovery latency/work steps?
- false STOP or false RESUME?

## 8. Additional defect found during this run

`CURRENT_IVDIVO_ENGINE_MACHINE_EXECUTION.json` is stale relative to `tools/ivdivo_next_action.py`.

The pointer still lists universal prerequisites:
- `NEXT_ACTION_SAFE_TRUE`
- `NEXT_ACTION_ZERO_COST_TRUE`
- `NEXT_ACTION_REVERSIBLE_TRUE`

But the modern resolver explicitly states these legacy flags are **not universal continuation prerequisites** under Autopilot v1.2+.

Correct current law is based on:
- freshness;
- authority;
- dependency PASS;
- executable-here;
- explicit STOP gates for Founder choice, human evidence, external provider availability, locked-layer reopen, irreversible/high-impact approval, blockers and FATAL/MAJOR.

Patch this pointer only; do not alter v11.2 packaged bytes retroactively.

## 9. Red Team

### FATAL if introduced
- checkpoint treated as canon;
- checkpoint overrides newer main/project state;
- secrets persisted;
- pending paid/provider action auto-replayed;
- irreversible action auto-replayed;
- chat-local artifact treated durable.

### MAJOR
- checkpoint written so frequently it materially starves production;
- multi-store write duplicated after partial success;
- stale checkpoint overwrites sibling-dialog advancement;
- two parallel recovery authorities created;
- checkpoint stores huge transcript/model scratchpad.

### Design answer
The candidate is intentionally small:
one protocol + one tool + one schema + one focused test suite + one machine-pointer migration.

## 10. Current deterministic evidence

Local isolated unit suite:
- 8 tests;
- 8 PASS;
- 0 FAIL.

Covered:
exact resume; repo drift; state drift; pending write; chat-local artifact; tamper; secret rejection; blocker.

Not yet proven:
- GitHub Actions on integrated branch;
- real abrupt logout recovery;
- cross-device/browser behavior;
- measured checkpoint overhead;
- production deployment in multiple independent projects.

## 11. Path to goal

1. Fresh-read main immediately before write.
2. Create branch from exact current main.
3. Add 18C/tool/schema/tests/CI and Run32 evidence package.
4. Patch machine-execution pointer drift.
5. Register SI-0010 as pending/pilot candidate without touching SI-0008/SI-0009.
6. Run CI.
7. Independent diff Red Team.
8. Re-read main; rebase/recreate branch if sibling work advanced overlapping files.
9. Merge only if no authority conflict and CI/diff review are green.
10. Mirror reports into Drive and verify non-empty readback.
11. Update checkpoint itself with resulting GitHub/Drive durable pointers.
12. Next real interruption becomes production pilot evidence.
