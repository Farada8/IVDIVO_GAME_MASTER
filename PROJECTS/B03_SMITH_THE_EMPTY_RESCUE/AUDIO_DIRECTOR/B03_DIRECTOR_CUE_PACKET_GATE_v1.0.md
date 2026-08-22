# B03 — DIRECTOR CUE PACKET + CH01 HARD-PILOT CUE GATE — v1.0

**Status:** **PASS — PROVIDER-INDEPENDENT CUE BINDINGS / LIVE AUDIO NOT RUN**  
**Story authority:** FOUNDER-LOCKED CH01–29  
**Text mutation:** **0 bytes**  
**CH30:** **NOT AUTHORIZED**

## What is now closed

- Deterministic render blocks: **108 / 108**.
- Exact-text segment coverage: **7465 / 7465**, each segment exactly once and in locked order.
- Sound cue coverage: **362 / 362**, each cue bound exactly once.
- Protected clue blocks: **8 / 8**.
- CH01 Hard-Pilot blocks: **10 / 10**, including all four CH01 protected clue blocks.
- Per-block `exact_text_sha256` is compiled from the locked segmentation package.
- Every block keeps `provider_voice_id = null` and `provider_dispatch_allowed = false`.
- Asset IDs and acceptance remain empty / `NOT_RUN`.

## Authority rebase applied

The older Performance Direction machine file contained one stale downstream rule for the CH27 authored message. This packet does **not** propagate it.

- `B03_CH27_S0136`: source author = `TAREN_SOR`; acoustic speaker = **SMITH**; delivery mode = `READ_ALOUD_DOCUMENT`.
- `B03_CH29_S0358`: acoustic speaker = **SMITH**, not `TAREN_SOR`.
- CH24 Packet 1 (`S0152`, `S0154`) = `PRECURSOR_SOURCE_CH24_PACKET_1`.
- CH24 Packet 2 (`S0376`, `S0378`, `S0380`) = `PRECURSOR_SOURCE_CH24_PACKET_2`.
- Inter-packet identity remains **UNKNOWN**.

Regression law preserved: `SOURCE_AUTHOR != ACOUSTIC_SPEAKER`; `CAST_REUSE != SOURCE_IDENTITY`.

## Director cue behavior

Each render block now carries:

`block_id`, chapter/range, segment count, exact-text char count/hash, cue IDs/categories, critical function, acoustic-passport candidates, candidate domain/perspective/channel, source identity when proved, acoustic-speaker override when required, delivery mode, protected-silence state, music permission, pronunciation holds, provider/asset holds, prohibited implications, and director notes.

Where existing evidence does not uniquely determine an acoustic passport, the packet deliberately stores `HOLD_*` rather than inventing a lock.

## Red Team / acceptance

PASS:
- 108 unique render blocks.
- 7465 segments exactly once, exact order.
- 362 cue IDs exactly once.
- 8 protected-clue blocks.
- CH24 packet sources stay separate.
- CH27 read-aloud routes to Smith.
- CH29 S0358 routes to Smith.
- no voice IDs, provider dispatch, generated asset, human-listening, mix/master, or market claim.

OPEN / HOLD:
- real provider workspace;
- real workspace voice/model inventory;
- temporary S0 audition candidates;
- Slovenian pronunciation evidence and adjudication;
- accepted SFX/Foley/IR/music assets;
- alignment;
- CH01 canary / Hard Pilot listening result;
- mix/master QC;
- bulk render.

## Next exact action

Proceed to **S0 EXECUTION PACKET + PRONUNCIATION EVIDENCE LEDGER**, provider-neutral until a real provider context exists. The packet may prepare request schemas and bounded audition text selection, but it must keep voice/model IDs null and dispatch false until live provider evidence is available.

**Bulk CH01–29 rendering remains forbidden.**
