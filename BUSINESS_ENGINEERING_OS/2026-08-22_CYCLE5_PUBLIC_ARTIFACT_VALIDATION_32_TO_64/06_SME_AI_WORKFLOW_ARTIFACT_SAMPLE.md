# PA-AI-001 — SME AI WORKFLOW DIAGNOSTIC CARD

**Lane:** SME AI workflow / implementation diagnostic  
**PA grade:** PA3 after Cycle5 regression  
**Market grade:** E2+ ceiling  
**Sample case:** fictional and explicitly labelled; no real enterprise approval is claimed.

## Decision
If a small enterprise has completed Digital for Business, which workflow/software implementation opportunities should it scope next, and which Grow Digital constraints must be checked before spending money?

## Current official programme rules bound to the artifact
Source: Local Enterprise Office Grow Digital, observed 22 Aug 2026.

- Grow Digital supports small enterprises with **1–50 paid employees**.
- A **Digital for Business** project completed within the previous two years is a prerequisite.
- Enterprise must generally be established/trading for at least **6 months**, be within the LEO area, not currently an Enterprise Ireland or IDA client, and demonstrate solvency.
- Grant aid is **50% of eligible costs**, minimum grant **€500**, maximum **€5,000**.
- Eligible software examples include CRM, booking/payments, job tracking, workflow management, e-invoicing, cloud accounting/payroll, BIM/3D modelling and analytics including AI systems.
- Software must be new to the business; simply increasing existing licence counts does not qualify.
- Training and IT configuration combined can be no more than **50% of overall project cost**.
- Bespoke software is not treated as a safe eligible assumption; systems for regulatory compliance are not a safe eligible category.

Official pointers:
- `https://www.localenterprise.ie/portal/growdigital/grow-digital-grant.html`
- `https://www.localenterprise.ie/portal/growdigital/who-is-eligible-/`

## Fictional SampleBusinessObject
- paid employees: 8
- trading age: 18 months
- Digital for Business completed: 12 months ago
- EI/IDA client: no
- solvent: ASSUMED FOR SAMPLE ONLY
- target software new to business: ASSUMED YES

These values exist only to exercise the engine.

## Workflow inventory template
For each workflow capture:
`trigger -> people -> systems -> manual steps -> handoffs -> delay -> error/rework -> data created -> desired decision -> candidate software category -> measurable outcome`.

### Candidate workflow categories for the sample
1. lead / enquiry capture -> CRM
2. quoting / follow-up -> CRM + e-signature
3. field jobs / status -> job or field-service tracking
4. bookings / appointments -> booking system
5. invoices / payment status -> e-invoicing / accounting
6. stock / orders -> order or stock-control system
7. drawing/model coordination -> BIM/3D modelling where applicable
8. reporting / pattern detection -> analytics / AI

## Artifact output
`PRELIMINARY_SCHEME_PATH = POTENTIALLY_ELIGIBLE_IF_ALL_ASSUMPTIONS_VERIFY`

`LEO_APPROVAL = NOT_PROVEN`

`PAID_ADVISORY_DEMAND = NOT_PROVEN`

## Public-support substitution finding
A generic 'digital readiness audit' has a serious substitution problem because Digital for Business itself is a fully funded one-to-one digital review. Therefore the commercial hypothesis must **not** be 'sell another generic audit'.

Candidate differentiated wedge:
`POST-DIGITAL-FOR-BUSINESS IMPLEMENTATION -> workflow decomposition -> tool/configuration selection -> migration/setup -> staff training -> measurement -> handover`.

Even this remains a hypothesis until real buyer interaction.

## Missing evidence
- actual Digital for Business report
- current software inventory
- specific workflow pain and frequency
- staff adoption constraints
- selected vendor and eligible subscription status
- total project cost / co-funding capacity
- LEO confirmation
- measurable baseline
- buyer willingness-to-pay for external implementation help

## Falsifier
Hold/reject if LEO rules or project facts make the expenditure ineligible, if the proposed tool is already in use, if the workflow is too infrequent to justify change, or if free/subsidised support already supplies the same implementation work sufficiently.

## Next cheapest test
Take one real post-Digital-for-Business workflow and produce a one-page `BEFORE -> BOTTLENECK -> SOFTWARE CATEGORY -> CONFIG/TRAINING -> MEASURE -> COST RANGE -> ELIGIBILITY QUESTIONS` implementation card, then test whether a real enterprise finds it decision-changing.

## Proof boundary
Public funding eligibility and AI/software categories prove a supported implementation pathway exists. They do not prove approval, WTP, profitability, retention or demand for an external adviser.