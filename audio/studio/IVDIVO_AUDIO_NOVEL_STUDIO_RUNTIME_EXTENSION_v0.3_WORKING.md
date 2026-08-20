# IVDIVO AUDIO NOVEL STUDIO — RUNTIME EXTENSION v0.3

**Status:** WORKING / IMPLEMENTATION EXTENSION — NOT UNIVERSAL CANON  
**Integration target:** current `00_IVDIVO_AUDIO_STUDIO_INDEX_v3.2.1.md` and its audited provider/evidence stack.  
**Replaces for development:** runtime-extension v0.1 working description; v0.1 remains historical.

## Purpose
Close the gap between rich audio-direction documents and what actually reaches rendering/mixing. One locked scene becomes one shared Scene State Graph. Every department derives its work from that same reality.

## Core law
The unit of production is the **listener-experienced dramatic moment**.

`STORY FACT -> CHARACTER KNOWLEDGE/ATTENTION -> WANT/TACTIC -> FELT/SHOWN EMOTION -> LISTENING/RESPONSE -> BODY -> PERFORMANCE/RHYTHM -> AUDITORY MISE-EN-SCENE -> SPACE -> FOLEY/SOUND -> MUSIC PERMISSION -> MIX FOCUS -> RENDER/ALIGN -> QC/HUMAN LISTEN -> LEARNING`.

No department may independently decorate the scene with uncaused sound.

## Runtime object: Scene State Graph
Each important turn/beat may carry:
- locked source IDs and exact text;
- knowledge and attention state;
- want, tactic and subtext;
- emotion as FELT vs SHOWN, suppression, leakage, transition cause and carryover;
- relationship and status/power state;
- heard event, response impulse, entry trigger and listening state;
- body, posture, physical occupation, mouth/food/drink state and audible actions;
- playable vocal behavior, breath and phrase ending;
- pause/overlap/interruption/protected silence;
- position, distance, head orientation, movement, occlusion and mono fallback;
- listener contract and focus owner;
- sound/music/mix permissions.

Schema pointer: `audio/studio/runtime/IVDIVO_SCENE_STATE_GRAPH_SCHEMA_v1.json`.

## Auditory mise-en-scène / camera of imagination
`runtime/auditory_mise_en_scene.py` explicitly models the changing mental scene the listener should construct:
- foreground/mid/far depth planes;
- current focus owner;
- what enters attention;
- what recedes;
- listener/auditory-camera position and movement;
- transition cause between mental frames;
- silence function.

The goal is not maximum sound density. It is a coherent succession of lived acoustic images.

## Executable modules
- `runtime/scene_state_graph.py` — multi-layer causal validation.
- `runtime/auditory_mise_en_scene.py` — mental-scene / auditory-camera compiler.
- `runtime/performance_compiler.py` — Actor Director Score + rhythm/pause/breath + provider-safe context packets.
- `runtime/body_foley_compiler.py` — physical-state and causal Foley compiler; food/mouth consequences and evocative-detail gate.
- `runtime/spatial_sound_compiler.py` — listener point of audition, character geography, movement/depth automation intent, ambience and story-valid sound events.
- `runtime/music_mix_compiler.py` — music only after declared value change; no-music windows and semantic mix intentions.
- `runtime/runtime_pipeline.py` — integrated pre-live compiler.
- `runtime/performance_qc.py` — WAV cadence/pause/regression evidence.
- `runtime/benchmark_gate.py` — candidate-vs-approved benchmark gate; critical regression blocks promotion.
- `runtime/learning_registry.py` — controlled self-improvement memory.

## Integrated pre-live compile
`python runtime/runtime_pipeline.py SCENE_STATE_GRAPH.json --out-dir OUT_RUNTIME`

Outputs:
`SCENE_STATE_VALIDATION / AUDITORY_MISE_EN_SCENE / ACTOR_DIRECTOR_SCORE / RHYTHM_PAUSE_BREATH_PLAN / PROVIDER_CONTEXT_PACKETS_DRY_RUN / BODY_FOLEY_PLAN / SPATIAL_SOUND_WORLD_PLAN / MUSIC_MIX_INTENT / RUNTIME_COMPILE_MANIFEST`.

Then the existing v3.2.1 provider stack owns preflight, ElevenLabs dispatch, live evidence, raw + normalized alignment and provider-specific constraints.

## Performance-before-decoration gate
Dialogue/performance must pass before Foley/music are allowed to conceal weakness. Known-bad Lesson Zero Scene 2 v1 remains a negative regression fixture. The replacement must materially beat it on mechanical cadence and human believability.

## Improvement architecture
Every pilot/chapter records:
`DEFECT -> ROOT_CAUSE -> REPAIR_HYPOTHESIS -> BEFORE_METRICS -> AFTER_METRICS -> HUMAN_RESULT -> REUSE_CONDITIONS`.

`learning_registry.py` requires repeated success across units and human passes before producing `CANDIDATE_FOR_REVIEW`. Nothing auto-rewrites canon.

`benchmark_gate.py` prevents calling a version better when one dimension improves while a critical dimension regresses. Candidate evidence may include cadence, pause variation, speech-rate variation, intelligibility, voice identity, spatial legibility, mono survival, microtexture fatigue, music masking, human believability and desire to continue.

## Current test law
CI workflow: `.github/workflows/audio-studio-runtime-tests.yml`.
It runs the new integrated runtime tests and existing Audio Studio tests on relevant pushes.

## Promotion gate to canonical runtime
Do not merge v0.3 into universal authority until:
1. runtime tests PASS;
2. Lesson Zero Scene 2 live performance is materially superior to v1 and passes human listen;
3. auditory mental-frame transitions are coherent;
4. performance still works with music muted and Foley reduced;
5. body/mouth states remain physically plausible and headphone-safe;
6. spatial design survives mono and does not use pan as a substitute for distance;
7. provider preflight/live evidence/alignment provenance remains valid under v3.2.1;
8. benchmark gate shows no critical regression;
9. learning-loop rules prove selective repair on at least two units;
10. Founder explicitly approves promotion or the designated authority process records it.
