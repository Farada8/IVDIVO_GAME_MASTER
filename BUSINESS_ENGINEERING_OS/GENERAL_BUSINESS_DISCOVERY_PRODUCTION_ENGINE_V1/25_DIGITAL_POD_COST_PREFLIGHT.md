# DIGITAL / POD COST PREFLIGHT — 2026-08-22

**Status:** INTERNAL COST + ASSET READINESS / NO LISTING / NO WTP CLAIM

## Purpose
Close the next dependency left by the P17–P24 Digital/POD lane using actual Drive artwork files plus current first-party Printful/Etsy cost inputs. This artifact does not create a market proof, listing, sale, WTP observation or authorization to publish/spend.

## Real Drive assets inspected

| Asset | Pixels | Native ratio | 4×6 effective DPI | 5×7 crop effective min DPI | 8×12 effective DPI | Readiness |
|---|---:|---:|---:|---:|---:|---|
| `house_many_windows_board.png` | 1536×1024 | 3:2 landscape | 256 | ~205 | 128 | CONCEPT_BOARD_NOT_RETAIL_MASTER |
| `women_carry_memory_board.png` | 1536×1024 | 3:2 landscape | 256 | ~205 | 128 | CONCEPT_BOARD_NOT_RETAIL_MASTER |
| `giulio_hyperreal_railway.png` | 1024×1536 | 2:3 portrait | 256 | ~205 | 128 | ARTWORK_CANDIDATE_SMALL_FORMAT_ONLY_WITH_CURRENT_FILE |

Printful general guidance: at least 150 DPI; paper products are best at ~300 DPI. Therefore:
- 4×6: technically above minimum; below ideal 300 DPI.
- 5×7: technically above minimum after crop; below ideal 300 DPI.
- 8×12: below the 150-DPI minimum with current files.

`PIXELS_EXIST != PRINT_MASTER_READY`.
`BOARD_ASSET != RETAIL_ARTWORK_MASTER`.

## Content gate
The first two assets contain presentation-board copy, explanatory panels and design-study layout. They are valuable source/design assets but should not be silently sold as finished wall art. A clean artwork extraction/re-render is required.

The railway image is the strongest current standalone visual candidate, but still requires:
1. provenance record;
2. clean print master;
3. crop/safe-area review;
4. sRGB export;
5. resolution gate for selected physical format;
6. final human visual QA.

## Current first-party fulfillment inputs
Observed 2026-08-22:
- Printful Enhanced Matte Paper Poster: catalog floor **€6.54 incl. VAT**; Europe small-poster flat shipping **$5.79**.
- Printful Enhanced Matte Paper Framed Poster: catalog floor **€20.17 incl. VAT**; Europe small-framed-poster flat shipping **$7.49**.
- Printful Standard Postcard 4×6: **€1.57 incl. VAT**; Europe postcard shipping **$4.09**, +$0.10 per additional postcard.
- Ireland is in Printful's Europe shipping region.

FX used only for this preflight envelope: $1 ≈ €0.854922 (2026-08-22 converter snapshot). Currency movement and Printful fulfillment location can change final charge.

Derived current shipping approximation:
- small poster: ~€4.95;
- small framed poster: ~€6.40;
- one postcard: ~€3.50;
- three postcards in one shipment: ~€3.67.

## Etsy current fee inputs
Observed current policy:
- listing fee: $0.20 per listing/renewal;
- transaction fee: 6.5%;
- Ireland Etsy Payments processing: 4% + €0.30.

For a conservative per-order preflight, the $0.20 listing fee is converted to ~€0.17 and included. Offsite Ads, VAT charged on Etsy fees where applicable, refunds, replacements and paid acquisition are NOT included in the envelope below and can only reduce contribution.

## Test-price envelopes — NOT WTP
These prices are synthetic test points for sensitivity analysis only. They are not recommended prices and do not prove willingness to pay.

Assume customer-facing price includes shipping and no paid ads.

### Small unframed poster — catalog-floor envelope
Fulfillment floor ≈ €6.54 + €4.95 = **€11.49**.

| Synthetic retail | Etsy fee envelope | Pre-CAC contribution | Contribution % |
|---:|---:|---:|---:|
| €19.90 | ~€2.56 | ~€5.85 | ~29.4% |
| €24.90 | ~€3.09 | ~€10.32 | ~41.5% |
| €29.90 | ~€3.61 | ~€14.80 | ~49.5% |

### Small framed poster — catalog-floor envelope
Fulfillment floor ≈ €20.17 + €6.40 = **€26.57**.

| Synthetic retail | Etsy fee envelope | Pre-CAC contribution | Contribution % |
|---:|---:|---:|---:|
| €39.90 | ~€4.66 | ~€8.67 | ~21.7% |
| €49.90 | ~€5.71 | ~€17.62 | ~35.3% |
| €59.90 | ~€6.76 | ~€26.57 | ~44.4% |

Current artwork files do not qualify for the 8×10+ framed route without a new print master, so these are economics-only envelopes, not product-ready SKUs.

### Three-card 4×6 set
Product ≈ 3×€1.57 = €4.71; shipping ≈ €3.67; fulfillment ≈ **€8.38**.

| Synthetic retail | Etsy fee envelope | Pre-CAC contribution | Contribution % |
|---:|---:|---:|---:|
| €14.90 | ~€2.04 | ~€4.49 | ~30.1% |
| €17.90 | ~€2.35 | ~€7.17 | ~40.1% |
| €19.90 | ~€2.56 | ~€8.96 | ~45.0% |

4×6 is the strongest current technical fit for the existing 3:2 assets at 256 DPI. This still does not prove buyer demand.

## Freshness warning
Printful currently announces product-price changes effective **2026-08-27**. Therefore this cost envelope is deliberately short-lived and MUST be refreshed before any actual listing or external test after that date.

`CURRENT_PRICE != FUTURE_PRICE`.
`CATALOG_FLOOR != FINAL_ORDER_COST`.

## Routing decision
- `house_many_windows_board.png` → KEEP_AS_SOURCE / CREATE_CLEAN_PRINT_MASTER.
- `women_carry_memory_board.png` → KEEP_AS_SOURCE / CREATE_CLEAN_PRINT_MASTER.
- `giulio_hyperreal_railway.png` → ADVANCE_TO_CLEAN_MASTER + PROVENANCE + SMALL_FORMAT_MOCKUP.
- 4×6 card-set route → ENGINEERING-ELIGIBLE after provenance/master QA.
- 5×7 poster route → ENGINEERING-ELIGIBLE after clean master/crop QA.
- 8×12+ wall-art route → HOLD_RESOLUTION until new master >=150 DPI at target size (preferably 300 DPI for paper).
- framed route → HOLD_PRINT_MASTER despite viable synthetic economics.

## Evidence boundary
- listings published = 0
- paid orders = 0
- WTP = NULL
- CAC = NULL
- conversion = NULL
- profitable SKU proven = 0
- external action authorized = false

## Next causal action
`CREATE_3_CLEAN_PRINT_MASTERS + PROVENANCE_RECORD + REFRESH_COSTS_AFTER_2026-08-27 -> INTERNAL_MOCKUP_GATE`.

Only after that can an explicitly authorized market test collect click/checkout/payment evidence.

READBACK_MARKER: `MONEY-MECHANISMS-POD-COST-PREFLIGHT-3ASSETS-PRINTMASTER-HOLD-NO-WTP-20260822`
