# OW-01 — AGENTIC COMMERCE WEDGE CORRECTION

**Date:** 2026-08-22  
**Status:** STRATEGIC MUTATION / ENGINEERING EVIDENCE UPDATED / NO WTP PROOF  
**Parent:** OW-01 Agentic Commerce Merchant Readiness

## Decision
The agentic-commerce wave remains real, but the original merchant-setup wedge is too broad.

`GENERIC UCP INSTALLATION FOR LARGE MANAGED COMMERCE PLATFORMS = KILL`

The sellable bottleneck is not "turn on UCP for a Shopify store".

## Evidence behind the mutation
Current Agent Commerce authority is ruleset `2026-08-22.3`, with P-EW02's same frozen 10-merchant sample preserved without substitution.

Corrected evidence:
- 10/10 merchants evaluated;
- 4 public UCP 2026-04-08 profiles;
- ruleset 0.3 corrected public-evidence false positives around MCP/embedded transport, REST-only probes, Identity Linking and unproven webhook signing;
- public/private UNKNOWN remains separate from deterministic FAIL;
- no platform approval, buyer demand, WTP, transaction or profitability proof was created.

Controlling ruleset correction: PR `#387`, merge `75cc0f5b15b3a7199839626cea299a7f781c0d56`.

## Platform kill signals
### Shopify
Shopify Spring '26 states that Shopify Catalog and UCP are enabled by default for Shopify merchants and that its agentic-commerce layer is becoming platform-native/self-serve.

First-party sources:
- https://www.shopify.com/news/spring-26-edition-merchant
- https://www.shopify.com/news/spring-26-edition-dev

Implication:
`SELL_SHOPIFY_UCP_ENABLEMENT = WEAK/COMMODITIZING WEDGE`

### BigCommerce / Commerce
Commerce states that it has built to UCP across BigCommerce/Feedonomics and is operating agentic discovery/checkout integrations.

First-party sources:
- https://investors.bigcommerce.com/news-releases/news-release-details/commerce-supports-universal-commerce-protocol-plans-offer-buying/
- https://investors.bigcommerce.com/static-files/24efd27b-3cfe-48dc-a92b-d0d9a269e89a

Implication:
`SELL_BIGCOMMERCE_BASIC_UCP_ENABLEMENT = WEAK WEDGE`

### WooCommerce
WooCommerce has native MCP in developer preview and is rapidly expanding canonical abilities/agent-commerce integrations. Native UCP remains a moving gap, not a durable monopoly.

First-party sources:
- https://developer.woocommerce.com/docs/features/mcp/
- https://developer.woocommerce.com/2026/05/12/mcp-abilities-api-10-9/
- https://woocommerce.com/feature-request/native-support-for-googles-universal-commerce-protocol-ucp-for-ai-agents/
- https://woocommerce.com/posts/stripe-agentic-commerce-suite-for-woocommerce/

Implication:
Any Woo-specific opportunity must be rechecked immediately before an offer because core/plugin/platform releases may erase the gap.

## KILL / DO NOT BUILD A BUSINESS AROUND
1. Shopify UCP installation/setup as the primary offer.
2. BigCommerce basic UCP enablement as the primary offer.
3. generic "AI-ready ecommerce" audits that output narrative advice without deterministic protocol findings.
4. manual work whose only value is reproducing platform defaults.

## KEEP AS TESTABLE WEDGES
1. **Cross-protocol conformance / drift diagnostic** — protocol/version compatibility, deterministic findings, regression monitoring.
2. **Custom / non-managed-stack readiness** — bespoke/headless commerce backends not automatically covered by managed-platform defaults.
3. **WooCommerce transition tooling** — only while a current verified gap exists.
4. **Product-data / agent-discovery quality diagnostics** — missing/stale/inconsistent product, availability, policy and discovery data.
5. **Developer regression / migration tooling** — reusable compatibility matrices, canaries and protocol-version migration checks.

## Founder fit
Retained wedges remain:
- remote-first;
- near-zero founder physical participation;
- no inventory/warehouse;
- low initial cash exposure;
- reusable software/test assets can compound.

Founder fit is not market proof.

## Monetization boundary
OW-01 remains:
`M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN`

`WTP = UNKNOWN`
`PRICE = NULL`
`PAID TRANSACTIONS = 0`
`CAC = UNKNOWN`
`PROFITABILITY = UNPROVEN`

## Next gate
Do not add more scanner features merely because they are technically possible.

If external buyer testing becomes explicitly authorized, test **cross-protocol/custom-stack agent-commerce diagnostics**, not generic Shopify/BigCommerce UCP setup.

If external testing remains unauthorized, return to Early-Wave Radar and monitor only material protocol/platform changes that create or erase bottlenecks.

## Self-improvement laws
`EARLY_WAVE_REAL != FIRST_SERVICE_IDEA_GOOD`
`PLATFORM_DEFAULTS_CAN_ERASE_SERVICE_WEDGE`
`REAL_PROTOCOL_ADOPTION != MERCHANT_WTP_FOR_SETUP`
`SCANNER_FALSE_POSITIVE != MERCHANT_DEFECT`
`CORRECTED_ENGINEERING_EVIDENCE_CAN_MUTATE_THE_BUSINESS_MODEL`
`DO_NOT_SELL_WHAT_THE_PLATFORM_ALREADY_AUTOMATES`

Drive mirror: `1GWGxroh4L8MQQOTf3xyX_M_pDHz3brTfmabURJHCd2w`  
Drive semantic readback: PASS.

READBACK_MARKER: `OW01-WEDGE-CORRECTION-RULESET03-KILL-GENERIC-UCP-SETUP-KEEP-CROSS-PROTOCOL-20260822`
