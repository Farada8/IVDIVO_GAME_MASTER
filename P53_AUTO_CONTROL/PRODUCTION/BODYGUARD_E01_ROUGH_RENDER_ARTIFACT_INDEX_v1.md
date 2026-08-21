# BODYGUARD — E01 ROUGH RENDER ARTIFACT INDEX v1

**Authority:** Recording Master v1.6 — RECORDING LANGUAGE CLEAN  
**Episode:** E01 — `11:43`  
**Story text:** LOCKED  
**Coverage:** PASS

## Machine-readable master
`BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json`

Drive file ID: `130imGSx-cMUojQ3cnSwnV0nfUgVIR2Tg`  
Spoken lines: `190`  
Spoken words: `1344`  
Spoken-sequence SHA-256: `2af60ca3b58bc90a2863e8f6dbee2bf7541d6b1f2315e78704f12ca214da9149`

The large per-line request manifest is stored as the raw JSON production authority in the BODYGUARD Drive folder.

## Voice binding
`BODYGUARD_E01_CURRENT_VOICE_MAP_TEMPLATE_v1.json`  
Drive file ID: `1DrJMFXQaT36-pllGBiYiDokfuQsfOYke`

Voice IDs remain null until audition. Temporary pilot lock is not a season lock.

## Take ledger
`BODYGUARD_E01_TAKE_MANIFEST_TEMPLATE_v1.json`  
Drive file ID: `1EtEE4Vj89_9bruZ2B-bQE2d2TqSHHUD1`  
Expected raw takes: `405`

This large ledger tracks every planned take, exact-text hash, future provider IDs, file names, QC and one selected take per spoken block.

## Acceptance gate
`BODYGUARD_E01_ROUGH_RENDER_ACCEPTANCE_GATE_v1.json`  
Drive file ID: `1yxIfOKd3m8b9MbwLd8TGBTbYmRvjkvHp`

Release sequence: `PRE_RENDER → RAW_RENDER_COMPLETE → DIALOGUE_ASSEMBLY_PASS → ROUGH_MIX_PASS → HUMAN_EVIDENCE_PASS → PILOT_GO`.

## Repository verification
- `BODYGUARD_E01_ROUGH_RENDER_COVERAGE_REPORT_v1.json`
- `BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_RUN_SHEET_v1_0.md`
- `BODYGUARD_E01_CURRENT_VOICE_MAP_TEMPLATE_v1.json`
- `BODYGUARD_E01_ROUGH_RENDER_ACCEPTANCE_GATE_v1.json`

## Hard rule
Do not alter `exact_text` when binding voices or rendering. Any text change requires a documented pickup gate after performed-audio evidence.
