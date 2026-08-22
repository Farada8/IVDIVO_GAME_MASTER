# CURRENT ROOM917 SFX ASSET FACTORY

**Status:** MACHINE_QC_PASS / FULL_BLIND_v6_READY / HUMAN_BLIND_GATE_PENDING  
**Date:** 2026-08-22

## Current production authority
Use:
- `ROOM917_SFX_ASSET_MANIFEST_v5.json` — active candidate registry;
- `sfx_registry_gate_v2.py` — fail-closed manifest/human-lock gate;
- `ROOM917_SFX_GATE_TEST_REPORT_v2.json` — regression evidence;
- `ROOM917_SFX_ALL_COMBINATIONS_QC_v1.json` — 30/30 critical candidate combinations PASS.

Historical v2/v3/v4 manifests and blind packs are evidence only and must not be used for new lock decisions.

## Active cue truth
- `S13_INTERNAL_DOUBLE_RING_OLD` — ordinary old internal double ring; no horror processing.
- `S14_UNMARKED_GLASS_LAMP_PING` — same material family as 916 marked lamp, but clue-distinct.
- `S17_COPPER_HISS` — narrow intimate old-line texture; no steady 50 Hz.
- `S19_TWO_PART_LINE_CUT` — two dry mechanically distinct interruptions, then authored hard silence.
- 916 selector/lamp and A01 50 Hz transformer remain active blind candidates from the original A01/A02 factory set.

## Repairs and retirement history
S19 candidates 1–2 were retired after cross-cue collision review against S13 ring. Candidates 3–4 and 5 failed progressively stronger distinctness gates. Active S19 candidates are **6 and 7**, both machine-QC PASS.

## Cross-cue proof
All 30 tested X/Y combinations PASS, including:
- every 916 marked-lamp candidate vs every S14 unmarked-lamp candidate;
- every selector candidate vs every relay-tremble candidate;
- every S13 ring candidate vs S19 candidates 6/7;
- phone-band survival for all critical clue assets;
- both 50 Hz transformer candidates vs both S17 hiss candidates.

## Fail-closed human lock
Before human blind selection the registry returns `HOLD`.
A selected cue must reference an **active candidate and exact SHA-256**. Retired candidates fail. Hash drift/tampering fails.
No `AUDIO_CANON_MASTER` may be declared from machine metrics alone.

## Durable bytes
Google Drive folder: `ROOM917_SFX_ASSET_FACTORY` inside `00_IVDIVO_UNIVERSAL_AUDIO_PRODUCTION_STUDIO`.

Current packs:
- `ROOM917_SFX_ASSET_FACTORY_v5_ADMIN.zip` — SHA-256 `195e6f1c2ad278b47505e9efcb4d337e9d9d1d28dd90f5243019c10b23cf4258`;
- `ROOM917_SFX_ENGINE_GATE_v2.zip` — SHA-256 `9ba06a847c6fe47ecc53a57535461f675366e2b8ba3744fbb856611fc2dffcce`;
- **`ROOM917_SFX_FULL_BLIND_v6.zip`** — current listener pack, SHA-256 `79adb2e0c21a6d4cb76150600c2af49f0a4bd38bf6b4c83566f1ec86693e6cee`;
- `ROOM917_SFX_FULL_ADMIN_v6.zip` — mapping + all-combination QC, SHA-256 `fda465ef77f80888aba3d9e60fb09129c1fd749a6d6c57e97bc625a698be5d3e`.

## Current boundary
Machine work for this requested factory scope is complete and green. The only non-simulatable gate is the human blind listen: X/Y/REJECT BOTH. After that result, run gate v2 and lock exact accepted bytes as `AUDIO_CANON_MASTER`.
