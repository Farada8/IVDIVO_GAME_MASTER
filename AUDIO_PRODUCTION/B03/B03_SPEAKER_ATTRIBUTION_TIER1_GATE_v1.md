# B03 — THE EMPTY RESCUE — SPEAKER ATTRIBUTION TIER 1 GATE v1

**Date:** 2026-08-22  
**Story state:** FOUNDER LOCKED / RELEASE READY  
**Input:** `77_B03_EXACT_TEXT_SEGMENTATION_PACKAGE_v1.0.zip`  
**Input SHA256:** `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`  
**Policy:** exact locked prose; speaker metadata only; no text mutation.

## Result

- chapters: 29/29
- total exact-text segments: 7,465
- narration segments already fixed to `NARRATOR`: 3,747
- dialogue segments requiring attribution: 3,718
- Tier-1 explicit dialogue assignments: **653**
- remaining dialogue `UNKNOWN`: **3,065**
- Tier-1 coverage: **17.56%**
- story/prose byte changes: **0**
- guessed ambiguous speakers: **0**

Full Tier-1 map is persisted in Drive:
`78_B03_SPEAKER_ATTRIBUTION_TIER1_EXPLICIT_v1.json`
Drive ID: `1jC_88TFKo6OvSWfF3Nayey4xRt48gkDZ`
Local generation SHA256: `97b2110ea21e8fa47d3367f8bb5412d7020ecf5786e01ff494de825a0867f2f4`.

## Tier-1 admissibility rule

A dialogue segment is assigned only when the immediate quote boundary contains an explicit named or role-based speech attribution such as:
- `Jana said/asked/...`
- `Smith said/asked/...`
- `Hydro control answered/...`
- `The OES reviewer said/...`

Canonical recurring identities are normalized (`Maja Rojc -> MAJA`, reviewer variants -> `OES_REVIEWER`, etc.).

Forbidden in Tier 1:
- pronoun resolution (`he/she`) without a separate contextual proof;
- alternating-turn assumptions;
- guessing from emotional content;
- guessing from gender alone;
- assigning a voice because a line “sounds like” a character;
- rewriting dialogue to make attribution easier.

## Frequent Tier-1 assignments

The explicit layer recovers recurring speakers including JANA, SMITH, TINA, NIKA, ANDREJ, MAJA, OES_REVIEWER, HYDRO_CONTROL, REGIONAL_DUTY_OFFICER, TAREN, EVA, LUKA and bounded role speakers.

## Gate disposition

`TIER1_EXPLICIT_ATTRIBUTION = PASS`

`FULL_SPEAKER_ATTRIBUTION_GATE = OPEN`

The map is deliberately incomplete. Tier 2 must resolve only contextually provable lines and keep all residual ambiguity as `UNKNOWN`. Voice-map lock is not authorized until the speaker-attribution gate has a documented residual-unknown disposition.