# BUSINESS RESUME / INPUT VALIDATOR — REAL NEGATIVE CONTROL 002

**Date:** 2026-08-22  
**Case:** `PROC-BALLYBUNION-8872468`  
**Source artifact:** `BUSINESS_ENGINEERING_OS/2026-08-22_P225_DOCUMENT_COORDINATE_DISCOVERY/00_DOCUMENT_COORDINATE_DISCOVERY.md`  
**Drive readback:** `18qL7O5QFUxlYwhFag7XQIXhXzZ4s-1tLZh_--yzIFvo`  
**Expected route:** `PROTECT_NO_CHANGE`  
**Observed root effect:** NONE

## Event
A materially new first-party coordinate appeared after the earlier bounded Gmail/Drive/File-Library nonfinding:

`https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`

Fresh public verification independently reconfirmed that this is the documents URL for the live `8872468` competition. Targeted exact-resource searches for PDF/tender-document/specification/drawing variants still returned only notice/index/route surfaces; no authoritative attachment inventory, document bytes, revision/addendum graph or authenticated export was acquired.

## Why this is a distinct real negative control
Negative control 001 proved:

`BOUNDED_CONNECTED_SOURCE_NONFINDING != ROOT_A_UNLOCK`

Negative control 002 proves a different failure mode:

`NEW_FIRST_PARTY_DOCUMENT_COORDINATE != TARGET_PACK_ACQUIRED`

A future agent must not interpret the discovery of a better URL as completion of P225.

Required outcome:

`DOCUMENT_COORDINATE_ONLY -> INPUT_VALIDATOR_HAS_NO_FILES -> ROOT_A_UNCHANGED -> PROTECT_NO_CHANGE`

It must NOT route to:
- `RESUME_P226_P234`;
- `RESUME_P252_P280`;
- BID/HOLD/NO-BID;
- proof promotion;
- external submission or other external action.

## Result
`NEGATIVE_CONTROL_002 = PASS`

`P225_EXECUTED = FALSE`  
`TARGET_PACK_ACQUIRED = FALSE`  
`ROOT_A = TARGET_PACK_NOT_ACQUIRED`  
`ROOT_B = NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`  
`RESUME_ROUTE = PROTECT_NO_CHANGE`  
`P225-P288 = 17/64 EXECUTED; 47 REMAINING`.

Proof remains `E2_PLUS / PA3`; `PA4=false`, `PA5=false`, `E3=false`, `E4=false`.

## Calibration state
- ResumeGate synthetic suite: `PASS_16_OF_16`.
- Input Validator synthetic suite: `PASS_15_OF_15`.
- Real negative controls: `2 PASS`.
- Real positive root events: `0`.

Therefore both mechanisms remain Business-local. No broader/global Self-Improvement promotion is justified until a real P225 or P235 authority event correctly switches the route.

READBACK MARKER: `BUSINESS-P225-NEGCTRL002-DOCUMENT-COORDINATE-ONLY-PASS-PROTECT-NO-CHANGE`
