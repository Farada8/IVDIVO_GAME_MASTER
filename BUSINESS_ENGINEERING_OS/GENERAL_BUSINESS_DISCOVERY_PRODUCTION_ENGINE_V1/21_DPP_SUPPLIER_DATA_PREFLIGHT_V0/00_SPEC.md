# P-EW04 — DPP SUPPLIER-DATA / REGISTRY PREFLIGHT V0

**Date:** 2026-08-22  
**Lane:** CF-03 / OW-03  
**Status:** INTERNAL ENGINEERING SAMPLE / NO LEGAL APPLICABILITY CLAIM / NO MARKET PROOF

## Objective
Demonstrate a bounded technical workflow that converts messy supplier/product source data into:
1. a traceable product-data object;
2. a missing-data ledger;
3. a registry-preflight view;
4. a correction/retest loop;
5. a decision on whether a fixed-scope DPP supplier-data diagnostic is technically supportable.

This artifact does **not** decide whether a real product currently requires a Digital Product Passport.

## Current official baseline
- The European Commission launched the DPP Registry and a testing environment on 20 July 2026.
- The Registry is an indexing service: it stores unique identifiers, registration data and high-level metadata rather than the full detailed DPP product dataset.
- Detailed DPP information remains decentralised under the responsibility of the relevant economic operator / service provider.
- ESPR Annex III defines categories of data that product-specific delegated acts may require or allow in a DPP.
- Product-group legal applicability and required fields depend on applicable Union legislation / delegated acts; a generic preflight must not manufacture that scope.
- The Commission states that the first implementation deadline is 18 February 2027 for certain large batteries; this fixture intentionally uses synthetic furniture so that product-specific obligation remains UNKNOWN rather than silently importing battery rules.

## Core laws
`DPP_DATA_READINESS != LEGAL_DPP_APPLICABILITY`

`REGISTRY_METADATA != FULL_DPP_DATASET`

`FIELD_PRESENT_WITHOUT_SOURCE != VERIFIED_DATA`

`MISSING_SUPPLIER_DATA != LEGAL_NONCOMPLIANCE`

`PRODUCT_GROUP_PRIORITY != CURRENT_MANDATORY_DPP`

`TEST_ENVIRONMENT_ACCESS != PRODUCTION_REGISTRATION_SUCCESS`

`SYNTHETIC_IDENTIFIER != REAL_OPERATOR_IDENTIFIER`

`GENERIC_ESPR_FIELD_CATEGORY != PRODUCT_SPECIFIC_REQUIRED_FIELD`

## Evidence states
Each candidate datum is routed to one of:
- `PRESENT_WITH_SOURCE`
- `PRESENT_SYNTHETIC_ONLY`
- `MISSING_SUPPLIER_DATA`
- `LEGAL_REQUIREDNESS_UNKNOWN`
- `NOT_APPLICABLE_VERIFIED`
- `FORMAT_OR_STANDARD_UNVERIFIED`

## Synthetic fixture
Product: a fictional EU-made wooden side table (`SYN-FURN-001`).

Why furniture:
- furniture is an ESPR priority product group;
- no product-specific DPP obligation is assumed by this fixture;
- it exposes the real business problem: supplier data exists in fragments before exact legal schemas are final/applicable.

## Candidate source buckets
The fixture tracks data under ESPR Annex III-style categories without declaring all categories mandatory:
- unique product identifier;
- GTIN/equivalent if relevant;
- commodity code if applicable;
- compliance-document references;
- manufacturer/economic-operator identity;
- importer/responsible-person fields where relevant;
- facility identifier if relevant;
- DPP service-provider/back-up reference if applicable;
- data-carrier / DPP-location reference;
- product-group sustainability data placeholders whose requiredness is product-act dependent.

## Preflight stages
### Stage A — ingest
Accept source records only with `source_ref` and `source_kind`. Untraceable values remain unverified.

### Stage B — normalize
Map heterogeneous supplier labels into canonical candidate fields. Never invent missing identifiers.

### Stage C — applicability boundary
Keep `legal_applicability = UNKNOWN` unless an authoritative product-specific rule/date has been pinned for the real product.

### Stage D — registry view
Create a high-level registration/index metadata view only. Do not serialize the full DPP dataset into the registry object.

### Stage E — gap ledger
Separate:
- actual missing supplier/source data;
- format/identifier checks still unresolved;
- product-specific legal requiredness unknowns.

### Stage F — correction loop
Apply only evidence-backed corrections, rerun validation, and report which gaps actually closed. Legal unknowns cannot be closed by better formatting alone.

## Acceptance criteria for P-EW04
P-EW04 passes engineering if:
1. initial synthetic record produces multiple distinct gap classes;
2. correction pass closes at least two supplier-data gaps without fabricating legal scope;
3. `legal_applicability=UNKNOWN` prevents false `REGISTRY_READY` promotion;
4. registry object contains high-level metadata only;
5. every populated externally meaningful value has provenance or is explicitly tagged synthetic;
6. validator produces deterministic machine-readable output;
7. tests cover false-promotion and source-traceability failures.

## Business implication gate
If P-EW04 passes, CF-03 may advance from `M0_INTERNAL_PROOF_ARTIFACT` to `M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN` **only as a technical service hypothesis**.

Potential future M1: `DPP Supplier-Data Readiness Diagnostic`.

No price, buyer demand, WTP, implementation transaction, recurring revenue or SaaS demand is proved here.

READBACK_MARKER: `P-EW04-DPP-SUPPLIER-DATA-PREFLIGHT-V0-SYNTHETIC-FURNITURE-NO-LEGAL-SCOPE-PROMOTION`
