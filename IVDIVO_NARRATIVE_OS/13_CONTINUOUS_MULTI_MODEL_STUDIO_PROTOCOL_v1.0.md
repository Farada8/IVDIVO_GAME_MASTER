# IVDIVO NARRATIVE OS — CONTINUOUS MULTI-MODEL STUDIO PROTOCOL

**Status:** PROPOSED CURRENT UPGRADE / Founder-requested integration
**Version:** 1.0
**Date:** 2026-08-21

## PURPOSE

Make IVDIVO production continuous across ChatGPT project conversations, Google Drive, GitHub, File Library and independent AI reviewers without restarting work, losing improvements, or requiring the Founder to repeatedly type `и` merely to move an already-unblocked pipeline forward.

This protocol does **not** authorize background/asynchronous work between user turns. It controls what the studio must do whenever an IVDIVO project turn is active.

## 1. THREE-LAYER AUTHORITY ARCHITECTURE

Do not build one mega-prompt.

### Layer A — Universal Narrative Authority
- Founder newest instruction;
- Writing & Story Production Canon;
- Narrative OS canon/config/router/runbook;
- Story Engine v4.1 / Reference Intelligence;
- Story/Character/Relationship/Scene/Dialogue/Continuity/Reader/Red Team gates.

### Layer B — Genre / Project Overlay
Examples:
- IVDIVO saga / Smith / Orbital Youth;
- Women’s Commercial Story / Dorama;
- romance P46–P53 + Romance Weight Dial;
- project-specific authority, canon, current manuscript and gates.

### Layer C — Downstream Production Overlay
Examples:
- Audio Studio;
- video/teaser;
- publishing/submission;
- localization.

A downstream adapter may not silently change locked story text.

## 2. CROSS-CONVERSATION DELTA BOOT

At the start of any substantial project turn, A00/Showrunner must recover the **latest accepted frontier**, then check for material deltas since the latest handoff/frontier.

Minimum delta surfaces when relevant and accessible:
1. Founder’s newer Project-conversation instructions;
2. GitHub Narrative OS changelog + current project authority/status;
3. Google Drive current authority, handoffs and recently changed project/system files;
4. ChatGPT File Library for newly uploaded engine/reference artifacts;
5. downstream production authority where the active phase requires it.

Do not reread the entire library mechanically. Scan deltas first; perform deep retrieval only for the actual problem.

### DELTA CLASSIFICATION
Every newly discovered mechanism/decision is classified as:
- `PROJECT_ONLY`;
- `GENRE_OVERLAY_CANDIDATE`;
- `UNIVERSAL_CANDIDATE`;
- `REFERENCE_ONLY`;
- `SUPERSEDED`;
- `REJECTED`.

Nothing becomes universal merely because another project used it successfully.

## 3. IMPLICIT CONTINUATION LAW

Explicit commands `и / дальше / продолжай / делай / работай` remain valid, but are no longer required merely to advance an already-open pipeline.

On **any project-relevant user turn** that does not explicitly switch project/subject or forbid further work:
1. answer the immediate request;
2. recover the current production frontier;
3. if the next dependent obligation is unblocked, continue it in the same work block;
4. continue through further dependent GREEN stages until a real stop condition occurs.

Do not end with “next I can…” when that next step is already executable.

### STOP CONDITIONS
Stop only for:
- Founder decision genuinely required;
- unavailable external evidence/provider/human signal;
- unresolved canon/authority conflict;
- FATAL blocker;
- hard tool/permission boundary;
- completion of the requested work unit plus all directly dependent unblocked stages.

## 4. PERSISTENT FRONTIER LAW

Cross-conversation continuation requires persistence. A material work block is not complete until the applicable state is saved.

Where the workflow uses persistence, update:
- current authority/frontier/status;
- decision/gate artifact;
- session handoff;
- affected manifests/hashes when machine-readable production is involved;
- GitHub canon/changelog + Drive mirror when a universal Narrative OS rule changes.

A decision left only in chat is `SESSION_ONLY / NON_AUTHORITY`.

## 5. CROSS-MODEL WORK LAW

Models are evidence-producing roles, not authorities by brand.

Recommended functional separation when multiple models are used:
- **Primary Integrator / Writer:** produces integrated current work and applies accepted fixes;
- **Independent Structural Adversary:** attacks causality, character, mystery, architecture and false certainty;
- **Cold Reader / Retention Adversary:** attacks boredom, clarity, market promise and listener/read-next desire;
- **Specialist Reviewer:** domain-specific medicine/law/science/audio/etc.;
- **Human Signal:** target-reader/listener evidence; never simulated by AI.

Claude/Grok/GPT may occupy these roles, but the role is the contract, not the brand.

### CROSS-MODEL OUTPUT CONTRACT
Each external/model report must record when possible:
- model/provider;
- date;
- project/version reviewed;
- authority loaded;
- exact question;
- finding severity;
- evidence location;
- proposed fix separately from diagnosis;
- status: `PENDING / ACCEPT / MODIFY / REJECT / HOLD`.

No model may promote its own recommendation to CANON/CURRENT.

## 6. PORTABILITY SCOUT

After a project develops a genuinely stronger mechanism, the studio must ask automatically:
1. Is this only story-specific?
2. Is it reusable within a genre?
3. Is it universal process improvement?
4. Does an equal/better mechanism already exist?
5. What regression risk does promotion create?

If reusable, abstract away project names/content and send the mechanism through:
`DISCOVERED -> ABSTRACTED -> COMPARED -> PILOTED -> ACCEPTED -> CURRENT`.

Do not copy project canon across projects.

## 7. DEFAULT REVIEW ORCHESTRATION

The 100-profession roster remains a **deep specialist catalog**, not a ritual headcount.

Default operational review is the smallest sufficient independent panel. For major story reviews, use the canonical 10-lens adversarial gate (see `15_ADVERSARIAL_10_LENS_REVIEW_GATE_v1.0.md`) and call deeper specialists only when a lens finds a real domain risk.

Do not simulate one hundred opinions.

## 8. TARGETED REPAIR LAW

Post-draft defects do not authorize whole-book rewriting by default.

Use the bounded repair protocol in `14_TARGETED_REPAIR_PATCH_CONTRACT_STANDARD_v1.0.md`:
`ISSUE -> PATCH_QUEUE -> PATCH_CONTRACT -> CANDIDATE -> LOCAL_QA -> SELECTIVE_COMMIT -> DOWNSTREAM_INVALIDATION -> REGRESSION`.

Structural/global defects route upward to the earliest failed authority/gate rather than being hidden by local prose edits.

## 9. HUMAN SIGNAL LAW

Internal AI scores are hypotheses, not market validation.

Where a release policy requires Human Signal:
- 5–7 target-audience readers/listeners is a useful minimum pilot;
- blind where practical;
- capture behavior/recall/comprehension/next-unit intent rather than asking for literary praise;
- AI cannot substitute for this gate.

## 10. REFERENCE DELTA LAW

Story Engine v4.1 remains the full Reference Intelligence source. Recovery adapters or project-specific mechanism lists may accelerate work but may not pretend to replace it.

For a live writing problem:
`PROBLEM -> SEARCH RELEVANT SOURCES -> SOURCE COMPLETENESS -> 2–3 INDEPENDENT MECHANISMS -> ABSTRACT -> TRANSFORM -> ORIGINAL CONSTRUCTION -> SIMILARITY/COPY BOUNDARY`.

Do not reread 171 files without a decision reason.

## 11. LOCK FIREWALL

A universal OS improvement does **not** reopen locked project text automatically.

Apply new universal rules to:
- new work;
- currently open stage;
- explicitly unlocked defects;
- downstream production where text remains protected.

Locked work reopens only with new FATAL/MAJOR evidence or Founder instruction.

## 12. HANDOFF MINIMUM

Every material handoff should state:
- ACTIVE PROJECT / BOOK / LINE;
- CURRENT AUTHORITY + IDs/paths;
- CURRENT PHASE;
- LAST COMPLETED STAGE;
- CURRENT GATE;
- OPEN BLOCKERS;
- ACCEPTED NEW MECHANISMS;
- REJECTED/SUPERSEDED branches;
- NEXT UNBLOCKED OBLIGATION;
- downstream artifacts invalidated by any accepted patch.

## 13. NEW-CHAT BEHAVIOUR

On the first project-relevant turn in a new chat:
1. load current router/authority;
2. load current handoff/frontier;
3. run delta boot;
4. reconcile only material new changes;
5. continue the highest-priority unblocked obligation.

Do not ask the Founder to repeat recoverable context.

## 14. SUCCESS CONDITION

The system succeeds when:
- a stronger mechanism discovered in one conversation can be safely reused elsewhere;
- stale branches cannot silently override current work;
- external AI findings remain evidence until integrated;
- locked text is protected;
- repair is selective and regression-tested;
- a new chat continues from persisted state instead of reconstructing from memory;
- explicit `и` becomes optional for pipeline progression inside an active user turn.
