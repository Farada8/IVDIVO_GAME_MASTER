# B03 — SPEAKER ATTRIBUTION CONTEXTUAL PASS CH02–CH03 v2

**Date:** 2026-08-22  
**Project:** B03 / THE EMPTY RESCUE  
**Story state:** FOUNDER LOCKED / CH01–29  
**Text mutation:** 0  
**Source package SHA256:** `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`

## Why this pass exists

The fresh strong-local rebuild correctly rejected the earlier Tier1–Tier4 speaker maps, but its `POST_PRONOUN_RESOLVED` rule still admitted a directional error: a pronoun could be assigned from a named character that appears **after** the pronoun in the evidence window.

A full audit of all **42** strong-map post-pronoun assignments found **2 forward-antecedent violations**:

- `B03_CH01_S0108`: base `NIKA` → corrected `JANA`.
- `B03_CH03_S0252`: base `NIKA` → corrected `JANA`.

CH01 is independently adjudicated by the existing 142/142 production speaker map, so the first correction has an external-in-project ground truth. The CH03 correction is explicit in local narration. No story text changes were made.

New safeguard:

`PRONOUN_ANTECEDENT_MUST_PRECEDE_PRONOUN`

and additionally:

`ANTECEDENT_TOKEN_PROXIMITY != GRAMMATICAL_SPEAKER_OWNERSHIP`

## Contextual review law

This pass does **not** use automatic alternating-turn fill.

A line is assigned only when local evidence makes the speaker unique through a bounded combination of:
- named entry into a call/radio exchange;
- closed two-party channel;
- explicitly anchored scene role;
- direct question/answer ownership;
- uninterrupted same-speaker continuation;
- operational role ownership supported by narration.

If two present speakers could plausibly own a line, it remains `UNKNOWN`.

## CH02 — THE CALL THAT WORKS

- raw quote segments: 108
- inline non-spoken semantic quote: `B03_CH02_S0200`
- spoken candidates: **107**
- contextually assigned: **104**
- residual UNKNOWN: **3**
- same as corrected strong base: 5
- new contextual assignments: **99**
- conflicts with corrected strong base: **0**

Residual UNKNOWN:
- `B03_CH02_S0100`
- `B03_CH02_S0108`
- `B03_CH02_S0214`

These are deliberately not guessed because multiple locally present speakers can plausibly own them.

## CH03 — THE THIRD DEPLOYMENT

- spoken candidates: **127**
- contextually assigned: **126**
- residual UNKNOWN: **1**
- strong-base same after correction: 8
- corrected strong-base conflict: 1
- new contextual assignments: **117**

Residual UNKNOWN:
- `B03_CH03_S0140`

The line is operationally plausible for more than one locally active command speaker, so it remains unresolved.

## Whole-book composed state

Current strong base before this pass:
- assigned: 502
- UNKNOWN: 3213
- coverage: 13.51%

After the 2 bounded corrections and 216 new CH02/CH03 contextual assignments:
- assigned: **718 / 3715**
- UNKNOWN: **2997**
- coverage: **19.33%**
- story/prose byte changes: **0**

The count remains 502 across the two corrections because they replace wrong speaker labels rather than add lines.

## Authority disposition

- exact-text segmentation: unchanged / authority preserved
- earlier Tier1–Tier4 maps: superseded
- strong-local rebuild: retained as **base layer**, but must be composed with the pronoun-direction corrections
- CH02 contextual pass: PASS
- CH03 contextual pass: PASS
- full speaker-attribution gate: **OPEN**
- voice-map lock: **NOT AUTHORIZED**

## Next gate

`CONTEXTUAL_SPEAKER_ATTRIBUTION_CH04_CH29`

Do not start whole-book voice locking until residual attribution has a provenance-clean disposition. Preserve `UNKNOWN` instead of forcing complete coverage.
