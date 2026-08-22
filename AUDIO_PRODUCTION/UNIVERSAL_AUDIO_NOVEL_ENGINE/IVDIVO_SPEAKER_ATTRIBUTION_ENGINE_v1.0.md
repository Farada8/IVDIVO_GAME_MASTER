# IVDIVO — SPEAKER ATTRIBUTION ENGINE v1.0

**Status:** ENGINEERING RUNTIME / FAIL-CLOSED  
**Date:** 2026-08-22

## Purpose

Convert exact-text dialogue segmentation into provenance-bearing speaker assignments without guessing. The engine operationalizes the existing `IVDIVO_SPEAKER_ATTRIBUTION_EVIDENCE_CONTRACT_v2.md`; it does not replace that contract.

## Core laws

1. `UNKNOWN` is a valid production result.
2. Exact source text is immutable.
3. Quote boundary is not automatically spoken dialogue.
4. Direct grammatical speech tags are preferred to contextual inference.
5. A known name mentioned inside a reporting clause is not automatically its grammatical subject. Example regression: `The caller on Nika’s line said` must not become Nika merely because Nika is the only configured alias.
6. Contextual rules cannot become AUTO merely because they improve coverage.
7. Project-promoted rules remain project-scoped until independent second-project replication.
8. Role-label compatibility is not voice-identity equivalence.

## Runtime

`tools/ivdivo_speaker_attribution.py`

The runtime provides one-sided direct tags, conservative pronoun review, project-gated grammatical-subject tracking, project-gated same-paragraph propagation, semantic non-spoken overrides, Wilson-bound promotion gates and fail-closed conflict handling.

## Promotion lifecycle

`OBSERVED -> VALIDATED -> PROJECT_AUTO -> CROSS_PROJECT_REPLICATION -> UNIVERSAL_AUTO`

Default project promotion gate: `n >= 30`, precision `>= 0.98`, Wilson 95% lower bound `>= 0.90`.

## B03 evidence

The current reconciled candidate combines corrected-v2 authority with the fixed runtime delta and reaches **599 / 3715** assignments while preserving **3116 UNKNOWN**, **0 story-text changes**, and no voice-map authorization.

The CH01 regression `The caller on Nika’s line said, “The passenger door’s jammed.”` is retained permanently. The generic parser must not assign Nika from that modifier mention; independent CH01 authority identifies the actual role as the real collision caller.

## Generalization boundary

B03 project-promoted same-paragraph and grammatical-subject rules are not yet universal. They require independent second-book replication before cross-project promotion.
