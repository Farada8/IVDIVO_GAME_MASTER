# CURRENT MAIN PROMOTION RECONCILIATION v1

Date: 2026-08-21
Branch: `audio-novel-engine/wave5-convergence-32x64-2026-08-21`
PR: #93

## Freshness result

At the beginning of this promotion pass, current `main` had advanced 34 commits beyond the Wave5 merge base. The branch was therefore treated as a review surface only; current main was re-read before any shared-runtime integration decision.

Current main already contains substantial Audio Studio production machinery:
- `audio/studio/runtime/` WORKING v0.3 scene/runtime lineage;
- `audio/studio/alignment_normalizer.py` provider-neutral TTD/TTS timestamp normalization;
- `audio/studio/provider_preflight.py` authenticated read-only model/voice capability preflight;
- `audio/studio/elevenlabs_adapter.py` TTD/TTS request compilation, request hashing, live dispatch, durable response/audio/alignment persistence;
- stereo integrity and timeline tests;
- newer multilingual PMV main additions: render-block compiler v2, TTD-vs-TTS dry experiment harness, audio QC verifier, dependency invalidation/rollback tooling.

Therefore these mechanisms are classified `REUSE_MAIN`, not reimplemented in Wave5.

## PR #82 reconciliation

PR #82 contained a broad `production_control.py` candidate. Function-by-function reconciliation produced a narrower genuinely missing provider-control layer:

PROMOTE AS CANDIDATE:
1. persistent request/spend state keyed by deterministic request hash;
2. duplicate-paid-dispatch prevention;
3. ambiguous-response quarantine;
4. explicit ambiguous charge/result reconciliation;
5. stable provider error categories + retry policy;
6. capability drift / no-auto-substitution policy;
7. generic dependency descendant invalidation helper;
8. selective rerender boundary validation;
9. control-layer release evidence gate.

DO NOT DUPLICATE:
- alignment normalization;
- provider preflight;
- TTD/TTS request building;
- response/audio persistence;
- scene performance compilation;
- pause/mic/body/Foley/spatial/music compilation;
- human artistic lock decisions.

Candidate location selected: `audio/studio/production_control.py`, beside provider adapter/preflight/alignment modules rather than creating a second runtime tree.

## PR #84 reconciliation

Keep as candidate/evidence concepts:
- same-source NARRATED / MULTI_VOICE / DRAMATIZED benchmark;
- human-review compression as review planning only;
- measured economics;
- fail-closed studio release evidence matrix.

Do not wholesale-promote Automatic Director because current main `runtime/performance_compiler.py` already emits Actor Director Score, Rhythm/Pause/Breath and provider-safe context packets. Unique future director deltas must be proven separately before porting.

## PR #86 + PMV reconciliation

Sound/QC and provider-routing functions increasingly exist on current main. Reuse before adding more modules. In particular, the PMV165-168 line already contributes render block v2, TTD/TTS dry comparison, audio QC and dependency invalidation evidence. Project-specific BODYGUARD roles, clue indices and RU story facts remain project-local.

## New candidate integration

Added on PR #93:
- `audio/studio/production_control.py`
- `audio/studio/tests/test_production_control.py`

Local deterministic result: 29/29 PASS.
Prior Wave5 convergence suite: 68/68 PASS.
Combined newly executed Wave5/convergence-control tests: 97 PASS, 0 FAIL, 0 ERROR.

This is not a live provider or human-quality PASS.

## Promotion gate

Before merge/promotion:
1. inspect GitHub CI/current-main compatibility;
2. ensure no newer main file independently implements the same production-control surface;
3. keep adapter and control separated unless a failing integration test proves a wrapper is needed;
4. merge/readback only if no regression/conflict;
5. after merge, mark duplicate PR82 production-control branch content superseded by current main;
6. live LESSON ZERO canary remains a separate provider/human/economics gate.

## Exact next internal action

Run/inspect PR #93 checks and current-main compatibility. If green, merge the narrow production-control candidate. Then fresh-read main again and continue only with the next unique convergence gap; do not recreate alignment/preflight/adapter/director/QC already present.
