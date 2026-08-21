# IVDIVO — CROSS-CONVERSATION STATE & AUTOPILOT

**Status:** CANONICAL OPERATIONAL CONTROL LAYER  
**Version:** 1.3  
**Established:** 2026-08-21  
**Updated:** 2026-08-21  
**Scope:** all IVDIVO writing/development/revision/reference workflows and all AI sessions that participate in them.  
**Parent authorities:** Founder newest instruction -> `IVDIVO_WRITING_PRODUCTION_CANON.md` -> locked book/saga canon -> `00_NARRATIVE_OS_CANON.md`.  
**Purpose:** make persisted project state, not repeated Founder nudges or chat memory, drive continuation.

---

## 1. PRIMARY LAW

A conversation is temporary. Persisted project state is the shared writers' room memory.

Do not treat ChatGPT, Claude, Grok, Codex or another model session as an isolated workroom. Before substantive work, restore current authority and state from connected project sources when available.

The Founder must not need to type `и / дальше / продолжай / делай / работай` merely to cause an already-determined next production step to happen.

If the next production obligation is unambiguous, unblocked and executable in the current session, continue to it automatically.

`и / дальше / продолжай / делай / работай` remains explicit RESUME shorthand, not a required heartbeat.

A session does not imply invisible background work after it stops. Persisted state makes the next executing session resume correctly.

If a previous conversation ends abruptly and the Founder pastes/copies that conversation into a new one, invoke `18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md` before normal continuation.

---

## 2. UNIVERSAL PROJECT BOOT

Before substantive work resolve:

`ACTIVE PROJECT/BOOK -> ACTIVE LINE -> CURRENT PROJECT AUTHORITY -> CURRENT SOURCE + VERSION + SHA256 -> ACTIVE BRANCH -> MODE/TEXT PROTECTION -> CURRENT PHASE -> BUILD/RUN MANIFEST -> LAST VERIFIED FRONTIER -> LAST COMPLETED ARTIFACT -> OPEN GATES -> UNRESOLVED FATAL/MAJOR -> NEXT UNBLOCKED OBLIGATION`

Required source order when relevant and available:
1. Founder newest direct instruction / Project context.
2. GitHub `Farada8/IVDIVO_GAME_MASTER`, branch `main`.
3. Google Drive current authority / source-of-truth / working mirrors.
4. ChatGPT File Library and uploaded reference sources.
5. Session memory only as convenience, never as silent authority over persisted state.

Authority and freshness are separate questions. A structurally authoritative document may contain an obsolete progress pointer; preserve its law while resolving the newest compatible provenance-valid production frontier.

If a required authority/source/version genuinely conflicts and cannot be reconciled, fail closed as `AUTHORITY_UNRESOLVED` or `FRONTIER_CONFLICT` rather than reconstructing canon from memory.

### Pasted-transcript boot override

If the input contains a copied/exported prior conversation or generated big-paste transcript, first classify it as `FULL_TRANSCRIPT / PARTIAL_TRANSCRIPT / UNKNOWN_COMPLETENESS / MULTI_TRANSCRIPT_BUNDLE`, run the transcript Recovery Ledger, verify any “saved/locked/passed” claims against persisted stores, recover substantive chat-only outputs as candidates, then resume normal project boot from the reconciled frontier.

---

## 3. DELTA-FIRST FRESHNESS LAW

Do not mechanically reread the entire archive on every continuation.

At a substantial project turn:
1. restore the last verified frontier;
2. scan material deltas since that frontier across accessible current sources;
3. deep-read only artifacts that can materially change the current decision;
4. classify discoveries as `PROJECT_ONLY / GENRE_OVERLAY_CANDIDATE / UNIVERSAL_CANDIDATE / REFERENCE_ONLY / SUPERSEDED / REJECTED`;
5. reconcile before execution.

For reference work, first reuse the current abstraction stack where valid:
`Library Audit -> Source Passports -> Mechanism Banks -> Semantic Dedupe -> Source Role Map -> Core Mechanisms -> Crosswalk -> Story Assembly`.

Run a fresh source pass when the problem requires evidence not represented in current extraction, existing extraction is insufficient, or a newer source materially changes the decision.

---

## 4. PROJECT STATE CONTRACT

Every active workflow should maintain equivalent semantics for:
- `project_id`;
- `active_book_or_line`;
- `active_branch`;
- `mode`;
- `current_phase`;
- `authority_sources[]` with path/ID, status, version/revision and hash where available;
- `current_source` and `current_source_sha256` where protected source exists;
- `canon_mode` / `text_protection_mode`;
- `last_verified_frontier`;
- `completed_artifacts[]` with version/hash where possible;
- `last_completed_stage`;
- `last_completed_artifact` and hash where possible;
- `open_gates[]`;
- `open_fatal[]`;
- `open_major[]`;
- `founder_decision_required`;
- `locked_invariants[]`;
- `invalidated_artifacts[]`;
- `dependency_dag`;
- `next_unblocked_obligations[]`;
- `selected_next_action`;
- `blocked_reasons[]`;
- `external_dependencies[]`;
- `external_feedback[]` with provenance;
- `model_handoffs[]` with provenance;
- `last_session_log`;
- `state_revision` / freshness marker where available;
- `updated_at` / `updated_by` / provenance;
- `state_status`.

When recovering from a pasted conversation, also preserve equivalent semantics for:
- `recovery_id`;
- transcript completeness;
- chunks processed/final tail processed;
- recovered Founder directives;
- artifact claims checked;
- verified persisted artifacts;
- `CHAT_ONLY_CANDIDATE / DISCOVERY_ONLY / UNRECOVERABLE_CHAT_ONLY` items;
- unresolved conflicts/unknowns;
- system-improvement candidates;
- recovery write/readback status.

File existence alone is not proof that an artifact is current. Reuse requires valid authority, matching upstream versions/hashes where used, no explicit invalidation, and no newer accepted superseding artifact.

If valid, reuse it. Do not recreate it because another AI/dialog already did the work.

---

## 5. AUTOPILOT / DEEP-WORK LAW

After completing a stage, compute the dependency DAG and highest-priority unblocked obligation.

Continue automatically in the same work block when all are true:
- authority is unambiguous;
- next stage follows causally/dependently from approved work;
- required inputs exist and are freshness-valid;
- no FATAL/MAJOR blocks progression;
- no new Founder canon/creative choice is required;
- no required external human evidence is missing;
- required provider/tool exists, or the stage is internal;
- executing it does not reopen a locked layer without evidence.

Do not stop merely to announce the next step if that step can be completed now.

### Continuous obligation loop

`RE-READ FRESH STATE -> RECOMPUTE DAG -> SELECT HIGHEST UNBLOCKED OBLIGATION -> EXECUTE -> VALIDATE -> PERSIST -> VERIFY READBACK -> REPEAT`

Do not artificially stop at one chapter, one five-episode batch, one audit or one artifact unless that unit is itself a real gate boundary.

### Mandatory stop states
Stop and report the exact blocker only on:
- `DECISION_GATE` — genuine Founder choice between materially different story/canon directions;
- `AUTHORITY_UNRESOLVED`;
- `FRONTIER_CONFLICT`;
- `CANON_APPROVAL_REQUIRED`;
- `HUMAN_EVIDENCE_REQUIRED` / Human Signal / human blind-swap;
- `EXTERNAL_PROVIDER_REQUIRED` when no valid provider exists;
- unresolved FATAL/MAJOR requiring upstream repair;
- irreversible/high-impact action requiring Founder approval;
- real tool/runtime/permission limitation;
- safety/legal constraint;
- explicit Founder `STOP / HOLD`.

Do not manufacture a question merely to obtain another user turn.

---

## 6. CONCURRENT-DIALOG / REBASE LAW

Multiple IVDIVO conversations may advance shared project state.

Immediately before a material write, promotion, lock, authority-pointer change or continuation from a cached plan:
1. re-read current persisted state/authority;
2. compare revision/hash/frontier with the state used to produce the candidate;
3. if unchanged, write normally;
4. if another dialog advanced a compatible independent branch, merge/rebase through artifacts and dependency contracts;
5. if another dialog advanced the same dependency/frontier, local candidate is stale until reconciled;
6. never overwrite a newer valid state because the local conversation started earlier.

Use optimistic-concurrency controls where available. A stale write failure is a synchronization signal, not permission to force overwrite.

Parallel model/dialog branches are allowed only when dependency-independent after parent PASS gates. They converge through persisted artifacts, hashes, manifests and evidence, not conversational memory.

---

## 7. DEPENDENCY-DAG LAW

Stages are dependencies, not a ritual checklist.

Generic writing spine:
`AUTHORITY/CONTINUITY -> REFERENCE INTELLIGENCE -> STORY DISCOVERY -> STORY CORE -> CHARACTER -> RELATIONSHIP/MYSTERY/WORLD as applicable -> ARCHITECTURE/WEAVE -> STORY GATE -> SCENE CONTRACTS -> PROSE -> DEVELOPMENT -> RED TEAM -> CHARACTER/RELATIONSHIP/VOICE REGRESSION -> READER -> CONTINUITY/SOURCE-DISTANCE -> LINE -> FINAL STORY GATE -> HUMAN/EXTERNAL SIGNAL where applicable -> LOCK`

Independent branches may run in parallel after upstream PASS. They must converge before a consumer that requires both.

When upstream changes, invalidate only true descendants. Preserve unrelated accepted siblings.

---

## 8. TARGETED REPAIR / EARLIEST-FAILURE LAW

Current detailed universal repair authority:
`IVDIVO_NARRATIVE_OS/14_TARGETED_REPAIR_PATCH_CONTRACT_STANDARD_v1.0.md`.

General route:
`SYMPTOM -> ROOT CAUSE -> EARLIEST FAILED LAYER -> PATCH_QUEUE/CONTRACT OR STRUCTURAL ROUTE -> CANDIDATE -> LOCAL QA -> SELECTIVE COMMIT OR ROLLBACK -> TRUE-DESCENDANT INVALIDATION -> REGRESSION`.

Never repair:
- story failure with line polish;
- character failure with exposition;
- relationship-authority failure with invented chemistry;
- world/technology failure with lore dump;
- voice/prosody/audio failure by rewriting locked story text unless text is proven failing layer.

Candidate-first. Freeze source/hash and affected scope where supported. Reject no-effect patches. Failed candidates do not mutate accepted bytes. Use finite repair cycles; repeated local failure is evidence to escalate scope.

A Founder-approved CANON repair that changes a global story contract requires explicit reapproval before downstream lock.

---

## 9. ADVERSARIAL REVIEW ROUTING

Current detailed review authority:
`IVDIVO_NARRATIVE_OS/15_ADVERSARIAL_10_LENS_REVIEW_GATE_v1.0.md`.

Default review uses compact independent lenses rather than ritual headcount. The 100-profession layer remains a deep specialist taxonomy/routing inventory.

Escalate only when a specialist can materially change a decision. Do not average FATAL/MAJOR into reassuring numeric scores. Human Signal remains separate external evidence.

---

## 10. CROSS-MODEL WORKFLOW

Models are replaceable specialist backends, not canon authorities. Choose model/tool by capability and task, not brand prestige.

Possible roles include:
- Primary Integrator / production writer-editor;
- Independent structural/architecture adversary;
- Character/relationship reviewer;
- Cold Reader / retention adversary;
- Market/packaging reviewer;
- specialist factual/domain reviewer;
- code/automation worker;
- audio/visual execution worker;
- schema/continuity validator.

Where independence matters, prefer a distinct reviewer path and preserve provenance.

Every external model receives a bounded `AGENT_PACKET` / `RUN_CARD`, not the uncontrolled archive:
- project/book ID and task ID;
- active line/branch/build;
- authority sources + versions/hashes;
- current stage/frontier;
- exact input artifacts;
- exact question/task;
- immutable locks;
- allowed change scope;
- forbidden changes;
- relevant reference mechanisms;
- open gates/blocker;
- required evidence/provenance;
- output schema/file names;
- acceptance gates;
- exact next consumer stage;
- whether pass must be independent of prior conclusions.

Returned recommendations are candidate evidence until disposition:
`ACCEPT / ACCEPT_WITH_MODIFICATION / HOLD_FOR_TEST / REJECT`.

Accepted recommendations are not complete until applied to actual authority/artifact, validated and persisted.

Never invent missing Claude/Grok/GPT feedback. Missing evidence = `UNKNOWN / NOT_RECEIVED`.
No model may self-certify Human Signal, human P51 blind-swap, market performance or publisher/editor feedback that did not occur.

---

## 11. CROSS-DIALOG DELTA HARVEST / PORTABILITY SCOUT

Before designing a new universal mechanism, prompt, program or production adapter, inspect newer neighboring artifacts in GitHub/Drive and relevant Library sources.

For each stronger mechanism ask:
`PROJECT ONLY? GENRE OVERLAY? UNIVERSAL? DUPLICATE? REGRESSION RISK?`

Promotion path:
`DISCOVERED -> ABSTRACTED -> COMPARED -> PILOTED/RED-TEAMED AS NEEDED -> ACCEPTED -> CURRENT`.

Transformation route:
`SOURCE PROJECT MECHANISM -> REMOVE project names/story facts/culprit/clue chain/voice IDs/secrets -> ABSTRACT CONTRACT -> COMPARE/RED TEAM -> UNIVERSAL/TEMPLATE LAYER -> REBIND THROUGH ACTIVE PROJECT OVERLAY`.

Promote only mechanisms that solve a recurring class of problems, have evidence of actual use/tests or strong production rationale, do not weaken higher authority/locks, and can be stated without importing another project's canon.

Before creating a new file, search for an existing current file with the same function. Prefer updating/reconciling one authority over adding a parallel router.

---

## 12. REFERENCE / BOOK INTELLIGENCE ROUTING

References remain mechanisms, never canon:
`REFERENCE -> ABSTRACT MECHANISM -> REMOVE DISTINCTIVE CONTENT -> COMPARE/COMBINE INDEPENDENT SOURCES -> TRANSFORM THROUGH ACTIVE HERO/SETTING/CONFLICT -> ORIGINAL APPLICATION -> SOURCE-DISTANCE CHECK`.

Useful world-through-story route:
`ORDINARY HUMAN OBJECTIVE -> ENVIRONMENTAL/SOCIAL/SYSTEM CONSTRAINT -> CONSEQUENCE -> CHARACTER CHOICE -> NEW EVIDENCE OR RELATIONSHIP/STATUS CHANGE`.

Prefer this to:
`TECHNOLOGY EXPLANATION -> CLEVER OBSERVATION -> PLOT CLUE`.

Craft-source routing:
- structure/scene/conflict/character diagnostics primarily serve development/rewrite and do not automatically reopen a GREEN Story Core;
- clarity/cohesion/emphasis/concision primarily serve late line/clarity work;
- dialogue/performance craft is action under pressure, not decorative wit;
- suspense craft tracks emotionally meaningful waiting questions, not arbitrary withholding;
- audio craft privileges causal listening, point-of-audition, useful silence and story-legible sound over decorative sonic density.

---

## 13. P51 / P52 / P53 / HUMAN SIGNAL INHERITANCE

Universal applicable fiction inherits:
- P51 voice differentiation;
- P52 emotional dynamic-range checks;
- current P53 control when character/relationship emotion is relevant;
- Human Signal as external-only evidence.

Current P53 is task-classified:
- A romance-bearing -> full P53;
- B relationship-bearing non-romantic -> relational truth without invented romance;
- C professional/investigative -> competence + hidden/private cost where relevant;
- D family/friendship -> relational truth;
- E antagonistic/status -> power/status/consequence;
- F exposition/information -> convert information into action/resistance/choice;
- G action/rescue/emergency -> after-action emotional consequence;
- H audio/performance -> emotional beats must be hearable;
- I visual/marketing -> female-gaze where appropriate + truthful-promise gate.

P53 never outranks causality, canon, professional truth, agency, consent/power, declared Romance Weight or relationship authority. It must not inject romance into a non-romantic scene.

Internal model review may diagnose; it may not impersonate external human validation.

---

## 14. CROSS-DOMAIN HANDOFF LAW

A locked/current story may hand off downstream without reopening story development:
`STORY LOCK/CURRENT SOURCE -> AUDIO / VISUAL / TRANSLATION / PUBLISHING / MARKETING ADAPTER`.

Each adapter restores its own current specialized authority and binds to story source/version/hash.

Downstream production cannot silently rewrite locked story to satisfy a provider unless text itself is the proven failing layer and reopening authority exists.

Project-specific identities, voice IDs, clue chains, relationship timing, signature sounds and obsolete branch facts never transfer merely because a production mechanism is reusable.

For voice/casting, current universal audio standard is `IVDIVO_AUDIO_VOICE_AUDITION_BINDING_STANDARD_v1.0.md`.

---

## 15. WRITE-BACK / PERSISTENCE LAW

Future-critical state must not exist only in chat.

Material advancement includes: Founder decisions; authority/canon changes; PASS/FAIL/LOCK/SUPERSEDED; accepted architecture/manuscript patches; validated prompt/program/protocol; completed production artifact; changed frontier; new/resolved FATAL/MAJOR; provider/asset/voice/build locks; external-human evidence that changes status.

Write-back order:
`ARTIFACT/RESULT -> PROJECT CURRENT-STATE POINTER -> RELEVANT CHANGELOG/DECISION RECORD -> DRIVE MIRROR WHERE REQUIRED -> READBACK VERIFICATION`.

Do not rewrite large canon files merely to record volatile local progress. Volatile progress belongs in project state/frontier artifacts; stable reusable laws belong in Narrative OS.

Recommended handoff artifacts:
- `CURRENT_PROJECT_STATE`;
- `CURRENT_PROMPTS_AND_SYSTEM_STATE` when system prompts change;
- provider/model-specific feedback with provenance;
- non-authority draft/variant area;
- timestamped session log with exact next obligation/blocker.

Do not duplicate locked masters into handoff folders. Handoff files point to authority; they do not replace it.

---

## 16. CONTINUATION COMMAND BEHAVIOR

When Founder says `и / дальше / продолжай / делай / работай` or opens a recoverable project continuation:
1. if a pasted/exported previous transcript is present, run `18B_FULL_CHAT_TRANSCRIPT_RECOVERY_AND_INGESTION_PROTOCOL_v1.0.md` first;
2. restore persisted authority/state;
3. resolve newest verified frontier;
4. delta-scan concurrent/newer neighbor artifacts;
5. run stale-work/reuse checks;
6. recompute open gates/DAG;
7. execute highest unblocked obligation;
8. validate, persist, verify;
9. re-read state and continue through further unblocked dependent stages in the same work block;
10. stop only on a mandatory stop state.

Never respond to a recoverable continuation with generic advice or “what should I do next?”.

### Full-chat emergency transfer

Founder workflow `OLD CHAT -> Ctrl+A -> Ctrl+C -> NEW CHAT -> paste -> продолжай` is explicitly supported.

The receiving session owns extraction, verification, dedupe, persistence and continuation. The Founder should not need to annotate the copied conversation manually unless a real authority ambiguity remains after recovery.

Do not dump the entire transcript into canon. Persist the material deltas, recovered artifacts/state and reusable learnings on their correct controlling surfaces.

---

## 17. SESSION-END CHECKPOINT

Before a substantial work block is considered cross-dialog complete, record where applicable:
`DONE / ACCEPTED_OR_CANDIDATE / GATE_STATUS / WHAT_CHANGED / WHAT_DID_NOT_CHANGE / CURRENT_FRONTIER / EXACT_NEXT_UNBLOCKED_OBLIGATION / BLOCKERS / SOURCE_PROVENANCE`.

Before claiming synchronization:
1. persist material results;
2. update current state/frontier;
3. record external-model disposition;
4. record open FATAL/MAJOR and gates;
5. record exact next obligation/blocker;
6. verify readback;
7. if a newer sibling-dialog state appeared, rebase/reconcile first;
8. if this session recovered a pasted transcript, verify `RECOVERY_STATUS = INGESTION_COMPLETE` or record exactly what recovery gap remains.

If persistence is unavailable, say so. Never claim a save that did not happen.

---

## FINAL PRINCIPLE

**STORY FIRST. CHARACTER SECOND. WORLD THROUGH STORY. SAGA THROUGH COMPLETED BOOKS.**

**PERSISTED STATE DRIVES THE WORK. REPEATED “И” IS OPTIONAL SHORTHAND, NOT WORKFLOW PLUMBING.**

**A COPIED OLD CHAT IS A RECOVERY CORPUS: VERIFY, RECOVER, DEDUPE, PERSIST, LEARN, THEN CONTINUE.**

**RESTORE ONCE, EXECUTE FORWARD, VALIDATE, PERSIST, REBASE WHEN NEEDED, AND CONTINUE UNTIL A REAL GATE STOPS EXECUTABLE WORK.**