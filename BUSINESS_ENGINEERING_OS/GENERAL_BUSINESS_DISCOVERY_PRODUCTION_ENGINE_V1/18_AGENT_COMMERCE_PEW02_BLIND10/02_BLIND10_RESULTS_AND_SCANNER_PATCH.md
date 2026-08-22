# P-EW02 — BLIND10 RESULTS + REAL-FIXTURE SCANNER PATCH

**Date:** 2026-08-22  
**Parent:** OW-01 Agentic Commerce Merchant Readiness  
**Frozen sample:** 10 merchants from `00_BLIND_PROTOCOL.md`; no substitutions.  
**Evidence run:** GitHub Actions `32558173769` on head `14a950014cfd3a98b6ab340d9ea82e4ef8a9ca9e`.  
**Actions artifact:** `9472016122`, digest `sha256:7a9a413460d1f2f154b10a15ce0746bd1d07f7df57975641288aa4e09349dcf9`.  
**Scanner ruleset after real-fixture correction:** `2026-08-22.2`.

## Test result
`P-EW02 = PASS_TEST` for scanner discrimination/evidence discipline only.

- 10/10 frozen merchants evaluated.
- 10/10 returned an HTTP response at the public UCP discovery URL.
- network-error count = 0.
- generic-advice output count = 0.
- false readiness/platform-approval promotions = 0.
- private OpenAI product feed was not inferred from public product pages for any merchant.
- no transaction-changing checkout probe, cart, order, account or outreach occurred.

This does **not** prove buyer demand, WTP, merchant adoption, platform approval, transactions or profitability.

## Frozen 10 results
| Merchant | `/.well-known/ucp` | Public UCP profile | v2026-04-08 | Transport | Checkout | Order | `signing_keys` observed | Current scanner result |
|---|---:|---|---|---|---|---|---|---|
| decathlon.ie | 404 | no | — | — | — | — | — | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-01`) |
| brownthomas.com | 410 | no | — | — | — | — | — | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-01`) |
| arnotts.ie | 410 | no | — | — | — | — | — | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-01`) |
| elverys.ie | 200 | yes | yes | mcp + embedded | declared | declared | no | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-10`); unresolved probes stay UNKNOWN |
| ikea.com | 404 | no | — | — | — | — | — | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-01`) |
| lego.com | 404 | no | — | — | — | — | — | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-01`) |
| patagonia.com | 410 | no | — | — | — | — | — | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-01`) |
| allbirds.com | 200 | yes | yes | mcp + embedded | declared | declared | no | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-10`); unresolved probes stay UNKNOWN |
| glossier.com | 200 | yes | yes | mcp + embedded | declared | declared | no | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-10`); unresolved probes stay UNKNOWN |
| gymshark.com | 200 | yes | yes | mcp + embedded | declared | declared | no | `BLOCKED_BY_DETERMINISTIC_DEFECT` (`UCP-10`); unresolved probes stay UNKNOWN |

## Real-fixture scanner defects discovered and repaired
The first blind run exposed two false-negative rules in scanner v0.1:

1. **MCP transport was incorrectly treated as invalid.** Current UCP supports multiple service transports including REST, MCP, A2A and embedded. The four observed UCP profiles advertise `mcp` and `embedded`. Ruleset 2026-08-22.2 now accepts supported transports and permits embedded service declaration without a separate endpoint.
2. **Unprobed order lifecycle was incorrectly collapsed to missing events.** A public profile declaring Order capability does not prove whether created/shipped/delivered webhook behavior has been implemented. `order_events=None` now yields `UCP-09 UNKNOWN`; only an explicit observed/declaration list missing required events yields FAIL.

These corrections remove **8 false-negative findings** across the four UCP-200 merchants: `UCP-05` and `UCP-09` each corrected on four merchants.

## Remaining deterministic profile-level gate
All four observed UCP-200 profiles declare `dev.ucp.shopping.order`, but the captured public profile does not contain `signing_keys` (or legacy `keys`). Under the pinned current UCP Order specification, order webhook payloads MUST be signed, signing uses a key from `signing_keys` in the business UCP profile, and verification locates the matching key in that public profile.

Therefore the scanner retains:
`ORDER_CAPABILITY + NO_PUBLIC_PROFILE_SIGNING_KEYS -> UCP-10 FAIL`.

Boundary: this is a **current public-profile-level finding**, not a claim that the merchant is globally noncompliant or unable to transact. Private/onboarding state and future profile updates are not inferred.

Primary spec references:
- `https://ucp.dev/latest/` — service discovery includes REST, MCP, A2A and embedded.
- `https://ucp.dev/specification/order/` — order webhooks MUST be signed; signing and verification use `signing_keys` in the business UCP profile.

## Laws learned
- `MCP_TRANSPORT != INVALID_UCP`
- `EMBEDDED_WITHOUT_SERVICE_ENDPOINT != INVALID_UCP`
- `UNPROBED_ORDER_EVENTS != MISSING_ORDER_EVENTS`
- `UNKNOWN_FUTURE_TRANSPORT -> UNKNOWN_NOT_FAIL`
- `ORDER_CAPABILITY + NO_PUBLIC_PROFILE_SIGNING_KEYS -> UCP10_FAIL_UNDER_PINNED_SPEC`
- `PUBLIC_UCP_PROFILE != PLATFORM_APPROVAL`
- `PUBLIC_PRODUCT_PAGE != OPENAI_PRODUCT_FEED`
- `BLIND_TEST_PASS != BUYER_DEMAND`
- `PUBLIC_PROFILE_DEFECT != GLOBAL_MERCHANT_NONCOMPLIANCE`

## Causal effect
P-EW02 demonstrates that the scanner can produce specific evidence-bound rule findings on a heterogeneous frozen real-world sample and, importantly, that real fixtures can falsify scanner assumptions and improve the ruleset.

This supports moving OW-01 from synthetic-only scanner engineering into a stronger **real-fixture engineering evidence** state. It still does not create market proof.

Next according to current General Business authority: do not mechanically deepen OW-01 sales/economics. Continue bounded WIP with `P-EW03` Article 50 technical transparency sample pack unless a newer CURRENT authority changes the frontier.

READBACK_MARKER: `AGENT-COMMERCE-P-EW02-BLIND10-PASS-4UCP200-8FALSEFAILS-CORRECTED-NO-DEMAND-PROOF`
