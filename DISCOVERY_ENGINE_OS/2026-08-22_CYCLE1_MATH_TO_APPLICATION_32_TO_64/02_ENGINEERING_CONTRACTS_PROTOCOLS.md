# DISCOVERY ENGINE OS — CYCLE1 ENGINEERING / CONTRACTS / PROTOCOLS

## Modules D001-D032

- D001 AuthorityResolver
- D002 LibraryPassportCompiler
- D003 ClaimAtomizer
- D004 NoveltyPlaneClassifier
- D005 PriorArtSearchPlanner
- D006 PriorArtFeatureMatrix
- D007 ClosestPriorArtResolver
- D008 NoveltyStatusEngine
- D009 ConjectureGenerator
- D010 CounterexampleSearch
- D011 FormalProofAdapter
- D012 ComputationalProofHarness
- D013 SymbolicRegressionEngine
- D014 InvariantDiscoveryEngine
- D015 AlgorithmEvolutionEngine
- D016 HiddenEvaluatorFirewall
- D017 MechanismExtractor
- D018 CrossDomainTransferGraph
- D019 TransferCounterexampleGate
- D020 PrototypeCompiler
- D021 ExperimentDesigner
- D022 MeasurementUncertainty
- D023 CausalClaimFirewall
- D024 PatentTriageAdapter
- D025 EngineeringTRLGate
- D026 ValueOfInformationRouter
- D027 ApplicationPortfolio
- D028 BusinessTransferBridge
- D029 ClaimLedger
- D030 RedTeamRouter
- D031 SelfImprovementAdapter
- D032 DiscoveryClosureEngine

## Contracts DC001-DC032

1. `FRESH_AUTHORITY_BEFORE_SEARCH` — resolve current authority before candidate generation.
2. `RAW_COPYRIGHTED_SOURCES_PRIVATE` — no raw copyrighted binaries in public GitHub.
3. `SOURCE_PASSPORT_REQUIRED` — mechanism use requires source identity/provenance/jurisdiction.
4. `CLAIM_ATOMIZATION_REQUIRED` — compound claims split into testable atoms.
5. `NOVELTY_PLANES_SEPARATE` — truth/scientific/patent/engineering/application/market planes are non-substitutable.
6. `ABSENCE_OF_MATCH_NOT_NOVELTY` — bounded no-match never emits NEW.
7. `PRIOR_ART_SEARCH_BEFORE_PROMOTION` — search known mechanisms before novelty promotion.
8. `SINGLE_REFERENCE_FEATURE_GATE` — patent novelty triage checks all features in one reference; inventive step remains separate.
9. `PATENT_TRIAGE_NOT_LEGAL_OPINION`.
10. `COUNTEREXAMPLE_BEFORE_THEOREM_PROMOTION`.
11. `FORMAL_PROOF_STATUS_TYPED` — source proof, kernel verification and external theorem novelty are separate.
12. `COMPUTATIONAL_VERIFICATION_BOUNDED` — finite/numerical evidence states its domain.
13. `REDISCOVERY_IS_SUCCESS_NOT_NOVELTY`.
14. `SYMBOLIC_REGRESSION_NEEDS_HOLDOUT`.
15. `ALGORITHM_SEARCH_NEEDS_HIDDEN_EVALUATOR`.
16. `GOODHART_FIREWALL` — evaluator optimization requires fresh hidden/adversarial controls.
17. `MECHANISM_NOT_APPLICATION`.
18. `TRANSFER_NEEDS_POSITIVE_AND_NEGATIVE_FIXTURE`.
19. `CAUSAL_CLAIM_FIREWALL`.
20. `PROTOTYPE_BEFORE_APPLICATION_CLAIM`.
21. `MEASUREMENT_UNCERTAINTY_EXPLICIT`.
22. `VOI_BEFORE_EXPENSIVE_EXPERIMENT`.
23. `ENGINEERING_TRL_TYPED`.
24. `ENGINEERING_SYNTHESIS_NOT_SCIENTIFIC_NOVELTY`.
25. `APPLICATION_VALUE_NOT_MARKET_PROOF`.
26. `BUSINESS_TRANSFER_USES_BUSINESS_OS_GATES`.
27. `FAILURES_ARCHIVED`.
28. `CLAIM_LEDGER_APPEND_ONLY`.
29. `RED_TEAM_BEFORE_RELEASE`.
30. `SELF_IMPROVEMENT_BOUNDED`.
31. `NO_AUTO_AUTHORITY_PROMOTION`.
32. `CLOSURE_FORBIDS_UNVERIFIED_NEW`.

## Protocol P1 — Candidate generation
Generate only after authority/source/prior-art restoration. Novel wording is not novelty evidence.

## Protocol P2 — Novelty planes
Maintain separate ledgers for mathematical truth, scientific novelty, patent novelty/inventive-step triage, engineering novelty, application evidence and market evidence. No plane promotes another automatically.

## Protocol P3 — Mathematical claim
`CONJECTURE -> EDGE CASES -> COUNTEREXAMPLE SEARCH -> ORDINARY PROOF -> FORMALIZATION TARGET -> PRIOR ART -> STATUS`.

## Protocol P4 — Algorithm/equation discovery
`TRAIN/SEARCH -> BASELINE -> HIDDEN -> ADVERSARIAL/SHIFT -> COMPLEXITY/INTERPRETABILITY -> PRIOR ART -> STATUS`.

## Protocol P5 — Cross-domain transfer
`SOURCE MECHANISM -> TARGET MAPPING -> POSITIVE FIXTURE -> NEGATIVE/LIMITATION FIXTURE -> PROTOTYPE -> DOMAIN RED TEAM`.
A transferred mechanism is `APPLICATION_CANDIDATE`, not automatically a new theorem.

## Protocol P6 — Patent triage
Use official prior-art framing only as research triage. Full disclosure in one reference may yield negative novelty triage; split references leave inventive step unresolved. No legal opinion.

## Protocol P7 — Engineering/application
`PROOF -> PROTOTYPE -> BENCH/LAB -> REAL ENVIRONMENT -> DOMAIN ACCEPTANCE`.

## Protocol P8 — Business bridge
Reuse Business Engineering OS evidence/non-substitution/cash gates. Technical application does not create buyer/payment proof.

## Protocol P9 — Self-improvement
`OBSERVE DEFECT -> CANDIDATE PATCH -> SANDBOX -> BENCHMARK -> HIDDEN/ADVERSARIAL -> LOCAL_KEEP/HOLD -> LEARNING`.
No automatic CURRENT/merge/release.

## Protocol P10 — Closure
Cycle closes only if 32 prompts are dispositioned, no unsupported NEW labels remain, failures/rediscoveries/counterexamples persist, tests/cold replay pass, and GitHub/Drive readback is recorded.
