# ARTICLE 50 REGULATORY DRIFT RECEIPT — REGULATION (EU) 2026/1744

**Date:** 2026-08-22  
**Lane:** CF-01 / P-EW03  
**Classification:** `PATCH_VERIFIED / NO_ROUTE_CHANGE / NO_MARKET_PROMOTION`

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

## Verified implementation authority
- implementation PR: `#412`;
- implementation head: `0fc63534eceba746d0ef43cc93552905d2c6b38e`;
- merge SHA: `e340213a88b9a59513209819ba966aa3cb7faad6`;
- review threads at merge gate: `0`;
- fresh-main overlap across the six Article 50 paths: `0`;
- exact-head Business CI: `7/7 SUCCESS`.

CI runs:
- Article 50 pack: `32570316435`;
- P-EW05 compatibility: `32570316420`;
- Discovery engine: `32570316412`;
- Buyer Evidence: `32570316384`;
- Fatal Tests: `32570316398`;
- Offer Engineering: `32570316408`;
- OPP37 AI-vs-SEO: `32570316421`.

## Authority effect
`P-EW03 = ENGINEERING_PASS + VERIFIED_REGULATORY_DRIFT_PATCH`

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

READBACK_MARKER: `ARTICLE50-REGULATORY-DRIFT-EU2026-1744-PR412-E340213A-7OF7-VERIFIED-NO-MARKET-PROMOTION`
