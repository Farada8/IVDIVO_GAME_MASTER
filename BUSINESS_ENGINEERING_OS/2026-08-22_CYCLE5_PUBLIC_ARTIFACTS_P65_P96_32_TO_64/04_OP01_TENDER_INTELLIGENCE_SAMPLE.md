# OP01 SAMPLE — TENDER INTELLIGENCE + BID/NO-BID SCREEN
**Status:** PUBLIC-ARTIFACT CANARY / NOT BUYER EVIDENCE / NOT A BID RECOMMENDATION
**As-of:** 2026-08-22
**Target:** Irish construction/retrofit/MMC SME owner or bid manager.
**Purpose:** rapid public-data triage before downloading full RFT documents.

## 1. Busáras historic retrofit — Quantity Surveying Services
- eTenders Resource ID: `8838702`
- Buyer: Office of Public Works (OPW)
- Published: 2026-08-14
- Deadline: 2026-09-16 15:00
- Public status: `OPEN_TENDER_SUBMISSION`
- Public estimated value: UNKNOWN / not relied on
- Initial fit: **MEDIUM**
- Reason: retrofit/refurbishment relevance; consultancy credentials may exclude many contractor SMEs.
- Before BID: full RFT qualification, insurance, turnover, experience, certifications, lots and capacity.

## 2. Refurbishment of 33 Leeson Street Lower, Dublin 2
- eTenders Resource ID: `8830439`
- Buyer: Tuath Housing Association Ltd
- Published: 2026-08-12
- Deadline: 2026-09-11 15:00
- Public status: `OPEN_TENDER_SUBMISSION`
- Public estimated value: UNKNOWN / not relied on
- Initial fit: **HIGH**
- Reason: general fit-out, basement reconfiguration, structural and M&E works.
- Before BID: full RFT qualification, insurance, turnover, experience, exclusions and capacity.

## 3. HSE Dublin North East — Main Contractors Panel for Minor Capital Works
- eTenders Resource ID: `8746824`
- Buyer: Health Service Executive (HSE)
- Published: 2026-08-11
- Deadline: 2026-09-07 12:00
- Public status: `RESTRICTED_TENDER_SUBMISSION`
- Public estimated value: UNKNOWN / not relied on
- Initial fit: **HIGH**
- Reason: panel route may create recurring access; qualification requirements need full-document review.

## 4. UL1080 — Project Management Consultant for LISB1 Library Refurbishment
- eTenders Resource ID: `8811036`
- Buyer: University of Limerick
- Published: 2026-08-11
- Deadline: 2026-09-09 12:00
- Public status: `OPEN_TENDER_SUBMISSION`
- Public estimated value: UNKNOWN / not relied on
- Initial fit: **MEDIUM**
- Reason: refurbishment signal; direct fit depends on consultancy credentials; possible PARTNER_ROUTE.

## 5. Cork ETB — Douglas Street Campus Building Works
- eTenders Resource ID: `8812186`
- Buyer: Cork Education and Training Board
- Published: 2026-08-07
- Deadline: 2026-08-28 17:00
- Public status: `OPEN_TENDER_SUBMISSION`
- Public estimated value: €400,000
- Initial fit: **HIGH**
- Reason: building upgrade works with multiple specialist spaces.

## Allowed outputs
`INVESTIGATE_NOW` / `PARTNER_ROUTE` / `NO_BID_PUBLIC_SCREEN` / `HOLD_NEED_RFT`.
A public listing alone can never return `BID`.

## Artifact test
Before: five portal alerts.
After: each record has buyer, deadline, status, fit, disqualifying unknowns, and next evidence required.
**Engineering result: PASS_PUBLIC_ARTIFACT.**

## Provenance
Official public source class: eTenders Ireland. Retrieval/as-of 2026-08-22. Status/deadline must be refreshed before operational use.
