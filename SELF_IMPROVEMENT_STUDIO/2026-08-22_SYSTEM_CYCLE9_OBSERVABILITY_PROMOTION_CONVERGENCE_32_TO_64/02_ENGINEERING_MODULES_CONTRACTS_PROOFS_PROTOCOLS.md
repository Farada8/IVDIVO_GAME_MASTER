# CYCLE9 — ENGINEERING MODULES / CONTRACTS / PROOFS / PROTOCOLS

**Design law:** extend v2; reuse Cycle7/SI-0014 durability and SI-0015 freshness; no second allocator/transaction engine.

## A. Engineering modules
**C9M01 AuthoritySurfaceSnapshot** — captures main/ref/current routers/registry/Drive pointers used for a decision.
**C9M02 SurfaceFreshnessComparator** — adapter to existing freshness authority; reports drift, never overwrites.
**C9M03 SourceSurfaceIndex** — classifies GitHub/Drive/File Library/raw-private/provenance-only locations.
**C9M04 CandidateSemanticDedupe** — groups aliases by problem/mechanism/owner/scope while preserving IDs/provenance.
**C9M05 PromotionEligibilityGate** — exact blockers or `ELIGIBLE_FOR_REVIEW`; cannot promote.
**C9M06 EvidenceClassFirewall** — prevents evidence-class substitution.
**C9M07 EvidenceFamilyNormalizer** — collapses derived summaries sharing one raw root for independence counting.
**C9M08 NegativeEvidenceRetentionGate** — blocks silent loss of counterexamples/failed transfers/rejections.
**C9M09 MissingAuthorityRouter** — explicit HOLD + missing dependency, never invented completion.
**C9M10 ImprovementEventCompiler** — typed observability records around defects/repairs/canaries/decisions.
**C9M11 DefectRepairLifecycle** — observation -> earliest failing layer -> verified outcome.
**C9M12 CanaryEvidenceCompiler** — fixture/control/evidence-root/FP/FN/decision-delta binding.
**C9M13 ReplicationMatrix** — project/domain/raw-root/implementation-root independence model.
**C9M14 EngineWorthinessGate** — NEW_ENGINE vs ADAPTER vs RULE vs REUSE.
**C9M15 MetaWorkBudgetGovernor** — P0–P6 priority + meta WIP + return-to-product.
**C9M16 CompactionPlanner** — removes duplicate boot/context while preserving provenance/history.
**C9M17 SupersessionPlanner** — safe retirement with replacement/dependent map.
**C9M18 PromptIRSemanticParityGate** — meaning-changing prohibition/gate drift vs harmless order/format drift.
**C9M19 SelfReferencePromotionGuard** — self-modifying SI cannot waive externalized lifecycle.
**C9M20 PromotionPacketCompiler** — evidence, blockers, scope, targets, rollback and readback in one review packet.

## B. Engineering contracts
**C9C01 AUTHORITY_SNAPSHOT_REQUIRED** — material evaluation/write requires recorded authority snapshot.
**C9C02 FRESHNESS_BEFORE_WRITE** — reconcile drift before mutation.
**C9C03 SOURCE_LOCATION_TRUTH** — File Library reference is not Drive/GitHub persistence.
**C9C04 SEMANTIC_DEDUPE_NEQ_ID_DELETION** — dedupe links; provenance IDs remain.
**C9C05 TEST_PASS_NEQ_PROMOTION** — deterministic PASS cannot create VERIFIED_CURRENT.
**C9C06 ELIGIBILITY_NEQ_PROMOTION** — machine returns review eligibility only.
**C9C07 EVIDENCE_CLASS_NON_SUBSTITUTION**.
**C9C08 EVIDENCE_FAMILY_ROOT_IDENTITY**.
**C9C09 NEGATIVE_EVIDENCE_IMMUTABLE_BY_DEFAULT**.
**C9C10 MISSING_AUTHORITY_IS_HOLD**.
**C9C11 EARLIEST_FAILURE_LAYER**.
**C9C12 PROTECT_NO_CHANGE** — healthy/no-defect is a successful result.
**C9C13 CANARY_CONTROL_REQUIRED**.
**C9C14 REPLICATION_INDEPENDENCE_EXPLICIT**.
**C9C15 ENGINE_WORTHINESS_REQUIRED**.
**C9C16 DURABLE_RUNTIME_SINGLE_OWNER** — SI-0014/Cycle7 owner reused.
**C9C17 META_WIP_BOUNDED** — one primary + up to two bounded pilots by default.
**C9C18 PRODUCT_PRIORITY_RETURN**.
**C9C19 HISTORICAL_PACKAGE_IMMUTABLE**.
**C9C20 SELF_REFERENCE_NO_WAIVER**.

## C. Proof obligations
**C9P01 CURRENT_AUTHORITY_READBACK**.
**C9P02 SOURCE_INDEX_LOCATION_PROOF**.
**C9P03 DUPLICATE_ENGINE_NEGATIVE_PROOF**.
**C9P04 MACHINE_TO_HUMAN_NEGATIVE_PROOF**.
**C9P05 SOURCE_TO_PROVIDER_NEGATIVE_PROOF**.
**C9P06 PUBLIC_TO_BUYER_NEGATIVE_PROOF**.
**C9P07 NEGATIVE_EVIDENCE_PRESERVATION_PROOF**.
**C9P08 PROMOTION_BLOCKER_EXACTNESS**.
**C9P09 ELIGIBILITY_ONLY_PROOF**.
**C9P10 META_BUDGET_PROOF**.
**C9P11 SELF_REFERENCE_ATTACK**.
**C9P12 CORRELATED_REPLICATION_PROOF**.
**C9P13 SUPERSESSION_DEPENDENT_PROOF**.
**C9P14 PROMPT_IR_CRITICAL_MEANING_PROOF**.
**C9P15 PROMPT_IR_HARMLESS_REORDER_PROOF**.
**C9P16 NO_GLOBAL_PROMOTION_PROOF**.

## D. Protocols
**C9R01 BOOT:** `FOUNDER INSTRUCTION -> CURRENT AUTHORITY -> MAIN/PR FRESHNESS -> REGISTRY/LEDGER -> ACTIVE PRODUCT FRONTIER -> META WIP`.
**C9R02 SOURCE INGEST:** `DISCOVER -> LOCATION -> BYTE/REVISION IF AVAILABLE -> DEDUPE -> EVIDENCE CLASS -> AUTHORITY RELATION -> INDEX`.
**C9R03 CANDIDATE INTAKE:** `DEFECT/SUCCESS -> ROOT EVIDENCE -> SEMANTIC DEDUPE -> OWNER/SCOPE -> DEVELOPMENT CONTRACT -> WIP DECISION`.
**C9R04 EXPERIMENT:** `HYPOTHESIS -> DECISION IT COULD CHANGE -> FIXTURE/CONTROL -> RUN -> RAW RESULT -> FP/FN -> DECISION DELTA -> LEARNING`.
**C9R05 PROMOTION:** `PILOT -> ADVERSARIAL -> REGRESSION -> INDEPENDENCE/HUMAN/PROVIDER WHERE REQUIRED -> EVALUATION -> REVIEW PACKET -> EXPLICIT PROMOTION DECISION -> APPLY -> READBACK`.
**C9R06 NEGATIVE RESULT:** `COUNTEREXAMPLE/FAILED_TRANSFER/REJECTION -> RETAIN -> LINK -> NARROW/HOLD/KILL -> SUPERSEDE ONLY WITH STRONGER EVIDENCE`.
**C9R07 CONCURRENCY:** `FRESH MAIN -> UNIQUE DELTA -> SEMANTIC REBASE/SALVAGE -> TEST -> PR -> FRESH COMPARE -> NO FORCE OVERWRITE`.
**C9R08 PERSISTENCE:** reuse existing durable transaction owner; Cycle9 writes observation receipts only.
**C9R09 COMPACTION:** `DUPLICATE BOOT -> SHARED INVARIANT -> TYPED DELTA -> PRESERVE HISTORY/RECEIPT`.
**C9R10 SUPERSESSION:** `REPLACEMENT -> EVIDENCE -> DEPENDENTS -> MIGRATION -> CURRENT POINTER -> RETIRE OLD -> KEEP PROVENANCE`.
**C9R11 META GOVERNOR:** `IS META DIRECT PREREQUISITE? -> IF NO, COMPARE P0-P6 -> ENFORCE WIP -> ROUTE HIGHEST-INFORMATION PRODUCT/EVIDENCE TASK`.
**C9R12 CLOSURE:** `RUN32 -> RED TEAM -> REGRESSION -> DRIVE/GITHUB READBACK -> FRESH MAIN -> NO AUTO-PROMOTION -> DERIVE NEXT64 FROM HOLDS/FAILURES`.
