# P225 DOCUMENT COORDINATE DISCOVERY — RESOURCE 8872468

**Date:** 2026-08-22  
**Observed at:** 2026-08-22T06:31:00+01:00  
**Case:** `PROC-BALLYBUNION-8872468`  
**Disposition:** `DOCUMENT_COORDINATE_DISCOVERED / PACK_NOT_ACQUIRED / REAL_NEGATIVE_CONTROL_002`  
**Authority effect:** EVIDENCE ROUTING + CALIBRATION ONLY; ROOTS UNCHANGED

## New admissible coordinate
The current procurement notice/public first-party surface identifies the exact procurement-document coordinate for resource `8872468`:

`https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`

Associated official workspace:

`https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8872468`

Associated participation/submission route:

`https://www.etenders.gov.ie/epps/cft/viewTenders.do?resourceId=8872468`

Google Drive readback surface: `18qL7O5QFUxlYwhFag7XQIXhXzZ4s-1tLZh_--yzIFvo`.

## Independent current confirmation
A fresh public-web verification for exact resource `8872468` reconfirmed:
- title: Climate Summer Works: Roof replacements and energy efficiency upgrades at St. Joseph’s Secondary School and the adjacent former Convent Building in Ballybunion, Co. Kerry;
- contracting authority: St Joseph's Secondary School (Ballybunion);
- status: Tender Submission;
- procedure: Open;
- deadline: 2026-09-02 17:00 +01:00;
- estimated value: EUR 1,600,000;
- documents URL points to the exact `listContractDocuments.do?resourceId=8872468` coordinate.

## Acquisition result
The new coordinate is real, but the accessible indexed/search surface still did **not** yield:
- authoritative complete attachment inventory;
- complete tender-document bytes;
- revision/addendum graph;
- an authenticated export/ZIP.

Targeted exact-resource searches for PDF/tender-document/specification/drawing variants returned the live notice/index and documents route, not attachment bytes.

Therefore:

`DOCUMENT_COORDINATE_DISCOVERED != TARGET_PACK_ACQUIRED`

`DOCUMENTS_URL_KNOWN != AUTHORITATIVE_ATTACHMENT_INVENTORY`

`NOTICE_INDEX != TENDER_DOCUMENT_BYTES`

`NEW_COORDINATE != P225_EXECUTION`

## Resume-gate result
This is a second real negative control for the Business local control plane:

`REAL_NEGATIVE_CONTROL_002 = PASS`

The presence of a new exact first-party coordinate must **not** switch the ResumeGate to `RESUME_P226_P234` until actual admissible target files are acquired, persisted/read back, and reconciled into core authority.

Current state remains:
- `P225_EXECUTED = FALSE`;
- `TARGET_PACK_ACQUIRED = FALSE`;
- `ROOT_A = TARGET_PACK_NOT_ACQUIRED`;
- `ROOT_B = NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`;
- `P225–P288 = 17/64 executed`;
- `47 remaining`;
- `RESUME_ROUTE = PROTECT_NO_CHANGE`;
- public/derived ceiling `E2_PLUS`;
- artifact plane `PA3`;
- `PA4=false`, `PA5=false`, `E3=false`, `E4=false`;
- `external_action_authorized=false`.

## No-loop refinement
The prior same-coordinate Gmail/Drive/File-Library search remains exhausted. This new first-party URL coordinate has now also been tested at the accessible public/index layer.

Do not repeat this exact route merely because the user says “continue”. Re-open acquisition only on a materially new evidence event, for example:
- authenticated eTenders session/export;
- user-provided official ZIP/files;
- a directly retrievable first-party attachment URL;
- a newly indexed attachment filename/object;
- a new revision/addendum coordinate.

READBACK MARKER: `BUSINESS-P225-COORDINATE-NEGCTRL002-8872468-PACK-NOT-ACQUIRED-PROTECT-NO-CHANGE`
