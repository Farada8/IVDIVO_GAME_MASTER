# BUSINESS RESUME / INPUT VALIDATOR — REAL NEGATIVE CONTROL 002

**Date:** 2026-08-22  
**Case:** `PROC-BALLYBUNION-8872468`  
**Expected route:** `PROTECT_NO_CHANGE`  
**Observed root effect:** NONE  
**Classification:** `REAL_NEGATIVE_CONTROL_002`

## Evidence event
Two independent additive surfaces now describe the same target-access boundary:

1. First-party coordinate artifact:
   `BUSINESS_ENGINEERING_OS/2026-08-22_P225_DOCUMENT_COORDINATE_DISCOVERY/00_DOCUMENT_COORDINATE_DISCOVERY.md`
2. Fresh public-access-surface delta:
   `BUSINESS_ENGINEERING_OS/2026-08-22_P225_PUBLIC_ACCESS_SURFACE_DELTA/00_EVIDENCE_DELTA.md`

Drive readbacks:
- coordinate discovery: `18qL7O5QFUxlYwhFag7XQIXhXzZ4s-1tLZh_--yzIFvo`;
- public-access delta: `1q2jijpkwsslQ-js6R2k0GWPBnMOhhceVQuQtA_e8ueY` in folder `1Gli4pUf_2XLgQ0zXSm_GpS6yk7_Vf7SJ`.

The exact official procurement-document route is known:

`https://www.etenders.gov.ie/epps/cft/listContractDocuments.do?resourceId=8872468`

The second delta additionally records an independent third-party descriptor `LOT-0001 NON-RESTRICTED-DOCUMENT`. That descriptor is corroborative only; it does not outrank eTenders and does not prove file acquisition.

## What was actually acquired
Acquired/observed:
- exact first-party documents coordinate;
- live current official workspace/status;
- independent corroboration that the reference is described as non-restricted.

Not acquired:
- authoritative complete attachment inventory;
- current attachment bytes;
- revision/addendum graph;
- authenticated official export/ZIP.

Therefore:

`DOCUMENT_COORDINATE_DISCOVERED != TARGET_PACK_ACQUIRED`

`PUBLIC_ACCESS_SURFACE != FILE_BYTES_ACQUIRED`

`THIRD_PARTY_NON_RESTRICTED_DESCRIPTOR != COMPLETE_OFFICIAL_PACK_ACQUIRED`

`NEW_ACCESS_EVIDENCE != P225_EXECUTION`

## Why this is a distinct negative control
Negative control 001 proved:

`BOUNDED_CONNECTED_SOURCE_NONFINDING != ROOT_A_UNLOCK`

Negative control 002 proves a different failure mode:

`BETTER_FIRST_PARTY_COORDINATE_AND_ACCESS_HINT != TARGET_PACK_ACQUIRED`

The correct route is:

`COORDINATE_OR_ACCESS_HINT_ONLY -> INPUT_VALIDATOR_HAS_NO_FILES -> ROOT_A_UNCHANGED -> PROTECT_NO_CHANGE`

It must NOT route to `RESUME_P226_P234`, downstream atomic join, BID/HOLD/NO-BID, proof promotion, submission, payment, contract acceptance or any other external action.

## Result
`NEGATIVE_CONTROL_002 = PASS`

- `P225_EXECUTED = FALSE`
- `TARGET_PACK_ACQUIRED = FALSE`
- `ROOT_A = TARGET_PACK_NOT_ACQUIRED`
- `ROOT_B = NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`
- `RESUME_ROUTE = PROTECT_NO_CHANGE`
- `P225-P288 = 17/64 EXECUTED; 47 REMAINING`
- proof = `E2_PLUS / PA3`; `PA4=false`, `PA5=false`, `E3=false`, `E4=false`
- `external_action_authorized=false`

## Calibration state
- ResumeGate synthetic suite: `PASS_16_OF_16`.
- Input Validator synthetic suite: `PASS_15_OF_15`.
- Real negative controls: `2 PASS`.
- Real positive root events: `0`.

Both mechanisms remain Business-local. No broader/global Self-Improvement promotion is justified until a real P225 or P235 authority event correctly switches the route.

## Next admissible event
Do not rediscover the URL or re-run the same public/index query. Re-open P225 only on materially new evidence such as:
- authenticated eTenders export;
- user-provided official ZIP/files;
- directly retrievable first-party attachment object/URL;
- newly indexed attachment filename/table;
- new revision/addendum coordinate.

READBACK MARKER: `BUSINESS-P225-NEGCTRL002-ACCESS-SURFACES-NO-BYTES-PASS-PROTECT-NO-CHANGE`
