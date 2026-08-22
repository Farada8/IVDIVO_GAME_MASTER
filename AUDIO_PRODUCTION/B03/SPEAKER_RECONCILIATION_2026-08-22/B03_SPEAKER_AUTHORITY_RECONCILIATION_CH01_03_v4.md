# B03 — SPEAKER AUTHORITY RECONCILIATION CH01–03 v4

**Status:** **PASS CH01–03 / 376 OF 376 / UNKNOWN 0 / EXACT TEXT UNCHANGED**  
**Date:** 2026-08-22  
**Story authority:** FOUNDER LOCKED CH01–29

## Current authority

- CH01: protected production map `77_B03_AUDIO_EXACT_TEXT_SEGMENTATION_CH01_v1.json` — **142/142**.
- CH02: corrected contextual authority v3 — **107/107**.
- CH03: corrected contextual authority v1 — **127/127**.
- Total CH01–03: **376/376 (100%)**.
- Exact-text changes: **0**.

## What was rejected/superseded

### Whole-book strong rebuilds
They remain diagnostic, not voice-map authority. Demonstrated failure:
`Jana stood behind Nika now, arms folded. “Walk the gallery,” she said.`
Nearest-name resolver assigned Nika; correct speaker is Jana. Artifact 113 independently confirms this root cause.

### CH01–03 context batch v0.3
Superseded:
- CH01: **2** Nika/Jana swaps.
- CH02: **5** wrong assignments.
- CH03: **3** UNKNOWN turns were resolvable from scene-entry boundary.

### CH02 112 rebased v2
Useful but not final:
- **5 wrong assignments** remained.
- `B03_CH02_S0108` remained UNKNOWN though contextual ownership is sufficiently bounded.

## CH02 six corrections from 112 v2

1. `S0034` → FLAGGED_HAZARD_CALLER: warning occurs before `The line ended`; Nika's bus-control call starts afterward.
2. `S0108` → JANA: Jana asks road-load question; supervisor answers; `Agreed. Close it.` closes that exchange; Nika then handles bus control.
3. `S0190` → ANDREJ: preceded by `His tone changed...`.
4. `S0192` → NIKA: answers Andrej's `What happened?`.
5. `S0194` → ANDREJ: asks `How far before?`.
6. `S0198` → ANDREJ: follows explicit Nika line and `Andrej was silent for a moment.`

## CH03 three resolutions

`S0240`, `S0244`, `S0248` → NIKA_ZUPAN.

Reason: all occur inside the Nika–technician exchange. Only after them does narration state:
`Jana came to Nika’s desk.`

This is scene-entry evidence, not turn alternation.

## Engineering decision

Global auto-attribution remains **FAIL-CLOSED / DIAGNOSTIC ONLY**.
Production authority is chapter-local until the full book is re-audited.
Coverage never outranks correctness.

**Next gate:** re-audit existing CH04–06 context batch v0.3 using Evidence Contract v2; do not promote it because of its headline coverage alone.
