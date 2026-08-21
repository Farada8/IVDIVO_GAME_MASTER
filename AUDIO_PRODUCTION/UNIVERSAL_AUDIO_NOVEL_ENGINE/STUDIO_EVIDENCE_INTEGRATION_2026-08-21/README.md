# IVDIVO AUDIO NOVEL ENGINE — STUDIO EVIDENCE INTEGRATION

Date: 2026-08-21
Status: FRESH-MAIN CANDIDATE / NO LIVE OR HUMAN CLAIMS

## Why this exists

PR #94 has already merged production-control into current `main`. Current main also owns scene/performance compilation, provider preflight/adapter/alignment, selective repair and post-render engineering primitives.

Old PR #84 mixed useful evidence mechanisms with functions that now overlap current main. This fresh-main integration keeps only the still-missing evidence layer.

## Promoted candidate surface

`audio/studio/runtime/studio_evidence.py` adds:

1. Same-source A/B/C benchmark contract for exactly:
   - `NARRATED`
   - `MULTI_VOICE`
   - `DRAMATIZED`

   Every variant must share the same locked source hash and exact-text hash.

2. Evidence-complete benchmark scoring requiring:
   - human believability;
   - clarity;
   - want-more;
   - fatigue resistance;
   - duration;
   - provider cost;
   - manual time / labor rate.

3. No-auto-winner law.
   Machine may expose quality leaders and economics but `winner=null`; artistic mode selection remains human/Founder decision.

4. Performance evidence gate.
   Multi-state + pronunciation + fatigue + human review (+ pair where required) are necessary before a candidate is even eligible for a human lock decision. Machine cannot lock a voice.

5. Human Review Compressor.
   Prioritizes suspected intervals for efficient review but cannot clear release and cannot replace final blind/full listen.

6. Measured Economics.
   Reports generated vs accepted minutes, provider/manual cost, cost per accepted minute, acceptance yield, cache reuse and regeneration waste. Missing measurements remain HOLD.

7. Studio Release Evidence Matrix.
   Even when all machine-readable evidence is complete, result is `GO_FOR_FOUNDER_RELEASE_DECISION`, never self-declared `PRODUCTION_READY`.

## Explicit non-duplication

NOT ported from old PR #84:
- Automatic Director — current `runtime/performance_compiler.py` already owns Actor Director / rhythm / provider-safe context compilation;
- selective repair planner — current main contains `runtime/audio_repair_router.py`, and ROOM917 has a bounded project-local post-render engineering pilot;
- provider dispatch/alignment/ingest — current main owns these after merged PR #94.

## Deterministic evidence

Local candidate suite: 24/24 PASS.

This proves only deterministic contract behavior. It does NOT prove:
- provider quality;
- voice suitability;
- pronunciation;
- chemistry;
- human listening quality;
- real economics;
- cross-project live portability;
- production readiness.

## Current empirical path

`AUTHENTICATED INVENTORY -> NARRATOR/ETHAN/AOIFE -> ИФА/КОНТАКТ -> MULTI-STATE/PAIR -> EXACT 3 LESSON ZERO LIVE REQUESTS -> DURABLE WAV+ALIGNMENT -> NARRATED/MULTI_VOICE/DRAMATIZED EVIDENCE -> BLIND HUMAN -> MEASURED COST -> CROSS-PROJECT LIVE PORTABILITY -> FOUNDER V1 DECISION`.
