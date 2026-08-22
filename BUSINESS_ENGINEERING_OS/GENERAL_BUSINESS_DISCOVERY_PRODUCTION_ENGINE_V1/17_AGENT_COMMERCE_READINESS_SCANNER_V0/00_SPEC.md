# AGENT COMMERCE READINESS SCANNER v0 — CURRENT RULESET

**Date:** 2026-08-22  
**Status:** DETERMINISTIC READINESS CHECKER / REAL-FIXTURE CALIBRATED / PUBLIC-EVIDENCE CORRECTED / NO PLATFORM APPROVAL  
**Parent:** `OW-01 Agentic Commerce Merchant Readiness`  
**Current ruleset:** `2026-08-22.3`

## Purpose
Given a normalized provenance-labelled merchant snapshot, emit evidence-bounded OpenAI product-feed and UCP readiness findings as `PASS / FAIL / UNKNOWN / NOT_APPLICABLE` without inferring hidden merchant systems.

Acquisition and evaluation are separate. Public observation never becomes merchant-declared private state.

## Core contracts
`READINESS != PLATFORM_APPROVAL`  
`MACHINE_READABLE != AGENTIC_CHECKOUT_READY`  
`PRODUCT_FEED_READY != UCP_READY`  
`UCP_PROFILE_PRESENT != ENDPOINT_VALID`  
`PUBLIC_PAGE_OBSERVATION != MERCHANT_DECLARATION`  
`UNKNOWN != FAIL`  
`UNKNOWN != PASS`  
`PROTOCOL_SPEC_CHANGE -> VERSIONED_RULESET`  
`GENERIC_ADVICE_OUTPUT = SCANNER_FAILURE`

## Evidence states
Input evidence remains one of `OBSERVED_PUBLIC`, `PROBED_PUBLIC`, `MERCHANT_DECLARED`, `UNKNOWN`, `NOT_APPLICABLE`.

A public product page does not prove a private OpenAI feed. A public capability declaration does not by itself prove execution of a private checkout, identity or webhook path.

## OpenAI feed lane
The pinned feed path checks required product identity/descriptive/URL/image/price/availability/seller/return-policy/geo fields and eligibility/policy dependencies. Without admissible feed evidence, the lane stays `UNKNOWN`.

## UCP service discovery
Current supported shopping transports:
- `rest`
- `mcp`
- `a2a`
- `embedded`

Binding-aware rules:
- REST/MCP/A2A require their applicable endpoint metadata;
- embedded does not require a separate endpoint;
- unknown future transport -> `UNKNOWN`, not FAIL;
- REST checkout endpoint probes apply only when a REST binding is advertised.

## Ruleset 2026-08-22.3 correction
Merged PR #387 corrected a second real-fixture false-positive class after the original P-EW02 receipt.

### Order capability
Public declaration of `dev.ucp.shopping.order` does **not** prove that the tested merchant path actually uses webhook delivery.

Therefore:
- `order_events=None` -> `UCP-09 UNKNOWN`;
- Order capability + missing `signing_keys` + webhook-flow use **unproven** -> `UCP-10 UNKNOWN`;
- explicit/observed webhook flow + missing `signing_keys` -> `UCP-10 FAIL`;
- explicit non-webhook tested path -> `UCP-10 NOT_APPLICABLE`;
- request-signing status is judged only after webhook-flow applicability is established.

This supersedes the old ruleset-0.2 interpretation that Order capability plus absent public `signing_keys` was automatically a deterministic profile defect.

### Identity linking
The OAuth evidence gate applies only when `dev.ucp.common.identity_linking` is advertised. Otherwise that gate is `NOT_APPLICABLE`.

### Payment handlers
`payment_handlers` is now a separate structural/evidence rule (`UCP-05P`). Absence is not automatically a deterministic checkout defect because valid non-payment paths can exist; malformed present structure can still fail deterministically.

## Historical P-EW02 receipt
The P-EW02 blind-10 evidence and hashes remain historically valid: same frozen 10 merchants, no substitution. Its ruleset-0.2 interpretation is preserved as historical evidence, not current scanner authority.

Current correction receipt:
`../18_AGENT_COMMERCE_PEW02_BLIND10/05_RULESET_03_PUBLIC_EVIDENCE_CORRECTION.md`

## Current rule families
### OAI-FEED
`OAI-FEED-00..06`

### UCP
`UCP-00` evidence/admissibility  
`UCP-01` public discovery  
`UCP-02` unauthenticated profile access  
`UCP-03` parseability  
`UCP-04` pinned version  
`UCP-05` shopping service/binding validity  
`UCP-05P` payment-handler structural/evidence state  
`UCP-06` checkout capability  
`UCP-07` REST checkout probe when applicable  
`UCP-08` Identity Linking OAuth when applicable  
`UCP-09` order lifecycle evidence state  
`UCP-10` signing-key evidence conditional on webhook-flow applicability  
`UCP-11` order request-signing evidence conditional on webhook-flow applicability

## Engineering authority
- P-EW01 implementation: PR #348.
- P-EW02 historical blind-10: PR #353.
- P-EW02 closure: PR #365.
- public-evidence ruleset correction: PR #387, merged; same frozen sample re-used; scanner regression expanded to 20 canaries.
- P-EW05 controlling General Business closure: PR #382; all three Early-Wave lanes M1, no M2/WTP proof.

## Evidence boundary
This scanner produces engineering evidence only. It does not prove merchant demand, WTP, platform approval, legal compliance, actual private transaction implementation, transactions, profitability or an early-wave winner.

READBACK_MARKER: `AGENT-COMMERCE-SCANNER-RULESET-2026-08-22-3-PUBLIC-EVIDENCE-CORRECTED`
