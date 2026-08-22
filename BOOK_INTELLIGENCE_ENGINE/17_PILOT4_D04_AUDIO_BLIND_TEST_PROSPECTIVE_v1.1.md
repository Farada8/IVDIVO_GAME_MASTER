# BOOK INTELLIGENCE ENGINE v1.1 — PILOT 4
## D04 AUDIO G4 BLIND-LISTENER METHOD — PROSPECTIVE CROSS-DOMAIN VALIDATION

**Date:** 2026-08-22  
**Domain:** AUDIO / SUBJECTIVE TEST DESIGN  
**Project:** D04 / SEVEN NIGHTS BEFORE CODE BLUE  
**Status:** PASS_REAL_PROJECT_PROCESS_GAIN_HUMAN_AUDIO_RESULT_PENDING

## Why this is a prospective validation
The v1.1 gateway was used before any real human-listener evidence was accepted. The active D04 state said `G4_MACHINE = PASS`, `G4_HUMAN = PENDING`, with a real blind packet ready for one human response. Book Intelligence opened a targeted official methodology source because the next production decision depended on the quality of that human evidence.

Sequence:

`CURRENT D04 AUTHORITY -> CURRENT BLIND PACKET -> TARGETED OFFICIAL SOURCE -> LOCATED METHODOLOGY CLAIMS -> AUDIO ADAPTER -> TEST-DESIGN DIAGNOSIS -> METHOD REPAIR -> DISTRIBUTABLE DRIVE PACKS -> MACHINE CONTRACT + HIDDEN KEY -> HUMAN GATE REMAINS PENDING`.

No result is credited retroactively and no listener outcome is invented.

## Baseline inspected
Current D04 state before repair:
- story E01–E24 complete / Final Story Gate PASS;
- G4 transfer prototype machine PASS;
- real 24-bit/48 kHz WAV assets already persisted;
- no live provider calls;
- no Moss speech rendered;
- human perceptual gate pending.

Baseline human packet:
`AUDIO_PRODUCTION/SEVEN_NIGHTS/SEVEN_NIGHTS_TRANSFER_BLIND_LISTENER_PACKET_v1.json`.

The v1 procedure asked one listener to hear STEREO -> MONO -> PHONE in one fixed order, choose forced `A_or_B`, and could then support wording equivalent to reliable recognition if all three were correct.

## Source adapter packet
Source pass:
`BOOK_INTELLIGENCE_ENGINE/16_ITU_BS1116_AUDIO_SUBJECTIVE_TEST_SOURCE_PASS_v1.0.md`.

Source:
ITU-R BS.1116-3, official ITU Recommendation.

Source state:
`VERIFIED / PARTIAL_TARGETED / MECHANISMS_EXTRACTED / NOT_FULL_READ`.

Selected mechanisms:
1. `ORDER_COUNTERBALANCE`;
2. `REPLICATE_BEFORE_RELIABLE`;
3. `FIX_LEVEL_WITHIN_SESSION`;
4. `EVIDENCE_SCOPE_LABEL`.

These are transferable bias-control mechanisms only. D04 does not claim formal BS.1116 compliance.

## Defect found before human evidence
### Defect class: FALSE_RELIABILITY_RISK
Three linked problems were found:
1. **single-listener promotion risk** — one person could close a gate labelled as reliable human recognition;
2. **fixed-order carryover** — after hearing the first modality the same listener knows what cue to search for in later modalities, so STEREO/MONO/PHONE are not independent observations;
3. **forced guessing** — `A_or_B` had no `CAN'T TELL`, so uncertainty could become a lucky correct answer.

The issue is not that the WAV assets failed. The issue is that the evidence collection method could overstate what the human evidence proved.

## Repair implemented
### 1. Three independent listener packs
Drive parent:
`D04 G4 BLIND LISTENER v2 — COUNTERBALANCED 3-LISTENER SCREEN`
ID: `11DuG5frwv9jFyT0boD0bVOuQgIdkF65C`.

Subfolders:
- LISTENER_01 `1jKvaK2xWq4D5c7FGzLJn3fmpuLnVjSX2`;
- LISTENER_02 `17dmI6pUznDgVDRGF_vgE0EiZcsvPY5Xn`;
- LISTENER_03 `1lahjeVPpjDJM9UcnxZlhvrWDLjnZgbyq`.

Each contains six neutral-named WAV copies (`T01_A/B`, `T02_A/B`, `T03_A/B`) plus its own instruction/response form.

### 2. Counterbalanced modality order
- Listener 01: MONO -> PHONE -> STEREO;
- Listener 02: PHONE -> STEREO -> MONO;
- Listener 03: STEREO -> MONO -> PHONE.

Visible A/B assignment is also reversed across listeners so a stable visible label cannot become a cue.

### 3. Explicit uncertainty
Response options are now:
`A / B / CAN'T TELL`.

`CAN'T TELL` is scored as not-correct for PASS, but it is not treated as a participant error worth discouraging. It prevents forced guessing from masquerading as perception.

### 4. Session-control rules
- comfortable volume fixed before T01 and held constant;
- same playback path for the session;
- no feedback between trials;
- each file max two plays per trial;
- no waveform/metadata/spectrogram/measurement inspection;
- plain-language description required;
- cinematic/horror interpretation captured as a semantic hard-fail signal.

### 5. Evidence-scope repair
New machine contract:
`AUDIO_PRODUCTION/SEVEN_NIGHTS/SEVEN_NIGHTS_TRANSFER_BLIND_LISTENER_PROTOCOL_v2.json`.

Internal key:
`AUDIO_PRODUCTION/SEVEN_NIGHTS/SEVEN_NIGHTS_TRANSFER_BLIND_LISTENER_KEY_INTERNAL_v2.json`.

One listener now produces only:
`SINGLE_LISTENER_OBSERVATION_ONLY`.

Internal replicated production PASS requires:
- at least 2/3 independent listeners correct on all 3 trials;
- every underlying modality correct for at least 2/3 listeners;
- no primary cinematic/horror interpretation.

This threshold is an IVDIVO production rule, not an ITU rule and not formal statistical proof.

## What was deliberately NOT changed
- Existing audio WAV content: unchanged; Drive copies/renames only.
- G4 machine metrics: unchanged.
- Story text: unchanged.
- Provider calls: 0.
- Moss voice: still unrendered.
- Human perceptual result: still PENDING.
- Release authorization: not advanced.

## Incremental gain
Observable process gain exists before human listening:
- a gate that could have been closed by one possibly lucky/carryover-influenced session can no longer do so;
- three independent counterbalanced packs are now directly distributable;
- answer-key leakage through original A/B filenames is removed from participant-facing folders;
- uncertainty is measurable rather than forced into A/B;
- result language is constrained to the evidence actually collected;
- no provider credits and no new render were required.

## Regression / safety
**FATAL:** 0  
**BLOCKING MAJOR:** 0  
**STORY CHANGES:** 0  
**AUDIO ASSET REDESIGN:** 0  
**PROVIDER CALLS:** 0  
**HUMAN RESULT FABRICATED:** 0

The original machine PASS remains valid as machine evidence only. The human gate remains external and unresolved.

## Pilot result
`PASS_REAL_PROJECT_PROCESS_GAIN_HUMAN_AUDIO_RESULT_PENDING`.

This is a second independent prospective project/domain with observable Book Intelligence v1.1 gain:
- Pilot 3: B03 STORY/FACTUAL — removed unsupported network-clock causality and closed a factual hold;
- Pilot 4: D04 AUDIO/METHODOLOGY — prevented a weak human-evidence procedure from producing an overstated perceptual PASS.

Therefore the **Book Intelligence v1.1 gateway architecture** now has two independent prospective project gains with FATAL 0 / MAJOR 0 and is eligible for cross-domain promotion under its own promotion contract.

Boundary: this does **not** universally promote every individual NASA/SRE/ITU-derived mechanism. Mechanism lifecycles remain separate.

## Next D04 gate
Run LISTENER_01, LISTENER_02 and LISTENER_03 as real independent human sessions, capture their forms without revealing the key, then score once against v2 internal key. Until that occurs:

`G4_HUMAN = PENDING`.