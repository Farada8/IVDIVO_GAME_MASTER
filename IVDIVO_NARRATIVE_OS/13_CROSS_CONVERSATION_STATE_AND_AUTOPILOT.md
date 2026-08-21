# IVDIVO — CROSS-CONVERSATION STATE & AUTOPILOT

**Status:** CANONICAL OPERATIONAL CONTROL LAYER  
**Version:** 1.0  
**Established:** 2026-08-21  
**Scope:** all IVDIVO writing/development/revision/reference workflows and all AI sessions that participate in them.  
**Parent authorities:** Founder newest instruction -> `IVDIVO_WRITING_PRODUCTION_CANON.md` -> locked book/saga canon -> `00_NARRATIVE_OS_CANON.md`.  
**Purpose:** make persisted project state, not repeated Founder nudges or chat memory, drive continuation.

---

## 1. PRIMARY LAW

A conversation is temporary. Persisted project state is the shared writers' room memory.

Do not treat ChatGPT, Claude, Grok, Codex or any other model session as an isolated workroom. Before substantive work, restore current authority and state from connected project sources when available.

The Founder must not need to type `и / дальше / продолжай / делай / работай` merely to cause an already-determined next production step to happen.

If the next production obligation is unambiguous, unblocked and executable in the current session, continue to it automatically.

`и / дальше / продолжай / делай / работай` remains an explicit RESUME command, not a required heartbeat.

---

## 2. UNIVERSAL PROJECT BOOT

Before substantive work resolve:

`ACTIVE PROJECT/BOOK -> ACTIVE LINE -> CURRENT PROJECT AUTHORITY -> CURRENT SOURCE + VERSION + SHA256 -> ACTIVE BRANCH -> MODE/TEXT PROTECTION -> CURRENT PHASE -> BUILD/RUN MANIFEST -> LAST COMPLETED ARTIFACT -> OPEN GATES -> UNRESOLVED FATAL/MAJOR -> NEXT UNBLOCKED OBLIGATION`

Required source order when relevant and available:
1. Founder newest direct instruction / Project context.
2. GitHub `Farada8/IVDIVO_GAME_MASTER`, branch `main`.
3. Google Drive current authority / source-of-truth / working mirrors.
4. ChatGPT File Library and uploaded reference sources.
5. Session memory only as a convenience, never as silent authority over persisted state.

If a required authority/source/version is ambiguous, fail closed as `AUTHORITY_UNRESOLVED` rather than reconstructing canon from memory.

---

## 3. PROJECT STATE CONTRACT

Every active workflow should maintain a machine- or human-readable state record with at least:

- `project_id`;
- `active_book`;
- `active_line`;
- `mode`;
- `current_phase`;
- `authority_sources[]` including path/ID, status, version/revision and hash where available;
- `current_source` and `current_source_sha256`;
- `active_branch`;
- `canon_mode` / `text_protection_mode`;
- `completed_artifacts[]`;
- `open_gates[]`;
- `unresolved_fatal_major[]`;
- `dependency_dag`;
- `next_unblocked_obligations[]`;
- `selected_next_action`;
- `blocked_reasons[]`;
- `external_feedback[]` with provenance;
- `model_handoffs[]` with provenance;
- `last_session_log`;
- `state_status`.

File existence alone is not proof that an artifact is current. Reuse requires matching authority/source hashes or other explicit freshness evidence.

Authority rank and progress freshness are separate dimensions: an older source may still own canon locks while a newer compatible artifact owns the current production frontier.

---

## 4. AUTOPILOT / DEEP-WORK LAW

After completing a stage, compute the dependency DAG and the highest-priority unblocked obligation.

Continue automatically in the same work block when all are true:
- current authority is unambiguous;
- the next stage follows causally/dependently from already-approved work;
- required inputs exist and are freshness-valid;
- no FATAL/MAJOR blocks progression;
- the action does not require a new Founder canon/creative choice;
- the action does not require external human evidence;
- a required external provider/tool is available, or the stage is internal;
- executing it does not reopen a locked layer without new evidence.

Do not stop merely to announce the next step if that step can be completed now.

### Mandatory stop states
Stop and report the exact blocker only on:
- `DECISION_GATE` — a genuine Founder choice between materially different story/canon directions;
- `AUTHORITY_UNRESOLVED`;
- `CANON_APPROVAL_REQUIRED`;
- `HUMAN_EVIDENCE_REQUIRED` / Human Signal / human blind-swap;
- `EXTERNAL_PROVIDER_REQUIRED` when no valid provider exists;
- unresolved FATAL or MAJOR requiring upstream repair;
- a real tool/runtime limitation;
- a safety/legal constraint.

Do not manufacture a question merely to obtain another user turn.

---

## 5. DEPENDENCY-DAG LAW

Stages are dependencies, not a ritual checklist.

Independent branches may run in parallel after their upstream PASS gates. They must converge before a consumer stage that requires both.

Generic writing dependency spine:

`AUTHORITY/CONTINUITY -> REFERENCE INTELLIGENCE -> STORY DISCOVERY -> STORY CORE -> CHARACTER -> RELATIONSHIP/MYSTERY/WORLD as applicable -> ARCHITECTURE/WEAVE -> STORY GATE -> SCENE CONTRACTS -> PROSE -> DEVELOPMENT -> RED TEAM -> CHARACTER/RELATIONSHIP/VOICE REGRESSION -> READER -> CONTINUITY/SOURCE-DISTANCE -> LINE -> FINAL STORY GATE -> HUMAN/EXTERNAL SIGNAL where applicable -> LOCK`

Do not invalidate all numerically later artifacts by default. Invalidate only true descendants of the changed source contract.

---

## 6. EARLIEST-FAILURE / MINIMUM-REPAIR LAW

Generalized from current Narrative OS, women’s-story production and audio production:

`SYMPTOM -> ROOT CAUSE -> EARLIEST FAILED LAYER -> SMALLEST EFFECTIVE REPAIR -> SELECTIVE DESCENDANT REGRESSION`

Never repair:
- story failure with line polish;
- character failure with exposition;
- relationship-authority failure with invented chemistry;
- world/technology failure with lore dump;
- voice/prosody/audio failure by rewriting locked story text unless text is the proven failing layer.

For every FATAL/MAJOR record:
- symptom;
- evidence;
- root cause;
- earliest responsible layer;
- repair scope;
- what must not break;
- acceptance test;
- descendants to invalidate/rerun.

If the causal map remains stable, continue prose/development. If the causal map breaks, stop drafting and repair upstream first.

Use milestone/block audits at meaningful causal boundaries; do not interrupt every paragraph with full-system review.

---

## 7. CROSS-MODEL WORKFLOW

Models are replaceable specialist backends, not canon authorities.

Default roles when multiple models are actually used:
- **Primary Integrator / production writer-editor:** integrates authority, executes approved work and writes persisted state.
- **Independent Architecture/Character/System Reviewer (e.g. Claude):** adversarial review; does not become canon automatically.
- **Independent Market/Packaging/Alternative-Diagnosis Reviewer (e.g. Grok):** adversarial review; does not become canon automatically.
- Other models/tools may be assigned bounded specialist roles when they materially improve the decision.

Every external model receives a bounded `AGENT_PACKET`, not the whole uncontrolled archive:
- active project/book/line;
- source artifact/version/hash;
- exact question;
- governing locks;
- forbidden changes;
- evidence schema;
- requested output;
- whether the pass must be independent of prior conclusions.

Every returned recommendation is classified:
`ACCEPT / ACCEPT_WITH_MODIFICATION / HOLD_FOR_TEST / REJECT`.

Accepted recommendations are not complete until they are applied to the actual authority/artifact and recorded in persisted state.

Never invent missing Claude/Grok/GPT feedback. Missing evidence = `UNKNOWN / NOT_RECEIVED`.

No model may self-certify:
- real Human Signal;
- human P51 blind-swap;
- market performance;
- publisher/editor feedback that did not occur.

---

## 8. CROSS-MODEL PERSISTENCE / HANDOFF

Future-critical state must not exist only in chat.

Persist when materially changed:
- canon or authority pointer;
- current phase/frontier;
- prompts/router/system architecture;
- FATAL/MAJOR defect register;
- accepted/rejected external critique;
- experimental drafts used for comparison;
- exact next action;
- locks and unresolved dependencies.

Recommended handoff artifacts:
- `CURRENT_PROJECT_STATE`;
- `CURRENT_PROMPTS_AND_SYSTEM_STATE` when system prompts change;
- provider/model-specific feedback files with provenance;
- non-authority draft/variant area;
- timestamped `SESSION_LOG` stating what changed, what is locked, what remains WORKING and the exact next unblocked obligation.

Do not duplicate locked masters into handoff folders and accidentally create parallel canon. Handoff files point to authority; they do not replace it.

---

## 9. REFERENCE / BOOK INTELLIGENCE ROUTING

References remain mechanisms, never canon.

`REFERENCE -> ABSTRACT MECHANISM -> REMOVE DISTINCTIVE CONTENT -> COMPARE/COMBINE INDEPENDENT SOURCES -> TRANSFORM THROUGH ACTIVE HERO/SETTING/CONFLICT -> ORIGINAL APPLICATION -> SOURCE-DISTANCE CHECK`

A useful generalized world-through-story mechanism from current orbital work is:

`ORDINARY HUMAN OBJECTIVE -> ENVIRONMENTAL/SOCIAL/SYSTEM CONSTRAINT -> CONSEQUENCE -> CHARACTER CHOICE -> NEW EVIDENCE OR RELATIONSHIP/STATUS CHANGE`

Prefer this to:
`TECHNOLOGY EXPLANATION -> CLEVER OBSERVATION -> PLOT CLUE`.

Craft-source routing:
- Linda Seger-style structure/scene/conflict/character diagnostics belong primarily to development/rewrite passes; they do not automatically reopen a GREEN Story Core.
- Joseph Williams/Bizup clarity/cohesion/emphasis/concision mechanisms belong primarily to late Line/Clarity passes; they do not outrank story, causality or character truth.

---

## 10. P51 / P52 / P53 / HUMAN SIGNAL INHERITANCE

Universal applicable fiction inherits:
- P51 voice differentiation for important speaking characters;
- P52 emotional dynamic-range checks for major emotional arcs;
- P53 only when relationship authority permits; no invented romance;
- Human Signal as external-only evidence.

P53 never outranks story causality, canon, professional truth, consent/power or established relationship authority.

Internal model review may diagnose; it may not impersonate external human validation.

---

## 11. CONTINUATION COMMAND BEHAVIOR

When Founder says `и / дальше / продолжай / делай / работай`:
1. restore persisted current state;
2. resolve active book/line and newest verified frontier;
3. recompute open gates and dependencies;
4. execute the highest unblocked obligation;
5. continue through further unblocked dependent stages in the same work block;
6. persist materially changed state;
7. stop only on a mandatory stop state.

Never respond to a recoverable continuation command with generic advice or “what should I do next?”.

---

## 12. SESSION-END / HANDOFF LAW

Before ending a substantive work block, when persistence tools are available:
1. persist material decisions/results;
2. update current state/frontier;
3. record external-model feedback disposition;
4. record unresolved FATAL/MAJOR and open gates;
5. record exact next unblocked obligation or exact blocker;
6. verify the write before claiming synchronization.

If persistence is unavailable, state that fact. Never claim a save that did not happen.

---

## FINAL PRINCIPLE

**STORY FIRST. CHARACTER SECOND. WORLD THROUGH STORY. SAGA THROUGH COMPLETED BOOKS.**

**CONTINUE UNTIL A REAL GATE STOPS THE WORK — NOT UNTIL THE CHAT NEEDS ANOTHER “И”.**
