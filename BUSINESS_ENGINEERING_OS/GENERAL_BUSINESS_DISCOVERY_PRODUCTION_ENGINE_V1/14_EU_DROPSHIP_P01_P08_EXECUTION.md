# MONEY MECHANISMS — EU-SUPPLIER DROPSHIPPING P01–P08

**Date:** 2026-08-22  
**Status:** INTERNAL_SCREENING_COMPLETE / ECONOMIC_GATE_BLOCKED_BY_WHOLESALE_AND_DESTINATION_SHIPPING_VISIBILITY  
**External action:** NONE. No account signup, listing, advertising, supplier contact, spend, inventory purchase or contract.

## P01 — hard rejection filters

Reject before product research if any applies:
1. prescription/controlled/age-restricted products;
2. supplements, cosmetics with claim/compliance uncertainty, medical/health devices;
3. electrical/battery products without product-specific conformity evidence;
4. toys/children's safety products as first experiment unless CE/GPSR documentation and liability route are verified;
5. highly fragile glass/ceramic;
6. apparel/footwear as first experiment where size/fit returns dominate;
7. food/perishables/live plants;
8. oversized furniture or freight-heavy goods before destination shipping is known;
9. products where brand approval or territory rights are unresolved;
10. products whose wholesale price + destination shipping are hidden cannot pass the economic gate; they may only remain candidates.

Consumer/ecommerce controls for Ireland/EU:
- most Irish online B2C purchases have a 14-day cancellation right;
- product safety/traceability duties apply to online sellers under EU product rules/GPSR;
- intra-EU distance sales can create VAT/OSS obligations depending on selling pattern;
- from 1 July 2026, direct low-value non-EU ecommerce imports into Ireland face €3 customs duty per item line, reinforcing the EU-stock-first experiment.

## P02 — 20 candidate products / four bounded niches

All candidates were observed in current Hertwill public catalogue/product pages. Hertwill is EU-based and states that most products ship across the EU, but Ireland eligibility, origin and shipping cost must be verified per SKU using the catalogue `Ships to` data before launch.

### Niche A — premium European work/tech carry
1. Craftory — Slim Note Sack — Estonia — in stock — 13-inch laptop/document sleeve.
2. Craftory — Briefcase Model Brief — Estonia — in stock — work briefcase.
3. Tairi Roosve — Leather Phone Bag — Estonia — in stock — compact phone/card carry.
4. NOEL — Multifunctional 3in1 Bag Triple — Estonia — in stock — laptop/work/travel bag.
5. e leriin seim — Crossbody Leather Bag TOURIST — Estonia — in stock / made-to-order 5–10 working days.

### Niche B — premium European handbags / design accessories
6. Gerda Retter Design — FACET shoulder bag — Estonia — in stock.
7. Craftory — Leather Handbag Half Moon — Estonia — in stock.
8. RR — BOX Bag — Latvia — in stock.
9. Zelma Kraft — Small Briefcase Handbag — Latvia — in stock / made-to-order 14 working days.
10. RR — Structured Tote Bag — Latvia — in stock.

### Niche C — small home/spa textiles
11. LOKO — Kitchen Towel Pärnumaa — Estonia — in stock.
12. LOKO — Kitchen Towel Harjumaa — Estonia — in stock.
13. LOKO — Kitchen Towel Hiiumaa Kaheksakanna — Estonia — in stock.
14. RÄTT — Hair Wrap for Women, Cotton Terry — Estonia — selected colours in stock.
15. RÄTT — Hair Wrap for Women, Cotton Waffle — Estonia — selected colours in stock.

### Niche D — design-led pet/home products
16. Labbvenn — Rico Cat/Dog Feeder — made in Europe — in stock.
17. Labbvenn — Rino Blanket — made in Europe — in stock.
18. Labbvenn — Finno Cushion — made in Europe — in stock.
19. Labbvenn — Oslo Cushion — made in Europe — in stock.
20. Labbvenn — Elva Dog Carrier & Personal Bag — European design/brand, in stock.

## P03 — supplier / fulfilment passport

### Hertwill
- company: Hertwill OÜ, Estonia, EU;
- model: automated dropshipping for Shopify/WooCommerce/Wix;
- inventory: no upfront inventory / no MOQ under platform model;
- free plan: up to 5 products;
- payment: merchant pays wholesale price + shipping after customer order and before fulfilment;
- EU delivery guidance: typically 3–8 business days from European warehouses;
- returns/exchanges: supported; exact route and cost product/destination dependent;
- warranty: platform states 2 years;
- multi-brand cart risk: different brands ship separately and incur separate shipping charges; platform states ~95% of orders are single-brand;
- exact product wholesale, shipping origin and destination shipping: account/catalogue data required;
- Ireland availability: platform says it serves EU stores and most products ship across EU, but each SKU must pass the `Ships to Ireland` check before selection.

### Alternative supplier networks retained as redundancy
- Syncee: EU supplier marketplace; supports multiple EU suppliers, automated product/order sync; wholesale data generally account-gated.
- AppScenic: EU supplier network with automated ordering and EU warehouse filters; exact supplier/product economics require product-level verification.
- vidaXL: 90,000+ products and European warehouse/dropshipping infrastructure, but direct-to-consumer price transparency creates a strong commodity-price negative control.

Supplier concentration rule: do not launch a store whose economics depend on one platform until at least one alternate route is mapped.

## P04 — null-safe contribution model

For each SKU collect:
- `P_gross`: customer checkout price;
- `VAT`: actual VAT treatment for destination/product;
- `W`: wholesale product cost;
- `S`: supplier shipping to destination;
- `PF`: payment/platform fee;
- `RA`: expected returns/refund allowance;
- `CS`: customer-service/exception allowance;
- `CAC`: observed acquisition cost only; NULL pre-test.

`PRE_CAC_CONTRIBUTION = P_gross - VAT - W - S - PF - RA - CS`

`POST_CAC_CONTRIBUTION = PRE_CAC_CONTRIBUTION - CAC`

Current state for all 20:
`W = UNKNOWN`, `S_TO_IRELAND = UNKNOWN`, `CAC = NULL`.
Therefore none can be labelled profitable.

## P05 — structural reject / hold / advance

### ADVANCE_TO_PRICE_SHIP_CHECK
A1 Slim Note Sack
A2 Briefcase Model Brief
A3 Leather Phone Bag
A4 Triple 3in1 Bag
A6 FACET shoulder bag
A7 Half Moon handbag
A8 BOX Bag
A10 Structured Tote
D16 Rico feeder
D17 Rino blanket
D20 Elva carrier

Rationale: differentiated European design, no apparel sizing, current stock shown, plausible higher AOV. Economic pass remains blocked.

### HOLD_LOW_AOV_BUNDLE_OR_COLLECTION_ONLY
C11 Pärnumaa towel
C12 Harjumaa towel
C13 Hiiumaa towel
C14 Cotton Terry Hair Wrap
C15 Cotton Waffle Hair Wrap

Rationale: small/light/low return risk but likely low ticket; shipping/payment/CAC can overwhelm unit margin. Test only as same-brand collection/free-shipping-threshold logic, not invented multi-SKU synced bundles.

### HOLD_FULFILMENT_OR_BULK_RISK
D18 Finno Cushion
D19 Oslo Cushion

Rationale: bulky soft goods; destination shipping must be known.

### HOLD_LONG_LEAD
A5 TOURIST made-to-order 5–10 workdays
A9 Small Briefcase Handbag made-to-order 14 workdays

Rationale: lead time adds conversion/cancellation/service risk.

## P06 — three offer forms

1. `SINGLE_HERO_SKU`: one differentiated product, one clear use case, simple fulfilment.
2. `CURATED_SINGLE_BRAND_COLLECTION`: several related products from one brand; avoids multi-brand split-shipping where possible.
3. `PROBLEM_SOLUTION_STORE`: store narrative around one job (e.g. premium work carry or design-led pet home), but keep individual synced SKUs rather than fake bundles.

Do not create multi-product bundles that break supplier stock/order synchronisation.

## P07 — three internal landing/listing concepts

### Concept 1 — European Work Carry
Positioning: durable, design-led work bags and sleeves made in Europe; not commodity laptop accessories.
Hero candidates: Slim Note Sack / Model Brief / Triple 3in1.
Proof needed: exact delivered cost to Ireland, direct-brand price comparison, returns, brand approval.

### Concept 2 — Nordic/European Home Textile Gifts
Positioning: small, useful textile gifts with genuine regional design provenance.
Hero candidates: LOKO kitchen towels / RÄTT hair wraps.
Proof needed: sufficient AOV without forced bundles; shipping threshold economics; search demand.

### Concept 3 — Pet Products That Belong in the Interior
Positioning: pet equipment as interior design rather than generic pet-supply catalogue.
Hero candidates: Rico feeder / Rino blanket / Elva carrier.
Proof needed: shipping volume, comparable Irish/EU retail prices, return rate and material/product-compliance details.

No page was published.

## P08 — red team / commodity substitution

Fatal risks:
1. wholesale and Ireland shipping are currently hidden -> economic ranking impossible;
2. direct brand/marketplace retail may compress price freedom;
3. paid CAC can erase apparently attractive gross spread;
4. 14-day online withdrawal obligations mean merchant must model returns even when supplier accepts them;
5. product-safety/traceability is the merchant's problem too, not only the fulfilment platform's;
6. multi-brand orders can create duplicate shipping charges;
7. handcrafted/made-to-order lead time can damage conversion and cancellation experience;
8. premium-brand dropshipping needs credible merchandising, not generic copied supplier pages;
9. marketplace/platform claims about merchant success are not independent demand evidence;
10. free supplier account/product-price access is the next information gate; it is not external market proof.

## P01–P08 disposition

`SCREENING_COMPLETE`  
`20_CANDIDATES_DISCOVERED`  
`11_ADVANCE_TO_PRICE_SHIP_CHECK`  
`5_HOLD_LOW_AOV`  
`2_HOLD_BULK_SHIPPING`  
`2_HOLD_LONG_LEAD`  
`PROFITABLE_SKUS_PROVEN = 0`  
`WTP = NULL`  
`CAC = NULL`  
`TRANSACTIONS = 0`

### Next highest-value dependency
Obtain product-level wholesale price + shipping-to-Ireland + Ireland eligibility for the 11 advanced candidates. Without that, P04/P05 cannot produce a defensible contribution-margin shortlist.

READBACK_MARKER: `MONEY-EU-DROPSHIP-P01-P08-SCREENED-20-CANDIDATES-0-PROFIT-PROOF`
