# 00 — IVDIVO AUDIO STUDIO INDEX v3.0

**Date:** 2026-08-20  
**Status:** CURRENT UNIVERSAL AUDIO STUDIO ROUTER

## Authority order
1. Founder’s newest direct instruction.
2. Locked story/project canon and current project authority.
3. `audio/00_IVDIVO_AUDIO_PRODUCTION_INDEX_v2.3.md` — current universal audio-production canon router.
4. `audio/studio/IVDIVO_AUDIO_STUDIO_OS_v3.0.md` — studio operating system.
5. `audio/studio/IVDIVO_AUDIO_STUDIO_10_SPECIALISTS_v1.0.md` — role/responsibility map.
6. `audio/studio/IVDIVO_AUDIO_STUDIO_END_TO_END_SOP_v1.0.md` — execution SOP.
7. `audio/studio/IVDIVO_AUDIO_STUDIO_MACHINE_CONTRACT_v1.0.yaml` — machine state/artifact/gate contract.
8. `audio/studio/IVDIVO_AUDIO_STUDIO_MASTER_PROMPT_STACK_v3.0.md` — execution prompts.
9. `audio/studio/IVDIVO_AUDIO_STUDIO_ARTIFACT_TEMPLATES_v1.0.json` — canonical starter templates for production artifacts.
10. `audio/studio/IVDIVO_ELEVENLABS_PROVIDER_ADAPTER_CONTRACT_v1.0.md` — provider implementation contract; below canon.
11. `audio/studio/IVDIVO_AUDIO_STUDIO_QC_RELEASE_GATES_v1.0.md` — fail-closed release standard.
12. `audio/studio/orchestrator.py` — local fail-closed stage/gate program; no live provider calls.
13. Project-specific overlay.
14. Working manifests/takes/assets/timelines/mixes/QC.

Evidence records include:
- `audio/IVDIVO_AUDIO_REFERENCE_INTELLIGENCE_AUDIT_BATCH1_v1.0.md`
- `audio/IVDIVO_AUDIO_REFERENCE_INTELLIGENCE_AUDIT_BATCH2_v1.0.md`
- `audio/IVDIVO_AUDIO_REFERENCE_INTELLIGENCE_AUDIT_BATCH3_v1.0.md`

## Ten-role studio
1. Executive Audio Producer / Authority Controller
2. Audio Dramaturg & Adaptation Supervisor
3. Casting + Performance Director
4. Dialogue Editor + TTS/Recording Supervisor
5. Foley + Human Microtexture Director
6. Sound Designer + Procedural Audio Designer
7. Ambience / Acoustic / Spatial Director
8. Music Supervisor + Score Director
9. Re-recording Mixer + Mastering Engineer
10. QC / Release Supervisor + Listener Advocate

## Universal pipeline
`LOCKED STORY → AUTHORITY → LISTENER CONTRACT → DRAMATIC FORCE MAP → STAGING → PERFORMANCE → PAUSE/BREATH/LISTENING → BODY/FOLEY → SOUND DESIGN → ACOUSTIC/SPATIAL → MUSIC → PROVIDER DRY RUN → PILOT → LOCKED TAKES/ASSETS → EDIT → ALIGNMENT → MIX ACTION SCORE → MIX → MASTER → MACHINE QC → HUMAN LISTEN → SELECTIVE REPAIR → RELEASE → MASTER LOCK`.

## Core operating principle
The studio is complete when it can answer, for every important audible event:
- what story function does it serve?
- who/what physically caused it?
- what must the listener infer?
- who owns attention?
- what is the performance state?
- where is the listener in acoustic space?
- what should be suppressed?
- how is the element versioned/locked?
- what QC proves it works?

## Execution program
Use `orchestrator.py` to initialize project folder structures, bind source hash, track required artifacts/gates and perform fail-closed release checks. It intentionally does not call providers; external adapters remain replaceable.

See `README.md` for quick start.
