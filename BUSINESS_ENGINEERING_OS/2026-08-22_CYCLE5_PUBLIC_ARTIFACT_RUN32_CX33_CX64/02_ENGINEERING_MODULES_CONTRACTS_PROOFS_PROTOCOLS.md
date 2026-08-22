# CYCLE5 PUBLIC ARTIFACT ENGINEERING MODULES / CONTRACTS / PROOFS / PROTOCOLS

**Scope:** cycle-local adapter/test layer over CURRENT Business Engineering OS. No new top-level OS, no global B/C namespace allocation, no new SI ID.

## Modules
1. `PA01 PublicArtifactProbeRunner` — bounded lawful-public-source experiment; outputs ARTIFACT_SET/PARTIAL/HOLD; sample shortfalls must be explicit.
2. `PA02 BidNoBidFieldCoverageMeter` — maps notice/attachment fields to coverage + missing-fields vector; never invents supplier eligibility.
3. `PA03 RootWorkloadDeduper` — deduplicates opportunity objects by recurring buyer job, not title/category.
4. `PA04 IncumbentBundlingKillGate` — outputs SURVIVE/MUTATE/KILL when free/included incumbents cover the job.
5. `PA05 DataReadinessKillGate` — outputs AUTOMATE/HYBRID/HUMAN_REQUIRED/HOLD; private/site data is never guessed.
6. `PA06 RecurrenceKillGate` — outputs RECURRING/PROJECT_REPEAT/ONE_OFF/HOLD; subscription requires recurring buyer work.
7. `PA07 BudgetProxyFirewall` — budget/grant/tender value => BUDGET_PROXY_ONLY unless actual buyer payment exists.
8. `PA08 ZeroCashTopologyRouter` — MANUAL_SERVICE/CUSTOMER_FUNDED/BROKER/HOLD; €0 new founder cash remains binding.
9. `PA09 NullSafeEconomicsVector` — price/CAC/conversion/margin/sales-cycle/retention remain null until measured.
10. `PA10 PublicEvidenceProvenanceReceipt` — binds source URL/title/date/claim/evidence class/root family/engine version/decision.
11. `PA11 SupersessionRevalidator` — changed source/guidance version => REVALIDATE affected descendants.
12. `PA12 PublicDataPrivacyGate` — rejects non-open personal data and unjustified profiling.
13. `PA13 HumanJudgmentBoundary` — routes accreditation/site/legal/safety/technical judgment to qualified humans.
14. `PA14 PortfolioWIPGovernor` — exactly one PRIMARY and no more than two PILOTs.
15. `PA15 SourceMechanismBridge` — book/source-passport mechanism can inform a hypothesis but cannot become current market proof.
16. `PA16 DecisionLineageDelta` — every KEEP/MUTATE/KILL records the evidence, competing hypothesis and next consequence.

## Contract pattern
Every PA module has: typed inputs; typed outputs; invariant; fail-closed cases; positive fixture; negative fixture; healthy/no-change control; evidence ceiling. A test PASS proves the contract mechanics only.

## Protocol stack
`FRESH_AUTHORITY -> PUBLIC_ARTIFACT -> PROVENANCE -> FIELD_COVERAGE -> ROOT_WORKLOAD -> BUNDLING_GATE -> DATA_READINESS -> RECURRENCE -> ZERO_CASH -> NULL_SAFE_ECONOMICS -> PRIVACY/HUMAN_BOUNDARY -> KEEP|MUTATE|KILL -> WIP_GOVERNOR -> PERSIST -> READBACK -> SELF_IMPROVEMENT_DELTA`

## Operational protocols
- **P-PA01 Fresh Authority:** read `branches/main`, current Business OS pointer and Drive library authority immediately before material writes.
- **P-PA02 Public Artifact Test:** define falsifiable claim, allowed sources, target sample, stop rule, observed sample, shortfall and disposition.
- **P-PA03 Kill-Gate Sequence:** incumbent bundling -> data readiness -> recurrence -> human/liability boundary; earliest fatal failure stops downstream over-analysis.
- **P-PA04 Zero-Cash:** manual-first, customer-funded, broker/partner, grant-backed or HOLD; no founder capex invented.
- **P-PA05 Evidence Promotion:** K/S/E proof planes are non-substitutable; public web evidence cannot satisfy Human Signal/payment.
- **P-PA06 Privacy:** reject non-open personal datasets; avoid property/person profiling without lawful necessity.
- **P-PA07 Persistence:** GitHub branch -> Drive mirror -> content readback -> fresh-main compare -> CI -> PR; stale main => rebase/salvage, no force.
- **P-PA08 Human Exit:** NO_OUTREACH remains until explicit authorization + decision-changing gap + consent/raw-answer packet.

## Proof classes
`MECHANICS_PROOF | PUBLIC_ARTIFACT_PROOF | REFERENCE_KNOWLEDGE | HUMAN_SIGNAL | PAYMENT_MARKET`.
Only the first three exist in this cycle. Human/payment/market proof is not claimed.
