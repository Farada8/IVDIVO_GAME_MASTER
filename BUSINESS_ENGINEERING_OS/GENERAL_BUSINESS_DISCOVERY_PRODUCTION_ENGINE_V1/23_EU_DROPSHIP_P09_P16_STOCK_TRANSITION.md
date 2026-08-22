# EU DROPSHIP — P09–P16 STOCK / PRIVATE-LABEL TRANSITION

**Date:** 2026-08-22  
**Status:** INTERNAL DECISION ENGINEERING / NO INVENTORY PURCHASE / NO PROFIT CLAIM  
**Parent:** Money Mechanisms comparison laboratory  
**Input:** P01–P08 screened 20 EU-stock candidates; 11 remain `ADVANCE_PRICE_SHIP_CHECK`.

## Current evidence boundary
Hertwill publicly exposes stock/product facts but the candidate wholesale prices are account-gated (`Login to see prices`) and candidate destination shipping to Ireland is not currently available in the public product surface. Therefore:

`WHOLESALE_COST = NULL`  
`IRELAND_SHIPPING = NULL`  
`CAC = NULL`  
`CONVERSION = NULL`  
`WTP = NULL`  
`PROFITABLE_SKUS_PROVEN = 0`

No unit count, margin, inventory return or private-label profitability is asserted from missing inputs.

---

## P09 — Proof required before moving dropship -> small batch
A SKU is **not** allowed into small-batch stock merely because it receives orders.

Predeclared transition gate `SB-GATE-1` requires all of:
1. verified supplier unit cost and destination shipping/landed-cost logic;
2. >=20 real paid orders for the same materially equivalent SKU/offer;
3. >=10 independent buyers; friends/test/self-orders excluded;
4. positive observed contribution **after** payment/platform fees, refunds/returns allowance and observed CAC where paid acquisition was used;
5. refund/cancellation/return rate <=10% over the qualifying cohort, unless category-specific evidence justifies another predeclared threshold;
6. >=90% of fulfilled orders meeting the promised delivery window, excluding buyer-caused exceptions;
7. no unresolved safety, authenticity, IP, product-quality or supplier-reliability fatal issue;
8. replenishment lead time and MOQ observed/verified;
9. stock purchase fits the experiment stop-loss without using money required for taxes/essential operations.

If CAC has not been observed because the orders were organic, the SKU may remain `DROPSHIP` but cannot use a fabricated CAC to justify inventory.

## P10 — Proof before private label
Private label is a stronger capital/operational commitment and requires `PL-GATE-1`:
1. `SB-GATE-1 = PASS`;
2. >=50 real paid orders for the core product proposition;
3. demand observed across >=6 weeks, with no single week contributing >40% of the qualifying orders;
4. at least one repeated demand signal: repeat purchase, replacement/accessory purchase, referral-attributed purchase, wait-list/reorder behaviour, or stable new-buyer sales across the qualifying period;
5. positive post-CAC contribution on the qualifying cohort;
6. supplier/manufacturer can support documented QC, packaging specification, defect remedy and traceability;
7. proposed brand/packaging differentiation has a stated buyer-choice hypothesis and can be tested before a large MOQ;
8. trademark/IP/product-safety review completed for the actual product/category before branding;
9. MOQ + tooling + packaging + freight remain inside a separately approved capital-at-risk limit.

`50 ORDERS != PRIVATE_LABEL_PROVEN`; it only opens a deeper private-label gate.

## P11 — €500 / €2,000 / €5,000 inventory scenarios
These are **scenario envelopes**, not recommendations.

For any SKU define:
- `L` = verified landed unit cost;
- `P` = observed/credible selling price;
- `F` = per-order payment/platform/fulfilment fees not already in L;
- `R` = expected return/refund allowance per order based on observed cohort;
- `C` = observed CAC per paid order, or NULL if unobserved;
- `B` = approved capital envelope.

Default capital allocation for scenario comparison only:
- 70% inventory purchase;
- 15% inbound freight/packaging/handling reserve;
- 15% contingency/markdown/defect reserve.

Maximum theoretical unit buy before MOQ/pack constraints:
`units = floor(0.70 * B / L)`

If `L` is NULL, units remain NULL.

| Envelope | Inventory allocation | Freight/pack reserve | Contingency reserve |
|---|---:|---:|---:|
| €500 | €350 | €75 | €75 |
| €2,000 | €1,400 | €300 | €300 |
| €5,000 | €3,500 | €750 | €750 |

No €5k scenario may be used simply because it produces a better unit price.

## P12 — Cash-conversion / stockout / markdown model
For stock:
`CCC_days = inventory_days + payout_delay_days - supplier_credit_days`

For prepaid small-batch purchasing, supplier credit is normally zero unless contractually verified.

Required observations:
- supplier lead time;
- inbound transit;
- sales velocity distribution, not only average;
- payout delay;
- return/refund timing;
- reorder point;
- markdown window / seasonality.

Risk states:
- `STOCKOUT_RISK`: projected days-to-stockout < verified replenishment lead time + safety buffer;
- `OVERSTOCK_RISK`: projected inventory cover > 2x predeclared sell-through horizon;
- `MARKDOWN_RISK`: required markdown makes post-CAC contribution <=0;
- `CASH_TRAP`: expected cash recovery exceeds the approved experiment horizon.

## P13 — Packaging / brand differentiation
A logo alone is not differentiation.

Candidate differentiation mechanisms for later testing:
- gift-ready packaging with measurable gift-use proposition;
- original care/provenance card that increases trust for European-made goods;
- functional bundle/accessory improving the core use case;
- category-specific protective storage/dust bag where useful;
- original visual identity and product story;
- post-purchase care/repair/replacement workflow.

Each mechanism must declare:
`buyer_choice_hypothesis -> measurable test -> success threshold -> incremental cost`.

No packaging spend is authorized by this document.

## P14 — Supplier concentration + QC risk
Hard risk vectors:
- one supplier / one brand / one warehouse dependency;
- undocumented manufacturing origin or traceability;
- unstable stock availability;
- long or volatile production lead time;
- no defect/replacement process;
- colour/material/size variation without acceptance standard;
- quality drift between dropship sample and batch production;
- supplier changes price/MOQ after demand is proven;
- returns address or warranty workflow becomes uneconomic.

Before stock, record:
`lot/sample acceptance -> defect taxonomy -> photo/evidence protocol -> remedy -> replacement/refund owner`.

`SUPPLIER_HAS_GOOD_REVIEWS != QC_CONTROL`.

## P15 — Kill rule for sales with negative contribution
A product is killed or paid acquisition is stopped when any predeclared condition is met:

1. after >=20 paid orders, observed contribution after refunds/returns and CAC is <=0; or
2. two consecutive >=10-order cohorts show negative post-CAC contribution; or
3. a required markdown pushes expected contribution <=0; or
4. return/defect costs consume the gross-margin buffer needed for acquisition; or
5. supplier/quality/safety failure creates a non-curable customer-risk condition.

Sales volume never overrides negative contribution.

`REVENUE != PROFIT`  
`ORDERS != UNIT_ECONOMICS_PASS`

## P16 — Routing contract
### DROP
Use when:
- deterministic fatal product/supplier/legal/quality problem exists; or
- post-CAC contribution is persistently <=0 under the P15 rule; or
- required inventory risk breaches stop-loss.

### DROPSHIP
Use when:
- product is technically fulfilable;
- demand/economics evidence is still insufficient for stock; or
- product works but verified batch economics do not improve risk-adjusted contribution enough.

### SMALL_BATCH
Use only when:
- `SB-GATE-1 = PASS`;
- inventory scenario fits stop-loss;
- replenishment/QC are acceptable;
- batch economics are demonstrably better than dropship economics after carrying/markdown risk.

### PRIVATE_LABEL
Use only when:
- `PL-GATE-1 = PASS`;
- differentiated specification/branding has a buyer-choice test;
- QC/traceability/IP/safety gates are closed;
- capital/MOQ is separately approved.

## P09–P16 execution disposition
`P09 PASS_ENGINEERING`  
`P10 PASS_ENGINEERING`  
`P11 PASS_ENGINEERING_NULL_SAFE`  
`P12 PASS_ENGINEERING`  
`P13 PASS_ENGINEERING_HYPOTHESIS_ONLY`  
`P14 PASS_ENGINEERING`  
`P15 PASS_ENGINEERING`  
`P16 PASS_ENGINEERING`

This means the **decision machinery** exists. It does not mean any SKU has passed into small batch or private label.

## Next dropship evidence dependency
`ACCOUNT_LEVEL_WHOLESALE + SKU_LEVEL_IRELAND_SHIPPING + REAL_ORDER_COHORT`

Until those exist, all 11 candidate SKUs remain:
`DROPSHIP_SCREENING / ECONOMICS_UNRESOLVED`.

READBACK_MARKER: `MONEY-MECHANISMS-DROPSHIP-P09-P16-STOCK-TRANSITION-NULLSAFE-NO-PROFIT-PROOF-20260822`
