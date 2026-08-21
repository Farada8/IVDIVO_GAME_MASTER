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
- `completed_artifacts[]` with version/hash where possible;
- `last_completed_artifact` and `last_completed_artifact_hash` where possible;
- `open_gates[]`;
- `unresolved_fatal_major[]`;
- `dependency_dag`;
- `next_unblocked_obligations[]`;
- `selected_next_action`;
- `blocked_reasons[]`;
- `external_feedback[]` with provenance;
- `model_handoffs[]` with provenance;
- `last_session_log`;
- `state_revision` or equivalent freshness marker where available;
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

### Continuous obligation loop

After each completed and persisted step:

`RE-READ FRESH STATE -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VERIFY -> PERSIST -> REPEAT`

Continue this loop inside the current executable work block until a mandatory stop state is reached. Do not artificially stop at one chapter, one five-episode batch, one audit or one artifact merely because that unit was convenient, unless the unit itself is the defined gate boundary.

### Mandatory stop states
Stop and report the exact blocker only on:
- `DECISION_GATE` — a genuine Founder choice between materially different story/canon directions;
- `AUTHORITY_UNRESOLVED`;
- `CANON_APPROVAL_REQUIRED`;
- `HUMAN_EVIDENCE_REQUIRED` / Human Signal / human blind-swap;
- `EXTERNAL_PROVIDER_REQUIRED` when no valid provider exists;
- unresolved FATAL or MAJOR requiring upstream repair;
- an irreversible/high-impact action requiring Founder approval;
- a real tool/runtime limitation;
- a safety/legal constraint;
- explicit Founder `STOP / HOLD`.

Do not manufacture a question merely to obtain another user turn.

This law governs work while a model/session is actually executing. It does not claim invisible background execution after the session stops.

---

## 5. CONCURRENT-DIALOG / REBASE LAW

Multiple IVDIVO conversations may advance the same shared project state.

Therefore, immediately before any material write, promotion, lock, authority-pointer change or continuation from a cached plan:
1. re-read the current persisted state/authority;
2. compare its revision/hash/frontier to the state used to produce the candidate;
3. if unchanged, write normally;
4. if another dialog advanced a compatible independent branch, merge/rebase through artifacts and dependency contracts;
5. if another dialog advanced the same dependency/frontier, treat the local candidate as stale until reconciled;
6. never overwrite a newer valid state merely because the local conversation started earlier.

Use optimistic-concurrency controls where available. A stale write failure is a synchronization signal, not permission to force overwrite.

If two newer artifacts disagree, classify `FRONTIER_CONFLICT` and reconcile authority, source hashes, parent artifacts and gates before further production.

---

## 6. DEPENDENCY-DAG LAW

Stages are dependencies, not a ritual checklist.

Independent branches may run in parallel after their upstream PASS gates. They must converge before a consumer stage that requires both.

Generic writing dependency spine:

`AUTHORITY/CONTINUITY -> REFERENCE INTELLIGENCE -> STORY DISCOVERY -> STORY CORE -> CHARACTER -> RELATIONSHIP/MYSTERY/WORLD as applicable -> ARCHITECTURE/WEAVE -> STORY GATE -> SCENE CONTRACTS -> PROSE -> DEVELOPMENT -> RED TEAM -> CHARACTER/RELATIONSHIP/VOICE REGRESSION -> READER -> CONTINUITY/SOURCE-DISTANCE -> LINE -> FINAL STORY GATE -> HUMAN/EXTERNAL SIGNAL where applicable -> LOCK`

Do not invalidate all numerically later artifacts by default. Invalidate only true descendants of the changed source contract.

---

## 7. EARLIEST-FAILURE / MINIMUM-REPAIR LAW

Generalized from current Narrative OS, women’s-story production, Story Recovery and audio production:

`SYMPTOM -> ROOT CAUSE -> EARLIEST FAILED LAYER -> SMALLEST EFFECTIVE REPAIR -> CANDIDATE -> LOCAL QA -> COMMIT OR ROLLBACK -> SELECTIVE DESCENDANT REBUILD -> REGRESSION`

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

Where the execution environment supports transactional repair, freeze source/hash and unaffected siblings, write a candidate branch first, reject no-effect changes, commit only after repair QA, rollback on failed regression, and rebuild only true descendants.

A Founder-approved CANON repair that changes a global story contract requires explicit reapproval before downstream lock.

If the causal map remains stable, continue prose/development. If the causal map breaks, stop drafting and repair upstream first.

Use milestone/block audits at meaningful causal boundaries; do not interrupt every paragraph with full-system review.

---

## 8. CROSS-MODEL WORKFLOW

Models are replaceable specialist backends, not canon authorities.

Default roles when multiple models are actually used:
- **Primary Integrator / production writer-editor:** integrates authority, executes approved work and writes persisted state.
- **Independent Architecture/Character/System Reviewer (e.g. Claude):** adversarial review; does not become canon automatically.
- **Independent Market/Packaging/Alternative-Diagnosis Reviewer (e.g. Grok):** adversarial review; does not become canon automatically.
- Other models/tools may be assigned bounded specialist roles when they materially improve the decision.

Every external model receives a bounded `AGENT_PACKET` / `RUN_CARD`, not the whole uncontrolled archive:
- project ID / active project/book/line;
- active branch;
- source artifact/version/hash;
- build/run ID if relevant;
- exact question/task;
- governing locks;
- forbidden changes;
- parent artifacts;
- open gates/blocker;
- allowed actions;
- required evidence;
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

Parallel model branches are allowed only when they are dependency-independent after their parent gate. Convergence happens through persisted artifacts, hashes, manifests and evidence, not prose memory.

---

## 9. CROSS-DIALOG DELTA HARVEST

Before designing a new universal mechanism, prompt, program or production adapter, inspect newer neighboring-work artifacts in GitHub/Drive and relevant Library sources.

If a useful mechanism already exists elsewhere:

`SOURCE PROJECT MECHANISM -> REMOVE project names/story facts/voice IDs/secrets -> ABSTRACT CONTRACT -> RED TEAM -> UNIVERSAL/TEMPLATE LAYER -> REBIND THROUGH ACTIVE PROJECT OVERLAY`

Promote only mechanisms that:
- solve a recurring class of problems;
- have evidence of actual use, tests or a strong production rationale;
- do not weaken higher authority or project-specific locks;
- can be stated without importing another project's canon.

Do not clone whole project packets into universal canon. Upstream contracts, not project facts.

Before creating a new file, search for an existing current file with the same function. Prefer updating/reconciling one authority over adding another parallel router.

---

## 10. CROSS-MODEL PERSISTENCE / HANDOFF

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

## 11. REFERENCE / BOOK INTELLIGENCE ROUTING

References remain mechanisms, never canon.

`REFERENCE -> ABSTRACT MECHANISM -> REMOVE DISTINCTIVE CONTENT -> COMPARE/COMBINE INDEPENDENT SOURCES -> TRANSFORM THROUGH ACTIVE HERO/SETTING/CONFLICT -> ORIGINAL APPLICATION -> SOURCE-DISTANCE CHECK`

A useful generalized world-through-story mechanism from current orbital work is:

`ORDINARY HUMAN OBJECTIVE -> ENVIRONMENTAL/SOCIAL/SYSTEM CONSTRAINT -> CONSEQUENCE -> CHARACTER CHOICE -> NEW EVIDENCE OR RELATIONSHIP/STATUS CHANGE`

Prefer this to:
`TECHNOLOGY EXPLANATION -> CLEVER OBSERVATION -> PLOT CLUE`.

Craft-source routing:
- structure/scene/conflict/character diagnostics belong primarily to development/rewrite passes and do not automatically reopen a GREEN Story Core;
- clarity/cohesion/emphasis/concision mechanisms belong primarily to late Line/Clarity passes and do not outrank story, causality or character truth;
- dialogue/performance craft is routed as action under pressure, not decorative wit;
- suspense craft tracks emotionally meaningful waiting questions, not arbitrary withholding;
- audio craft privileges causal listening, point-of-audition, useful silence and story-legible sound over decorative sonic density.

---

## 12. P51 / P52 / P53 / HUMAN SIGNAL INHERITANCE

Universal applicable fiction inherits:
- P51 voice differentiation for important speaking characters;
- P52 emotional dynamic-range checks for major emotional arcs;
- current P53 inherited control when character/relationship emotion is relevant;
- Human Signal as external-only evidence.

Current P53 routing is task-classified rather than romance-only:
- A romance-bearing -> full P53;
- B relationship-bearing non-romantic -> relational truth without invented romance;
- C professional/investigative -> preserve competence and hidden personal cost where relevant;
- D family/friendship -> relational truth;
- E antagonistic/status -> power/status/relational consequence;
- F exposition/information -> convert information into action/resistance/choice;
- G action/rescue/emergency -> after-action emotional consequence;
- H audio/performance -> emotional beats must be hearable;
- I visual/marketing -> female-gaze where appropriate plus truthful-promise gate.

P53 never outranks story causality, canon, professional truth, character agency, consent/power, declared Romance Weight or established relationship authority. It must not inject romance into a non-romantic scene.

Internal model review may diagnose; it may not impersonate external human validation.

---

## 13. CONTINUATION COMMAND BEHAVIOR

When Founder says `и / дальше / продолжай / делай / работай`:
1. restore persisted current state;
2. resolve active book/line and newest verified frontier;
3. detect concurrent/newer neighbor artifacts;
4. recompute open gates and dependencies;
5. execute the highest unblocked obligation;
6. verify and persist it;
7. re-read state and continue through further unblocked dependent stages in the same work block;
8. stop only on a mandatory stop state.

Never respond to a recoverable continuation command with generic advice or “what should I do next?”.

---

## 14. SESSION-END / HANDOFF LAW

Before ending a substantive work block, when persistence tools are available:
1. persist material decisions/results;
2. update current state/frontier;
3. record external-model feedback disposition;
4. record unresolved FATAL/MAJOR and open gates;
5. record exact next unblocked obligation or exact blocker;
6. verify the write before claiming synchronization;
7. if a newer sibling-dialog state appeared during the work block, rebase/reconcile before claiming the project synchronized.

If persistence is unavailable, state that fact. Never claim a save that did not happen.

---

## FINAL PRINCIPLE

**STORY FIRST. CHARACTER SECOND. WORLD THROUGH STORY. SAGA THROUGH COMPLETED BOOKS.**

**PERSISTED STATE DRIVES THE WORK. REPEATED “И” IS OPTIONAL SHORTHAND, NOT WORKFLOW PLUMBING.**

**CONTINUE UNTIL A REAL GATE STOPS THE EXECUTABLE WORK — NOT UNTIL THE CHAT NEEDS ANOTHER TURN.**
