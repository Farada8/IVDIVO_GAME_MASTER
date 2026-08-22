# BOOK INTELLIGENCE ENGINE — ALL-ENGINE ADAPTER CONTRACT v1.1

**Date:** 2026-08-22  
**Status:** ENGINEERING CURRENT CANDIDATE; supersedes v1.0 after current-state promotion.

## Call contract
Input:
`DOMAIN + ACTIVE_PROJECT + TASK/DECISION + CURRENT_AUTHORITY + PROTECTED_INVARIANTS + EVIDENCE_NEEDED`.

Book Intelligence returns:
- selected source IDs;
- exact claim/source locators;
- source state: integrity + read coverage + extraction stage;
- maximum 1–3 mechanisms by default;
- failure modes / contraindications / contradictions;
- AdapterPacket;
- verification plan;
- real validation requirement;
- rollback;
- traceability bundle;
- change-impact set when an existing rule is modified;
- whether fresh targeted source reading is needed.

## Universal adapter guards
1. `BOOK_MECHANISM_NEQ_DOMAIN_AUTHORITY`.
2. `ENGINEERING_VERIFICATION_NEQ_REAL_VALIDATION`.
3. `BIDIRECTIONAL_TRACEABILITY_REQUIRED_FOR_PROMOTION`.
4. `EXTRACTION_STAGE_NEQ_FULL_READ`.
5. `MAX_3_LOCAL_MECHANISMS_DEFAULT`.
6. `NO_NEW_EVIDENCE -> NO_GLOBAL_REWRITE`.
7. `DUPLICATE_SOURCE_COPY -> ZERO_NEW_INDEPENDENT_WEIGHT`.
8. `BASELINE_CHANGE -> CHANGE_IMPACT_SET -> WRITE_THROUGH -> READBACK`.
9. `LEGACY_UNCLASSIFIED_EVIDENCE -> DOES_NOT_COUNT_AS_REAL_VALIDATION`.
10. `PROMPT_COUNT_NEQ_PROGRESS`.

## STORY
`BOOK ENGINE -> STORY ADAPTER -> CURRENT STORY AUTHORITY`.
Book mechanisms can diagnose/open work but cannot silently reopen locked prose. Validate on actual causal/human/reader outcome, not tool score alone.

## AUDIO
`BOOK ENGINE -> AUDIO ADAPTER -> CURRENT AUDIO AUTHORITY`.
Book mechanisms can influence performance/sound/reliability design but cannot replace provider render, acoustic/QC evidence or human listener evidence.

## BUSINESS
`BOOK ENGINE -> BUSINESS ADAPTER -> CURRENT BUSINESS READ MODEL`.
Books can classify evidence, expose constraints and design tests. They cannot create current tender pack, bidder designation, buyer interaction, payment, PO, economics or market proof.

## SELF-IMPROVEMENT
`BOOK ENGINE -> SI CANDIDATE -> ENGINEERING VERIFICATION -> REAL PROJECT VALIDATION -> SECOND PROJECT -> PROMOTION/HOLD`.
Architecture work must prove incremental production value. Safe replication with zero incremental gain is not enough for universal promotion.

## RESEARCH
Use decision-first targeted retrieval. Maintain hypothesis/model/evidence/fact distinction and exact locators. A partial targeted source pass may support a bounded local mechanism without claiming FULL_READ.

## GAME / VISUAL / OPERATIONS / GENERAL
Use the same provenance and V/V contract, with domain-specific validation artifacts.

## Traceability minimum
For any mechanism proposed for reusable promotion:
`SOURCE -> SECTION -> CLAIM -> MECHANISM -> ADAPTER -> PROJECT_APPLICATION -> TEST -> RESULT` must pass end-to-end audit.
If promoted further:
`RESULT -> LEARNING -> ENGINE_RULE` must also be present.

## Change law
When a source claim, mechanism or engine rule changes, compute downstream impacted nodes first. Repair affected surfaces selectively; do not use change-impact analysis as permission for global rewrites.

## Default local-use algorithm
`RESTORE CURRENT AUTHORITY -> DEFINE DECISION -> BOOK ENGINE -> SELECT <=3 MECHANISMS -> DOMAIN ADAPTER -> EXECUTE REAL WORK -> VERIFY IMPLEMENTATION -> VALIDATE OUTCOME -> TRACE RESULT -> LEARNING OR HOLD`.