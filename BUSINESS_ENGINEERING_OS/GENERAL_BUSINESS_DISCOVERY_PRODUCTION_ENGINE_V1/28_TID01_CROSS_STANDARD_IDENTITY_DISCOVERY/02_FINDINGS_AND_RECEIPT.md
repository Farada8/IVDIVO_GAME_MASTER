# T-ID01 — FINDINGS + ENGINEERING RECEIPT

**Date:** 2026-08-22  
**Status:** `PASS_INTERNAL_ENGINEERING_DISCRIMINATION`  
**Dedicated CI:** `General Business T-ID01 Cross-Standard Interop` run `32571774671` — SUCCESS  
**Corpus:** DNS-AID / ANS / A2A / MCP Registry, documentation-derived and read-only

## Result
The predeclared kill test did **not** kill the hypothesis.

A naive universal manifest would lose or invent material semantics. The canaries detect six distinct incompatibility/drift classes.

### F001 — WELL_KNOWN_PATH_DRIFT
A2A 0.2.6 documents `/.well-known/agent.json`; A2A 0.3.0 documents `/.well-known/agent-card.json`.

This is a resolver/migration compatibility break, not a label difference. A hard-coded discovery client can miss a current agent or probe a stale path.

### F002 — VERSION_SEMANTICS_COLLISION
The word/version concept is not equivalent across the families:
- A2A separates `protocolVersion` from provider-defined agent `version`;
- ANS version participates in the versioned `ans://` identity;
- DNS-AID native metadata has agent version while protocol is separately declared;
- MCP `server.json` has server version and a separate schema URI/version.

A common `version` field is lossy.

### F003 — TRUST_ASSURANCE_NON_EQUIVALENCE
A single `verified=true` is unsafe:
- A2A Agent Card JWS, when present, protects card integrity;
- ANS adds FQDN proof-of-control, certificate binding and transparency evidence;
- DNS-AID may carry DNS/domain-control and capability-digest evidence;
- MCP Registry namespace/package-integrity evidence is a different assurance class.

These must remain typed dimensions. Presence of one does not prove the others.

### F004 — CAPABILITY_FRESHNESS_MISMATCH
A2A skills can be statically advertised in an Agent Card. DNS-AID can resolve capabilities through multiple sources with a precedence chain. MCP Registry `server.json` is static discovery/install metadata, while the live MCP tool set is runtime protocol data.

Therefore a common `capabilities[]` without `source_type`, `freshness` and `live_introspection_required` can present stale/incomplete data as current capability truth.

### F005 — ENDPOINT_ROLE_COLLISION
MCP Registry distinguishes remote servers from installable packages, including local `stdio` packages. A package identifier is not a remote interaction URL.

A universal `endpoint` field would invent connectivity semantics.

### F006 — GLOBAL_IDENTITY_SCOPE_MISMATCH
ANS exposes a versioned canonical ANSName anchored to proven domain identity. The minimal public A2A AgentCard does not provide an equivalent globally verified canonical identifier.

A normalizer that synthesizes a global identity from A2A display name or URL would create data that the source did not prove.

## Test outcome
- frozen fixture families: 4
- predeclared finding classes: 6
- finding classes detected: 6/6
- deterministic canaries: 10/10 PASS
- dedicated CI: SUCCESS
- neighboring General Business regressions on the same head: 5/5 SUCCESS
- production access: none
- external credentials: none
- customer interaction: none

## Business meaning
This is sufficient to keep the narrow optionality thesis alive:

`CROSS_STANDARD_AGENT_IDENTITY_DISCOVERY_INTEROP_AND_DRIFT = ENGINEERING_PROBLEM_DEMONSTRATED`

It is **not** sufficient to say:
- buyers care enough to pay;
- a standalone product is needed;
- this beats Okta/Ping/DNS-AID/ANS/A2A/MCP ecosystem tooling;
- this candidate should replace current WIP.

## Next causal decision
Do not add a large UI, SaaS backend or agent registry.

The next useful internal step is a **real-public-fixture drift sample**, not more schema engineering:
- sample current public agent/discovery artifacts from at least 5 independent publishers/projects;
- run the same loss-aware checks;
- require at least 2 non-synthetic, externally-authored drift/incompatibility findings;
- kill/deprioritize if findings exist only in our synthetic documentation-derived fixtures.

Suggested gate: `T-ID02_REAL_PUBLIC_FIXTURE_DRIFT_5`

## Proof boundary
`ENGINEERING_PROBLEM_DEMONSTRATED = TRUE`
`REAL_EXTERNAL_FIXTURE_FINDINGS = NOT_YET_PROVEN`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`MARKET_WINNER = NONE`
`WIP_PROMOTED = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

READBACK_MARKER: `TID01-PASS-6OF6-GAPS-CI32571774671-NO-WTP-NO-WIP-20260822`
