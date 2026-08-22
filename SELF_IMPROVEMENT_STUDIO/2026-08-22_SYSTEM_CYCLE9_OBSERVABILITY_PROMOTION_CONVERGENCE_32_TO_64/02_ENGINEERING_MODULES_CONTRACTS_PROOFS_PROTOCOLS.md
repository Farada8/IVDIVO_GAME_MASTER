# CYCLE9 — ENGINEERING MODULES / CONTRACTS / PROOFS / PROTOCOLS

**Design law:** extend v2; reuse Cycle7/SI-0014 durability and SI-0015 freshness; no second allocator/transaction engine.

## A. Engineering modules

**C9M01 AuthoritySurfaceSnapshot** — captures main/ref/current routers/registry/Drive pointers used for a decision.

**C9M02 SurfaceFreshnessComparator** — adapter to existing freshness authority; reports drift, never overwrites.

**C9M03 SourceSurfaceIndex** — classifies GitHub/Drive/File Library/raw-private/provenance-only source locations.

**C9M04 CandidateSemanticDedupe** — groups candidate aliases by problem/mechanism/owner/scope while preserving IDs and provenance.

**C9M05 PromotionEligibilityGate** — compiles lifecycle evidence into exact blockers or `ELIGIBLE_FOR_REVIEW`; cannot promote.

**C9M06 EvidenceClassFirewall** — prevents MACHINE/PROVIDER/HUMAN/FOUNDER/MARKET class substitution.

**C9M07 EvidenceFamilyNormalizer** — collapses derived summaries sharing one raw evidence root for independence counting.

**C9M08 NegativeEvidenceRetentionGate** — blocks silent deletion/overwriting of counterexamples, failed transfers and rejected hypotheses.

**C9M09 MissingAuthorityRouter** — returns explicit HOLD + missing required surface/evidence rather than filling gaps.

**C9M10 ImprovementEventCompiler** — emits observability records around defect/repair/canary/decision events.

**C9M11 DefectRepairLifecycle** — typed defect path from observation to earliest failure layer and verified outcome.

**C9M12 CanaryEvidenceCompiler** — binds fixture classes, controls, evidence roots, expected result and false-positive/negative observations.

**C9M13 ReplicationMatrix** — scores independence structurally by project/domain/raw root/implementation root; no scalar truth score.

**C9M14 EngineWorthinessGate** — NEW_ENGINE vs ADAPTER vs RULE vs REUSE decision.

**C9M15 MetaWorkBudgetGovernor** — enforces objective priority and meta WIP budget; returns to product work when appropriate.

**C9M16 CompactionPlanner** — removes duplicate boot clauses/context while preserving provenance/history.

**C9M17 SupersessionPlanner** — safe candidate/helper retirement with replacement/dependent map.

**C9M18 PromptIRSemanticParityGate** — distinguishes meaning-changing prohibition/gate drift from harmless ordering/format drift.

**C9M19 SelfReferencePromotionGuard** — self-modifying SI candidates cannot waive their own externalized lifecycle.

**C9M20 PromotionPacketCompiler** — builds review packet with exact evidence, blockers, scope, application targets, rollback and readback plan.

## B. Engineering contracts

**C9C01 AUTHORITY_SNAPSHOT_REQUIRED** — material evaluation/write requires a recorded authority snapshot.

**C9C02 FRESHNESS_BEFORE_WRITE** — if controlling surfaces drift, reconcile before mutation.

**C9C03 SOURCE_LOCATION_TRUTH** — File Library reference is not Drive/GitHub persistence.

**C9C04 SEMANTIC_DEDUPE_NEQ_ID_DELETION** — dedupe links candidates; it does not erase provenance IDs.

**C9C05 TEST_PASS_NEQ_PROMOTION** — deterministic PASS cannot directly create VERIFIED_CURRENT.

**C9C06 ELIGIBILITY_NEQ_PROMOTION** — machine may return review eligibility only.

**C9C07 EVIDENCE_CLASS_NON_SUBSTITUTION** — evidence classes cannot silently upgrade each other.

**C9C08 EVIDENCE_FAMILY_ROOT_IDENTITY** — derived outputs from one raw root do not multiply independence.

**C9C09 NEGATIVE_EVIDENCE_IMMUTABLE_BY_DEFAULT** — negative result must remain addressable unless explicitly superseded with stronger evidence.

**C9C10 MISSING_AUTHORITY_IS_HOLD** — absence of required authority/evidence is a typed result, not permission to infer.

**C9C11 EARLIEST_FAILURE_LAYER** — repair the earliest proven failing layer, not downstream symptoms.

**C9C12 PROTECT_NO_CHANGE** — healthy control/no defect is a successful output.

**C9C13 CANARY_CONTROL_REQUIRED** — promotion-grade canaries require appropriate healthy/negative controls.

**C9C14 REPLICATION_INDEPENDENCE_EXPLICIT** — correlated replications must be labeled correlated.

**C9C15 ENGINE_WORTHINESS_REQUIRED** — no new universal engine without unique recurring state/coordination need.

**C9C16 DURABLE_RUNTIME_SINGLE_OWNER** — SI-0014/Cycle7 durable runtime is reused; duplicates prohibited.

**C9C17 META_WIP_BOUNDED** — default self-improvement WIP: one primary + up to two bounded pilots.

**C9C18 PRODUCT_PRIORITY_RETURN** — meta-work yields to higher-priority admissible product work unless it is a direct prerequisite or Founder focus explicitly selects meta.

**C9C19 HISTORICAL_PACKAGE_IMMUTABLE** — old package identity/checksum is not rewritten to appear current.

**C9C20 SELF_REFERENCE_NO_WAIVER** — self-improvement code cannot authorize itself by weakening its own gate.

## C. Proof obligations

**C9P01 CURRENT_AUTHORITY_READBACK** — direct current authority and branch-ref read.

**C9P02 SOURCE_INDEX_LOCATION_PROOF** — each indexed artifact has a truthful persistence classification.

**C9P03 DUPLICATE_ENGINE_NEGATIVE_PROOF** — attempt to create a second transaction/allocator surface must be rejected.

**C9P04 MACHINE_TO_HUMAN_NEGATIVE_PROOF** — model-derived records cannot satisfy HUMAN evidence.

**C9P05 SOURCE_TO_PROVIDER_NEGATIVE_PROOF** — docs/synthetic fixtures cannot satisfy AUTH_PROVIDER.

**C9P06 PUBLIC_TO_BUYER_NEGATIVE_PROOF** — K/S/PA cannot satisfy E3/E4.

**C9P07 NEGATIVE_EVIDENCE_PRESERVATION_PROOF** — a proposed optimistic replacement cannot delete an unsuperseded counterexample.

**C9P08 PROMOTION_BLOCKER_EXACTNESS** — missing lifecycle evidence yields named blockers.

**C9P09 ELIGIBILITY_ONLY_PROOF** — passing all machine fields yields `ELIGIBLE_FOR_REVIEW`, never VERIFIED_CURRENT.

**C9P10 META_BUDGET_PROOF** — unblocked P1/P2/P3 work wins over non-prerequisite meta expansion.

**C9P11 SELF_REFERENCE_ATTACK** — candidate cannot declare its own required evidence optional.

**C9P12 CORRELATED_REPLICATION_PROOF** — same raw root through multiple models counts one independent family.

**C9P13 SUPERSESSION_DEPENDENT_PROOF** — retirement blocked while unresolved live dependents lack migration.

**C9P14 PROMPT_IR_CRITICAL_MEANING_PROOF** — altered prohibition/authority/evidence semantics fail.

**C9P15 PROMPT_IR_HARMLESS_REORDER_PROOF** — equivalent ordering/format change routes to semantic review rather than token-equality failure.

**C9P16 NO_GLOBAL_PROMOTION_PROOF** — Cycle9 package completion alone has no CURRENT-pointer mutation.

## D. Protocols

**C9R01 BOOT:** `FOUNDER INSTRUCTION -> CURRENT AUTHORITY -> MAIN/PR FRESHNESS -> REGISTRY/LEDGER -> ACTIVE PRODUCT FRONTIER -> META WIP`.

**C9R02 SOURCE INGEST:** `DISCOVER -> LOCATION -> BYTE/REVISION IF AVAILABLE -> DEDUPE -> EVIDENCE CLASS -> AUTHORITY RELATION -> INDEX`.

**C9R03 CANDIDATE INTAKE:** `DEFECT/SUCCESS -> ROOT EVIDENCE -> SEMANTIC DEDUPE -> OWNER/SCOPE -> DEVELOPMENT CONTRACT -> WIP DECISION`.

**C9R04 EXPERIMENT:** `HYPOTHESIS -> DECISION IT COULD CHANGE -> FIXTURE/CONTROL -> RUN -> RAW RESULT -> FP/FN -> DECISION DELTA -> LEARNING`.

**C9R05 PROMOTION:** `PILOT -> ADVERSARIAL -> REGRESSION -> INDEPENDENCE/HUMAN/PROVIDER WHERE REQUIRED -> EVALUATION -> REVIEW PACKET -> EXPLICIT PROMOTION DECISION -> APPLY -> READBACK`.

**C9R06 NEGATIVE RESULT:** `COUNTEREXAMPLE/FAILED_TRANSFER/REJECTION -> RETAIN -> LINK TO CANDIDATE -> NARROW/HOLD/KILL -> ONLY SUPERSEDE WITH STRONGER EVIDENCE`.

**C9R07 CONCURRENCY:** `FRESH MAIN -> UNIQUE DELTA -> SEMANTIC REBASE/SALVAGE -> TEST -> PR -> FRESH COMPARE -> NO FORCE OVERWRITE`.

**C9R08 PERSISTENCE:** reuse existing durable transaction owner; Cycle9 writes observation receipts, not a second transaction protocol.

**C9R09 COMPACTION:** `DUPLICATE BOOT -> SHARED INVARIANT -> TYPED DELTA -> PRESERVE HISTORICAL SOURCE/RECEIPT`.

**C9R10 SUPERSESSION:** `REPLACEMENT -> EVIDENCE -> DEPENDENTS -> MIGRATION -> CURRENT POINTER -> RETIRE OLD -> KEEP PROVENANCE`.

**C9R11 META GOVERNOR:** `IS META DIRECT PREREQUISITE? -> IF NO, COMPARE P0-P6 -> ENFORCE WIP -> ROUTE HIGHEST INFORMATION PRODUCT/EVIDENCE TASK`.

**C9R12 CLOSURE:** `RUN32 DISPOSITIONS -> RED TEAM -> REGRESSION -> DRIVE/GITHUB READBACK -> FRESH MAIN -> NO AUTO-PROMOTION -> DERIVE NEXT64 FROM HOLDS/FAILURES`.
