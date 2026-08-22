# OPP-37 — TEST-37 INTERNAL SEO-vs-AI DIFFERENTIAL NEGATIVE CONTROL

**Date:** 2026-08-22  
**Opportunity:** OPP-37 Tourism AI Discoverability & Bookability  
**Test type:** internal public-web negative control; no contact, no account access, no private analytics.  
**Predeclared pass rule:** across 3 declared tourism sites, at least 2 must show >=1 material, reproducible, actionable AI-specific defect not already captured by the ordinary page-level SEO/web control.  
**Evidence ceiling:** public technical observation only. This is not buyer behavior, demand, WTP, conversion uplift or transaction proof.

## Declared control model

### Ordinary page-level SEO/web control
A site is not allowed to count an “AI defect” merely because it has an obvious conventional web/SEO problem. Control checks:
1. clear entity/category/location on first-party pages;
2. indexable descriptive text;
3. relevant constraint facts on first-party pages;
4. direct booking/contact CTA or booking path;
5. usable page-level commercial information.

### Incremental AI-answerability layer
A defect counts only when the page-level SEO control is substantially usable but answer-engine grounding still has a material problem, especially:
1. contradictory first-party facts for the same entity/offering;
2. ambiguous canonical fact/action source across first-party pages;
3. stale source competing with a newer source where an answer engine could cite either;
4. material constraint fact not composable into a reliable answer despite otherwise usable pages.

The test deliberately does **not** count generic ranking weakness, missing keywords, ordinary duplicate-content hygiene, page design taste, or third-party OTA differences as AI-specific evidence.

## Site A — Pallas Karting & Adventure Centre

First-party pages inspected:
- https://www.pallaskarting.com/
- https://www.pallaskarting.com/karting/
- https://www.pallaskarting.com/terms-conditions/

### Ordinary control
PASS for the bounded test: location/category are explicit; direct booking is present; age/height constraints and current public prices are exposed; the karting product pages are indexable and commercially actionable.

### Incremental AI-grounding defect
**PASS / material fact-consistency defect.** Current first-party pages disagree on core kart specifications:
- homepage: 1500m track / Sodi SR5 up to **90kph**, family/beginners up to **55kph**;
- karting page: advanced track described as **85kph** Thunderkarts and beginners up to **55kph**;
- terms page: 1500m track **90kph**, 500m track **50kph**.

This is not merely a ranking/CTA defect: an answer engine grounding a query such as “how fast are the family and advanced karts at Pallas?” can retrieve mutually incompatible first-party values even though the ordinary booking/content path is usable.

**Actionable repair:** publish one canonical kart-spec fact table with effective date/equipment version; make homepage, karting, terms and booking surfaces reference the same source-of-truth values; retire stale equipment/speed claims.

**Reproduction:** observed in initial search retrieval and direct second-pass opens of the same first-party pages.

Result A: `INCREMENTAL_AI_DEFECT = TRUE`.

## Site B — Clissmann Horse Caravans / Glamping

First-party pages inspected:
- https://clissmannhorsecaravans.com/faq-2/
- https://clissmannhorsecaravans.com/glamping-wicklow/
- https://clissmannhorsecaravans.com/book-now/

### Ordinary control
PASS for the bounded test: the site clearly identifies the Wicklow glamping product, capacity/amenities, season, direct availability/booking route and pricing workflow.

### Incremental AI-grounding defect
**PASS / material first-party timing contradiction.** For the same glamping accommodation:
- FAQ says check-in is **4pm (16:00)** and checkout 11:00;
- glamping product page says reception/check-in is **14:00–18:00**, checkout 11:00.

The site otherwise has a strong direct-booking/content path, so the contradiction is specifically harmful to an answer engine expected to return one definitive check-in time from first-party sources.

**Actionable repair:** choose a canonical interpretation (fixed check-in time vs arrival window), add effective-date/source ownership, and synchronize FAQ/product/booking confirmation surfaces.

**Reproduction:** observed in initial retrieval and second-pass direct opens/finds on both first-party pages.

Result B: `INCREMENTAL_AI_DEFECT = TRUE`.

## Site C — Townsend House Guesthouse, Birr

First-party pages inspected:
- https://townsendhouse.ie/
- https://townsendhouse.ie/accommodation/
- supporting public discovery evidence around current direct-booking/room facts.

### Ordinary control
PASS for the bounded test: entity/location, room types, direct accommodation booking CTA, cancellation facts, parking/Wi-Fi/breakfast and contact route are publicly available.

### Incremental AI-grounding defect
**NOT PROVEN.** Legacy/indexed content and differing presentation of booking/rates may justify ordinary SEO/index-hygiene work, but this test does not have enough clean evidence to label it a distinct AI-answerability defect beyond conventional content/index maintenance.

Result C: `INCREMENTAL_AI_DEFECT = FALSE_FOR_CURRENT_TEST`.

## Threshold result

| Site | Ordinary control usable | Material incremental AI defect | Reproduced | Actionable | Counts |
|---|---:|---:|---:|---:|---:|
| Pallas | yes | yes | yes | yes | 1 |
| Clissmann | yes | yes | yes | yes | 1 |
| Townsend House | yes | not proven | n/a | n/a | 0 |

Count = **2/3**.

Predeclared internal threshold = at least 2/3.

**TEST-37 INTERNAL DIFFERENTIAL: PASS.**

## What this PASS means — and does not mean

It supports only the technical fatal assumption that an AI-specific answerability layer can identify at least some actionable defects beyond the declared ordinary page-level SEO control in the current bounded sample.

It does **not** prove:
- that tourism operators perceive this as an important problem;
- that they will share analytics/access;
- that they will implement a recommendation;
- that conversion/direct-booking revenue will improve;
- willingness to pay;
- unit economics;
- market size;
- repeatability across a larger population.

Therefore OPP-37 does **not** advance to external-signal state. Buyer-behavior stage remains gated.

## Causal effect

- `OPP37_FATAL1_INTERNAL_DIFFERENTIAL = PASS_2_OF_3`
- `OPP37_BUYER_BEHAVIOR = FALSE`
- `OPP37_EXTERNAL_TEST = NOT_EXECUTED`
- `WTP = NULL`
- `TRANSACTION = NULL`
- `PROOF_PROMOTION = FALSE`
- Next64 accounting remains **24/64**; TEST-37 is an experiment prerequisite, not another numbered prompt.
- The machine-declared next block **P25–P32** may now be engineered internally, but external use of any offer/artifact remains authorization-gated.

READBACK_MARKER: `GENERAL-BUSINESS-OPP37-TEST37-INTERNAL-PASS-2OF3-NO-BUYER-PROOF`
