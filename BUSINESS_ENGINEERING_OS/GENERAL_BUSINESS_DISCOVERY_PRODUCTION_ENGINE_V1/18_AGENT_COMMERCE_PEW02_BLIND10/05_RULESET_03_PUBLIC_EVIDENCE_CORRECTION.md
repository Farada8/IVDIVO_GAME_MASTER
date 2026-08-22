# P-EW02 POST-HOC PUBLIC-EVIDENCE CORRECTION — RULESET 2026-08-22.3

**Date:** 2026-08-22  
**Type:** authority correction / no new market experiment  
**Controlling runtime correction:** merged PR #387  
**Frozen sample:** same 10 merchants as P-EW02; no substitution.

## Why this receipt exists
The original blind-10 receipt is an immutable record of the ruleset-0.2 interpretation at that time. Later audit of the same public evidence found a second false-positive class: public Order capability was being treated as proof that webhook execution applied, causing absent public `signing_keys` to be labelled deterministic FAIL even when webhook-flow use was unproven.

Merged PR #387 corrected the runtime. This receipt prevents future restore from treating the historical ruleset-0.2 interpretation as current authority.

## Current rule
`PUBLIC_ORDER_CAPABILITY != PROVEN_WEBHOOK_FLOW`

- webhook flow unproven + signing keys absent -> `UNKNOWN`, not FAIL;
- webhook flow explicitly observed/declared + signing keys absent -> `FAIL`;
- webhook path explicitly not used for tested path -> `NOT_APPLICABLE`;
- signing execution remains unresolved until webhook applicability is established.

Additional corrections:
- REST checkout probes run only for advertised REST bindings;
- Identity Linking OAuth gate applies only when Identity Linking capability is advertised;
- `payment_handlers` has its own structural/evidence rule;
- unknown/missing hidden implementation remains UNKNOWN, never inferred.

## Historical evidence preserved
The original P-EW02 facts remain valid historical observations:
- frozen sample size 10;
- no merchant substitution;
- four public UCP 200 profiles in the original captured run;
- original body hashes/artifact digest remain provenance;
- no buyer demand/WTP/transaction/profitability proof was created.

Only the **interpretation layer** changed.

## Causal effect
This correction does not alter the P-EW05 monetization route. OW-01 remains an M1 fixed-scope diagnostic candidate because real-public-fixture discrimination exists, while WTP and paid demand remain unknown.

`RULE_CORRECTION != NEW_MARKET_EVIDENCE`

`HISTORICAL_RECEIPT != CURRENT_RULESET_AUTHORITY`

`P-EW05_M1_ROUTE_UNCHANGED`

READBACK_MARKER: `AGENT-COMMERCE-RULESET03-CORRECTION-HISTORICAL-PEW02-PRESERVED-NO-MARKET-PROMOTION`
