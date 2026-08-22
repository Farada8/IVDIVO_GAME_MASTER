# CYCLE5 — NEXT64 EVIDENCE-DRIVEN PROMPTS

These are not blind autorun tasks. Execute by dependency and current constraint. IDs P33–P96 continue the completed Cycle5 Run32.

## Procurement PRIMARY — P33–P48
P33. Obtain the complete official tender pack for eTenders resource 8872468 and inventory every file/revision/addendum; do not infer unseen requirements.
P34. Build `TenderQualificationObject`: mandatory criterion -> evidence required -> supplier evidence state -> source -> fatal/nonfatal.
P35. Build a null-safe `SupplierCapabilityProfile` template for turnover, insurance, tax, references, personnel, safety, certifications, capacity and geography.
P36. Classify each qualification gap as `MET / UNKNOWN / CURABLE_BEFORE_DEADLINE / NONCURABLE / NOT_APPLICABLE`.
P37. Build deadline/clarification/site-visit clock from full documents and calculate decision deadlines without inventing absent dates.
P38. Extract award criteria, weighting, quality subcriteria and price rules; preserve ambiguity exactly.
P39. Extract mandatory site-visit and access constraints; identify evidence required to attend/comply.
P40. Extract programme, school-occupation, phasing, working-hours and completion constraints.
P41. Extract bonds, retention, payment schedule, insurance and other cash-timing requirements; keep unknown economics null.
P42. Extract subcontracting/consortium/relied-upon-entity rules and map possible delivery structures.
P43. Extract similar-project/reference requirements and design a reference-evidence matrix.
P44. Extract exact insurance levels and compare only against a verified supplier insurance profile.
P45. Extract H&S/PSCS/PSDP/competence declarations and build a compliance-evidence checklist without giving legal clearance.
P46. Build a null-safe bid-effort model: hours/cost remain ranges or null until document count, quality burden and team availability are known.
P47. Run the first real `BID / HOLD / NO-BID` engine only after P33–P46 plus a verified supplier profile; record fatal reason and proof grade.
P48. PA4 test: give the same full tender pack + supplier profile to an independent reviewer/alternate implementation and compare decision, gaps and missed fatal criteria.

## Retrofit PILOT — P49–P64
P49. Create a real-property intake object: MPRN, dwelling type, construction/occupation year, BER, occupancy, county, current systems, measures, budget and objectives.
P50. Add a pre-1940/traditional-building branch and route moisture/ventilation/fabric assumptions to specialist evidence instead of standard retrofit defaults.
P51. Compile BER/current-energy evidence requirements and define which decisions can and cannot be made without a BER.
P52. Compile heat-pump technical-assessment dependencies and prevent heat-pump route selection without required current evidence.
P53. Query current county-level One Stop Shop/provider coverage for one real property and distinguish listing from capacity/availability.
P54. Compare Individual Grant vs One Stop Shop as a vector: management burden, measure scope, assessment, timing, cash, coordination and proof requirements; no total score.
P55. Compile grant-approval validity/expiry and application timing into a live project clock.
P56. Compile reimbursement/upfront-payment timing and separate grant value from actual cash needed before/through works.
P57. Create a quote-comparison schema that normalizes scope, exclusions, VAT, grant treatment, provisional sums, warranty and schedule.
P58. Verify registered-contractor status for each proposed measure/provider at decision time; stale registry snapshots fail closed.
P59. Build a measure-sequencing dependency graph for fabric, ventilation, heating and controls using current technical guidance.
P60. Model Home Energy Upgrade Loan Scheme as a separate finance decision; no approval or affordability inference from retrofit eligibility.
P61. Build a project cash-gap timeline from deposits, milestones, grant deductions/reimbursements and finance events; unknown amounts remain null.
P62. Produce a homeowner-facing one-page Route Card and test whether it changes a real property owner's next action.
P63. Produce a contractor/OSS-facing qualification card and test whether it reduces unqualified enquiries or missing information.
P64. PA4 test: independent retrofit professional reviews the same property packet; compare route, missing evidence and unsafe assumptions.

## SME AI / Digital PILOT — P65–P80
P65. Define a schema for ingesting a real Digital for Business report without copying irrelevant or sensitive content into public artifacts.
P66. For one real workflow, measure frequency, actors, handoffs, waiting, rework and failure modes before proposing software.
P67. Establish a baseline measurement plan; time saved and euro value remain null until observed/measured.
P68. Map the workflow to candidate software categories first; vendors come later and must not drive the diagnosis.
P69. Prove whether the proposed software is genuinely new to the business and not merely added licences/modules of an existing system.
P70. Recheck current Grow Digital eligible/ineligible expenditure categories before making any grant-path recommendation.
P71. Build a co-funding/cash object: total project cost, eligible subset, grant fraction/cap and enterprise cash requirement; no approval inference.
P72. Enforce the training/configuration combined-cost cap in a sample project budget and route excess scope outside grant assumptions.
P73. Build a current LEO eligibility checklist and separate enterprise eligibility, expenditure eligibility and approval outcome.
P74. Tier AI use cases by consequence/data sensitivity and route high-risk/legal/privacy questions to appropriate authority; do not imply compliance clearance.
P75. Add human-in-the-loop, override, audit-log and failure-recovery fields to AI workflow designs where consequential decisions are affected.
P76. Add data provenance/privacy/security unknowns as explicit blockers; never let grant eligibility substitute for these checks.
P77. Compile an implementation backlog: data cleanup -> configuration -> migration -> integration -> training -> pilot -> measurement -> handover.
P78. Compile outcome metrics tied to the workflow decision: cycle time, missed handoffs, rework, backlog, conversion or other observed measure.
P79. Compare the proposed paid service against Digital for Business, vendor onboarding, public training and other free/subsidised alternatives; kill redundant scope.
P80. PA4 test: an independent SME/digital practitioner reviews the same workflow card and implementation backlog for decision utility and missing risks.

## Cross-lane engine + Self-Improvement — P81–P96
P81. Define `DecisionDelta`: what decision would the user make before vs after seeing an artifact; zero delta triggers HOLD/REJECT.
P82. Build TimeSavedNullSafeEstimator fixtures proving that no time-saving number appears until measured or sourced.
P83. Build ErrorAvoidanceEstimator fixtures separating observed errors, plausible avoided errors and monetized value.
P84. Create a multi-axis artifact rubric: completeness, freshness, null-safety, decision delta, falsifiability and next-action clarity; no opaque total score.
P85. Stress-test `ArtifactInputCompletenessGate` with missing deadlines, property fields and DfB prerequisites; fail closed.
P86. Add source half-life/revalidation rules per field class and record exactly which artifact fields go stale first.
P87. Expand `AlternativeAlreadyFreeDetector` into a substitution matrix: free/public/vendor/internal/paid alternative -> coverage -> gap -> differentiation needed.
P88. Red-team all three PA3 artifacts specifically for false confidence created by polished presentation or generated prose.
P89. Enforce portfolio WIP=3 in runtime; any fourth lane must displace, merge with or wait behind an existing lane.
P90. Re-evaluate PRIMARY/PILOT ranking using artifact decision utility, evidence accessibility and next-test kill power rather than excitement.
P91. Convert only repeated artifact failures into Self-Improvement candidates; single failures remain observations.
P92. Build canary regressions for any proposed Self-Improvement rule and prove no regression across procurement, retrofit and SME-AI lanes.
P93. PA4 cross-validation: independent model/human reviewer gets the same source packet and schema without seeing the first artifact output; compare results.
P94. Design the smallest safe real decision-use test for each lane, with no paid ad spend and no claim of buyer proof before interaction.
P95. Define PA5/E3 promotion evidence: target-user identity/class, actual decision before/after, interaction artifact, timestamp and what changed; compliments alone fail.
P96. Cycle6 eligibility gate: advance only the lane(s) that obtain PA4 or stronger evidence; archive/HOLD lanes that cannot create decision utility or differentiation.

## Dependency law
Do not execute all 64 merely because they exist. Current preferred sequence:
`P33–P48 procurement -> PA4; P49–P64 only when real property packet exists; P65–P80 only when real post-Digital-for-Business workflow exists; P81–P96 continuously as cross-lane safeguards.`