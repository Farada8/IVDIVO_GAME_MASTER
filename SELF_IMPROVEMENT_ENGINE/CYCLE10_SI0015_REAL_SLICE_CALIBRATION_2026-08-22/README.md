# Cycle10 — SI-0015 real project-slice calibration

Status: REAL PROJECT / SOURCE-GROUNDED ENGINEERING PILOT. Authority effect: NONE.

This pilot reuses the existing merged classifier `tools/si0015_project_slice_freshness_canary.py`; it does not create a second freshness engine.

## Corpus
20 source-grounded slices across D01, D04, D09 and D10, derived from current router/project-state files and exact blob identities.

Key real finding: `CURRENT_IVDIVO_SYSTEM_STATE.json` still embeds D01 as active E96/working-branch state, but its pointed old execution file is explicitly `SUPERSEDED_ARCHIVE_POINTER` and the controlling D01 state is Founder-locked E01-E120. SI-0015 therefore correctly classifies this as `STALE_CURRENT_SLICE`.

Other controls include current D10/D04 matches, a real D09 Founder-approval-missing state, and D01 historical/superseded references that must remain exempt rather than become false positives.

## Result
- fixtures: 20
- expected/observed matches: 20/20
- false positives in this bounded corpus: 0
- false negatives in this bounded corpus: 0

## Critical evidence boundary
Expected labels were source-hierarchy adjudicated in this engineering pass, not independently human-reviewed. Therefore this is stronger than synthetic canaries but is not independent Human Signal and does not authorize SI-0015 promotion.

Next gate: independent/manual expected-label review plus telemetry from real routing use; repair the proven D01 stale central-router slice through the normal freshness/rebase transaction rather than by changing the classifier.
