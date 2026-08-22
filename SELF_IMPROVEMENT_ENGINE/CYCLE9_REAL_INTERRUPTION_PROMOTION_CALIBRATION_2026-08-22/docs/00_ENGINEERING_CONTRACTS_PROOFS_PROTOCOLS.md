# Cycle9 Engineering Contracts / Proofs / Protocols

## Concrete modules C9-M01..C9-M20
1. AuthoritySnapshot
2. SourceLibraryRegistry
3. CandidateFamilyFreshness
4. RealInterruptionClassifier
5. RecoveryQualificationCounter
6. ProjectSliceFreshnessGate
7. FalseResumeDetector
8. EvidenceClassFirewall
9. PromotionReadinessGate
10. MetaWIPLimiter
11. ValueOfInformationRouter
12. CausalSystemModel
13. PolicyResistanceGate
14. DoubleLoopLearningTrigger
15. Uncertainty/MeasureJustEnough discipline
16. DecisionDeltaLedger
17. MechanismDedupePruner
18. CrossStoreClosureGate
19. SelfReferenceGuard
20. SequentialEvidenceLedger

## Contracts C9-C01..C9-C32
1. FOUNDER_NEWEST_INSTRUCTION_HIGHEST.
2. V2_VERIFIED_CURRENT_UNTIL_EXPLICIT_PROMOTION.
3. REFERENCE_MECHANISM_NEQ_AUTHORITY.
4. NEWER_BRANCH_NEQ_CURRENT_AUTHORITY.
5. FULL_CANDIDATE_FAMILY_BEFORE_NEW_ID.
6. STALE_BRANCH_REBASE_NO_FORCE_OVERWRITE.
7. RAW_COPYRIGHTED_REFERENCE_STAYS_PRIVATE.
8. PUBLIC_GITHUB_METADATA_DERIVED_ONLY.
9. REAL_INTERRUPTION_NEQ_QUALIFYING_RECOVERY.
10. SYNTHETIC_INTERRUPTION_COUNTS_ZERO_REAL_EVENTS.
11. QUALIFYING_RECOVERY_REQUIRES_PROJECT_SLICE_READBACK.
12. QUALIFYING_RECOVERY_REQUIRES_STORE_IDENTITY.
13. QUALIFYING_RECOVERY_REQUIRES_ZERO_FALSE_RESUME.
14. AMBIGUOUS_IRREVERSIBLE_EFFECT_QUARANTINE.
15. CURRENT_SLICE_MUST_MATCH_CONTROLLING_FRONTIER.
16. HISTORICAL_SLICE_EXEMPT_FROM_FRESHNESS_ERROR.
17. EXPLICIT_APPROVAL_REQUIRES_AUTHORITY_EVENT.
18. AUTOMATED_TEST_NEQ_HUMAN_SIGNAL.
19. SOURCE_INSPECTION_NEQ_RUNTIME_EXECUTION.
20. MODEL_AGREEMENT_NEQ_INDEPENDENT_EVIDENCE.
21. ONE_PRIMARY_PLUS_TWO_PILOTS_META_WIP.
22. METRIC_REQUIRES_DECISION_RELEVANCE.
23. MEASURE_ONLY_IF_INFORMATION_VALUE_JUSTIFIES_COST.
24. PROMOTION_PILOT_REQUIRES_CAUSAL_MODEL_AND_GUARDRAILS.
25. LOCAL_GAIN_NEQ_SYSTEM_GAIN.
26. REPEATED_LOCAL_FAILURE_TRIGGERS_DOUBLE_LOOP_REVIEW.
27. NO_DECISION_DELTA_NEQ_PROGRESS.
28. DUPLICATE_MECHANISM_MERGE_NOT_CLONE.
29. HIGH_FALSE_POSITIVE_MECHANISM_NARROW.
30. SELF_IMPROVEMENT_MAY_NOT_SELF_EXEMPT.
31. VERIFIED_CURRENT_REQUIRES_APPLICATION_PLUS_READBACK_VERIFICATION.
32. PROMOTION_MUST_HAVE_ROLLBACK_AND_CAN_BE_PRUNED_LATER.

## Proof obligations C9-P01..C9-P20
- P01 exact main SHA captured before branch work.
- P02 old Cycle9 branch divergence is detected.
- P03 candidate family has unique IDs SI-0008..SI-0015.
- P04 real browser/dialog loss is recorded as real interruption observation.
- P05 same observation does not qualify without slice/store/readback evidence.
- P06 synthetic incident does not count.
- P07 three qualified recoveries across two projects can satisfy threshold.
- P08 stale CURRENT slice is detected.
- P09 historical slice is not falsely flagged.
- P10 missing explicit approval is detected.
- P11 test evidence cannot create Human Signal.
- P12 WIP over-limit fails.
- P13 decision-irrelevant metric is rejected.
- P14 local-positive/system-negative result detects policy resistance.
- P15 repeated local failure triggers double-loop review.
- P16 duplicate mechanism -> MERGE.
- P17 high-FP mechanism -> NARROW.
- P18 confirmed store hash mismatch -> STOP.
- P19 direct VERIFIED_CURRENT without apply/readback -> BLOCK.
- P20 self-exemption -> REJECT.

## Protocols
### P-SI-01 Fresh Authority Boot
Founder instruction -> current router -> machine state -> full candidate family -> current main SHA -> parallel branch compare -> work target.

### P-SI-02 Real Interruption Evidence
Incident -> real/synthetic classification -> affected projects -> exact project slices -> store identities -> replay decisions -> readback -> false-resume check -> qualifying/not qualifying.

### P-SI-03 Project Slice Freshness
Embedded CURRENT claim -> controlling source -> compare -> approval-event check -> CURRENT_MATCH / STALE / UNRESOLVED / APPROVAL_EVENT_MISSING.

### P-SI-04 Promotion Calibration
Candidate -> causal hypothesis -> baseline -> canary -> adversarial -> regression -> real pilot -> evidence-class matrix -> promotion review -> apply -> readback -> verify.

### P-SI-05 Meta WIP + VOI
Backlog unlimited -> active primary <=1 -> independent pilots <=2 -> choose next experiment by decision relevance + expected information gain + cost/delay.

### P-SI-06 Double-loop Learning
Repeated defect -> stop patch repetition -> revisit model/boundary/goal/assumption -> new falsifiable hypothesis -> bounded test.

### P-SI-07 Cross-store Closure
Plan -> per-store intended identity -> execute reversible steps -> readback -> quarantine ambiguous irreversible effects -> exact closure -> ledger.

### P-SI-08 Prune / Rollback
Telemetry -> duplicate/unused/high-FP/no-delta identification -> KEEP/NARROW/MERGE/HOLD/ROLLBACK -> preserve provenance -> update router only after verification.
