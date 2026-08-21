# IVDIVO — CROSS-CONVERSATION STATE & AUTOPILOT

**Status:** CANONICAL OPERATIONAL CONTROL LAYER  
**Version:** 1.1  
**Established:** 2026-08-21  
**Updated:** 2026-08-21  
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

This law governs continuation **during active user turns**. It does not claim autonomous background/asynchronous work between turns unless a separate scheduled automation explicitly exists.

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

### 2.1 DELTA BOOT — WHAT CHANGED SINCE THE LAST FRONTIER

After current authority/frontier is restored, inspect **material deltas since the latest accepted handoff/state**, not the whole archive by default.

When relevant and accessible, compare:
- newer Founder / Project-conversation instructions;
- GitHub current authority, changelog and project status changes;
- Google Drive current authority, handoffs and recently modified project/system artifacts;
- newly uploaded File Library engine/craft/reference material;
- downstream production authority for the active phase.

Do not reread every book, reference or production file mechanically. Start with the delta. Deep-retrieve older sources only when the current decision requires them.

Classify each material new item before integration:
- `PROJECT_ONLY`;
- `GENRE_OVERLAY_CANDIDATE`;
- `UNIVERSAL_CANDIDATE`;
- `REFERENCE_ONLY`;
- `SUPERSEDED`;
- `REJECTED`.

A newer timestamp is not enough to override higher authority.

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
- `accepted_portable_mechanisms[]`;
- `candidate_portable_mechanisms[]`;
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

On a project-relevant user turn, satisfy the immediate request and then continue directly dependent unblocked obligations. Explicit continuation shorthand is optional.

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

For post-draft bounded repair, use the current universal standard:
`14_TARGETED_REPAIR_PATCH_CONTRACT_STANDARD_v1.0.md`.

Its core chain is:
`ISSUE -> PATCH_QUEUE -> PATCH_CONTRACT -> CANDIDATE -> LOCAL_QA -> SELECTIVE_COMMIT -> DOWNSTREAM_INVALIDATION -> REGRESSION`.

A recovery/adaptor implementation may supply a proven mechanism without becoming the higher Narrative OS authority itself.

---

## 7. CROSS-MODEL WORKFLOW

Models are replaceable specialist backends, not canon authorities.

Default roles when multiple models are actually used:
- **Primary Integrator / production writer-editor:** integrates authority, executes approved work and writes persisted state.
- **Independent Architecture/Character/System Reviewer:** adversarial review; does not become canon automatically.
- **Independent Market/Packaging/Alternative-Diagnosis Reviewer:** adversarial review; does not become canon automatically.
- **Bounded Domain Specialist:** medicine, law, science, sociology, audio, youth, etc., only when domain evidence can change the decision.
- **Human Signal:** separate external evidence class; never simulated by AI.

Claude, Grok, GPT or another model may occupy different bounded roles in different tasks. The role contract matters more than the model brand.

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

### 7.1 PORTABILITY SCOUT — LEARN FROM NEIGHBORING PROJECTS WITHOUT CANON LEAK

Whenever a project/dialog produces a materially stronger mechanism, the Integrator must ask:
1. Is this story/project-specific?
2. Is it reusable only inside a genre/format overlay?
3. Is it a universal production improvement?
4. Does an equal or stronger current mechanism already exist?
5. What regression risk would promotion create?

Promotion path:
`DISCOVERED -> ABSTRACTED -> COMPARED -> PILOTED/VALIDATED -> ACCEPTED -> CURRENT`.

Only the **abstract mechanism** may cross projects. Never silently transfer:
- project canon;
- character names/relationships;
- culprit/solution;
- distinctive clue chain;
- signature sound motif;
- chronology;
- provider voice IDs;
- obsolete branch facts.

If another conversation already promoted an equivalent or stronger universal mechanism, reconcile to that current authority instead of creating a duplicate file/version.

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
- accepted/rejected portability decisions;
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

Reference Intelligence should be queried by the current problem. Do not mechanically reread the full reference library when the current delta/problem can be resolved by targeted retrieval.

---

## 10. REVIEW ORCHESTRATION / P51 / P52 / P53 / HUMAN SIGNAL

The 100-person production layer remains a **deep specialist catalog / role taxonomy**, not evidence that one hundred independent opinions occurred.

Default major internal review should use the current compact operational gate:
`15_ADVERSARIAL_10_LENS_REVIEW_GATE_v1.0.md`.

Escalate from a lens to deeper specialists only when the domain result can materially change a decision.

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
3. run material delta boot;
4. recompute open gates and dependencies;
5. execute the highest unblocked obligation;
6. continue through further unblocked dependent stages in the same work block;
7. persist materially changed state;
8. stop only on a mandatory stop state.

The same progression rule applies after any substantive project-relevant user turn when the next dependent obligation is already known and unblocked.

Never respond to a recoverable continuation with generic advice or “what should I do next?”.

---

## 12. SESSION-END / HANDOFF LAW

Before ending a substantive work block, when persistence tools are available:
1. persist material decisions/results;
2. update current state/frontier;
3. record external-model feedback disposition;
4. record accepted/rejected portable mechanisms when relevant;
5. record unresolved FATAL/MAJOR and open gates;
6. record exact next unblocked obligation or exact blocker;
7. verify the write before claiming synchronization.

If persistence is unavailable, state that fact. Never claim a save that did not happen.

---

## FINAL PRINCIPLE

**STORY FIRST. CHARACTER SECOND. WORLD THROUGH STORY. SAGA THROUGH COMPLETED BOOKS.**

**CONTINUE UNTIL A REAL GATE STOPS THE WORK — NOT UNTIL THE CHAT NEEDS ANOTHER “И”.**
