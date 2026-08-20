# Runtime — WORKING v0.2

Executable extensions behind the current audited `audio/studio/orchestrator.py` v1.1 / Audio Studio v3.2.1 stage-gate contract.

## Purpose
Turn one locked scene into one coherent machine-readable production reality, then derive acting, rhythm, body/Foley, spatial sound world, music permissions and pre-alignment mix intentions from that same scene state. This is the bridge between canon/prompt knowledge and actual provider execution.

## Current modules
- `scene_state_graph.py` — validates multi-layer scene reality: story, knowledge, attention, action/tactic, FELT/SHOWN emotion, relationship/status, listening, body, performance, rhythm, space, sound and listener state.
- `IVDIVO_SCENE_STATE_GRAPH_SCHEMA_v1.json` — working runtime contract.
- `performance_compiler.py` — Scene State Graph -> Actor Director Score + Rhythm/Pause/Breath + provider-safe context packets.
- `body_foley_compiler.py` — causal body/mouth/Foley plan; enforces speech consequences and evocative-detail gate.
- `spatial_sound_compiler.py` — listener point of audition + positions + motion/depth automation intent + ambience + story-valid sound cues.
- `music_mix_compiler.py` — music permission only after value change + no-music windows + semantic Mix Action intentions. Never invents absolute timestamps pre-alignment.
- `performance_qc.py` — mechanical WAV performance/regression QC.
- `learning_registry.py` — evidence-based production memory; cannot silently mutate canon.
- `runtime_pipeline.py` — integrated pre-live scene compiler.

## Pipeline
`LOCKED SOURCE/CANON -> SCENE STATE GRAPH -> VALIDATE -> PERFORMANCE/RHYTHM -> BODY/FOLEY -> SPACE/SOUND -> MUSIC/MIX INTENT -> PROVIDER-SAFE RENDER BLOCKS -> CURRENT PROVIDER ADAPTER -> LIVE ALIGNMENT -> PERFORMANCE QC -> EDIT/SELECTIVE RERENDER -> ASSET PRODUCTION -> RESOLVED TIMELINE -> AUTOMIX -> MASTER -> HUMAN LISTEN -> LEARNING REGISTRY`.

The provider adapter remains separate. Runtime never stores secrets and does not treat ElevenLabs or another provider as story authority.

## Integrated compile
```bash
python runtime/runtime_pipeline.py SCENE_STATE_GRAPH.json --out-dir OUT_RUNTIME
```
Expected pre-live outputs include:
- `SCENE_STATE_VALIDATION.json`
- `ACTOR_DIRECTOR_SCORE.json`
- `RHYTHM_PAUSE_BREATH_PLAN.json`
- `PROVIDER_CONTEXT_PACKETS_DRY_RUN.json`
- `BODY_FOLEY_PLAN.json`
- `SPATIAL_SOUND_WORLD_PLAN.json`
- `MUSIC_MIX_INTENT.json`
- `RUNTIME_COMPILE_MANIFEST.json`

## Regression / tests
`audio/studio/tests/test_audio_novel_runtime.py` checks:
- valid scene compiles;
- music without a story value change fails;
- ear-specific staging without mono fallback fails;
- integrated pipeline emits required artifacts.

Existing Scene 2 dry-voice pilot remains the negative regression benchmark for mechanical cadence. A new performance render must beat it before Foley/music are allowed to hide defects.

## Learning law
Every finished pilot/unit may write evidence into the learning registry:
`DEFECT -> ROOT CAUSE -> REPAIR -> RETEST -> RESULT -> REUSE CONDITIONS`.
One success/failure does not rewrite universal canon. Repeated evidence may be promoted only through explicit review/Red Team and a versioned authority update.

## Promotion gate
This runtime remains `WORKING`, not universal canon, until:
1. offline tests pass;
2. Lesson Zero Scene 2 live performance test passes human listening;
3. body/spatial/music layers do not hide a performance failure;
4. regression baseline is materially beaten;
5. no conflict with v3.2.1 provider/live-evidence contracts is found.
