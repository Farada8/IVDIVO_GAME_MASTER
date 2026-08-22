# BUSINESS CYCLE9 — CORE + EVIDENCE OVERLAY CLOSURE

## Why this exists
Concurrent Business work repeatedly produced valid evidence deltas after the core Cycle9 causal state had already closed. Rewriting one large `CURRENT_BUSINESS_ENGINEERING_AUTHORITY.md` for every evidence refresh created avoidable authority races.

## New local architecture
`CORE CURRENT + MANDATORY EVIDENCE OVERLAY = CURRENT BUSINESS READ MODEL`.

Core file:
`BUSINESS_ENGINEERING_OS/CURRENT_BUSINESS_ENGINEERING_AUTHORITY.md`

Evidence overlay:
`BUSINESS_ENGINEERING_OS/CURRENT_BUSINESS_ENGINEERING_EVIDENCE_DELTA.md`

## Contract
- Core owns causal frontier, completed Run32 history, proof frontier, WIP, current gate and stop rules.
- Evidence overlay owns fresh bounded supplier/source facts and non-findings inside its declared scope.
- Overlay can supersede stale evidence fields but cannot silently change causal frontier, proof grade, WIP, market authority or Self-Improvement authority.
- Any evidence delta that changes a root blocker must trigger explicit core reconciliation.
- A new evidence delta that does not change a root blocker should update the overlay only.

## Current reconciliation
Merged evidence through PR #259 is preserved in the overlay:
- PR #253 bidder primary evidence;
- PR #259 connected-source refresh;
- CORE registration-number evidence;
- A1 declaration correctly classified as not a Certificate of Incorporation;
- Revenue account evidence kept separate from Tax Clearance;
- EWI invoices kept separate from payment/revenue;
- connected-source TCC/insurance non-findings kept as nonexistence-neutral.

Current root blockers remain:
`ROOT_A_TARGET_PACK_NOT_ACQUIRED`
`ROOT_B_NO_EXPLICIT_BIDDER_DESIGNATION_AND_COMPLETE_PACKET`

Cycle9 remains:
`P193–P224 = 32/32 EXECUTED`
`P225–P288 = 64 DESIGNED / 0 EXECUTED`
`PA4=FALSE; PA5=FALSE; E3=FALSE; E4=FALSE`

## Self-improvement disposition
`CORE_AUTHORITY_PLUS_MANDATORY_EVIDENCE_OVERLAY` = BUSINESS-LOCAL CANDIDATE/KEEP.
No new global SI ID. No v3 promotion.

## Concurrency disposition
Older competing CURRENT rewrite PRs that do not contain unique evidence should be closed as superseded after this architecture is merged. Their unique evidence, if any, must be salvaged into the overlay before closure.

READBACK MARKER: BUSINESS-C9-CORE-PLUS-EVIDENCE-OVERLAY-CLOSURE
