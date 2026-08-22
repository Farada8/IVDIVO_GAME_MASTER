# PL-07 Business Research

PL-07 creates a deterministic provenance-first research packet for one business decision. It deliberately does **not** embed web scraping, paid-provider calls, or hidden market data. External/source acquisition is separate; this layer organizes supplied evidence and calculations reproducibly.

## Input contract

Required:
- `question`
- `geography`
- `industry`
- `as_of` (`YYYY-MM-DD`)

Optional structured sections:
- `sources`
- `claims`
- `calculations`
- `comparison`
- `conclusions`
- `open_questions`
- `freshness_max_days`

## Output contract

Each run persists under `projects/<project>/artifacts/research/<research_id>/`:
- `sources.json`
- `claims.json`
- `comparison.csv`
- `conclusions.md`
- `open_questions.md`
- `manifest.json`

The input hash determines `research_id`, so an identical request reopens the same packet instead of silently duplicating it.

## Evidence semantics

Research statuses are exactly:
- `OBSERVED`
- `CALCULATED`
- `INFERRED`
- `UNKNOWN`

PL-07 reuses PL-03:
- source material becomes DOCUMENT + SOURCE records;
- OBSERVED claims become SOURCE_CLAIM records;
- INFERRED claims remain AI_INFERENCE;
- calculated claims use TEST_RESULT;
- UNKNOWN remains HYPOTHESIS/UNKNOWN and is not coerced to false.

`OBSERVED != VERIFIED_FACT`.

A source existing in the packet proves only that the supplied source was recorded. It does not independently prove source correctness.

## Calculations

Supported bounded operations:
- SUM
- SUBTRACT
- MULTIPLY
- DIVIDE

No `eval` or arbitrary expression execution is used. A missing operand yields `result: null` and `status: UNKNOWN`; it never becomes zero. Division by zero fails closed.

## Freshness

Each source may carry `source_as_of` and `retrieved_at`. Relative to research `as_of`:
- missing source date -> `UNKNOWN`;
- future-dated source -> `FUTURE`;
- with `freshness_max_days`: within threshold -> `FRESH`, beyond -> `STALE`;
- without a threshold, a dated source is `DATED` and still carries `age_days`.

## Conclusions

Every conclusion must reference a known claim and/or calculation. The service resolves its source/calculation IDs before writing `conclusions.md`. A conclusion with no traceable evidence/calculation is rejected.

## Null safety

Missing comparison cells are written as blank CSV cells. They are never converted to `0`, `false`, or a fabricated market value.

## Executable acceptance

```bash
python -m unittest personal-ai/tests/test_business_research.py -v
```

The PL-07 CI also runs the complete Personal AI regression suite.
