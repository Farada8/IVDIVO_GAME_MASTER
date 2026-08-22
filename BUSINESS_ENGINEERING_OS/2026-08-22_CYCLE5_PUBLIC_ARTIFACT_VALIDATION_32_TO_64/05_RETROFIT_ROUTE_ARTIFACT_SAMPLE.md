# PA-RETRO-001 — RETROFIT ROUTE CARD

**Lane:** retrofit qualification / orchestration  
**PA grade:** PA3 after Cycle5 regression  
**Market grade:** E2+ ceiling  
**Sample data:** yes. No real property eligibility or financing is claimed.

## Decision
Which SEAI route should a homeowner or retrofit coordinator investigate first: individual grants or a registered One Stop Shop complete upgrade?

## Current official rule set bound to the artifact
Sources: Sustainable Energy Authority of Ireland (SEAI), observed 22 Aug 2026.

1. Grant approval must be in place before grant-supported works begin.
2. For individual grants, the homeowner can manage the project but must use an SEAI-registered contractor for the relevant measure.
3. A registered One Stop Shop manages the full customer journey, including assessment, grant application, contractor works and follow-up BER.
4. The complete One Stop Shop route is designed to reach at least a B BER.
5. The registered One Stop Shop search returned 31 providers at read time; provider coverage varies by county and service.
6. One Stop Shops can support access to the Home Energy Upgrade Loan Scheme, but finance approval remains a separate lender decision.

Official source pointers:
- `https://www.seai.ie/grants/home-energy-grants/one-stop-shop`
- `https://www.seai.ie/grants/home-energy-grants/individual-grants/support-for-individual-grants`
- `https://www.seai.ie/grants/find-a-registered-professional/one-stop-shop-providers`

## Sample PropertyInputObject
All values below are deliberately UNKNOWN until a real property is supplied:
- owner/applicant class: UNKNOWN
- MPRN: UNKNOWN
- dwelling type: UNKNOWN
- build and occupation year: UNKNOWN
- current BER: UNKNOWN
- fabric condition / heat-loss data: UNKNOWN
- desired measures: UNKNOWN
- budget and cash timing: UNKNOWN
- registered contractor availability: UNKNOWN
- technical assessment requirement: UNKNOWN

## Artifact output
`ROUTE = INPUTS_REQUIRED_BEFORE_ROUTE`

No numerical lead score is generated.

## Route logic
### Candidate: Individual-grant route
Use when the applicant wants one or several eligible measures on their own timeline and can manage contractors/application workflow. Must preserve the grant-approval-before-works rule and registered-contractor dependency.

### Candidate: One Stop Shop route
Use when a complete coordinated upgrade is intended and the homeowner values a managed assessment/project/grant/works/BER path. Provider availability and project economics still need confirmation.

## Why a single lead score was rejected
Public grant rules cannot establish technical readiness, property suitability, quote quality, contractor capacity, finance suitability or the owner's willingness to proceed. Combining those unknowns into one score creates false precision.

## Missing evidence before a real route recommendation
- MPRN and property eligibility data
- build/occupation year
- dwelling type and current BER
- desired measures / target BER
- relevant technical assessment
- current quotes
- registered contractor or OSS coverage
- cash available before reimbursement / loan route
- heritage/traditional-building conditions where relevant

## Falsifier
If current property facts or updated SEAI rules show the assumed route is unavailable, technically inappropriate or financially infeasible, the route must be changed or held.

## Next cheapest test
Collect the PropertyInputObject, then run:
`ELIGIBILITY -> MEASURE DEPENDENCIES -> TECHNICAL ASSESSMENT -> PROVIDER COVERAGE -> QUOTES -> CASH TIMELINE -> ROUTE`.

## Proof boundary
SEAI programme scale and rules demonstrate a real externally funded workflow. They do not prove that a homeowner will purchase an independent orchestration service or that any project will be profitable.