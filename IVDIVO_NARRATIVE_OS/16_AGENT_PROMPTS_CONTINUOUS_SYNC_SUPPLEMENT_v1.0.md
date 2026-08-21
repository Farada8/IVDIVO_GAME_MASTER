# IVDIVO — AGENT PROMPTS CONTINUOUS SYNC SUPPLEMENT v1.0

**Status:** CANONICAL COMPATIBILITY ROUTER — NO DUPLICATE PROMPT AUTHORITY  
**Established:** 2026-08-21  
**Purpose:** satisfy the canonical Narrative OS v1.3 bootstrap path without creating a second multi-model/prompt system.

## Current controlling sources

Load and obey, in this order where applicable:

1. `IVDIVO_NARRATIVE_OS/13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md` — persisted-state/autopilot/rebase law.
2. `CURRENT_IVDIVO_SYSTEM_STATE.json` — current machine-readable shared frontier; routing state, not story canon.
3. `IVDIVO_NARRATIVE_OS/14_CONTINUOUS_DELTA_AND_LEARNING_REGISTRY.md` — bounded delta scan, learning/promotion, semantic dedupe and write-through law.
4. `IVDIVO_NARRATIVE_OS/14_MULTI_MODEL_HANDOFF_PROMPTS.md` — canonical operational prompt pack for new-chat resume, primary integration, independent reviews, reconciler and handoff.
5. `CURRENT_IVDIVO_CROSS_AI_HANDOFF.md` — current portfolio/project resume card where still freshness-valid.
6. `IVDIVO_NARRATIVE_OS/17_CHAT_LOCAL_ASSET_PERSISTENCE_AND_ESCROW_v1.0.md` — future-critical binary/large assets may not remain chat-local when durable persistence is available.
7. Active project/book authority and project-specific execution state/source-of-truth.

If this compatibility router conflicts with any newer current source above, the newer governing source wins. Do not copy this file into project canon and do not fork its rules into a parallel prompt authority.

## Machine autopilot helpers

Where a project maintains a compatible explicit execution-state artifact, these current GitHub-main helpers may be used:

- `schemas/IVDIVO_EXECUTION_STATE_SCHEMA_v1.json` — generic operational state contract; never story canon.
- `tools/ivdivo_next_action.py` — read-only fail-closed decision helper.

The resolver may return `CONTINUE` only when:
- no declared blocker exists;
- continuation policy explicitly enables automatic continuation;
- repeated continuation word is explicitly not required;
- next action explicitly declares `safe=true`, `zero_cost=true`, `reversible=true`, and `tool_executable_here=true`.

Missing fields fail closed. The resolver never calls providers, spends credits, writes canon or mutates state. Human-readable current authority remains superior to the helper.

## Runtime continuation contract

A project conversation is temporary; persisted state is shared production memory.

For substantive work:

`CURRENT AUTHORITY -> CURRENT SYSTEM/PROJECT STATE -> FRESHNESS SWEEP -> CONCURRENT-DIALOG REBASE -> STALE-WORK GATE -> RECOMPUTE DAG -> HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VERIFY -> PERSIST -> REREAD/REPEAT`.

`и / дальше / продолжай / делай / работай` are optional resume shorthand, not a required heartbeat.

Continue only while the next action is unambiguous, dependency-valid and executable without crossing a real decision/authority/human/provider/FATAL-MAJOR/tool/safety gate. Do not claim invisible background work between sessions.

## Asset-persistence gate

When a work block creates, receives or depends on a future-critical binary/large asset (for example WAV, stems, MP3, ZIP, image, video, PDF, DOCX, alignment sidecar, render log or bundled production output), apply `17_CHAT_LOCAL_ASSET_PERSISTENCE_AND_ESCROW_v1.0.md`.

A chat-visible attachment is not a durable handoff.

Before closing the producing work block, when supported by available tools:
`IDENTIFY/HASH -> PERSIST ORIGINAL BYTES TO SHARED PROJECT STORAGE -> REGISTER POINTER/PROVENANCE -> READBACK ACCESS VERIFY -> UPDATE PROJECT STATE`.

If the current model can see the asset but cannot transfer its bytes with available tools, mark `CHAT_LOCAL_ONLY / PERSISTENCE_BLOCKER` immediately. Do not discover the missing shared bytes only after a later conversation needs them.

Before asking Founder to re-upload a supposedly missing asset, search persisted project state, ingest register, shared Drive/folders, File Library where available, current cross-AI handoff and exact filename/hash/source-conversation discovery.

Do not regenerate a critical missing source asset merely to make the pipeline move.

## Multi-model law

Use model systems as bounded specialist backends, not authorities. Every model receives the same freshness-valid project/source/run context required by its task. Parallel work is allowed only on dependency-independent PASS-gated branches. Merge through persisted artifacts/hashes/evidence, never model voting or conversational consensus.

Classify returned recommendations:
`ACCEPT / ACCEPT_WITH_MODIFICATION / HOLD_FOR_TEST / REJECT`.

Accepted recommendations are incomplete until applied to the controlling artifact and persisted.

## Anti-duplication law

Before inventing a prompt/program/mechanism:
- scan relevant current GitHub/Drive deltas;
- locate any persisted neighboring implementation;
- classify portability;
- abstract only project-neutral mechanism;
- do not transfer names, story facts, clue chains, relationship timing, provider IDs, motifs or secrets.

This file exists only because `01_NARRATIVE_OS_CONFIG.yaml` names this path. The substantive prompt authority remains the current sources listed above.
