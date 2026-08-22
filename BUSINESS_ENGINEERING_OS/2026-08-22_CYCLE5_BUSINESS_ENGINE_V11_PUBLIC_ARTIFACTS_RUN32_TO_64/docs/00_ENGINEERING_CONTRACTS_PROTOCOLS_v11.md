# BUSINESS ENGINE v1.1 — ENGINEERING CONTRACTS / PROOFS / PROTOCOLS

## New modules BE161–BE176
- **BE161 PublicArtifactCompiler** — source-bound artifact with explicit unknowns and E2+ ceiling.
- **BE162 SourceLineageResolver** — current/superseded/amendment lineage; stale values never fill current nulls silently.
- **BE163 RequirementEvidenceCompiler** — MUST/SHOULD/INFO/UNKNOWN with fatal-if-missing semantics.
- **BE164 HardExclusionGate** — vetoes before any soft comparison.
- **BE165 ArtifactProvenanceDigest** — deterministic content/source digest.
- **BE166 ManualBaselineProtocol** — measured baseline or null; estimates do not become observed evidence.
- **BE167 ArtifactProductionMeasurement** — engine/operator minutes only from observed run.
- **BE168 ErrorTaxonomyEngine** — stale source / missing source / unknown laundering / fatal requirement / proof overclaim.
- **BE169 DecisionDeltaLedger** — research is progress only when it changes a decision or adds independent information.
- **BE170 ExperimentStopGate** — repeated no-delta tests stop or change hypothesis.
- **BE171 ProofTransitionFirewall** — public E2+; real buyer E3; real payment/PO/deposit E4.
- **BE172 ArtifactSelectiveInvalidation** — semantic downstream recomputation only; locked nodes block mutation.
- **BE173 InformationGainPortfolioGovernor** — 1 primary + 2 pilots with independent hypothesis families.
- **BE174 ArtifactEconomicsGate** — contribution economics only from actual revenue/cost/time observations.
- **BE175 MechanismPruningEngine** — KEEP/NARROW/MERGE/HOLD based on duplication, false positives and use.
- **BE176 SelfImprovementArtifactBridge** — repeated evidence-backed defects become candidates; never self-promote.

## Contracts C185–C216
1. `RAW_LIBRARY_AUTHORITY_SINGLE_POINTER` — raw uploaded business sources remain in the one private Drive authority.
2. `PUBLIC_GIT_METADATA_ONLY_FOR_COPYRIGHTED_RAW` — no raw copyrighted books in public GitHub.
3. `SOURCE_ID_NEQ_CURRENT_FACT` — a source record alone does not make its facts current.
4. `CURRENT_AND_SUPERSEDED_EXPLICIT` — every changing public signal has current/superseded state.
5. `OLD_VALUE_NEQ_CURRENT_NULL_FILL` — stale values never fill a current null without explicit current evidence.
6. `PUBLIC_ARTIFACT_SOURCE_REQUIRED`.
7. `PUBLIC_ARTIFACT_E2_PLUS_MAX`.
8. `MUST_REQUIREMENT_MISSING_CAN_VETO`.
9. `HARD_EXCLUSION_BEFORE_SOFT_FIT`.
10. `UNKNOWN_FIELDS_STAY_NULL_OR_EXPLICIT_UNKNOWN`.
11. `PUBLIC_BUDGET_NEQ_VENDOR_REVENUE`.
12. `PUBLIC_ROLE_NEQ_CONFIRMED_BUYER`.
13. `SUPPORT_PATH_NEQ_GRANT_AWARD`.
14. `SUPPORT_PATH_NEQ_BUYER_DEMAND`.
15. `BASELINE_MINUTES_REQUIRE_OBSERVATION`.
16. `ENGINE_MINUTES_REQUIRE_OBSERVATION`.
17. `TIME_SAVED_REQUIRES_SAME_TASK_PAIR`.
18. `ERROR_REDUCTION_REQUIRES_PREDECLARED_ERROR_TAXONOMY`.
19. `NO_DECISION_DELTA_NEQ_PROGRESS`.
20. `TWO_NO_DELTA_TESTS_TRIGGER_STOP_OR_HYPOTHESIS_CHANGE`.
21. `REAL_BUYER_EVENT_REQUIRED_FOR_E3`.
22. `REAL_PAYMENT_PO_DEPOSIT_REQUIRED_FOR_E4`.
23. `PAYMENT_EVENT_REQUIRES_EVIDENCE_REF`.
24. `NO_OUTREACH_MEANS_E3_E4_BLOCKED`.
25. `DEADLINE_CHANGE_INVALIDATES_ONLY_SEMANTIC_DESCENDANTS`.
26. `LOCKED_DESCENDANT_NEQ_AUTO_REWRITE`.
27. `PORTFOLIO_PILOTS_REQUIRE_INDEPENDENT_INFORMATION`.
28. `ACTUAL_ECONOMICS_ONLY_FROM_OBSERVED_VALUES`.
29. `DUPLICATE_MECHANISM_MERGE_NOT_CLONE`.
30. `HIGH_FALSE_POSITIVE_MECHANISM_NARROW`.
31. `UNUSED_MECHANISM_HOLD_TELEMETRY`.
32. `SI_CANDIDATE_REQUIRES_REPEATED_EVIDENCE_REGRESSION_READBACK`.

## Proof obligations P185–P216
P185 Library pointer resolves to current 78-file authority.  
P186 GitHub library contains metadata/registry/passports only.  
P187 Old and reissued Skerries notices remain distinct lineage nodes.  
P188 Old EUR245k value is not promoted into the reissued notice with blank current value.  
P189 Current deadline uses current source.  
P190 Public artifact without source fails.  
P191 Public artifact claiming E3 fails.  
P192 Fatal unverified MUST requirement fails.  
P193 Explicit unknowns survive serialization.  
P194 Public tender budget does not populate our revenue.  
P195 Public procurement role stays PUBLIC_ROLE/UNKNOWN, not buyer commitment.  
P196 Digital support availability cannot set grant_awarded.  
P197 Digital support availability cannot set buyer_commitment.  
P198 Missing baseline minutes remains null/HOLD.  
P199 Missing engine minutes remains null/HOLD.  
P200 Measured paired times can compute time saved.  
P201 Measured paired errors can compute errors reduced.  
P202 Decision change emits DECISION_CHANGED.  
P203 No decision change emits NO_DECISION_DELTA.  
P204 Two no-delta outcomes trigger STOP_OR_CHANGE_HYPOTHESIS.  
P205 Public-only returns E2_PLUS.  
P206 Real buyer event returns E3.  
P207 Real payment event returns E4.  
P208 PO without evidence reference is not E4.  
P209 Semantic dependency graph ignores non-semantic ordering edges.  
P210 Deadline invalidation propagates only through semantic descendants.  
P211 Locked submission blocks rewrite.  
P212 Portfolio admits information-independent pilot families only.  
P213 Economics stays null without actual revenue/cost/time.  
P214 Duplicate mechanism -> MERGE.  
P215 High false-positive -> NARROW.  
P216 SI candidate review requires repeat evidence + regression + readback + decision delta.

## Protocols
- **P-BIZ-17 Library Registry:** RAW AUTHORITY → COUNTS → QUARANTINE/DUPLICATE RULES → SOURCE PASSPORTS → READBACK.
- **P-BIZ-18 Source Lineage:** DISCOVER → CURRENT/SUPERSEDED → FIELD LINEAGE → UNKNOWN PRESERVATION → INVALIDATION.
- **P-BIZ-19 Public Artifact:** SOURCE → REQUIREMENTS → HARD EXCLUSIONS → UNKNOWN REGISTRY → ARTIFACT → DIGEST.
- **P-BIZ-20 Measurement:** SAME TASK → MANUAL BASELINE → ENGINE RUN → ERROR TAXONOMY → TIME/ERROR DELTA.
- **P-BIZ-21 Decision Value:** ARTIFACT → DECISION BEFORE/AFTER → UNIQUE INFORMATION → CONTINUE/RESHAPE/STOP.
- **P-BIZ-22 Proof Transition:** PUBLIC E2+ → REAL BUYER E3 → REAL PAYMENT E4; no substitution.
- **P-BIZ-23 Selective Recompute:** CHANGE → SEMANTIC DEPENDENCY GRAPH → DIRTY → LOCK BLOCK → MINIMAL REBUILD.
- **P-BIZ-24 Self Improvement:** OBSERVE → REPEAT → LOCALIZE → MINIMAL PATCH → REGRESSION → READBACK → CANDIDATE REVIEW.
