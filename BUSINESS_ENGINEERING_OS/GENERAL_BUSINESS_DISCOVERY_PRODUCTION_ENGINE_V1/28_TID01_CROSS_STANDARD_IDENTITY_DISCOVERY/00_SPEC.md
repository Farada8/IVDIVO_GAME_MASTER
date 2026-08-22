# T-ID01 — CROSS-STANDARD AGENT IDENTITY / DISCOVERY COMPATIBILITY CORPUS

**Date:** 2026-08-22  
**Status:** INTERNAL READ-ONLY ENGINEERING TEST  
**Parent:** `26_EARLY_WAVE_RED_TEAM_TOP3_2026-08-22.md`  
**Candidate:** `CROSS_STANDARD_AGENT_IDENTITY_DISCOVERY_INTEROP_AND_DRIFT`

## Question
Can one provider-neutral manifest normalize current public DNS-AID, ANS, A2A and MCP discovery metadata **without silently changing meaning**?

This is not a product build and not a demand test.

## Public evidence basis
The fixture corpus is deliberately minimal and documentation-derived. It does not copy private systems or claim to be a complete implementation of any protocol.

Current public sources used:
1. DNS-AID reference implementation / getting started:
   - `https://github.com/dns-aid/dns-aid-core`
   - DNS SVCB/TXT discovery, optional capability URI/digest, protocol declarations, DNS index, native agent metadata and A2A/MCP bridging.
2. Agent Name Service (ANS):
   - `https://github.com/agentnameservice/ans`
   - `https://github.com/agentnameservice/ans-registry`
   - versioned `ans://` identity, FQDN proof-of-control, certificates, transparency-log / SCITT evidence.
3. A2A 0.3 specification:
   - `https://a2a-protocol.org/v0.3.0/specification/`
   - Agent Card with `protocolVersion`, provider-defined agent `version`, endpoints/transports, skills, security schemes and optional JWS signatures.
4. A2A 0.2.6 historical specification:
   - `https://a2a-protocol.org/v0.2.6/specification/`
   - used only as a version-drift fixture for the well-known path.
5. Official MCP Registry / MCP specification:
   - `https://github.com/modelcontextprotocol/registry`
   - `https://modelcontextprotocol.io/`
   - static `server.json` discovery/install metadata; remote endpoints and installable packages are distinct; live tools are protocol runtime data.

## Predeclared success condition
T-ID01 remains interesting only if the frozen public corpus exposes at least **one semantic incompatibility or drift case** that a naive common schema would misrepresent.

Success is engineering discrimination only:
`REAL_PUBLIC_SEMANTIC_GAP_FOUND = TRUE`

It does **not** imply buyer demand, WTP or market opportunity.

## Predeclared kill condition
If the four families can be safely flattened to a small common shape without information loss relevant to discovery, identity, transport, capabilities or trust, then:
`CROSS_STANDARD_INTEROP_WEDGE = DEPRIORITIZE`

## Normalization contract
A loss-aware manifest must keep these dimensions separate:
- `source_family`
- `source_version`
- `canonical_id`
- `identity_anchor_kind`
- `agent_version`
- `protocol_version`
- `discovery_locations[]`
- typed `endpoints[]` with `role` and `transport`
- `capability_evidence.source_type`
- `capability_evidence.freshness`
- `capability_evidence.live_introspection_required`
- separate trust evidence dimensions:
  - domain control
  - card/content signature
  - transparency receipt
  - certificate binding
  - integrity digest / package hash

Forbidden flattening:
`ONE_VERSION_FIELD`
`ONE_ENDPOINT_FIELD`
`ONE_VERIFIED_BOOLEAN`
`ONE_CAPABILITIES_ARRAY_WITHOUT_PROVENANCE_OR_FRESHNESS`

## Frozen incompatibility classes tested
- F001 `WELL_KNOWN_PATH_DRIFT`
- F002 `VERSION_SEMANTICS_COLLISION`
- F003 `TRUST_ASSURANCE_NON_EQUIVALENCE`
- F004 `CAPABILITY_FRESHNESS_MISMATCH`
- F005 `ENDPOINT_ROLE_COLLISION`
- F006 `GLOBAL_IDENTITY_SCOPE_MISMATCH`

## Evidence boundary
`PUBLIC_FIXTURES_ONLY = TRUE`
`PRODUCTION_SYSTEM_ACCESS = FALSE`
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`WIP_PROMOTED = FALSE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`
