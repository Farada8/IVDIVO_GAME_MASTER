# PL-06 Business Core

PL-06 implements the first deterministic business workflow:

`CLIENT REQUEST -> JOB DESCRIPTION -> COST ESTIMATE -> LABOUR -> MATERIAL -> MARGIN -> QUOTE -> SAVE`

## Minimum entities

The module exposes serializable `Lead`, `Customer`, `Job`, `Quote`, `Invoice`, `Supplier`, `Expense`, `Payment`, and `FollowUp` entities. The first workflow persists the `Job` and `Quote`; later workflows may use the other entities without changing their public names.

## No-invented-price law

The quote engine does not research, estimate, infer, or silently default missing commercial values.

- missing `hours` or `labour_rate` -> labour `TBD`;
- missing material quantity or unit price -> material total `TBD`;
- missing materials without `materials_not_required=true` -> materials `TBD`;
- `materials_not_required=true` is the explicit path to a known material cost of zero;
- missing `margin_percent` -> margin and final total `TBD`;
- area/quantity is descriptive only and never becomes a price without explicit cost inputs;
- zero is allowed when explicitly supplied, but absence is never converted to zero.

All money arithmetic uses `Decimal` and final money values are rounded to two decimals only at the document boundary.

Optional `price_source` labels on material lines are preserved as provenance but are not treated as independently verified market evidence. Stronger source verification belongs to PL-03/PL-07.

## Persistence

Every successful request saves:

- structured JSON under `projects/<project>/artifacts/business/quotes/<quote_id>.json`;
- readable Markdown alongside it;
- `Job` and `Quote` entity JSON under `runtime/business/entities/`;
- a PL-02 `OUTPUT` memory record pointing to the quote artifacts.

A quote may persist with `status=TBD`; this is a valid fail-closed result, not a failed run.

## CLI

Create a project, prepare a request JSON, then run:

```bash
python personal-ai/run.py --home /tmp/pai project create demo
python personal-ai/run.py --home /tmp/pai business quote demo request.json
```

The request JSON uses explicit inputs such as `client_request`, `job_type`, `hours`, `labour_rate`, `materials`, `materials_not_required`, `margin_percent`, and `currency`.
