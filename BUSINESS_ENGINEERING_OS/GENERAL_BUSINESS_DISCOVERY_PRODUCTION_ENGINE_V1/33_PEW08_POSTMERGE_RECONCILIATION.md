# P-EW08 — POST-MERGE RECONCILIATION

**Date:** 2026-08-22  
**Status:** TECHNICAL GAP CONFIRMED / COMMERCIAL WEDGE KILLED / NO WIP PROMOTION

## Controlling authority
- PR #453
- merge: `ba491bb9c11811e4ca7173777c786f6645c3ed19`
- tested head: `acb7529770d299ab270bcbb47f2afdcc7f3e272f`
- dedicated CI: `32573258186` SUCCESS
- artifact: `pew08-doclang-real-roundtrip-evidence`
- artifact id: `9475901171`
- artifact SHA256: `a3f9d1110aea50043e4fd416df8e7aeeb38858487afdb64dbfaf62e1b7536c77`
- review threads: 0
- all five inherited General Business regressions on the final head: SUCCESS

## Real current reproduction
Runtime pins:
- `docling==2.121.0`
- `doclang==0.7.3`
- Python 3.12

The current Docling runtime generated DocLang from a real bounded source fixture. The default `DoclingDocument.export_to_doclang()` output failed the current official DocLang XSD. The same current serializer, with only `DocLangParams(include_namespace=True)`, passed the same official XSD.

Observed route:
`PASS_REAL_DEFAULT_NAMESPACE_COMPATIBILITY_GAP_TECHNICAL_ONLY`

Observed gap plane:
`DEFAULT_PRODUCER_NAMESPACE_VS_OFFICIAL_XSD`

Minimal control fix:
`DocLangParams(include_namespace=True)`

## Root cause
Current `DoclingDocument.export_to_doclang()` constructs the serializer using default `DocLangParams()`.
Current `DocLangParams.include_namespace` defaults to `False`.
The current DocLang 0.7.3 XSD declares target namespace `https://www.doclang.ai/ns/v0` and `elementFormDefault="qualified"`.

Therefore the default producer path and the official structural validator are incompatible unless namespace emission is enabled explicitly.

## Economic Red Team
This is a **real current technical defect**, but it is not a durable commercial wedge by itself.

Reasons:
1. the defect is narrow;
2. the workaround is one explicit serializer parameter;
3. current public issue searches did not reveal an already-filed exact namespace issue, but absence of an issue is not buyer demand;
4. an upstream default change could erase this entire defect immediately;
5. generic converter/XSD tooling is already platform-native or open-source.

Killed as primary wedges:
- `GENERIC_DOCLANG_CONVERSION_SERVICE`
- `GENERIC_DOCLANG_XSD_VALIDATION_SERVICE`
- `DOCLANG_NAMESPACE_FIX_CONSULTING`

Only broader hypothesis that may remain on radar:
`INDEPENDENT_MULTI_CONVERTER_MULTI_VERSION_FIDELITY_AND_CONFORMANCE_REGRESSION_QA`

That hypothesis is **not WIP** and cannot advance without evidence that multiple independent current defects recur across real pipelines and escape native tests.

## Self-improvement laws
`ONE_FLAG_UPSTREAM_FIXABLE_BUG != DURABLE_COMMERCIAL_WEDGE`
`REAL_TECHNICAL_GAP != BUYER_DEMAND`
`CURRENT_REPRODUCTION != PREVALENCE`
`UPSTREAM_FIX_CAN_ERASE_SERVICE_WEDGE`
`GREEN_CI != MARKET_WINNER`

## Cross-store closure
Drive document:
`1Z0qRLPN07bxZiPBtNtA-hIxWU9QT27D2smu9iqup_ks`

Semantic readback marker:
`P-EW08-DEFAULT-NAMESPACE-GAP-PR453-BA491BB9-CI32573258186-NO-WIP-NO-WTP-20260822`

## Proof boundary
`BUYER_DEMAND = UNPROVEN`
`WTP = UNKNOWN`
`PRICE = NULL`
`TRANSACTIONS = 0`
`PROFITABILITY = UNPROVEN`
`WIP_PROMOTION = FALSE`
`MARKET_WINNER = NONE`
`EXTERNAL_ACTION_AUTHORIZED = FALSE`

## Next causal frontier
Do not add DocLang features merely because the bug is reproducible.
Return to `EARLY_WAVE_RADAR_DELTA03` and search for broader, recurring, remote-first infrastructure/evidence bottlenecks.
