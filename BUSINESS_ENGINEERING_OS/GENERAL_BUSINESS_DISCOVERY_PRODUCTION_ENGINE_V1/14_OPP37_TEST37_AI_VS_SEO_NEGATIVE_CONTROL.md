# OPP-37 — TEST-37 INTERNAL SEO-vs-AI DIFFERENTIAL NEGATIVE CONTROL

**Date:** 2026-08-22  
**Opportunity:** OPP-37 Tourism AI Discoverability & Bookability  
**Test type:** internal public-web negative control; no contact, no account access, no private analytics.  
**Predeclared pass rule:** across 3 declared tourism sites, at least 2 must show >=1 material, reproducible, actionable AI-specific defect not already captured by the ordinary page-level SEO/web control.  
**Evidence ceiling:** public technical observation only. This is not buyer behavior, demand, WTP, conversion uplift or transaction proof.

## Ordinary control vs incremental AI layer

Ordinary control checks: clear entity/category/location, indexable descriptive text, relevant constraint facts, direct booking/contact path, and usable commercial information.

An incremental AI-answerability defect counts only when ordinary control is substantially usable but answer-engine grounding still has a material problem: contradictory first-party facts, ambiguous canonical facts/actions, competing stale/current first-party statements, or a material constraint that cannot be composed reliably into one answer.

Generic rankings, missing keywords, ordinary duplicate-content hygiene, visual taste, and third-party OTA differences do not count.

## Site A — Pallas Karting & Adventure Centre

First-party verification coordinates:
- https://www.pallaskarting.com/
- https://www.pallaskarting.com/karting/
- https://www.pallaskarting.com/terms-conditions/

Ordinary control: PASS for this bounded test. Location/category, direct booking, age/height constraints, prices and commercial pages are available.

Incremental AI defect: TRUE. Current first-party pages disagree on core kart specifications:
- homepage: 1500m Sodi SR5 up to 90kph; 500m family/beginners up to 55kph;
- karting page: advanced Thunderkarts 85kph; beginners up to 55kph;
- terms page: 1500m 90kph; 500m 50kph.

An answer engine asked a simple factual question about kart speeds can therefore ground to mutually incompatible first-party values even though the ordinary booking/content path is usable.

Actionable repair: one canonical kart-spec fact table with effective date/equipment version; all homepage, product, terms and booking surfaces reference that source of truth; obsolete claims retired.

Result A: `INCREMENTAL_AI_DEFECT = TRUE`.

## Site B — Clissmann Horse Caravans / Glamping

First-party verification coordinates:
- https://clissmannhorsecaravans.com/faq-2/
- https://clissmannhorsecaravans.com/glamping-wicklow-2/

Ordinary control: PASS for this bounded test. Product, amenities, direct availability/booking flow and practical visitor information are available.

Incremental AI defect: TRUE. For the glamping product, current first-party pages expose different check-in statements:
- FAQ: glamping check-in 4pm / 16:00, checkout 11am;
- glamping product page: reception/check-in from 14:00 to 18:00, checkout 11:00.

The two statements may represent a fixed check-in time vs an arrival/reception window, but the site does not expose a canonical interpretation. That ambiguity is material for an answer engine expected to return one precise check-in answer.

Actionable repair: define the canonical rule (fixed check-in vs arrival window), assign source ownership/effective date, and synchronize FAQ, product and booking-confirmation surfaces.

Result B: `INCREMENTAL_AI_DEFECT = TRUE`.

## Site C — Townsend House Guesthouse, Birr

First-party coordinates:
- https://townsendhouse.ie/
- https://townsendhouse.ie/accommodation/

Ordinary control: sufficiently usable for the bounded comparison.

Incremental AI defect: NOT PROVEN. Weaknesses observed around indexed/legacy presentation can be explained by conventional SEO/index hygiene. They are deliberately not promoted to an AI-specific finding.

Result C: `INCREMENTAL_AI_DEFECT = FALSE_FOR_CURRENT_TEST`.

## Threshold

| Site | Ordinary control usable | Material incremental AI defect | Reproduced | Actionable | Counts |
|---|---:|---:|---:|---:|---:|
| Pallas | yes | yes | yes | yes | 1 |
| Clissmann | yes | yes | yes | yes | 1 |
| Townsend House | yes | not proven | n/a | n/a | 0 |

Count = **2/3**. Predeclared threshold = **>=2/3**.

**TEST-37 INTERNAL DIFFERENTIAL: PASS.**

## Evidence boundary

This supports only the bounded technical assumption that an AI-answerability audit can expose actionable first-party fact-grounding defects beyond the declared ordinary page-level web control in this sample.

It does not prove operator pain, buyer role, analytics sharing, implementation behavior, conversion uplift, WTP, unit economics, market size, transaction or repeatability.

Therefore:
- `OPP37_FATAL1_INTERNAL_DIFFERENTIAL = PASS_2_OF_3`
- `OPP37_BUYER_BEHAVIOR = FALSE`
- `OPP37_EXTERNAL_TEST = NOT_EXECUTED`
- `WTP = NULL`
- `TRANSACTION = NULL`
- `PROOF_PROMOTION = FALSE`
- Next64 accounting remains 24/64; TEST-37 is a prerequisite experiment, not another numbered prompt.
- P25–P32 may be engineered internally; external use remains authorization-gated.

## Freshness / coexistence

Fresh first-party web verification was repeated on 2026-08-22 before persistence. The concurrently merged Money Mechanisms Run32 is a discovery overlay and explicitly records that the old OPP-33/36/37 WIP is not invalidated. TEST-37 changes no Money Mechanisms accounting or authority.

READBACK_MARKER: `GENERAL-BUSINESS-OPP37-TEST37-INTERNAL-PASS-2OF3-NO-BUYER-PROOF`
