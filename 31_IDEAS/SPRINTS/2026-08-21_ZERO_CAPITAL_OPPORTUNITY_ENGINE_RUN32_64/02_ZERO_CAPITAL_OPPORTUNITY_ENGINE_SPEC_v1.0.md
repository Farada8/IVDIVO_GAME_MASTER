# 02 — ZERO CAPITAL OPPORTUNITY ENGINE SPEC v1.0

## Mission
Find, test and scale opportunities where the Founder can obtain the **first commercial proof without new founder cash**, then use customer money, supplier terms, grant/loan/working-capital facilities or later investment only after evidence justifies them.

## Engineering modules
| ID | Module | Contract / output |
|---|---|---|
| M01 | AuthorityReconciler | `AuthoritySnapshot_v1` |
| M02 | SignalIngestor | `SignalPacket_v1` with source/date/claim |
| M03 | OpportunityNormalizer | `OpportunityCandidate_v1` |
| M04 | ZeroCashGate | PASS/FAIL + exact pre-proof cash reason |
| M05 | BuyerBeforeBuildValidator | buyer reachable + manual deliverable + payment trigger |
| M06 | EvidenceLedger | append-only `EvidencePacket_v1` |
| M07 | ProofLadder | P0–P7 state transition |
| M08 | ContractArchitect | deposit/PO/retainer/commission structure |
| M09 | TenderGrantProcurementRouter | public opportunity/support routing; no approval assumptions |
| M10 | UnitEconomicsEngine | actual time/cost/revenue/contribution after paid delivery |
| M11 | ExperimentScheduler | cheapest discriminating test first |
| M12 | RiskFirewall | legal/regulatory/reputation/cash exposure gates |
| M13 | FinanceReadinessTranslator | E4/E5 evidence → lender/grant/investor package |
| M14 | PersistenceWriter | GitHub/Drive write-through + readback |
| M15 | SelfImprovementAdapter | defect/success → candidate patch + regression |
| M16 | NextActionResolver | choose one PRIMARY + ≤2 pilots |

## State machine
`DISCOVERY → E1_SIGNAL → E2_PAIN → E3_INTEREST → E4_PAYMENT → E5_REPEAT → E6_FINANCE_READY → E7_SCALE`

Forbidden transition: `E1_SIGNAL → "MARKET PROVEN"`.

## ZeroCashGate
Strict PASS requires:
- `founder_cash_pre_proof_eur == 0`;
- no irrevocable inventory/property/equipment commitment before E4;
- no paid marketing required for first test;
- the offer can be sold before bespoke build;
- any grant requiring prior spend is classified `REIMBURSABLE`, not `ZERO_CASH`, unless a confirmed bridge exists.

## Opportunity score
Heuristic only:
- 22% cashless start;
- 18% buyer-before-build;
- 15% speed to first revenue;
- 15% authoritative demand signal;
- 10% repeatability;
- 10% finance ladder;
- 10% gross-margin potential;
- regulation and long-cycle penalties.

The evidence grade overrides score whenever they conflict.

## Self-improvement loop
`OBSERVE REAL RESULT → EARLIEST FAILURE → CHEAPEST DISCRIMINATING TEST → MINIMAL PATCH → REGRESSION → WRITE-THROUGH`.

No model-generated buyer reaction, payment, conversion rate, margin or lender decision may be written as observed evidence.
