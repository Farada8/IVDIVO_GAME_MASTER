# 125_B03 — SPEAKER CONTEXT BATCH CH19–21 GATE v0.4

**Status:** **PASS — batch only. FULL SPEAKER GATE NOT PASSED.**  
**Story authority:** FOUNDER-LOCKED CH01–29.  
**Text mutation:** **0 bytes**.  
**Voice IDs assigned:** **0**.

## Inputs
- Immutable exact-text segmentation package: Drive `1FuDJDUGNjgsNITpNmfQV_d8N4oIrs5HB`.
- Segmentation package SHA-256: `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`.
- Repaired speaker engine gate: Drive `1Xv_Ys0a7AnHHJMNl0pgoA90t8iE5FVU_`.
- Semantic exception patch: `100_B03_SPEAKER_SEMANTIC_EXCEPTION_PATCH_v0.3`.
- Evidence contract: `IVDIVO_SPEAKER_ATTRIBUTION_EVIDENCE_CONTRACT_v2`.

## Batch result
- CH19 actual speech turns: **113/113 assigned**, UNKNOWN 0.
- CH20 actual speech turns: **132/132 assigned**, UNKNOWN 0.
- CH21 actual speech turns: **110/110 assigned**, UNKNOWN 0.
- Batch total: **355/355 assigned**.
- New semantic narrator-inline exceptions found in CH20–21: **0**.
- Known CH19 exception `B03_CH19_S0206` (`“second hit”`) remains narrator delivery and is excluded from the speech denominator.
- Exact-text changes: **0**.
- Personal identities invented for anonymous voices: **0**. Anonymous operational speakers remain role-labelled.

## Cumulative CH01–21
- Reviewed actual speech turns: **2390**.
- Assigned: **2387**.
- UNKNOWN retained: **3**.
- Reviewed-scope coverage: **99.87%**.
- Remaining UNKNOWN are unchanged: `B03_CH03_S0240`, `B03_CH03_S0244`, `B03_CH03_S0248`.
- Full-book actual speech denominator: **3714**.
- Actual speech turns not yet context-reviewed after CH21: **1324**.

## Authority safeguards
- Locked prose and causality were not edited.
- CH30 remains unauthorized.
- Local Slovenian operational authority remains local; speaker labels do not promote OES/Confederation authority.
- Role labels such as `HYDRO_CONTROL_CH19`, `ROAD_CONTROL_CH20`, `HYDRO_ENGINEER_CH21`, and `REGIONAL_DUTY_OFFICER` identify only the textual operational role, not an invented person.
- `voice_id = null` remains mandatory until full speaker gate + casting evidence.

## Decision
**GO to CH22–24 contextual speaker review.**

Full speaker gate remains open. No provider call, paid synthesis, human audition, voice lock, WAV, alignment, mix/master, audio QC, market evidence, or Human Signal is claimed.
