# P225 PUBLIC ACCESS SURFACE DELTA — PROC-BALLYBUNION-8872468

**DATE:** 2026-08-22  
**STATUS:** BOUNDED EVIDENCE DELTA / P225 REMAINS HOLD  
**AUTHORITY IMPACT:** NONE — additive evidence only.

## Fresh observations

1. Official eTenders CfT workspace for resource `8872468` is live and current.
2. The official procurement-document route remains:
   `https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`.
3. The accessible indexed official workspace still does **not** expose the attachment inventory, document versions/addenda, or file bytes for the current target pack.
4. Independent procurement index Patterno labels the procurement-document reference as `LOT-0001 NON-RESTRICTED-DOCUMENT` and points to the portal/TED notice surfaces.
5. Target-specific searches for filenames, attachment-table variants, specification/drawing/Form-of-Tender/Suitability terms did not recover the actual current attachment inventory.

## Evidence provenance

### Official first-party
- eTenders workspace: `https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8872468`
- eTenders document route: `https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`
- TED notice: `576830-2026`

### Independent third-party observation
- Patterno tender record for TED `576830-2026` exposes descriptor `LOT-0001 NON-RESTRICTED-DOCUMENT`.

The Patterno descriptor is corroborative only and does not outrank official eTenders authority.

## Interpretation boundary

`THIRD_PARTY_NON_RESTRICTED_DESCRIPTOR != COMPLETE_OFFICIAL_PACK_ACQUIRED`

`DOCUMENT_ROUTE_KNOWN != ATTACHMENT_INVENTORY_RECOVERED`

`PUBLIC_WORKSPACE_AVAILABLE != FILE_BYTES_ACQUIRED`

`NO_INDEXED_ATTACHMENT_TABLE != NO_TENDER_DOCUMENTS`

The new observation narrows the acquisition hypothesis: the blockage may be an indexing/session/rendering-access problem rather than evidence that the documents are legally restricted. This remains a bounded hypothesis because the `NON-RESTRICTED-DOCUMENT` descriptor is third-party-derived.

## Root state — unchanged

- `ROOT_A = TARGET_PACK_NOT_ACQUIRED`
- `ROOT_B = NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`
- `P225 = HOLD_TARGET_PACK_NOT_ACQUIRED`
- `P235 = HOLD_NO_EXPLICIT_BIDDER_DESIGNATION`
- `PA4=false`
- `PA5=false`
- `E3=false`
- `E4=false`
- `BID_NO_BID=UNAUTHORIZED`

## Next admissible P225 acquisition order

1. Authenticated/user-provided official eTenders export or ZIP download from the current document page.
2. Direct official attachment-table read if/when the public index exposes resource `8872468`.
3. User-provided official tender files.

Do not infer requirements from resource `8176962` or any benchmark pack. Do not treat TED notice documents or third-party tender-index descriptors as the current tender pack.

## Drive mirror

Folder: `1Gli4pUf_2XLgQ0zXSm_GpS6yk7_Vf7SJ`  
Doc: `1q2jijpkwsslQ-js6R2k0GWPBnMOhhceVQuQtA_e8ueY`

`READBACK_MARKER=P225-8872468-PUBLIC-ACCESS-SURFACE-DELTA-HOLD-NO-PROMOTION`
