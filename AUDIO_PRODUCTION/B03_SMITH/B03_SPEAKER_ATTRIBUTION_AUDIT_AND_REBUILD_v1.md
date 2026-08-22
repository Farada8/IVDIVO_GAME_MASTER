# B03 — SPEAKER ATTRIBUTION AUDIT + REBUILD v1

**Date:** 2026-08-22  
**Project:** B03 / THE EMPTY RESCUE  
**Status:** PARTIAL PASS / PREVIOUS TIER1–TIER4 MAP SUPERSEDED

## Trigger
The previous Tier-4 speaker map contained direct contradictions with immutable exact-text narration. Examples included segments where `Tina said,` preceded a quote that the map assigned to ANDREJ, and `Hydro control said,` preceded a quote assigned to TINA.

## Immutable source boundary
The locked CH01–CH29 exact-text segmentation package remains unchanged. Story text changes: 0. Exact-text byte changes: 0. Semantic speaker work is downstream metadata only.

Source package SHA256: `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`.

## Semantic quote correction
Three curly-quote segments are demonstrably inline quoted terms rather than separately spoken dialogue:
- `B03_CH02_S0200` — `“bad”`
- `B03_CH16_S0082` — `“SAVED THE PASS.”`
- `B03_CH19_S0206` — `“second hit”`

Therefore:
- original curly-quote segments: 3718
- semantic spoken-dialogue candidates: 3715
- inline non-spoken overrides: 3

Drive authority: `82_B03_SEGMENT_SEMANTIC_OVERRIDES_v1.json`.

## Audit finding
A full comparison of the previous Tier-4 map against strong local syntactic evidence found **77 direct contradictions**.

Root cause: paragraph-start narration and next-speaker setup were sometimes treated as though they were post-speech tags for the preceding quote. This is invalid in this manuscript style.

## Rebuild law
The new base accepts only strong local evidence:
1. immediate pre-quote direct attribution such as `Jana said, “…”`;
2. same-paragraph post-quote tag such as `“…” Jana said.`;
3. post-tag pronoun only where the nearest named antecedent is gender-consistent and locally unambiguous;
4. paragraph-start narration is never treated as a post-tag;
5. alternating-turn inference is forbidden;
6. conflicts and weak contextual cases remain `UNKNOWN`.

## Rebuild result
- semantic spoken candidates: **3715**
- strong assignments: **502**
- UNKNOWN: **3213**
- strong-map coverage: **13.51%**
- direct contradictions found in previous Tier-4: **77**
- FATAL story/text changes: **0**

Drive full rebuild: `83_B03_SPEAKER_ATTRIBUTION_REBUILD_STRONG_v1.json` — Drive ID `1cFXTf1l4Avo2pjIvGNyb1rjdg3pHLlL6`.

Drive audit report: `84_B03_SPEAKER_ATTRIBUTION_AUDIT_REPORT_v1.json` — Drive ID `1tQpp0qj56Ot3vGp7HDAaWfQVdtqN7-4T`.

## Supersession
`78_B03...Tier1`, `79_B03...Tier2`, `80_B03...Tier3`, and `81_B03...Tier4` are retained for provenance only and **must not feed a voice map**.

## Universal learning
Two reusable audio-production rules are promoted as engineering safeguards:

`QUOTE_BOUNDARY != SPOKEN_DIALOGUE`

A segmentation system may preserve quote boundaries without asserting that every quoted token is a separately spoken utterance.

`PARAGRAPH_START_NARRATION != POST_SPEECH_TAG`

When a quote ends and the next narration begins a new paragraph, a later `X said/asked/...` construction may introduce the next speaker and must not be attributed backward to the preceding quote.

## Next gate
Build a contextual evidence queue from the 3213 UNKNOWN spoken candidates. Promote only cases with independent textual evidence. Preserve UNKNOWN where unresolved. Do not start voice locking until the current attribution layer is provenance-clean.
