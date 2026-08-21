# WAVE5 — CONVERGENCE ARCHITECTURE + MIGRATION MAP

## Core decision

`ONE CANONICAL AUDIO RUNTIME, MANY PROJECT OVERLAYS.`

Target: `audio/studio/runtime` on current main. Fresh read confirms it is `WORKING v0.3`, not a hypothetical target.

Wave5 does not promote into shared runtime directly while the repository is advancing concurrently. Exact file/function reconciliation and current-main CI must precede shared-runtime writes.

## Fresh-read current runtime
Current main includes Scene State Graph, auditory mise-en-scene, performance compiler, body/Foley compiler, spatial/sound world, music/mix compiler, performance QC, benchmark gate, learning registry and integrated runtime pipeline.

## Migration classes

### Existing runtime — KEEP/REUSE first
- Scene State Graph
- performance/Actor Director Score + rhythm/pause/breath compiler
- body/Foley compiler
- sound-world/spatial compiler
- music permission/mix actions
- integrated scene pipeline
- auditory mise-en-scene
- benchmark regression gate
- mechanical performance QC
- learning registry

### PR82 / PR86 promotion candidates
- source/canary identity pre-dispatch validation
- spend/idempotency ledger
- ambiguous response reconciler
- provider error taxonomy
- 48 kHz asset/hash ingest
- TTD/TTS alignment normalization
- capability snapshot/no-auto-swap
- scoped invalidation/selective rerender
- protected-silence/stem-topology negative fixtures

Fresh direct read of `audio/studio/runtime/production_control.py` on main returned 404 while PR82 contains it. Therefore production-control is a genuine candidate gap as of this read.

### PR84 Studio Intelligence candidates
- NARRATED/MULTI_VOICE/DRAMATIZED benchmark fairness/economics layer
- Performance Intelligence evidence gate
- Human Review Compressor
- Economics Engine
- selective repair dependency closure
- Studio release matrix

Do NOT port PR84 Automatic Director wholesale: current-main `performance_compiler.py` already owns Actor Director Score, rhythm/pause/breath and provider-safe context; `auditory_mise_en_scene.py` owns changing auditory scene logic. Decompose and port only unique behavior.

Do NOT replace `benchmark_gate.py`; extend only genuinely absent three-mode/economic comparison behavior.

### NMM reusable mechanisms
- cryptographic source fingerprint chain
- `NO_BRANCH_FALLBACK`
- exact master replay/alias
- one-listen fact set
- spoiler-neutral casting veto
- clean-first processing domain
- TTS/TTD selective-regeneration routing

### ROOM917 reusable mechanisms
- post-render interval localization before repair
- protected silence
- causal Foley/body/room-bed coverage
- microphone choreography evidence grading
- stereo topology regression
- musical-fact identity contract
- earliest-cause selective repair
- no-scale-until-pilot-proof law

## Prohibited transfers
Never transfer voice IDs, actor/candidate names, story/character/clue facts, project acoustic values, timestamps, project asset hashes or project-specific bus topology unless explicitly declared by target project.

## Integration lifecycle
`DISCOVER -> FRESH READ MAIN -> MAP FUNCTION-BY-FUNCTION -> DEDUPE -> NEGATIVE FIXTURES -> PORT UNIQUE DELTA -> CURRENT-MAIN CI -> REVIEW -> MERGE -> READBACK -> UPDATE AUTHORITY -> RETIRE/SUPERSEDE DUPLICATE DRAFTS`

No branch test count can skip this lifecycle.

## Release model
Deterministic code closes internal uncertainty. It does not prove provider reality, performance naturalness, pair chemistry, pronunciation, long-form fatigue, real alignment, mix translation, listener preference or real cost. Those remain live evidence gates.
