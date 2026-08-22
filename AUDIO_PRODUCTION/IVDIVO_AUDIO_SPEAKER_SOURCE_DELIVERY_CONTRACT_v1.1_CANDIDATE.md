# IVDIVO AUDIO — SPEAKER / SOURCE / DELIVERY CONTRACT v1.1 CANDIDATE

**Status:** CANDIDATE — B03-PROVEN, SECOND-PROJECT REPLICATION REQUIRED  
**Date:** 2026-08-22

## Purpose
Extend the existing speaker-attribution evidence safeguards after B03 exposed failures that occur *after* lexical speaker ownership is apparently complete: source identity collapse, authored-message/acoustic-delivery confusion, paragraph-boundary transfer errors and cast-graph drift.

## New candidate laws

### 1. SOURCE_AUTHOR != ACOUSTIC_SPEAKER
A document/message may be authored by A and audibly read by B. Store both fields. The cast voice follows acoustic delivery, not semantic authorship, unless the production intentionally inserts a separately authorized source-voice performance.

B03 regression fixture: `TAREN_SOR_MESSAGE_CH27` — source author Taren, acoustic reader Smith.

### 2. SOURCE_IDENTITY != CAST_IDENTITY
One performer may portray multiple unrelated sources. Performer reuse is production economics, not evidence that those sources are the same entity.

### 3. SAME_TOPIC_OR_PACKET_CLASS != SAME_SOURCE_IDENTITY
Separate recordings/packets with similar content remain separate source identities unless text/canon/evidence proves equivalence.

B03 fixture: CH24 Packet 1 and Packet 2.

### 4. PARAGRAPH_BREAK_ALONE_DOES_NOT_TRANSFER_SPEAKER
A formatting boundary is not a speaker-change proof. Re-evaluate local discourse ownership, speech tags and reaction beats.

### 5. NAMED_PAUSE_CAN_BE_LISTENER_REACTION
`X paused` between another speaker's continuation and X's later reply does not necessarily transfer the preceding line to X. Treat pause/reaction beats as evidence requiring local sequence analysis, not as automatic backward attribution.

B03 fixture: `B03_CH29_S0358`.

### 6. ROSTER_CARDINALITY_MUST_BE_REVALIDATED_AFTER_SOURCE_SPLIT
If one source ID becomes two, rerun same-scene/same-chapter collision coloring. Do not inherit an old cast-slot count.

### 7. DELIVERY_ARITHMETIC_MUST_CLOSE
For an exact-text production, the sum of narrator deliveries + cast speech deliveries must equal the exact-text delivery denominator. A one-line mismatch is a blocking provenance defect, not rounding noise.

B03 found old voice-slot speech sum 3713 vs actual speech 3714 because an authored message was routed outside its acoustic reader's slot.

## Required downstream fields
Where mediated speech exists, metadata should support:
- `source_author`
- `source_identity`
- `source_boundary`
- `acoustic_speaker`
- `delivery_mode`
- `cast_slot`
- `provider_voice_id`

## Promotion boundary
These safeguards are structurally justified and B03-proven, but universal `VERIFIED_CURRENT` promotion requires an independent second project or corpus regression showing that the fields/rules prevent real errors without forcing false distinctions.

Until then:
`B03_PROJECT_USE = PASS`
`UNIVERSAL_STATUS = CANDIDATE_SECOND_PROJECT_REPLICATION_REQUIRED`
