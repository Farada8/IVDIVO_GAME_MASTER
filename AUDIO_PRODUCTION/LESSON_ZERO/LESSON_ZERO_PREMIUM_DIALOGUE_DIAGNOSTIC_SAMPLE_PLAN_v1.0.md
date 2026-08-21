# LESSON ZERO — PREMIUM DIALOGUE DIAGNOSTIC SAMPLE PLAN v1.0

**Status:** CURRENT DIAGNOSTIC PLAN — EXACT TEXT FIRST PASS  
**Established:** 2026-08-21  
**Purpose:** separate WRITING defects from PERFORMANCE / ADAPTATION / TRANSLATION defects before any global prose revision.  
**Source:** `LESSON_ZERO_BOOK_ONE_v0.17_READING_EDITION.pdf`.

## Selection principle

The sample must stress different dialogue regimes. It is not a highlight reel and must not select only scenes already known to work.

Target duration: **45–60 minutes** at realistic audiobook pace.

Programmatic page extraction of the current PDF gives this diagnostic set:

| Segment | PDF pages | Approx words | Function under test |
|---|---:|---:|---|
| CH01 `FRIDAY NIGHT CONTACT` | 2–7 | 1,412 | early five-person chemistry, Samir boundary, Ethan management, Aoife observation, banter/subtext |
| CH04 `LESSON ZERO` | 23–27 | 1,268 | institutional speech, group problem-solving, world/procedure without lecture |
| CH09 `THE FIVE` excerpt | 77–82 | 1,490 | public pressure, status, group differentiation, fast multi-speaker response |
| CH22 `NOT YOUR CALL` excerpt | 252–258 | 2,170 | intimate/friendship boundary conflict, emotional misalignment, listening and repair |
| CH32 `THE CHOICE THAT IS HIS` excerpt | 408–414 | 1,798 | later high-stakes decision, communication under uncertainty, earned character growth |

**Total:** ~8,138 words.  
Estimated duration: ~54 min at 150 wpm; ~49 min at 165 wpm, before additional dramatic pauses.

## Why these five

### CH01
Tests whether the ensemble feels like five people rather than one writer distributing dry intelligence. Contains a strong positive-control subtext exchange and the Ethan/Aoife `failing investment bank` test case.

### CH04
Tests whether institutional/worldbuilding dialogue remains action rather than documentation. Important because IVDIVO frequently uses procedural systems.

### CH09 excerpt
Tests group voice separation under public/status pressure and whether recurrent dry correction syntax spreads across speakers.

### CH22 excerpt
Tests the hardest category for LLM prose: two people who know each other well, are emotionally misaligned, and cannot simply state the correct theme. Performance must preserve hesitation, injury, resistance and incomplete repair.

### CH32 excerpt
Tests whether later philosophical/ethical stakes are embodied in choice and communication rather than delivered as thesis statements.

## Exact-text diagnostic law

First performance pass must preserve the manuscript verbatim.

No line rewrite, shortening, localization, joke replacement or exposition repair before listening evidence exists.

## Performance requirements

- distinct locked/provisional character identities;
- actors play objectives and listen to previous behavior;
- do not pre-plan each line as isolated emotional delivery;
- underplay witty lines; no `punchline voice` unless the character is intentionally performing;
- preserve interruption and silence logic;
- add overlap only where response mechanics justify it and exact words remain intelligible;
- characters doing physical tasks must sound physically occupied;
- teenage voices are not generic children;
- institutional adults are not robots;
- technical material is not sermonized;
- Foley/ambience restrained and below the diagnostic function;
- music minimal / absent under key dialogue-testing passages.

## Founder listening interface

Founder does not need an editorial report. While listening, mark moments with any of:

`BELIEVE`  
`DON'T BELIEVE`  
`BORING`  
`CONFUSING`  
`WRITER TALK`  
`PERFORMANCE WRONG`  
`STRONG`  
`WANT MORE`

A timestamp or rough phrase is sufficient.

## Post-listen classification

Every flagged moment must be classified independently as:

- `PERFORMANCE_DEFECT`
- `WRITING_DEFECT`
- `ADAPTATION_DEFECT`
- `TRANSLATION_DEFECT`
- `CONTEXT_REQUIRED`
- `NO_DEFECT`

Do not rewrite for `PERFORMANCE_DEFECT`.

## Text-only companion gate

Run the same sample through `19_HUMAN_SCENE_DIALOGUE_PROMPT_STACK_v1.0.md` with names blinded where useful. Compare model/editor flags to listening flags.

High confidence WRITING_DEFECT requires convergent evidence from the text behavior itself and/or repeated Human Signal after a credible performance.

## A/B repair

Only proven WRITING_DEFECT moments receive:
- A = current exact line/beat;
- B = smallest repair preserving story facts, clue order, character objective and relationship state;
- read-aloud rerender of affected local block;
- scene and chapter regression.

## Output artifacts

1. `LESSON_ZERO_DIALOGUE_DIAGNOSTIC_EXACT_TEXT_MAP_v1.json`
2. `LESSON_ZERO_DIALOGUE_DIAGNOSTIC_DIRECTOR_SCORE_v1.json`
3. performance blocks / voice binding references
4. diagnostic audio master
5. `LESSON_ZERO_FOUNDER_LISTENING_MARKERS_v1.json`
6. `LESSON_ZERO_TEXT_VS_PERFORMANCE_DIAGNOSIS_v1.json`
7. targeted repair list, if any
8. learning-registry delta for reusable defects only

## Stop / scale rule

Do not scale to the full 113k+ word book until this sample demonstrates:
- major voices are believable over time;
- character identities remain separable;
- technical/institutional dialogue stays human;
- no unresolved repeated MAJOR naturalism failure;
- Founder can listen without persistent `writer talk` breaks.

If the sample passes, scale audio production without reopening prose globally.
If it fails, repair the earliest proven layer and rerun only affected sample blocks.

**AUDIO IS A DIAGNOSTIC INSTRUMENT HERE, NOT AN EXCUSE FOR TEXT AND NOT A SUBSTITUTE FOR TEXT QUALITY.**
