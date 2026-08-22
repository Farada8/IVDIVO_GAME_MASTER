# POST-MERGE CLOSURE — SUPPLIER STATUS V2

**Date:** 2026-08-22
**PR:** #222
**Merge SHA:** `eb300dcde872b7f3ab31eb2ad5463ce6b18ed0ae`
**Final reviewed head:** `681e548b35ccc455e85a6213e9f5e72ad6923344`
**Exact-head CI:** GitHub Actions run `32549722143` — SUCCESS.

## Evidence integrated
- A1 `SR5869785` -> NACE 6399.
- Later recovered A1 `SR6505561` -> NACE 8559.
- Constitution dated 2025-08-24 confirms legal name `SYNTHESIS-IVDIVO LIMITED` and private-company-limited-by-shares legal form.
- Public Irish company index observed 2026-08-22, source data updated 2026-08-13, includes `Synthesis-Ivdivo Limited | Dublin, Ireland`.

## Fail-closed reconciliation
`FORMATION_ACTIVITY_CODE_CURRENT = NULL` because recovered A1 versions conflict and the final authoritative registry record is not recovered.

`PUBLIC_REGISTRY_PRESENCE = CONFIRMED` but `ACTIVE/INACTIVE STATUS = UNKNOWN`.

`COMPANY_NUMBER = UNKNOWN`.

No construction capability, tax clearance, financial capacity, insurance, H&S/PSCS competence, references, staffing, delivery capacity or tender eligibility is inferred.

## New contracts
- `FORMATION_METADATA_IS_VERSIONED`
- `CONFLICTING_FORMATION_VERSIONS_REQUIRE_FINAL_AUTHORITY`
- `LATEST_RECOVERED_FORM_NEQ_FINAL_REGISTRY_RECORD`
- `PUBLIC_REGISTRY_PRESENCE_NEQ_ACTIVE_STATUS`

Supplier/legal-status regression: 8/8 PASS.

## Cross-store
Drive evidence document `1yjs4NorTtyK0KqgT5DBujEw8jlswNoQb9tlAAh7TJmQ` in Cycle7 authority folder `1J7NbU_m4Hz-Vz_5yH4a5ioZTTmN5nd2A` was updated with the same version conflict, registry-presence boundary and next evidence action.

## Current procurement state
`PROC-BALLYBUNION-8872468` remains `HOLD_MISSING_AUTHORITY`.
Requirement join remains blocked.
BID/HOLD/NO-BID remains unauthorized.
PA4/PA5/E3/E4 remain false.

## Next causal acquisition
1. Current authoritative CRO/company record or Certificate of Incorporation with company number and current status.
2. Current tax registration/tax-clearance evidence.
3. Current tender pack.
4. Tender-required supplier capability evidence.
