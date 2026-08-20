# 00 — IVDIVO AUDIO STUDIO INDEX v3.2.1 AUDITED + PROVIDER VERIFIED

**Date:** 2026-08-20  
**Status:** CURRENT UNIVERSAL AUDIO STUDIO ROUTER

## Authority order
1. Founder’s newest direct instruction.
2. Locked story/project canon and current project authority.
3. `audio/00_IVDIVO_AUDIO_PRODUCTION_INDEX_v2.3.md` — underlying universal audio canon.
4. `audio/studio/IVDIVO_AUDIO_STUDIO_OS_v3.0.md` — base studio OS.
5. `audio/studio/IVDIVO_AUDIO_STUDIO_CANON_PATCH_v3.2_AUDITED.md` — current audit-derived additive authority.
6. `audio/studio/IVDIVO_AUDIO_STUDIO_MACHINE_CONTRACT_v1.1.yaml` — current machine/gate contract.
7. `audio/studio/IVDIVO_AUDIO_STUDIO_MASTER_PROMPT_STACK_v3.0.md` interpreted through v3.2 patch.
8. `audio/studio/IVDIVO_AUDIO_STUDIO_ARTIFACT_TEMPLATES_v1.1.json`.
9. `audio/studio/IVDIVO_ELEVENLABS_PROVIDER_ADAPTER_CONTRACT_v1.1_VERIFIED_2026-08-20.md` — current verified ElevenLabs adapter profile.
10. `audio/studio/alignment_normalizer.py`.
11. `audio/studio/provider_preflight.py`.
12. `audio/studio/elevenlabs_adapter.py`.
13. `audio/studio/stereo_integrity_qc.py`.
14. `audio/studio/orchestrator.py` v1.1 dependency-DAG/live-evidence controller.
15. Base SOP/QC/10-role documents where not superseded.
16. Project-specific overlay.
17. Working production artifacts.

## Independent audit status
v3.1 independent Red Team verdict was `READY WITH BLOCKERS`. v3.2/v3.2.1 dispositioned the blockers rather than rewriting the architecture.

Closed in canon/program contracts:
- provider alignment schema divergence;
- LIVE/DRY_RUN/MIXED evidence ambiguity;
- cross-build reuse provenance;
- voice-binding drift;
- silent-reaction compiler gap;
- manual-review ambiguity;
- source-vs-stem stereo collapse blind spot;
- cross-domain clue/music acoustic/pitch identity;
- provider connectivity/credential/capability preflight;
- human-review triage;
- linear-vs-parallel gate mismatch.

## Current verified provider facts
Official ElevenLabs docs were rechecked 2026-08-20.
- TTD timestamps: `POST /v1/text-to-dialogue/with-timestamps`; documented response includes `voice_segments`, `alignment`, `normalized_alignment`; max 10 unique voice IDs; reliability guidance ≈2000 total input characters; up to 3 pronunciation dictionaries; default model currently documented as `eleven_v3`; seed is best-effort only.
- Single-voice timestamp TTS: `POST /v1/text-to-speech/{voice_id}/with-timestamps`; response uses character alignment arrays; documented default model differs (`eleven_multilingual_v2`).
- Preflight: `GET /v1/models` + known-voice `GET /v1/voices/{voice_id}` with `xi-api-key` secret from environment.

These are runtime provider facts, not permanent story canon.

## Current pipeline
`LOCKED STORY → AUTHORITY/BUILD MANIFEST → LISTENER CONTRACT → DRAMATURGY → STAGING → VOICE BINDING + PERFORMANCE → SILENT REACTIONS/PAUSE/BREATH → FOLEY/BODY → SOUND/ACOUSTIC IDENTITY → SPATIAL/STEREO INTENT → MUSIC → PROVIDER DRY RUN → PROVIDER PREFLIGHT → PILOT → PARALLEL DIALOGUE+ASSET PRODUCTION → LOCKS → EDIT → RAW ALIGNMENT → NORMALIZED ALIGNMENT → TIMELINE → MIX ACTION + OVERLAP/STEREO QC → MIX → MASTER → MACHINE QC → REVIEW PRIORITY → HUMAN LISTEN/MANUAL REVIEW → SELECTIVE REPAIR → RELEASE → MASTER LOCK`.

## Release law
No DRY_RUN build can release. Required live/reused evidence must be complete and provenance-valid. Mandatory MANUAL_REVIEW must be resolved. Open FATAL=0 and MAJOR=0. Raw provider alignment may not bypass normalization. Real provider preflight and live pilot evidence remain per-project runtime gates.
