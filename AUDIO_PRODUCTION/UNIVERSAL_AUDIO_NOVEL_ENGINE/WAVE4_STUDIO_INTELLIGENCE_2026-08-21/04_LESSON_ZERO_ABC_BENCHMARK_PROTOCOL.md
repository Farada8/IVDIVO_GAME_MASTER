# LESSON ZERO — A/B/C AUDIO BENCHMARK PROTOCOL v1

## Source lock

Benchmark uses the already established LESSON ZERO canary identity only:
- 3 render requests;
- 36 spoken units;
- 2163 characters;
- roles: Narrator / Ethan / Aoife;
- RB001: 1271 chars, U001–U024;
- RB002: 203 chars, U025–U029;
- RB003: 689 chars, U030–U036;
- existing block hashes remain immutable.

No new story text is introduced for the benchmark.

## Variant A — NARRATED

Goal: establish lowest-complexity baseline.

Rules:
- same locked words;
- narrator carries all text;
- no dramatized Foley/music except essential recording normalization;
- same target playback normalization as B/C for review.

## Variant B — MULTI_VOICE

Goal: measure value of role separation without full dramatization.

Rules:
- same locked words;
- Narrator + Ethan + Aoife provisional cast;
- semantic pauses and microphone perspective allowed;
- no decorative scene sound that would confound the comparison.

## Variant C — DRAMATIZED

Goal: measure incremental value of full scene treatment.

Rules:
- same locked words and voice bindings as B;
- only causally declared Foley/ambience/protected silence/music;
- preserve CUE008–CUE012 canary sound subset where applicable;
- do not force ROOM917 bus topology onto LESSON ZERO.

## Fairness controls

All three:
- same source identity;
- same story facts;
- same listening loudness target;
- same device test set;
- randomized/blinded labels for human comparison where practical;
- no prose repair between A/B/C.

## Human dimensions (0–5)

- believability;
- clarity;
- want-more;
- fatigue resistance.

Founder quick markers remain compatible:
`BELIEVE`, `DON'T BELIEVE`, `BORING`, `CONFUSING`, `WRITER TALK`, `PERFORMANCE WRONG`, `STRONG`, `WANT MORE`.

## Economics

For each variant record measured:
- provider cost;
- manual review time;
- accepted duration;
- regenerated duration;
- cache reuse.

## Decision law

Do not choose a winner from aesthetics alone.

A mode can be preferred for a product tier only after:
- real audio exists;
- human scores exist;
- measured costs exist;
- major defects are classified;
- repair burden is known.

Current status: `HOLD_FOR_LIVE_RENDER_EVIDENCE`.
