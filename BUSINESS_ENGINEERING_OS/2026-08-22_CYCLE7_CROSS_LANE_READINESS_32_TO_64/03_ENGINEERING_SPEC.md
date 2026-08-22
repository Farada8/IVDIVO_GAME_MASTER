# CYCLE7 — CROSS-LANE READINESS ENGINEERING SPEC

## Purpose
Compile heterogeneous real opportunities into explicit decision-readiness states without laundering public/source evidence into applicant, buyer, commercial, legal or market proof.

## Modules C7M01–C7M16
1. **C7M01 AuthorityReconciler** — fresh-read current authority and parallel bounded work before mutation.
2. **C7M02 OpportunityCaseCompiler** — normalize domain-neutral readiness case while preserving domain overlays.
3. **C7M03 EvidenceItemNormalizer** — field/value/source/currentness evidence object.
4. **C7M04 RequirementClaimCompiler** — authoritative requirement + provenance + fatality semantics.
5. **C7M05 CapabilityClaimCompiler** — capability + source + verification + expiry.
6. **C7M06 AuthorityCompletenessGate** — FULL / PARTIAL / MISSING, including intentional partial authority.
7. **C7M07 ProfileCompletenessGate** — only sourced, verified, non-null capability claims satisfy required profile fields.
8. **C7M08 RequirementCapabilityJoin** — requirement-by-requirement join preserving unmatched requirements.
9. **C7M09 GapStateRouter** — MET / UNKNOWN / CURABLE_BEFORE_DEADLINE / NONCURABLE / NOT_APPLICABLE.
10. **C7M10 DeadlineCurabilityEngine** — curability requires a proven clock; no speculative cure state.
11. **C7M11 FreshnessRevalidationGuard** — field-specific freshness and revalidation.
12. **C7M12 ReadinessDecisionStateMachine** — ordered typed states, no opaque score.
13. **C7M13 ReadinessReasonGraph** — explain earliest blocking layers.
14. **C7M14 NextEvidenceRouter** — route to authority/profile/gap/technical/review evidence by blocker priority.
15. **C7M15 ScopedSIPromotionGate** — recurrent defects promote only at the evidence-supported scope.
16. **C7M16 PersistenceTransactionGuard** — GitHub+Drive fresh-read/write/test/readback/reconcile/merge lifecycle.

## Contracts C7C01–C7C24
1. `CURRENT_POINTER_MUST_FRESH_READ`.
2. `MISSING_REQUIRED_AUTHORITY_EXPLICIT_HOLD`.
3. `PARTIAL_AUTHORITY_NEQ_MISSING`.
4. `UNKNOWN_NEQ_FAIL`.
5. `UNKNOWN_NEQ_PASS`.
6. `FATAL_REQUIRES_PROVEN_REQUIREMENT_PLUS_PROVEN_MISMATCH`.
7. `REQUIREMENT_SOURCE_PROVENANCE_REQUIRED`.
8. `CAPABILITY_SOURCE_PROVENANCE_REQUIRED`.
9. `JOIN_UNMATCHED_REQUIREMENTS_PRESERVED`.
10. `CURABLE_REQUIRES_DEADLINE_PROOF`.
11. `DEADLINE_NULL_NEQ_CURABLE`.
12. `PUBLIC_ARTIFACT_NEQ_MARKET_PROOF`.
13. `OFFICIAL_BRIEF_NEQ_APPLICANT_READINESS`.
14. `FULL_PACK_NEQ_SUPPLIER_ELIGIBILITY`.
15. `FINAL_SITE_TBD_CAN_BE_VALID_PARTIAL_AUTHORITY`.
16. `OPPORTUNITY_EXISTS_NEQ_APPLICANT_READY`.
17. `NEXT_EVIDENCE_BY_BLOCKER_NOT_PROMPT_COUNT`.
18. `PROMPT_COUNT_NEQ_PROGRESS`.
19. `NO_MAGIC_READINESS_SCORE`.
20. `PARALLEL_BOUNDED_ADAPTERS_PRESERVED`.
21. `GITHUB_DRIVE_READBACK_REQUIRED`.
22. `CURRENT_POINTER_AFTER_MERGE_ONLY`.
23. `RAW_COPYRIGHTED_BINARIES_DRIVE_ONLY`.
24. `SI_PROMOTION_SCOPED_BY_EVIDENCE`.

## Proof gates C7P01–C7P12
1. **AuthorityCompletenessProof** — required authority inventory and explicit FULL/PARTIAL/MISSING result.
2. **RequirementProvenanceProof** — requirement must trace to authoritative source.
3. **CapabilityProvenanceProof** — capability must trace to verified source and current state.
4. **JoinCoverageProof** — all authoritative requirements survive the join, including unmatched rows.
5. **UnknownSafetyProof** — UNKNOWN cannot be coerced to PASS or FAIL.
6. **FatalGapProof** — NONCURABLE requires authoritative requirement plus verified incompatible capability plus non-curability.
7. **CurabilityClockProof** — cure status requires deadline feasibility.
8. **ProofPlaneIsolation** — `K != S != PA != E`; public-only <= E2+.
9. **IndependentReviewProof** — same-input blinded independent review required for `INDEPENDENT_PA4`.
10. **RealInteractionProof** — PA5/E3 requires a real target-user decision-use record.
11. **PersistenceReadbackProof** — declared GitHub/Drive artifacts must be read back before current promotion.
12. **ScopedSIPromotionProof** — repeated cross-case defect + bounded scope + regression protection.

## Protocols C7R01–C7R10
1. **FreshReadReconcile** — read CURRENT + latest main + parallel branches/Drive deltas -> semantic disposition.
2. **OpportunityCompile** — real opportunity -> authority/profile/technical/proof state.
3. **RequirementCapabilityJoin** — requirements -> verified capabilities -> unmatched preservation.
4. **GapRouting** — join row -> MET/UNKNOWN/CURABLE/NONCURABLE/N/A with provenance.
5. **ReadinessDecision** — relevance -> authority -> profile -> gaps -> technical package -> independent review -> real decision-use.
6. **NextEvidence** — earliest blocker -> exact evidence acquisition action.
7. **IndependentPA4** — same packet -> blinded independent reviewer -> divergence record -> PA4/HOLD.
8. **RealDecisionUse** — target user -> before decision -> artifact use -> after decision -> PA5/E3 candidate only if behavioral evidence exists.
9. **TwoSurfacePersistence** — branch/folder -> writes -> CI -> Drive write/readback -> fresh-main rebase/reconcile -> merge -> closure pointer.
10. **SIPromotion** — repeated defect -> candidate -> scoped canaries -> bounded promotion -> monitor false positives/negatives.

## Decision states
- `REJECT_IRRELEVANT`
- `HOLD_MISSING_AUTHORITY`
- `HOLD_CAPABILITY_EVIDENCE`
- `HOLD_REQUIREMENT_GAPS`
- `HOLD_TECHNICAL_PACKAGE`
- `READY_FOR_INDEPENDENT_REVIEW`
- `READY_FOR_REAL_DECISION_USE_TEST`

No single numeric readiness score exists.

## Missing-authority taxonomy
- `MISSING_FULL_PACKET`
- `MISSING_VERIFIED_PROFILE`
- `PARTIAL_SITE_AUTHORITY`
- `MISSING_PROPOSAL_PACKAGE`
- `MISSING_COST_MODEL`
- `MISSING_INDEPENDENT_REVIEW`
- `MISSING_REAL_USER_INTERACTION`

## Scoped Self-Improvement promotion
Cycle7 supports promotion **inside Business Engineering only**:

`MISSING_REQUIRED_AUTHORITY -> EXPLICIT_TYPED_HOLD -> NEXT_EVIDENCE_ACTION`

Evidence basis: procurement and two independent public-art fixtures all fail at different required-evidence boundaries. The promoted rule controls state semantics and next-action routing; it does not assert that any opportunity is commercially good or bad.

Global Self-Improvement remains v2 CURRENT. v3 remains CANDIDATE ONLY.