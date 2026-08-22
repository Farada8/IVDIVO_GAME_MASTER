# PL-03 Source / Evidence Layer

PL-03 adds provenance-aware claims on top of the existing PL-02 `MemoryStore`.

## Claim types

- `FACT`
- `SOURCE_CLAIM`
- `USER_DECISION`
- `AI_INFERENCE`
- `HYPOTHESIS`
- `TEST_RESULT`

Every claim persists claim text/type, project ID, source IDs, confidence, verification state and immutable PL-02 version history.

## Provenance route

`trace_claim(claim_id)` returns the claim plus all registered SOURCE records, their DOCUMENT parents and the project ID where available.

The evidence layer does not infer missing provenance. A claim source must be an existing `SOURCE` record in the same project, and each source must trace to an existing `DOCUMENT` record.

## Verification law

A new claim always starts `UNVERIFIED`.

An explicit `verify_claim()` call creates a separate immutable `EVENT` record with verifier + verification evidence, then updates the claim to reference that event.

`emit_verified_fact()` is fail-closed. It creates a new PL-02 `FACT` record only when:

1. the claim state is `VERIFIED`;
2. `verification_event_id` exists;
3. that EVENT points back to the same claim and records result `VERIFIED`.

The original claim is never silently rewritten from `AI_INFERENCE`/`HYPOTHESIS` into `FACT`. The emitted fact links back to both the claim and the explicit verification event.

Therefore:

`UNVERIFIED_AI_INFERENCE != VERIFIED_FACT`

and

`VERIFIED_FACT = CLAIM + EXPLICIT_VERIFICATION_EVENT + TRACEABLE_PROVENANCE`.

## Executable acceptance

```bash
python -m unittest personal-ai/tests/test_source_evidence_layer.py -v
```

The negative acceptance test proves an unverified AI inference cannot be emitted/stored as a verified FACT. Additional tests cover all registered claim types, source/document/project tracing, verification-event persistence, version history, duplicate fact emission protection and cross-project provenance rejection.
