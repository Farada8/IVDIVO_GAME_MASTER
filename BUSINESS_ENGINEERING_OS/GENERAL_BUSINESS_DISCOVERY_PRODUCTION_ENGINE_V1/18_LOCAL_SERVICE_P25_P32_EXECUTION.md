# MONEY MECHANISMS — LOCAL SERVICE + CUSTOMER ACQUISITION P25–P32

Date: 2026-08-22
Status: INTERNAL_SERVICE_ARCHITECTURE_COMPLETE / NO_OUTREACH_NO_SPEND
External action: NONE

## P25 — bounded local micro-market
Micro-market: Dublin homeowner exterior-house repaint, starting with ordinary terraced and semi-detached houses where the work can be surveyed and scoped without specialist structural repair.
Buyer job: make the exterior look cared-for and weather-protected without coordinating separate preparation, painting, access and cleanup providers.

Current 2026 seller-published Dublin price guides sampled for this run show exterior retail reference bands of roughly EUR1,200–2,500 for terraced homes, EUR1,800–3,800 for semi-detached homes, and EUR2,500–5,500+ for detached homes. One current source gives a two-painter crew reference around EUR350–500/day. These are market references only, not our costs, not verified transaction data, and not an instruction to quote at those levels.

## P26 — three fixed-scope offer hypotheses
PKG-A EXTERIOR WALLS REFRESH: survey, protection, routine surface preparation, spot primer where needed, two coats to agreed wall surfaces, cleanup. Major repairs, complex access and extra trim surfaces are separate.
PKG-B EXTERIOR FULL SHELL PAINT: PKG-A plus agreed fascia, soffit, downpipe and trim surfaces where substrate and access are suitable.
PKG-C PREP-HEAVY EXTERIOR RECOVERY: materially more scraping, filling and spot priming, but still excludes structural or major render repair. Site survey required.
Acceptance for every package: signed surface scope, before/after photos, obvious misses/runs corrected, cleanup complete, punch-list closed.

## P27 — delivery economics
DIRECT contribution:
CM_DIRECT = PRICE_EX_VAT_IF_APPLICABLE - MATERIALS - PAID_LABOUR_OR_OWNER_OPPORTUNITY_COST - ACCESS_EQUIPMENT - TRAVEL - DISPOSAL - INSURANCE_ADMIN_ALLOCATION - REWORK_RESERVE - ACQUISITION_COST

SUBCONTRACT contribution:
CM_SUB = PRICE_EX_VAT_IF_APPLICABLE - VERIFIED_SUBCONTRACT_QUOTE - OWNER_SUPPLIED_MATERIALS_IF_ANY - ACCESS_EQUIPMENT_IF_OUR_ACCOUNT - SURVEY_PM_TIME - TRAVEL - INSURANCE_ADMIN_ALLOCATION - REWORK_RESERVE - ACQUISITION_COST

REFERRAL contribution:
CM_REFERRAL = VERIFIED_REFERRAL_OR_BOOKING_REVENUE - CUSTOMER_ACQUISITION_COST - QUALIFICATION_TIME - INVALID_INQUIRY_RESERVE - PLATFORM_PAYMENT_FEES

Current inputs: direct labour cost NULL; subcontract quote NULL; materials per reference job NULL; observed rework NULL; observed close-rate NULL; observed acquisition cost NULL. Therefore no route has proven profit.

## P28 — maximum affordable customer-acquisition cost
BREAKEVEN_COST_PER_QUALIFIED_INQUIRY = OBSERVED_CLOSE_RATE * CM_JOB_BEFORE_ACQUISITION - OBSERVED_QUALIFICATION_COST_PER_INQUIRY
TARGET_COST = reserve_factor * BREAKEVEN_COST, where reserve_factor is selected before spending and remains below 1.
Until real close-rate and contribution are known: MAX_AFFORDABLE_ACQUISITION_COST = NULL.

## P29 — acquisition routes
Owned/low-variable-cost: Google Business Profile, local landing pages/SEO, referrals/repeat customers, area-specific before/after content.
Subscription/marketplace: Onlinetradesmen.ie; Homedeal.ie; other Irish trade marketplaces as controlled comparisons.
Paid acquisition: Google Search/eligible local ads and Meta only after the quote flow measures inquiry -> survey -> quote -> job.

Current Onlinetradesmen public material states local job opportunities with no per-job commission and plans from about EUR43.33/month, subject to qualification/accreditation. Homedeal publicly states no subscription and payment only when a provider chooses to unlock a quote request. Third-party 2026 Irish trade benchmarks show a wide range of per-inquiry costs on shared/paid platforms; those figures are benchmarks, not our observed acquisition cost.

## P30 — landing / quote flow
Required fields: area/postcode; property type; exterior size band; surface type; current condition; trim requirement; access constraints; current photos; preferred timing; owner/authorized occupier confirmation; contact details and quote-contact consent.
Routing: simple/sound exterior -> remote prequalification then survey; prep-heavy or uncertain access -> site survey; major repair need -> out of scope or specialist; outside configured service area -> hold/referral.
No binding automatic price where substrate/access uncertainty is material.

## P31 — predeclared experiment guards
These are experiment rules, not universal market truths.
After at least 20 genuinely qualified paid inquiries from one channel: quote-to-job conversion below 10% -> pause and diagnose; acquisition cost above 20% of pre-acquisition contribution on the median won job -> hold scaling; invalid/uncontactable inquiry rate above 25% -> audit/pause channel.
Delivery: callback/rework cost above 10% of revenue across a 10-job sample -> fail route pending repair; any subcontract route without written scope, suitable insurance/competency evidence, acceptance criteria and defect responsibility -> hold; travel time that destroys contribution -> reject area rather than hide time cost.
Margin: positive contribution after all known direct costs plus explicit rework/admin reserve is required before external scale.

## P32 — route contract
DIRECT: scope within capability, cost inputs known enough to quote, capacity available, compliance boundaries satisfied, positive contribution after acquisition and reserve.
SUBCONTRACT: verified scope-specific quote, responsibilities and defect handling documented, management/acquisition costs included, positive contribution retained.
REFERRAL_ONLY: acquisition reliably produces buyer-intent inquiries/booked surveys, a real paying trade-partner arrangement exists, customer consent/data handling is appropriate, verified referral revenue exceeds acquisition and qualification costs.
HOLD: default whenever required evidence is incomplete.

## Result
MICRO_MARKET = DUBLIN_HOMEOWNER_EXTERIOR_REPAINT
3_FIXED_SCOPE_PACKAGE_HYPOTHESES = CREATED
DIRECT_COST_MODEL = CREATED_INPUTS_NULL
SUBCONTRACT_COST_MODEL = CREATED_INPUTS_NULL
REFERRAL_MODEL = CREATED_INPUTS_NULL
MAX_AFFORDABLE_ACQUISITION_COST = NULL
LANDING_QUOTE_FLOW = SPECIFIED
ROUTER = DIRECT / SUBCONTRACT / REFERRAL_ONLY / HOLD
CURRENT_ROUTE = HOLD_FOR_REAL_COST_AND_CLOSE_RATE_INPUTS
OUTREACH = 0
SPEND = 0
JOBS_CREATED_BY_RUN = 0
WTP = NULL

Next dependency: capture three comparable cost sets before any paid acquisition test — one realistic self-delivery cost sheet for a standard semi exterior, at least two scope-equivalent subcontract cost references/quotes, and material/access/travel allowances for the same reference job. Then calculate the maximum affordable acquisition cost and choose the first external route test.

READBACK_MARKER: MONEY-LOCAL-SERVICE-P25-P32-ROUTER-HOLD-COSTS-NULL-0-SPEND
