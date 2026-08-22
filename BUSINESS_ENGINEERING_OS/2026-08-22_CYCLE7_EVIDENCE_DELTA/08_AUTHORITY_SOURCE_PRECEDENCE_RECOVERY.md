# CYCLE7 EVIDENCE DELTA — AUTHORITY SOURCE PRECEDENCE RECOVERY

**Date:** 2026-08-22
**Case:** `PROC-BALLYBUNION-8872468`
**Disposition:** additive fail-closed authority recovery; no BID/NO-BID promotion.

## Fresh official first-party read
The current eTenders CfT workspace for resource `8872468` remains the primary public authority surface. It confirms the works/open-procedure record, MEAT, current scope, estimated value EUR 1.6m, clarification deadline 2026-08-31 14:00, tender deadline 2026-09-02 17:00, tender opening 2026-09-02 17:30, duration 9 months, and `EU funding: No`.

A publicly indexed procurement mirror exposes the current eTenders procurement-documents route:
`https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`

The route is known, but the accessible indexed surface still does not expose the complete attachment/revision/addendum inventory or bytes. Therefore:
`DOCUMENT_ROUTE_KNOWN != CURRENT_ATTACHMENT_INVENTORY_RECOVERED`.

## Secondary-source conflict found
A third-party tender aggregator for TED notice `576830-2026` reports `EU Funded: Yes`, while the official eTenders CfT workspace reports `EU funding: No`.

The same aggregator's language renderings expose deadline localization/normalization differences; official eTenders remains authoritative for current portal time.

Authority resolution:
- official first-party current source wins over a conflicting aggregator field;
- the lower-ranked conflict is retained as provenance, not silently discarded;
- conflicting lower-ranked data cannot unlock requirements, eligibility, finance, or decision gates;
- if two equal-ranked current first-party sources conflict, fail closed and require reconciliation.

## Connected-source supplier search
Fresh Gmail/Drive searches for Certificate of Incorporation, CRO/company number, corporate Revenue/ROS/TR2/Tax Clearance evidence did not recover a decisive current document in the accessible connected-source results.

This is recorded as `NOT_FOUND_IN_CONNECTED_SOURCES`, not as evidence that the documents do not exist.

Supplier state remains:
- legal name/legal form: verified by private primary formation material;
- formation NACE: version-conflicted (6399 vs 8559), final/current registry authority still required;
- public registry presence: observed;
- company number: null/unverified;
- current ACTIVE/INACTIVE CRO status: null/unverified;
- corporate tax clearance: null/unverified;
- financial capacity, corporate insurance, H&S/PSCS, personnel, specialist construction capability, references and delivery capacity: null/unverified.

## New engineering contracts
1. `OFFICIAL_CURRENT_FIRST_PARTY_GT_THIRD_PARTY_AGGREGATOR`
2. `LOWER_SOURCE_CONFLICT_RETAINED_NOT_PROMOTED`
3. `EQUAL_TOP_AUTHORITY_CONFLICT_FAILS_CLOSED`
4. `DOCUMENT_ROUTE_NEQ_ATTACHMENT_INVENTORY`
5. `NOT_FOUND_IN_CONNECTED_SOURCES_NEQ_DOCUMENT_DOES_NOT_EXIST`

## Decision state
`HOLD_MISSING_AUTHORITY` remains unchanged.

`REQUIREMENT_JOIN = BLOCKED`.

`BID/HOLD/NO-BID = NOT AUTHORIZED`.

`PA4 = false`, `PA5 = false`, `E3 = false`, `E4 = false`.

## Next causal actions
1. Recover the actual current attachment inventory and file bytes from the eTenders documents route using an authenticated/browser-capable path if required.
2. Recover a current CRO/company-number authority document or official company profile.
3. Recover corporate Revenue/Tax Clearance evidence only from a source that identifies the company, not from personal myAccount mail.
4. Hash and bind every recovered artifact before requirement join.
