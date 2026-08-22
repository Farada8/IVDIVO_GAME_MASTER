# OP03 PUBLIC ARTIFACT — Retrofit Lead Qualification / Grant Readiness Pack
**Observed:** 2026-08-22
**Evidence ceiling:** E2+ public-only. This pack cannot guarantee grant eligibility, technical suitability, contractor availability, project cost, grant payment, or customer demand.

## Minimum lead data
- owner/applicant type;
- property MPRN;
- dwelling type;
- year built and occupied;
- current BER / Advisory Report where available;
- Heat Loss Indicator (HLI) where relevant;
- attic and wall insulation condition;
- proposed measure(s);
- self-managed individual-grant route vs registered One Stop Shop;
- chosen SEAI-registered contractor / assessor where required.

## Windows + doors gate
Current official SEAI rules state:
- eligible owner categories include homeowners, companies/OMCs, charities, holiday-home owners, AHBs and landlords;
- property must be built and occupied before 2011;
- attic and wall insulation must be good;
- replacement windows must meet U-value 1.4 W/m²K or lower;
- post-works HLI must be <=2.3 W/K·m² **or** attic/walls rated Good/Very Good;
- grant amounts: windows €1,500 apartment / €1,800 mid-terrace / €3,000 semi/end-terrace / €4,000 detached; external doors €800 each, max 2;
- self-managed route: grant paid after works; One Stop Shop route: eligible grant deducted upfront.
Official source: https://www.seai.ie/grants/home-energy-grants/individual-grants/windows-and-doors

**Lead outcome:** `READY_FOR_QUOTE_AND_GRANT_APPLICATION_CHECK`, `NEEDS_BER/INSULATION_CHECK`, or `HOLD_NOT_ELIGIBLE_ON_KNOWN_RULE`.

## Heat-pump gate
Current official SEAI rules state:
- MPRN required; home built and occupied before 2021;
- total heat-pump bundle up to €12,500 for houses / €9,500 apartments depending on system/dwelling; components include up to €6,500 heat-pump unit, up to €2,000 heating-component upgrades, and €4,000 renewable-heat bonus when conditions are met;
- pre-2007 homes need a Technical Assessment unless a valid BER shows HLI <=2.3 W/(K.m²);
- SEAI-registered contractor required;
- grant approval before work starts;
- eight-month drawdown window; post-works BER required.
Official source: https://www.seai.ie/grants/home-energy-grants/individual-grants/heat-pump-systems

## Cash-timing gate
- Individual grant route: applicant/contractor generally receives grant after completed works and correctly submitted payment/declaration documents.
- One Stop Shop route: grant is deducted upfront from the cost charged by the registered OSS.
Official sources:
- https://www.seai.ie/grants/home-energy-grants/individual-grants/support-for-individual-grants
- https://www.seai.ie/grants/home-energy-grants/one-stop-shop

Therefore `grant_amount != cash_available_before_work`. A self-managed project can carry a working-capital gap.

## Contractor gate
Grant-aided works require the appropriate SEAI-registered contractor. SEAI registration includes technical standards/code requirements, tax compliance, insurance and a standard homeowner contract; renewable installations have additional installer registration requirements.
Official source: https://www.seai.ie/contractors-and-suppliers/register-with-seai/contractor

## Reject / hold taxonomy
- `HOLD_MISSING_MPRN_OR_OWNERSHIP`
- `HOLD_BUILD_YEAR`
- `HOLD_BER_HLI_UNKNOWN`
- `HOLD_INSULATION_PRECONDITION`
- `HOLD_CONTRACTOR_NOT_CONFIRMED`
- `HOLD_GRANT_NOT_APPROVED`
- `HOLD_WORKING_CAPITAL`
- `READY_FOR_NEXT_OFFICIAL_APPLICATION_STEP`

## Artifact result
This public artifact can pre-structure a lead and reduce obvious eligibility errors. It does not establish willingness-to-pay or replace SEAI, a BER assessor, a Technical Assessment, a registered contractor, or an OSS.
