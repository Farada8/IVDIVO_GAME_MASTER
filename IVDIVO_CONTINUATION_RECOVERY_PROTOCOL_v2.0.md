# IVDIVO — CONTINUATION / RECOVERY / CROSS-CONVERSATION PROTOCOL v2.0

**Status:** PROPOSED CANON ROUTING ADDENDUM — PR REVIEW REQUIRED  
**Updated:** 2026-08-21  
**Scope:** all IVDIVO book, story-engine, women’s-story, audio and production-system conversations.

## PURPOSE

A short Founder command such as `и / дальше / продолжай / делай / работай` must be enough to resume real work when the continuation point is recoverable.

A chat is temporary. Persisted production state is the shared studio memory.

This protocol does **not** make chat history canon. It defines how to use Project context / sibling-conversation history as a discovery aid, reconcile it against persisted authority, reject stale work, and continue from the freshest verified frontier.

## AUTHORITY AND FRESHNESS

Authority order:

1. Founder’s newest direct instruction.
2. Approved/locked active project or book canon + current Production Master / Source of Truth.
3. Current governing IVDIVO authority for the active domain.
4. Project-specific operational state: `CURRENT_EXECUTION_STATE`, `DRAFT_STATUS`, accepted gate, build/release state, or equivalent.
5. `CURRENT_PROMPTS` / `CURRENT_WORKSTATE` as routing memory only.
6. Source-specific external feedback with disposition.
7. WORKING drafts/candidates/experiments.
8. Reference library/archive.

Within one authority level, prefer the newest **verified content state**, not the newest filename or filesystem timestamp.

GitHub `main` is canonical production storage where the project is represented there. Drive may contain a newer verified WORKING frontier awaiting reconciliation. Never silently choose an older artifact simply because a router named it first.

## MANDATORY FRESHNESS SWEEP

Before substantive work:

1. Resolve `ACTIVE PROJECT / BOOK / EPISODE / SYSTEM` from the Founder’s current instruction and Project context.
2. Load the active project’s current authority / exact source.
3. Load its project-specific status artifact (`CURRENT_EXECUTION_STATE`, `DRAFT_STATUS`, current accepted gate, etc.).
4. Inspect relevant current GitHub `main` state/recent project commits when available.
5. Inspect Drive `CURRENT_PROMPTS`, `CURRENT_WORKSTATE`, active project authority/work files and newer verified working frontier.
6. Use File Library/reference books/scripts/research only when they materially improve the decision.
7. Inspect new Claude/Grok/GPT/other-model handoff material for this project.
8. Build an internal status map: `CANON / ACTIVE / LOCKED / WORKING / OPTION / UNKNOWN / REFERENCE ONLY / SUPERSEDED / REJECTED`.
9. Run `STALE_WORK_GATE`.
10. Determine `LAST_COMPLETED / OPEN_GATES / BLOCKERS / HIGHEST_UNBLOCKED_NEXT_OBLIGATION`.
11. Execute actual work.
12. Persist/version material results, verify readback and update current status/index if the frontier changed.

## SIBLING-CONVERSATION LAW

Project/sibling-chat history is a **locator**, not durable authority.

If another conversation appears to have advanced the work:

1. identify the claimed artifact/stage/result;
2. locate the persisted file, commit, Drive document, File Library artifact or project status pointer;
3. verify version/status/hash/test or acceptance evidence where available;
4. compare it with the current router/workstate;
5. use the newer valid frontier;
6. update central pointers if the old handoff is materially stale.

Do not ask the Founder to restate information that can be recovered this way.

If the newer accomplishment exists only in chat and cannot be verified/persisted, mark it `UNVERIFIED WORKING MEMORY`; do not silently promote it.

## STALE_WORK_GATE

Re-route instead of working if any of these is true:

- proposed stage already has `PASS / GREEN / LOCKED / ACCEPTED`;
- a newer project-specific state supersedes the generic workstate/router snapshot;
- proposed work depends on a superseded branch/source;
- accepted material would be rebuilt merely because a newer module or format exists;
- external AI feedback has not been accepted/disposed;
- source branch/hash/protected-text state is ambiguous;
- work would silently switch project/book;
- audio/process work would silently reopen locked story;
- an artifact is blocked on real external evidence and the task is only pretending that evidence exists.

## FOUNDER SHORT COMMAND

On `и / дальше / продолжай / делай / работай`:

1. run the freshness sweep;
2. run `STALE_WORK_GATE`;
3. execute the highest unblocked next obligation;
4. do not return to theory unless theory itself is the unresolved obligation;
5. save/version the result;
6. update the active status pointer;
7. report only what is operationally useful: `DONE / STATUS / EXACT NEXT ACTION`.

## EARLIEST-CAUSE + DEPENDENCY-REBUILD LAW

When a real defect exists, repair the earliest causal layer that failed, then rebuild only affected descendants.

Repair order:

`premise/story discovery -> engine -> character -> psychology/social reality -> relationship -> world/mystery/evidence -> architecture -> scene -> dialogue/voice -> audio/sonic execution -> continuity -> packaging`.

Do not polish dialogue around a broken scene or prose around a broken engine.

For a repair transaction:

1. freeze authority and unaffected descendants;
2. locate earliest failed layer;
3. create explicit repair contract;
4. snapshot state before mutation;
5. generate candidate;
6. compute semantic delta;
7. run local/target QA;
8. reject no-effect/out-of-scope candidate;
9. commit only after PASS;
10. invalidate and rebuild only true descendants;
11. run selective regression;
12. rollback the whole transaction on failure;
13. require Founder reapproval before a CANON change becomes authoritative.

This is the integration target for proven Story Recovery transactional mechanisms. A newer recovery test suite is not automatically higher authority than the current engine.

## SCENE / DIALOGUE REPAIR LAW

Scene gate:

`WHO WANTS WHAT? / WHY NOW? / WHAT STOPS THEM? / WHAT CHANGES?`

Enter late. Exit after change.

Dialogue is action. If characters’ motives never cross, there is no dramatic turn. Fix event/character design before endlessly paraphrasing lines.

## MULTI-MODEL HANDOFF CONTRACT

External models are workers/reviewers, not canon authorities.

Every substantive outgoing task should state:

- PROJECT;
- ACTIVE AUTHORITY;
- MATERIAL TO REVIEW;
- STATUS OF MATERIAL;
- TASK;
- WHAT MUST NOT CHANGE;
- KNOWN BLOCKERS/UNCERTAINTIES;
- REQUIRED OUTPUT;
- ACCEPTANCE GATES;
- HANDOFF DESTINATION.

Every returned handoff should record:

- `SOURCE_MODEL`;
- date;
- source artifacts / hashes / URLs when available;
- findings;
- severity (`FATAL / MAJOR / MEDIUM / POLISH`) where applicable;
- proposed repair;
- evidence;
- disposition (`ACCEPTED / PARTIAL / REJECTED / UNRESOLVED`);
- changed artifacts;
- tests/gates;
- blockers;
- exact next action.

Claude feedback remains under `CLAUDE_FEEDBACK`; Grok under `GROK_FEEDBACK`; GPT/other non-authority drafts under `GPT_DRAFTS` or equivalent source-specific working storage unless promoted through authority.

If models disagree, compare evidence and authority. Do not average opinions.

## REFERENCE LIBRARY LAW

Uploaded fiction/scripts/craft/research are `REFERENCE ONLY` unless explicitly promoted.

`REFERENCE -> ABSTRACT MECHANISM -> REMOVE DISTINCTIVE CONTENT -> COMBINE 2–3 INDEPENDENT MECHANISMS WHEN USEFUL -> TRANSFORM THROUGH ACTIVE HERO/SETTING/CONFLICT -> REBIND THROUGH CURRENT CANON -> ORIGINAL STORY`.

## PERSISTENCE / SYNC LAW

Material result is not safely handed off until:

`WORK -> correct status -> GitHub canonical update or review branch/PR where applicable -> Drive mirror/update -> readback verification -> status/index update if frontier changed`.

If GitHub merge is pending, mark the corresponding Drive/system state `SYNC_PENDING`; never claim `main` is updated.

Never store API keys, passwords, secrets or provider credentials in canon/prompts/handoff files.

## FINAL LAW

**DO NOT MAKE THE FOUNDER RE-EXPLAIN RECOVERABLE WORK.**

**DO NOT REPEAT COMPLETED WORK.**

**STORY FIRST. CHARACTER SECOND. WORLD THROUGH STORY. SAGA THROUGH COMPLETED BOOKS.**
