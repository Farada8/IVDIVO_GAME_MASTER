# WAVE 4 — AUTHORITATIVE RUNTIME RECONCILIATION + TEST RESULT

## Purpose
Reconcile Wave3 candidate mechanisms against current `main` without creating a second Audio Novel Engine.

## Freshness result
The original stacked Wave4 branch created from `32x-wave3-finalize` was compared with current `main` and found **193 commits behind**. It is provenance-only. Current writes use fresh main-based branch `audio-novel-engine/32x-wave4-main-rebase-2026-08-21`.

## Existing authority reused
Current `main` already contains the live-provider canary/casting cascade, shared musical-fact contract, and project-specific ROOM917/LESSON_ZERO/BODYGUARD audio state. Wave4 therefore adds only candidate executable gaps for review.

## Bounded reconciliation map
- Canary identity: governing principle exists; no matching executable helper located in bounded current-main search → candidate helper + tests.
- Spend/restart idempotency: cost/provenance law exists; no `SpendLedger` helper located → candidate helper + tests.
- Ambiguous response safety: fail-closed principle exists; no reconciler located → candidate helper + tests.
- Error taxonomy: provider law exists; no stable helper located → candidate helper + sanitized tests.
- 48 kHz asset normalization/hash: production law exists; no current helper located → candidate helper + tests.
- TTD/TTS alignment normalization: timing law exists; no main helper located in bounded search → candidate helper + tests.
- Capability drift/no auto-swap: identity law exists; no helper located → candidate helper + tests.
- Scoped voice/pronunciation invalidation: dependency-DAG law exists; no exact LZ helper located → candidate helper + tests.

Absence means **not located in bounded current-main search**, not that no historical implementation exists in archives.

## Deterministic verification
- `test_wave4_runtime_promotion_candidate.py`: **36/36 PASS**.
- `test_wave4_quality_core.py`: **46/46 PASS**.
- Total: **82/82 PASS**.

Coverage includes canary drift, spend idempotency, ambiguous request reconciliation, provider error taxonomy, 48 kHz normalization, TTD/TTS alignment normalization, capability drift, scoped invalidation, live provenance/36-unit gates, synthetic timing firewall, acoustic passports, ambience/protected silence, Foley causality, diegetic media, music causality, musical facts, mono/mobile, ABC evidence boundary, post-FX silence, information priority, stereo collapse, earliest cause and edit-before-regenerate.

## Promotion decision
`GO_FOR_CODE_REVIEW`, **not CURRENT**.

To become current: review against any production implementation not exposed by bounded search; integrate only genuine missing pieces; run current-main CI; merge through reviewed PR; then update current pointers. Branch tests cannot self-promote.
