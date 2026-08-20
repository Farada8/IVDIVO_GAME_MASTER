# IVDIVO Microphone Choreography / Virtual Radio Stage Engine

Current version: v1.0. Current studio router: `audio/studio/00_IVDIVO_AUDIO_STUDIO_INDEX_v3.3.md`.

Purpose: make actor movement around microphones/listener a first-class production system instead of treating it as simple pan automation.

Architecture:
`PERFORMANCE ENGINE → MICROPHONE CHOREOGRAPHY ENGINE → WORLD SOUND ENGINE → EDIT/ALIGNMENT → MIX/MASTER/QC`.

Modes:
- REAL_STAGE — actors physically move relative to microphone(s).
- VIRTUAL_STAGE — clean performances are spatially staged in post.
- HYBRID_STAGE — performance carries body/projection behavior; post supplies exact geometry. Recommended default for premium AI drama.

Package:
- canonical engine specification;
- machine contract;
- MC-00..MC-15 prompt stack;
- spatial-performance QC;
- Reference Intelligence Batch 4;
- `microphone_choreography.py` planning compiler.

Compiler use:
```bash
python microphone_choreography.py scene.json --output compiled_spatial_manifest.json
```

The compiler preserves semantic anchors and deliberately does not invent final timestamps before accepted dialogue alignment. Its dB/pan/room-send outputs are renderer-neutral planning estimates, not a physical acoustic simulation.