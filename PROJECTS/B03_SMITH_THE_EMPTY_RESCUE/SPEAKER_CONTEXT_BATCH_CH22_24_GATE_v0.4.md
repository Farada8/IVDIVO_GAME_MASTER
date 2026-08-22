# 129_B03 — SPEAKER CONTEXT BATCH CH22–24 GATE v0.4

**Status:** **PASS — batch only. FULL SPEAKER GATE NOT PASSED.**  
**Story authority:** FOUNDER-LOCKED CH01–29.  
**Text mutation:** **0 bytes**.  
**Voice IDs assigned:** **0**.

## Inputs
- Immutable exact-text segmentation package: Drive `1FuDJDUGNjgsNITpNmfQV_d8N4oIrs5HB`.
- Segmentation package SHA-256: `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`.
- Evidence contract: `IVDIVO_SPEAKER_ATTRIBUTION_EVIDENCE_CONTRACT_v2`.
- Strong baseline cross-check: `95_B03_SPEAKER_ATTRIBUTION_CURRENT_BASELINE_v1_5.json`.
- CH01–03 reconciliation authority: `B03_SPEAKER_AUTHORITY_RECONCILIATION_CH01_03_v4`.

## Batch result
- CH22 actual speech turns: **163/163 assigned**, UNKNOWN 0.
- CH23 actual speech turns: **138/138 assigned**, UNKNOWN 0.
- CH24 actual speech turns: **207/207 assigned**, UNKNOWN 0.
- Batch total: **508/508 assigned**.
- New semantic narrator-inline exceptions: **0**.
- Exact-text changes: **0**.
- Personal identities invented for anonymous voices: **0**.

## Cross-check result
- Strong-baseline assignments overlapping CH22–24: **145**.
- Substantive speaker conflicts after role-alias normalization: **0**.
- One initial contextual read in CH22 (`B03_CH22_S0216`) was corrected before promotion: manual strong evidence showed the duty officer explicitly addressed road control, so the response is `ROAD_CONTROL_CH22`, not Maja.

## Reconciled cumulative CH01–24
- Full-book actual speech denominator: **3714**.
- Context-reviewed actual speech: **2898**.
- Assigned: **2898**.
- UNKNOWN in reviewed scope: **0**.
- Not yet context-reviewed: **816**.
- Remaining scope is exactly CH25–29: CH25 120, CH26 169, CH27 153, CH28 166, CH29 208.

The previous downstream pointer carried three CH03 UNKNOWN values from a stale pre-reconciliation state. `B03_SPEAKER_AUTHORITY_RECONCILIATION_CH01_03_v4` closed those three without text mutation; they must not be propagated forward.

## Drive authority
- CH22 map: `1kZJy91dPNU7dakbXEoYyVLo6mHCnvgex`
- CH23 map: `1P-UZtTun34pGfK1hpkI0edf-mySB7x4j`
- CH24 map: `10sXNFUDoGjCQhT12uIp0SnmmhKqSl4eP`
- manifest: `1y6B7lEr9zWFuyxjta8s3G5TFR666m-ZX`
- voice-map template: `1mUgsInTYtlqWRXyhp_Xhdmr8n6VIuU5x`
- gate: `1E8vd8aZRfjKoBhjr2MBW4ihDu7TTkLua`
- ZIP: `1ey9xi1JJFz7mr6HIE2gVjQ3vb025k_70`

## Authority safeguards
- Locked prose and causality were not edited.
- CH30 remains unauthorized.
- Local Slovenian operational authority remains local.
- Anonymous operational voices remain role-labelled. No personal identity or precursor ontology is invented.
- `voice_id = null` remains mandatory until the full speaker gate and casting evidence pass.
- No alternating-turn heuristic is promoted as a machine rule.

## Decision
**GO to CH25–27 contextual speaker review.**

Full speaker gate remains open. No provider call, paid synthesis, human audition, voice lock, WAV, alignment, mix/master or audio QC is claimed.
