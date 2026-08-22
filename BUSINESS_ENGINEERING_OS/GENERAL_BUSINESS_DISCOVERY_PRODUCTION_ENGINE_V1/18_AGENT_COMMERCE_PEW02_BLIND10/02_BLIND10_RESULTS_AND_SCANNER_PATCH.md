# P-EW02 — BLIND10 RESULTS + REAL-FIXTURE SCANNER PATCH

**Date:** 2026-08-22  
**Parent:** OW-01 Agentic Commerce Merchant Readiness  
**Frozen sample:** 10 merchants from `00_BLIND_PROTOCOL.md`; no substitutions.  
**Authority:** merged PR #353, merge `0f83a4b223b8355b7163616d2a2cec527ec228db`.  
**Evidence run:** GitHub Actions `32558173769` on exact head `14a950014cfd3a98b6ab340d9ea82e4ef8a9ca9e`.  
**Actions artifact:** `9472016122`, digest `sha256:7a9a413460d1f2f154b10a15ce0746bd1d07f7df57975641288aa4e09349dcf9`.  
**Scanner ruleset after real-fixture correction:** `2026-08-22.2`.

## Result
`P-EW02 = PASS_TEST` for scanner discrimination/evidence discipline only.

- 10/10 frozen merchants evaluated; sample substitution = 0.
- 10/10 returned an HTTP response; network-error count = 0.
- generic-advice output count = 0.
- false readiness/platform-approval promotions = 0.
- private OpenAI product feed was not inferred from public product pages.
- no transaction-changing checkout probe, cart, order, account or outreach occurred.

This does **not** prove buyer demand, WTP, merchant adoption, platform approval, transactions or profitability.

## Frozen 10
| Merchant | `/.well-known/ucp` | Public profile | Transport | Checkout / Order | `signing_keys` observed | Current scanner finding |
|---|---:|---|---|---|---|---|
| decathlon.ie | 404 | no | — | — | — | `UCP-01 FAIL` |
| brownthomas.com | 410 | no | — | — | — | `UCP-01 FAIL` |
| arnotts.ie | 410 | no | — | — | — | `UCP-01 FAIL` |
| elverys.ie | 200 | UCP 2026-04-08 | mcp + embedded | both declared | no | `UCP-10 FAIL`; unprobed lanes UNKNOWN |
| ikea.com | 404 | no | — | — | — | `UCP-01 FAIL` |
| lego.com | 404 | no | — | — | — | `UCP-01 FAIL` |
| patagonia.com | 410 | no | — | — | — | `UCP-01 FAIL` |
| allbirds.com | 200 | UCP 2026-04-08 | mcp + embedded | both declared | no | `UCP-10 FAIL`; unprobed lanes UNKNOWN |
| glossier.com | 200 | UCP 2026-04-08 | mcp + embedded | both declared | no | `UCP-10 FAIL`; unprobed lanes UNKNOWN |
| gymshark.com | 200 | UCP 2026-04-08 | mcp + embedded | both declared | no | `UCP-10 FAIL`; unprobed lanes UNKNOWN |

## Scanner corrections forced by real fixtures
The first blind execution falsified two v0.1 assumptions:

1. MCP was incorrectly rejected by a REST-only service rule. UCP supports multiple shopping-service transports, including REST, MCP, A2A and embedded. Ruleset `2026-08-22.2` accepts the supported transports and does not require a separate endpoint for an embedded binding.
2. `order_events=None` was incorrectly collapsed into an empty observed set. It now yields `UCP-09 UNKNOWN`; only explicit evidence showing missing required event coverage yields FAIL.

That repairs **8 false-negative findings**: UCP-05 + UCP-09 on each of the four UCP-200 merchants.

## Remaining profile-level gate
All four observed UCP-200 profiles declare `dev.ucp.shopping.order`, but no `signing_keys`/`keys` were observed in the captured public profile. Under the pinned current UCP Order specification, order webhook payloads MUST be signed, signing uses a key from `signing_keys` in the business UCP profile, and verification locates that key in the profile.

Therefore:
`ORDER_CAPABILITY + NO_PUBLIC_PROFILE_SIGNING_KEYS -> UCP-10 FAIL UNDER PINNED SPEC`.

This is a public-profile-level finding only. It is **not** a claim that a merchant is globally noncompliant, rejected by a platform or unable to transact.

Primary spec references:
- `https://ucp.dev/latest/`
- `https://ucp.dev/specification/order/`

## Learned laws
`MCP_TRANSPORT != INVALID_UCP`  
`EMBEDDED_WITHOUT_SERVICE_ENDPOINT != INVALID_UCP`  
`UNPROBED_ORDER_EVENTS != MISSING_ORDER_EVENTS`  
`UNKNOWN_FUTURE_TRANSPORT -> UNKNOWN_NOT_FAIL`  
`PUBLIC_UCP_PROFILE != PLATFORM_APPROVAL`  
`PUBLIC_PRODUCT_PAGE != OPENAI_PRODUCT_FEED`  
`BLIND_TEST_PASS != BUYER_DEMAND`  
`PUBLIC_PROFILE_DEFECT != GLOBAL_MERCHANT_NONCOMPLIANCE`

## Causal effect
OW-01 now has real-fixture engineering evidence rather than synthetic-only evidence. More importantly, real merchants caused a reproducible scanner patch, demonstrating the intended self-correction loop. Market proof is still absent.

Next route under current WIP orchestration: `P-EW03` Article 50 Technical Transparency sample pack unless a newer CURRENT authority changes the frontier.

READBACK_MARKER: `AGENT-COMMERCE-P-EW02-BLIND10-PASS-4UCP200-8FALSEFAILS-CORRECTED-NO-DEMAND-PROOF`
