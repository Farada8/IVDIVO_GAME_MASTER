# OW-01 — AGENTIC COMMERCE WEDGE CORRECTION

**Date:** 2026-08-22  
**Status:** STRATEGIC MUTATION / ENGINEERING EVIDENCE UPDATED / NO WTP PROOF  
**Parent:** OW-01 Agentic Commerce Merchant Readiness

## Why this correction exists
The original OW-01 thesis was intentionally broad: merchants may need a readiness layer for machine-readable product, policy, checkout and agent-discovery surfaces.

P-EW02 plus current first-party platform evidence now makes one part of that thesis too weak to pursue:

`GENERIC UCP INSTALLATION FOR LARGE MANAGED COMMERCE PLATFORMS = KILL`

The wave remains real, but the sellable bottleneck is not "turn on UCP for a Shopify store".

## Corrected P-EW02 evidence
Ruleset `2026-08-22.3` was introduced after the frozen blind-10 exposed a second false-positive class in the scanner.

Frozen sample remains unchanged:
- decathlon.ie
- brownthomas.com
- arnotts.ie
- elverys.ie
- ikea.com
- lego.com
- patagonia.com
- allbirds.com
- glossier.com
- gymshark.com

Corrected rerun result:
- 10/10 evaluated;
- 0 network-inaccessible fixtures;
- 0 generic-advice outputs;
- 0 readiness/platform false promotions;
- 6 domains returned deterministic 404/410 for `/.well-known/ucp`;
- 4 domains returned HTTP 200 UCP 2026-04-08 profiles: `elverys.ie`, `allbirds.com`, `glossier.com`, `gymshark.com`;
- those four advertise usable `mcp + embedded` shopping bindings, checkout/order capabilities and payment-handler registries;
- those four now classify `HOLD_UNRESOLVED_EVIDENCE`, not `BLOCKED_BY_DETERMINISTIC_DEFECT`, because public profile evidence does not prove private OpenAI feed state or webhook/order conformance.

Scanner repair law:
`PUBLIC ORDER CAPABILITY + NO PROVEN WEBHOOK FLOW + NO SIGNING_KEYS != DETERMINISTIC FAILURE`

Additional repair laws:
`NON_REST_BINDING != REST_ENDPOINT_REQUIREMENT`
`NO IDENTITY_LINKING CAPABILITY != OAUTH DEFECT`
`UNKNOWN PRIVATE FEED != FAIL`

Ruleset PR: `#387`  
Merge: `75cc0f5b15b3a7199839626cea299a7f781c0d56`  
Exact-head scanner CI: `32568940358` SUCCESS  
Frozen blind-10 CI: `32568940347` SUCCESS  
Postmerge closure regression: `32568940386` SUCCESS

## Platform evidence and kill signal
### Shopify
Shopify Spring '26 states that Shopify Catalog and UCP are enabled by default for Shopify merchants, with eligible products entering Catalog by default and product data syndicated across AI channels without manual feeds. Shopify also opened its agentic-commerce layer self-serve to developers.

First-party sources:
- https://www.shopify.com/news/spring-26-edition-merchant
- https://www.shopify.com/news/spring-26-edition-dev

Implication:
`SELL_SHOPIFY_UCP_ENABLEMENT = WEAK/COMMODITIZING WEDGE`

### BigCommerce / Commerce
Commerce states that it has fully built to UCP across BigCommerce/Feedonomics and is already running agentic checkout/discovery flows on multiple AI surfaces.

First-party sources:
- https://investors.bigcommerce.com/news-releases/news-release-details/commerce-supports-universal-commerce-protocol-plans-offer-buying/
- https://investors.bigcommerce.com/static-files/24efd27b-3cfe-48dc-a92b-d0d9a269e89a

Implication:
`SELL_BIGCOMMERCE_BASIC_UCP_ENABLEMENT = WEAK WEDGE`

### WooCommerce
WooCommerce currently has native MCP support in developer preview and is expanding transport-neutral canonical abilities. A current Woo feature request still states that native UCP support is absent, while Woo/Stripe are building agentic-commerce integration through Stripe Agentic Commerce Suite.

First-party sources:
- https://developer.woocommerce.com/docs/features/mcp/
- https://developer.woocommerce.com/2026/05/12/mcp-abilities-api-10-9/
- https://woocommerce.com/feature-request/native-support-for-googles-universal-commerce-protocol-ucp-for-ai-agents/
- https://woocommerce.com/posts/stripe-agentic-commerce-suite-for-woocommerce/

Implication:
Woo is a moving integration surface, but a generic one-off "install UCP" service is vulnerable to being erased by core/plugin/platform releases.

## Corrected OW-01 economic hypothesis
### KILL / DO NOT BUILD A BUSINESS AROUND
1. Shopify UCP installation/setup as the primary offer.
2. BigCommerce basic UCP enablement as the primary offer.
3. generic "AI-ready ecommerce" audits that output narrative advice without deterministic protocol findings.
4. a manual service whose only value is copying platform defaults that the platform will automate.

### KEEP AS TESTABLE WEDGES
1. **Cross-protocol conformance/drift diagnostic**
   - UCP / MCP / platform-specific agent surfaces / product-feed contracts;
   - deterministic evidence-bound findings;
   - version-drift monitoring as protocols/platforms change.

2. **Custom/non-managed-stack readiness**
   - merchants or software vendors not automatically covered by Shopify/BigCommerce defaults;
   - custom commerce backends, headless implementations, bespoke checkout/order integrations.

3. **WooCommerce transition tooling**
   - only while there is a real current gap between MCP/abilities and full consumer agent-commerce interoperability;
   - must be rechecked before every offer because core/plugin support can erase the gap quickly.

4. **Product-data / agent-discovery quality diagnostics**
   - not "turn on protocol";
   - detect missing, stale, inconsistent or cross-channel product/availability/policy data that platforms cannot safely infer.

5. **Developer/tooling layer**
   - test harnesses, compatibility matrices, regression canaries, protocol-version migration checks;
   - potentially stronger compounding asset than one-off merchant setup.

## Founder-fit check
All retained wedges remain compatible with the current Founder profile:
- remote-first;
- near-zero physical participation;
- no inventory/warehouse;
- low initial cash exposure;
- reusable software/test assets can compound.

This is founder-fit only, not market proof.

## Monetization boundary
OW-01 remains:
`M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN`

No M2 promotion.

`WTP = UNKNOWN`
`PRICE = NULL`
`PAID TRANSACTIONS = 0`
`CAC = UNKNOWN`
`PROFITABILITY = UNPROVEN`

## Next gate
Do not add more scanner features solely because they are technically possible.

If external buyer testing becomes explicitly authorized, the first OW-01 test must use the corrected wedge:
**cross-protocol/custom-stack agent-commerce diagnostic**, not Shopify UCP enablement.

The test contract must predeclare:
- buyer role;
- exact diagnostic scope;
- sample selection;
- success/failure threshold;
- stop-loss;
- evidence capture;
- no legal/platform-approval claims.

If external testing is not authorized, return to Early-Wave Radar and monitor only material protocol/platform changes that can create or erase a bottleneck.

## Self-improvement laws
`EARLY_WAVE_REAL != FIRST_SERVICE_IDEA_GOOD`
`PLATFORM_DEFAULTS_CAN_ERASE_SERVICE_WEDGE`
`REAL_PROTOCOL_ADOPTION != MERCHANT_WTP_FOR_SETUP`
`SCANNER_FALSE_POSITIVE != MERCHANT_DEFECT`
`CORRECTED ENGINEERING EVIDENCE CAN MUTATE THE BUSINESS MODEL`
`DO_NOT_SELL WHAT THE PLATFORM ALREADY AUTOMATES`

READBACK_MARKER: `OW01-WEDGE-CORRECTION-RULESET03-KILL-GENERIC-UCP-SETUP-KEEP-CROSS-PROTOCOL-20260822`
