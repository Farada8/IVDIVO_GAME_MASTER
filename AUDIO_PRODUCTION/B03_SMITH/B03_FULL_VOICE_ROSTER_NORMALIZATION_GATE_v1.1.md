# B03 — FULL VOICE ROSTER NORMALIZATION + CASTING GATE v1.1

**Date:** 2026-08-22  
**Status:** **PASS — PROVIDER-AGNOSTIC ROSTER NORMALIZATION / LIVE CASTING NOT RUN**  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Locked-text mutation:** 0 bytes  
**Provider Voice IDs:** 0

## Authority

Current full speaker authority is `v1.2_SOURCE_AND_CH29_RECONCILED`, Drive `1lFmVbEZJSMnCZMn65nAEV5U-rESC-qFX`, package `1qA2DzFdlg-N6v_Wc104PIYDNfQJ5bS00`.

The prior voice architecture (`121_B03_VOICE_MAP_ARCHITECTURE_v1.0.json`, Drive `1JsWpwwtxdZb0CD3mGRB248zhH8bwxiN2`) is used only as the collision-graph base. Its old 120-ID/28-slot cardinality is not inherited as proof.

## Repairs that force a rebase

1. CH24 now has two separate packet-local source identities rather than one aggregate precursor role.
2. `TAREN_SOR_MESSAGE_CH27` has source author Taren but acoustic speaker Smith reading aloud.
3. CH29 S0358 is Smith, not Taren.

## Revalidated result

- textual source/speaker IDs: **121**
- actual speech turns: **3714**
- narrator delivery segments: **3751**
- total delivery segments: **7465**
- dedicated character slots: **15**
- ensemble reuse slots: **12**
- narrator slots: **1**
- maximum cast slots after current collision revalidation: **28**
- same-chapter ensemble collisions: **0**
- non-null provider Voice IDs: **0**

The old slot-level arithmetic exposed a real defect: it summed to 3713 speech deliveries because the CH27 Taren-authored line was routed outside Smith's acoustic slot. Current normalization gives `3714 + 3751 = 7465` exactly.

## Source/acoustic routing

### Taren message CH27
`source_author=TAREN_SOR`, `acoustic_speaker=SMITH`, `delivery_mode=READ_ALOUD_DOCUMENT`, `voice_slot=V_D01`.

### CH24 packet sources
- Packet 1: `PRECURSOR_SOURCE_CH24_PACKET_1`, 2 turns, temporary collision-safe slot `V_E07`.
- Packet 2: `PRECURSOR_SOURCE_CH24_PACKET_2`, 3 turns, temporary collision-safe slot `V_E01`.
- inter-packet identity remains **UNKNOWN**.

The two packet roles deliberately occupy distinct audition slots. A later casting choice may reuse a performer, but that never becomes source-identity evidence.

### CH29 S0358
Direct Smith speech +1; direct Taren speech -1. No story-text change.

## Collision proof

The 12 ensemble reuse slots were recomputed after the packet split. `V_E01` had no CH24 role before adding Packet 2; `V_E07` contains Packet 1 and no second CH24 role. Revalidation across all ensemble slots returns **0 same-chapter collisions**. Thus the current source split does not require a 29th cast slot; the 28-slot maximum is re-earned rather than inherited.

## Casting law

All slots remain `provider_voice_id=null` and `UNCAST`. Accent/dialect and exact vocal age stay unset unless canon or audition evidence supports them. Provider candidates are temporary until human listening and pronunciation adjudication.

Hard laws:
- `SOURCE_AUTHOR != ACOUSTIC_SPEAKER`
- `SOURCE_IDENTITY != CAST_SLOT`
- `CAST_REUSE != CHARACTER_OR_SOURCE_IDENTITY`
- `SAME_TOPIC_OR_PACKET_CLASS != SAME_SOURCE_IDENTITY`
- `VOICE_ID = null` until casting evidence
- no bulk CH01–29 synthesis before bounded S0 + CH01 Hard Pilot PASS

## Evidence locations

Full normalized roster JSON: Drive `1FB_3rqk4ax4HMFykTli6focbZmz6dH-o`.  
Human gate: Drive `1RzwTzmagtVHHDEVrm-4gcphCjDBKQO_2au1kovDhKvo`.

## Next

Provider-dependent frontier: obtain a real current voice/model inventory, bind temporary S0 candidates, run only bounded auditions, preserve request/model/voice/audio/alignment provenance, and perform human cast + Slovenian pronunciation adjudication.

Provider-independent audio work may continue in parallel through the SFX/ambience/music/acoustic-passport architecture and CH01 Hard-Pilot cue binding.
