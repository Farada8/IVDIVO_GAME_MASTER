# IVDIVO Speaker Attribution Engine v1.0

**Status:** IMPLEMENTED / LOCAL 18/18 PASS / EXACT-REPOSITORY CI REQUIRED  
**Authority:** `IVDIVO_SPEAKER_ATTRIBUTION_EVIDENCE_CONTRACT_v2.md`

## Role
Machine implementation of the fail-closed speaker-attribution contract used by audiobook/TTS production. It operates downstream of immutable quote-boundary segmentation and semantic speech classification.

Pipeline:
`EXACT TEXT -> QUOTE SEMANTIC CLASSIFICATION -> DIRECT SYNTACTIC EVIDENCE -> PROJECT-PROMOTED CONTEXT RULES -> CONFLICT=UNKNOWN -> PROVENANCE -> VOICE MAP`

## Universal hard laws
- `QUOTE_BOUNDARY != SPOKEN_DIALOGUE`.
- `UNKNOWN > GUESS`.
- New paragraph is an evidence barrier unless syntax explicitly proves otherwise.
- Conflicting candidates return no assignment.
- Exact source text is never mutated.
- Contextual rules require measured promotion; coverage alone never promotes a rule.

## Rule scopes
### Universal machine rules
`PRE_DIRECT_TAG` and `POST_DIRECT_TAG`: explicit named/role grammatical speech tags. Longest alias wins over nested generic roles. These remain fail-closed if more than one speaker survives parsing.

### B03 project-promoted only
`AUTO_SAME_PARAGRAPH_KNOWN_SPEAKER_PROPAGATION`: promotion evidence 36/36, precision 1.000, Wilson 95% lower 0.9036.

`AUTO_PRONOUN_GRAMMATICAL_SUBJECT_TRACKER`: promotion evidence 36/36, precision 1.000, Wilson 95% lower 0.9036. Tracks grammatical subject rather than nearest name; object mentions do not replace subject.

These are **not universal** until a second independent book replicates them.

### Review-only / forbidden auto
- standalone prior-paragraph attribution: 42/43, Wilson 0.8794 -> REVIEW_ONLY.
- single action subject: 29/49 -> REVIEW_ONLY.
- alternating turn: 5/27 -> FORBIDDEN_AUTO.
- same-speaker sandwich: 0/5 -> FORBIDDEN_AUTO.
- nearest-name/gender-only pronoun binding -> REVIEW_ONLY / fail closed on ambiguity.

## B03 current project evidence
After semantic overrides, B03 has 3715 spoken-dialogue candidates. Current provenance-clean baseline after project-promoted runtime expansion: 661 assigned / 3054 UNKNOWN = 17.79%. No story-text changes. Voice-map remains blocked because unresolved dialogue is still material.

## Promotion threshold
Default contextual-rule gate: `n >= 30`, precision `>= 0.98`, Wilson 95% lower bound `>= 0.90`, zero known fatal regression conflicts. A project promotion remains project-scoped until independent replication.

## Runtime
`tools/ivdivo_speaker_attribution.py`

## Tests
`tests/test_ivdivo_speaker_attribution.py`

## Next gate
1. exact-repository CI;
2. independent second-book replication of B03 project rules;
3. only then consider universal promotion;
4. voice-map remains downstream and may consume only provenance-clean assignments.
