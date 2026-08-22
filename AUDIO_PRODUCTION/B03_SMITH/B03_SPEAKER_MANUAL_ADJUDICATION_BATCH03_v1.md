# B03 — SPEAKER MANUAL ADJUDICATION BATCH 03

**Date:** 2026-08-22  
**Status:** PASS_36_INDIVIDUAL_HIGH_INFORMATION_ASSIGNMENTS / NO_RULE_PROMOTION

## Input authority
Baseline before batch: `92_B03_SPEAKER_ATTRIBUTION_CURRENT_BASELINE_v1_4.json` = **544 / 3715** assigned.

UNKNOWN review queue: `93_B03_UNKNOWN_SPEAKER_HIGH_INFORMATION_REVIEW_QUEUE_v1_2.json`.

## Method
Thirty-six high-information UNKNOWN segments were reviewed individually against immutable exact local context. Accepted evidence included explicit same-paragraph continuation, direct named addressee/response chains, explicit channel entry, explicit `continued/answered/kept speaking/called` narration, locally unambiguous pronoun antecedents, and response text whose referent is uniquely bound by the immediate narration.

No contextual heuristic was promoted from this batch. Alternating-turn inference, same-speaker sandwich inference and action-subject auto assignment remain prohibited.

## Result
- assignments before batch: 544
- manual adjudications added: **36**
- current assignments: **580**
- semantic spoken candidates: 3715
- remaining UNKNOWN: **3135**
- coverage: **15.61%**
- story text changes: 0
- exact-text byte changes: 0
- voice map authorized: **NO**

## Drive evidence
- Batch JSON: `94_B03_SPEAKER_MANUAL_ADJUDICATION_BATCH03_v1.json` — Drive ID `1DwGXsFpVw6SomL-aZUNRwzFuBksDFCRF`
- Current baseline: `95_B03_SPEAKER_ATTRIBUTION_CURRENT_BASELINE_v1_5.json` — Drive ID `1cNgPDMNK2F7_c-yOOxpY2iJIiiNbXUev`
- Updated UNKNOWN queue: `96_B03_UNKNOWN_SPEAKER_HIGH_INFORMATION_REVIEW_QUEUE_v1_3.json` — Drive ID `1f1EfVdWFwgIR7G16tY8boq41mByrIOog`

## Production law
`INDIVIDUAL_CONTEXT_ADJUDICATION != GENERIC_RULE_PROMOTION`

UNKNOWN remains valid. A voice-map must not consume superseded Tier1–Tier4 maps.

## Next gate
Continue evidence-first adjudication from the 3135 UNKNOWN cases. Prefer named channel entry, direct question/addressee evidence, explicit discourse continuation and recurring-major-character resolution. Do not chase coverage percentage by guessing.
