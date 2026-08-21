# MURAL / PUBLIC ART BUSINESS ENGINE — MODULES B81–B112

## B81 — MuralOpportunityIngestor
Normalize public-art/mural opportunities into typed objects with source, budget, deadline and commission type.

## B82 — DeadlineSLAEngine
Compute deadline state and urgency while refusing to invent missing clock times.

## B83 — EligibilityGate
Fail closed on residency, geography, experience, team or professional-status eligibility.

## B84 — BriefRequirementCompiler
Convert artist brief into exact deliverable checklist and evidence map.

## B85 — SiteSuitabilityRouter
Route wall/garden/standalone/indoor/site-specific requirements before concept selection.

## B86 — ArtformFitClassifier
Separate mural, permanent public art, temporary work, socially engaged residency and hybrid commissions.

## B87 — PortfolioEvidenceMapper
Map each criterion to actual portfolio evidence; unsupported experience remains gap.

## B88 — ConceptReuseGraph
Reuse concept mechanisms without pretending site-specific work is transferable unchanged.

## B89 — LocalHistoryEvidenceBinder
Bind every historical claim to a source/evidence status.

## B90 — CommunityEngagementPlanner
Represent participation method, safeguarding, decision rights, feedback and outputs.

## B91 — VisualImpactModel
Evaluate silhouette, focal hierarchy, distance readability and landmark potential.

## B92 — ViewingDistanceLegibilityGate
Require defined primary viewing zones and minimum readable scales.

## B93 — TrompeLOeilFeasibilityGate
Check viewpoint, occlusion, wall geometry and perspective feasibility for illusionistic work.

## B94 — SurfaceConditionAssumptionGate
No material system lock until substrate/moisture/coating condition is known.

## B95 — AccessScaffoldMEWPPlanner
Separate access method, permits, ground condition, exclusion zones and contractor dependencies.

## B96 — WeatherWindowRiskModel
Model Irish exterior-paint weather and cure-window risk; exact production dates remain uncertain until site plan.

## B97 — PaintSystemDurabilityRouter
Select candidate primer/paint/clearcoat families from substrate/environment, not style alone.

## B98 — MaintenanceLifecycleModel
Record expected inspection, cleaning, touch-up, graffiti removal and repaint responsibilities.

## B99 — HealthSafetyDocsCompiler
Compile RAMS-like inputs, working-at-height controls, public segregation and contractor interfaces.

## B100 — InsuranceRequirementRouter
Route Public Liability, Employers Liability and Professional Indemnity requirements from brief/work method.

## B101 — PermissionPlanningGate
Track owner consent, planning/roads/signage/licence dependencies without claiming approval.

## B102 — CopyrightProvenanceBinder
Bind original concept/image assets to hashes, authorship records, licences and third-party references.

## B103 — BidBudgetCompiler
Build line-item budget: artist fee, design, research, community, materials, access, contractors, travel, install, insurance, documentation, contingency, VAT.

## B104 — ArtistFeeProtectionGate
Expose artist fee separately; advisory target range is planning guidance, not universal rule.

## B105 — ContingencyInflationGate
Carry explicit contingency and stale-quote flags.

## B106 — CashTimingMilestonePlanner
Model deposits/milestones/outflows separately from accounting margin.

## B107 — BidEffortValueModel
Estimate application effort, reusable-asset leverage, deadline risk and evidence value before spending.

## B108 — BidNoBidDecisionEngine
Produce vector decision KEEP/HOLD/KILL with reasons; no magic aggregate score.

## B109 — SubmissionPackAssembler
Assemble CV, portfolio, proposal, visuals, technical method, programme, maintenance, budget and declarations.

## B110 — PublicEvidenceScorecard
Reuse K/S/E proof planes and prevent public-call evidence from becoming willingness-to-pay/win claims.

## B111 — PortfolioReuseLearningLoop
Turn each bid into reusable verified assets, criterion evidence and failure patterns.

## B112 — MuralSelfImprovementBridge
Feed only real pilot findings to SI lifecycle; synthetic tests stay DISCOVERY_ONLY.
