# PL-06 Business Core

Deterministic estimate/quote layer with a strict evidence firewall. It does not research or invent market prices.

## Price rule

A line is price-ready only when both exist:
- explicit `unit_price`;
- explicit provenance via `price_source` or a resolvable ACTIVE PL-02 `price_source_id`.

If any line is incomplete, the persisted document has `status = NEEDS_PRICE_EVIDENCE`, `subtotal_ex_tax = null`, and no final tax-inclusive total. Supplied lines may contribute to `priced_subtotal`, which is explicitly partial.

## Tax rule

No VAT/tax rate is assumed. With no `tax_rate`, a fully sourced document is `READY` ex tax. If a tax rate or tax evidence is supplied without its counterpart, status becomes `NEEDS_TAX_EVIDENCE`. A supplied tax rate must be between 0 and 1 and have provenance.

## Persistence

Every request, including blocked/incomplete ones, produces:
- a JSON artifact under the project's `artifacts/business/` directory;
- a PL-02 `OUTPUT` memory record with document id/type/status/currency/artifact path metadata.

This preserves the failed-evidence state instead of silently dropping it.

## CLI

```bash
python personal-ai/run.py --home /tmp/pai business quote demo request.json --enforce-ready
python personal-ai/run.py --home /tmp/pai business estimate demo request.json
```

`--enforce-ready` returns exit code 2 when the result is not `READY`.

PL-06 does not claim that a user-provided price source is independently verified market evidence. It only guarantees that the system did not manufacture the price and that provenance supplied to it is retained. PL-03/PL-07 will add stronger external evidence semantics later.
