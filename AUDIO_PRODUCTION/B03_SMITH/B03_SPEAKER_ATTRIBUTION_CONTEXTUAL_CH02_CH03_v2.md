# B03 — SPEAKER ATTRIBUTION CONTEXTUAL CH02–CH03 — FRESH-MAIN RECONCILIATION v2.1

**Date:** 2026-08-22  
**Project:** B03 / THE EMPTY RESCUE  
**Story state:** FOUNDER LOCKED / CH01–29  
**Text mutation:** 0  
**Voice-map lock:** NOT AUTHORIZED

## Fresh-main authority

While the CH02–CH03 contextual review was being prepared, `main` advanced to a newer strong baseline:

- spoken dialogue candidates: **3,715**
- strong assignments: **512**
- UNKNOWN: **3,203**
- coverage: **13.78%**
- strong conflicts: **0**
- prior Tier-4 contradictions detected: **79**
- Drive strong baseline: `85_B03_SPEAKER_ATTRIBUTION_REBUILD_STRONG_v1_2.json` — `1qX0_z-d_S-VuA18eos2nk3T0IGTNWoeN`

The associated contextual-heuristic validation promoted **no automatic contextual rule**. Alternation and same-speaker-sandwich inference are rejected for automatic use; single-action-subject is review-only; small perfect samples remain HOLD rather than PASS.

Drive validation: `86_B03_SPEAKER_CONTEXT_HEURISTIC_VALIDATION_v1.json` — `1BkUn_5tN6YnpVna40auSMePcwV3i7Lec`.

Therefore the earlier 502-base composition must not be promoted.

## New defect found inside the fresh 512 baseline

A complete audit of all **42** `POST_PRONOUN_RESOLVED` assignments found **2 directional antecedent violations**.

### `B03_CH01_S0108`
Current strong baseline: `NIKA`  
Corrected speaker: `JANA`

The local evidence is `Jana stood behind Nika now...` followed by the quote and `she said.` The strong rule incorrectly resolves `she` to the later `Nika` mention. The existing independently adjudicated CH01 production map also assigns this turn to JANA.

### `B03_CH03_S0252`
Current strong baseline: `NIKA`  
Corrected speaker: `JANA`

The local narration explicitly places Jana as the acting speaker before the quote. The later Nika mention cannot serve as a backward antecedent for the preceding `she asked`.

New generic safeguard:

`PRONOUN_ANTECEDENT_MUST_PRECEDE_PRONOUN`

Supporting law:

`ANTECEDENT_TOKEN_PROXIMITY != GRAMMATICAL_SPEAKER_OWNERSHIP`

These are label corrections only. Strong assignment count remains **512**; story/prose bytes remain unchanged.

## CH02–CH03 contextual work: disposition changed

The earlier contextual review generated **216 candidate speaker proposals** from the current UNKNOWN pool. Fresh-main heuristic validation requires a stricter disposition:

- candidate proposals: **216**
- automatically promoted: **0**
- status: **REVIEW_QUEUE_ONLY / NOT SPEAKER AUTHORITY**
- four deliberately unresolved lines remain unproposed:
  - `B03_CH02_S0100`
  - `B03_CH02_S0108`
  - `B03_CH02_S0214`
  - `B03_CH03_S0140`

The proposed labels are useful as a review queue, not as a voice map. Each candidate must acquire independent per-line evidence before promotion. Closed-channel membership or apparent turn alternation alone is insufficient.

## Current working state

After applying only the two proof-backed corrections:

- assigned: **512 / 3,715**
- UNKNOWN: **3,203**
- coverage: **13.78%**
- text mutation: **0**
- contextual auto-promotion from this pass: **0**
- full speaker-attribution gate: **OPEN**
- voice map: **BLOCKED**

## Next gate

`ADJUDICATE_CONTEXTUAL_QUEUE_WITH_PER_LINE_EVIDENCE_CH02_CH03`

Then continue:

`CONTEXTUAL_SPEAKER_ATTRIBUTION_CH04_CH29`

Promotion law:

`PROPOSED_SPEAKER != AUTHORITATIVE_SPEAKER`

and:

`UNKNOWN > UNSUPPORTED_COMPLETENESS`

No whole-book voice locking until speaker attribution has a provenance-clean disposition.
