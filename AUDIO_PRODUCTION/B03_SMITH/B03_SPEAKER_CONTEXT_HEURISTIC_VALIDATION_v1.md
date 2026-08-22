# B03 — SPEAKER CONTEXT HEURISTIC VALIDATION v1

**Date:** 2026-08-22  
**Project:** B03 / THE EMPTY RESCUE  
**Status:** PASS_EVALUATION / NO_CONTEXT_HEURISTIC_AUTO_PROMOTED

## Current strong baseline
Authoritative conservative rebuild:
`85_B03_SPEAKER_ATTRIBUTION_REBUILD_STRONG_v1_2.json`

- semantic spoken candidates: **3715**
- strong assignments: **512**
- UNKNOWN: **3203**
- strong coverage: **13.78%**
- conflicts in strong layer: **0**
- previous Tier-4 contradictions detected by refined audit: **79**

The exact locked prose is unchanged.

## Validation law
A contextual rule may not enter automatic speaker attribution because it sounds plausible. It must first be tested against independent strong-label cases from the same production corpus.

`PLAUSIBLE_HEURISTIC != VALIDATED_ATTRIBUTION_RULE`

`UNKNOWN > UNSUPPORTED_SPEAKER_GUESS`

Small perfect samples are HOLD, not PASS.

## Tested contextual heuristics

### R1 — NO_BREAK_NO_SPEECHVERB
Test coverage: **n=0**.  
Disposition: `HOLD_NO_TEST_COVERAGE`.

### R1B — NO_PARAGRAPH_BREAK
Test coverage: **2/2 correct = 100%**.  
95% Wilson lower bound ≈ **34.24%** because the sample is only two cases.  
Disposition: `HOLD_INSUFFICIENT_SAMPLE` — no auto assignment.

### R2 — SAME_SPEAKER_SANDWICH
Test coverage: **0/5 correct = 0%**.  
Disposition: `REJECT_AUTO`.

Same-speaker anchors on both sides do not prove that an unlabelled middle quote belongs to the same speaker in this manuscript.

### R3 — SINGLE_ACTION_SUBJECT
Test coverage: **29/49 correct = 59.18%**.  
95% Wilson lower bound ≈ **45.25%**.  
Disposition: `REVIEW_ONLY_REJECT_AUTO`.

An action subject may be a useful review signal but is not reliable enough to bind a voice automatically.

### R4 — ALTERNATION
Test coverage: **5/27 correct = 18.52%**.  
95% Wilson lower bound ≈ **8.18%**.  
Disposition: `REJECT_AUTO`.

Alternating-turn inference is empirically unsafe in this corpus and is forbidden for automatic speaker attribution.

## Current automatic layer
Only strong local syntactic evidence remains eligible:
- PRE_DIRECT_TAG;
- POST_DIRECT_TAG within the same paragraph;
- POST_PRONOUN_RESOLVED with local gender-consistent unambiguous antecedent;
- PRE_STANDALONE_NEW_PARAGRAPH_EXACT when the new paragraph is an exact standalone speech introduction.

Method counts in v1.2:
- PRE_DIRECT_TAG: 358
- POST_DIRECT_TAG: 102
- POST_PRONOUN_RESOLVED: 42
- PRE_STANDALONE_NEW_PARAGRAPH_EXACT: 10
- total: **512**

## Universal safeguards promoted from this failure
1. `SPEAKER_HEURISTIC_MUST_BE_VALIDATED_BEFORE_AUTO_PROMOTION`.
2. `UNKNOWN_IS_VALID_OUTPUT`.
3. `NO_ALTERNATING_TURN_AUTO_INFERENCE`.
4. `NO_SAME_SPEAKER_SANDWICH_AUTO_INFERENCE`.
5. `ACTION_SUBJECT_IS_REVIEW_SIGNAL_NOT_SPEAKER_PROOF` at current evidence quality.
6. `QUOTE_BOUNDARY != SPOKEN_DIALOGUE`.
7. `PARAGRAPH_START_NARRATION != POST_SPEECH_TAG`.

## Production disposition
Speaker gate remains **PARTIAL**. Voice-map/voice-lock is **not authorized** from 13.78% strong coverage.

Next obligation:
`BUILD_HIGH_INFORMATION_UNKNOWN_REVIEW_QUEUE -> ADJUDICATE_WITH_EXPLICIT_EVIDENCE -> REVALIDATE_ANY_NEW_RULE -> PRESERVE_UNKNOWN_WHERE_UNRESOLVED`.

No story rewrite. No exact-text byte mutation. No voice guessing.
