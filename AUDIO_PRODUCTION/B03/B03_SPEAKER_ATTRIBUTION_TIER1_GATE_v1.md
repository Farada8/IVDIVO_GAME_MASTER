# B03 — THE EMPTY RESCUE — SPEAKER ATTRIBUTION TIER 1 GATE v1

**SUPERSEDED / REJECTED FOR SPEAKER AUTHORITY — 2026-08-22**

This historical gate claimed 653 Tier-1 explicit assignments. A later boundary-ownership Red Team found **70 direct speaker conflicts** on overlapping assignments and showed that attribution evidence could be reused across adjacent quote boundaries. Therefore `TIER1_EXPLICIT_ATTRIBUTION = PASS` from this v1 document is withdrawn.

## Historical input
- Story state: FOUNDER LOCKED / RELEASE READY.
- Input: `77_B03_EXACT_TEXT_SEGMENTATION_PACKAGE_v1.0.zip`.
- Input SHA256: `4f7f779fc42007f384512cb1e1cef84a98ef0c0756f010404a835e204e05c0ac`.
- Text mutation: none.

## Reconciliation result
- historical v1 assignments: 653
- corrected strict one-sided Tier-1 assignments: **471**
- common IDs: 440
- same speaker: 370
- direct conflicts: **70**
- v1-only assignments: 213
- corrected-only assignments: 31
- narrator-inline semantic quote exceptions: 3
- actual dialogue spans after semantic quote classification: 3,715

Root cause: a speech tag belonging to the next quote could capture the preceding quote. Corrected rule: a POST tag owns only the quote immediately before it; a PRE speech-intro owns only the quote immediately after it; the same evidence is never reused bidirectionally.

## Current authority
Do not use this v1 map as speaker authority.

Current reconciliation: `AUDIO_PRODUCTION/B03/B03_SPEAKER_ATTRIBUTION_RECONCILIATION_v2.md`.
Current private whole-book map: `110_B03_SPEAKER_ATTRIBUTION_TIER2_REBASED_v2.json`, Drive `1px9HoDaBujFK1iJ0NiyQ1bRgvI5GHoS1`.
Current gate: Drive `1W6TluQh58BDju0C5-IMSVJETiBJLvoJS`.

`TIER1_V1 = REJECTED / SUPERSEDED`
`CURRENT_TIER1_STRICT = 471`
`FULL_SPEAKER_ATTRIBUTION_GATE = OPEN`
