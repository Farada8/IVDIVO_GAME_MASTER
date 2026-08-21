# SOURCE ADEQUACY GATE v0.2

**Status:** WORKING / REAL-PILOT EVIDENCE / NOT GLOBAL AUTHORITY.

## Law
A validator may only interpret a missing field as missing story data when the selected source class is expected to carry that field.

Summaries/profiles such as `ROUTING_STATE`, `FINAL_GATE_SUMMARY`, `PARTIAL_AUTHORITY_SUMMARY`, and `SEASON_BIBLE_CHARACTER_PROFILE` may legitimately omit architecture/corpus detail. Missing required fields on these source roles return:

`INSUFFICIENT_SOURCE_NOT_STORY_DEFECT`

rather than a FATAL/MAJOR finding or permission to reopen prose.

## Proof
- D01 routing state lacked most Story Core fields but its text is Final Story Gate PASS; source inadequacy correctly prevented false reopening.
- D10 Final Gate summary lacked wrong-strategy/midpoint/climax detail; Season Bible + Causal Grid subsequently supplied enough evidence to pass those gates.
- D10 Season Bible character profile still does not constitute a full ordinary-life ledger; ordinary-life coverage therefore remains HOLD rather than being invented.

## Evidence grades
Every adapter disposition should carry one of:
- `SOURCE_EXPLICIT`
- `SOURCE_EXPLICIT_PLUS_STRUCTURED_MAPPING`
- `DERIVED_INFERENCE_FROM_SOURCE_CAUSAL_CHAIN`
- `SOURCE_ADEQUACY_HOLD`

## Prohibition
Do not repair a book solely because a routing summary, final-gate summary, or partial profile omits information stored in another source class.
