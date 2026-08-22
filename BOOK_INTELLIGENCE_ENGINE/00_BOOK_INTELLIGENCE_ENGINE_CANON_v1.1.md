# IVDIVO — BOOK INTELLIGENCE ENGINE v1.1

**Status:** CURRENT ENGINEERING CANDIDATE — IMPLEMENTED / PROTOTYPE 9/9 PASS / EXACT REPOSITORY CI NOT YET OBSERVED  
**Established:** 2026-08-22  
**Supersedes for current Book Intelligence routing after state promotion:** `00_BOOK_INTELLIGENCE_ENGINE_CANON_v1.0.md`  
**Purpose:** one evidence-aware gateway for material use of books, manuals, papers, scripts and long-form references across IVDIVO engines.

## 0. Authority boundary
Book Intelligence is reference-processing infrastructure, not story canon, business/market proof, scientific truth, legal authority or permission to copy protected expression.

`FOUNDER -> LOCKED PROJECT/DOMAIN AUTHORITY -> PROJECT STATE -> BOOK INTELLIGENCE OUTPUT -> RAW REFERENCE`.

A book can generate a candidate mechanism. It cannot override locked project state, current factual evidence, market/customer/payment evidence, human listener evidence, provider evidence or Founder decisions.

## 1. Universal route
`REGISTER -> RIGHTS/ACCESS -> INTEGRITY -> READ COVERAGE -> CLAIM + LOCATOR -> MECHANISM -> FAILURE MODES -> CROSS-SOURCE COMPARISON -> SEMANTIC DEDUPE -> DOMAIN ADAPTER -> PROJECT APPLICATION -> VERIFICATION + VALIDATION -> RESULT -> LEARNING -> WRITE-THROUGH`.

No material path `BOOK -> PROMPT/CANON` is allowed.

## 2. Orthogonal source state
v1.0 used one linear lifecycle and incorrectly implied that extracted mechanisms required a cover-to-cover full read. v1.1 separates three dimensions.

### integrity_status
`UNKNOWN | VERIFIED | FAILED | QUARANTINED`

### read_coverage
`NONE | STRUCTURE_ONLY | PARTIAL_TARGETED | FULL_READ`

### extraction_stage
`NONE | CLAIMS_EXTRACTED | MECHANISMS_EXTRACTED | FAILURE_MODES_MAPPED | CROSS_SOURCE_COMPARED | OPERATIONALIZED | PROJECT_VALIDATED | SYNTHESIZED`

Hard laws:
- `EXTRACTION_STAGE DOES NOT IMPLY FULL_READ`.
- targeted extraction may use `PARTIAL_TARGETED` when exact locators exist;
- claims/mechanisms require at least `PARTIAL_TARGETED` + locator;
- failed/quarantined sources cannot support mechanisms;
- legacy `lifecycle_stage` is compatibility metadata, not the current epistemic model;
- `FULL_READ`, `STRICT_COMPLETE` and equivalent labels require direct evidence and are never inferred from source prestige, summaries, TOCs or extraction state.

## 3. SourcePassport
Required current fields:
- source_id
- title
- provenance
- rights_status
- independent_source_group
- integrity_status
- read_coverage
- extraction_stage

Use author/edition/year/content locator/license/hash/structure map/claim IDs/mechanism IDs when available.

Rights states:
`USER_PROVIDED | OPEN_LICENSE | PUBLIC_DOMAIN | ACCESS_ONLY | UNKNOWN`.

Rights and epistemic status are separate. User-provided copyrighted sources may be analyzed in the authorized workspace but are not redistributed by default.

## 4. Claim and mechanism objects
A source-derived ClaimCard needs a stable locator, scope, claim type, assumptions/evidence status and extraction confidence.

A MechanismCard must be project-neutral before reuse and preserve:
- source IDs and evidence locators;
- semantic key;
- failure modes/contraindications;
- domain targets;
- confirmation that distinctive source expression was removed;
- pilot evidence classified by evidence class;
- disposition and rollback/application contract.

Contradictory sources remain explicit `ContradictionSet`s. Do not average disagreement into generic advice.

## 5. Retrieval law
Default is **mechanism-first, source-second, decision-first**.

For a real problem:
1. restore the current project/domain authority;
2. define the decision and evidence capable of changing it;
3. query current mechanisms;
4. select maximum 1–3 for local application unless a larger set is explicitly justified;
5. perform fresh targeted source reading only where existing extraction is insufficient, disputed, stale or decision-relevant;
6. stop when another source has lower information value than a real pilot.

`BOOK COUNT != KNOWLEDGE` and `PROMPT COUNT != PROGRESS`.

## 6. Verification != Validation
Evidence classes:
- `ENGINEERING_VERIFICATION`
- `REAL_PROJECT_VALIDATION`
- `HUMAN_VALIDATION`
- `PROVIDER_VALIDATION`
- `MARKET_VALIDATION`
- `FACTUAL_SPECIALIST_VALIDATION`
- `LEGACY_UNCLASSIFIED`

Engineering verification proves conformance of implementation. It does not prove intended-use value.

Only real validation classes can count toward reusable-mechanism promotion. Legacy unclassified evidence is not silently promoted; it must be classified from actual artifacts.

Examples:
- unit/contract tests ≠ better story;
- CI PASS ≠ market demand;
- dry audio render ≠ human listener validation;
- source inspection ≠ factual specialist validation;
- model vote ≠ customer/payment evidence.

## 7. Bidirectional traceability
Canonical trace:
`SOURCE -> SECTION -> CLAIM -> MECHANISM -> ADAPTER -> PROJECT_APPLICATION -> TEST -> RESULT -> LEARNING -> ENGINE_RULE`.

Promotion requires:
- backward trace from result/rule to source/claim/mechanism;
- forward trace from source-derived mechanism to actual application/test/result;
- no orphan edges;
- relation endpoint types must match;
- end-to-end result must be reachable from a source when the bundle claims end-to-end provenance.

Runtime: `audit_traceability_bundle()`.

## 8. Change impact
Before modifying a baseline mechanism, contract or source-derived rule:
1. identify changed node(s);
2. compute downstream descendants with `change_impact_set()`;
3. inspect affected adapters/projects/tests/learnings/rules;
4. apply the smallest justified change;
5. verify and read back all required controlling surfaces.

This does not authorize global rewrites. It prevents partial write-through and stale routers.

## 9. Originality / copyright firewall
Creative transfer:
`SOURCE -> ABSTRACT PRINCIPLE -> REMOVE DISTINCTIVE PLOT/CHARACTER/SETTING/SCENE ORDER/SIGNATURE LANGUAGE -> REBIND THROUGH ACTIVE PROJECT -> SOURCE-DISTANCE CHECK`.

Technical/business transfer:
- store mechanisms/constraints/provenance;
- do not copy raw copyrighted binaries into GitHub;
- do not treat source possession as redistribution permission.

Duplicate copies add zero independent evidence weight.

## 10. Domain adapter contract
The normal production interface is an AdapterPacket:
- domain/project/task;
- max 1–3 mechanisms by default;
- disposition/evidence locators;
- protected invariants;
- failure modes;
- application/test/rollback;
- traceability requirement.

Guards:
- Story: no locked-book reopening without new failure evidence.
- Audio: book evidence cannot simulate provider/listener evidence.
- Business: book knowledge cannot become live bidder/tender/customer/payment/market evidence.
- Self-Improvement: architecture change requires bounded pilot and real outcome.
- Research: separate hypothesis/model/evidence/established fact.
- Game/Visual/Operations: same provenance contract with domain-specific validation.

## 11. Promotion lifecycle
Dispositions:
`REFERENCE_ONLY | LOCAL_TEST | PILOT_READY | PROMOTABLE | HOLD | REJECT`.

Default reusable promotion gate:
`VALID PROVENANCE`
+ `PROJECT-NEUTRAL ABSTRACTION`
+ `NO DISTINCTIVE EXPRESSION`
+ `REAL VALIDATION PROJECT #1`
+ `REAL VALIDATION PROJECT #2`
+ `MEASURABLE OR CLEARLY OBSERVABLE GAIN`
+ `FATAL 0 / MAJOR 0`
+ `TRACEABILITY PASS`
→ `PROMOTABLE`.

Engineering verification alone may support `LOCAL_TEST`; it cannot satisfy real-validation gates.

## 12. Current evidence
Cycle 1: 32/32 prompts executed, with 26 engineering passes and 6 evidence holds; no fabricated FULL_READ.

Pilot 1 / Story: real production benefit — stale B03 frontier was detected and current CH25–29/P72 lineage recovered, preventing duplicate prose work.

Pilot 2 / Business: cross-domain safety replication PASS but no incremental decision gain — Book Intelligence correctly preserved `PROTECT_NO_CHANGE` and did not convert library knowledge into tender/market evidence.

NASA Systems Engineering targeted deep-source pass exposed the v1.0 lifecycle defect and produced the v1.1 V/V + traceability upgrade. It is `PARTIAL_TARGETED`, not `FULL_READ`.

Prototype v1.1 deterministic regression: 9/9 PASS. Exact repository CI remains a separate evidence class and must be observed before claiming exact-repo verification.

## 13. Current artifacts
- source register: `BOOK_INTELLIGENCE_ENGINE/01_SOURCE_LIBRARY_MANIFEST_v1.1.json`
- schema: `BOOK_INTELLIGENCE_ENGINE/02_BOOK_INTELLIGENCE_SCHEMAS_v1.1.json`
- runtime: `tools/ivdivo_book_intelligence.py`
- regression tests: `BOOK_INTELLIGENCE_ENGINE/tests/test_book_intelligence_v1_1.py`
- CI: `.github/workflows/book-intelligence-v1-1.yml`
- NASA deep source: `BOOK_INTELLIGENCE_ENGINE/08_NASA_SYSTEMS_ENGINEERING_DEEP_SOURCE_PASS_v1.0.md`
- upgrade contract: `BOOK_INTELLIGENCE_ENGINE/09_ORTHOGONAL_SOURCE_LIFECYCLE_AND_TRACEABILITY_UPGRADE_v1.1.md`
- machine state: `CURRENT_BOOK_INTELLIGENCE_ENGINE_STATE.json`

## 14. Final law
**A LIBRARY IS NOT MEMORY. A SUMMARY IS NOT KNOWLEDGE. A BOOK IS NOT CANON. A TEST PASS IS NOT VALIDATION.**

Usable knowledge is:
`TRACEABLE SOURCE -> LOCATED CLAIM -> TESTABLE MECHANISM -> DOMAIN-SAFE APPLICATION -> REAL RESULT -> CLASSIFIED LEARNING`.