# IVDIVO AUDIO — SPEAKER ATTRIBUTION EVIDENCE CONTRACT v1.1

**Status:** ENGINEERING SAFEGUARD — CURRENT SUCCESSOR TO v1.0  
**Date:** 2026-08-22

## Purpose
Prevent voice-map contamination by plausible but unsupported speaker guesses in audiobooks, audio drama and TTS preparation.

## Hard laws

### 1. QUOTE_BOUNDARY != SPOKEN_DIALOGUE
Quoted spans may be terms, labels, remembered wording, display text or other non-spoken content. Byte segmentation and semantic speech classification are separate gates.

### 2. PARAGRAPH_START_NARRATION != POST_SPEECH_TAG
A later `X said/asked/...` in a new paragraph may introduce the next speaker and must not be attributed backward to the previous quote.

### 3. UNKNOWN_IS_VALID_OUTPUT
Insufficient or conflicting speaker evidence resolves to `UNKNOWN`, not a forced voice assignment.

### 4. SPEAKER_HEURISTIC_MUST_BE_VALIDATED_BEFORE_AUTO_PROMOTION
Contextual heuristics require measurement against independent strong labels before automatic assignment. Plausibility is not validation.

### 5. NO_ALTERNATING_TURN_AUTO_INFERENCE
B03 control precision was 5/27 = 18.52%. Alternation is prohibited for automatic assignment.

### 6. NO_SAME_SPEAKER_SANDWICH_AUTO_INFERENCE
B03 control precision was 0/5. Sandwich inference is prohibited for automatic assignment.

### 7. ACTION_SUBJECT_IS_REVIEW_SIGNAL_NOT_SPEAKER_PROOF
B03 control precision was 29/49 = 59.18%. It may rank review but cannot bind a voice automatically at this evidence quality.

### 8. SMALL_PERFECT_SAMPLE = HOLD
A perfect tiny sample does not authorize a rule. Example: B03 no-paragraph-break observed 2/2 and remained HOLD.

### 9. PRONOUN_ANTECEDENT_MUST_PRECEDE_PRONOUN
A post-quote pronoun such as `she said` or `he asked` may not resolve to a named token that occurs only **after** that pronoun in the evidence window.

Required directional invariant:

`FORWARD_NAMED_TOKEN != VALID_BACKWARD_ANTECEDENT`

A parser must search/validate antecedents in grammatical direction. Nearest-token distance across the pronoun boundary is not speaker ownership.

B03 production proof found two live violations in the then-current 517-assignment baseline:
- `B03_CH01_S0108`: NIKA -> JANA;
- `B03_CH03_S0252`: NIKA -> JANA.

Both are label repairs with zero story-text mutation and zero assignment-count change.

## Evidence classes

`STRONG_LOCAL_SYNTACTIC` — eligible for automatic attribution only under a regression-tested parser contract.

`MANUAL_LOCAL_ADJUDICATION` — accepted individual assignment with explicit preserved context; does not promote a general rule.

`REVIEW_SIGNAL` — ranks attention only; never assigns by itself.

`UNKNOWN` — unresolved and valid.

`REPAIR_OVERLAY` — corrects a proven bad label in an otherwise retained baseline without laundering the old label into downstream voice authority.

## Required provenance per assignment
- immutable segment id;
- exact quote reference;
- evidence class;
- local pre/post context or locator;
- parser/rule version or manual adjudication id;
- directionality proof for pronoun/coreference rules;
- confidence is not a substitute for evidence class;
- no source-text mutation.

## Required pronoun/coreference regression set
Every parser or rule capable of `POST_PRONOUN_RESOLVED` attribution must include:
1. a forward-token rejection case;
2. a valid preceding-antecedent acceptance case;
3. a case with multiple same-gender names where ambiguity remains UNKNOWN unless grammar/context resolves it;
4. a no-source-text-mutation assertion.

B03 seed fixtures:
- reject/repair `B03_CH01_S0108`;
- reject/repair `B03_CH03_S0252`;
- keep `B03_CH01_S0076` -> NIKA;
- keep `B03_CH03_S0154` -> JANA.

## Voice-map gate
A voice map may consume only current provenance-clean attribution authority plus explicit current repair overlays. Superseded speaker maps remain provenance only.

Do not lock voices merely because a percentage target has been reached. Unresolved recurring/major-character dialogue must be surfaced before scaled rendering.

## Generalization boundary
B03 numerical heuristic results are corpus evidence, not universal language statistics. The universal rules are the fail-closed safeguards: validate before automatic binding, respect grammatical direction, preserve UNKNOWN, and carry repairs forward explicitly.
