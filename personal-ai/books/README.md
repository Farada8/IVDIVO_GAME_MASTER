# PL-08 Book Production Core

Persisted manuscript state machine. It does not claim that a manuscript is good merely because a model generated it.

## State machine

`DRAFT -> CONTINUITY_REVIEW -> READY_FOR_FINAL -> FINAL`

A manuscript cannot enter `FINAL` until a continuity result is explicitly recorded as `PASS` for the exact SHA-256 of the current manuscript.

## Integrity rule

The continuity gate stores the manuscript SHA-256 that was reviewed. Any manuscript update:
- returns the book to `DRAFT`;
- invalidates the prior PASS/FAIL result to `NOT_RUN`;
- requires a fresh continuity review before finalization.

Direct file edits are also detected: submit/result/finalize recompute hashes and fail closed on mismatch.

## Continuity input boundary

PL-08 accepts a continuity result plus a non-empty source label. It does not itself prove the reviewer is correct. PL-09 Continuity Checker will later produce stronger evidence-pair/severity results.

A FAIL requires at least one structured finding. A PASS may have zero findings.

## Persistence

Each book is stored under the owning project's `artifacts/books/<book_id>/` directory:
- `state.json` — machine state and continuity receipt;
- `manuscript.md` — current mutable manuscript;
- `final.md` — immutable final copy after gate passage.

Finalization also persists the exact final text as a PL-02 `OUTPUT` memory record with book id, manuscript hash, continuity source/attempt and final artifact path.

## CLI

```bash
python personal-ai/run.py --home /tmp/pai book create demo b01 "Example Book"
python personal-ai/run.py --home /tmp/pai book manuscript demo b01 manuscript.md
python personal-ai/run.py --home /tmp/pai book submit demo b01
python personal-ai/run.py --home /tmp/pai book continuity demo b01 continuity.json
python personal-ai/run.py --home /tmp/pai book finalize demo b01
python personal-ai/run.py --home /tmp/pai book status demo b01
```

`continuity.json` shape:
```json
{"passed": true, "source": "manual continuity review fixture", "findings": []}
```

No LLM/network call is required for the PL-08 acceptance gate. Provider-backed drafting can be layered later without weakening this deterministic finalization invariant.
