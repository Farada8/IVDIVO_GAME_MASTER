# B03 — CH28–29 SPEAKER CONTEXT RECONCILIATION v0.5

**Status:** PASS — CURRENT FINAL CHAPTER BATCH AUTHORITY.  
**Story:** FOUNDER-LOCKED CH01–29.  
**Text mutation:** 0 bytes.  
**Voice IDs:** 0 assigned.

## Result

- CH28: **166/166** confirmed.
- CH29: **208/208** confirmed after one v0.4 correction.
- Batch: **374/374**.
- Residual UNKNOWN acoustic-speaker ownership: **0**.

## v0.4 → v0.5 correction

`B03_CH29_S0358`

`“The strongest warning was not tested. The locally discovered route succeeded without source-route disclosure.”`

- old v0.4: `TAREN_SOR`
- current: **`SMITH`**

Local proof:
1. `Smith said,` introduces S0356.
2. S0357 is only a paragraph break and contains no speaker-transfer cue.
3. S0358 continues Smith's caution/counterevidence.
4. `Taren paused.` is the listener's reaction.
5. S0360 begins Taren's first-person reply.

Regression law: `PARAGRAPH_BREAK_ALONE_DOES_NOT_TRANSFER_SPEAKER; NAMED_PAUSE_CAN_MARK_LISTENER_REACTION_BEFORE_NEXT_RESPONSE`.

`B03_CH29_S0312 = OES_SUPERVISOR_CH29` remains valid from the earlier Red Team.

## Drive authority

- CH28 current map: `1mv0Z8BKu2hhi6eNY-r-7xVRbGWbs978K`
- CH29 v0.5 map: `1AAUv6Pp85WxycZUlVXBHhhTBUTN5Dagy`
- reconciliation manifest: `1lDCAfLqoXQxvqqruph4mJt63aJAwSt_r`
- reconciliation gate: `1GSQyc44UOA44xnTdyevNVs3Ilmf1L_9G`
- Full Speaker Gate v1.2: `1lFmVbEZJSMnCZMn65nAEV5U-rESC-qFX`
- authority router v1.2: `1SF30eK_uoJDFgeR6GyODfGUrIaig-ZWa`
- authority ZIP v1.2: `1qA2DzFdlg-N6v_Wc104PIYDNfQJ5bS00`

## Decision

CH28–29 speaker ownership is closed. No further generic speaker-engine work is authorized absent a demonstrated defect.

Next: full voice-roster normalization and casting slots with `voice_id = null`.
