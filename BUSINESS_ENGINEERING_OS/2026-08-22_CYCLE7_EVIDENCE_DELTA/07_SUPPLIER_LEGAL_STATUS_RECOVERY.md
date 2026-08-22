# SUPPLIER LEGAL STATUS RECOVERY — VERSIONED FORMATION + PUBLIC REGISTRY PRESENCE

**Date:** 2026-08-22
**Supplier:** SYNTHESIS-IVDIVO LIMITED
**Case:** PROC-BALLYBUNION-8872468

## Recovered private-primary formation evidence
Three private-primary artifacts were compared rather than collapsed:

1. A1 declaration submission `SR5869785` records:
   - company name `SYNTHESIS-IVDIVO LIMITED`;
   - NACE 6399 — Other information service activities n.e.c.;
   - proposed central administration at 13 Adelaide Road, Dublin, D02 P950.

2. A later recovered A1 declaration submission `SR6505561` records:
   - the same company name;
   - NACE 8559 — Other education n.e.c.;
   - proposed central administration at 13 Adelaide Road, Dublin, D02 P950.

3. Constitution dated 2025-08-24 records:
   - company name `SYNTHESIS-IVDIVO LIMITED`;
   - private company limited by shares under Part 2 Companies Act 2014;
   - share capital EUR 100 divided into 100 ordinary EUR 1 shares.

## Version conflict
The recovered A1 formation declarations contain two different NACE codes: `6399` and `8559`.

Therefore no single formation activity code is promoted as the current registry fact.

`FORMATION_ACTIVITY_CODE_CURRENT = NULL`.

Typed state:
`CONFLICTING_FORMATION_VERSIONS_FINAL_REGISTRY_RECORD_NOT_RECOVERED`.

The later recovered submission `SR6505561` may be recorded as the latest recovered A1 version, but:
`LATEST_RECOVERED_FORM != FINAL_REGISTRY_RECORD`.

## Public registry/index evidence
A public Irish company index observed on 2026-08-22 and labelled as data updated 2026-08-13 includes `Synthesis-Ivdivo Limited | Dublin, Ireland`.

This supports only:
`PUBLIC_REGISTRY_INDEX_PRESENCE_CONFIRMED = TRUE`.

It does not support:
- company number;
- current ACTIVE/INACTIVE status;
- tax registration;
- tax clearance;
- construction capability;
- insurance;
- tender eligibility.

Engineering rule:
`PUBLIC_REGISTRY_PRESENCE != ACTIVE_STATUS`.

## Current legal-status state
- legal name: VERIFIED / multisource private-primary;
- legal form: VERIFIED / private-primary constitution;
- public registry/index presence: CONFIRMED;
- company number: UNKNOWN;
- current CRO active/inactive status: UNKNOWN;
- final/current NACE classification: UNKNOWN due version conflict;
- tax clearance: UNKNOWN.

Supplier evidence therefore remains partial and cannot unlock tender qualification.

## New contracts
- `FORMATION_METADATA_IS_VERSIONED`;
- `CONFLICTING_FORMATION_VERSIONS_REQUIRE_FINAL_AUTHORITY`;
- `LATEST_RECOVERED_FORM_NEQ_FINAL_REGISTRY_RECORD`;
- `PUBLIC_REGISTRY_PRESENCE_NEQ_ACTIVE_STATUS`.

## Next evidence acquisition
1. Recover current authoritative CRO/company record or Certificate of Incorporation containing the company number.
2. Verify current legal status from an authoritative current source.
3. Recover current tax registration/tax-clearance evidence separately.
4. Keep capability evidence separate from legal identity/status evidence.
