# AGENT COMMERCE READINESS SCANNER v0 — P-EW01

**Date:** 2026-08-22  
**Status:** ENGINEERING CANDIDATE / DETERMINISTIC READINESS CHECKER / NO PLATFORM APPROVAL  
**Parent:** `OW-01 Agentic Commerce Merchant Readiness`  
**Ruleset:** `2026-08-22.1`

## Purpose
Convert current public agentic-commerce technical requirements into deterministic merchant-readiness findings. The scanner is deliberately narrower than an SEO audit or consultancy checklist.

It answers: **given a normalized, provenance-labelled merchant snapshot, which current feed/UCP requirements are satisfied, broken, unknown or not applicable?**

It does not crawl arbitrary sites by itself in v0 and it does not infer hidden merchant systems.

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
Every input lane must be labelled:
- `OBSERVED_PUBLIC`
- `PROBED_PUBLIC`
- `MERCHANT_DECLARED`
- `UNKNOWN`
- `NOT_APPLICABLE`

The scanner never upgrades one state into another. In particular, a public webpage cannot prove a private checkout implementation.

## Output states
Each rule emits exactly one:
- `PASS`
- `FAIL`
- `UNKNOWN`
- `NOT_APPLICABLE`

Overall disposition is fail-closed but not a magic score:
- any deterministic defect -> `BLOCKED_BY_DETERMINISTIC_DEFECT`;
- no defect but unresolved critical evidence -> `HOLD_UNRESOLVED_EVIDENCE`;
- all applicable checks pass -> `READY_FOR_PLATFORM_CONFORMANCE_TEST_NOT_APPROVAL`;
- no applicable evidence -> `NO_APPLICABLE_EVIDENCE`.

## Current source-derived rules

### OpenAI Agentic Commerce file-upload product feed
Current OpenAI product schema marks the following as required for the non-Ads feed path used by this scanner:
- `is_eligible_search`
- `is_eligible_checkout`
- `item_id`
- `title`
- `description`
- `url`
- `brand`
- `image_url`
- `price` with currency
- `availability`
- `seller_name`
- `seller_url`
- `return_policy`
- `target_countries`
- `store_country`

Conditional dependencies implemented:
- `is_eligible_checkout=true` requires `is_eligible_search=true`;
- checkout-eligible rows require seller privacy-policy and terms links;
- `pre_order` availability requires `availability_date`;
- price syntax includes a three-letter currency and must be positive in the scanner's normal physical-product path.

The scanner does not claim the schema above is complete for every vertical or Ads feed. Optional/recommended media, shipping, variant, review and compliance fields remain outside the v0 fatal core unless a later version promotes them with evidence.

### Google Universal Commerce Protocol (UCP)
Current Google UCP integration guidance provides an independently testable discovery surface:
- merchant publishes a public unauthenticated JSON profile at `/.well-known/ucp`;
- profile declares protocol version, services, capabilities, endpoints, payment handling and public keys;
- current Google guide exposes stable versions including `2026-04-08` and `2026-01-23`;
- native checkout requires core REST create/update/complete flows;
- identity path is guest checkout or identity linking; identity linking requires OAuth 2.0 metadata/endpoints;
- order integration requires lifecycle updates, including created/shipped/delivered, and signed webhook handling.

The v0 scanner accepts only versions known to the pinned ruleset. An unknown newer version yields `UNKNOWN` rather than FAIL so stale code cannot falsely reject a future valid merchant implementation.

## Normalized snapshot boundary
`scanner.py` consumes JSON. It intentionally separates acquisition from evaluation.

Example top-level shape:
```json
{
  "merchant_id": "merchant-01",
  "openai_feed": {
    "evidence_state": "MERCHANT_DECLARED",
    "products": []
  },
  "ucp": {
    "evidence_state": "PROBED_PUBLIC",
    "well_known_http_status": 200,
    "authentication_required": false,
    "profile": {},
    "checkout_endpoints": {"create": null, "update": null, "complete": null},
    "identity_path": "guest",
    "order_events": [],
    "order_request_signing": null
  }
}
```

`null` endpoint/signing values mean unproven, not failed.

## Rule families
### OAI-FEED
- `OAI-FEED-00` evidence/admissibility
- `OAI-FEED-01` non-empty observed/declared feed
- `OAI-FEED-02` required fields
- `OAI-FEED-03` search/checkout eligibility dependency
- `OAI-FEED-04` price/currency syntax
- `OAI-FEED-05` availability dependency
- `OAI-FEED-06` checkout seller policy links

### UCP
- `UCP-00` evidence/admissibility
- `UCP-01` public `/.well-known/ucp` HTTP 200
- `UCP-02` no authentication on public profile
- `UCP-03` parseable profile after HTTP 200
- `UCP-04` pinned protocol version
- `UCP-05` shopping service metadata/endpoint
- `UCP-06` checkout capability
- `UCP-07` create/update/complete endpoint probe state
- `UCP-08` guest vs identity-linking/OAuth path
- `UCP-09` order lifecycle event coverage
- `UCP-10` signing key declaration when order capability is used
- `UCP-11` order request-signing state

## Source authority
First-party / specification sources used for v0:
- OpenAI Developers — Agentic Commerce, `Products – File Upload` product schema, current crawl 2026-08.
- Google for Developers — UCP profile guide, last updated 2026-08-19.
- Google for Developers — UCP overview / production integration; public profile + 3 core native checkout endpoints + identity path + order sync.
- Google for Developers — Native checkout REST API version 2026-04-08.
- Google for Developers — Order lifecycle / signed updates.
- Universal Commerce Protocol GitHub/specification — open standard and current `2026-04-08` release.

## P-EW01 acceptance gate
P-EW01 is complete only if:
1. deterministic code exists;
2. UNKNOWN is preserved separately from FAIL;
3. at least one fully ready synthetic fixture reaches conformance-test readiness but never platform approval;
4. missing required feed fields fail;
5. UCP 404 fails;
6. identity-linking without OAuth metadata fails;
7. unknown future UCP version yields UNKNOWN, not FAIL;
8. missing mandatory order lifecycle event fails;
9. regression CI passes on exact PR head;
10. Drive mirror and semantic readback close.

P-EW01 does **not** execute P-EW02. Synthetic canaries are engineering evidence only; the 10-real-public-merchant blind test remains a separate gate.

READBACK_MARKER: `AGENT-COMMERCE-SCANNER-V0-P-EW01-SPEC-20260822`
