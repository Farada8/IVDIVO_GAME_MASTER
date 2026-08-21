# IVDIVO STUDIO INTELLIGENCE LAYER v0.1 — ARCHITECTURE

## Product objective

Turn the existing audio-production framework into an evidence-driven studio pipeline:

`LOCKED SOURCE -> DIRECTOR COMPILATION -> CAST/RENDER -> ALIGNMENT -> SELECTIVE ASSEMBLY -> HUMAN REVIEW -> ECONOMICS -> BENCHMARK -> RELEASE`

## 1. Automatic Audio Director

Input:
- immutable source text hash;
- spoken units;
- character objectives;
- listener/reaction states;
- declared microphone perspective;
- declared causal events and source facts.

Output:
- performance cues;
- semantic pause functions;
- microphone choreography;
- Foley/ambience/music/silence cues only when supported by declared story/production facts.

Hard laws:
- no story rewrite;
- no invented causal Foley/music fact;
- no absolute timestamp before real alignment;
- machine output is advisory until accepted into a Director Score.

## 2. Performance Intelligence

Purpose: replace “pretty voice” selection with evidence.

Required for provisional pilot-lock eligibility:
- multi-state audition;
- pronunciation pass;
- long-form fatigue pass;
- human review;
- pair/ensemble pass where relationship function requires it.

Machine flags may identify risks such as cadence repetition, regularized pauses or breath patterns. They do not auto-reject and never auto-lock a voice.

## 3. Human Review Compressor

Purpose: reduce repetitive manual listening during repair cycles.

Machine can prioritize:
- FATAL/MAJOR flags;
- suspected AI-tells;
- pronunciation anomalies;
- alignment uncertainty;
- protected-silence damage;
- mix/device translation failures.

But:
- compressed review is a triage interface;
- final blind acceptance still requires human listening;
- machine cannot clear release by absence of flags.

## 4. Economics Engine

Measured fields:
- generated seconds;
- accepted seconds;
- provider cost;
- manual review minutes and labor rate;
- cache-reused seconds;
- regeneration seconds.

Derived metrics:
- acceptance yield;
- total cost;
- cost per accepted minute;
- cache reuse fraction;
- regeneration fraction.

Unknown costs stay `HOLD_MISSING_EVIDENCE`.

## 5. A/B/C Benchmark

Three product modes use the same locked source:
- `NARRATED`
- `MULTI_VOICE`
- `DRAMATIZED`

Compare:
- believability;
- clarity;
- want-more;
- fatigue resistance;
- total cost;
- cost per accepted minute;
- repair burden.

No mode wins until all three have real rendered assets, human evidence and cost evidence.

## 6. Selective Repair

Defect route:
`DETECT -> CLASSIFY EARLIEST LAYER -> REPAIR SMALLEST ASSET -> INVALIDATE DECLARED DEPENDENCIES -> RE-RUN LOCAL QC`.

Default forbidden behavior:
- rewrite story because a voice failed;
- rerender full chapter because one pronunciation failed;
- recompute unrelated accepted assets.

## 7. Release gate

`GO_STUDIO_V1` requires all:
- benchmark PASS;
- performance lock eligibility for required roles;
- economics PASS;
- blind human acceptance;
- live provider evidence.

No machine override.
