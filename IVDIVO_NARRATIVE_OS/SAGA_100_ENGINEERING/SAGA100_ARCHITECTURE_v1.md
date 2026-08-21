# IVDIVO SAGA100 — LONG-HORIZON ARCHITECTURE v1.0

**Status:** FOUNDER-DIRECTED WORKING ARCHITECTURE / NOT A RETCON OF LOCKED BOOKS  
**Date:** 2026-08-21  
**Scope:** one IVDIVO saga/universe, scalable toward 100 complete novels without padding.

## 1. Founder macro-law

The saga is one evolving universe, not three unrelated franchises.

Default long-run unit:

`SMITH/OES -> ORBITAL -> CONFEDERATION/FRONTIER -> CROSSING`

Three books must each work as independent complete novels. The fourth is a consequence-driven shared novel in which the three civilizational lenses collide because one problem genuinely crosses lives, knowledge, rights, institutions or jurisdictions.

Target scale: up to **25 cycles x 4 books = 100 books**. This is a capacity target, never a quota that justifies weak stories.

## 2. Philosophical/civilizational function

Every cycle has one `CIVILIZATION_QUESTION` and tests it at four distances.

### SMITH / OES lens — inherited matrices
Shows what humanity brings from the old world through professional practice: security, investigation, classification, secrecy, law, bureaucracy, force, institutional memory, old agreements, hidden knowledge, rights, mistakes and responsibility. Smith remains a professional human character, not an exposition device. Philosophy changes perception and choice but does not solve the case.

Required cycle output: `OLD_MATRIX_EXPOSED`, `PROFESSIONAL_PRICE`, `HUMAN_RIGHTS_TENSION`, `UNRESOLVED_LIMIT`.

### ORBITAL lens — next achievable human step
Shows what humans can plausibly build next: habitats, work, money, housing, education, family, relationships, transport, law, citizenship, AI/synthetic persons, body/neurorights, maintenance, culture, status, enterprise and politics. The future must be lived, not catalogued.

Required cycle output: `NEXT_STEP_IMPLEMENTED`, `OLD_ERROR_CARRIED`, `NEW_INSTITUTION_OR_PRACTICE`, `NEW_HUMAN_COST`.

### CONFEDERATION / FRONTIER lens — farther possibility
Shows a mature civilization with wider possibilities: embodiment, multiple body classes, distributed identity, advanced AI/synthetic life, nonhuman cultures, post-scarcity domains where earned, new forms of work, education, responsibility, law, consent and exploration. It must never be a perfect utopia; capability does not erase conflict, limits or ethics.

Required cycle output: `FAR_POSSIBILITY_SHOWN`, `CONFEDERATION_LIMIT`, `INTERNAL_DISAGREEMENT`, `HUMAN_COMPARISON_WITHOUT_SERMON`.

### CROSSING lens — synthesis under pressure
Does not assemble a permanent super-team by default. It creates one complete problem that requires interaction among inherited Earth matrices, Orbital institutions/life and Confederation knowledge/actors. Knowledge is not jurisdiction; capability is not authority.

Required cycle output: `CROSS_LINE_DEPENDENCY_PROVEN`, `JURISDICTION_CONFLICT`, `SYNTHESIS_CHOICE`, `CIVILIZATION_DELTA_LOCKED`.

## 3. Do not destructively renumber existing books

Existing B01–B08 project IDs predate the new 25x4 scheduler and contain historical routing conflicts. Therefore introduce a second non-destructive coordinate system:

- `PROJECT_ID` = existing durable project identity, e.g. B02, B03, B07, B08.
- `SAGA_SLOT_ID` = long-horizon slot, e.g. `S100-C01-S`, `S100-C01-O`, `S100-C01-C`, `S100-C01-X`.

No existing project is renumbered until `LegacySequenceReconciler` emits an evidence-backed mapping and Founder/project authority accepts it.

## 4. Engine modules

1. **AuthorityResolver** — resolves Founder/project/canon/current/working/superseded layers fail-closed.
2. **LegacySequenceReconciler** — maps existing Bxx projects into SAGA100 slots without retcon.
3. **SagaCycleCompiler** — creates one four-book cycle contract from a civilization question.
4. **LineFunctionRouter** — assigns S/O/C/X responsibilities and prevents functional duplication.
5. **CivilizationProgressionLedger** — tracks what humanity/Orbit/Confederation know, possess, can manufacture, may legally use and use in ordinary life.
6. **PhilosophicalQuestionCompiler** — converts abstract questions into human decisions, professional conflicts, relationships and prices.
7. **ProfessionalMatrixEngine** — Smith-specific catalogue of old-world professional matrices and their evolution.
8. **OrbitalTransitionEngine** — converts near-future change into lived institutions, jobs, infrastructure and ordinary life.
9. **ConfederationPossibilityEngine** — generates farther possibilities with limits, internal disagreement and non-utopian constraints.
10. **CrossingNecessityCompiler** — permits X-books only when at least two line-specific dependencies and one jurisdiction/rights conflict are irreducible.
11. **HumanProblemSelector** — story begins from recognizable human pain/desire rather than lore.
12. **BookIndependenceGate** — requires complete hero arc, main conflict closure and reader satisfaction per book.
13. **ConsequenceLedger** — persists injuries, relationships, knowledge, status, law, technology, institutional changes and unpaid prices.
14. **ContinuitySubstitutionMatrix** — substitutes real upstream consequences into future architecture before prose.
15. **RelationshipBridgeGraph** — tracks friendships, romance, family, mentor/student and rivalries across world boundaries.
16. **JurisdictionCapabilityMatrix** — separates knowledge/capability/access/manufacture/legal authority/current jurisdiction.
17. **TechnologyAccessLadder** — prevents Confederation capability from instantly becoming ordinary human technology.
18. **RevealBudgetManager** — controls cosmology/ontology reveal ceilings per cycle.
19. **GenerationalHandoffManager** — permits characters to age and new generations to enter without reset.
20. **NoRepeatVectorizer** — compares human problem, arena, protagonist position, genre emphasis, amplifier, closure and relationships.
21. **CivilizationDeltaProofEngine** — proves each book changed at least one durable world variable through story.
22. **CrossingRegressionGate** — checks that a crossover does not erase independence of S/O/C lines.
23. **BookStateMachine** — IDEA -> DISCOVERY -> ARCHITECTURE -> STORY_GATE -> PROSE -> DEVELOPMENT -> FINAL_GATE -> LOCK -> DOWNSTREAM.
24. **CycleStateMachine** — QUESTION -> S/O/C planned -> each line closed -> X eligible -> X closed -> cycle delta lock -> next cycle.
25. **PortfolioScheduler** — selects next book from dependencies, maturity, diversity and evidence rather than numeric sequence alone.
26. **ReferenceMechanismMinerAdapter** — consumes existing Source Passports/Mechanism Bank/Reference Intelligence without copying plots.
27. **ProofPackager** — emits machine-readable PASS/FAIL evidence for book/cycle gates.
28. **RegressionRunner** — reruns only descendants affected by an accepted change.
29. **PersistenceMirrorProtocol** — GitHub canonical candidate + Drive working mirror + readback verification.
30. **CrossConversationFreshnessGuard** — prevents old aggregate state from overriding newer project authority.
31. **SelfImprovementEvidenceBridge** — sends observed failures/improvements to existing Self-Improvement v2 as candidates; never promotes automatically.
32. **LongHorizonDriftDetector** — detects philosophical repetition, power inflation, lore inflation, protagonist flattening and civilization jumps without earned bridges.

## 5. Core engineering contracts

### C-S100-01 — Cycle contract
Inputs: `cycle_id`, `civilization_question`, current continuity snapshot, unresolved consequences, capability/jurisdiction state, relationship graph, reveal ceiling.

Outputs: four line briefs S/O/C/X, distinct human problems, required civilization deltas, dependency graph, proof obligations, no-repeat vectors.

FAIL if: the question can only be answered by exposition; S/O/C tell the same story; X is fan-service-only; required upstream continuity is unknown and outcome depends on it.

### C-S100-02 — Book independence contract
Every book must contain `HERO/WANT/WHY_NOW/OPPOSITION/WRONG_STRATEGY/PRICE/MIDPOINT/CLIMAX_CHOICE/RESOLUTION/CHANGE`.

FAIL if its main conflict exists only to tee up the next book.

### C-S100-03 — Civilization progression contract
A future capability may move only through explicit states:

`EXISTS_ELSEWHERE -> KNOWN -> CONTACT_ACCESS -> RESTRICTED_USE -> LOCAL_PROTOTYPE -> LEGALIZED_USE -> SCALABLE_MANUFACTURE -> ORDINARY_LIFE`.

Skipping states requires story evidence and a recorded exception.

### C-S100-04 — Crossing eligibility contract
A crossing is eligible only when:
- all prerequisite line books are locally closed;
- actual consequences are loaded;
- at least two line-specific competencies are necessary;
- at least one conflict cannot be solved by simply granting the most advanced actor command authority;
- Confederation knowledge does not silently equal jurisdiction;
- resolution changes the shared civilization state.

### C-S100-05 — Self-improvement bridge contract
A saga-engine observation enters Self-Improvement as:
`OBSERVATION -> CANDIDATE -> EVIDENCE -> PROOF_RUN -> REGRESSION -> ACCEPT/HOLD/REJECT -> PROMOTION`.

Forbidden: auto-canonization, auto-promotion from model agreement, treating repeated copies as independent evidence.

## 6. Proof obligations

Every book/cycle can generate these proofs:

- `P-S100-BI` Book Independence Proof.
- `P-S100-HP` Human Problem First Proof.
- `P-S100-PM` Smith Professional Matrix Proof when S-line.
- `P-S100-OT` Orbital Next-Step Realism Proof when O-line.
- `P-S100-CP` Confederation Possibility + Limit Proof when C-line.
- `P-S100-XN` Crossing Necessity Proof when X-line.
- `P-S100-JC` Jurisdiction/Capability Separation Proof.
- `P-S100-CD` Civilization Delta Proof.
- `P-S100-CC` Consequence Carry Proof.
- `P-S100-NR` No-Repetition Proof.
- `P-S100-RB` Relationship Bridge Proof.
- `P-S100-PH` Philosophy Through Action Proof.
- `P-S100-RG` Selective Regression Proof after changes.
- `P-S100-PS` Persistence + Readback Proof.

## 7. Long-horizon progression model

Do not pre-write 100 plots. Pre-design **25 civilization questions / developmental thresholds** with flexible order. Each threshold receives four novels only when story evidence supports them.

Possible threshold families, not locked plots:
1. personhood;
2. autonomy/consent;
3. memory/identity;
4. ownership/access;
5. death/continuity;
6. family/parenthood;
7. work/value;
8. education/competence;
9. privacy/neural rights;
10. justice/security;
11. citizenship/migration;
12. synthetic persons;
13. embodiment/body choice;
14. AI agency;
15. distributed identity;
16. scarcity/post-scarcity boundaries;
17. governance/representation;
18. cultural belonging;
19. contact/nonintervention;
20. ecological personhood;
21. planetary/orbital sovereignty;
22. interspecies obligations;
23. frontier responsibility;
24. legacy/generational accountability;
25. mature synthesis / next unknown frontier.

These are sequencing candidates; actual cycle order must be consequence-driven.

## 8. Existing assets reused rather than replaced

- NARR-009 70-book multiline plan -> `SEED_BANK / HUMAN_PROBLEM_BANK / WAVE_MODEL`.
- Narrative OS / Book Workroom / 100-person studio -> production and specialist routing.
- Story Engine v4.1 / Source Passports / Mechanism Bank / Crosswalk -> mechanism intelligence.
- current project states -> higher authority for actual books.
- Self-Improvement v2 / Improvement Registry / proof-run pattern -> evidence-based engine evolution.
- Audio Production Engine -> downstream adaptation after text lock; not allowed to mutate story authority silently.

## 9. Stop/fail-closed rules

Stop a book/cycle compile on: Founder decision, authority ambiguity, unresolved FATAL/MAJOR, missing upstream consequence that changes motive/outcome, required human/external evidence, or unavailable source bytes.

Do not stop merely because the next engineering step is obvious. Continue through unblocked dependencies and persist the resulting state.

## 10. Immediate implementation path

1. persist this architecture and machine contracts;
2. execute Cycle32 research/engineering prompts;
3. derive corrections from the 32 results;
4. create 64 next run cards;
5. reconcile existing B01–B08 into non-destructive SAGA_SLOT candidates;
6. build first 25-question Civilization Progression Map without locking 100 plots;
7. run diversity and continuity proof;
8. only then promote accepted elements into higher Narrative OS/Saga Bible authority.
