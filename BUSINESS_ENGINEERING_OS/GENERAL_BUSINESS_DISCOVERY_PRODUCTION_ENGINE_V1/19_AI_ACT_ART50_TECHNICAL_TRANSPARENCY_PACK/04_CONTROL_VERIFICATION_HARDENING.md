# P-EW03 — CONTROL VERIFICATION HARDENING

**Date:** 2026-08-22  
**Base authority:** merged PR #367, merge `3f65b522c59a7cdc988cbae893c1d54651eab6e6`  
**Verified base head:** `5a2db19731aeb23eac7c15c2da374cdaea3023a5`  
**Base Article 50 CI:** `32561576738` SUCCESS  
**Status:** ADDITIVE HARDENING / NO SECOND P-EW03 EXECUTION

## Why this layer exists
The merged #367 router answers `WHICH ARTICLE50 ROUTE / EVIDENCE OBJECT IS REQUIRED?`. This hardening adds the distinct second question: `IS THE REQUIRED TECHNICAL CONTROL EVIDENCE ACTUALLY PRESENT IN THE DECLARED PACKET?`

`REQUIRED_EVIDENCE_OBJECT != EVIDENCE_OBJECT_PRESENT`

## Control-verification states
- `PASS_CONTROL` — required technical evidence/control object explicitly declared present.
- `FAIL_CONTROL` — active route and required technical control explicitly absent.
- `UNKNOWN_CONTROL` — active route but presence/absence not established.
- `REVIEW_REQUIRED` — scope/exception/legislative claim cannot be automated.
- `NOT_ACTIVE` — no active technical obligation route in declared facts.

These are engineering states only.

## Critical negative control — machine marking vs human disclosure
For an active deepfake deployer route, provider-side machine-readable marking does not satisfy the human-facing `ContentDisclosureEvidence` requirement.

`MachineReadableMarkingEvidence=true + ContentDisclosureEvidence=false -> FAIL_CONTROL`

Current Commission Q&A states that deployer deepfake disclosure must be perceivable by people at first exposure and cannot be fulfilled merely by relying on provider machine-readable marking.

## Closed-loop / machine-only / non-final output
Current Commission Q&A lists exclusively machine-to-machine outputs and closed-loop industrial/product-development outputs, unless final outputs, among Article 50(2) scope exclusions. The canonical router conservatively routes such claims to `PENDING_EXCEPTION_REVIEW`; this hardening preserves that fail-closed boundary and never turns a scope claim into a compliance PASS.

## Legacy transition claim
Current Commission signing FAQ states that the AI Omnibus proposal envisages a grandfathering rule for Article 50(2) systems placed on the market before 2 August 2026 and, **if adopted**, would allow a transition to 2 December 2026.

Therefore:
`PRE_2026_08_02_SYSTEM + GRANDFATHERING_CLAIM -> LEGISLATIVE_REVIEW_REQUIRED`

The engine must not convert a proposal into an operative current-law exception.

## Evidence map contract
A verification fixture contains the router `case`, an `evidence` mapping of required evidence-object names to `true | false | null`, and optional `legacy_transition_claim`. Active-route technical evidence is checked; legal/review objects are never auto-passed by a boolean fixture.

## Engineering boundary
`CONTROL_PRESENT != LEGAL_COMPLIANCE`
`ROUTER_APPLIES != CONTROL_PRESENT`
`DECLARED_EVIDENCE != INDEPENDENT_VERIFICATION`
`PROPOSED_TRANSITION != OPERATIVE_EXCEPTION`
`PASS_CONTROL != CUSTOMER_DEMAND`
`PASS_CONTROL != WTP`
`PASS_CONTROL != TRANSACTION`

## Cross-store receipt
Drive folder: `15N2xm8iEYe5MBg7Jp3W1qazgLAdkD9Qp`  
Drive doc: `1zG-MB0LZ64hOkh4NXOQgP6phWo0p-uFcZ6pJjaXqo60`  
Marker: `P-EW03-PR367-BASE-PR370-SUPERSEDED-UNIQUE-CONTROL-VERIFICATION-SALVAGE-NO-PROOF-PROMOTION`
