# MONEY MECHANISMS — LOCAL SERVICE + CUSTOMER ACQUISITION P25–P32

Date: 2026-08-22
Status: INTERNAL_SERVICE_ARCHITECTURE_COMPLETE / NO_OUTREACH_NO_SPEND

## P25
Micro-market: Dublin homeowner exterior-house repaint, starting with ordinary terraced/semi-detached homes that can be surveyed and scoped without specialist structural repair.
Buyer job: make the exterior look cared-for and weather-protected without coordinating separate preparation, painting, access and cleanup providers.
Public 2026 seller-published Dublin price guides sampled for this run show exterior retail references roughly EUR1,200–2,500 terraced, EUR1,800–3,800 semi-detached, EUR2,500–5,500+ detached. One source gives a two-painter crew reference around EUR350–500/day. These are reference prices only, not our costs or verified transactions.

## P26
Three fixed-scope hypotheses:
1 EXTERIOR WALLS REFRESH.
2 EXTERIOR FULL SHELL PAINT.
3 PREP-HEAVY EXTERIOR RECOVERY.
Each requires included/excluded surfaces, access assumptions, acceptance criteria and photo/punch-list closeout.

## P27
CM_DIRECT = PRICE - MATERIALS - LABOUR_OR_OPPORTUNITY_COST - ACCESS_EQUIPMENT - TRAVEL - DISPOSAL - ADMIN_INSURANCE - REWORK_RESERVE - ACQUISITION_COST
CM_SUB = PRICE - VERIFIED_SUBCONTRACT_QUOTE - OUR_MATERIAL_ACCESS_COST - SURVEY_PM - TRAVEL - ADMIN_INSURANCE - REWORK_RESERVE - ACQUISITION_COST
CM_REFERRAL = VERIFIED_REFERRAL_OR_BOOKING_REVENUE - ACQUISITION_COST - QUALIFICATION_TIME - INVALID_INQUIRY_RESERVE - PLATFORM_FEES
Current direct labour, subcontract quote, materials, observed rework, close-rate and acquisition cost are NULL. No profitable route is proven.

## P28
BREAKEVEN_COST_PER_QUALIFIED_INQUIRY = OBSERVED_CLOSE_RATE * CM_JOB_BEFORE_ACQUISITION - OBSERVED_QUALIFICATION_COST_PER_INQUIRY.
Until real close-rate and contribution are known: MAX_AFFORDABLE_ACQUISITION_COST = NULL.

## P29
Owned routes: Google Business Profile, local landing pages/SEO, referrals/repeat, area-specific before/after content.
Marketplace/subscription: Onlinetradesmen.ie, Homedeal.ie and controlled comparison with other Irish trade platforms.
Paid: Google/Meta only after inquiry -> survey -> quote -> job instrumentation exists.
Current Onlinetradesmen public material states local job opportunities with no per-job commission and plans from about EUR43.33/month, subject to qualification/accreditation. Homedeal states no subscription and payment only for quote requests a provider chooses to unlock. Third-party cost figures are benchmarks, not our observed acquisition cost.

## P30
Quote flow: area/postcode; property type; size band; surface; condition; trim requirement; access; photos; timing; authority to request work; contact consent. Simple jobs -> prequalify then survey; uncertain access/prep -> site survey; major repair -> specialist/out-of-scope; outside configured area -> hold/referral. No binding automatic price where material uncertainty remains.

## P31
Experiment guards, not universal market truths: after at least 20 qualified paid inquiries from one channel, quote-to-job below 10% -> pause; acquisition cost above 20% of pre-acquisition contribution on median won job -> hold scaling; invalid/uncontactable rate above 25% -> audit/pause. Callback/rework cost above 10% of revenue across a 10-job sample -> fail delivery route pending repair. Subcontracting without written scope, suitable competency/insurance evidence, acceptance criteria and defect responsibility -> HOLD.

## P32
DIRECT requires known-enough cost inputs, capability/capacity and positive contribution.
SUBCONTRACT requires verified scope-specific quote, documented responsibilities and positive contribution after management/acquisition costs.
REFERRAL_ONLY requires a real paying partner arrangement and verified positive referral economics.
HOLD is default while required evidence is missing.

## Result
MICRO_MARKET = DUBLIN_HOMEOWNER_EXTERIOR_REPAINT
3_FIXED_SCOPE_PACKAGE_HYPOTHESES = CREATED
DIRECT_COST_MODEL = CREATED_INPUTS_NULL
SUBCONTRACT_COST_MODEL = CREATED_INPUTS_NULL
REFERRAL_MODEL = CREATED_INPUTS_NULL
MAX_AFFORDABLE_ACQUISITION_COST = NULL
ROUTER = DIRECT / SUBCONTRACT / REFERRAL_ONLY / HOLD
CURRENT_ROUTE = HOLD_FOR_REAL_COST_AND_CLOSE_RATE_INPUTS
OUTREACH = 0
SPEND = 0
JOBS_CREATED_BY_RUN = 0
WTP = NULL

Next dependency: one realistic self-delivery cost sheet for a standard semi exterior + at least two scope-equivalent subcontract cost references/quotes + material/access/travel allowances. Then calculate maximum affordable acquisition cost and select first external route test.

READBACK_MARKER: MONEY-LOCAL-SERVICE-P25-P32-ROUTER-HOLD-COSTS-NULL-0-SPEND
