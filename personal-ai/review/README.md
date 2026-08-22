# PL-10 Multi-Model Review

PL-10 proves reviewer **orchestration isolation**, not model quality.

## Lifecycle

1. `start` freezes the exact review input and critic definitions.
2. Each `critic` invocation receives only its own instruction plus the same frozen review input/hash.
3. Critic results persist separately under `critics/<critic_id>.json` and are immutable/idempotent.
4. `aggregate` is blocked while any critic lacks a terminal `COMPLETE`, `HOLD`, or `FAILED` result.
5. Aggregation verifies critic/frozen-input hashes before reading results.
6. Aggregate output preserves each critic result and disagreement; it never claims truth or consensus.

## Offline/live boundary

A network-backed provider is `HOLD / NETWORK_NOT_AUTHORIZED` unless the invocation explicitly supplies `--allow-network`. Offline/mock success proves only orchestration. It does not prove external provider availability or review quality.

## Agreement semantics

- `EXACT_MATCH` — at least two completed critics returned byte-identical normalized response text.
- `DISAGREEMENT` — at least two completed critics returned different response hashes.
- `INSUFFICIENT_COMPLETED_CRITICS` — fewer than two critics completed.

`EXACT_MATCH != TRUTH`. The aggregate always emits `consensus_claimed=false` and `truth_claimed=false`.

## CLI

```bash
python personal-ai/review_cli.py --home /path/to/home start PROJECT request.json
python personal-ai/review_cli.py --home /path/to/home critic PROJECT REVIEW_ID CRITIC_ID
python personal-ai/review_cli.py --home /path/to/home aggregate PROJECT REVIEW_ID
python personal-ai/review_cli.py --home /path/to/home status PROJECT REVIEW_ID
python personal-ai/review_cli.py --home /path/to/home run PROJECT request.json
```

Request example:

```json
{
  "content": "Frozen artifact or decision to review",
  "critics": [
    {
      "id": "logic",
      "provider": "mock",
      "model": "mock-logic",
      "instruction": "Find logical contradictions.",
      "required": true
    },
    {
      "id": "evidence",
      "provider": "mock",
      "model": "mock-evidence",
      "instruction": "Audit evidence and unsupported claims.",
      "required": true
    }
  ]
}
```
