# P-EW02 — RULESET FALSE-POSITIVE PATCH

**Date:** 2026-08-22  
**Status:** P-EW02 CALIBRATION DELTA / RULESET PATCH BEFORE REAL-MERCHANT SCORING  
**From:** `2026-08-22.1`  
**To:** `2026-08-22.2`

## Reproducible divergence found
The first P-EW02 specification replay found that Scanner v0 was not actually vendor-neutral across UCP transports.

Old behavior:
- selected only the first `dev.ucp.shopping` service binding;
- treated non-REST transport as an invalid binding;
- universally required `schema + endpoint`;
- ran REST create/update/complete endpoint checks whenever checkout capability existed;
- could treat missing public order-event evidence as a deterministic FAIL.

This creates false positives for valid UCP profiles that use MCP, A2A or Embedded transport and for public-only observations that cannot prove private order/webhook implementation.

## Official evidence
Current UCP documentation explicitly supports multiple service transport bindings:
- REST — OpenAPI;
- MCP — OpenRPC;
- A2A — Agent Card;
- Embedded — OpenRPC.

Transport-specific requirements differ:
- REST/MCP business bindings require schema + endpoint;
- A2A requires its agent-card endpoint and does not require the REST/OpenRPC schema field;
- Embedded requires schema but may have no endpoint.

Current UCP profile structure also requires `ucp.services` and `ucp.payment_handlers` registries to be present even when empty. Capabilities may be optional at protocol-profile level.

The public spec uses root `keys[]` for JWK discovery. Current Google merchant implementation examples use root `signing_keys[]`. Scanner v0.2 accepts both as documented ecosystem variants rather than forcing one alias.

## Patch contracts
`MULTI_TRANSPORT_UCP != REST_ONLY`

`TRANSPORT_BINDING_REQUIREMENTS_ARE_TRANSPORT_SPECIFIC`

`NON_REST_CHECKOUT != REST_ENDPOINT_FAILURE`

`PUBLIC_PROFILE != PRIVATE_ORDER_EVENT_PROOF`

`ORDER_CAPABILITY != WEBHOOK_FLOW_PROVEN`

`PAYMENT_HANDLERS_REGISTRY_REQUIRED_EVEN_IF_EMPTY`

`GOOGLE_SIGNING_KEYS_ALIAS != GENERIC_UCP_KEYS_ALIAS_ERROR`

## v0.2 changes
- inspect all shopping service bindings, not first only;
- accept `rest`, `mcp`, `a2a`, `embedded`;
- apply binding-specific required fields;
- add `UCP-05P` for mandatory payment-handlers registry presence/type;
- run UCP-07 REST endpoint probes only when REST transport is actually advertised;
- preserve unobserved order events as UNKNOWN;
- require signing keys/signing only when webhook flow is explicitly declared;
- preserve `keys` and `signing_keys` aliases;
- ruleset bumped to `2026-08-22.2`;
- regression suite expanded from 8 to 14 canaries.

## Proof effect
This is a **scanner quality repair**, not positive merchant evidence and not a proof upgrade.

`FALSE_POSITIVE_CLASS_FOUND_AND_FIXED != MARKET_VALIDATION`

P-EW02 remains NOT_EXECUTED until the corrected ruleset is used on the predeclared ten real public merchant fixtures.

READBACK_MARKER: `AGENT-COMMERCE-SCANNER-RULESET-20260822-2-PEW02-FALSE-POSITIVE-PATCH`
