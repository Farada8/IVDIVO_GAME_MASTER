# P-EW01 / P-EW02 — AGENT COMMERCE READINESS SCANNER v0

**Date:** 2026-08-22  
**Parent authority:** `GENERAL_BUSINESS_DISCOVERY_PRODUCTION_ENGINE_V1/16_EARLY_WAVE_RADAR_STATE.json`  
**Lane:** `OW-01 Agentic Commerce Merchant Readiness Layer`  
**Status:** INTERNAL ENGINEERING / PUBLIC-EVIDENCE BLIND TEST / NO MARKET-PROOF PROMOTION

## 1. Objective
Build a vendor-neutral scanner that can separate protocol-specific merchant readiness evidence from generic ecommerce/SEO advice, then blind-test it on ten public merchant fixtures.

This scanner is not a compliance certificate, security audit, integration certification, or proof that a merchant needs outside help.

## 2. Evidence laws
`PUBLIC_SIGNAL != MERCHANT_INTERNAL_STATE`  
`NOT_OBSERVABLE_PUBLICLY != ABSENT`  
`PARTNER_ANNOUNCEMENT != COMPLETE_PROTOCOL_IMPLEMENTATION`  
`DISCOVERY_INTEGRATION != CHECKOUT_INTEGRATION`  
`SHOPIFY_CATALOG_INTEGRATION != INDIVIDUAL_MERCHANT_BACKEND_WORK`  
`UCP_PROFILE_PRESENT != FULL_UCP_CONFORMANCE`  
`ACP_DISCOVERY != ACP_CHECKOUT`  
`PROTOCOL_SPECIFIC_GAP != GENERIC_SEO_ADVICE`  
`SCANNER_OUTPUT != WTP`  
`TEN_FIXTURE_TEST != MARKET VALIDATION`

## 3. Primary-source-derived protocol surfaces
### UCP
The Universal Commerce Protocol exposes a public business profile at `/.well-known/ucp`. The profile can declare versions, services/transports/endpoints, capabilities, payment handlers, and signing keys. Google’s current implementation guidance also uses the profile as a production-validation surface.

Scanner-visible UCP dimensions:
1. public profile discoverability;
2. protocol version and supported versions;
3. service transport(s) and endpoints;
4. declared capabilities: catalog/search, cart, checkout, fulfillment, order, identity linking where applicable;
5. payment handler declarations;
6. signing/public-key material where the profile/spec requires it;
7. consistency between declared capability and publicly observable evidence, when any.

### ACP
The Agentic Commerce Protocol supports product discovery and agentic checkout. Current OpenAI material says merchants can share product feeds/promotions for discovery, while the checkout specification defines stateful checkout endpoints and requires protocol-specific robustness such as authenticated requests, signatures, idempotency, request tracing, versioning, authoritative cart state, fulfillment options and order completion.

Scanner-visible ACP dimensions:
1. documented product/discovery integration;
2. documented checkout integration versus discovery-only;
3. checkout interface evidence only when explicitly public/authorized;
4. authoritative cart/price/availability/fulfillment state;
5. security/idempotency/versioning evidence only when observable or supplied by the merchant.

### AP2 / trust / interoperability
FIDO states that agentic commerce standards work is drawing on Google AP2 and Mastercard Verifiable Intent. Mastercard separately exposes credentialing, permissioning, transacting and settlement as foundational machine-payment capabilities. A2A, MCP/AAIF and DNS-AID show that agent discovery/interoperability is an evolving open-infrastructure layer, but their existence does not imply a retailer must expose any one of them.

The scanner therefore records these as `VENDOR_SPECIFIC_UNKNOWN` unless a merchant explicitly exposes/claims a relevant surface.

## 4. Allowed observation states
Each observable accepts one of:
- `PRESENT`
- `ABSENT_VERIFIED`
- `NOT_OBSERVABLE_PUBLICLY`
- `VENDOR_SPECIFIC_UNKNOWN`
- `NOT_APPLICABLE`

`ABSENT_VERIFIED` requires an authoritative negative observation. Search-engine non-finding is never enough.

## 5. Issue classifications
- `ACTIONABLE_GAP` — a protocol-specific required/declared surface is verifiably absent or internally inconsistent.
- `NOT_OBSERVABLE_PUBLICLY` — backend/security/checkout state cannot be inferred from the public web.
- `VENDOR_SPECIFIC_UNKNOWN` — platform/onboarding/protocol-specific state cannot be resolved from admissible evidence.
- `NOISE` — generic SEO, page aesthetics, or unrelated website advice incorrectly presented as agent-commerce readiness.

Positive evidence is recorded separately as `POSITIVE_SIGNAL`; it is not an issue.

## 6. Scanner dimensions
`D1_DISCOVERY_CHANNEL` — official evidence of ACP/UCP/other agentic discovery participation.  
`D2_UCP_PUBLIC_PROFILE` — `/.well-known/ucp` profile only when directly observed.  
`D3_CAPABILITY_DECLARATION` — catalog/cart/checkout/fulfillment/order capabilities if a UCP profile is observed.  
`D4_PRODUCT_DATA_PLANE` — official product feed/catalog integration evidence.  
`D5_CHECKOUT_STATE_PLANE` — documented deterministic checkout interface; never infer from a human checkout page alone.  
`D6_FULFILLMENT_ORDER_STATE` — machine-usable fulfillment/order lifecycle only when protocol evidence exists.  
`D7_AUTHORIZATION_TRUST` — signatures, idempotency, permission/intent boundaries where observable/authorized.  
`D8_PAYMENT_HANDLER_BOUNDARY` — payment handlers/processor boundary from protocol evidence.  
`D9_AGENT_DISCOVERY_INTEROP` — A2A/MCP/DNS-AID or equivalent only when explicitly exposed.  
`D10_EVIDENCE_FRESHNESS` — current dated source versus historical announcement.

## 7. Anti-generic gate
The scanner MUST NOT recommend any of the following merely because they are common ecommerce advice:
- “improve SEO”;
- “add more keywords”;
- “write better product descriptions”;
- “make the site faster” without a protocol-specific failure;
- “add llms.txt” as a universal agent-commerce requirement;
- generic schema.org advice as a substitute for ACP/UCP evidence.

If the result ledger collapses into generic advice, `P-EW02 = FAIL_GENERIC_ADVICE`.

## 8. Blind-test design
Ten named public merchants are mapped to anonymous fixture IDs before routing. The scanner consumes only normalized evidence fields. Merchant names are rejoined after output generation.

The test intentionally includes:
- merchants with officially documented ACP discovery integration;
- a Shopify-catalog example where OpenAI says individual merchant discovery work is not required;
- a merchant with a directly observable public UCP profile;
- merchants with strong agentic-channel evidence but private backend checkout/security state.

This is designed to punish hallucinated “gaps”. A good scanner should often return `NOT_OBSERVABLE_PUBLICLY`, not manufacture failures.

## 9. P-EW01 acceptance
PASS only if:
- protocol-specific dimensions are executable;
- tri-state/fail-closed evidence handling works;
- positive evidence is separate from deficiencies;
- generic SEO signals cannot change readiness disposition;
- no merchant-internal state is inferred from public branding/partnership announcements.

## 10. P-EW02 acceptance
PASS only if all ten fixtures run deterministically and:
- every issue is one of the four allowed classifications;
- a directly observed UCP profile is parsed into protocol-specific positive signals;
- documented ACP discovery is not falsely upgraded to checkout readiness;
- non-observable backend controls stay non-observable;
- generic SEO noise is ignored;
- output contains concrete next verification actions rather than narrative hype.

`P-EW02 PASS != COMMERCIAL WINNER`.

## 11. External-action boundary
No outreach, merchant probing behind authentication, checkout transaction, account creation, purchase, payment, vulnerability testing, scraping bypass, or representation of certification is authorized.
