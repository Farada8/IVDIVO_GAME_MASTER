# B03 — 121–126 DEPENDENCY RED TEAM — v1.1

**Status:** PASS — dependency classification complete; downstream speaker-routing repair still open.  
**Story authority:** FOUNDER-LOCKED CH01–29.  
**Locked prose mutation:** 0 bytes.  
**Provider Voice IDs:** 0.

## Evidence
Current roster: `143_B03_VOICE_ROSTER_AND_CAST_ARCHITECTURE_v1.1.json` — Drive `13Go1HxW86AmYf7dfptH8o1QzihCqexSL`.  
Stale→current diff: `142_B03_STALE_120_TO_CURRENT_MANIFEST_DIFF_v1.1.json` — Drive `1FkYxNZW3rEHZwqWj84zVhyp5YDRtHMUR`.

- old speaker IDs: 120
- current speaker IDs: 119
- changed speech rows: **291**
- changed voice slots: **287**
- unchanged slot despite identity normalization: **4**
- slot-class crossings: **81**
- same-class identity changes: **210**
- unaffected speech rows: **3423**
- narrator delivery rows structurally salvageable: **3751**
- total render rows structurally salvageable before repair: **7174 / 7465**

## Tribunal
- **121 — REPLACE.** Old routing is superseded; `143 v1.1` is current roster/cast architecture.
- **122 — SALVAGE + PATCH.** Global contracts and Narrator + 15 dedicated performance profiles survive. Repair two fixture bindings: `CH24 S0380 → PRECURSOR_SOURCE_CH24_PACKET_2`; `CH27 S0202 → REGIONAL_DUTY_OFFICER`.
- **123 — PARTIAL REBUILD.** 291 rows require speaker/slot rebind; **81 class-crossing rows require full performance recomputation**. The other 210 require local performance revalidation after rebinding; no automatic carry-forward claim.
- **124 — KEEP CONTENT / REVALIDATE PROVENANCE.** Sound architecture contains no speaker/voice routing fields except its source-performance pointer.
- **125 — KEEP CONTENT.** Asset/acoustic requirement model contains no speaker/voice/performance-routing dependency.
- **126 — PARTIAL REBUILD.** 291 speech render units have stale speaker routing; 287 change voice slot; 81 require full performance recomputation. Provider IDs remain null.

## Drive proof artifacts
- tribunal JSON: `1aJDozMTwrjkE54dY4TLz8U2eAFhVc7JR`
- tribunal MD: `13n5qQF1LiP1StPhRSDkRqxgyB7MRHeaS`
- revalidated 122 JSON: `1MJLR6MQroSDBM8mjKXJeCGqhJoEwdHmT`
- 122 gate: `1s6eF9pczwydNpjxZrcD8dncSaDGrQl5k`
- 123 repair queue, 291 rows: `1OQG5hxgBL1fozW1A253qDcifL9r75eDV`
- 126 repair queue, 291 rows: `1pvxTstBU2sfvIynr8zACs-dWYTGFhUC8`
- 124 revalidation receipt: `18aRJSsCfJGbGlG7EhdKoMUiKp2CUakA4`
- 125 revalidation receipt: `1wzL9bl27JX07xKCz2SevTYx_Lq57AK9P`

## Law
`TEXT-INDEPENDENT_METADATA MAY SURVIVE; SPEAKER/VOICE ROUTING MAY NOT CROSS AN AUTHORITY CHANGE WITHOUT ROW-LEVEL REVALIDATION.`

## Next
Rebuild/revalidate affected 123 rows → refresh 124 provenance → retain 125 → rebuild affected 126 units → only then audit 127–132 transitively. No live-provider claim is permitted before real provider evidence.
