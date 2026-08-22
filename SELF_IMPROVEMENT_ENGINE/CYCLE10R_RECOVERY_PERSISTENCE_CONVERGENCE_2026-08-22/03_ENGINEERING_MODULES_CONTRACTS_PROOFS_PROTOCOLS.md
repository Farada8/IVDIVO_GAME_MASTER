# CYCLE10R — ENGINEERING MODULES / CONTRACTS / PROOFS / PROTOCOLS

Cycle10R is an additive extension of existing v2/Cycle9/SI-0014/SI-0015 owners. It introduces **no new global SI ID** and no second durable-write runtime.

## 16 bounded modules
1. **C10RM01 ProjectRecoveryFrontier** — resolves one project slice from persisted authority/evidence and returns current frontier + holds.
2. **C10RM02 FreshnessVector** — represents embedded pointer, observed main, authoritative closure and source timestamps without scalar freshness magic.
3. **C10RM03 AuthorityPointerLagGuard** — stale embedded CURRENT routes `REBASE_FIRST`.
4. **C10RM04 CrossStoreArtifactRecord** — logical artifact + GitHub identity + Drive identity + semantic anchors + readback states.
5. **C10RM05 CrossStorePersistenceManifest** — classifies `COMPLETE / PARTIAL / FAILED` without external-evidence inflation.
6. **C10RM06 ReadbackAnchorVerifier** — existence/title is insufficient; required semantic anchors must be present.
7. **C10RM07 PartialPersistenceRepairPlanner** — executes only missing safe/reversible side; no accepted-write replay.
8. **C10RM08 RecoveryIncidentLedger** — one real interruption owns one incident ID and many project slices.
9. **C10RM09 QualifiedRecoveryCounter** — counts unique qualifying incident IDs only.
10. **C10RM10 DistinctProjectCounter** — counts distinct recovered projects independently from incident count.
11. **C10RM11 FalseResumeGuard** — any qualifying false resume blocks promotion eligibility.
12. **C10RM12 SemanticSalvagePlanner** — keeps newer authority, salvages only unique compatible delta, otherwise HOLD.
13. **C10RM13 EvidenceFamilyNormalizerAdapter** — reuses current evidence-family logic; one raw root counts once.
14. **C10RM14 V3MechanismTribunal** — mechanism-by-mechanism MERGE/HOLD/REJECT; no whole-v3 promotion shortcut.
15. **C10RM15 ProductionReturnGate** — every meta cycle declares a real production return target.
16. **C10RM16 LibrarySurfaceRegistry** — stores source location/identity/status without equating physical file, byte hash, canonical work or authority.

## 24 contracts
1. `C10RC01 SAME_INTERRUPTION_MULTI_PROJECT_NEQ_MULTI_EVENT`
2. `C10RC02 RECOVERY_EVENT_REQUIRES_REAL_INTERRUPTION`
3. `C10RC03 QUALIFYING_EVENT_REQUIRES_READBACK`
4. `C10RC04 FALSE_RESUME_ZERO_REQUIRED_FOR_PROMOTION`
5. `C10RC05 DISTINCT_PROJECT_COUNT_SEPARATE_FROM_EVENT_COUNT`
6. `C10RC06 SI0014_PROMOTION_REQUIRES_GE3_EVENTS_GE2_PROJECTS`
7. `C10RC07 STALE_CURRENT_POINTER_REBASE_FIRST`
8. `C10RC08 NEWER_CLOSURE_NEQ_OLDER_CURRENT_PROSE`
9. `C10RC09 WRITE_CLAIM_NEQ_PERSISTED_ARTIFACT`
10. `C10RC10 MATERIAL_WRITE_REQUIRES_READBACK`
11. `C10RC11 READBACK_REQUIRES_SEMANTIC_ANCHORS`
12. `C10RC12 PARTIAL_PERSISTENCE_NEQ_PASS`
13. `C10RC13 DRIVE_ONLY_NEQ_ABSENT`
14. `C10RC14 GITHUB_ONLY_NEQ_COMPLETE_PERSISTENCE`
15. `C10RC15 PARTIAL_REPAIR_MUST_NOT_REPLAY_ACCEPTED_WRITE`
16. `C10RC16 CROSS_STORE_PARITY_IS_SEMANTIC_NOT_REQUIRED_BYTE_IDENTITY`
17. `C10RC17 PHYSICAL_FILE_NEQ_BYTE_HASH_NEQ_CANONICAL_WORK`
18. `C10RC18 FILE_LIBRARY_REFERENCE_NEQ_RAW_DURABILITY`
19. `C10RC19 RAW_COPYRIGHTED_SOURCE_STAYS_PRIVATE`
20. `C10RC20 NO_NEW_SI_ID_FOR_EXISTING_MECHANISM_EXTENSION`
21. `C10RC21 ACTIVE_BRANCH_RESERVATION_COUNTS_FOR_ID_COLLISION`
22. `C10RC22 V3_MECHANISM_VALUE_NEQ_V3_GLOBAL_PROMOTION`
23. `C10RC23 EXTERNAL_EVIDENCE_CLASSES_NON_SUBSTITUTABLE`
24. `C10RC24 META_CYCLE_REQUIRES_PRODUCTION_RETURN`

## 12 proof families
- **C10RP01 Authority proof** — v2 remains controlling; newer evidence layers do not self-promote.
- **C10RP02 Recovery-frontier proof** — project frontier recovered from GitHub + Drive, not chat memory.
- **C10RP03 Same-event proof** — adding Business project slice leaves event count unchanged.
- **C10RP04 Project-diversity proof** — Self-Improvement + Business Engineering = 2 distinct projects.
- **C10RP05 False-resume proof** — qualifying event remains zero-false-resume.
- **C10RP06 Promotion-counter proof** — 1/3 events cannot promote SI-0014.
- **C10RP07 Freshness proof** — stale Business CURRENT prose loses to later merged closure.
- **C10RP08 Partial-persistence proof** — one-store state is typed PARTIAL.
- **C10RP09 Readback proof** — required content anchors and correct destination are verified.
- **C10RP10 Library-boundary proof** — 35 systems physical entries reported without invented unique count; raw remains private.
- **C10RP11 Dedupe/ID proof** — PR #147 SI-0016 reservation blocks duplicate allocation.
- **C10RP12 v3 tribunal proof** — references/model agreement cannot produce global promotion.

## 8 protocols
### C10RR01 RESTORE_AND_REBASE
`READ MAIN -> READ CURRENT ROUTER -> READ REGISTRY FAMILY -> READ PROJECT CLOSURE -> COMPARE -> CURRENT / REBASE_FIRST / HOLD`

### C10RR02 RECOVERY_INCIDENT
`OBSERVED REAL INTERRUPTION -> INCIDENT ID -> PROJECT SLICES -> GITHUB READBACK -> DRIVE READBACK -> FALSE RESUME CHECK -> QUALIFIED/FAILED`

### C10RR03 COUNTING
`UNIQUE QUALIFYING INCIDENT IDs -> EVENT COUNT`  
`DISTINCT QUALIFYING PROJECT IDs -> PROJECT COUNT`  
Never derive one from the other.

### C10RR04 PERSISTENCE_TRANSACTION
`INTENT -> EXPECTED DESTINATIONS -> WRITE -> READBACK -> SEMANTIC ANCHORS -> CROSS-STORE CLASSIFICATION -> REPAIR MISSING SAFE SIDE -> READBACK`.

### C10RR05 SEMANTIC_SALVAGE
`FRESH MAIN -> PARALLEL DELTA -> CAPABILITY/MEANING DEDUPE -> KEEP NEWER AUTHORITY -> SALVAGE UNIQUE COMPATIBLE DELTA -> REGRESSION -> READBACK`.

### C10RR06 LIBRARY_INGEST
`DISCOVER -> LOCATION -> PHYSICAL ID -> VALIDITY/QUARANTINE -> HASH IF PROVEN -> CANONICAL WORK IF PROVEN -> SOURCE PASSPORT -> MECHANISM -> AUTHORITY CLASS`.

### C10RR07 V3_TRIBUNAL
`MECHANISM -> EXISTING OWNER? -> REAL PROJECT EVIDENCE? -> HEALTHY CONTROL? -> MEASURED NET GAIN? -> MERGE / LOCAL PILOT / HOLD / REJECT`.

### C10RR08 CLOSE_AND_RETURN
`RED TEAM -> TEST -> PERSIST -> READBACK -> UPDATE ONLY JUSTIFIED STATE -> NEXT64 AS BACKLOG -> RETURN TO HIGHEST-INFORMATION PRODUCTION GATE`.

## Evidence boundary
Deterministic canaries can prove routing/contract behavior only. They cannot prove Human Signal, provider quality, market demand, literary quality or economic value. Unknown external evidence remains null/HOLD.