# P-EW01 / P-EW02 — PRIMARY SOURCE LEDGER

**Captured:** 2026-08-22  
**Use:** engineering requirements only; not market proof.

| ID | Source | Dated / freshness | Supported use |
|---|---|---|---|
| S01 | OpenAI — `Powering Product Discovery in ChatGPT` — https://openai.com/index/powering-product-discovery-in-chatgpt/ | 2026-03-24 | ACP extends into product discovery; product feeds/promotions; named retailers integrated into ACP for discovery; Shopify Catalog provides product-data integration; Walmart in-ChatGPT app. |
| S02 | OpenAI — `Buy it in ChatGPT: Instant Checkout and the Agentic Commerce Protocol` — https://openai.com/index/buy-it-in-chatgpt/ | 2025-09-29, historical architecture source | ACP merchant-of-record model; historical Instant Checkout launch; merchant control of payment/fulfillment/customer relationship. Do not treat 2025 rollout status as current without later source. |
| S03 | ACP specification — https://www.agenticcommerce.dev/docs/reference/checkout and public protocol repository | current spec family, repository updated 2026 | Checkout sessions, authoritative state, HTTPS/JSON, authentication/signature/idempotency/versioning/fulfillment/order mechanics. |
| S04 | Google Developers — UCP Profile — https://developers.google.com/merchant/ucp/guides/ucp-profile | current 2026 guidance | Public `/.well-known/ucp`; versions, services, capabilities, payment handlers, signing keys. |
| S05 | Google Developers — UCP Overview — https://developers.google.com/merchant/ucp/guides/overview | updated 2026-08-13 | Merchant Center + product feed/shipping/returns preparation; UCP profile; native checkout endpoints; optional OAuth identity linking; order status sync. |
| S06 | UCP specification — https://ucp.dev/latest/ | current 2026 | Capability negotiation, business profile, key discovery, version compatibility, protocol-neutral rules. |
| S07 | FIDO Alliance — Google donates AP2 / agentic authentication standards — https://fidoalliance.org/fido-alliance-to-develop-standards-for-trusted-ai-agent-interactions/ and https://fidoalliance.org/google-donates-agent-payments-protocol-to-fido-alliance/ | 2026-04-28/29 | AP2/open agentic payment standards are forming; do not hard-code merchant readiness to one payment protocol. |
| S08 | Visa — OpenAI collaboration — https://investor.visa.com/news/news-details/2026/Visa-Partners-with-OpenAI-to-Power-the-Next-Generation-of-AI-Commerce/default.aspx | 2026-06-10 | Independent payment-network evidence that agentic commerce/payment infrastructure is active. |
| S09 | Mastercard — Agent Pay for Machines — https://www.mastercard.com/us/en/news-and-trends/press/2026/june/mastercard-launches-agent-pay-for-machines.html | 2026-06-10 | Credentialing, permissioning, transacting, settlement; 30+ supporters; independent trust/payment-rail evidence. |
| S10 | Linux Foundation — A2A first-year production milestone — https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year | 2026-04-09 | A2A production/open interoperability signal; complements MCP; does not make A2A mandatory for a merchant. |
| S11 | Linux Foundation — DNS-AID — https://www.linuxfoundation.org/press/linux-foundation-announces-dns-aid-project-to-advance-decentralized-ai-agent-discovery | 2026-05-27 | Open decentralized agent/MCP discovery is forming; merchant adoption is optional/unknown unless observed. |
| S12 | Linux Foundation — Agentic AI Foundation report — https://www.linuxfoundation.org/hubfs/Research%20Reports/Open%20Source%20and%20the%20Future%20of%20AI_Report_2026.pdf | 2026 | AAIF is neutral home anchored by MCP, AGENTS.md and Goose; supports interoperability thesis, not merchant demand. |
| S13 | Etsy current investor/public material — https://investors.etsy.com/sec-filings/all-sec-filings/content/0001370637-26-000079/q226shareholderletter.htm | 2026-08-05 | Etsy continues testing/using agentic shopping; current channel evidence. |
| S14 | Etsy — Google AI-powered shopping partnership — https://www.etsy.com/ca/news/etsy-partners-with-google-on-ai-powered-shopping | 2026 | UCP-powered Etsy/Google partnership and UCP co-development evidence. |
| S15 | Lloyds Online Doctor Ireland public UCP profile — https://lloydsonlinedoctor.ie/.well-known/ucp | observed/indexed 2026 | Real public profile fixture: UCP 2026-04-08; MCP/embedded services; checkout/cart/order/catalog capabilities; Shopify catalog; payment handlers. Presence proves exposed declarations, not end-to-end conformance. |

## Current OpenAI discovery facts used for fixtures
S01 explicitly states that **Target, Sephora, Nordstrom, Lowe’s, Best Buy, The Home Depot, and Wayfair** have integrated into ACP for discovery. It separately states that Shopify product data is integrated through Shopify Catalog and individual Shopify merchants do not need additional work for product-data participation. These facts are used only as positive discovery evidence; they are never promoted to deterministic checkout readiness.

## Source precedence
Current primary vendor/protocol documentation > current first-party merchant statement > older launch announcement > third-party commentary.

Third-party articles are not used to manufacture protocol requirements.
