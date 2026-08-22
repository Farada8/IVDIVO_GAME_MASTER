# CYCLE5 — THREE PUBLIC SAMPLE DELIVERABLES

Evidence ceiling for every artifact below: **E2+ PUBLIC ONLY**.

These are manual-first sample artifacts. They do not prove buyer fit, willingness-to-pay, procurement eligibility, legal clearance, ROI, margin or conversion.

---

## PRIMARY — OP01 — Tender / bid-no-bid decision intelligence

### Sample tender
**Tullow Community School — Summer Works 2026 — Refurbishment of 2 Home Economics Rooms**

Official public source observed 2026-08-22:
`https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8894062`

Observed public facts:
- contracting authority: Tullow Community School;
- procurement type: Works;
- procedure: Open;
- CPV includes construction work / school construction;
- estimated value: EUR 230,000;
- publication: 2026-08-21 11:10;
- clarification deadline: 2026-09-11 17:00;
- tender deadline: 2026-09-18 17:00;
- stated works: refurbishment of two Home Economics rooms including associated building, M&E works and finishes.

### One-page decision brief — sample
**Question:** Is this tender worth a contractor spending deeper estimating/qualification time on?

**Fast public-fit checks**
1. Geography/logistics: can the contractor serve Tullow, Co. Carlow within the required programme?
2. Capability: does current team/subcontractor capacity cover building + M&E + finishes?
3. Project scale: is EUR 230k within the contractor's normal project band and bonding/cash-flow tolerance?
4. Programme: can the works fit current resource plan and the stated contract duration?
5. Procurement burden: what declarations, references, insurances, H&S/PSCS obligations, schedules and pricing documents are required in the tender pack?
6. Commercial conflict: are there live jobs whose opportunity cost makes this tender unattractive?
7. Clarification clock: what questions must be resolved before 2026-09-11?
8. Submission clock: what internal owner signs off pricing, compliance and upload before 2026-09-18?

**Missing target-company data — MUST REMAIN NULL until supplied/verified**
- turnover and cash position;
- current workload/capacity;
- insurance limits;
- H&S/PSCS competence and required registrations;
- relevant project references;
- M&E supply chain availability;
- actual tender-document requirements beyond public workspace summary;
- pricing competitiveness;
- margin target;
- legal/procurement eligibility.

**Machine conclusion:** `PUBLIC_SAMPLE_READY / NOT_A_BID_RECOMMENDATION`.

### Corroborating workload examples
A second current public works tender published 2026-08-21 concerns refurbishment/repair of sash windows at Moyderwell, Tralee, estimated EUR 200,000, deadline 2026-09-21:
`https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8899923`

A larger open TU Dublin building-maintenance works competition published 2026-08-14 is estimated EUR 1.7m with a 2026-09-11 deadline:
`https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8856454`

These corroborate tender-monitoring workload, not willingness-to-pay for our proposed service.

---

## PILOT A — OP03 — Retrofit lead qualification / grant-readiness coordination

Official public sources observed 2026-08-22:
- SEAI One Stop Shop eligibility and multiple-upgrade rules: `https://www.seai.ie/grants/home-energy-grants/one-stop-shop/multiple-energy-upgrades`
- Registered One Stop Shops: `https://www.seai.ie/grants/find-a-registered-professional/one-stop-shop-providers`
- SEAI OSS support/provider rules: `https://www.seai.ie/contractors-and-suppliers/support-for-one-stop-shop`

Observed public facts used in the sample:
- OSS grant route is available through registered OSS providers;
- home must generally have been built and occupied before 2011 for the OSS scheme;
- post-works outcome must reach minimum BER B plus heat pump or required primary-energy uplift as specified by SEAI;
- prior grant/energy-credit history can exclude repeat support for the same measure;
- official provider/design rules govern actual eligibility and delivery.

### Manual qualification checklist — sample
Collect before routing a lead to technical assessment:
1. property ownership/status;
2. address/county and property type;
3. year built/occupied;
4. current BER if available;
5. prior SEAI grants / EEOS credits by measure;
6. proposed measures;
7. heat-pump intent / heating-system constraints;
8. known building-fabric issues;
9. MPRN and basic utility information where appropriate;
10. desired timing and financing constraints;
11. whether the homeowner accepts a registered OSS route;
12. missing documents / unknowns requiring official/provider verification.

**Output classes:**
- `READY_FOR_OSS_TECHNICAL_ASSESSMENT`
- `MORE_INFORMATION_REQUIRED`
- `PUBLIC_RULE_CONFLICT_REVIEW_REQUIRED`

These classes are workflow-routing hypotheses only. They are **not** an official SEAI grant determination.

**Machine conclusion:** `PUBLIC_SAMPLE_READY / GRANT_ELIGIBILITY_NOT_CLAIMED`.

---

## PILOT B — OP19 — SME AI workflow diagnostic

Official public sources observed 2026-08-22:
- Grow Digital eligibility: `https://www.localenterprise.ie/portal/growdigital/who-is-eligible-/`
- AI — Good for Business: `https://enterprise.gov.ie/en/news-and-events/department-news/2026/may/202605281.html`
- DETE SME supports: `https://enterprise.gov.ie/en/what-we-do/supports-for-smes/`

Observed public facts used in the sample:
- Grow Digital is for qualifying small enterprises with 1–50 paid employees;
- applicant must have completed Digital for Business within the previous two years and meet additional trading/client/solvency/location rules;
- AI — Good for Business promotes practical, gradual AI adoption, skills/readiness and access to support information;
- public support availability does not prove that a specific business should buy an AI diagnostic.

### Manual AI workflow diagnostic — sample
For one candidate workflow, capture:
1. workflow name and accountable owner;
2. trigger/input;
3. monthly volume/frequency;
4. current steps and handoffs;
5. current delay/error/rework points;
6. data sources and data sensitivity;
7. decisions that require human approval;
8. existing software/integrations;
9. narrow AI/non-AI automation hypothesis;
10. failure mode and human fallback;
11. measurable before/after metric;
12. support-programme eligibility facts separately from implementation suitability.

**Stop conditions:**
- sensitive/high-risk use cannot be safely bounded;
- no measurable repeated workload exists;
- the problem is process design/data quality rather than AI;
- required data is unavailable/unlawful to use;
- public support eligibility is uncertain.

**Machine conclusion:** `PUBLIC_SAMPLE_READY / AI_SUITABILITY_AND_ROI_NOT_CLAIMED`.

---

## Cross-artifact proof law

A polished sample can show that we can transform public information into a structured decision aid. It does **not** establish that any real buyer values it. Promotion to E3 requires a real buyer interaction bound to the exact artifact hash; promotion to E4 requires real money/deposit/PO bound to the same lineage.
