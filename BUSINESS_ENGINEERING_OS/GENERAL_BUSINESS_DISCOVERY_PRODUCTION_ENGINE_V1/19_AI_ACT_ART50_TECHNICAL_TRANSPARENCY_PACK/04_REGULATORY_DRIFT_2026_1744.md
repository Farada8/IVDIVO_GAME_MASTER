# ARTICLE 50 REGULATORY DRIFT RECEIPT — REGULATION (EU) 2026/1744

**Date:** 2026-08-22  
**Lane:** CF-01 / P-EW03  
**Classification:** `PATCH_REQUIRED / NO_ROUTE_CHANGE / NO_MARKET_PROMOTION`

## Trigger
The original P-EW03 pack correctly modeled Article 50 provider/deployer obligations, exceptions and technical evidence, but it did not encode the later binding transition added by Regulation (EU) 2026/1744.

## New binding fact
Providers of AI systems, including general-purpose AI systems, generating synthetic audio, image, video or text content that were placed on the market before 2 August 2026 must take the necessary steps to comply with Article 50(2) by 2 December 2026.

This is a narrow transition for Article 50(2). It is not:
- an exemption;
- a blanket Article 50 grace period;
- a deferral of Article 50(1), (3), or (4);
- evidence of compliance;
- evidence of customer demand, WTP, transaction, or profitability.

## Runtime delta
New state: `APPLIES_TRANSITIONAL_DEADLINE`.

Required transition evidence:
- provider role;
- in-scope synthetic-content generation;
- evidence that the system was placed on the market before 2026-08-02;
- explicit assessment date before 2026-12-02;
- transition remediation plan;
- machine-readable marking evidence due by 2026-12-02.

Fail-closed rules:
- legacy placement claim + missing assessment date -> `UNKNOWN`;
- assessment on/after 2026-12-02 -> ordinary `APPLIES` route;
- potential scope exception still routes to review before transition logic;
- transition never sets `legal_compliance_proven=true`.

## Regression delta
Three transition canaries added:
1. pre-deadline legacy system -> `APPLIES_TRANSITIONAL_DEADLINE`;
2. assessment on 2026-12-02 -> ordinary `APPLIES`;
3. missing assessment date -> `UNKNOWN / HOLD_UNRESOLVED_SCOPE_OR_EXCEPTION`.

The frozen six synthetic sample cases are not rewritten; derived test variants preserve the original P-EW03 evidence history.

## Authority effect
`P-EW03 = ENGINEERING_PASS + REGULATORY_DRIFT_PATCH`

`P-EW05 = UNCHANGED`

`OW-01 = M1`

`CF-01 = M1`

`CF-03 = M1`

`M2_PLUS = 0`

`WTP = UNKNOWN`

`EXTERNAL_ACTION_AUTHORIZED = FALSE`

## Primary sources
- Regulation (EU) 2026/1744, Official Journal / EUR-Lex.
- European Commission Article 50 FAQ.
- European Commission announcement that the AI Omnibus entered into force on 27 July 2026.

READBACK_MARKER: `ARTICLE50-REGULATORY-DRIFT-EU2026-1744-A50_2-TRANSITION-NO-MARKET-PROMOTION-20260822`
