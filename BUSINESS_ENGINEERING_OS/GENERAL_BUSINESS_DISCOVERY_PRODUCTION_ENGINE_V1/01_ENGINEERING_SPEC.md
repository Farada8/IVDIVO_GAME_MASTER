# GENERAL BUSINESS DISCOVERY & PRODUCTION ENGINE v1 — ENGINEERING SPEC

## 32 modules
BDP01 AuthorityRestoreRouter — restore CURRENT, evidence overlay, vertical states and live opportunity registry before work.  
BDP02 OpportunityIntakeNormalizer — normalize idea/signal/customer request/problem into OpportunityObject.  
BDP03 SignalFreshnessAndAuthorityGate — source hierarchy, freshness, contradictions and expiry.  
BDP04 BuyerJobProblemCompiler — identify user, buyer, budget owner, job, pain, delay and workaround.  
BDP05 MicroMarketDefinitionEngine — define narrow reachable market before TAM narratives.  
BDP06 WhyNowAndTriggerEngine — detect regulatory, cost, technology, deadline, demographic or workflow trigger.  
BDP07 AlternativeAndNonconsumptionMapper — current alternatives, DIY, delay, incumbent and doing-nothing path.  
BDP08 FounderAdvantageInventory — evidence-backed access, skill, asset, distribution, credibility and capital advantages.  
BDP09 FatalAssumptionRanker — rank assumptions by probability × consequence × information value, without magic total score.  
BDP10 DecisiveExperimentRouter — cheapest valid test for highest-value uncertainty.  
BDP11 CustomerEvidenceLedger — interview/behavior/request evidence with provenance and contradiction handling.  
BDP12 ValueHypothesisCompiler — measurable outcome, avoided loss, time saved, risk reduced or revenue enabled.  
BDP13 OfferArchitectureEngine — scope, deliverable, exclusions, proof, timing and acceptance criteria.  
BDP14 ArtifactPrototypeEngine — build minimum decision-valuable sample, diagnostic, mockup, report, workflow or demo.  
BDP15 PricingHypothesisEngine — price logic from value/cost/alternatives; WTP remains unknown until external evidence.  
BDP16 UnitEconomicsEngine — contribution margin, delivery effort, CAC assumptions, payback, working capital; null-safe.  
BDP17 CashConversionEngine — deposit, milestone, reimbursement, credit, receivable and founder-cash timeline.  
BDP18 RouteToMarketEngine — direct sales, channel, marketplace, tender, partnership, referral, broker or inbound.  
BDP19 CreateBrokerAcquireRouter — choose build service/product, broker opportunity, or acquire existing cash flow.  
BDP20 SalesExperimentCompiler — bounded target list, message, CTA, success/failure thresholds; no autonomous outreach.  
BDP21 ObjectionAndFailureModeEngine — price, trust, timing, switching, legal, technical, procurement and operational objections.  
BDP22 TransactionEvidenceGate — distinguish interest, meeting, quote, intent, deposit, signed order, payment and repeat purchase.  
BDP23 DeliverySystemDesigner — SOP, roles, tools, QA, handoff, scope control and exception routing.  
BDP24 CapacityAndConstraintEngine — founder hours, skills, subcontractors, capital, geography and throughput constraints.  
BDP25 RetentionRecurringValueEngine — repeat trigger, renewal logic, expansion, switching cost and customer success.  
BDP26 RiskComplianceDependencyRouter — specialist dependencies, licences, insurance, safety, tax/legal/professional boundaries.  
BDP27 PortfolioAllocationEngine — 1 PRIMARY + up to 2 PILOTS, WIP cap, kill/hold/watch rules.  
BDP28 EvidenceWeightedDecisionEngine — decision vector with fatal gates; no scalar magic score.  
BDP29 LearningLoopEngine — experiment result -> belief update -> next test -> state transition.  
BDP30 CrossLanePatternMiner — extract reusable mechanisms across construction, AI, design, hospitality, digital and procurement.  
BDP31 AdversarialBusinessRedTeam — attack demand, economics, differentiation, deliverability, cash and evidence quality.  
BDP32 SelfImprovementPromotionGate — promote only mechanisms that beat controls across real cases; no auto-promotion.

## 32 contracts
CDP01 CURRENT_BEFORE_NEW_WORK  
CDP02 IDEA_NEQ_OPPORTUNITY  
CDP03 SIGNAL_NEQ_DEMAND  
CDP04 USER_NEQ_BUYER_NEQ_BUDGET_OWNER  
CDP05 MICRO_MARKET_BEFORE_TAM  
CDP06 WHY_NOW_REQUIRED_FOR_PRIORITY  
CDP07 DO_NOTHING_IS_AN_ALTERNATIVE  
CDP08 FOUNDER_ADVANTAGE_REQUIRES_EVIDENCE  
CDP09 FATAL_ASSUMPTION_BEFORE_BUILD  
CDP10 CHEAPEST_DECISIVE_TEST_FIRST  
CDP11 INTERVIEW_NEQ_BEHAVIOR  
CDP12 VALUE_CLAIM_REQUIRES_MEASURABLE_OUTCOME  
CDP13 OFFER_HAS_SCOPE_EXCLUSIONS_ACCEPTANCE  
CDP14 PROTOTYPE_MUST_CHANGE_A_DECISION  
CDP15 PRICE_HYPOTHESIS_NEQ_WTP  
CDP16 ECONOMICS_NULLS_PRESERVED  
CDP17 REIMBURSEMENT_NEQ_ZERO_CASH  
CDP18 CHANNEL_ASSUMPTION_REQUIRES_TEST  
CDP19 CREATE_BROKER_ACQUIRE_EXPLICIT  
CDP20 OUTREACH_REQUIRES_AUTHORIZATION  
CDP21 OBJECTION_LOG_BEFORE_SCALE  
CDP22 INTEREST_NEQ_TRANSACTION  
CDP23 PAYMENT_NEQ_REPEATABILITY  
CDP24 CAPACITY_LIMITS_ARE_FIRST_CLASS  
CDP25 RETAINER_REQUIRES_RECURRING_VALUE  
CDP26 SPECIALIST_DEPENDENCY_EXPLICIT  
CDP27 PORTFOLIO_WIP_MAX_3  
CDP28 NO_MAGIC_TOTAL_SCORE  
CDP29 EVERY_TEST_UPDATES_STATE  
CDP30 CROSS_LANE_TRANSFER_REQUIRES_BOUNDARY  
CDP31 RED_TEAM_BEFORE_MAJOR_COMMITMENT  
CDP32 SELF_IMPROVEMENT_NO_AUTO_PROMOTION

## Proof gates
PG01 SOURCE_VALID — evidence provenance/freshness adequate.  
PG02 OPPORTUNITY_DEFINED — buyer/job/micro-market/trigger explicit.  
PG03 FATALS_BOUNDED — highest-risk assumptions and tests defined.  
PG04 VALUE_BOUNDED — measurable value hypothesis exists.  
PG05 OFFER_TESTABLE — scope/artifact/price hypothesis/CTA testable.  
PG06 ECONOMICS_BOUNDED — null-safe unit economics and cash timeline.  
PG07 SALES_TEST_READY — authorized bounded experiment packet exists.  
PG08 EXTERNAL_SIGNAL — real buyer behavior observed.  
PG09 TRANSACTION — deposit/order/payment evidence exists.  
PG10 DELIVERY_PROVEN — delivery acceptance and actual effort measured.  
PG11 REPEATABILITY — repeat/renewal/referral or multiple comparable wins.  
PG12 SCALE_READY — capacity/economics/channel/risks support expansion.

## Protocol families
P-BDP-01 RESTORE_AND_RECONCILE  
P-BDP-02 DISCOVER_AND_NORMALIZE  
P-BDP-03 BUYER_PROBLEM_MICROMARKET  
P-BDP-04 FATAL_ASSUMPTION_AND_VOI_TEST  
P-BDP-05 VALUE_OFFER_ARTIFACT  
P-BDP-06 PRICE_ECONOMICS_CASH  
P-BDP-07 SALES_EXPERIMENT_AND_EVIDENCE  
P-BDP-08 TRANSACTION_AND_DELIVERY  
P-BDP-09 RETENTION_AND_SCALE  
P-BDP-10 PORTFOLIO_AND_KILL  
P-BDP-11 RED_TEAM  
P-BDP-12 LEARN_AND_SELF_IMPROVE

## State machine
`S0_RESTORE -> S1_DISCOVERED -> S2_QUALIFIED -> S3_FATAL_TEST_READY -> S4_VALUE_BOUNDED -> S5_OFFER_TESTABLE -> S6_ECONOMICS_BOUNDED -> S7_SALES_TEST_READY -> S8_EXTERNAL_SIGNAL -> S9_TRANSACTION -> S10_DELIVERY_PROVEN -> S11_REPEATABILITY -> S12_SCALE_READY`.

Transitions can move backward when evidence contradicts assumptions. HOLD and KILL are valid terminal/parking outcomes. No prompt counter forces a state transition.
