# CYCLE5 ENGINEERING — MODULES B113–B138 / CONTRACTS C153–C184 / PROTOCOLS P-BIZ-17–24

## Modules
- **B113 SignalFreshnessScheduler** — published/observed/effective/deadline timestamps -> age/SLA state; never infer status from crawl freshness.
- **B114 OfficialUrlLineageResolver** — canonicalise official URLs while preserving identity keys such as eTenders resourceId.
- **B115 SyndicationFamilyDetector** — collapse mirrors/press-release copies into one evidence family.
- **B116 ProcurementStateVerifier** — deadline + portal state + award state -> OPEN/CLOSED/AWARDED/REVALIDATE contradiction.
- **B117 SourceSupersessionGraph** — policy/grant versions -> only latest verified version gets current authority.
- **B118 BudgetOwnerGate** — separate programme/project budget, contracting authority and actual payer.
- **B119 BuyerAccessPathVerifier** — official procurement portal/register/directory -> verified public access path.
- **B120 MarketStateClassifier** — NONCONSUMPTION/UNDERSHOT/OVERSHOT/currently-served labels as hypotheses, not facts.
- **B121 MotivationAbilityFixtureEngine** — separate incentive/obligation from ability/support pathways.
- **B122 IncumbentAsymmetryFixtureEngine** — test whether entrant process/motivation differs enough to justify a new route.
- **B123 WhyNowFalsifier** — every WhyNow claim has an explicit public kill/hold condition.
- **B124 OpportunityHalfLifeEngine** — policy SLA by signal class; heuristic is visible and revalidatable.
- **B125 FatalAssumptionQueue** — veto-first ordering by kill-power × uncertainty × testability.
- **B126 SharedAssumptionGraph** — one discriminating test can update multiple opportunities without evidence double-counting.
- **B127 NoOutreachExperimentLibrary** — select zero-cash, no-contact experiments by VOI rate.
- **B128 PublicArtifactCompiler** — build sample deliverables with explicit E2+ ceiling and external-proof firewall.
- **B129 ArtifactDeliveryTimeLedger** — machine generation observed separately from human review/delivery time.
- **B130 E3CaptureProtocolEngine** — only real external buyer behavior can promote to E3.
- **B131 E4PaymentProofEngine** — cash + binding transaction evidence required for E4.
- **B132 PricingNullSafeSchema** — price is null until an external price signal exists.
- **B133 FounderCashTimelineEngine** — committed cash events separated from hypothetical scenarios.
- **B134 GrantReimbursementBridgeDetector** — detect after-spend reimbursement versus upfront deduction.
- **B135 FundingTopologySelector** — payer + funding source + upfront cash requirement must be explicit.
- **B136 WorkingCapitalStressEngine** — model pre-finance cash gap; null-safe where inputs are unknown.
- **B137 ContributionMarginObject** — price – variable cost – delivery-time cost – rework; null-safe.
- **B138 ServiceCapacityQueueModel** — arrival/service/available hours -> utilization; null-safe and WIP-aware.

## Contracts
- **C153** — Publication, observation, effective, opening and deadline dates are distinct fields.
- **C154** — Expired/stale signal has zero action authority until revalidated.
- **C155** — Canonical source URL must preserve stable identity parameters and strip tracking noise.
- **C156** — Syndicated copies of one underlying event count as one evidence family.
- **C157** — Procurement state is determined from deadline/award/status semantics, not crawl freshness alone.
- **C158** — Superseded source versions have zero current-authority weight.
- **C159** — Programme/project budget does not prove buyer, payer or obtainable revenue.
- **C160** — Buyer access requires an official public path or remains HOLD.
- **C161** — NONCONSUMPTION/UNDERSHOT/OVERSHOT labels are test hypotheses, not market facts.
- **C162** — Motivation and ability are separate causal dimensions.
- **C163** — Incumbent asymmetry must be explicit and falsifiable.
- **C164** — Every WhyNow claim carries a kill/hold condition.
- **C165** — Opportunity half-life is a visible policy parameter, not hidden truth.
- **C166** — Fatal assumptions are tested before additive attractiveness.
- **C167** — A shared assumption can update multiple opportunities, but evidence family is counted once.
- **C168** — No-outreach/public experiments cannot exceed E2+.
- **C169** — An OP01 public artifact does not prove a buyer or WTP.
- **C170** — An OP03 retrofit artifact does not prove homeowner/installer demand or grant award.
- **C171** — An OP19 AI artifact does not prove WTP and must differentiate from public Digital for Business support.
- **C172** — Human manual delivery/review time stays null until actually observed.
- **C173** — Tender briefs must show official source, status/deadline and unknown qualification barriers.
- **C174** — Retrofit qualification packs must never guarantee SEAI grant eligibility or payment.
- **C175** — AI diagnostic artifacts must distinguish official facts from model-authored workflow hypotheses.
- **C176** — Future interview scripts avoid compliments and hypothetical-future answers as validation.
- **C177** — E3 requires an actual external buyer behavioral signal.
- **C178** — E4 requires cash received plus binding transaction evidence.
- **C179** — Price stays null until an external price signal exists.
- **C180** — Committed and hypothetical cash flows must not be summed as if equally real.
- **C181** — Reimbursement funding is not upfront cash.
- **C182** — Funding topology is HOLD until payer, funding source and upfront-cash requirement are known.
- **C183** — Material/labour-heavy routes require a working-capital stress pass before scale.
- **C184** — Contribution/capacity outputs remain null where required inputs are unknown.

## Protocols
- **P-BIZ-17 Freshness & Lineage** — `SOURCE -> CANONICAL URL -> DATE SEMANTICS -> EVIDENCE FAMILY -> AGE/SLA -> FRESH/REVALIDATE/STALE`.
- **P-BIZ-18 Procurement State** — `OFFICIAL NOTICE -> DEADLINE -> PORTAL STATE -> AWARD -> CONTRADICTION CHECK -> OPEN/CLOSED/AWARDED/HOLD`.
- **P-BIZ-19 Fatal Assumption** — `OPPORTUNITY -> VETO ASSUMPTIONS -> SHARED GRAPH -> HIGHEST-VOI TEST -> KILL/RESHAPE/HOLD/SURVIVE`.
- **P-BIZ-20 Public Artifact** — `OFFICIAL FACTS -> SAMPLE DELIVERABLE -> UNKNOWN FIELDS -> E2+ FIREWALL -> DECISION QUALITY CHECK`.
- **P-BIZ-21 E3/E4 Promotion** — `EXTERNAL BEHAVIOUR -> E3; CASH + BINDING TRANSACTION -> E4; GENERATED ARTIFACTS NEVER SUBSTITUTE`.
- **P-BIZ-22 Cash & Funding** — `PAYER -> FUNDING SOURCE -> UPFRONT/REIMBURSEMENT -> COMMITTED CASH TIMELINE -> WORKING-CAPITAL GATE`.
- **P-BIZ-23 Economics & Capacity** — `EXTERNAL PRICE -> VARIABLE COST -> OBSERVED HUMAN TIME -> CONTRIBUTION -> ARRIVAL/SERVICE CAPACITY -> SCALE/HOLD`.
- **P-BIZ-24 Self Improvement** — `DEFECT -> MINIMUM PATCH -> REGRESSION -> PROVENANCE -> DRIVE/GITHUB READBACK -> SCOPED PROMOTION/NO_OP`.

## Proof boundary
All public-only/source-only work remains `<= E2+`. K/S/E planes remain non-substitutable. Unknown economics, buyer behavior, human delivery time, legal status and qualification barriers remain explicit `null/HOLD`.
