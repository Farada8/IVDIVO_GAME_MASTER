# P-EW10 — SAFE CONTRACT MATURITY / SUBSTITUTION PREFLIGHT

**Date:** 2026-08-22  
**Status:** WORKING INTERNAL PREFLIGHT / NO WIP PROMOTION / NO EXTERNAL ACTION

## Candidate

`SAFE_AI_INCIDENT_FINDINGS_EXCHANGE_COMPATIBILITY_AND_EVIDENCE_QA`

This is the next independent early-wave candidate after P-EW09 OSERA failed its predeclared two-gap threshold.

## Why this is a preflight, not a product proof

The Shared AI Findings Exchange (SAFE) RFC is a real new forcing signal: the Linux Foundation published the RFC on 2026-08-04 and the draft requires incident evidence preservation, weekly machine-readable updates while material risks remain unresolved, reproducible verification methods, and future machine-readable policies/tests.

But a conformance/compatibility business cannot be tested honestly until there is a canonical-enough machine-readable exchange contract.

`FORCING_EVENT != STABLE_CONTRACT != BUYER_WEDGE`

## Live maturity controls

The CI preflight reads the current public `OpenSecureAIAlliance/RFCs` repository and checks:

1. the SAFE RFC exists;
2. the RFC still contains machine-readable requirements;
3. the repository contains a normative-looking schema/serialization artifact (`*.schema.json`, JSON/YAML schema, protobuf/IDL, etc.), or the RFC explicitly adopts a canonical representation;
4. open issue #5 status and whether it still records that the evidence requirements name no format;
5. whether a conformance proof can be defined without inventing fields that SAFE itself has not adopted.

## Classification

- If a canonical representation/schema is adopted -> `PROOF_ELIGIBLE_M1_ONLY`; define the smallest independent compatibility/completeness test next.
- If not -> `WATCH_SCHEMA_NOT_STABLE_ENOUGH_FOR_CONFORMANCE_PROOF`; do **not** manufacture a validator against a self-invented schema.

## Substitution boundary

Even if SAFE later becomes proof-eligible, generic telemetry capture / agent observability is **not** the preferred wedge. Existing adjacent infrastructure already includes:

- OpenTelemetry GenAI semantic conventions for agent/model/tool traces;
- OCSF AI/agentic security event work and validation tooling;
- SIEM/observability/governance products already selling agent traces, audit records and runtime evidence.

Therefore a future surviving wedge must be specific to a SAFE-adopted exchange/assurance contract: cross-format normalization, completeness, compatibility, evidence-pack determinism, or regression testing that incumbents do not automatically absorb.

## Commercial boundary

`BUYER_DEMAND = UNPROVEN`  
`WTP = UNKNOWN`  
`PRICE = NULL`  
`TRANSACTIONS = 0`  
`PROFITABILITY = UNPROVEN`  
`WIP_PROMOTION = FALSE`  
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

No SAFE certification, legal compliance, security guarantee, or incident-handling service is claimed.