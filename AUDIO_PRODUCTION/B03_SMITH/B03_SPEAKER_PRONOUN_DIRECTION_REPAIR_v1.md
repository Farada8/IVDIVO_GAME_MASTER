# B03 — SPEAKER PRONOUN-DIRECTION REPAIR v1

**Date:** 2026-08-22  
**Status:** PASS_2_LABEL_REPAIRS / NO_COUNT_CHANGE / NO_STORY_MUTATION  
**Story authority:** FOUNDER LOCKED / CH01–29

## Current baseline inspected

Drive `89_B03_SPEAKER_ATTRIBUTION_CURRENT_BASELINE_v1_3.json` — `1zAoXqX_mMsQNpMf4K2GeOEmwU_gzv1A2`

Baseline before repair:
- spoken candidates: 3715
- assigned: 517
- UNKNOWN: 3198
- coverage: 13.92%

## Defect class

The `POST_PRONOUN_RESOLVED` path may resolve a post-quote pronoun from a named character that appears only **after** the pronoun in the evidence window. This is backward coreference and can bind the preceding quote to the wrong voice.

A complete audit of the 42 current `POST_PRONOUN_RESOLVED` assignments found two such cases.

## Repairs

### B03_CH01_S0108
Current label: `NIKA`  
Correct label: `JANA`

Pre-quote narration: `Jana stood behind Nika now, arms folded.`  
Quote: `“Walk the gallery,”`  
Post-tag: `she said.`

The later text `Nika passed it on` cannot be used as the antecedent of the earlier `she`. Independent CH01 production speaker authority also maps this turn to JANA.

### B03_CH03_S0252
Current label: `NIKA`  
Correct label: `JANA`

Pre-quote narration: `Jana came to Nika’s desk.`  
Quote: `“What is Old Earth Security?”`  
Post-tag: `she asked.`

The later text `Nika looked at the three recordings` cannot resolve the preceding `she`. Local narration makes JANA the active speaker.

## New guard

`PRONOUN_ANTECEDENT_MUST_PRECEDE_PRONOUN`

Supporting invariant:

`FORWARD_NAMED_TOKEN != VALID_BACKWARD_ANTECEDENT`

and:

`ANTECEDENT_TOKEN_PROXIMITY != GRAMMATICAL_SPEAKER_OWNERSHIP`

## Regression controls

The repair does not disable valid post-pronoun attribution. Known valid controls include:
- `B03_CH01_S0076` → NIKA: preceding narration explicitly names Nika before `she asked`.
- `B03_CH03_S0154` → JANA: preceding narration ends with `Jana did not move` before `she asked`.

## Effective state after repair

- assigned: **517 / 3715**
- UNKNOWN: **3198**
- coverage: **13.92%**
- labels corrected: **2**
- assignment-count change: **0**
- story/prose byte changes: **0**
- voice map: **BLOCKED** until the attribution authority is provenance-clean

This repair is a narrow overlay on the current v1.3 baseline. It does not promote any contextual heuristic and does not consume the earlier 216 CH02–CH03 speaker proposals as authority.
