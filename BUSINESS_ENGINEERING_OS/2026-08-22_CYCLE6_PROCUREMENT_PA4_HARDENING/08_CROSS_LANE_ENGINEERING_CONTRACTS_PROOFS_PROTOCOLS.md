# CYCLE6 CROSS-LANE ENGINEERING — P81–P96

This layer is additive to PR #191 and touches no procurement P33–P48 files.

## Modules C6X-M01–C6X-M16
1. **C6X-M01 DecisionDeltaEngine** — before/after decision with null/zero-delta states.
2. **C6X-M02 TimeSavedNullSafeEstimator** — time saved only from measured/sourced times.
3. **C6X-M03 ErrorAvoidanceEstimator** — observed error delta; monetisation optional/null-safe.
4. **C6X-M04 ArtifactVectorRubric** — six explicit axes; no aggregate score.
5. **C6X-M05 ArtifactInputCompletenessGate** — missing required inputs fail closed.
6. **C6X-M06 FieldHalfLifeRegistry** — revalidation policy by field class.
7. **C6X-M07 SubstituteCoverageMatrix** — native/free/subsidised/vendor/internal coverage -> residual unsolved job.
8. **C6X-M08 FalseConfidenceGuard** — polish cannot raise proof grade.
9. **C6X-M09 PortfolioWIPGate** — hard cap 3.
10. **C6X-M10 ParetoOpportunityRouter** — non-dominated routing on decision utility/evidence access/kill power.
11. **C6X-M11 RepeatedFailureSICandidateGate** — recurrent cross-case defect required.
12. **C6X-M12 CrossLaneInvariantValidator** — PA/K/S/E, price and polish guards.
13. **C6X-M13 IndependentPA4Gate** — same packet + independent + blinded output.
14. **C6X-M14 DecisionUseTestDesigner** — smallest safe real-user decision test per lane.
15. **C6X-M15 PA5E3EvidenceGate** — real interaction record, compliments fail.
16. **C6X-M16 CycleAdvanceGate** — advance only PA4+ lanes.

## Contracts C6X-C01–C6X-C24
- C01 missing before/after decision => DecisionDelta null.
- C02 identical before/after decision => ZERO_DELTA_HOLD.
- C03 time saved requires measured or authoritative sourced times.
- C04 plausible time savings cannot be monetised as observed value.
- C05 observed errors and plausible avoided errors are different evidence types.
- C06 error monetisation requires an observed/sourced cost basis.
- C07 artifact quality is a vector, not a hidden additive score.
- C08 missing mandatory artifact input blocks dependent decision.
- C09 source half-life is field-specific and recorded as policy.
- C10 expired field fails closed until revalidated.
- C11 free/public/vendor/internal substitute coverage is evaluated before differentiation claims.
- C12 zero residual job => HOLD/RESHAPE/REJECT, not demand invention.
- C13 polished presentation cannot upgrade PA/K/S/E.
- C14 WIP >3 freezes excess lane.
- C15 portfolio routing cannot use excitement or opaque total score.
- C16 Self-Improvement candidate needs repeat failure across >=2 distinct cases.
- C17 public-only artifact cannot create E3.
- C18 unsourced price remains null.
- C19 PA4 requires an independent reviewer/implementation blind to the first output.
- C20 self-review is not independent PA4.
- C21 real decision-use tests require actual target users; design alone is not PA5/E3.
- C22 compliments alone do not promote PA5/E3.
- C23 PA5/E3 record requires user class, before/after decision, interaction artifact, timestamp and decision change.
- C24 Cycle advance requires PA4+; PA3 remains HOLD.

## Proof gates C6X-P01–C6X-P10
1. **DecisionDeltaProof** — observed decision change only.
2. **MeasuredTimeProof** — measurement/source provenance required.
3. **ObservedErrorProof** — observed event counts distinguished from scenarios.
4. **NullSafetyProof** — missing evidence returns null/HOLD.
5. **SubstitutionProof** — residual unsolved job required.
6. **ProofPlaneIsolation** — `PA != K != S != E`.
7. **WIPProof** — max 3 active market lanes.
8. **IndependentPA4Proof** — blinded independent review.
9. **RealInteractionProof** — target-user interaction required for PA5/E3.
10. **NoPromotionProof** — zero PA4 => no Cycle6 market-proof promotion.

## Protocols C6X-R01–C6X-R08
- R01 `INPUTS -> COMPLETENESS -> ARTIFACT -> DECISION BEFORE/AFTER -> DELTA/HOLD`.
- R02 `BASELINE -> OBSERVE -> AFTER -> TIME/ERROR DELTA -> OPTIONAL VALUE`.
- R03 `JOB -> SUBSTITUTES -> COVERAGE -> RESIDUAL GAP -> DIFFERENTIATE/RESHAPE/REJECT`.
- R04 `ARTIFACT -> VECTOR RUBRIC -> UNKNOWN SURVIVAL -> NEXT TEST`.
- R05 `ACTIVE LANES -> WIP GATE -> PARETO FRONT -> KEEP/FREEZE`.
- R06 `FAILURES -> GROUP BY DEFECT/CASE -> REPEAT CHECK -> SI CANDIDATE/OBSERVATION`.
- R07 `PA3 PACKET -> INDEPENDENT BLIND REVIEW -> AGREEMENT/DIVERGENCE -> PA4/HOLD`.
- R08 `REAL USER -> BEFORE DECISION -> ARTIFACT USE -> AFTER DECISION -> PA5/E3 GATE`.

## Regression
Local `test_cycle6_cross_lane_engine.py`: 16/16 PASS. This is engineering proof only; it does not create independent PA4 or market E3.
