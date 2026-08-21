# 02 — 32 PROMPTS EXECUTED — CYCLE 3

**Status:** 32/32 EXECUTED  
**Execution order:** 01 → 32 exactly as defined in Cycle-3 prompt stack.  
**Evidence:** S1–S7 from `01_SOURCE_EVIDENCE_MATRIX.md`.

---

## 01 — CERTAINTY WORD AUDIT
**Source:** BLOODBOUND E07 + LESSON ZERO forensic baseline.  
**Observation:** E07 contains strong restraint markers: `Maybe` and `We have a wording change. We do not yet have intent.` These correctly keep policy evidence separate from motive. Nia's earlier `They erased what the state was allowed to call them` is intentionally pulled back by Mira. In LESSON ZERO, the recurring precision/correction syntax increases risk that grammatical certainty becomes a stylistic reflex rather than evidence state.  
**Decision:** STRENGTHEN. Certainty must be tracked at claim level, but deliberate overconfidence is allowed if character-owned.  
**Engine delta:** add `EPISTEMIC_MODALITY_TAG = FACT / STRONG_INFERENCE / WEAK_INFERENCE / BELIEF / RHETORICAL_CONFIDENCE / WRONG_CONFIDENCE`.

## 02 — INFERENCE-AS-FACT DETECTOR
**Source:** BLOODBOUND E07.  
**Observation:** `Mira hated that she had already learned which of his silences meant patience and which meant surveillance` is vivid but grammatically close to certainty about Rian's internal meaning. Later `Now she heard restraint` more clearly marks interpretation. The episode generally avoids mind-reading, but the first line could become a template for disguised omniscience if repeated.  
**Decision:** ADD SOFT GATE. Do not automatically hedge every POV inference; require the prose to expose ownership of interpretation.  
**Engine delta:** `POV_INFERENCE_OWNER` field and regression question: `Did later evidence confirm/revise/leave unresolved this interpretation?`.

## 03 — DISCONFIRMING CUE REQUIREMENT
**Source:** BLOODBOUND E07.  
**Observation:** Mira worries because Rian does not defend the Council. A plausible disconfirming cue already exists: his family narrative has just destabilized, so silence can mean processing rather than guilt/alignment. The scene benefits when both readings remain available.  
**Decision:** PROMOTE as soft mystery/relationship gate.  
**Engine delta:** for high-confidence interpersonal judgments store `SUPPORTING_CUES[]` and `DISCONFIRMING_CUES[]`; zero disconfirming cues at a major ambiguous beat becomes a review flag.

## 04 — EPISTEMIC COMPRESSION WITHOUT CAVEAT DIALOGUE
**Source:** BLOODBOUND E07.  
**Observation:** the episode sometimes handles epistemic boundaries through dialogue (`not claimants`, `not intent`) and sometimes through behavior/state. The strongest moment is Tomas: Mira interrupts a polished correction ladder by sliding the circular toward him and asking for consequence. This proves clue-boundary discipline can move into action.  
**Decision:** KEEP + GENERALIZE.  
**Engine delta:** before adding a verbal caveat, test `STATE / ACTION / NARROWER QUESTION / SILENCE` alternatives. If one preserves fair-play logic, prefer it over repeated semantic corrections.

## 05 — WRONG-CONFIDENCE VALUE TEST
**Source:** BLOODBOUND E07.  
**Observation:** Nia's confident interpretation gives emotional force; Mira's correction keeps the investigation honest. If everyone stayed cautious, the scene would flatten. If Mira shared Nia's certainty, mystery fairness would break.  
**Decision:** ADD `DISTRIBUTED CONFIDENCE` law: different characters may hold different confidence levels about the same evidence.  
**Engine delta:** scene cards should include `CLAIM -> CHARACTER CONFIDENCE MAP`, not one global truthiness label.

## 06 — KNOWLEDGE SOURCE COLLISION
**Source:** BLOODBOUND E07.  
**Observation:** E07 is strong here. Rian owns inherited family teaching; Pela owns archive practice; Nia owns the working index; Tomas owns procedural practice; the circular and Council archivist provide documentary/institutional sources. These sources are not interchangeable and sometimes contradict.  
**Decision:** PROMOTE to universal high-risk scene gate.  
**Engine delta:** `SOURCE_PROVENANCE_GRAPH`: PERSON/DOCUMENT/SYSTEM -> CLAIM -> VERSION -> TRUST/BIAS -> WHO_RECEIVED_WHICH_VERSION.

## 07 — POV INTERPRETATION DEBT
**Source:** BLOODBOUND E07 + LESSON ZERO baseline.  
**Observation:** Mira interprets Rian's silence, smile and non-defense. If every such reading later proves correct, POV becomes covert omniscience. LESSON ZERO's observant characters have the same systemic risk.  
**Decision:** ADD HARD REGRESSION for recurring relationship/mystery interpretations.  
**Engine delta:** `INTERPRETATION_DEBT_LEDGER` with status `OPEN / CONFIRMED / REVISED / WRONG / ABANDONED`. Require nonzero revised/wrong interpretations over long-form work where uncertainty matters.

## 08 — MYSTERY EPISTEMIC REGRESSION
**Source:** BLOODBOUND causal grid + E07.  
**Observation:** E07 legitimately establishes: daughters continued under changed names; affinity is non-universal; postwar classification wording changed; Council minutes exist and are restricted. It does **not** establish intent, modern culprit, or Sabine's role. The script explicitly protects this boundary.  
**Decision:** PASS + PROMOTE.  
**Engine delta:** after each clue-heavy block compile `CHARACTER_KNOWLEDGE_BY_EPISODE_BOUNDARY`; later drafts cannot import future conclusions backward.

---

## 09 — ATTENTION BUDGET CARD
**Source:** BLOODBOUND E07.  
**Observation:** Tomas scene shows realistic selective attention: he routes through Rian, then fixes on the paper. Group workroom scenes are riskier because several competent people can appear to track every clue, emotional micro-signal and procedural detail simultaneously.  
**Decision:** ADD SOFT GATE for ensembles/high load.  
**Engine delta:** `ATTENTION_BUDGET` qualitative allocation across TASK / THREAT / BODY / RELATIONSHIP / STATUS / ENVIRONMENT / PRIVATE WORRY. Numbers are diagnostic only.

## 10 — MISSED-BUT-AVAILABLE FACT
**Source:** BLOODBOUND E07 + E08 handoff.  
**Observation:** Rian's family archive/chapel knowledge is not used in E07 even though his background plausibly gives him access. This is acceptable only if E08 provides a concrete trigger from the phrase/circular/Corven copy that re-anchors him to that source. Otherwise it would feel like delayed retrieval for plot convenience.  
**Decision:** ADD `RETRIEVAL_TRIGGER_REQUIRED` gate.  
**Engine delta:** every delayed use of previously available knowledge needs `WHY_NOT_NOW` + `WHAT_TRIGGERS_RETRIEVAL_LATER`.

## 11 — COGNITIVE LOAD SPEECH DISTORTION
**Source:** BLOODBOUND E07 + LESSON ZERO baseline.  
**Observation:** E07 is mostly controlled archival work; polished language is plausible. However even during emotionally destabilizing beats, Mira/Rian remain unusually syntactically clean. LESSON ZERO also risks maintaining clever precision under pressure.  
**Decision:** NEEDS MULTI-SCENE EVIDENCE; do not force fragments everywhere.  
**Engine delta:** character profile gets `STRESS_DEFORMATION`: shorter/longer, more formal, more repetitive, more literal, more silent, more sarcastic, etc.; later crisis scenes must show some owned deformation.

## 12 — RECALL FRICTION LADDER
**Source:** BLOODBOUND E07.  
**Observation:** E07 correctly relies on documents rather than miraculous memory. No major memory event justifies inserting artificial hesitation.  
**Decision:** KEEP AS CONDITIONAL GATE, NO TEXT CHANGE.  
**Engine delta:** for consequential remembered facts choose one of `INSTANT_EXACT / DELAYED_EXACT / PARTIAL / CONFIDENT_WRONG / UNCERTAIN_FRAGMENT`; default may remain exact when conditions genuinely support it.

## 13 — MEMORY CONTAMINATION TEST
**Source:** BLOODBOUND E07.  
**Observation:** Rian's `My family taught the clean version` is not personal memory of the historical event; it is inherited narrative. That distinction is excellent and should be explicit engine law.  
**Decision:** PROMOTE.  
**Engine delta:** memory/source types: `WITNESSED / REMEMBERED / RETOLD / INHERITED_NARRATIVE / DOCUMENT_DERIVED / RECONSTRUCTED_AFTER_DISCUSSION`.

## 14 — INTERRUPTED RETRIEVAL
**Source:** BLOODBOUND E07.  
**Observation:** no important retrieval currently needs interruption. Adding one merely to look natural would be decorative simulation.  
**Decision:** REJECT AS MANDATORY STYLE; retain as diagnostic option only.  
**Engine delta:** interruption may be used only when it changes retrieval or behavior and has a causal source.

## 15 — FATIGUE / PAIN INFORMATION LOSS
**Source:** BLOODBOUND E07.  
**Observation:** setting is a morning work session; severe fatigue/pain is not established. Degrading cognition here would invent state.  
**Decision:** NO CHANGE / CONTEXT-BOUND.  
**Engine delta:** human realism gate must first verify `BODY_STATE_EVIDENCE`; never add fatigue effects because a scene is dramatic.

## 16 — ATTENTION RE-ANCHOR TRIGGER
**Source:** BLOODBOUND E07.  
**Observation:** strong triggers already exist: new circular wording; Rian physically steps closer; Tomas's gaze shifts to paper; archivist pauses lengthen. These make attention shifts visible rather than author-directed.  
**Decision:** PROMOTE as positive-control pattern.  
**Engine delta:** important attention shift stores `TRIGGER = WORD / OBJECT / SOUND / MOVEMENT / SILENCE / STATUS_CHANGE / THREAT`.

---

## 17 — LIVE TRIGGER TRACE
**Source:** BLOODBOUND E07.  
**Observation:** most major replies attach to a live stimulus. Strong examples: Rian's `Read the next line` follows the circular; Mira's `Show me what happened after this line entered procedure` follows her detection of a polished exchange; final `architecture / decision` line is directly triggered by Rian's `Difference?`. A few witty/reframing lines (`Bad habit everywhere else`) are less necessary and more writer-shaped.  
**Decision:** PROMOTE `LIVE_TRIGGER_COVERAGE` as scene metric, not numeric pass/fail alone.  
**Engine delta:** every high-impact line must point to live stimulus, unresolved prior business, or internal processing; `OUTLINE_ONLY` origin is FAIL.

## 18 — EMOTIONAL LATENCY CURVE
**Source:** BLOODBOUND E07.  
**Observation:** Rian's family destabilization is well staged: silence/restraint -> family-clean-version admission -> physical margin gesture -> no cathartic naming. Mira/Rian attraction is likewise noticed, irritating, not declared.  
**Decision:** PASS / POSITIVE CONTROL.  
**Engine delta:** emotional scene cards may track `BODY -> TACTIC -> LEAK -> PRIVATE_RECOGNITION -> EXPLICIT_LANGUAGE`; not all stages must occur in one scene.

## 19 — LATENCY CHARACTER SIGNATURE
**Source:** BLOODBOUND E07 only + prior gate note.  
**Observation:** one episode cannot establish a robust character signature across three scenes. Current evidence suggests Mira verbalizes process errors relatively quickly but delays intimacy; Rian delays emotional naming and converts discomfort into task/legal questions.  
**Decision:** NEED MORE CORPUS.  
**Engine delta:** do not promote signature until at least 3 materially different scenes are sampled; store provisional profile meanwhile.

## 20 — DISPLACEMENT TARGET TEST
**Source:** BLOODBOUND E07.  
**Observation:** Mira repeatedly shifts emotional discomfort into categorization/task precision; Rian shifts family destabilization into document questions. Both displacements are character/role consistent and preserve human cost under competence.  
**Decision:** PROMOTE as optional naturalism enhancer for competence-heavy characters.  
**Engine delta:** `UNANSWERABLE_REAL_ISSUE -> SAFER_TARGET -> PROTECTIVE_FUNCTION`.

## 21 — ACTION-FIRST COMPETITION
**Source:** BLOODBOUND E07.  
**Observation:** several strong beats already act before speech: Rian steps closer, Tomas grips paper, Mira puts down pencil, Rian's jaw changes. The flirt-light `That was almost a joke / Do not make it one` is performance-sensitive; action-only could plausibly work but would change relationship texture.  
**Decision:** KEEP EXACT TEXT FOR NOW; mark selected polished lines for performance canary rather than automatic deletion.  
**Engine delta:** `ACTION_ONLY / ACTION+MIN_WORD / FULL_LINE` competition required only for high-risk polished beats.

## 22 — REPAIR STYLE STRESS TEST
**Source:** BLOODBOUND E07.  
**Observation:** Mira's repair `Sorry. That sounded like I was finishing the thought for you. ... Go on.` is functional and self-aware, but unusually explicit for a tense early relationship. It may be authentic to a forensic/process-minded person—or writerly emotional literacy.  
**Decision:** HOLD FOR A/B/PERFORMANCE.  
**Engine delta:** create repair-style profile per register. Candidate minimal alternative for testing only: `Sorry. I did that for you. Go on.` Do not replace without evidence.

## 23 — REPAIR CEILING TEST
**Source:** BLOODBOUND E07.  
**Observation:** repair does not create instant trust. Rian answers `You were`, then continues his own thought. Relationship status does not leap forward.  
**Decision:** PASS.  
**Engine delta:** every apology/repair gets `MAX_BELIEVABLE_IMMEDIATE_DELTA`; exceeding it without action/consequence is MAJOR naturalism risk.

## 24 — FAILED-REPAIR AFTERSHOCK
**Source:** BLOODBOUND E07.  
**Observation:** E07 contains a partial successful repair, not a failed one. The broader relationship still carries custody/surveillance tension. No reason to manufacture failure.  
**Decision:** CONDITIONAL ONLY.  
**Engine delta:** when repair fails, open `AFTERSHOCK_DEBT` for next 3 interactions; when repair succeeds partially, preserve unresolved relationship debts separately.

---

## 25 — CORRECTION-SYNTAX CORPUS SCAN
**Source:** BLOODBOUND E07 complete script + LESSON ZERO forensic counts.  
**Observation:** **CRITICAL FINDING.** E07 uses repeated contrastive/corrective forms across narrator and multiple speakers: `Not one surname. The moment...`; `Twelve people. Not twelve claimants.`; `That is a department.`; `Those are not opposites.`; `Not a confession. A limit.`; `Not because she was tired. Because...`; `No. The answer is...`; `less like a mistake... more like a choice`. This survives despite an explicit house-style watch in the script. LESSON ZERO independently showed repeated `That is... / That was not...` patterns.  
**Decision:** PROMOTE to **UNIVERSAL CORPUS HARD REVIEW GATE**.  
**Engine delta:** `CONTRASTIVE_SYNTAX_FINGERPRINT` by narrator and speaker. A line may remain, but unsupported cross-speaker concentration triggers targeted review.

## 26 — ACKNOWLEDGMENT PHRASE COLLISION
**Source:** BLOODBOUND E07 + LESSON ZERO forensic baseline.  
**Observation:** E07 uses `I know` for Nia and Mira in close proximity. LESSON ZERO has 94 `I know` matches. Neutral acknowledgments are semantically invisible but can erase speaker identity at scale.  
**Decision:** PROMOTE as corpus diagnostic.  
**Engine delta:** `ACKNOWLEDGMENT_FUNCTION_MATRIX`: AGREEMENT / DEFENSE / IMPATIENCE / SHAME / FACE-SAVING / CLOSURE / INVITATION. Track phrase + function by speaker; target function collisions, not raw frequency alone.

## 27 — REGISTER DISTANCE SCORECARD
**Source:** BLOODBOUND E07.  
**Observation:** role registers are reasonably differentiated: Mira forensic/task; Rian operational/legal; Tomas procedural-defensive; Pela archive-practical; Nia colleague/intimate shorthand. Mira/Rian intimate register is still emerging, so LOW–MEDIUM distance from professional speech is plausible now.  
**Decision:** PASS WITH WATCH.  
**Engine delta:** `REGISTER_DISTANCE = LOW/MEDIUM/HIGH` by pair/state; expected distance evolves with relationship arc and must not be judged against end-state intimacy too early.

## 28 — VOCABULARY BIOGRAPHY
**Source:** BLOODBOUND E07 + LESSON ZERO baseline.  
**Observation:** most technical vocabulary has life-source ownership. Mira's classification language, Rian's authority/ward language, Pela's archive language and Tomas's procedural phrasing are supported. The final `A locked room is architecture. A restricted record is a decision.` uses an architecture metaphor not obviously rooted in Mira's biography; it is elegant but may be author-owned. LESSON ZERO's `failing investment bank` joke has the same provenance question for a teenager.  
**Decision:** ADD `UNUSUAL_LANGUAGE_PROVENANCE` gate.  
**Engine delta:** unusual metaphor/term must be `BIOGRAPHY_SUPPORTED / SHARED_CULTURE / CONTEXT_GENERATED / AUTHOR_OWNED_CANDIDATE`.

## 29 — METAPHOR DOMAIN COLLISION
**Source:** BLOODBOUND E07 + LESSON ZERO baseline.  
**Observation:** E07 mostly stays within archive/law/paper/structure domains. `architecture` is a cross-domain spike. LESSON ZERO's finance metaphor is another spike. Cross-domain metaphor is not bad; unexplained recurrence across unrelated speakers is the problem.  
**Decision:** PROMOTE corpus-level metaphor ownership map as soft gate.  
**Engine delta:** per recurring character define owned/available metaphor domains; maintain narrator domains separately.

## 30 — STRESS DEFORMATION REGRESSION
**Source:** BLOODBOUND E07 + current context.  
**Observation:** E07 is moderate-pressure investigative work, not crisis. Language remains controlled, which is plausible. Evidence is insufficient to judge whether each speaker deforms under acute threat.  
**Decision:** NEEDS FUTURE CRISIS SAMPLE; no invented degradation.  
**Engine delta:** next BLOODBOUND block must sample calm vs high-pressure for Mira/Rian/Nia/Tomas before stress profile becomes authoritative.

## 31 — QUESTION-FAMILY SEPARABILITY
**Source:** BLOODBOUND E07.  
**Observation:** promising separability. Mira asks terse forensic extraction questions (`Date?`, `Results?`, `Meaning?`, `Names.`). Rian asks authority/procedure questions (`Duration?`, `Who renewed the restriction?`). Tomas mostly answers/deflects; Nia asks collaborative clarification. This is stronger than vocabulary-only differentiation.  
**Decision:** PASS + PROMOTE BLIND TEST.  
**Engine delta:** maintain `QUESTION_FAMILY_PROFILE` and run name-stripped samples at block gates.

## 32 — DISAGREEMENT-FAMILY SEPARABILITY
**Source:** BLOODBOUND E07 + LESSON ZERO baseline.  
**Observation:** Mira disagrees through narrowing/reclassification; Rian often disagrees through restraint or procedural question; Tomas through procedural defense; Nia through emotional/intellectual push. However the narrator and speakers share too much contrastive syntax, partially collapsing this difference.  
**Decision:** PARTIAL PASS.  
**Engine delta:** separate `TACTIC_IDENTITY` from `SURFACE_SYNTAX`. A scene can have distinct tactics but still sound authored by one rhetorical hand.

---

# 32/32 EXECUTION SUMMARY

## Strong positive controls
- distributed confidence rather than universal caution;
- source provenance separation;
- mystery knowledge boundary protection;
- physical/sensory attention triggers;
- emotional latency without instant therapeutic naming;
- action-first beats;
- relationship repair ceiling;
- question-family differentiation.

## Strongest new defect evidence
1. **Contrastive/corrective syntax collision across narrator + multiple speakers.**
2. **Neutral acknowledgement collision (`I know`) across characters and across books.**
3. **Elegant metaphor provenance risk** (`architecture`, `investment bank`) where wording may be author-owned unless biography/relationship/performance earns it.
4. Scene-level naturalism notes do not by themselves prevent corpus-level convergence.

## No-change findings matter too
Prompts 12, 14, 15, 24, 30 did **not** justify adding artificial hesitation, interruptions, fatigue, failed repairs or stress fragmentation. Naturalism is not noise injection.

## Promotion principle derived
`DO NOT ASK ONLY: WOULD A PERSON SAY THIS?`

Ask:
`WHY THIS PERSON -> FROM THIS SOURCE -> NOTICING THIS CUE -> UNDER THIS LOAD -> USING THIS TACTIC -> IN THIS REGISTER -> WITH THIS RHETORICAL HABIT -> SAYS THIS NEXT, AND DOES THE CORPUS STILL SOUND LIKE DIFFERENT PEOPLE?`
