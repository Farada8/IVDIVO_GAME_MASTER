# B03 — CH24 PACKET SOURCE QUARANTINE REPAIR v0.5

**Date:** 2026-08-22  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Scope:** speaker metadata only  
**Text mutation:** **0 bytes**  
**Voice IDs assigned:** **0**

## Verdict

**REPAIR REQUIRED / PASS AFTER SOURCE-BOUNDARY SPLIT.**

The CH22–24 v0.4 batch is correct on coverage and story text, but CH24 uses one `speaker_id` (`PRECURSOR_CALLER_CH24_HELD_SOURCE`) for dialogue from **two separate packet recordings**. The locked text does not establish that the packets share a speaker identity.

Under `IVDIVO_SPEAKER_ATTRIBUTION_EVIDENCE_CONTRACT_v2`, unknown sources must not be role-merged across separate source boundaries without textual/canon identity proof. A shared speaker_id would become an unsafe downstream voice-binding shortcut.

## Source-boundary evidence

### Packet 1
Boundary: `One new packet.` / `The voice in the packet was calmer than the previous sources.`

Segments:
- `B03_CH24_S0152`
- `B03_CH24_S0154`

New source role: `PRECURSOR_SOURCE_CH24_PACKET_1`

### Packet 2
Boundary: the flagged workstation chimes again later; `The packet began with a clear male voice.`

Segments:
- `B03_CH24_S0376`
- `B03_CH24_S0378`
- `B03_CH24_S0380`

New source role: `PRECURSOR_SOURCE_CH24_PACKET_2`

Identity relation between Packet 1 and Packet 2: **UNKNOWN**.

## Repair

Five metadata labels only:
- S0152: `PRECURSOR_CALLER_CH24_HELD_SOURCE` → `PRECURSOR_SOURCE_CH24_PACKET_1`
- S0154: same → `PRECURSOR_SOURCE_CH24_PACKET_1`
- S0376: same → `PRECURSOR_SOURCE_CH24_PACKET_2`
- S0378: same → `PRECURSOR_SOURCE_CH24_PACKET_2`
- S0380: same → `PRECURSOR_SOURCE_CH24_PACKET_2`

No dialogue text, narration, causality, story canon, chapter count, or coverage changes.

## Result

- CH24 actual speech: **207**
- assigned: **207/207**
- UNKNOWN speaker ownership at packet boundary: **0** (source ownership is packet-local)
- inter-packet identity equivalence: **UNKNOWN**
- exact-text changes: **0**
- voice IDs: **0**
- full speaker gate: **OPEN**

Corrected Drive map: `130_B03_SPEAKER_CONTEXT_BATCH_CH24_v0.5_SOURCE_QUARANTINE.json` — `1hzNIm7VyLiiuip2gDiZS4InvEPpzGKqx`
SHA-256: `8c10023044771e420ae0fd59e9f2188a3696b449428a296a18ec66aa37c7c04e`

Drive repair gate: `130_B03_CH24_PACKET_SOURCE_QUARANTINE_REPAIR_v0.5.md` — `1tl4xYMLOQmnJPT-PIAzDOMNFwrrzpu9L`
Drive v0.5 batch manifest: `130_B03_SPEAKER_REVIEW_BATCH_CH22_24_MANIFEST_v0.5.json` — `1eGz0wHrkl7owFgXlSlmHec88-5_Fnsth`

## Downstream rule

`SAME_TOPIC_OR_PACKET_CLASS != SAME_SPEAKER_IDENTITY`

Do not bind Packet 1 and Packet 2 to the same voice solely because both are precursor/flagged packet sources. A later casting decision may choose the same performer for artistic reasons, but that must not be represented as proven source identity.
