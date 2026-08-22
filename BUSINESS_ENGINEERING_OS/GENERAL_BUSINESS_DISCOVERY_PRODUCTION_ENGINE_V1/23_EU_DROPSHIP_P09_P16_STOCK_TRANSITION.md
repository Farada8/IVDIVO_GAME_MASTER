# EU DROPSHIP — P09–P16 STOCK / PRIVATE-LABEL TRANSITION

**Date:** 2026-08-22  
**Status:** INTERNAL DECISION ENGINEERING / NO INVENTORY PURCHASE / NO PROFIT CLAIM  
**Parent:** Money Mechanisms comparison laboratory  
**Input:** P01–P08 screened 20 EU-stock candidates; 11 remain `ADVANCE_PRICE_SHIP_CHECK`.

## Current evidence boundary
Hertwill publicly exposes stock/product facts but candidate wholesale prices are account-gated (`Login to see prices`) and candidate destination shipping to Ireland is not currently available in the public product surface.

`WHOLESALE_COST = NULL`  
`IRELAND_SHIPPING = NULL`  
`CAC = NULL`  
`CONVERSION = NULL`  
`WTP = NULL`  
`PROFITABLE_SKUS_PROVEN = 0`

## P09 — proof before small batch
`SB-GATE-1` requires all of: verified landed-cost logic; >=20 real paid orders; >=10 independent buyers; positive observed contribution after fees/refunds/returns and observed CAC where paid acquisition is used; return rate <=10%; delivery SLA >=90%; no unresolved fatal safety/authenticity/IP/quality/supplier issue; MOQ and replenishment lead time verified; stock purchase inside predeclared stop-loss.

If CAC is unobserved because orders are organic, do not fabricate CAC to justify inventory.

## P10 — proof before private label
`PL-GATE-1` requires SB-GATE-1 plus: >=50 real paid orders; >=6 weeks of demand; no single week >40% of qualifying orders; repeat/stable-demand signal; positive post-CAC contribution; documented QC/packaging/defect remedy/traceability; differentiation with a buyer-choice test; actual IP/product-safety review; MOQ/tooling/packaging/freight inside separately approved capital-at-risk.

`50 ORDERS != PRIVATE_LABEL_PROVEN`.

## P11 — €500 / €2,000 / €5,000 scenarios
Scenario envelopes only, not recommendations or purchase authorization.
- €500: €350 inventory / €75 freight-pack reserve / €75 contingency.
- €2,000: €1,400 / €300 / €300.
- €5,000: €3,500 / €750 / €750.

`units = floor(0.70 * budget / verified_landed_unit_cost)`. If landed cost is NULL, units remain NULL.

## P12 — cash conversion / stock risk
`CCC_days = inventory_days + payout_delay_days - supplier_credit_days`.
Track supplier lead time, inbound transit, sales-velocity distribution, payout delay, return timing, reorder point and markdown horizon.

Risk states: `STOCKOUT_RISK`, `OVERSTOCK_RISK`, `MARKDOWN_RISK`, `CASH_TRAP`.

## P13 — packaging / brand differentiation
A logo alone is not differentiation. Candidate mechanisms: gift-ready packaging, original care/provenance card, functional bundle/accessory, protective storage where useful, original visual identity/story, post-purchase care/repair workflow.

Each requires `buyer_choice_hypothesis -> measurable test -> threshold -> incremental cost`.

## P14 — supplier concentration / QC
Track single supplier/brand/warehouse dependence, manufacturing traceability, unstable stock, production lead time, defect/replacement process, material/colour variation, batch quality drift, MOQ/price changes and returns/warranty economics.

`SUPPLIER_HAS_GOOD_REVIEWS != QC_CONTROL`.

## P15 — negative-contribution kill rule
DROP or stop paid acquisition when: after >=20 paid orders observed contribution after refunds/returns and CAC <=0; or two consecutive >=10-order cohorts are negative; or markdown/returns/defects consume the acquisition margin; or non-curable supplier/quality/safety risk appears.

`REVENUE != PROFIT`  
`ORDERS != UNIT_ECONOMICS_PASS`

## P16 — routing contract
- `DROP`: fatal risk, persistently negative post-CAC contribution, or stop-loss breach.
- `DROPSHIP`: fulfilable but insufficient demand/economics for stock, or batch does not improve risk-adjusted economics.
- `SMALL_BATCH`: only after SB-GATE-1 + separate capital approval.
- `PRIVATE_LABEL`: only after PL-GATE-1 + separate capital/IP/QC approval.

## Execution
P09 PASS_ENGINEERING  
P10 PASS_ENGINEERING  
P11 PASS_ENGINEERING_NULL_SAFE  
P12 PASS_ENGINEERING  
P13 PASS_ENGINEERING_HYPOTHESIS_ONLY  
P14 PASS_ENGINEERING  
P15 PASS_ENGINEERING  
P16 PASS_ENGINEERING

Decision machinery exists; no SKU has passed into stock/private label. All 11 remain `DROPSHIP_SCREENING / ECONOMICS_UNRESOLVED`.

## Next dependency
`ACCOUNT_LEVEL_WHOLESALE + SKU_LEVEL_IRELAND_SHIPPING + REAL_ORDER_COHORT`

No supplier signup, listing, advertising, purchase or inventory action is authorized.

READBACK_MARKER: `MONEY-MECHANISMS-DROPSHIP-P09-P16-STOCK-TRANSITION-NULLSAFE-NO-PROFIT-PROOF-20260822`
