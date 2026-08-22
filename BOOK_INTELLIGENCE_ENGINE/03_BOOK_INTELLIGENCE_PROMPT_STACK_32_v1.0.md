# IVDIVO — BOOK INTELLIGENCE ENGINE — 32-PROMPT STACK v1.0

**Status:** EXECUTABLE ENGINEERING PROMPT PROGRAM  
**Established:** 2026-08-22  
**Rule:** execute against verified source access; never manufacture full-read status or source claims.

Each pass returns:
`INPUTS / OBSERVATIONS / EVIDENCE LOCATORS / DECISIONS / NEW OBJECTS / REJECTED OR HELD / TEST / NEXT`.

## PHASE A — SOURCE INTAKE, RIGHTS, INTEGRITY

### P01 — Library Inventory Resolver
Inventory all relevant book/reference files and access endpoints. Cluster duplicate files/editions/translations. Assign stable `source_id`. Do not count duplicate copies as independent evidence.

### P02 — Rights + Access Boundary
For each source classify `USER_PROVIDED / OPEN_LICENSE / PUBLIC_DOMAIN / ACCESS_ONLY / UNKNOWN`. Separate permission to analyze from permission to redistribute. Produce a no-redistribution list.

### P03 — File Integrity + Identity Gate
Verify title/author/edition/file type and basic readability where tool access permits. Quarantine broken, placeholder, partial, encrypted or uncertain files instead of treating them as studied.

### P04 — Lifecycle Truth Audit
Assign the highest evidenced lifecycle stage only. Downgrade any source whose stated status exceeds actual evidence. Explicitly distinguish TOC-mapped, partial-read and full-read.

## PHASE B — STRUCTURE AND CLAIM EXTRACTION

### P05 — Structure Map Compiler
Map parts/chapters/appendices, conceptual dependencies, definitions, examples, methods, tests and limitations. Produce a StructureMap, not a generic summary.

### P06 — Question-to-Section Router
Given an active project question, select only the sections most likely to change the decision. Return why each section is relevant and why omitted sections are not currently needed.

### P07 — Claim Extractor with Locators
Extract only decision-relevant claims. Bind every source-derived claim to a stable page/chapter/section/URL locator and classify the claim type.

### P08 — Scope + Assumption Extractor
For every important claim identify population/context/scale/time assumptions and boundary conditions. Block universalization of claims with unbounded scope.

## PHASE C — MECHANISMS, FAILURE MODES, CONTRADICTIONS

### P09 — Mechanism Abstraction
Convert claims into project-neutral mechanisms. Remove names, signature examples, source-specific terminology and protected expression.

### P10 — Failure-Mode Miner
For each mechanism ask when it fails, when it is harmful, what prerequisite it assumes and what signal should stop its use.

### P11 — Counterexample Search
Search the same source and current library for counterexamples or explicit limitations. Record negative evidence rather than maximizing supportive evidence.

### P12 — Contradiction Resolver
Compare conflicting claims at matching scope. Resolve as `A_DOMINATES / B_DOMINATES / BOTH_CONDITIONAL / UNRESOLVED`; never average a real contradiction into vague advice.

### P13 — Semantic Dedupe
Cluster equivalent mechanisms across books, editions, mirrors, summaries and model outputs. Preserve provenance but give duplicate repetition zero independent evidence weight.

### P14 — Independent Evidence Grouper
Assign sources to independent evidence groups. Treat translation, mirror, derivative summary, same experiment, same author chain or common primary source as potentially dependent.

### P15 — Source-Distance / Originality Gate
For creative sources verify that plot, characters, setting, objects, scene order, signature phrasing and signature inventions have been stripped before use.

### P16 — Mechanism Bank Update Candidate
Produce normalized MechanismCards with semantic keys, evidence locators, failure modes, domain targets and lifecycle disposition. Do not promote yet.

## PHASE D — RETRIEVAL / KNOWLEDGE ARCHITECTURE

### P17 — Retrieval Architecture Design
Design exact, lexical, semantic, metadata, contradiction and failure-mode retrieval channels. Keep retrieval quality measurable and separate from generation quality.

### P18 — Retrieval Evaluation Fixture
Create representative queries with expected relevant sources/mechanisms. Define precision/recall-style or task-success acceptance checks appropriate to the library.

### P19 — Relevance Feedback Loop
Use project outcomes and reviewer feedback to improve retrieval ranking/query expansion without changing source claims. Keep feedback lineage.

### P20 — Provenance Graph Compiler
Build the graph `SOURCE -> SECTION -> CLAIM -> MECHANISM -> ADAPTER -> PROJECT -> TEST -> RESULT -> LEARNING -> RULE`. Require every promoted rule to have a backward trace.

## PHASE E — DOMAIN ADAPTERS

### P21 — Story Adapter
Map only relevant mechanisms into causality/character/dialogue/POV/suspense/style tasks. Default max 1–3 mechanisms. Preserve Story First and locked-book boundaries.

### P22 — Audio Adapter
Map performance/acoustic/workflow mechanisms into Audio. Block book evidence from substituting for real provider, render or human-listener evidence.

### P23 — Business Adapter
Map strategy/economics/constraint/measurement mechanisms into Business Engineering. Block book evidence from substituting for market, bidder, payment or customer proof.

### P24 — Self-Improvement Adapter
Map architecture/reliability/decision/reproducibility mechanisms into Self-Improvement. Require bounded pilots and return to production; no recursive prompt factory.

### P25 — Research Adapter
Map evidence/retrieval/knowledge-representation/uncertainty mechanisms into Research. Distinguish hypothesis/model/evidence/established fact.

### P26 — Game/Visual/Operations Adapter
Create shared adapter contract for remaining engines. Rebind only project-neutral mechanisms and define domain-specific acceptance evidence.

## PHASE F — ARCHITECTURE CHANGE + REAL VALIDATION

### P27 — Architecture Gap Detector
Compare current engine interfaces to supported mechanisms. Propose a new module only where an observed limitation cannot be solved by an existing component/adapter.

### P28 — Architecture Candidate Contract
For each real gap define interface, inputs/outputs, invariants, failure modes, migration impact, rollback and tests before implementation.

### P29 — Verification Gate
Verify that code/schema/router implements the architecture candidate as designed. Unit/contract PASS is implementation evidence only.

### P30 — Real Project Validation Gate
Pilot on one real project against a baseline. Measure whether the actual target problem improves; classify FATAL/MAJOR regressions separately.

### P31 — Second-Project Replication + Promotion
Repeat on an independent project/domain. Promote universal mechanisms only after two-project replication or an explicitly stronger evidence path; otherwise keep `PILOT_READY/HOLD`.

### P32 — Write-Through / Current-State Closure
Write accepted mechanisms through to current routers/config/prompts/tests/learning state, read back the result, record invalidations, and set the highest unblocked next obligation. Do not count the existence of this report as promotion.

## Operating macro

For future book use, engines call:

`RESTORE PROJECT -> BOOK ENGINE ROUTE -> SELECT 1–3 MECHANISMS -> DOMAIN ADAPTER -> EXECUTE PROJECT WORK -> TEST -> RETURN RESULT TO BOOK/LEARNING LEDGER`.

The Book Intelligence Engine is therefore a gateway and learning compiler, not a separate content-generation bureaucracy.
