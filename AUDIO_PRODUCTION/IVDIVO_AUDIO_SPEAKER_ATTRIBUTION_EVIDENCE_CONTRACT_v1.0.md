# IVDIVO AUDIO — SPEAKER ATTRIBUTION EVIDENCE CONTRACT v1.0

**Status:** ENGINEERING SAFEGUARD — DERIVED FROM B03 PRODUCTION FAILURE  
**Date:** 2026-08-22

## Purpose
Prevent voice-map contamination by plausible but unsupported speaker guesses in audiobooks, audio drama and TTS preparation.

## Hard laws

### 1. QUOTE_BOUNDARY != SPOKEN_DIALOGUE
A quoted span may be an inline term, label, remembered wording, display text or other non-spoken content. Quote-boundary segmentation preserves bytes; semantic speech classification is a separate gate.

### 2. PARAGRAPH_START_NARRATION != POST_SPEECH_TAG
A later `X said/asked/...` in a new paragraph may introduce the next speaker. It must not be attributed backward to the previous quote merely because it is the nearest speech verb.

### 3. UNKNOWN_IS_VALID_OUTPUT
When speaker evidence is insufficient or conflicting, emit `UNKNOWN`. Do not force complete voice binding by guessing.

### 4. SPEAKER_HEURISTIC_MUST_BE_VALIDATED_BEFORE_AUTO_PROMOTION
A contextual heuristic must be measured against an independent strong-label set from the production corpus before it can assign speakers automatically.

Plausibility, narrative expectation or a handful of attractive examples are not validation.

### 5. NO_ALTERNATING_TURN_AUTO_INFERENCE
B03 validation: alternating-turn heuristic was correct only 5/27 = 18.52% on strong-label controls. It is prohibited for automatic assignment.

### 6. NO_SAME_SPEAKER_SANDWICH_AUTO_INFERENCE
B03 validation: same-speaker anchor sandwich was correct 0/5 on strong-label controls. It is prohibited for automatic assignment.

### 7. ACTION_SUBJECT_IS_REVIEW_SIGNAL_NOT_SPEAKER_PROOF
B03 validation: single-action-subject heuristic was correct 29/49 = 59.18%. It may rank a manual review queue but cannot bind a voice automatically at this evidence quality.

### 8. SMALL_PERFECT_SAMPLE = HOLD
A perfect result on a tiny sample does not authorize an automatic rule. B03 `NO_PARAGRAPH_BREAK` observed 2/2 and remained HOLD.

## Evidence classes
`STRONG_LOCAL_SYNTACTIC` — eligible for automatic attribution when the parser contract itself is regression-tested.

`MANUAL_LOCAL_ADJUDICATION` — accepted individual assignment with explicit preserved context; does not promote a general rule.

`REVIEW_SIGNAL` — ranks attention only; does not assign.

`UNKNOWN` — unresolved and valid.

## Required provenance per assignment
- immutable segment id;
- exact quote reference;
- evidence class;
- local pre/post context or locator;
- parser/rule version or manual adjudication id;
- confidence is not a substitute for evidence class;
- no source-text mutation.

## Voice-map gate
A voice map may consume only the current provenance-clean attribution authority. Superseded speaker maps remain provenance only.

Do not lock voices merely because some percentage of the corpus has speaker labels. Unresolved recurring/major-character dialogue must be surfaced explicitly before scaled rendering.

## B03 failure evidence
The earlier Tier1–Tier4 pipeline reached an apparent 856/3718 mapping, but later audit found direct contradictions with immutable narration. The pipeline was superseded rather than patched forward.

Current B03 conservative architecture demonstrates the required response:
`AUDIT -> INVALIDATE UNSAFE MAP -> REBUILD STRONG BASELINE -> VALIDATE HEURISTICS -> KEEP UNKNOWN -> MANUAL EVIDENCE BATCHES -> ONLY THEN VOICE MAP`.

## Generalization boundary
The numerical B03 heuristic accuracies are corpus evidence, not universal language statistics. The universal promotion is the safeguard: test contextual rules before automatic speaker binding and preserve UNKNOWN when evidence is inadequate.
