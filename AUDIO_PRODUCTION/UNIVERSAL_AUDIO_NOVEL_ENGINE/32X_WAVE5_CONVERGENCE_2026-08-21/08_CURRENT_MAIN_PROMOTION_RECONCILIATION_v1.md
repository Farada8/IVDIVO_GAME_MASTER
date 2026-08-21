# CURRENT MAIN PROMOTION RECONCILIATION v2

Date: 2026-08-21
Branch: `audio-novel-engine/wave5-convergence-32x64-2026-08-21`
PR: #93

## Freshness result

Current `main` advanced repeatedly during this convergence pass. Every shared-runtime decision was therefore re-read against fresh main rather than promoted from an older Wave branch.

Current main already contains substantial Audio Studio production machinery:
- `audio/studio/runtime/` WORKING v0.3 scene/runtime lineage;
- `audio/studio/alignment_normalizer.py` provider-neutral TTD/TTS timestamp normalization;
- `audio/studio/provider_preflight.py` authenticated read-only model/voice capability preflight;
- `audio/studio/elevenlabs_adapter.py` TTD/TTS request compilation, request hashing, live dispatch, durable response/audio/alignment persistence;
- stereo integrity and timeline tests;
- multilingual PMV additions including render-block compiler v2, TTD-vs-TTS dry experiment harness, audio QC verifier and dependency invalidation/rollback tooling.

These mechanisms are `REUSE_MAIN` and must not be recreated in Wave5.

## Production-control convergence — CLOSED ON MAIN

A narrow Wave5-local production-control experiment was initially implemented and passed 29/29 deterministic tests. During the mandatory sibling-delta sweep, fresher PR #94 was discovered. PR #94 contained a stronger fresh-main integration with controlled dispatch, exact identity+capability live gates, restart-safe spend/idempotency, ambiguous-response reconciliation, strict 48 kHz ingest, provider-vs-production acceptance separation, repair routing and expanded CI.

PR #94 final evidence before merge:
- Audio Studio Runtime workflow SUCCESS;
- dedicated runtime 4/4 PASS;
- full Audio Studio discovery 88/88 PASS;
- no weakening of provider/human/economics evidence boundaries.

PR #94 was promoted from Draft to Ready and merged with expected-head protection.
Merge commit: `49a4d0e455b62dfd68932bf7c60ca4dee7df7b68`.

Post-merge readback confirms current main now contains:
- `audio/studio/runtime/production_control.py`;
- `audio/studio/controlled_provider_dispatch.py`;
- `audio/studio/runtime/audio_asset_ingest.py`;
- `audio/studio/runtime/provider_reconciliation.py`;
- `audio/studio/runtime/production_control_cli.py`;
- `audio/studio/runtime/audio_repair_router.py`;
- associated regression tests and CI hardening.

The duplicate Wave5-local `audio/studio/production_control.py` and its duplicate test file were therefore DELETED from PR #93 before merge. Their 29/29 run remains experiment evidence only; it is not another candidate runtime.

## Supersession result

PR #82 = SUPERSEDED by merged #94. Do not merge it.
PR #86 = historical Wave4 research/evidence package; any integration function duplicated by #94/main is superseded. Preserve history, do not merge stale runtime concepts over main.
PR #93 = convergence/research/state package only; it must not carry a second shared runtime implementation.

## PR #84 reconciliation — NEXT UNIQUE INTERNAL FRONTIER

PR #84 still contains potentially unique Studio Intelligence evidence mechanisms:
- same-source `NARRATED / MULTI_VOICE / DRAMATIZED` benchmark manifest;
- evidence-only benchmark scoring requiring human quality + measured cost;
- performance evidence envelope and no-auto-lock law;
- Human Review Compressor as advisory review planning only;
- measured economics (`generated`, `accepted`, provider cost, manual time, cache/regeneration waste);
- Studio v1 release evidence matrix.

DO NOT wholesale-promote:
- Automatic Director: current main `runtime/performance_compiler.py` already emits Actor Director Score, Rhythm/Pause/Breath and provider-safe context packets; any unique director delta needs its own proof.
- selective repair planner: current main now has `runtime/audio_repair_router.py` and ROOM917 project-local post-render engineering; reuse those unless a concrete missing contract is demonstrated.

## Exact next internal action

Fresh-read post-merge main -> reconcile PR #84 function-by-function -> create only missing Studio Intelligence evidence modules/tests -> run full Audio Studio CI -> merge/readback if green -> update Wave5/Drive/current workstate -> close redundant historical PRs.

## Exact next external action

`AUTHENTICATED INVENTORY -> NARRATOR/ETHAN/AOIFE -> ИФА/КОНТАКТ -> MULTI-STATE/PAIR -> EXACT 3 LIVE LESSON ZERO REQUESTS -> DURABLE WAV+ALIGNMENT -> RESOLVED TIMELINE/MINI-MIX -> BLIND HUMAN -> MEASURED COST -> V1 DECISION`.

No provider/human/economics evidence may be simulated.
