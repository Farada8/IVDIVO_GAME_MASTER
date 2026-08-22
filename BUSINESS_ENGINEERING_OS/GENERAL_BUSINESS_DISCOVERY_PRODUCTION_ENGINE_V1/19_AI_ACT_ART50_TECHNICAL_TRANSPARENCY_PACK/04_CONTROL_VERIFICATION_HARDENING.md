# P-EW03 — CONTROL VERIFICATION HARDENING

**Date:** 2026-08-22  
**Base authority:** merged PR #367, merge `3f65b522c59a7cdc988cbae893c1d54651eab6e6`  
**Verified base head:** `5a2db19731aeb23eac7c15c2da374cdaea3023a5`  
**Base Article 50 CI:** `32561576738` SUCCESS  
**Status:** ADDITIVE HARDENING / NO SECOND P-EW03 EXECUTION

## Why this layer exists
The merged #367 router answers the first question correctly:

`WHICH ARTICLE50 ROUTE / EVIDENCE OBJECT IS REQUIRED?`

This hardening adds a distinct second question:

`IS THE REQUIRED TECHNICAL CONTROL EVIDENCE ACTUALLY PRESENT IN THE DECLARED PACKET?`

Routing an obligation to `MachineReadableMarkingEvidence` or `ContentDisclosureEvidence` is not itself evidence that the control exists.

`REQUIRED_EVIDENCE_OBJECT != EVIDENCE_OBJECT_PRESENT`

## Control-verification states
- `PASS_CONTROL` — the required evidence/control object is explicitly declared present.
- `FAIL_CONTROL` — the route is active and the required technical control is explicitly declared absent.
- `UNKNOWN_CONTROL` — the route is active but presence/absence is not established.
- `REVIEW_REQUIRED` — router scope/exception is unresolved or a legislative-transition claim cannot be automated.
- `NOT_ACTIVE` — no active technical obligation route in the declared facts.

These states are engineering states only.

## Critical negative control — machine marking vs human disclosure
For an active deepfake deployer route, a provider-side machine-readable mark does **not** satisfy the human-facing `ContentDisclosureEvidence` requirement.

`MachineReadableMarkingEvidence=true + ContentDisclosureEvidence=false -> FAIL_CONTROL`

This matches current Commission Q&A: deepfake deployer disclosure must be perceivable by people at first exposure and cannot be fulfilled merely by relying on provider machine-readable marking.

## Closed-loop / machine-only / non-final output
Current Commission Q&A lists certain outputs outside the Article 50(2) marking scope, including exclusively machine-to-machine outputs and closed-loop industrial/product-development outputs unless they are final outputs.

The canonical router already treats such facts as `PENDING_EXCEPTION_REVIEW`, which is intentionally conservative. This hardening preserves that fail-closed boundary: the verifier never turns a scope-exclusion claim into a compliance PASS.

## Legacy transition claim
Current Commission signing FAQ says the AI Omnibus proposal **envisages** a grandfathering rule for Article 50(2) systems placed on the market before 2 August 2026 and, **if adopted**, would allow transition to 2 December 2026.

Therefore:

`PRE_2026_08_02_SYSTEM + GRANDFATHERING_CLAIM -> LEGISLATIVE_REVIEW_REQUIRED`

The engine must not convert the proposal into an operative current-law exception.

## Evidence map contract
A verification fixture contains:
- `case`: the same declared facts consumed by `router.py`;
- `evidence`: mapping of required evidence-object names to `true | false | null`;
- optional `legacy_transition_claim`.

For active router decisions only, required technical evidence objects are checked. Legal-review objects are not auto-passed by booleans; they remain `REVIEW_REQUIRED`.

## Engineering boundary
`CONTROL_PRESENT != LEGAL_COMPLIANCE`

`ROUTER_APPLIES != CONTROL_PRESENT`

`DECLARED_EVIDENCE != INDEPENDENT_VERIFICATION`

`PROPOSED_TRANSITION != OPERATIVE_EXCEPTION`

`PASS_CONTROL != CUSTOMER_DEMAND`

`PASS_CONTROL != WTP`

`PASS_CONTROL != TRANSACTION`

No legal certification, buyer proof, WTP, transaction, profitability or external action is created by this hardening.

## Cross-store receipt
Drive folder: `15N2xm8iEYe5MBg7Jp3W1qazgLAdkD9Qp`  
Drive doc: `1zG-MB0LZ64hOkh4NXOQgP6phWo0p-uFcZ6pJjaXqo60`  
Marker: `P-EW03-PR367-BASE-PR370-SUPERSEDED-UNIQUE-CONTROL-VERIFICATION-SALVAGE-NO-PROOF-PROMOTION`
