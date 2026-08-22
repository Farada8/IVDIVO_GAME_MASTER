# CURRENT ROOM917 SFX ASSET FACTORY

**Status:** MACHINE_QC_PASS / HUMAN_BLIND_GATE_PENDING  
**Date:** 2026-08-22

## Authority
Current E01 Sound Director authority resolves:
- `S13_INTERNAL_DOUBLE_RING_OLD` — sharp ordinary old internal telephone double ring; no horror processing.
- `S14_UNMARKED_GLASS_LAMP_PING` — same material family as 916, spatially distinct.
- `S17_COPPER_HISS` — narrow intimate low-voltage old-line texture; authentic 917 line has no steady 50 Hz hum.
- `S19_TWO_PART_LINE_CUT` — two mechanically distinct interruptions, then silence.

## Current candidate bytes
`S13` and `S14` are byte-identical aliases of already-produced A02 candidates. They must not be regenerated under new cue names.

`S17` and `S19` now have two 48 kHz / 24-bit PCM candidates each, plus mono and 180–7000 Hz phone/mobile QC proxies.

Machine checks:
- all candidate records: PASS;
- S13/S14 alias byte identity: PASS;
- S17 steady-50-Hz rejection: PASS;
- S19 authored post-cut silence: PASS;
- 916-marked vs unmarked lamp family discriminability: PASS.

## Fail-closed lock rule
Use `sfx_registry_gate.py` with `ROOM917_SFX_ASSET_MANIFEST_v2.json`.

Before human blind selection, `ROOM917_SFX_HUMAN_LOCK_TEMPLATE_v1.json` intentionally returns `HOLD`.
After human blind acceptance, selected cue/candidate/hash triples must match the manifest exactly. Any changed hash returns `FAIL`.

Test evidence: `ROOM917_SFX_GATE_TEST_REPORT_v1.json` = PASS, including an intentional tampered-hash failure fixture.

## Durable bytes
Google Drive folder: `ROOM917_SFX_ASSET_FACTORY` under `00_IVDIVO_UNIVERSAL_AUDIO_PRODUCTION_STUDIO`.

Stored packs:
- `ROOM917_SFX_ASSET_FACTORY_v2_ADMIN.zip` — SHA-256 `3b74be72c24109f9a97036ab847c45f5bcf4f2197afbf1fe0049c05af0694ded`;
- `ROOM917_SFX_S13_S14_S17_S19_BLIND_v2.zip` — SHA-256 `8b66af4cf3a3fe728e476d83a9227be1d4bd1e3576f748212acaafefe80ebfdc`;
- `ROOM917_SFX_ENGINE_GATE_v1.zip` — SHA-256 `5a53faa0cdd78cfdfed4141572393c9ae0dd7e8ae8ec8b07e30ccff880a91875`.

## Next executable gate
Human blind listen selects X/Y or rejects both. No cue becomes `AUDIO_CANON_MASTER` before that evidence exists.
