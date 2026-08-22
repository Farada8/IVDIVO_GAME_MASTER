# IVDIVO — BOOK INTELLIGENCE ENGINE — CYCLE 2
## STORY MECHANISM INTELLIGENCE 32→64

**Date:** 2026-08-22  
**Status:** CANDIDATE ENGINEERING LAYER / ADDITIVE TO BOOK INTELLIGENCE v1  
**Local candidate id:** `BOOK-MECH-C01` (not a global SI id)  
**Authority effect:** NONE until normal Self-Improvement promotion gates pass.

## 1. Why this cycle exists
Cycle 1 already solved the library-processing architecture: source identity, rights/access, lifecycle truth, structure map, claim+locator, mechanism abstraction, failure modes, contradiction handling, semantic dedupe, domain adapters, provenance graph, verification and promotion gates.

The remaining story-domain gap is downstream of extraction:
`MECHANISM EXISTS` does not answer `WHICH MECHANISM SHOULD THIS STORY PROBLEM USE, WITH WHAT OTHER MECHANISM, UNDER WHICH CONSTRAINTS, AND DID IT ACTUALLY HELP?`

Therefore this cycle does not create a second Book Intelligence Engine, Story Engine, mechanism register, Self-Improvement Engine, Narrative OS or Writers' Room. It adds one bounded layer:

`LIVE STORY PROBLEM -> STORY PROBLEM SIGNATURE -> ELIGIBLE MECHANISMS -> CONTRAINDICATION GATE -> LEXICOGRAPHIC MATCH VECTOR -> PAIR/SET COMPATIBILITY -> 1–3 MECHANISM COMPOSITION -> STORY MECHANISM PACKET -> BASELINE/CANDIDATE OBSERVATION -> OUTCOME FEEDBACK -> SELF-IMPROVEMENT REVIEW`

## 2. Parallel-development reconciliation
Current reusable authorities found and retained:
- `BOOK_INTELLIGENCE_ENGINE/*` is the universal material-book/reference gateway.
- `tools/ivdivo_book_intelligence.py` owns SourcePassport, mechanism normalization, provenance/promotion and AdapterPacket basics.
- `00_SYSTEM_MECHANISM_PORTABILITY_REGISTER v1.1` is the operational inventory of portable mechanisms; no duplicate registry is created.
- Narrative OS remains story/canon/process authority.
- Self-Improvement v2 remains `VERIFIED_CURRENT`; v3 is not promoted by this cycle.
- B03 / THE EMPTY RESCUE is Founder-locked CH01–29 and release-ready; story mutation is forbidden. It may be used only as a retrospective/shadow control.
- Existing parallel Business Pilot2 was discovered and reused: cross-domain safety replication PASS, no incremental decision gain, promotion HOLD. No duplicate pilot created.
- Fresh parallel NASA deep-source work adds VERIFY/VALIDATE split and bidirectional traceability candidates; this cycle consumes those as upstream and does not duplicate them.

## 3. Concrete engineering modules

### SM-01 Story Problem Signature
Typed input describing the actual decision problem, not a genre wish list. Required: `project_id`, `stage`, `problem_tags`, `desired_effects`, `hard_constraints`. Additional fields: `genre_tags`, `available_conditions`, `protected_facts`, `forbidden_moves`, `max_mechanisms` hard-capped at 3, `locked`.

### SM-02 Mechanism Fit Vector
No magic literary-quality score. Each mechanism receives a visible decision vector: desired-effect fit; problem-tag fit; evidence/lifecycle rank; genre fit; independent source-group coverage; failure-mode completeness. Ranking is lexicographic and auditable. The vector is a routing aid, not proof of story quality.

### SM-03 Contraindication Gate
A mechanism is excluded before ranking when any hard rule fails: HOLD/REJECT lifecycle; distinctive expression not confirmed removed; project-only mechanism crossing projects; missing prerequisites; contraindication intersects current problem/constraint; mechanism requires a forbidden move; locked text would have to mutate.

### SM-04 Mechanism Interaction Gate
Checks explicit pair incompatibility and effect conflicts before composition.

### SM-05 Bounded Composition Engine
Enumerates compatible combinations of 1–3 eligible mechanisms. Chooses by ordered decision vector: desired-effect coverage; problem-tag coverage; weakest evidence strength; independent source-group coverage; fewer mechanisms when equivalent. This implements `MORE MECHANISMS != BETTER`.

### SM-06 Story Mechanism Packet Compiler
Produces a bounded packet containing problem signature hash, selected mechanisms, provenance/evidence locators, match vectors, failure modes, predicted effects clearly marked PREDICTION ONLY, authority/originality constraints and baseline/regression requirements.

### SM-07 Locked-Project Shadow Gate
If a project is locked, packet status becomes `SHADOW_ONLY`. Any mechanism requiring text mutation is rejected. This allows retrospective learning without reopening the book.

### SM-08 Baseline/Candidate Outcome Evaluator
Observed dimensions are compared individually: IMPROVED / SAME / REGRESSED. There is no aggregate literary score. Any protected-dimension regression or MAJOR/FATAL regression blocks the candidate even if another dimension improves.

### SM-09 Outcome Feedback Recorder
Adds project application evidence to the mechanism without changing its source claim/provenance. One real project gain -> SECOND_PROJECT_REQUIRED; two independent real-project gains -> PROMOTION_REVIEW_READY, not auto-promotion; MAJOR/FATAL regression -> HOLD_APPLICATION.

### SM-10 Self-Improvement Bridge
Reusable learning goes through the existing lifecycle: `CANDIDATE -> DEVELOPMENT CONTRACT -> PILOT -> ADVERSARIAL REVIEW -> REGRESSION -> PROMOTION DECISION -> APPLICATION MAP -> APPLY -> READBACK -> VERIFIED_CURRENT`. No new global SI identity is allocated in this cycle.

## 4. Engineering contracts

**C1 Authority:** `FOUNDER/CANON/CURRENT_PROJECT_AUTHORITY > STORY_MECHANISM_PACKET > REFERENCE_MECHANISM`.

**C2 Originality:** `REFERENCE -> ABSTRACT MECHANISM -> DISTINCTIVE EXPRESSION REMOVED -> COMBINE INDEPENDENT MECHANISMS -> CURRENT STORY TRANSFORMATION`. Forbidden transfer includes distinctive plot, characters, setting, scene sequence, solution, signature dialogue, proprietary terminology and signature inventions.

**C3 Evidence:** `MATCH_VECTOR != STORY_QUALITY_PROOF`; `PREDICTED_EFFECT != OBSERVED_EFFECT`; `RETRIEVAL_PASS != DRAFT_PASS`; `MODEL_AGREEMENT != HUMAN_SIGNAL`; `BOOK_KNOWLEDGE != MARKET/PROVIDER/HUMAN EVIDENCE`.

**C4 Bounded composition:** default maximum = 3 mechanisms. Above 3 is invalid input in v0.1, not a soft recommendation.

**C5 Failure first:** missing prerequisites, contraindications, originality risk and locked-project mutation are hard rejection gates and are evaluated before ranking.

**C6 Baseline:** a gain claim requires an observable baseline/candidate comparison or a stronger explicit external evidence event. Missing/mismatched dimensions -> EVIDENCE_HOLD.

**C7 Protected dimensions:** a candidate cannot compensate for causality/canon/continuity/character-truth regression by gaining polish, novelty or retention.

**C8 Learning separation:** outcome feedback may alter future application readiness. It may not rewrite source claim, locator or canon.

**C9 Locked work:** locked work is SHADOW ONLY unless explicit Founder Unlock/New Failure Evidence authorizes reopening.

**C10 Promotion:** two-project success only opens PROMOTION_REVIEW_READY; actual universal promotion remains a Self-Improvement authority decision.

## 5. Protocols

### Protocol P-A — Live story use
1. Restore current project authority/freshness.
2. State the exact story problem.
3. Build StoryProblemSignature.
4. Query Book Intelligence/Mechanism Register problem-first.
5. Normalize candidates.
6. Run contraindication/originality gates.
7. Compose max 1–3.
8. Issue StoryMechanismPacket.
9. Apply only at authorized story layer.
10. Run existing Story/Character/Continuity/Reader/Red Team gates.
11. Compare observed result to baseline.
12. Persist outcome evidence.

### Protocol P-B — Library retrieval
Do not reread the library blindly. Retrieval is triggered by a decision-changing story problem. Prefer relevant sections/sources, then promote source lifecycle only when actually inspected.

### Protocol P-C — Failure/rollback
If candidate introduces FATAL/MAJOR, restore accepted baseline, record regression, lower application readiness, and do not alter source truth.

### Protocol P-D — Cross-project learning
A mechanism that works in one project is evidence, not universal law. Test on another independent project/genre before promotion review.

### Protocol P-E — Parallel work
Before persistence, fresh-read GitHub main and relevant Drive CURRENT pointers. Reuse stronger parallel work, replay only unique semantic delta, never force-overwrite.

## 6. Proofs produced this cycle
- Existing Book Intelligence Cycle1 architecture recognized and reused instead of duplicated.
- Existing Mechanism Portability Register recognized and reused instead of duplicated.
- New runtime candidate: `tools/ivdivo_story_mechanism_intelligence.py`.
- Deterministic local regression: **24/24 PASS**.
- Existing Business Pilot2 reused rather than duplicated.
- B03 locked shadow control: current Founder Lock forces `SHADOW_ONLY`; no manuscript mutation permitted.
- Fresh NASA deep-source work reused as upstream candidate evidence for V/V + traceability.
- Literary-quality gain remains unproven until an open story receives baseline/candidate application and reader/editor evidence where required.

## 7. Red Team
**FATAL 0. BLOCKING MAJOR 0** for the bounded engineering candidate.

MEDIUM / unresolved evidence:
1. Real literary-gain A/B pilot on an open story has not yet been run.
2. Human-reader/editor discrimination is not available and cannot be simulated.
3. Story-mechanism metadata coverage across the historical Drive library is incomplete by design; backfill must remain problem-targeted.
4. Mechanism interaction knowledge is initially sparse; explicit incompatibilities are safer than inferred synergy.
5. Lexicographic ranking is transparent but still only a routing heuristic; it must be calibrated from real outcomes.

## 8. Path to goal
Goal is not more prompts. Goal is a production learning loop:

`GOOGLE DRIVE BOOKS -> TRACEABLE CLAIMS -> ABSTRACT MECHANISMS -> PROBLEM-SPECIFIC SELECTION -> SAFE COMPOSITION -> ORIGINAL STORY APPLICATION -> STORY GATES -> OBSERVED RESULT -> LEARNING LEDGER -> BETTER FUTURE SELECTION`.

The next decisive story-quality gate is one **open, non-locked book/story problem** with a preserved baseline and a bounded mechanism packet. Retain the candidate only if it improves the intended story function without causality/character/continuity regression.
