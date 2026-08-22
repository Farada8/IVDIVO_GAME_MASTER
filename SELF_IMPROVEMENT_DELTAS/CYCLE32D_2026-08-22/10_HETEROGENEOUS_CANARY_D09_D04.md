# CYCLE32D — HETEROGENEOUS CANARY D09 + D04

Date: 2026-08-22
Status: REGRESSION / FALSE-POSITIVE CONTROL PASS

## D09 — THE MAN WHO CAME BACK
Project state: E01-E24 text complete, final story gate PASS, Founder lock not yet issued. Next safe action is Founder approval/lock; E25 and continuation before lock are prohibited.

Aggregate portfolio router does not mark D09 as active project; it lists D09 under pending Founder decision gates. Therefore the stale-router validator returns `NOT_APPLICABLE` for active-project comparison rather than quarantining unrelated work.

Semantic consistency check: aggregate pending gate and D09 project state both require Founder lock decision. No stale conflict found.

## D04 — SEVEN NIGHTS BEFORE CODE BLUE
Project state: story complete; downstream audio pack ready. Current unblocked next action requires a real human blind-listener response. Live provider evidence remains unproven and voice binding unlocked.

Aggregate portfolio router does not mark D04 as active project. Validator returns `NOT_APPLICABLE` for active-project comparison. This is correct: the validator must not mistake a valid downstream external-evidence gate for stale routing.

## Result
- D01: true-positive stale-router catch -> QUARANTINE.
- D10: negative/regression canary -> no false story reopening.
- D09: unrelated/pending-founder gate -> NOT_APPLICABLE, semantically consistent.
- D04: unrelated downstream-human gate -> NOT_APPLICABLE, preserves external-evidence boundary.

## Disposition
The narrow mechanism now has heterogeneous support across writing completion, Founder-decision gating and downstream audio/human-evidence states. Keep local candidate. Still no whole-v3 or whole-Cycle32D promotion.
