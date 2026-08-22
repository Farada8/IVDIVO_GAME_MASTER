# PL-11 Test Benchmark Runner

Executable baseline/candidate comparison layer used to reject regressions before a later change-control layer can promote a patch.

## Suite input

A JSON suite contains a name, optional `min_weighted_delta`, and one or more cases. Each case declares:
- `id` — unique case id;
- `baseline` and `candidate` — finite numeric measurements;
- `direction` — `higher_is_better` or `lower_is_better`;
- `weight` — positive aggregation weight;
- `critical` — whether a regression is release-blocking;
- `max_regression` — tolerated adverse oriented delta for this case.

For higher-is-better metrics, oriented delta is `candidate - baseline`. For lower-is-better metrics it is `baseline - candidate`.

## Decision rule

1. Any critical case whose oriented delta is worse than `-max_regression` causes `FAIL / REJECT_CRITICAL_REGRESSION` regardless of aggregate gains.
2. Otherwise, if weighted oriented delta is below suite `min_weighted_delta`, result is `FAIL / REJECT_AGGREGATE_DELTA`.
3. Otherwise result is `PASS / ACCEPT`.

Non-critical regressions remain explicitly listed even when aggregate result passes.

Every run persists a JSON report under `<PERSONAL_AI_HOME>/runtime/benchmarks/`.

## Offline demo

```bash
python personal-ai/run.py benchmark run personal-ai/benchmarks/fixtures/demo_suite.json
```

PL-11 evaluates measurements; it does not invent benchmark scores, execute arbitrary shell commands, modify code, or promote a change. PL-12 Change Control will consume benchmark decisions later.
