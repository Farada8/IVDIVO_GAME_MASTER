# EARLY-WAVE RADAR — DELTA 03

**Date:** 2026-08-22  
**Status:** HORIZON SCAN + INCUMBENT SUBSTITUTION RED TEAM / `PROTECT_NO_CHANGE` / NO WIP PROMOTION / NO EXTERNAL ACTION  
**Parent:** `CURRENT_GENERAL_BUSINESS_ENGINE.md` after verified P-EW07 closure  
**Recovery:** recovered from Drive-verified stale branch onto fresh `main` after Money Mechanisms 58/64 closure  
**Profile:** REMOTE-FIRST / EUR0–500 preferred / test-before-build / WIP max 3

## Purpose
Search for genuinely new regulatory, infrastructure and technical forcing functions that could justify a new low-capital internal proof **after** Delta02/P-EW07.

Delta03 adds a stronger admission rule than a normal idea scan:

`FORCING_FUNCTION -> NATIVE/OFFICIAL_SUBSTITUTION_CHECK -> COMMERCIAL_INCUMBENT_CHECK -> RESIDUAL_JOB -> SMALLEST_FALSIFIABLE_PROOF`

If the residual job is already substantially covered, legal-heavy, too early, or overlaps an existing WIP, the candidate is killed/held **before** another artifact is built.

`NEW_DEADLINE != NEW_MARKET`
`REGULATORY_COMPLEXITY != INDEPENDENT_WEDGE`
`PUBLIC_GUIDANCE_GAP != BUYER_BUDGET`
`PLATFORM_NATIVE_WORKFLOW_CAN_ERASE_SERVICE_WEDGE`
`CROWDED_COMPLIANCE_SAAS != LOW_CAPITAL_WHITE_SPACE`

## Scoring note
Scores below are routing heuristics (0–100), not market proof. High forcing-function strength can coexist with a KILL disposition if native/incumbent substitution is already strong.

Factors:
- forcing-function immediacy — 20%;
- founder fit / reversibility — 15%;
- residual job after official/native tooling — 25%;
- incumbent saturation resistance — 20%;
- smallest-proof feasibility — 10%;
- non-legal/non-regulated delivery simplicity — 10%.

# Red-Team radar

## EW-D03-01 — CRA incident/vulnerability reporting workflow — 72/100 signal, **KILL GENERIC BUILD**
**Forcing function:** Cyber Resilience Act reporting obligations begin **11 September 2026**. Manufacturers report actively exploited vulnerabilities and severe security incidents through ENISA's Single Reporting Platform (SRP): early warning within 24 hours, main notification within 72 hours, and later final reports.

First-party evidence:
- https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp
- https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions
- https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-notification-submission-and-update
- https://digital-strategy.ec.europa.eu/en/policies/cra-reporting

### Native/official substitution
ENISA provides the SRP, registration/submission guidance, mandatory-field errors inside the platform, and continuously updated operational instructions.

### Commercial/open-source substitution
The exact obvious wedge already exists:
- `cra-scope` open-source/PyPI prepares structured CRA notification content and advertises schema validation / CSIRT routing for SRP preparation;
- CRA Ready offers incident clocks, evidence collection and 24h/72h/final report generation;
- CRATrust advertises SRP-aligned JSON, report status and audit history;
- multiple CRA readiness toolkits already cover classification, SBOM, evidence and reporting.

Examples:
- https://github.com/Usingthefork/cra-scope-cli
- https://pypi.org/project/cra-scope/
- https://www.cra-ready.io/
- https://www.cratrust.com/features

### Residual job
Possible future residue: independent regression against **changing SRP field/schema/guidance behaviour** across internal security tooling.

But current evidence does not show a differentiated paid problem beyond tools already shipping this preparation layer.

**Disposition:** `KILL_GENERIC_CRA_REPORT_PREP_OR_DEADLINE_TRACKER`  
**Watch only:** `SRP_SCHEMA_GUIDANCE_DRIFT_REGRESSION`  
**Smallest proof now:** `NOT_AUTHORIZED_NOT_JUSTIFIED`

---

## EW-D03-02 — CBAM supplier emissions evidence / Registry precheck — 70/100 signal, **KILL GENERIC BUILD**
**Forcing function:** CBAM definitive regime is active in 2026; the Commission Registry supports authorisation, reporting, emissions data and declarant monitoring.

First-party evidence:
- https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-registry_en
- Irish AMM guidance: https://www.revenue.ie/en/customs/businesses/cbam/access-amm.aspx

### Native/official substitution
The Commission's CBAM Registry already includes:
- Authorisation Management Module;
- Data Reconciliation for Monitoring and Control (DRMC);
- O3CI for non-EU installation operators;
- sharing of installation/emissions data so declarants can retrieve and use it;
- operational guides and training.

This destroys a large part of a generic `supplier data portal / registry helper` thesis.

### Commercial substitution
CarbonChain and Greenly already provide supplier requests, primary-data collection, validation, mapping, reporting and Registry-ready outputs.

Examples:
- https://www.carbonchain.com/cbam/signup
- https://learn.carbonchain.io/en/articles/13745420-how-to-use-carbonchain-connect
- https://greenly.earth/en-us/products/cbam

### Residual job
Independent reconciliation across supplier evidence, customs data and Registry state could exist in complex implementations, but current public evidence does not establish a small underserved wedge that beats native Registry + mature CBAM SaaS.

**Disposition:** `KILL_GENERIC_CBAM_SUPPLIER_DATA_OR_REPORTING_PRODUCT`  
**Overlap:** do not create a new WIP beside existing evidence-readiness/DPP engineering.  
**Smallest proof now:** `NO`

---

## EW-D03-03 — Machinery Regulation digital instructions / digital DoC QA — 67/100, **WATCH / NO BUILD**
**Forcing function:** Regulation (EU) 2023/1230 applies mandatorily from **20 January 2027**. It permits digital instructions subject to concrete access/print/download/save/availability rules and permits internet address or machine-readable-code access to digital EU declarations of conformity, with long retention requirements.

First-party evidence:
- https://eur-lex.europa.eu/eli/reg/2023/1230/en
- https://single-market-economy.ec.europa.eu/sectors/mechanical-engineering/machinery_en

### Incumbent substitution
The market is already forming around exactly this workflow:
- CEM4 manages machinery risk assessment and technical files and is updated for Regulation 2023/1230;
- Safety Software offers controlled declaration/QR workflows;
- NORMAN offers long-lived public manual hosting, versioning, multilingual access and DoC co-publication;
- SOPX and other tools explicitly sell 2027 digital-instruction workflows.

Examples:
- https://cem4.eu/en/
- https://safetysoftware.eu/en/p/eu-declaration-of-conformity-generator
- https://www.normaneu.com/en
- https://sopx.io/use-cases/digital-instructions-for-use/

### Residual job
An independent **external longevity/link/version/language/print-download accessibility regression** could be orthogonal to authoring/hosting platforms. But there is no present public buyer-pain or WTP evidence, and the compliance date is still months away.

**Disposition:** `WATCH_INDEPENDENT_DIGITAL_DOCUMENT_DELIVERY_REGRESSION`  
**No proof now:** wait for fresher implementation evidence or a concrete failure corpus.

---

## EW-D03-04 — Construction-product DPP — 65/100, **WATCH / EXISTING-DPP OVERLAP**
**Forcing function:** the DPP Registry is operational and can support product groups including construction products. CPR 2024 provides for a construction DPP system, but Commission timeline currently places construction-product DPP delegated requirements around **Q2 2027**.

First-party evidence:
- https://single-market-economy.ec.europa.eu/news/digital-product-passport-registry-now-live-2026-07-20_en
- https://single-market-economy.ec.europa.eu/single-market/digital-product-passport_en
- https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32024R3110

### Residual job
Construction data/BIM interoperability may later create a useful product-specific evidence mapping problem.

### Why no build now
- product-specific delegated layer is not yet sufficiently frozen;
- this substantially overlaps the existing CF-03 DPP supplier-data lane;
- another DPP project would violate WIP discipline without new product-specific evidence.

**Disposition:** `WATCH_Q2_2027_DELEGATED_LAYER / NO_NEW_WIP`

---

## EW-D03-05 — PPWR packaging compliance — 61/100 signal, **KILL GENERIC BUILD**
**Forcing function:** Regulation (EU) 2025/40 applies from **12 August 2026**. Commission guidance confirms Article 6(1)'s general recyclability requirement applies from that date, while later detailed recyclability/design criteria phase in.

First-party evidence:
- Commission guidance, OJ C 10.6.2026: https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52026XC03084

### Incumbent saturation
A dense specialist market already exists with low-cost/self-serve offerings for declarations, packaging data, EPR, supplier evidence, recyclability and DPP readiness: PPWR Connect, Repax ecosystem, PPWRify, VerdLynx, PPWR Toolkit, AtroPIM, Dcycle and others.

Examples:
- https://ppwrconnect.com/
- https://www.ppwrify.de/en/
- https://www.verdlynx.com/
- https://www.ppwrtoolkit.com/
- https://www.atropim.com/en/ppwr-compliance
- https://dcycle.io/ppwr-compliance/

Some self-serve offerings advertise entry prices around EUR29/month. A generic PPWR readiness dashboard or DoC generator is therefore not a credible white-space thesis.

**Disposition:** `KILL_GENERIC_PPWR_COMPLIANCE_SOFTWARE_OR_SERVICE`

---

## EW-D03-06 — EU Right to Repair manufacturer readiness — 57/100, **KILL GENERIC BUILD**
**Forcing function:** new repair rights began applying from **31 July 2026** for specified product categories. Manufacturer duties include repair-service information and repair/spare-parts obligations within the legal scope.

First-party/current Ireland evidence:
- https://enterprise.gov.ie/en/what-we-do/the-business-environment/right-to-repair-directive/
- https://commission.europa.eu/news-and-media/news/right-repair-new-consumer-rights-easy-and-attractive-repairs-2026-07-31_en

### Native/incumbent substitution
- EU/national repair-platform infrastructure is part of the policy implementation;
- FixFirst already markets manufacturer R2R operating-system/compliance workflows, ERIF generation, parts/info-request tracking and audit evidence.

Examples:
- https://fixfirst.io/solutions/manufacturers
- https://right2repair-compliance.com/

**Disposition:** `KILL_GENERIC_RIGHT_TO_REPAIR_READINESS_PLATFORM`

---

## EW-D03-07 — Empowering Consumers / green-claims evidence — 55/100, **LEGAL-HEAVY HOLD**
**Forcing function:** Ireland's implementation applies from **27 September 2026** and changes environmental claims, durability/repairability information, software-update information and consumer-facing notices.

Sources:
- https://enterprise.gov.ie/en/what-we-do/the-business-environment/empowering-consumers-for-the-green-transition/
- https://www.ccpc.ie/information-for-businesses/guidance-for-businesses/consumer-protection-guidance/european-union-%28empowering-consumers-for-the-green-transition%29-regulations-2026

### Red Team
The hard part is legal/contextual assessment of marketing claims, certification schemes, substantiation and misleading presentation. A naive AI website scanner would drift into legal advice and false-certification risk. Law firms and certification bodies already occupy much of the decision layer.

A technical evidence-link checker could exist, but no distinct non-legal residual job is established strongly enough for a proof.

**Disposition:** `HOLD_LEGAL_HEAVY / NO_TECHNICAL_PROOF`

---

## EW-D03-08 — EUDR due-diligence/geolocation tooling — 52/100, **KILL GENERIC BUILD**
**Forcing function:** revised EUDR timing still creates a future compliance wave, but supply-chain/geolocation/due-diligence software is already a mature specialist category.

Commercial evidence includes dedicated platforms that collect supplier evidence, geolocation/GeoJSON, risk state and due-diligence statement preparation.

Example:
- https://eudr.io/eudr-compliance-software

**Disposition:** `KILL_GENERIC_EUDR_DUE_DILIGENCE_OR_GEOLOCATION_PLATFORM`

---

# Delta03 decision

## No candidate advances to a smallest proof
`DELTA03_ADVANCE_TO_SMALLEST_PROOF = NONE`

The strongest forcing functions are real, but the obvious implementation wedges are already substituted by one or more of:
1. official/native regulatory infrastructure;
2. open-source preparation tools;
3. specialist SaaS with existing workflows;
4. mature compliance/technical-document platforms;
5. legal/specialist judgement beyond the intended non-legal role;
6. overlap with existing WIP.

Therefore the correct portfolio action is:

`DELTA03_DISPOSITION = PROTECT_NO_CHANGE`

This is a positive decision-quality result, not a lack of ideas.

## Current WIP remains unchanged
- PRIMARY: `OW-01 Agentic Commerce` — M1 only;
- PILOT: `CF-01 Article 50 Technical Transparency` — M1 only;
- PILOT: `CF-03 DPP Supplier-Data / Registry Readiness` — M1 only.

`WIP_COUNT = 3`
`WIP_PROMOTION_FROM_DELTA03 = FALSE`

## Watch coordinates only
Keep these low-cost observation coordinates, without building products:
1. `CRA_SRP_SCHEMA_GUIDANCE_DRIFT` — only if ENISA changes fields/interfaces or real cross-tool failures become visible;
2. `MACHINERY_DIGITAL_DOCUMENT_DELIVERY_REGRESSION` — only if a public failure corpus shows broken links/version/language/download/retention problems not handled by current platforms;
3. `CONSTRUCTION_DPP_DELEGATED_LAYER` — revisit when product-specific CPR DPP acts/technical rules are published;
4. existing DPP Registry standards/API evolution — route into CF-03 rather than creating a new WIP.

## Reopen conditions
A Delta03 candidate may be reopened only if at least one material new fact appears:
- first-party interface/schema change creates a measurable compatibility gap;
- incumbent/native tooling demonstrably misses an important deterministic control;
- a public real-fixture corpus shows repeatable failure not covered by existing tools;
- external buyer evidence is explicitly authorized and shows a budgeted residual problem;
- a current WIP is deliberately retired, freeing a slot.

Absent those facts:
`NO_NEW_ADMISSIBLE_DELTA -> PROTECT_NO_CHANGE`

## Proof boundary
`PUBLIC_EVIDENCE_CEILING = E2_PLUS_ENGINEERING`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`WIP_PROMOTION = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

## Recovery provenance
Original Delta03 authority was discovered in Drive and on stale GitHub branch `business-engineering/early-wave-radar-delta03-20260822`. The Drive semantic readback marker matched the branch artifact. Fresh recovery starts from current main `18ece63df7a0c8a3d5efb1892dbc7c722a2b93de`, which already contains Money Mechanisms 58/64 merge `46cc5c954084a893c5e37c08d8a2537d0276fbb5`. Recovery changes no Delta03 disposition and creates no new market evidence.

READBACK_MARKER: `EARLY-WAVE-RADAR-DELTA03-PROTECT-NO-CHANGE-CRA-CBAM-PPWR-MACHINERY-SUBSTITUTION-NO-WIP-20260822`
