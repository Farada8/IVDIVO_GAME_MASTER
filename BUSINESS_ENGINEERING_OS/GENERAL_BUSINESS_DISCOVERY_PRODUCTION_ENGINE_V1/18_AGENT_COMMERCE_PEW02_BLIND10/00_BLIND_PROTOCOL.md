# P-EW02 — AGENT COMMERCE READINESS SCANNER BLIND 10-MERCHANT TEST

**Date:** 2026-08-22  
**Parent:** OW-01 Agentic Commerce Merchant Readiness  
**Dependency:** P-EW01 scanner merged via PR #348.  
**Mode:** public-web only; no merchant accounts, private feeds, checkout mutation, orders, outreach, spend or merchant declarations.

## Blindness rule
The 10 merchant domains below are frozen **before** probing `/.well-known/ucp` or constructing scanner snapshots. Do not replace a merchant because its result is inconvenient, blocked, missing or ambiguous.

## Frozen sample
1. `decathlon.ie`
2. `brownthomas.com`
3. `arnotts.ie`
4. `elverys.ie`
5. `ikea.com`
6. `lego.com`
7. `patagonia.com`
8. `allbirds.com`
9. `glossier.com`
10. `gymshark.com`

Selection rationale: mixed Ireland/EU/global ecommerce merchants, multiple scales and likely platform stacks, all with public product-commerce surfaces. No UCP result was inspected before freezing this list in the project artifact.

## Evidence acquisition contract
For each merchant:
- probe public `https://<domain>/.well-known/ucp`;
- record resolved status/content evidence where accessible;
- do not infer a private OpenAI product feed from product pages; `openai_feed.evidence_state=UNKNOWN` unless an admissible public/merchant-declared feed is actually found;
- do not probe transaction-changing checkout methods;
- do not create carts/orders/accounts;
- only populate UCP endpoint/identity/order fields when public profile/probe evidence actually supports them.

## Scanner contract
Use the merged P-EW01 ruleset, preserving `PASS / FAIL / UNKNOWN / NOT_APPLICABLE` and overall disposition without magic score.

## Predeclared P-EW02 decision criteria
P-EW02 is useful only if the scanner produces **merchant-specific, reproducible rule findings** rather than generic advice.

- `PASS_TEST`: all 10 frozen merchants evaluated; >=8 produce a deterministic merchant-specific rule result or an evidence-bound UNKNOWN; zero merchant is falsely promoted to platform approval/readiness from missing private evidence; generic advice output count = 0.
- `AMBIGUOUS_TEST`: 10 evaluated but >2 are inaccessible/unresolvable at the public probe layer or the scanner cannot distinguish deterministic defect from missing evidence.
- `FAIL_TEST`: sample substitution occurs, generic advice is emitted as the main output, UNKNOWN is collapsed into FAIL/PASS, or any merchant is promoted to approval/transaction readiness without admissible evidence.

This gate tests scanner discrimination and evidence discipline only. It does not prove buyer demand, WTP, merchant adoption, platform approval, transaction volume or profitability.

READBACK_MARKER: `AGENT-COMMERCE-P-EW02-BLIND10-PROTOCOL-FROZEN-20260822`
