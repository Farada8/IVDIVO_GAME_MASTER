# IVDIVO — SELF-IMPROVEMENT ENGINE

**Status:** CANONICAL OPERATIONAL ENGINE — FOUNDER DIRECTIVE  
**Version:** 1.0  
**Established:** 2026-08-21  
**Parent authorities:** Founder newest instruction; `16_PROJECT_WIDE_CONTINUATION_LAW_v1.0.md`; `13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md`.  
**Scope:** story ideas, craft mechanisms, prompts, programs, process rules, production methods, cross-model workflows, tooling improvements, market/human evidence and domain-specific discoveries across IVDIVO.

---

## 1. PURPOSE

The project must improve cumulatively rather than lose valuable discoveries in conversational fragmentation.

A strong idea is not preserved merely because it appeared in a chat, note, folder or draft. It is preserved only when it enters a tracked lifecycle with provenance, development, testing, disposition and application state.

Core lifecycle:

`DISCOVER -> CAPTURE -> DEDUPE -> CLASSIFY -> DEVELOP -> EVIDENCE -> PILOT/CANARY -> RED TEAM/REGRESSION -> PROMOTION DECISION -> APPLY -> VERIFY -> MONITOR -> RETAIN OR ROLLBACK`

No useful candidate may disappear between DISCOVER and a terminal disposition.

---

## 2. WHAT COUNTS AS A CANDIDATE

Candidate types:
- `STORY_IDEA`;
- `STORY_ENGINE`;
- `CHARACTER_OR_RELATIONSHIP_MECHANISM`;
- `WORLD_OR_SYSTEM_MECHANISM`;
- `CRAFT_MECHANISM`;
- `PROMPT`;
- `PROGRAM_OR_CODE`;
- `PROCESS_OR_ROUTER_RULE`;
- `REPAIR_MECHANISM`;
- `REFERENCE_INSIGHT`;
- `EXTERNAL_MODEL_FINDING`;
- `HUMAN_OR_MARKET_SIGNAL`;
- `AUDIO_VISUAL_PRODUCTION_MECHANISM`;
- `BUG_OR_FAILURE_PATTERN`;
- `TOOLING_OR_AUTOMATION`;
- `OTHER_IMPROVEMENT`.

Capture threshold: the candidate must plausibly improve story quality, character truth, emotional impact, reader engagement, continuity, production reliability, speed, cost, originality, safety, market fit or institutional memory.

Do not flood the registry with every sentence. Capture distinct mechanisms, decisions, hypotheses or failures with material reuse value.

---

## 3. SOURCES / HARVEST

On substantial project work, harvest deltas from relevant available sources:
1. newer sibling Project conversations;
2. GitHub current and working artifacts;
3. Google Drive current/working artifacts;
4. File Library/reference books and prior uploads when relevant;
5. external-model feedback with provenance;
6. human beta feedback / market data where real;
7. production failures, regressions and unexpected successes;
8. current task itself.

Sibling-chat memory without persisted evidence may trigger capture as `DISCOVERY_ONLY`, but must not be promoted until persisted evidence is located or the idea is explicitly restated/captured with source provenance.

---

## 4. CENTRAL REGISTRY LAW

Canonical machine registry:
`31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json`.

Schema:
`31_IDEAS/IMPROVEMENT_REGISTRY_SCHEMA_v1.json`.

Every non-terminal candidate MUST contain:
- stable `candidate_id`;
- title;
- candidate type;
- source provenance;
- source artifact/version/hash where available;
- problem/opportunity;
- proposed mechanism;
- scope classification;
- evidence state;
- risk state;
- owner role;
- current status;
- `next_action`;
- `next_gate`;
- affected systems/projects;
- protected authorities / things that must not break;
- last movement timestamp/date.

### Anti-loss invariant

A non-terminal candidate with no `next_action` or no provenance is a registry failure.

The audit must flag:
- orphan candidate;
- stale candidate;
- chat-only candidate with no persisted substance;
- candidate whose source disappeared;
- promoted candidate not applied to controlling artifact;
- applied candidate not verified;
- rejected/superseded candidate without reason.

---

## 5. STATUS STATE MACHINE

Allowed principal states:

`DISCOVERED`
`CAPTURED`
`DEDUPING`
`DEVELOPING`
`READY_FOR_PILOT`
`PILOTING`
`PILOT_PASS`
`PILOT_FAIL`
`PROMOTION_REVIEW`
`PROMOTED_PROJECT`
`PROMOTED_DOMAIN`
`PROMOTED_UNIVERSAL`
`APPLYING`
`APPLIED_UNVERIFIED`
`VERIFIED_CURRENT`
`HOLD_WITH_TRIGGER`
`REJECTED_WITH_REASON`
`SUPERSEDED`
`ROLLED_BACK`

Terminal states:
`VERIFIED_CURRENT / HOLD_WITH_TRIGGER / REJECTED_WITH_REASON / SUPERSEDED / ROLLED_BACK`.

`HOLD_WITH_TRIGGER` is valid only with an explicit reopen trigger.

---

## 6. DEDUPE / CLUSTER LAW

Before developing a new candidate, search current registry and current authorities for equivalent function.

Classify relationship:
- `NEW`;
- `DUPLICATE`;
- `EXTENSION`;
- `COMPETING_ALTERNATIVE`;
- `SUPERSEDING_CANDIDATE`;
- `PROJECT_SPECIFIC_VARIANT`.

Do not create a new engine/router/prompt merely because wording differs. Prefer improving one controlling authority.

Multiple independently discovered versions of the same mechanism increase evidence only when discovery paths are genuinely independent.

---

## 7. SCOPE CLASSIFICATION

Every candidate is classified before promotion:
- `PROJECT_ONLY`;
- `BOOK_OR_SERIES`;
- `GENRE_OR_DOMAIN`;
- `UNIVERSAL_IVDIVO`;
- `REFERENCE_ONLY`.

Promotion must remove source-project identities, secrets, culprit logic, character names, voice IDs, exact clue chains and other nonportable content.

A mechanism is universal only if it solves a recurring class of problems without importing another project's canon.

---

## 8. DEVELOPMENT CONTRACT

A captured idea must be developed enough to test.

Required fields before pilot:
- exact problem;
- mechanism/hypothesis;
- expected benefit;
- causal explanation of why it should work;
- target layer(s);
- inputs/outputs;
- dependencies;
- failure modes;
- regression risks;
- what must not break;
- smallest viable pilot;
- acceptance test;
- rollback path;
- alternatives/baseline.

For STORY_IDEA candidates, development means Story Discovery, not immediate canonization: human pressure, hero/want/why-now/opposition/price, story engine, emotional promise, distinctiveness and source-distance.

---

## 9. PRIORITY MODEL

Do not rely on one fake precision score. Use a priority vector:
- potential impact: LOW/MEDIUM/HIGH/CRITICAL;
- recurrence: ONE_OFF/RECURRING/SYSTEMIC;
- evidence strength: HYPOTHESIS/INTERNAL_EVIDENCE/INDEPENDENT_REVIEW/PRODUCTION_EVIDENCE/HUMAN_MARKET_EVIDENCE;
- implementation effort: LOW/MEDIUM/HIGH;
- regression risk: LOW/MEDIUM/HIGH/CRITICAL;
- reversibility: EASY/MODERATE/HARD/IRREVERSIBLE;
- urgency: LOW/MEDIUM/HIGH;
- affected surface: LOCAL/DOMAIN/PORTFOLIO.

Router prioritizes high-impact recurring low-regression reversible improvements, but severity/authority gates override priority scoring.

---

## 10. PILOT / CANARY LAW

No broad self-modification directly from an idea.

Preferred route:
`SANDBOX -> SMALL FIXTURE/PILOT -> ADVERSARIAL TEST -> REGRESSION -> LIMITED REAL USE -> PROMOTION`.

For code/programs:
- deterministic tests where possible;
- old regression suite must remain green;
- explicit negative/adversarial tests;
- cold/reproducibility test where package matters;
- fail closed on invalid schemas or missing evidence.

For prompts/process:
- compare against current baseline on bounded representative fixtures;
- record what improved and what regressed;
- do not promote because output merely sounds better.

For story/craft mechanisms:
- pilot on a nonlocked or explicitly authorized scope;
- measure causal/character/reader defects, not word count;
- avoid reopening locked work without new evidence.

For audio/visual/provider mechanisms:
- use canary before scale;
- bind to source/version/hash;
- verify rendered/output behavior, not request construction alone.

---

## 11. RED TEAM / REGRESSION GATE

Before promotion ask:
- Does it weaken higher canon or authority?
- Does it duplicate an existing current mechanism?
- Does it solve the actual root cause or only the symptom?
- Could it improve one metric while harming story/character/continuity?
- Does it silently widen scope?
- Does it require human evidence being simulated by AI?
- Can it be rolled back?
- Which descendants must be retested?
- Does it create more process overhead than value?

Any FATAL/MAJOR unresolved regression blocks promotion.

---

## 12. PROMOTION GATE

Promotion route:

`PROMOTION_REVIEW -> TARGET AUTHORITY -> MIGRATION PLAN -> APPLY -> VERIFY READBACK/TESTS -> UPDATE CURRENT POINTERS -> MARK VERIFIED_CURRENT`.

Promotion levels:
- `PROMOTED_PROJECT`: controlling artifact for one project/book;
- `PROMOTED_DOMAIN`: shared overlay/system for a genre/domain (romance, audio, orbital youth, Smith, etc.);
- `PROMOTED_UNIVERSAL`: Narrative OS / Current system behavior.

A candidate is NOT promoted merely because:
- it is newer;
- multiple models like it;
- test count is larger;
- filename says FINAL;
- it exists in Drive/GitHub;
- it is intellectually elegant.

Promotion requires evidence that it is stronger for the target problem and does not violate higher authority.

---

## 13. APPLICATION MAP

Promotion without application is incomplete.

Every promoted candidate must list exact target artifacts/components:
- prompt(s);
- engine/program code;
- router/config;
- schema;
- project overlays;
- tests;
- handoff/current state;
- docs/Drive mirrors where required.

State changes:
`PROMOTED_* -> APPLYING -> APPLIED_UNVERIFIED -> VERIFIED_CURRENT`.

If only some targets are migrated, candidate remains `APPLYING`.

---

## 14. MONITOR / LEARNING LOOP

After promotion, collect real downstream evidence:
- new defects;
- repeated repairs;
- cycle time;
- regression incidence;
- human signal where available;
- market behavior where real;
- provider/render failures;
- contradictory sibling-project evidence.

A promoted mechanism may be downgraded, constrained, superseded or rolled back when new evidence is stronger.

Self-improvement means evidence-sensitive adaptation, not permanent accumulation of rules.

---

## 15. RULE PRUNING / ANTI-BUREAUCRACY

The engine must also remove obsolete complexity.

At review, ask:
- Is this rule still used?
- Does another current rule subsume it?
- Is it duplicated?
- Does it create ritual without changing decisions?
- Can it be reduced to a simpler invariant?

Possible dispositions:
`KEEP / MERGE / NARROW / SUPERSEDE / DELETE_FROM_CURRENT_AND_ARCHIVE`.

The self-improvement engine is allowed to simplify the system when evidence supports simplification.

---

## 16. STORY IDEA PRESERVATION LAW

Story ideas are especially vulnerable to chat loss.

When a Founder idea or a strong studio-generated story premise is materially distinct and worth future consideration:
1. preserve RAW wording/context where available;
2. create a candidate record;
3. classify `CANON_RELATION = NONE / POSSIBLE / EXISTING_CANON_DEPENDENT`;
4. do not silently convert it to canon;
5. develop a Story Discovery brief when priority warrants;
6. link derivatives/variants to the parent candidate;
7. record why one version wins or loses;
8. retain rejected strong alternatives when their reusable mechanism remains valuable.

A story idea should not vanish because another conversation became active.

---

## 17. AUTOMATIC ROUTER BEHAVIOR

At project boot or a substantial work block, Router runs a bounded Improvement Sweep:
1. read current improvement registry;
2. delta-scan relevant newer sibling artifacts/feedback/failures;
3. capture materially new candidates;
4. dedupe/cluster;
5. surface candidates relevant to the active task;
6. advance any unblocked candidate lifecycle work that can be completed without distracting from higher-priority active production;
7. apply VERIFIED promoted mechanisms through current authority;
8. persist registry changes.

Self-improvement must not starve actual story production. The active story/book remains the primary production obligation unless a FATAL/MAJOR system defect blocks it.

---

## 18. MULTI-AI DEVELOPMENT

Different models may develop/review the same candidate when independence adds evidence.

Use bounded packets. Record model/provider, date, source hashes and whether the model saw prior conclusions.

Recommended independent roles:
- proposer/developer;
- adversarial reviewer;
- implementation worker;
- regression verifier;
- reader/market specialist where relevant.

Never average model opinions into truth. Reconcile through evidence and authority.

---

## 19. REQUIRED AUDITS

### Anti-loss audit
FAIL if any active candidate lacks provenance, next_action, next_gate or owner_role.

### Promotion integrity audit
FAIL if promoted candidate has no applied target or verification evidence.

### Orphan implementation audit
FAIL if a CURRENT mechanism has no source/promotion record when one should exist.

### Stale candidate audit
WARN/FAIL according to priority if a high-impact candidate has had no movement without HOLD trigger.

### Duplication audit
WARN when two current mechanisms solve the same function; require reconciliation.

### Regression audit
FAIL when a promotion creates unresolved FATAL/MAJOR downstream defects.

---

## 20. CURRENT STORAGE

Canonical operational files:
- `IVDIVO_NARRATIVE_OS/17_SELF_IMPROVEMENT_ENGINE_v1.0.md` — law/engine;
- `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json` — live candidate state;
- `31_IDEAS/IMPROVEMENT_REGISTRY_SCHEMA_v1.json` — machine schema;
- `tools/ivdivo_self_improvement.py` — executable local registry/audit utility when available;
- `CURRENT_IVDIVO_SYSTEM_STATE.json` — pointer to current self-improvement state, not candidate detail.

Drive mirrors are working/human-readable surfaces; GitHub main remains canonical where current policy says so.

---

## FINAL LAW

**A GOOD IDEA IS NOT SAVED UNTIL ITS STATE, EVIDENCE, NEXT ACTION AND APPLICATION PATH ARE SAVED.**

**CAPTURE THE BEST. DEVELOP THE BEST. TEST THE BEST. PROMOTE THE BEST. APPLY THE BEST. VERIFY THE RESULT.**

**THE SYSTEM MUST LEARN — AND IT MUST ALSO REMEMBER WHY IT LEARNED.**
