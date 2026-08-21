# NMM E01 SOUND / POST / QC SPEC — CYCLE 2

## Phone / voice-note post chains

**STATUS:** DESIGN PASS / CLEAN ACCEPTED SPEECH INPUT PENDING.

### PHONE_REMOTE_CHAIN_A
Clean voice → HPF 250 Hz → LPF 3.6 kHz → mild 2:1 compression → subtle saturation → output trim.
Goal: telephone identity while preserving consonant/timestamp intelligibility.
Hard fail: actor identity collapses or critical consonants blur.

### PHONE_REMOTE_CHAIN_B
Clean voice → HPF 180 Hz → LPF 4.2 kHz → light 1.8–2.6 kHz emphasis → 2.5:1 compression → output trim.
Goal: wider modern-call bandwidth for voices harmed by Chain A.

### VOICE_NOTE_RECORDING_CHAIN_A
Clean Leo master → HPF 120 Hz → LPF 6.8 kHz → mild device compression → stable authored environment → no added room reverb.
`W_EXTRA_SHORT` remains a separate story asset inserted at the authored source point.

### VOICE_NOTE_RECORDING_CHAIN_B
Clean Leo master → HPF 150 Hz → LPF 5.5 kHz → slightly stronger device compression → stable authored environment.
Use only if A remains too clean after actual device testing.

No chain may be locked before testing on accepted clean speech.

## Foley minimalism
Retain only if action, space, attention or causality changes.

KEEP/TEST: phone vibration; phone unlock/replay; incoming call; service/security door; paper cup only if staging retains it; headphones/replay actions where analytically necessary; footsteps only where movement needs spatial clarification.

SUPPRESS BY DEFAULT: continuous cloth; generic stationary-dialogue footsteps; decorative cup handling; repeated UI ticks; cinematic door slams; random room decoration.

## Sound-density regression
Information-critical beats: max **1 primary focus + 1 low contextual bed**.

1. Leo confession — recording/dialogue primary; no music; environment below masking threshold.
2. 11:47 vs 12:04 — timestamps primary; phone coloration cannot compete.
3. Memory vs inference — dialogue primary; roomtone only.
4. Leo recognizes own recording — replay/recognition primary; no decorative Foley.
5. Short vs long whistle — whistle identity primary; dialogue yields transient space; music absent.
6. Final `That whistle isn't from your match.` — Isla primary → protected silence → score only after silence.

FAIL if two clue-bearing sources compete, music supplies hidden interpretation, ambience masks consonants/time phrases, Foley steals attention, or mix EQ invents a whistle difference not present in the selected assets.
