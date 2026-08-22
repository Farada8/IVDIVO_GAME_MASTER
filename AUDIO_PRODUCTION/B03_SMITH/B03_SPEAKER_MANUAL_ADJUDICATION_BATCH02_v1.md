# B03 — SPEAKER MANUAL ADJUDICATION BATCH 02

**Date:** 2026-08-22  
**Status:** PASS_27_INDIVIDUAL_HIGH_INFORMATION_ASSIGNMENTS / NO_RULE_PROMOTION

## Input authority
Current baseline before batch: `89_B03_SPEAKER_ATTRIBUTION_CURRENT_BASELINE_v1_3.json` = **517 / 3715** assigned.

UNKNOWN review queue: `90_B03_UNKNOWN_SPEAKER_HIGH_INFORMATION_REVIEW_QUEUE_v1_1.json`.

## Method
Twenty-seven high-information UNKNOWN segments were adjudicated individually from preserved exact local context. Evidence classes included:
- explicit same-paragraph continuation with a locally resolved speaker;
- named channel/radio entry with unambiguous speaking subject;
- role-bound speech where the grammatical subject and speech act coincide;
- locally resolved pronoun/coreference with no competing antecedent;
- self-reference or response context that uniquely identifies the speaker when corroborated by local narration.

No generic contextual heuristic was promoted. Alternating-turn inference, same-speaker sandwich inference and single-action-subject auto assignment remain prohibited.

## Result
- assignments before batch: 517
- manual adjudications added: **27**
- current assignments: **544**
- semantic spoken candidates: 3715
- remaining UNKNOWN: **3171**
- coverage: **14.64%**
- story text changes: 0
- exact-text byte changes: 0
- voice map authorized: **NO**

## Drive evidence
- Batch JSON: `91_B03_SPEAKER_MANUAL_ADJUDICATION_BATCH02_v1.json` — Drive ID `1RFNlUm4LrVDDrjkcWpgxQIGLghoQohwz`
- Current baseline: `92_B03_SPEAKER_ATTRIBUTION_CURRENT_BASELINE_v1_4.json` — Drive ID `1YtLq1LWMqusgipHkwzbzD18XgslMk0O0`
- Updated UNKNOWN review queue: `93_B03_UNKNOWN_SPEAKER_HIGH_INFORMATION_REVIEW_QUEUE_v1_2.json` — Drive ID `1ni9yX6WYXJFsNfXzeMMnOzvTQ6-y0vRz`

## Production law
`MANUAL_EVIDENCE_GAIN != RULE_PROMOTION`

A repeated pattern may generate a candidate rule, but the rule must be validated independently before automatic use.

## Next gate
Continue adjudication from the highest-information UNKNOWN cases, preserving UNKNOWN when evidence is incomplete. Do not enter voice lock until the attribution layer is sufficiently complete for recurring/major-character dialogue and provenance-clean.
