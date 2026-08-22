# AGENT COMMERCE READINESS SCANNER v0 — P-EW01 + P-EW02 CALIBRATION

**Date:** 2026-08-22  
**Status:** DETERMINISTIC READINESS CHECKER / REAL-FIXTURE CALIBRATED / NO PLATFORM APPROVAL  
**Parent:** `OW-01 Agentic Commerce Merchant Readiness`  
**Ruleset:** `2026-08-22.2`

## Purpose
Convert current public agentic-commerce technical requirements into deterministic merchant-readiness findings. The scanner is deliberately narrower than an SEO audit or consultancy checklist.

It answers: **given a normalized, provenance-labelled merchant snapshot, which current feed/UCP requirements are satisfied, broken, unknown or not applicable?**

It does not infer hidden merchant systems. Acquisition and evaluation remain separate.

## Core contracts
`READINESS != PLATFORM_APPROVAL`  
`MACHINE_READABLE != AGENTIC_CHECKOUT_READY`  
`PRODUCT_FEED_READY != UCP_READY`  
`UCP_PROFILE_PRESENT != ENDPOINT_VALID`  
`CHECKOUT_ENDPOINT_PRESENT != SAFE_TRANSACTION`  
`PUBLIC_PAGE_OBSERVATION != MERCHANT_DECLARATION`  
`UNKNOWN != FAIL`  
`UNKNOWN != PASS`  
`PROTOCOL_SPEC_CHANGE -> VERSIONED_RULESET`  
`GENERIC_ADVICE_OUTPUT = SCANNER_FAILURE`

## Evidence states
Every input lane is labelled `OBSERVED_PUBLIC`, `PROBED_PUBLIC`, `MERCHANT_DECLARED`, `UNKNOWN`, or `NOT_APPLICABLE`. The scanner never silently upgrades one evidence state into another. A public product page does not prove a private OpenAI feed or private checkout implementation.

## Output states
Every rule emits exactly one of `PASS`, `FAIL`, `UNKNOWN`, `NOT_APPLICABLE`.

Overall disposition is fail-closed without a magic score:
- any deterministic defect -> `BLOCKED_BY_DETERMINISTIC_DEFECT`;
- no deterministic defect but unresolved critical evidence -> `HOLD_UNRESOLVED_EVIDENCE`;
- all applicable checks pass -> `READY_FOR_PLATFORM_CONFORMANCE_TEST_NOT_APPROVAL`;
- no applicable evidence -> `NO_APPLICABLE_EVIDENCE`.

## OpenAI Agentic Commerce feed lane
For the pinned non-Ads file-upload product-feed path, the scanner checks required product identity, descriptive, URL/image, price/currency, availability, seller, return-policy and geo fields plus search/checkout eligibility dependencies and checkout seller-policy links.

A public product page is never promoted into evidence that an OpenAI upload feed exists. If an admissible feed observation/declaration is absent, this lane remains `UNKNOWN`.

## UCP lane — ruleset 2026-08-22.2
The public discovery surface is `/.well-known/ucp`. The profile can declare protocol version, services, capabilities and public signing material.

Supported shopping-service transports in the pinned ruleset are:
- `rest`
- `mcp`
- `a2a`
- `embedded`

Transport-specific validation is binding-aware:
- REST/MCP/A2A service entries require a discoverable endpoint plus version/spec/schema where applicable;
- an embedded service declaration does not require its own separate service endpoint;
- an unknown future transport yields `UNKNOWN`, not a stale-code FAIL.

Known pinned UCP versions remain `2026-04-08` and `2026-01-23`; a newer unknown version yields `UNKNOWN` pending ruleset refresh.

### Order evidence discipline
When Order capability is declared:
- explicit observed/declaration event coverage can be checked for required lifecycle behavior;
- **unprobed** order lifecycle implementation is `UNKNOWN`, not missing-event FAIL;
- public `signing_keys` are checked at profile level because the pinned UCP Order spec requires signed webhooks and verification against the business profile;
- request-signing execution itself remains `UNKNOWN` unless observed or declared.

## Rule families
### OAI-FEED
`OAI-FEED-00..06`: admissibility, non-empty feed, required fields, eligibility dependency, price/currency, availability dependency, checkout seller policy.

### UCP
`UCP-00` evidence/admissibility  
`UCP-01` public discovery HTTP 200  
`UCP-02` no authentication on public profile  
`UCP-03` parseable profile  
`UCP-04` pinned protocol version  
`UCP-05` shopping service/binding validity  
`UCP-06` checkout capability  
`UCP-07` checkout endpoint probe state  
`UCP-08` guest vs identity-linking/OAuth state  
`UCP-09` order lifecycle evidence state  
`UCP-10` profile signing-key declaration when Order is declared  
`UCP-11` order request-signing evidence state

## Real-fixture calibration — P-EW02
P-EW02 was executed on a frozen 10-merchant public sample and merged via PR #353. Four merchants exposed valid UCP `2026-04-08` public profiles with `mcp + embedded` shopping transports.

That test falsified two scanner-v0.1 assumptions:
1. REST-only service validation was wrong; MCP/embedded are valid UCP bindings.
2. Unprobed order events were incorrectly collapsed to an empty observed set.

Ruleset `2026-08-22.2` repairs both. Across the four UCP-200 fixtures, eight false-negative findings were removed (`UCP-05` and `UCP-09` on each merchant).

The captured profiles declared Order capability but did not expose `signing_keys`; under the pinned Order specification the scanner therefore retains a profile-level `UCP-10 FAIL`. This finding is bounded to the public profile and is not a global merchant-compliance claim.

P-EW02 evidence receipt:
`../18_AGENT_COMMERCE_PEW02_BLIND10/02_BLIND10_RESULTS_AND_SCANNER_PATCH.md`

## Source authority
Primary current sources include:
- OpenAI Developers — Agentic Commerce product-feed schema;
- Universal Commerce Protocol — overview/service discovery, including REST/MCP/A2A/embedded;
- Universal Commerce Protocol — Order capability and signed webhook requirements.

Pinned references:
- `https://ucp.dev/latest/`
- `https://ucp.dev/specification/order/`

## Evidence boundary
Synthetic and real-fixture scanner tests are engineering evidence only. They do not prove merchant demand, WTP, platform approval, transaction readiness, transactions, profitability or an early-wave winner.

READBACK_MARKER: `AGENT-COMMERCE-SCANNER-V0-RULESET-20260822-2-PEW02-CALIBRATED`
