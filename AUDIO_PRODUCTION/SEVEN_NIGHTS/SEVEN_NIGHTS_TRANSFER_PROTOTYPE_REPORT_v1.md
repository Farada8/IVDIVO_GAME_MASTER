# SEVEN NIGHTS BEFORE CODE BLUE — NORMAL vs SECOND TRANSFER ENGINEERING PROTOTYPE v1

**DATE:** 2026-08-21  
**STATUS:** MACHINE PASS / HUMAN LISTENER PENDING  
**LIVE PROVIDER CALLS:** 0  
**MOSS VOICE:** NOT RENDERED  
**FINAL SOUND LOCK:** NOT CLAIMED

## Purpose

Test the protected story fact that the listener must distinguish the ordinary NORMAL TRANSFER from SECOND TRANSFER, including on mono/ordinary-phone playback, before any full E01 audio scale-up.

## Produced real assets

All assets are 24-bit / 48 kHz / 24.0 seconds and are durably stored in the D04 Audio Production Pack Drive folder.

- Stereo: `SN_TRANSFER_PROTOTYPE_STEREO_MACHINE_v1.wav` — Drive `1HKcTVYJLWMJSXQIfFpXDc8XylrMbSZTk` — SHA256 `006b94f88e5d04384ea6e29bdd5df5b88d10990842bccf119c79c672a90d39e5`.
- Mono: `SN_TRANSFER_PROTOTYPE_MONO_MACHINE_v1.wav` — Drive `1JiDJI9cLGxsBayVGO1YkBqxbXKwpQteg` — SHA256 `b44dd6c9a5a89870fd54070a0bfe689e6053bf6388949b115b6e226d8dd3a371`.
- Phone-band: `SN_TRANSFER_PROTOTYPE_PHONE_MACHINE_v1.wav` — Drive `1LWxnBUqNJpIjOVuq8tNWnMYH02K0oGmy` — SHA256 `5c3d3bda0d22c9745d07e59c54e8b78c7aad62c1ca2b9dcc85cae6edd8ef46fe`.
- Machine QC: Drive `1k3fpSq622_GcQl1IqXGkNN_EPNJ7zga0`; GitHub JSON `SEVEN_NIGHTS_TRANSFER_PROTOTYPE_MACHINE_QC_v1.json`.

## Timeline

- 00.00–05.00 — ordinary equipment-room bed.
- 05.00 — P1 NORMAL TRANSFER: ordinary relay/load-state change.
- 05.65–08.60 — settled normal-state analysis window.
- 09.00–13.80 — same ordinary environment; no protected silence claim.
- 14.00 — P3 SECOND TRANSFER begins with the same primary change.
- 14.35 — distinct additional mechanical/load-state change.
- 14.85–17.80 — settled second-state analysis window.
- 18.40–21.00 — reserved radio slot; exact line `Hold the second transfer.` is deliberately UNRENDERED because no real Moss cast/provider evidence exists.

## Design rules

The second event is not a cinematic sting. No music, boom, riser or horror cue is used. Its extra identity is mechanical/load-state information in the mid band (880/1320/1760 Hz) so the distinction does not depend on sub-bass.

## Machine QC

- stereo peak: -19.50 dBFS
- mono peak: -19.79 dBFS
- phone peak: -21.39 dBFS
- NaN/Inf: PASS
- machine differentiability gate: PASS
- phone 600–1800 Hz settled-state delta, SECOND minus NORMAL: **+7.28 dB**
- phone 600–1000 Hz delta: +5.45 dB
- phone 1000–1800 Hz delta: +18.09 dB

These measurements prove a machine-detectable mid-band difference. They do **not** prove that a human listener interprets it correctly.

## Required human gate

Blind listener must hear stereo, mono and ordinary-phone versions without labels/explanation and correctly report that SECOND TRANSFER contains an extra state change. The difference must not depend on sub-bass or visual annotation.

PASS requires reliable recognition across all three playback variants. FAIL if:
- NORMAL and SECOND are confused;
- extra state disappears on mono/phone;
- cue reads as cinematic effect instead of ordinary equipment behavior.

## Production disposition

`G4_MACHINE = PASS`

`G4_HUMAN = PENDING`

No E01 full render is authorized by this machine pass. Provider/casting G1 remains independently blocked on authenticated voice/model inventory and exactly six candidate-A bindings.
