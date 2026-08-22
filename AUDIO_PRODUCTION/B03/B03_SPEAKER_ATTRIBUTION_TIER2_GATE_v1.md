# B03 — THE EMPTY RESCUE — SPEAKER ATTRIBUTION TIER 2 GATE v1

**Date:** 2026-08-22  
**Input:** immutable exact-text segmentation package v1.0  
**Story mutation:** forbidden / none performed

## Result

- dialogue segments: 3,718
- Tier-1 explicit assignments: 653
- Tier-2 additional safe pronoun resolutions: 47
- cumulative assigned: **700**
- residual UNKNOWN: **3,018**
- cumulative coverage: **18.83%**
- prose byte changes: **0**

Full cumulative map:
`79_B03_SPEAKER_ATTRIBUTION_TIER2_CONSERVATIVE_v1.json`
Drive ID: `1D9ZVwn1VQxqv4zQ2ZjrMENhH4qy023ix`
SHA256 at generation: `f8fdeddaf7831c0f85b9d25875aa02bb3952026916290b5b52013569d5a66235`.

## Tier-2 rule

Tier 2 adds a pronoun-attribution only when all conditions pass:
1. quote boundary explicitly says `he/she said/asked/answered/...`;
2. immediately preceding narration contains a named grammatical subject at sentence start;
3. subject is a known named character with known gender from locked text;
4. pronoun gender matches that subject;
5. no speaker is already assigned by stronger Tier-1 evidence.

This deliberately rejects tempting but unsafe cases. Example class: narration may mention Nika immediately before a line ending in `he asked`; gender mismatch prevents a false Nika assignment even if she is the nearest name.

## Current highest-volume recurring explicit/verified speaker IDs

- JANA 194
- SMITH 99
- TINA 58
- NIKA 54
- OES_REVIEWER 52
- ANDREJ 49
- MAJA 47
- HYDRO_CONTROL 31
- REGIONAL_DUTY_OFFICER 19
- TAREN 11
- TECHNICIAN 11

Counts are attribution-map counts, not final spoken-word or casting weights.

## Gate disposition

`TIER2_CONSERVATIVE = PASS`

`FULL_SPEAKER_ATTRIBUTION = OPEN`

Next admissible layer is contextual attribution with explicit evidence objects. It may use bounded scene participants, vocatives, and action-beat ownership only where each assignment is auditable. It must not use naive alternating-turn assumptions. Residual ambiguity remains `UNKNOWN` and can later be handled by human/director review rather than inventing certainty.