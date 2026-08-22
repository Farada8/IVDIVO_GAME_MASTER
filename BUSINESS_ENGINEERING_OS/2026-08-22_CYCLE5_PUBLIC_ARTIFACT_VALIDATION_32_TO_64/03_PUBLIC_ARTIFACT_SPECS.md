# CYCLE5 — PUBLIC ARTIFACT SPECS

**Evidence class:** official/public sources only; maximum E2+.

## Artifact A — Procurement Decision Intelligence

### Buyer job
Reduce time spent scanning irrelevant public opportunities and surface which notices require immediate human review.

### Named decisions
`IGNORE / REVIEW NOW / REVIEW LATER / CAPABILITY CHECK / QUALIFICATION CHECK`.

### Required fields
Resource ID; contracting authority; title; publication date; submission deadline; estimated value if published; procurement type/procedure; sector/work package; geography if explicit; source freshness; fatal unknowns; capability-fit vector; next human action.

### Null-safety
Do not infer supplier eligibility, turnover thresholds, insurance, framework access, certifications, capacity or margin unless the tender documents provide them and the supplier profile is known.

### Cycle5 public sample
1. **8885468 — Sustainable Energy Development — Skerries Harps**. Published 2026-08-21; deadline 2026-09-14; estimated value €80,000; BESS + hybrid inverter. Decision: `CAPABILITY CHECK`; supplier fit remains null until capability/qualification profile exists.
2. **8894062 — Tullow Community School — refurbishment of 2 Home Economics rooms**. Published 2026-08-21; deadline 2026-09-18; estimated value €230,000; building + M&E works. Decision: `CAPABILITY CHECK`.
3. **8838702 — OPW — QS services for Busáras historic building retrofit**. Published 2026-08-14; deadline 2026-09-16; services/open procedure; estimated value recorded as 0/unspecified in search index. Decision: `QUALIFICATION CHECK`; no invented contract value.
4. **8763611 — SEAI — Gas and Electricity Infrastructure Technical Services framework**. Published 2026-07-31; deadline 2026-09-15; estimated value €200,000. Decision: `QUALIFICATION CHECK`.
5. **8809597 — OPW — Consultant and Project Archaeologist Services for Flood Risk Management**. Published 2026-08-11; deadline 2026-09-21; estimated value €2.65m. Decision: `CAPABILITY CHECK`.
6. **8732419 — Louth County Council — Consultant Engineering Services River Screens**. Published 2026-07-27; deadline 2026-08-31. Decision: `REVIEW NOW` because deadline is near; commercial/supplier fit remains null.
7. **8746824 — HSE Dublin North East — Main Contractors Panel for Minor Capital Works**. Published 2026-08-11; deadline 2026-08-31. Decision: `REVIEW NOW / QUALIFICATION CHECK`.

### Artifact hypothesis
A useful procurement product is not “a list of tenders”. It is a refreshed decision queue with dedupe, deadline risk, capability gaps, fatal unknowns and explainable reasons.

---

## Artifact B — Retrofit Qualification / Route Triage

### Buyer job
Determine the correct public scheme/provider route before paying for the wrong assessment, starting ineligible work, or assuming grant cash arrives at the wrong time.

### Decision routes
1. `INDIVIDUAL_GRANTS` — staged/self-managed measures using registered contractors; grant is generally paid after completed works/documentation.
2. `ONE_STOP_SHOP` — complete/whole-house upgrade managed end-to-end; grants deducted upfront; target generally minimum B/B2 under the national whole-home route.
3. `TRADITIONAL_HOME_PILOT` — typically pre-1940 traditional construction; Traditional Building Professional + participating OSS; whole-house route; heritage-appropriate treatment; B/B2 target is not the same default requirement as ordinary OSS route.
4. `FULLY_FUNDED_WARMER_HOMES` — eligibility depends on qualifying circumstances; do not infer from property alone.
5. `ROUTE_UNRESOLVED` — missing property/owner/measure facts.

### Required fields
Construction era; current BER if known; property/owner eligibility facts; measures wanted; whole-house vs staged intent; prior grants/works; cash/upfront constraint; traditional construction indicators; provider route; registered-professional requirements; grant timing; missing information; next cheapest verification.

### Public-substitution result
Generic “we manage the whole retrofit journey” is highly substituted by registered One Stop Shops. Cycle5 therefore narrows the pilot to **pre-qualification, route triage, exceptions, provider fit, grant/cash-timing readiness and document preparation**.

---

## Artifact C — SME AI Workflow / Implementation Readiness

### Buyer job
Turn a business workflow problem into an evidence-backed implementation backlog while showing what public supports already cover.

### Public support constraints
- Grow Digital: small enterprises with 1–50 paid employees; trading at least 6 months; not current EI/IDA clients; solvent; within LEO area; Digital for Business project completed within previous two years.
- Grant: 50% of eligible costs, €500 minimum grant to €5,000 maximum; up to two projects within cumulative €5,000.
- Eligible software must be new/off-the-shelf; examples include CRM, workflow/field management, BIM, analytics including AI.
- Training/configuration can be eligible but combined amount is capped at 50% of overall project cost.
- Bespoke software and systems for regulatory compliance are not eligible under the Grow Digital rules cited in Cycle5.
- Digital for Business already provides analysis of existing digital systems/gaps, optimisation/integration opportunities and guidance on implementation.

### Consequence
A generic “AI/digital maturity diagnostic” has high public-substitute risk. The Cycle5 pilot must differentiate as one or more of:
- sector-specific workflow evidence inventory;
- pre-consultant input/evidence pack;
- implementation backlog after Digital for Business;
- tool/integration/control map;
- measurement plan with baseline and falsifier;
- operational/security/risk routing;
- vendor/configuration readiness for a specific workflow.

### Required fields
Business eligibility facts; workflow/job; current tools; pain/frequency; process owner; data inputs; desired outcome; baseline metric; candidate software class; integration/configuration need; AI/security/regulatory risk; public support substitute; eligible/ineligible unknowns; implementation backlog; next test.

## Common acceptance
PASS only if the artifact names a decision, uses current/official inputs, keeps unknowns null, identifies free/subsidised substitutes and creates a plausible decision delta. This is artifact utility evidence, not market proof.