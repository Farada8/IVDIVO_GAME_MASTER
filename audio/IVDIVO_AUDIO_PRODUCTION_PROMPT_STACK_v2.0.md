# IVDIVO AUDIO PRODUCTION PROMPT STACK v2.0

**Date:** 2026-08-20  
**Status:** CANON / PRODUCTION PROMPTS  
**Use:** internal studio prompts for converting locked fiction into directed, provider-ready, quality-controlled audio.

These prompts never outrank project-specific canon or Founder instructions. They operate on locked story material and must preserve protected text/clues/relationship state.

---

## P0 — AUTHORITY RESTORE / AUDIO BOOT

```text
ACTIVE PROJECT: {PROJECT}
ACTIVE EPISODE/CHAPTER: {UNIT}

Restore current production authority from current Drive/GitHub sources before making any audio decision.

Build a source map:
CANON / WORKING / OPTION / UNKNOWN / SUPERSEDED / REJECTED.

Identify:
- active branch;
- locked source script and hash;
- delivery mode;
- current cast/voice locks;
- pronunciation locks;
- project sound identity;
- recurring locked assets;
- forbidden old branches/material;
- exact last completed audio artifact;
- exact next unblocked production obligation.

Do not rewrite story. Do not restore archive material. Return a machine-readable authority manifest and a compact human summary.
```

## P1 — STORY AUDIO ANALYSIS + SCENE AUDIO DRAMATURGY

```text
Using only the locked source and current project overlay, analyze the episode/chapter as an audio work.

For every scene define:
START STATE
WHO WANTS WHAT
WHY NOW
RESISTANCE
WHAT CHANGES
LISTENER FOCUS
TENSION 0–10
EMOTIONAL TEMPERATURE 0–10
INFORMATION PRIORITY
ESCALATION POINTS
REVERSAL / RECOGNITION
AFTERMATH
END STATE
NEXT-LISTEN QUESTION

Then build an episode audio arc showing changes in tension, density, intimacy, information load, silence and music opportunity.

Do not add SFX yet except when a source action is already explicit. Do not invent timestamps.
```

## P2 — ACTOR / PERFORMANCE DIRECTOR

```text
Create the Actor Director Score for the locked script.

For each important dialogue turn/block preserve EXACT_TEXT and derive:
IMMEDIATE WANT
WHY NOW
RESISTANCE
TACTIC
SUBTEXT
UNSAID / UNSAYABLE
STATUS BEFORE / AFTER
STATE_IN / STATE_OUT
ENERGY 1–10
TEMPO
LISTENING STATE
NEXT ENTRY IMPULSE
REPLY MODE
BREATH/PAUSE CAUSE
TACTIC CHANGE
FORBIDDEN PERFORMANCE

Use playable verbs, not literary mood summaries.

Direct silent listening when dramatically relevant. Do not insert random sighs, gasps, laughs or vocalizations. If a non-verbal reaction is proposed, include its cause and story function.

Maintain performance continuity across render blocks.
```

## P3 — BLOCKING / PROXIMITY / ACOUSTIC STAGING

```text
Create the physical staging of every scene.

For each character track:
POSITION
BODY ORIENTATION
DISTANCE TO PARTNER
PROXIMITY STATE: SOCIAL / WORK / PERSONAL / INTIMATE / WITHDRAWAL
MIC PERSPECTIVE
MOVEMENT PATH
OFF-AXIS STATE
OCCLUSION
CONTACT EVENT

For each location define/load the Acoustic Passport:
room size
materials
early reflections
reverb behavior
noise floor
stereo width
distance law
occlusion behavior
ambient layers
critical clue exceptions

Every spatial change must have a physical cause. Do not make all voices remain studio-close while characters move.
```

## P4 — AUDIO COMPOSITION SCORE

```text
Build the complete semantic-time Audio Composition Score.

For every beat determine only what serves story:
DIALOGUE / NARRATION
SILENCE
AMBIENCE
FOLEY
ACTION SFX
CLUE/EVIDENCE SFX
PROCESSING
MUSIC
SPATIAL MOVEMENT
TRANSITION
MONTAGE

For every beat define:
FOCUS_1
FOCUS_2
BACKGROUND
SUPPRESS
SOUND_DENSITY 0–10
SPEECH TEMPO
REPLY MODE
PAUSE DENSITY
OVERLAP DENSITY
MOVEMENT ACTIVITY
MUSIC INTENSITY
STEREO ACTIVITY

Use only semantic anchors:
SCENE_START / BEFORE_TURN / AFTER_TURN / BEFORE_EVENT / AFTER_EVENT / DURING_ACTION.

Never invent absolute timestamps before accepted render alignment.

Prefer subtracting competing sound before adding a dramatic effect.
```

## P5 — SOUND WORLD / FOLEY / OBJECT / CLUE PLAN

```text
Create all required sound assets from the Audio Composition Score.

For each cue define:
ASSET_ID
EVENT_TYPE
STORY_FUNCTION
PHYSICAL_SOURCE
CHARACTER/ACTION CAUSE if applicable
MATERIAL
DISTANCE
SPACE
DURATION RULE
ONE_SHOT / LOOP
FOREGROUND / BACKGROUND
CLUE / NON_CLUE
MUST_BE_DISTINCT_FROM
GENERATION/SEARCH PROMPT
NEGATIVE PROMPT
MIX PRIORITY
MONO_CRITICAL
CAN_OVERLAP_DIALOGUE
NEGATIVE_IMPLICATIONS
BLIND_TEST_QUESTION

Maintain Foley causality:
CHARACTER → ACTION → OBJECT → SOUND → RESULT.

Reuse locked recurring assets rather than silently regenerating a new identity.

For phones, radios, recorders, intercoms and archive media, specify the physical transmission path and keep clean human performance separate from medium degradation when practical.
```

## P6 — MUSIC DRAMATURGY

```text
Build the music score only after dialogue, silence, sound causality and attention map are known.

For every proposed music cue ask:
What value has already changed?
Why music rather than silence?
Will it mask words or evidence?
Will it imply romance/guilt/fear/importance before earned?
Can the beat work better without music?

If music is justified define:
CUE_ID
FUNCTION: IDENTITY / DESIRE / ATTRACTION / MEMORY / LOSS / THREAT / CHOICE / AFTERMATH / TRANSITION / END_BUTTON
ENTRY_CAUSE
EXIT_CAUSE
MOTIF_ID
INSTRUMENTATION
INTENSITY 0–10
DIALOGUE_POLICY
DURATION_RULE
NEGATIVE_IMPLICATIONS
FORBIDDEN_WINDOWS

No continuous underscore by default. Music loses every conflict with comprehension.
```

## P7 — PROVIDER PERFORMANCE COMPILER / ELEVENLABS

```text
Compile the internal Director Score into provider-safe render blocks.

Do NOT send raw psychology directly to the provider.
Translate:
PSYCHOLOGY → PLAYABLE BEHAVIOUR → PROVIDER-SAFE INSTRUCTION.

For each block choose:
TTD_BLOCK / ISOLATED_TTS / VOCALIZATION / PERFORMANCE_SOUND / LOCKED_ASSET.

Preserve exact protected text.
Include:
source turn IDs
speaker/voice IDs
exact text
context summary
playable direction
provider-safe instruction
pronunciation refs
tag budget
take plan
forbidden performance
post-processing domain
request hash/provenance fields

Use sparse tags. Do not stack tags on every line.

Take plan:
A = baseline
B = exactly one controlled alternative
C = only for a critical clue/emotional beat

Keep ambience, story-critical SFX, music and heavy device processing out of clean actor masters when practical.
```

## P8 — EDIT / TAKE / TIMELINE DIRECTOR

```text
After provider render, evaluate each take against:
exact words
speaker identity
pronunciation
intention
state continuity
status
clue comprehension
false romance/guilt/villain implications
provider artifacts

If words, voice identity and intention pass and the problem is timing/trim/spacing/crossfade/reaction placement, prefer EDIT_ONLY.

Otherwise SELECTIVE_RERENDER the smallest responsible turn/block.

Lock accepted takes.

Resolve semantic anchors to absolute time only from accepted take timing/alignment.
Do not disturb unrelated locked blocks.
```

## P9 — AUTOMIX / MASKING / MASTERING

```text
Create AutoMix from accepted takes, accepted/locked assets and resolved timeline.

Priority:
1 spoken clue / human action
2 evidence sound required for causality
3 room orientation
4 emotional silence
5 Foley/ambience detail
6 music

For each stem/cue define:
gain
pan
width
direct/reverb ratio
early reflections
occlusion
fade
ducking
processing
mono protection
priority

Check speech/clue masking and repair using ducking, EQ space, reduced reverb, narrower ambience, transient control or stem level before touching script.

Master to delivery target without flattening authored micro-dynamics, breath, silence, proximity or distance.
```

## P10 — FINAL AUDIO QC + SELECTIVE REPAIR

```text
Run fail-closed release QA.

AUTHORITY:
active branch
source hash
wrong-branch contamination

CONTENT:
exact text
speaker binding
missing/duplicate/reordered units
pronunciation
clue order
protected wording

PERFORMANCE:
state continuity
believability
status/subtext
AI cadence
false implication
vocal texture continuity

SOUND:
causal Foley
location orientation
recurring asset identity
clue audibility
media authenticity
protected silence
music policy
masking

TECHNICAL:
clicks/dropouts/hard splices
clipping/peak/loudness
stereo/mono/mobile/low volume/1.25x
stem completeness

AI ARTIFACTS:
VOICE_DRIFT
UNNATURAL_CADENCE
SYLLABLE_SMEAR
WRONG_STRESS
BREATH_GLITCH
DUPLICATED_WORD
TRUNCATED_WORD
FAKE_LAUGH
TIMBRE_JUMP
UNNATURAL_SILENCE
OVER_EMPHASIS
SPOKEN_TAG

For each defect output:
timestamp/anchor
unit/block/cue ID
layer
severity
cause
repair action: EDIT_ONLY / SELECTIVE_RERENDER / REMIX_ONLY / ASSET_REPLACE / MANUAL_REVIEW / NO_ACTION
protected unchanged material
retest gate

Do not rerender the whole work unless a proven systemic FATAL requires it.
```

## P11 — HUMAN LISTENING GATE

```text
Do not fabricate listener results.

Ask target listeners without script/production notes to evaluate:
CONTENT: what happened and what changed?
PERFORMANCE: do these sound like believable people with distinct intentions?
SOUND: can you orient physically and understand causal sounds?
EMOTION: what did you feel and at what moment?
RETENTION: what do you want to hear next?
AI BLIND: where, if anywhere, did the audio feel synthetic or generated?

Collect confusion/drop timestamps and repeated complaints. Reopen only the smallest responsible layer when evidence repeats.
```

## P12 — FULL STUDIO RUN

```text
RUN IVDIVO AUDIO STUDIO on {PROJECT}/{UNIT}.

Use current authority and the Universal Audio Production Canon + Audio Director v2.0.
Do not rewrite locked story unless a concrete production failure satisfies the Story Lock exception.

Execute in order:
P0 Authority
P1 Audio Dramaturgy
P2 Performance
P3 Blocking/Acoustic
P4 Audio Composition
P5 Sound World
P6 Music
P7 Provider Compilation
P8 Take/Edit/Timeline
P9 AutoMix
P10 QC
P11 Human gate when required

Return one integrated production package, not fake committee transcripts.
Stop before paid/live provider calls when DRY_RUN is requested.
```
