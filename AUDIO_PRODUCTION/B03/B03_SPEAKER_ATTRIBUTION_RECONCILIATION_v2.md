# B03 — THE EMPTY RESCUE — SPEAKER ATTRIBUTION RECONCILIATION v2

**Date:** 2026-08-22  
**Story state:** FOUNDER LOCKED / RELEASE READY  
**Text mutation:** none  
**Current whole-book speaker state:** **CORRECTED PARTIAL MAP / FULL GATE OPEN**

## Red-team finding

The parallel Tier-1 v1 map (`78_B03_SPEAKER_ATTRIBUTION_TIER1_EXPLICIT_v1.json`, Drive `1jC_88TFKo6OvSWfF3Nayey4xRt48gkDZ`) claimed 653 explicit assignments but fails quote-boundary ownership. Comparison against the corrected one-sided engine found:

- Tier-1 v1 assignments: 653
- corrected strict one-sided assignments: 471
- common segment IDs: 440
- same speaker on common IDs: 370
- direct speaker conflicts: **70**
- v1-only assignments: 213
- corrected-only assignments: 31

Root cause: v1 can allow an attribution belonging to the following quote to capture the preceding quote. Speech-tag evidence must never be reused bidirectionally.

Concrete examples include CH01 `Keep hydro access separate if you can.` (Jana; v1 incorrectly assigned CALLER), CH28 `Extraction side is upper inspection if the current attempt succeeds.` (HYDRO_CONTROL; v1 assigned MAJA), and CH27 `So Contact thinks it is good.` (REGIONAL_DUTY_OFFICER; v1 assigned SMITH).

## Tier-2 salvage

The cumulative Tier-2 v1 map inherited the invalid 653 baseline and therefore cannot remain authority as a 700-line cumulative map. Its 47 pronoun-resolution additions were isolated and independently rechecked. All 47 survive the intended conservative rule.

Correct rebased cumulative state:

- original curly-quote spans: 3,718
- narrator-inline semantic quote exceptions: 3
- actual dialogue spans: 3,715
- Tier-1 one-sided explicit assignments: **471**
- revalidated Tier-2 pronoun additions: **47**
- cumulative assigned: **518**
- residual UNKNOWN: **3,197**
- cumulative coverage: **13.94%**
- prose byte changes: 0

Current private map: `110_B03_SPEAKER_ATTRIBUTION_TIER2_REBASED_v2.json`, Drive `1px9HoDaBujFK1iJ0NiyQ1bRgvI5GHoS1`. Gate: Drive `1W6TluQh58BDju0C5-IMSVJETiBJLvoJS`.

## CH01 production lane

CH01 is separately protected. The private CH01 production map (`77_B03_AUDIO_EXACT_TEXT_SEGMENTATION_CH01_v1.json`, Drive `1aw17696W4KOLVgCcnOkKxpaOJE15YRMg`) was audited 142/142 against locked text and scene/turn context with zero conflicts. It demonstrably does not blindly inherit the defective whole-book autopass; it correctly resolves a known counterexample where the old engine fails.

CH01 reconciliation: Drive JSON `10WMtxygCb24N2XnBZeL6z0-B0PJUZZFY`, MD `1ofWRzJoeWpidY0BkOGJsOqQKHMMnygLC`.

Therefore the separate CH01 `PROVIDER_BRIDGE_READY / LIVE EVIDENCE REQUIRED` frontier remains valid. No CH01 downstream quarantine is required from this speaker-engine repair alone.

## Authority routing

- Tier-1 v1 / 653 = **REJECTED FOR SPEAKER AUTHORITY**.
- Tier-2 v1 cumulative 700 = **REJECTED AS CUMULATIVE MAP; 47-line delta salvaged**.
- Rebasing v2 / 518 = **CURRENT PARTIAL WHOLE-BOOK SPEAKER MAP**.
- Full speaker attribution remains OPEN.
- CH02–29 must continue only from corrected v2 plus auditable contextual review.
- No alternating-turn autofill, no semantic voice guessing, no story rewrite.
