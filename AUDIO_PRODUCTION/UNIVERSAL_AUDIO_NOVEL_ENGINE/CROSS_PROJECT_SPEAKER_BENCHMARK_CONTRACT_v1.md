# CROSS-PROJECT SPEAKER BENCHMARK CONTRACT v1

Date: 2026-08-22
Status: `VERIFICATION_CONTRACT_CURRENT`
Applies to: candidate speaker-attribution rules seeking promotion from project-local to universal automatic use.

## 1. Purpose

This contract prevents project-local success, tiny perfect samples, synthetic duplication, circular labelling, or adapted-script convenience from being misreported as universal speaker-attribution evidence.

A rule may be useful inside one project without being universal. Promotion requires materially independent evidence.

## 2. Admissible benchmark corpus

A corpus is admissible only when all of the following are true:

1. **Immutable source** — the literary source is locked/frozen and identified by version plus cryptographic hash where available.
2. **Material independence** — the corpus is not B03 and was not authored or rewritten to create favourable rule triggers after seeing candidate predictions.
3. **Natural prose surface** — the evaluated text contains ordinary prose/dialogue structure. A screenplay or production script whose speaker labels directly expose the answer does not by itself test natural-prose attribution.
4. **Independent ground truth** — speaker ownership was established independently of the candidate rule output, for example by pre-existing production annotation or a separately performed human adjudication.
5. **Pre-score freeze** — candidate quote/segment IDs and inclusion/exclusion rules are frozen before accuracy is scored.
6. **No self-labelling** — model/engine predictions cannot be copied into the answer key and then used as validation evidence.
7. **No synthetic multiplication** — duplicated, paraphrased, mechanically varied, or generated examples cannot be used to manufacture sample size.
8. **Traceable provenance** — source identity, version, hashes, ground-truth artifact, runtime/commit and scoring date are recorded.

## 3. Per-rule promotion gate

Each candidate rule is scored independently. Aggregate success across multiple rules cannot satisfy another rule's sample requirement.

Default gate:

- triggered examples `n >= 30`;
- precision `>= 0.98`;
- Wilson 95% lower confidence bound `>= 0.90`.

All three conditions are conjunctive.

### Critical statistical boundary

`min_n = 30` is only a nominal floor, not an automatic PASS threshold.

With perfect observed precision:

- `30/30` -> Wilson 95% lower ≈ `0.8865` -> **FAIL**;
- `34/34` -> Wilson 95% lower ≈ `0.8985` -> **FAIL**;
- `35/35` -> Wilson 95% lower ≈ `0.9011` -> **PASS**.

Therefore, under the current Wilson threshold, the first mathematically possible perfect-sample PASS is `35/35`. Any errors can require a larger sample or make promotion impossible at that sample size.

The runtime function `rule_auto_promotable()` is the executable authority for this conjunction; the nominal `min_n` must never be interpreted alone.

## 4. Mapping and ambiguity law

Adaptations may merge, split, translate, omit, or reorder literary utterances. Such transformations can be used only when speaker ownership for the original evaluated boundary remains unambiguous.

Before scoring, every candidate is assigned exactly one disposition:

- `SCORABLE_MATCH` — original boundary maps unambiguously to independent speaker truth;
- `EXCLUDE_MAPPING_AMBIGUOUS` — adaptation/production mapping does not uniquely preserve ownership;
- `EXCLUDE_NON_SPOKEN` — quote-like material is not actual cast speech;
- `EXCLUDE_SOURCE_MISMATCH` — source versions differ materially at the candidate;
- `EXCLUDE_GROUND_TRUTH_NOT_INDEPENDENT` — answer key is circular or derived from candidate output.

Excluded cases do not count toward `n` and their exclusion reason must be frozen before score calculation.

## 5. Anti-cherry-pick protocol

The benchmark must enumerate **all triggers of the candidate rule in the frozen evaluation scope**, not a favourable subset.

Permitted scope examples:

- one entire locked chapter;
- a predeclared chapter range;
- an entire locked book.

Forbidden:

- selecting only correct-looking predictions after execution;
- discarding hard cases because they reduce precision;
- extending the corpus only until the gate happens to pass without recording sequential testing decisions.

If the scope is expanded, preserve the earlier frozen result as a prior evidence stage.

## 6. Change-control and regression

If attribution runtime behaviour changes after a benchmark is frozen:

1. record the old runtime commit/hash;
2. rerun existing semantic regression fixtures;
3. rerun the frozen benchmark with the new runtime;
4. compare prediction deltas;
5. require warm regression on the development project and cold regression on the independent project before promotion.

A code change invalidates any claim that only the old runtime was tested.

## 7. Promotion states

Allowed states:

- `PROJECT_LOCAL` — usable only in the validated project;
- `SECOND_PROJECT_PARTIAL_EVIDENCE` — correct independent examples exist but gate is not met;
- `HOLD_SAMPLE_SIZE` — insufficient independent triggers / confidence;
- `HOLD_PRECISION` — precision below threshold;
- `HOLD_WILSON` — confidence lower bound below threshold;
- `REJECTED_CROSS_PROJECT` — replicated evidence demonstrates unacceptable error;
- `UNIVERSAL_CANDIDATE_PASS` — all statistical and provenance gates pass but release/write-through is not yet complete;
- `UNIVERSAL_VERIFIED_CURRENT` — exact-head CI, registry/state write-through and main readback complete.

No automatic rule changes from project-local to universal merely because a second project contains some correct examples.

## 8. Current application: Lesson Zero CH01

Current second-book evidence for the B03-only rules is intentionally retained as partial evidence:

- `PRONOUN_GRAMMATICAL_SUBJECT_TRACKER`: `1/1`, Wilson lower `0.2065`;
- `SAME_PARAGRAPH_KNOWN_SPEAKER_PROPAGATION`: `2/2`, Wilson lower `0.3424`.

This is positive portability evidence but nowhere near promotion evidence. Both rules remain `PROJECT_B03 / AUTO_PROJECT_ONLY`.

Reference: `LESSON_ZERO_CH01_SPEAKER_RULE_REPLICATION_v1.md`.

## 9. Claim boundary

This contract governs evidence and promotion. It does **not** authorize:

- scaled voice-map generation;
- provider dispatch;
- voice ID assignment;
- story/text rewriting;
- reporting production contextual ownership as deterministic engine verification.

Current B03 deterministic engine authority remains `599/3715`; production contextual speaker ownership is a separate authority surface.
