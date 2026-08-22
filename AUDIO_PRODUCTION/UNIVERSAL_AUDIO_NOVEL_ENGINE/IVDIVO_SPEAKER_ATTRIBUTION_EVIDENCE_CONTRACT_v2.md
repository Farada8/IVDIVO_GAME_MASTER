# IVDIVO — SPEAKER ATTRIBUTION EVIDENCE CONTRACT v2

**Status:** ENGINEERING CONTRACT / FAIL-CLOSED  
**Date:** 2026-08-22  
**Triggered by:** B03 THE EMPTY RESCUE speaker-attribution defects

## Objective

Assign a dialogue segment to a production speaker only when text-local evidence supports ownership. Coverage is subordinate to correctness. UNKNOWN is a valid output.

## Evidence priority

### E1 — DIRECT TAG
Highest authority.
- `"..." Jana said.`
- `Jana said, "..."`
- equivalent direct reporting verbs where grammatical subject is explicit.

Hard rule: a tag belongs only to its syntactic quote. Never reuse the same tag backward and forward across adjacent quote boundaries.

### E2 — SAME-PARAGRAPH ACTION OWNERSHIP
Strong contextual evidence when a named character action is immediately followed by a quote in the same paragraph and no competing speaker is introduced.
Example proven in B03:
`Nika looked at the photographs again. “So the call saved them.”`

This outranks generic turn alternation.

### E3 — SCENE / CHANNEL ENTRY BOUNDARY
A speaker cannot own a local exchange before the text places that speaker in the scene/channel.
Example:
three questions to a technician occur before `Jana came to Nika’s desk`; those questions cannot be Jana's.

### E4 — NEGATIVE ANSWERABILITY
Narration such as `before Nika could answer` proves that the immediately preceding utterance was addressed to Nika and therefore was not Nika's.
Use only as exclusion evidence; combine with bounded local participant set to assign another speaker.

### E5 — BOUNDED CONTEXTUAL REVIEW
Human/contextual review may resolve a turn when:
- active participant set is textually bounded;
- scene/channel continuity is explicit;
- earlier/later E1–E4 anchors constrain ownership;
- no competing interpretation survives.

Record evidence block and confidence. This is not an alternating-turn autofill rule.

## Forbidden evidence shortcuts

1. **Nearest named antecedent alone.**
   Demonstrated failure:
   `Jana stood behind Nika now, arms folded. “Walk the gallery,” she said.`
   Nearest-name heuristic selects Nika incorrectly; discourse subject is Jana.

2. **Alternating-turn autofill.**
   A two-person conversation can contain consecutive lines by one speaker, interrupted actions, quoted playback, or scene re-entry.

3. **Character voice/style.**
   Vocabulary, tone, profession or likely attitude may support human reading but may not be sole authority.

4. **Gender-only pronoun resolution.**
   Multiple same-gender candidates require grammatical/discourse evidence.

5. **Role merging across unknown sources.**
   `PRECURSOR_CALLER_CH02` does not equal CH01 caller unless text/canon establishes identity.

6. **Paragraph-start narration treated as post-tag.**
   A new paragraph starts a new evidence scope unless syntax explicitly links it backward.

## Conflict protocol

When two mechanisms disagree:
- do not choose the higher-coverage engine;
- quarantine segment as UNKNOWN;
- preserve both evidence traces;
- run contextual review;
- record correction as a regression fixture.

## Regression fixtures from B03

- CH01 `Walk the gallery` → JANA_KOVAC.
- CH01 `Can I write coincidence and close it?` → JANA_KOVAC.
- CH01 following `No.` → NIKA_ZUPAN.
- CH02 `So the call saved them.` → NIKA_ZUPAN.
- CH02 `It gave us a reason...` → JANA_KOVAC.
- CH02 `That is a careful way to say yes.` → NIKA_ZUPAN.
- CH02 `It is the way I’m writing it.` → JANA_KOVAC.
- CH02 `What happened?` after `His tone changed...` → ANDREJ_KOSIR.
- CH03 technician questions before `Jana came to Nika’s desk` → NIKA_ZUPAN.

Any future attribution engine must pass these fixtures before promotion.

## Promotion gate

A speaker engine may become production authority only if:
- 0 known regression-fixture failures;
- 0 bidirectional tag reuse;
- 0 semantic quote misclassified as spoken dialogue;
- conflicts fail closed to UNKNOWN;
- chapter-local audit sample passes;
- no exact-text mutation occurs.

**Coverage percentage alone is never a promotion criterion.**
