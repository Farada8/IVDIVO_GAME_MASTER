# P225 — FIRST-PARTY DOCUMENT COORDINATE DISCOVERY

Date: 2026-08-22
Case: `PROC-BALLYBUNION-8872468`
Resource ID: `8872468`
Status: `DOCUMENT_COORDINATE_DISCOVERED / PACK_NOT_YET_ACQUIRED`
Authority effect: evidence routing only; no root closure; no backlog execution count change.

## New admissible coordinate
The current contract-notice surface exposes the official procurement-documents address:

`https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`

The current official CfT workspace remains:

`https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8872468`

The current contract notice also exposes electronic participation/submission routing:

`https://www.etenders.gov.ie/epps/cft/viewTenders.do?resourceId=8872468`

## Evidence provenance
- Current first-party eTenders workspace/search confirms resource `8872468`, title, authority, open procedure, live tender-submission status and deadline.
- The contract-notice publication exposes the exact procurement-documents URL above.
- A web-reader attempt against the exact document-list URL did not yield the attachment inventory or document bytes in the current tool surface.
- Therefore the coordinate is proven; the pack is not.

## Causal boundary
`DOCUMENT_COORDINATE_DISCOVERED != TARGET_PACK_ACQUIRED`

`DOCUMENTS_URL_KNOWN != ATTACHMENT_INVENTORY_READ_BACK`

`DOCUMENTS_URL_KNOWN != DOCUMENT_BYTES_ACQUIRED`

`LINK_DISCOVERY != P225_EXECUTION`

`P225_EXECUTED = FALSE`

`TARGET_PACK_ACQUIRED = FALSE`

`ROOT_A = TARGET_PACK_NOT_ACQUIRED`

`ROOT_B = NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`

Parent backlog remains `P225-P288 = 17/64 executed; 47 remaining`.

Proof frontier remains `E2_PLUS / PA3`; `PA4/PA5/E3/E4 = FALSE`.

Resume route remains `PROTECT_NO_CHANGE` until the Input Validator receives actual pack files and authoritative inventory/completeness evidence, or until an independent valid P235 event occurs.

## Next admissible P225 action
Use the exact first-party documents coordinate through an authenticated/browser-capable eTenders session and acquire:
1. all current attachment bytes;
2. authoritative attachment inventory;
3. revision/addendum state;
4. source receipt tied to resource `8872468`.

Then submit the resulting files through the existing Business Input Validator. A URL alone is not an admissible pack event because `validate_p225_input(..., files=[]) -> HOLD_P225_NO_FILES`.

## No-loop effect
Do not re-run broad discovery for the documents URL. It is now known exactly. Future P225 work should target acquisition/readback of the contents behind this coordinate.

Readback marker: `BUSINESS-P225-DOCUMENT-COORDINATE-8872468-DISCOVERED-PACK-NOT-ACQUIRED-V1`
