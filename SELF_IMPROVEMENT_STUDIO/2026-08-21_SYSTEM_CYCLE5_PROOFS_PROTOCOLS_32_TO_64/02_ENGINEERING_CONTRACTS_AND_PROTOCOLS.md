# CYCLE 5 — ENGINEERING CONTRACTS + PROTOCOLS

**Status:** WORKING / PILOT / NOT CURRENT AUTHORITY.  
All contracts are subordinate to Founder instruction, project authority and CURRENT Self-Improvement v2.

## 01 REGISTRY_IDENTITY
**Purpose:** candidate IDs must be unique across base registry + every extension shard.  
**Input:** complete current registry family.  
**Output:** uniqueness proof or fail-closed collision report.  
**Gate:** partial registry visibility cannot allocate a new ID.  
**Protocol:** `READ_FULL_FAMILY -> HASH/ENUMERATE_IDS -> COLLISION_CHECK -> ALLOCATE_UNUSED_ID -> READBACK`.

## 02 DURABLE_RECONCILIATION
**Purpose:** multi-store GitHub/Drive/state writes are one logical transaction.  
**States:** `PREPARED / APPLIED / COMMITTED_VERIFIED / REPAIR_REQUIRED / INCOMPLETE`.  
**Gate:** mixed store states can never be called complete.  
**Protocol:** `TXN_ID -> READ_EACH_STORE -> RECONCILE -> REPAIR_ONLY_MISSING/FAILED -> READBACK_ALL`.

## 03 CHECKPOINT_LINEAGE
**Purpose:** resumable execution checkpoints form an ordered tamper-evident chain.  
**Fields:** `seq / payload / parent_hash / hash`.  
**Gate:** hash integrity does not prove freshness or authority; those are re-read separately.  
**Protocol:** `MATERIAL_BOUNDARY -> CHECKPOINT -> HASH_PARENT -> PERSIST -> NEXT_SESSION_VALIDATE_LINEAGE -> FRESHNESS_GATE`.

## 04 INTERRUPTION_LEARNING
**Purpose:** turn real interruptions into evidence without overgeneralizing one incident.  
**Fields:** interruption type, durable state before/after, duplicate work, recovery minutes.  
**Gate:** one successful recovery remains `ONE_INCIDENT_ONLY`.  
**Protocol:** `INCIDENT -> DURABLE_BEFORE/AFTER -> RECOVERY_RESULT -> COST -> LEARNING_LEDGER -> REPLICATION`.

## 05 BOOK_SI_BRIDGE
**Purpose:** ingest Book Engine observations into global SI without granting authority.  
**Disposition:** `MERGE_WITH_EXISTING / ACCEPT_WITH_SCOPE / HOLD_FOR_CROSS_PROJECT_TEST / REJECT / SUPERSEDE`.  
**Gate:** project `PILOT_PASS` is not global promotion.  
**Protocol:** `BOOK_OBSERVATION -> EVIDENCE_CLASS -> EARLIEST_FAILURE -> DEDUPE -> CANDIDATE -> CROSS_BOOK_GATE`.

## 06 BOOK_SENSOR_TRANSFER
**Purpose:** transfer source-hash-bound story-state/promise/causality sensors.  
**Gate:** must include both positive detection and healthy no-change control.  
**Protocol:** `SOURCE_HASH -> SENSOR -> POSITIVE_FIXTURE -> HEALTHY_CONTROL -> FALSE_POSITIVE_CHECK -> SECOND_BOOK`.

## 07 FRONTIER_DRIFT
**Purpose:** survive rapid project advancement across sibling dialogs/branches.  
**Gate:** newest compatible persisted frontier wins below authority; stale episode resumption is blocked.  
**Protocol:** `COLLECT_FRONTIERS -> STATUS/TIME/PROVENANCE -> RESOLVE -> STALE_WORK_GATE -> ROUTE_NEXT`.

## 08 HUMAN_SIGNAL
**Purpose:** keep real human evidence separate from model review.  
**Classes:** `FOUNDER_SIGNAL / HUMAN_SIGNAL / MODEL_REVIEW`.  
**Gate:** prepared questionnaire != completed Human Signal; model personas never substitute.  
**Protocol:** `REAL_PARTICIPANTS -> UNCOACHED_RAW_RESPONSES -> STORE_RAW -> SYNTHESIZE -> DISPOSITION`.

## 09 EVIDENCE_INDEPENDENCE
**Purpose:** count independent root evidence families, not reports/models.  
**Gate:** multiple reports sharing one root source/evidence lineage count as one family.  
**Protocol:** `REPORT -> ROOT_PROVENANCE -> CLUSTER -> FAMILY_COUNT -> RECONCILE`.

## 10 PACKAGE_WITNESS
**Purpose:** prove exact package identity.  
**Evidence:** ZIP byte SHA-256 + member manifest + cold reproducibility.  
**Gate:** a version label cannot inherit post-package GitHub changes.  
**Protocol:** `BUILD -> HASH -> MEMBER_MANIFEST -> COLD_UNPACK -> TEST -> SIDECAR_CHECKSUM`.

## 11 PROMOTION_PROOF
**Purpose:** define minimum evidence before a candidate can even become eligible for authority review.  
**Required:** application target, regression PASS, readback PASS, rollback, evidence boundary.  
**Gate:** required external evidence missing -> HOLD.  
**Protocol:** `APPLY_BOUNDED -> REGRESSION -> READBACK -> ROLLBACK_TEST -> EVIDENCE_CLASS -> REVIEW_ELIGIBILITY`.

## 12 TELEMETRY_PROOF
**Purpose:** prevent telemetry inflation.  
**Required event fields:** event ID, project, kind, decision, evidence class.  
**Gate:** unmeasured zero is invalid; unknown remains `null`.  
**Protocol:** `OBSERVE -> MEASURED? -> VALUE/NULL -> SOURCE -> APPEND -> AUDIT`.

## 13 ECONOMICS_PROOF
**Purpose:** calculate production economics only from measured inputs.  
**Required:** provider spend, human minutes, accepted minutes, human hourly cost.  
**Gate:** any missing measured field -> HOLD.  
**Protocol:** `CAPTURE_REAL_SPEND/TIME -> ACCEPTED_MINUTES -> COMPUTE -> STORE_PROVENANCE`.

## 14 SECOND_PROJECT_REPLICATION
**Purpose:** prevent one-project success from becoming domain truth.  
**Gate:** independent project + unchanged generic mechanism hash + PASS on both.  
**Protocol:** `FREEZE_MECHANISM -> ADAPT_PROJECT_DATA_ONLY -> SECOND_PROJECT -> COMPARE -> SCOPE_REVIEW`.

## 15 PROOF_LEDGER
**Purpose:** attach evidence classes and source references to self-improvement claims.  
**Evidence classes:** `ENGINEERING_TEST / PERSISTED_READBACK / HUMAN_SIGNAL / LIVE_PROVIDER / MEASURED_ECONOMICS / MARKET_BEHAVIOR`.  
**Gate:** cross-class substitution is blocking.  
**Protocol:** `CLAIM -> EVIDENCE_CLASS -> SOURCE_REF -> APPEND_ONLY_LEDGER -> PROMOTION_CHECK`.

## 16 SELF_IMPROVEMENT_GOVERNOR
**Purpose:** prevent recursive meta-work from starving product/evidence work.  
**Decision inputs:** priority, information value, effort, authorization, task kind.  
**Gate:** higher-information P1/P2/human/provider evidence explicitly displaces lower-value meta work.  
**Protocol:** `CURRENT_OPTIONS -> FILTER_AUTHORIZED -> COMPARE_INFORMATION_VALUE -> ROUTE -> RECORD_REJECTED_META_IF_APPLICABLE`.

## Shared enforcement law
`FRESH READ -> AUTHORITY -> INPUT IDENTITY -> EXECUTE BOUNDED ACTION -> READBACK -> EVIDENCE CLASS -> DISPOSITION -> PERSIST`.

Never fabricate Founder approval, Human Signal, live provider success, measured economics or market behavior.