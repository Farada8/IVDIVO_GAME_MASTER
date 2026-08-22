# IVDIVO — BOOK INTELLIGENCE ENGINE v1.0

**Status:** CURRENT UNIVERSAL BOOK/REFERENCE GATEWAY — ENGINEERING v1.0  
**Established:** 2026-08-22  
**Repository:** `Farada8/IVDIVO_GAME_MASTER`  
**Purpose:** make every IVDIVO engine that uses books, manuals, papers, scripts or long-form references pass through one evidence-aware book intelligence layer instead of inventing its own ad-hoc reading/RAG workflow.

## 0. Authority boundary

This engine is a **reference-processing and learning infrastructure**, not story canon, business proof, scientific truth, legal authority, or permission to copy source expression.

Authority remains:

`FOUNDER -> LOCKED PROJECT/DOMAIN AUTHORITY -> PROJECT STATE -> BOOK INTELLIGENCE OUTPUT -> RAW REFERENCE`.

A book can inform a mechanism. It cannot silently override a locked project, factual evidence, live market evidence, human listener evidence, provider evidence or an explicit Founder decision.

## 1. Universal law

Every material use of a book/reference by an IVDIVO engine follows:

`REGISTER -> RIGHTS/ACCESS -> INTEGRITY -> STRUCTURE MAP -> CLAIMS + LOCATORS -> MECHANISMS -> FAILURE MODES -> CROSS-SOURCE COMPARISON -> SEMANTIC DEDUPE -> DOMAIN ADAPTER -> PROJECT PILOT -> REGRESSION -> PROMOTION/HOLD/REJECT -> WRITE-THROUGH`.

No engine may jump directly from `BOOK -> PROMPT/CANON`.

## 2. The problem this solves

Before v1.0, useful book-handling existed in several places:
- Narrative OS Reference Intelligence / Source Passports / Mechanism Banks;
- strict craft lifecycle;
- Business Engineering `LibraryAuthorityResolver`, `SourcePassportCompiler`, `FileIntegrityGate`, `MechanismExtractor`, `MechanismCrosswalk`, `ContradictionResolver`, `EvidenceCitationBinder`, `KnowledgeScopeFirewall`;
- Self-Improvement Learning Ledger;
- project-local reference packs.

Those components were valuable but distributed. The failure mode was **parallel book intelligence**: each engine could re-read, summarize, score or operationalize sources differently.

v1.0 changes the topology:

`RAW LIBRARY / OPEN WEB BOOKS`
→ **BOOK INTELLIGENCE ENGINE**
→ `STORY ADAPTER`
→ `AUDIO ADAPTER`
→ `BUSINESS ADAPTER`
→ `SELF-IMPROVEMENT ADAPTER`
→ `RESEARCH ADAPTER`
→ `GAME/VISUAL/OPERATIONS ADAPTERS`.

Existing domain modules remain valid implementations behind the gateway; they are not deleted or duplicated.

## 3. Core data objects

### 3.1 SourcePassport
Minimum:
- `source_id`
- `title`
- `author`
- `edition/year` when known
- `provenance`
- `content_locator`
- `rights_status`
- `independent_source_group`
- `lifecycle_stage`
- `domain_targets`
- `integrity_notes`
- `duplicate_of`
- `source_hash_or_revision` when available

Rights states:
`USER_PROVIDED | OPEN_LICENSE | PUBLIC_DOMAIN | ACCESS_ONLY | UNKNOWN`.

Rights and epistemic quality are separate. A user-provided copyrighted source can be analyzed, but is not automatically redistributable.

### 3.2 StructureMap
Captures:
- parts / chapters / appendices;
- conceptual dependency graph;
- definitions and terminology;
- claims;
- examples/cases;
- methods;
- tests/evaluation;
- limitations/counterexamples;
- bibliography/links.

A TOC is not a full read.

### 3.3 ClaimCard
Minimum:
- `claim_id`
- `source_id`
- `claim`
- exact locator: page/chapter/section/paragraph or stable URL fragment;
- `claim_type`: descriptive / normative / causal / empirical / formal / anecdotal;
- evidence strength;
- scope and assumptions;
- alternative interpretation;
- extraction confidence.

### 3.4 MechanismCard
Minimum:
- `mechanism_id`
- project-neutral mechanism statement;
- `source_ids`
- `semantic_key`
- evidence locators;
- assumptions;
- failure modes;
- contraindications;
- domain targets;
- distinctive source expression removed: boolean;
- pilot evidence;
- lifecycle disposition.

### 3.5 ContradictionSet
Books can conflict. Store:
- claim A;
- claim B;
- whether they actually address the same scope;
- evidence class;
- boundary conditions;
- resolution: `A_DOMINATES | B_DOMINATES | BOTH_CONDITIONAL | UNRESOLVED`.

Never average contradictions into vague advice.

### 3.6 AdapterPacket
The only normal interface from books into a production engine.

Fields:
- active domain/project/task;
- maximum 1–3 mechanisms by default;
- mechanism state (`PROMOTABLE`, `PILOT_READY`, `LOCAL_TEST`, etc.);
- evidence locators;
- application contract;
- failure modes;
- protected project invariants;
- test/rollback instruction.

## 4. Strict source lifecycle

Canonical stages:

1. `REGISTERED`
2. `INTEGRITY_VERIFIED`
3. `STRUCTURE_MAPPED`
4. `FULL_READ`
5. `CLAIMS_EXTRACTED`
6. `MECHANISMS_EXTRACTED`
7. `FAILURE_MODES_MAPPED`
8. `CROSS_SOURCE_COMPARED`
9. `OPERATIONALIZED`
10. `PROJECT_VALIDATED`
11. `SYNTHESIZED`

A source must not be labelled `FULL_READ`, `STRICT_COMPLETE`, `SYNTHESIZED` or equivalent unless the corresponding evidence exists.

Search snippets, model memory, publisher blurbs, table of contents, isolated chapter reads and summaries remain below `FULL_READ`.

## 5. Retrieval architecture

The default is **mechanism-first, source-second**.

For an active problem:
1. restore current project/domain state;
2. query current Mechanism Bank;
3. select at most 1–3 relevant mechanisms;
4. open raw sources only when the current extraction is insufficient, disputed, stale, or the decision could change;
5. stop research when another source is unlikely to change the decision and a project pilot is more informative.

The engine therefore avoids the failure mode `REREAD_ENTIRE_LIBRARY_EVERY_TURN`.

### Retrieval channels
- exact locator / heading / term;
- lexical retrieval;
- semantic retrieval;
- source-type filter;
- domain filter;
- lifecycle-stage filter;
- evidence-strength filter;
- contradiction query;
- negative evidence / failure-mode query.

Retrieval quality is evaluated separately from output quality.

## 6. Provenance graph

The engine maintains a graph, conceptually:

`SOURCE -> SECTION -> CLAIM -> MECHANISM -> ADAPTER_PACKET -> PROJECT_APPLICATION -> TEST -> RESULT -> LEARNING -> ENGINE_RULE`.

Each edge carries provenance. A result must be traceable backward to the source and forward to the production test.

Duplicate files point to the same source identity. Duplicate copies add **zero independent evidence weight**.

## 7. Cross-source rule

One book can generate a **candidate**. It does not gain universal authority by prestige.

For reusable rules:
- identify independent source groups;
- compare compatible claims;
- record contradictions;
- avoid counting translations, mirrors, later summaries or repeated model outputs as independent evidence;
- use project evidence as a separate evidence class.

`2 BOOKS AGREE != REAL PROJECT VALIDATION`.

## 8. Originality / copyright firewall

For creative sources:

`SOURCE -> ABSTRACT PRINCIPLE -> REMOVE PLOT/CHARACTER/SETTING/OBJECT/SCENE-ORDER/SIGNATURE LANGUAGE -> REBIND THROUGH CURRENT PROJECT -> SOURCE-DISTANCE CHECK`.

Never export source-specific protected expression into a project merely because the source is in the library.

For technical/business books:
- summarize mechanisms and constraints;
- retain attribution/provenance;
- do not redistribute raw copyrighted book binaries unless rights permit;
- user-provided/access-only source bytes remain outside GitHub.

GitHub stores metadata, schemas, mechanisms, tests and provenance — not copyrighted raw books.

## 9. Promotion lifecycle

Mechanism dispositions:

- `REFERENCE_ONLY` — source known, not ready for use;
- `LOCAL_TEST` — usable as a bounded hypothesis;
- `PILOT_READY` — passed one real project or has sufficient targeted evidence for a bounded pilot;
- `PROMOTABLE` — replicated with measurable net gain and no FATAL/MAJOR regression;
- `HOLD` — evidence incomplete or authority unclear;
- `REJECT` — harmful, invalid, derivative, contradictory without boundary, or failed regression.

Default universal promotion gate:

`VALID SOURCE PROVENANCE`
+ `PROJECT-NEUTRAL ABSTRACTION`
+ `NO DISTINCTIVE EXPRESSION`
+ `REAL PROJECT PASS #1`
+ `REAL INDEPENDENT PROJECT PASS #2`
+ `MEASURABLE OR CLEARLY OBSERVABLE NET GAIN`
+ `FATAL 0 / MAJOR 0`
→ `PROMOTABLE`.

Promotion still requires write-through to affected routers/config/prompts/tests. Document existence alone is not promotion.

## 10. Verification vs validation

The engine distinguishes:
- **verification:** did we implement the intended mechanism correctly?
- **validation:** did the mechanism improve the real target problem?

A perfect schema or passing unit test cannot prove a stronger story, better business, better audio or more truthful research.

## 11. Domain adapters

### STORY
Consumes mechanisms for causality, character, dialogue, suspense, POV, genre, style, reader cognition, etc.
Guard: Story First; no locked-book reopening without new failure evidence.

### AUDIO
Consumes performance, acoustics, sound dramaturgy, reliability/workflow mechanisms.
Guard: book evidence cannot simulate provider or human-listener evidence.

### BUSINESS
Consumes strategy, economics, constraints, experimentation, acquisition, measurement and operating-system mechanisms.
Guard: library knowledge cannot substitute for market/payment/bidder/customer evidence.

### SELF_IMPROVEMENT
Consumes architecture, reliability, decision, learning, evidence and workflow mechanisms.
Guard: meta-work must return to production and prove net gain.

### RESEARCH
Consumes scientific method, information retrieval, knowledge representation, reproducibility, uncertainty and evidence handling.
Guard: distinguish hypothesis, model, evidence and established fact.

### GAME / VISUAL / OPERATIONS
Use the same SourcePassport/MechanismCard/AdapterPacket contracts with domain-specific tests.

## 12. Architecture-change protocol

A book-derived idea can change engine architecture only through:

`OBSERVED LIMITATION`
→ `BOOK/REFERENCE EVIDENCE`
→ `ARCHITECTURE CANDIDATE`
→ `INTERFACE + INVARIANTS`
→ `UNIT/CONTRACT TEST`
→ `REAL DOMAIN PILOT`
→ `SECOND-DOMAIN/PERFORMANCE REGRESSION`
→ `PROMOTE OR ROLLBACK`.

Books may therefore help build architecture, but they do not directly rewrite architecture.

## 13. Mandatory engine contracts

1. `BOOK_GATEWAY_REQUIRED_FOR_MATERIAL_REFERENCE_USE`
2. `SOURCE_PASSPORT_REQUIRED`
3. `RIGHTS_AND_EVIDENCE_SEPARATED`
4. `NO_FALSE_FULL_READ`
5. `LOCATOR_REQUIRED_FOR_SOURCE_DERIVED_CLAIM`
6. `DUPLICATE_EVIDENCE_WEIGHT_ZERO`
7. `CONTRADICTION_NOT_AVERAGED`
8. `MECHANISM_ABSTRACTION_REQUIRED`
9. `DISTINCTIVE_EXPRESSION_FIREWALL`
10. `MAX_3_LOCAL_MECHANISMS_DEFAULT`
11. `MECHANISM_FIRST_RETRIEVAL`
12. `NO_LIBRARY_REREAD_BY_DEFAULT`
13. `DOMAIN_ADAPTER_REQUIRED`
14. `VERIFY_SEPARATE_FROM_VALIDATE`
15. `REAL_PROJECT_PILOT_REQUIRED_FOR_PROMOTION`
16. `SECOND_PROJECT_REPLICATION_FOR_UNIVERSAL_PROMOTION`
17. `FATAL_MAJOR_REGRESSION_FAIL_CLOSED`
18. `NO_BOOK_EVIDENCE_AS_MARKET_HUMAN_PROVIDER_PROOF`
19. `NO_LOCKED_PROJECT_REOPEN_WITHOUT_FAILURE_EVIDENCE`
20. `WRITE_THROUGH_AND_READBACK_REQUIRED`

## 14. Runtime

Current reference implementation:
`tools/ivdivo_book_intelligence.py`

Machine state:
`CURRENT_BOOK_INTELLIGENCE_ENGINE_STATE.json`

Source register:
`BOOK_INTELLIGENCE_ENGINE/01_SOURCE_LIBRARY_MANIFEST_v1.0.json`

Schema:
`BOOK_INTELLIGENCE_ENGINE/02_BOOK_INTELLIGENCE_SCHEMAS_v1.0.json`

32-pass prompt stack:
`BOOK_INTELLIGENCE_ENGINE/03_BOOK_INTELLIGENCE_PROMPT_STACK_32_v1.0.md`

Cycle-1 execution:
`BOOK_INTELLIGENCE_ENGINE/04_CYCLE1_32_PROMPTS_EXECUTION_REPORT_v1.0.md`

Integration contracts:
`BOOK_INTELLIGENCE_ENGINE/05_ALL_ENGINE_ADAPTER_AND_INTEGRATION_CONTRACT_v1.0.md`

## 15. Final rule

**A LIBRARY IS NOT MEMORY. A SUMMARY IS NOT KNOWLEDGE. A BOOK IS NOT CANON.**

The usable unit is:

`TRACEABLE SOURCE -> TESTABLE MECHANISM -> DOMAIN-SAFE ADAPTER -> REAL RESULT -> LEARNING`.
