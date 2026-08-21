# AUDIO NOVEL ENGINE — WAVE3 → CURRENT RUNTIME RECONCILIATION v1

**Date:** 2026-08-21  
**Status:** WAVE4 PROMPT 09 EXECUTED / WORKING PR CANDIDATE  
**Rule:** current GitHub `main` remains authority until this branch is reviewed/merged.

## Current production modules inspected

- `audio/studio/provider_preflight.py` — current read-only ElevenLabs secret/model/voice preflight.
- `audio/studio/elevenlabs_adapter.py` — current TTD/TTS request compilation, live dispatch, audio persistence and normalized alignment evidence.
- `audio/studio/alignment_normalizer.py` — current provider-neutral alignment normalization; unknown schema fails closed.
- `audio/studio/runtime/performance_compiler.py` — current provider-safe performance/context/rhythm packet compiler.
- `audio/studio/runtime/*` current Scene State Graph / Foley / spatial / music / pipeline modules.
- current targeted repair standard: `IVDIVO_NARRATIVE_OS/14_TARGETED_REPAIR_PATCH_CONTRACT_STANDARD_v1.0.md`.

## Reconciliation matrix

| Wave3 candidate mechanism | Fresh current-state finding | Wave4 disposition |
|---|---|---|
| Exact canary identity validation | No generic pre-dispatch identity-fixture gate found in current production path | **PORTED_NOW** to `runtime/production_control.py`; exact Lesson Zero fixture stored as project data, not runtime hardcode |
| Persistent spend/idempotency ledger | Existing adapter persists request evidence but no immutable restart-safe spend ledger was found | **PORTED_NOW** `SpendLedger`; connected by controlled dispatch wrapper |
| Ambiguous response quarantine | Existing adapter classifies provider/connectivity failure but had no persisted ambiguity state / reconciliation contract | **PORTED_NOW_PARTIAL**: quarantine + provider-lookup reconciliation contract; real provider lookup capability still external/unknown |
| Stable provider error taxonomy | Existing provider modules contain local failure labels but no cross-module stable domain taxonomy | **PORTED_NOW** with sanitized fixtures; live payload corpus still open |
| 48 kHz PCM/WAV normalization + hash | Existing adapter hashes decoded audio but canonical 48 kHz ingest gate was not found | **PORTED_NOW** `runtime/audio_asset_ingest.py` |
| TTD/TTS alignment normalizer | Already current at `audio/studio/alignment_normalizer.py` and used by adapter persistence | **ALREADY_CURRENT / DO NOT DUPLICATE** |
| Capability drift / no auto-substitution | `provider_preflight.py` already reads models/voices; no explicit expected-vs-snapshot no-auto-swap gate found | **PORTED_NOW** comparison gate; wrapper can consume preflight snapshot; authenticated snapshot remains external |
| Provider mock | Existing unit-test mocking is sufficient; production runtime does not need a fake provider object | **TEST_ONLY / DO NOT PROMOTE AS RUNTIME FEATURE** |
| Silent reaction contract | Performance compiler carries context/rhythm but no explicit zero-spoken-unit silent-reaction validator found | **PORTED_NOW** as semantic contract |
| Functional pause taxonomy | Performance compiler carries pause fields; no centralized fail-closed semantic taxonomy found | **PORTED_NOW**; timing remains semantic until alignment |
| Reply latency semantic state | Existing reactivity/rhythm fields exist | **STRENGTHENED** with explicit no-absolute-pre-render-time contract |
| Microphone choreography state | Spatial/performance layers already support proximity/orientation | **STRENGTHENED / NO SECOND SPATIAL ENGINE** with small validated state vocabulary |
| AI-tell flags | No current production auto-reject rule should exist | **PORTED AS ADVISORY ONLY**, never authoritative |
| Performance lock | Human/audition authority exists conceptually; no generic code gate found | **PORTED_NOW** fail-closed evidence gate; machine may not auto-lock |
| Candidate CLI clean-build/resume/invalidation | Wave3 CLI was research-layer only | **PORTED AS PRODUCTION-CONTROL CLI** with dispatch disabled for freeze/resume/invalidation |
| Earliest-cause repair router | Universal patch standard exists, but audio specialization was not a small executable router | **PORTED_NOW** as audio-only earliest-cause router subordinate to story authority |

## New/changed production integration files on this branch

- `audio/studio/runtime/production_control.py`
- `audio/studio/runtime/production_control_cli.py`
- `audio/studio/runtime/audio_asset_ingest.py`
- `audio/studio/runtime/audio_repair_router.py`
- `audio/studio/runtime/provider_reconciliation.py`
- `audio/studio/controlled_provider_dispatch.py`
- regression tests under `audio/studio/tests/`
- Wave4 fixtures under this folder.

## Important non-promotions

1. Wave3 branch itself is not made authority merely because 44/44 candidate tests passed there.
2. Existing `alignment_normalizer.py` is reused rather than reimplemented.
3. Existing `provider_preflight.py` and `elevenlabs_adapter.py` remain the provider-specific primitives; the new wrapper adds control around them rather than replacing provider behavior.
4. Provider mock remains test-only.
5. No voice/model candidate is inferred without authenticated account inventory.
6. No human performance, pronunciation, fatigue, chemistry, cost or live portability PASS is inferred from code.
7. No locked story text changes.

## Current integration verdict

**NO PARALLEL ENGINE CREATED.**  
The missing value was cross-cutting production control around existing runtime/provider modules: identity, spend/idempotency, ambiguity, drift, asset ingest, evidence locks and earliest-cause repair. Those mechanisms are now represented on the integration branch, but remain **WORKING / CI_PENDING / REVIEW_PENDING** until tests/checks and rebase against freshest `main` are read back.
