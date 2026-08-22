# GENERAL BUSINESS ENGINE — MONEY MECHANISMS RUN32

**Date:** 2026-08-22  
**Purpose:** remove public-signal/tender bias and scan 32 distinct legal money mechanisms.  
**Engine:** `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1`.

## Hard rules

- `EASY_TO_VERIFY != BEST_BUSINESS`.
- `PUBLIC_SIGNAL_DENSITY != BUSINESS_ATTRACTIVENESS`.
- `MECHANISM != NICHE != OFFER`.
- `PRICE_HYPOTHESIS != WTP`.
- `GROSS_MARGIN_ESTIMATE != PROFIT`.
- `PROMPT_COUNT != PROGRESS`.
- Start-capital and time-to-first-revenue ranges below are planning estimates only.
- No external outreach, spend, listing, purchase or contract is authorized by this run.

## Current market context used

- Ireland remains highly digital: CSO reported 85% of internet users bought online in 2025; 37.5% of enterprises had e-commerce sales in 2025.
- Eurostat 2026 reports Ireland among the highest EU e-sales turnover shares.
- From 1 July 2026 Ireland applies a €3 customs duty per line item on low-value e-commerce consignments from outside the EU; VAT/IOSS obligations remain relevant.
- Etsy permits seller-designed digital downloads and seller-designed products fulfilled by production partners; marketplace/payment fees materially reduce low-ticket margins.
- Irish small-business AI adoption is growing but still far from universal, creating implementation opportunity without proving WTP.

## Run32

| # | Money mechanism | Typical start cash | Planning time to first revenue | Engine result | Cheapest decisive test |
|---|---|---:|---|---|---|
| 01 | Direct local skilled service | €50–€500 | 1–14 days | **TEST_NOW** | Define 3 fixed-scope jobs and compare real local quote demand |
| 02 | Productized service package | €0–€300 | 3–21 days | **TEST_NOW** | One outcome, one scope, one acceptance criterion, one price hypothesis |
| 03 | Service arbitrage / subcontract margin | €0–€500 | 3–21 days | **TEST_NOW** | Obtain supplier/subcontract cost bands before offering anything |
| 04 | Local lead generation sold per lead/booking | €100–€500 | 2–8 weeks | **TEST_NOW** | One niche + one area + one landing page + organic demand check |
| 05 | High-ticket B2B sourcing / brokerage commission | €0–€500 | 2–8 weeks | **TEST_NOW** | Match one real buyer problem to three credible suppliers |
| 06 | Managed project coordination | €0–€500 | 1–6 weeks | **TEST_NOW** | Map one project where coordination saves measurable owner time/risk |
| 07 | Custom commissioned creative/design work | €0–€300 | 1–6 weeks | **TEST_NOW** | Three commission packages with visual proof and bounded deliverables |
| 08 | Public procurement / tender work | €0–€1k | 2–12 weeks | **KEEP_VERTICAL** | Remains one channel only; no portfolio dominance from evidence availability |
| 09 | Used-goods / marketplace arbitrage | €100–€1k | 1–14 days | **TEST_NOW** | Track 20 sold-price spreads before buying inventory |
| 10 | Wholesale small-batch resale | €500–€2k | 1–6 weeks | **TEST_AFTER_PRODUCT** | Precompute landed cost and sell-through threshold on 3 SKUs |
| 11 | Generic non-EU dropshipping | €300–€1k | 2–8 weeks | **MUTATE** | Reject commodity catalog model unless margin survives €3/item duty, VAT, returns and paid acquisition |
| 12 | EU-supplier dropshipping | €300–€1k | 2–8 weeks | **TEST_NOW** | Find 20 products with EU stock, delivery SLA and contribution margin before ads |
| 13 | High-ticket dropshipping / direct-ship | €500–€2k | 2–10 weeks | **TEST** | Verify supplier warranty, delivery and after-sales economics on 5 products |
| 14 | Print-on-demand | €50–€500 | 1–6 weeks | **TEST_NOW** | Build 10 design/SKU hypotheses and marketplace fee economics |
| 15 | Private label after product validation | €2k–€5k+ | 1–4 months | **HOLD_SEQUENCE** | Only after a product has repeat sales under lower-risk fulfillment |
| 16 | Local/EU supplier e-commerce resale | €300–€2k | 1–8 weeks | **TEST** | Compare direct supplier terms vs marketplace prices and local availability |
| 17 | Etsy digital downloads | €20–€200 | 1–21 days | **TEST_NOW** | 10 original digital listings; model Etsy listing + transaction + payment fees |
| 18 | Templates / toolkits / licensed digital packs | €0–€200 | 1–21 days | **TEST_NOW** | Build one pack that replaces 1–3 hours of buyer work |
| 19 | Books / serial fiction / audio IP | €0–€500 | 2–12 weeks | **TEST** | One complete paid unit + retention/next-purchase signal |
| 20 | Art licensing / print rights / stock assets | €0–€300 | 2–12 weeks | **TEST** | Package 20 licensable assets with use cases and licence tiers |
| 21 | Affiliate / content commerce | €0–€500 | 2–6 months | **WATCH** | Demand/traffic proof before assuming commission income |
| 22 | Paid research / intelligence / decision pack | €0–€300 | 1–4 weeks | **TEST_NOW** | Produce one sample that changes a real internal decision |
| 23 | Micro-SaaS | €200–€2k | 1–4 months | **TEST_AFTER_PROBLEM** | Manual concierge version before writing software |
| 24 | Marketplace app / plugin / template product | €100–€1k | 1–4 months | **WATCH_TO_TEST** | Validate repeated workflow pain inside one ecosystem first |
| 25 | AI workflow implementation | €0–€500 | 1–6 weeks | **TEST_NOW** | Automate one measurable admin workflow; compare before/after minutes and errors |
| 26 | No-code automation maintenance retainer | €0–€500 | 2–8 weeks | **TEST_AFTER_IMPLEMENTATION** | Retainer only if workflow creates recurring maintenance value |
| 27 | Compliance/admin implementation pack | €0–€500 | 2–8 weeks | **HOLD_BOUNDARY** | Operational implementation only; legal/professional assurance requires specialist authority |
| 28 | SEO/local lead-generation asset | €100–€500 | 1–6 months | **TEST** | One micro-market keyword/area with measurable lead intent |
| 29 | Equipment rental | €1k–€5k | 1–8 weeks | **TEST_BEFORE_ASSET** | Measure rental demand/utilisation before purchasing equipment |
| 30 | Asset-as-a-service / production machine | €2k–€5k+ | 1–12 weeks | **MUTATE** | Broker/lease/partner first; buy only after utilisation proof |
| 31 | Buy an existing small business | €5k+ | 1–6 months | **WATCH_CAPITAL** | Search only businesses with verifiable owner earnings and financing path |
| 32 | White-label / JV / revenue-share distribution | €0–€500 | 1–8 weeks | **TEST_NOW** | Find one proven supplier/product/service missing a route-to-market you can provide |

## Run32 disposition

- `TEST_NOW`: 13
- `TEST / TEST_AFTER_*`: 10
- `MUTATE`: 2
- `WATCH / HOLD`: 6
- `KEEP_VERTICAL`: 1
- `KILL`: 0

The absence of KILL does **not** mean all 32 should be pursued. Most remain mechanisms, not active opportunities.

## Main finding

The previous engine over-selected tenders because official opportunities have unusually clean public evidence. That created an **evidence-availability bias**. The correct discovery unit is the money mechanism plus a bounded buyer problem, not the presence of a government notice.

## New local self-improvement candidate

`DISCOVERY_SOURCE_BALANCE_GATE`:
1. every broad business scan must cover service, commerce, digital/IP, software/AI, brokerage, asset and acquisition mechanisms;
2. public procurement may occupy at most one mechanism slot unless the user explicitly requests procurement;
3. ranking must use fatal gates and decision vectors, never source-count or document-volume as a proxy for attractiveness;
4. local promotion only until tested on multiple discovery cycles.

READBACK_MARKER: `GENERAL-BUSINESS-MONEY-MECHANISMS-RUN32-20260822`
