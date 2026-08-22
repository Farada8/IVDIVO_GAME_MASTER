# CYCLE4 CONVERGENCE — ENGINEERING MODULES / CONTRACTS / PROOFS / PROTOCOLS

## New bounded modules
These extend Cycle3/Cycle4 convergence control. They are **not a second top-level Business Engine**.

### G-CX01 NamespaceCollisionGate
Input: proposed namespace+semantic owner, current/open/Drive claims.  
Output: PASS or `HOLD_NAMESPACE_COLLISION`.  
Law: same numeric/string ID cannot silently bind two semantic owners; no auto-rename.

### G-CX02 ConcurrentAuthorityRestore
Input: expected/observed main SHA, relevant open-PR heads, library physical count, Drive CURRENT pointer.  
Output: `PASS_FRESH_AUTHORITY_SNAPSHOT` or HOLD with drift map.  
Law: substantial writes stop on authority drift.

### G-CX03 LibraryDeltaAfterCycleGate
Input: prior/current physical counts + enumerated new file IDs.  
Output: closure allowed only when arithmetic delta is fully enumerated.  
Observed canary: 69→78 requires exactly 9 distinct delta IDs.

### G-CX04 DatasetNeqEngine
Input: evidence-object count, persistence, unique runtime-contract flag.  
Output: ADAPTER/EVIDENCE_PACK or ENGINE_REVIEW_CANDIDATE.  
Law: persistence/size cannot auto-promote a dataset to core.

### G-CX05 OpportunityRootDedupe
Specification-only this cycle. Dedupes by recurring buyer job + decision artifact, never title/category similarity. Preserves source-row lineage and legal/domain rule boundaries.

### G-CX06 GenericConsultingKillGate
Specification-only. If a candidate lacks repeatable input schema, evidence object, decision output and falsifiable public observable, mutate to a concrete artifact job or KILL.

## Engineering contracts

**CCX01 SOURCE_PLANE_FIREWALL**  
K/S/E/D/T planes cannot substitute for one another.

**CCX02 RAW_PRIVATE_DERIVED_PUBLIC**  
Copyrighted source binaries remain private Drive; GitHub receives derived metadata/hashes/passports only.

**CCX03 PHYSICAL_NEQ_WORK**  
`physical_file != byte_hash != edition_alias != canonical_work`. Canonical count may remain null.

**CCX04 DUPLICATE_ZERO_ADDITIONAL_WEIGHT**  
Exact-byte duplicate sources contribute zero incremental evidence weight.

**CCX05 BROKEN_ZERO_EVIDENCE**  
Placeholder/corrupt files remain quarantined and cannot satisfy K1+.

**CCX06 NAMESPACE_SEMANTIC_IDENTITY**  
Namespace + semantic contract defines global identity; integer availability does not.

**CCX07 CONCURRENT_FRESHNESS_BEFORE_WRITE**  
Fresh main/open-PR/Drive/library reconciliation precedes substantial writes and closure.

**CCX08 DATASET_NEQ_ENGINE**  
Opportunity/result corpus is evidence; engine status requires a unique reusable runtime contract and review.

**CCX09 HYPOTHESIS_NEQ_TRUTH**  
Every business mechanism/opportunity remains falsifiable until the appropriate evidence plane passes.

**CCX10 VOI_BEFORE_ACTIVITY**  
Choose the cheapest observation likely to change the decision; volume of research is not progress by itself.

**CCX11 WIP_LIMIT**  
Active opportunity WIP stays ≤3 until an explicit authority changes it.

**CCX12 UNKNOWN_REMAINS_NULL**  
Price, conversion, WTP, margin, CAC, finance approval and legal clearance stay null when not measured.

**CCX13 ROOT_JOB_NOT_TITLE**  
Opportunity dedupe uses buyer workload/decision artifact, not similar names/categories.

**CCX14 SHARED_PRIMITIVE_NEQ_SHARED_MARKET**  
Reuse of SupplierEvidence/Eligibility/Deadline/etc. does not merge buyer segments or regulatory regimes.

**CCX15 PUBLIC_ARTIFACT_NEQ_BUYER_PROOF**  
A strong sample deliverable can prove execution capability and information structure, not willingness-to-pay.

**CCX16 NO_GENERIC_CONSULTING_OBJECT**  
Generic consulting is not a root workload unless converted to repeatable evidence inputs and a decision artifact.

## Proof obligations

**PCX01 LIBRARY78_PROOF** — 69+9=78 with 58 unique valid hashes, 8 exact duplicate groups, 5 quarantined placeholders; canonical unique works null.

**PCX02 MOM_TEST_ALIAS_PROOF** — new physical Mom Test has exact known duplicate SHA and adds zero evidence weight.

**PCX03 SOURCE_GROUNDING_PROOF** — source passports distinguish direct text-supported mechanisms from inference/reference-only status.

**PCX04 NAMESPACE_NEGATIVE_CANARY** — proposed B81/Public colliding with B81/Shillelagh must HOLD.

**PCX05 FRESH_MAIN_NEGATIVE_CANARY** — changed main SHA must HOLD before write.

**PCX06 LIBRARY_DELTA_NEGATIVE_CANARY** — 69→78 with only eight enumerated delta IDs must HOLD.

**PCX07 DATASET_PERSISTENCE_NEGATIVE_CANARY** — 64 persisted objects with no unique runtime contract remain evidence/adapters.

**PCX08 PR173_SUPERSESSION_PROOF** — a fresh PR-state read must override stale plan to renamespace/merge the whole branch; salvage only after supersession.

**PCX09 WIP_PROOF** — active root registry has exactly R01/R02/R05, with R04 reserve.

**PCX10 EVIDENCE_CEILING_PROOF** — all 64 input opportunity objects remain ≤ public evidence ceiling; no E3/E4 introduced by dedupe.

## Protocols

### P-CX01 FRESHNESS-RECONCILE-WRITE
1. read current main authority;
2. read matching open PRs;
3. read Drive CURRENT/library pointers;
4. run authority restore guard;
5. only then write;
6. rerun before merge/closure.

### P-CX02 SOURCE-PASSPORT
`FILE ID + HASH -> READABLE TEXT -> DIRECTLY SUPPORTED CLAIMS -> ABSTRACT MECHANISM -> BUSINESS USE -> FORBIDDEN INFERENCE -> STATUS`.

### P-CX03 LIBRARY-DELTA
`PRIOR PHYSICAL COUNT -> ENUMERATE NEW FILE IDs -> BYTE HASH/QUARANTINE -> DUPLICATE WEIGHT -> CURRENT COUNT -> READBACK`.

### P-CX04 OPPORTUNITY-ROOT
`SOURCE ROWS -> BUYER JOB -> DECISION ARTIFACT -> SHARED PRIMITIVES -> DOMAIN RULES -> FATAL ASSUMPTION -> PUBLIC OBSERVABLE -> EVIDENCE CEILING -> WIP`.

### P-CX05 GENERIC-KILL
`GENERIC OFFER -> REPEATABLE INPUT? -> EVIDENCE OBJECT? -> DECISION OUTPUT? -> FALSIFIABLE OBSERVABLE?`; if any essential answer is no, MUTATE once or KILL.

### P-CX06 SELF-IMPROVEMENT-DISCOVERY
Record `DEFECT -> ROOT CAUSE -> REPAIR -> RETEST -> RESULT -> REUSE CONDITIONS`; never allocate/promote SI authority merely because a rule sounds sensible.

## Tests
`tests/test_convergence_guards.py` contains 10 deterministic canaries for collision, authority drift, dataset/core separation and library delta closure. CI also runs existing procurement/capital and public-signal regressions.
