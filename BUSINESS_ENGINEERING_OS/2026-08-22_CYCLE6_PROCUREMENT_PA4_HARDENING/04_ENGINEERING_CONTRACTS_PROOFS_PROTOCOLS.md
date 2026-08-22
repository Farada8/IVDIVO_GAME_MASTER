# CYCLE6 — ENGINEERING CONTRACTS, PROOFS, PROTOCOLS

## Modules C6M01–C6M10
1. `OfficialPackCompletenessGate`
2. `TenderQualificationCompiler`
3. `SupplierCapabilityProfileCompiler`
4. `GapCurabilityRouter`
5. `TenderClockCompiler`
6. `AwardCriteriaNullSafeExtractor`
7. `CashTimingRequirementCompiler`
8. `BidDecisionFailClosedGate`
9. `IndependentPA4PacketBuilder`
10. `ProcurementSourceFreshnessGuard`

## Contracts C6C01–C6C16
- **C6C01 FULL_PACK_BEFORE_FULL_QUALIFICATION** — no complete official pack, no complete qualification claim.
- **C6C02 OFFICIAL_PRIMARY_OVER_MIRROR** — third-party tender mirrors may aid discovery but do not supersede official documents.
- **C6C03 UNKNOWN_NEQ_MET** — unknown supplier evidence cannot satisfy a criterion.
- **C6C04 UNKNOWN_NEQ_NONCOMPLIANT** — missing evidence cannot be silently converted to failure unless the tender contract defines absence itself as failure and the absence is verified.
- **C6C05 MEAT_NEQ_WEIGHTING** — knowing that MEAT applies does not reveal criteria or weights.
- **C6C06 ESTIMATED_VALUE_NEQ_CASH_TIMING** — estimated contract value proves neither payment profile nor working-capital burden.
- **C6C07 PUBLIC_SCOPE_NEQ_WORKS_REQUIREMENTS** — listing description is not the full Works Requirements.
- **C6C08 DEADLINE_SOURCE_REQUIRED** — every deadline/clarification/site-visit clock requires source and timestamp.
- **C6C09 SUPPLIER_PROFILE_VERIFICATION_REQUIRED** — supplier capabilities remain unverified until backed by documents/current facts.
- **C6C10 REQUIREMENT_BY_REQUIREMENT_JOIN** — no opaque aggregate fit score may replace criterion-level evidence.
- **C6C11 FATAL_GAP_EXPLAINABLE** — every fatal decision must cite the unmet mandatory requirement and evidence state.
- **C6C12 CURABLE_HAS_TIME_PROOF** — `CURABLE_BEFORE_DEADLINE` requires a feasible dated remediation path.
- **C6C13 BID_EFFORT_NULL_SAFE** — bid hours/cost stay null/ranges until workload inputs exist.
- **C6C14 LEGAL_CLEARANCE_FORBIDDEN_FROM_ARTIFACT** — artifact may surface legal/compliance questions but cannot grant legal clearance.
- **C6C15 PA4_SAME_INPUTS_BLIND_REVIEW** — independent PA4 review receives the same authoritative source packet and supplier profile without first-output leakage.
- **C6C16 EVIDENCE_PLANES_NON_SUBSTITUTABLE** — PA maturity does not promote market E proof.

## Proof gates C6P01–C6P08
- **C6P01 PACK_INVENTORY_PROOF:** complete filename/revision/addendum inventory with authoritative provenance.
- **C6P02 REQUIREMENT_TRACE_PROOF:** every extracted criterion traces to a document locator.
- **C6P03 SUPPLIER_FACT_PROOF:** every MET state traces to current supplier evidence.
- **C6P04 CLOCK_PROOF:** all time-critical constraints have source, timezone and observed timestamp.
- **C6P05 CASH_PROOF:** bonds/retention/payment/insurance amounts are sourced or null.
- **C6P06 DECISION_PROOF:** BID/HOLD/NO-BID includes fatal reason(s), unknowns and proof grade.
- **C6P07 PA4_DIVERGENCE_PROOF:** independent reviewer differences are recorded rather than averaged away.
- **C6P08 NO_PROMOTION_PROOF:** PA4/PA5/E3 stay false unless their independent conditions occur.

## Protocols C6R01–C6R08
1. **AcquirePack:** fetch official package; inventory every attachment, revision and addendum; hash/store metadata; fail closed on missing pieces.
2. **CompileRequirements:** extract one criterion at a time with exact source locator; preserve ambiguity.
3. **VerifySupplier:** populate supplier profile only from current evidence; timestamp each fact.
4. **JoinAndRoute:** map criterion to supplier evidence and classify gap; never use a magic total score.
5. **Clock:** normalize all deadlines to source timezone, record clarification/site-visit dependencies and revalidate amendments.
6. **CashTiming:** separate contract value from deposits/bonds/retention/payment cycle and supplier liquidity.
7. **Decision:** authorize BID/NO-BID only when pack completeness + verified supplier + fatal-gap routing pass; otherwise HOLD.
8. **IndependentPA4:** blind second implementation/reviewer compares extracted requirements, gap states and decision; disagreements become new tests.

## Self-Improvement candidate from this run
`MISSING_AUTHORITY_IS_A_FIRST_CLASS_RESULT`: when the decisive authoritative artifact cannot be acquired, emit an explicit acquisition dependency and prevent downstream certainty. Candidate only; not promoted globally from one run.