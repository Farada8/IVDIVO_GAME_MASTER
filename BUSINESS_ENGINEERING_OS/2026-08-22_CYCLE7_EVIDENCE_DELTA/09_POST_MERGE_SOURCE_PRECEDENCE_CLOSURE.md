# POST-MERGE CLOSURE — AUTHORITY SOURCE PRECEDENCE

**Date:** 2026-08-22
**Case:** `PROC-BALLYBUNION-8872468`

## Merge
- superseded non-mergeable PR: #233 — closed without merge after parallel main advancement;
- fresh-main replay PR: #236;
- final reviewed head: `8322f37a81203a043eaa7cf7cafc666a9edf9e22`;
- exact-head GitHub Actions run: `32550331583` — SUCCESS;
- merge SHA: `3a738950b02834addc67d8576a100c20f6d3133b`.

## Persisted semantic delta
- `SourcePrecedenceResolver` ranks current official first-party authority above secondary aggregators;
- lower-ranked conflicts are retained as provenance but cannot override/promote authority;
- equal-ranked top-authority conflicts fail closed;
- `DocumentRouteState` prevents a published documents URL from being treated as recovered attachment inventory;
- connected-source non-findings remain `NOT_FOUND_IN_CONNECTED_SOURCES`, never `DOCUMENT_DOES_NOT_EXIST`.

Evidence regression is **11/11 PASS** on the exact merged head.

## Current decision boundary
The official documents route for eTenders resource `8872468` is known, but the complete current attachment/revision/addendum inventory and bytes are not recovered. Supplier company number/current CRO status/corporate tax clearance and the verified capability packet remain unproven.

Therefore:
- `HOLD_MISSING_AUTHORITY`;
- `REQUIREMENT_JOIN = BLOCKED`;
- `BID/HOLD/NO-BID = NOT AUTHORIZED`;
- `PA4/PA5/E3/E4 = false/unproven`.

## Concurrency proof
This cycle also produced a concrete process proof: when PR #233 became non-mergeable after substantial parallel advancement of `main`, no force merge was used. The three-file semantic delta was replayed onto fresh `main`, verified `ahead 3 / behind 0`, re-tested, and merged as #236.

Scoped self-improvement candidate:
`CONCURRENT_MAIN_ADVANCE -> FRESH_READ -> SEMANTIC_DELTA_REPLAY -> EXACT_HEAD_CI -> MERGE`, not blind force-merge.

## Next causal unlock
1. recover current official attachment inventory + bytes;
2. recover current authoritative CRO/company-number evidence;
3. recover company-bound Revenue/tax-clearance evidence;
4. acquire only supplier capability evidence required by the current tender;
5. then run the atomic requirement join.
