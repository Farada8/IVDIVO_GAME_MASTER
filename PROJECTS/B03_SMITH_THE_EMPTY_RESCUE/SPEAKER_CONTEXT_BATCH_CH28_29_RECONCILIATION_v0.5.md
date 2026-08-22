# B03 — SPEAKER CONTEXT BATCH CH28–29 RECONCILIATION v0.5

**Status:** PASS — FINAL CHAPTER BATCH RECONCILED  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Text mutation:** 0 bytes  
**Voice IDs assigned:** 0

## Result

- CH28: **166/166**, UNKNOWN 0
- CH29: **208/208**, UNKNOWN 0
- CH28–29: **374/374**, UNKNOWN 0
- Full-book production speaker ownership after reconciliation: **3714/3714**, UNKNOWN 0

## Current Drive authority

- CH28 map v0.4: `1mv0Z8BKu2hhi6eNY-r-7xVRbGWbs978K`
- CH29 map v0.5 reconciled: `1AAUv6Pp85WxycZUlVXBHhhTBUTN5Dagy`
- reconciliation manifest: `1lDCAfLqoXQxvqqruph4mJt63aJAwSt_r`
- reconciliation gate: `1GSQyc44UOA44xnTdyevNVs3Ilmf1L_9G`

## Reconciliation corrections

### `B03_CH29_S0312`
Current acoustic speaker: `OES_SUPERVISOR_CH29`.

The local scene has the OES supervisor as the active male grammatical/discourse subject before `“I have the case instruction,” he said.` This defeats the older nearest-named-male assignment to Smith.

### `B03_CH29_S0358`
Current acoustic speaker: **SMITH**.

Text chain:
- `Smith said,` introduces S0356.
- S0357 is only a paragraph break; there is no speaker-transfer cue.
- S0358 continues Smith's caution: `“The strongest warning was not tested. The locally discovered route succeeded without source-route disclosure.”`
- `Taren paused.` is the listener reaction.
- S0360 begins Taren's first-person response.

Regression law:
`PARAGRAPH_BREAK_ALONE_DOES_NOT_TRANSFER_SPEAKER; NAMED_PAUSE_CAN_MARK_LISTENER_REACTION_BEFORE_NEXT_RESPONSE`.

## Superseded production material

CH29 v0.4 and the previous CH28–29 v0.4 gate are provenance only because they retain the wrong S0358 ownership. Drive copies are explicitly marked SUPERSEDED.

## Boundary

This is production chapter-local speaker authority. It does **not** claim that all 3714 assignments were generated or verified by the deterministic speaker engine. The current deterministic engine-verified subset remains **599**.

No provider dispatch, casting, pronunciation approval or synthesis is authorized by this receipt.
