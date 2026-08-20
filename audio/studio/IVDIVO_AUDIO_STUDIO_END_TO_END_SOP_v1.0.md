# IVDIVO AUDIO STUDIO — END-TO-END SOP v1.0

**Status:** CANON / EXECUTION SOP  
**Applies to:** every audio production after text/story authority is available.

## A. Required project folder tree
```text
PROJECT_AUDIO/
  00_AUTHORITY/
  01_DRAMATURGY/
  02_STAGING/
  03_PERFORMANCE/
  04_DIALOGUE_RENDER/
  05_FOLEY_MICROTEXTURE/
  06_SFX_SOUND_DESIGN/
  07_AMBIENCE_SPATIAL/
  08_MUSIC/
  09_EDIT_ALIGNMENT/
  10_MIX/
  11_MASTER/
  12_QC/
  13_RELEASE/
  99_ARCHIVE_SUPERSEDED/
```

## B. Naming rule
`PROJECT_EP_SCENE_ARTIFACT_vMAJOR.MINOR_STATUS.ext`

Every machine-readable artifact includes source hash and authority versions.

## C. Gate lifecycle
Every stage state is one of:
`NOT_STARTED / WORKING / REVIEW_PENDING / PASS / FAIL / LOCKED / SUPERSEDED`.

No downstream production consumes a FAIL or ambiguous artifact.

## D. Execution procedure

### STEP 0 — INGEST / AUTHORITY
Owner: Role 1.

Do:
1. identify exact source file and version;
2. calculate source hash;
3. identify spoken-text protection level;
4. identify delivery mode A/B/C/D;
5. load universal audio authority;
6. load project overlay;
7. list forbidden branches/tokens if project has history contamination;
8. record release target and technical delivery requirements.

Create:
`AUTHORITY_MANIFEST.json`

Fail if source is ambiguous.

### STEP 1 — SCENE/BLOCK MAP
Owners: Roles 1 + 2.

Segment by causal scene and dramatic beat, not arbitrary character count.
Assign stable IDs before directing.

Create:
`SCENE_MAP.json`
`TEXT_UNIT_MAP.json`

Exact-text productions require 100% spoken-unit coverage.

### STEP 2 — LISTENER CONTRACT
Owner: Role 2.
For every important beat define:
- what listener must understand;
- what listener may feel;
- what remains active/awaited;
- focus owner;
- layers to suppress;
- possible dangerous misunderstanding.

Create:
`LISTENER_CONTRACT.json`

### STEP 3 — DRAMATIC FORCE + AUDIO ARC
Owner: Role 2.
Track only story-earned curves such as trust, desire, fear, control, knowledge, isolation, connection.

Create:
`DRAMATIC_FORCE_MAP.json`
`AUDIO_DRAMATURGY.json`

### STEP 4 — AUDIO STAGING
Owner: Role 2 with Role 7.
Map:
- where scene starts/ends;
- entries/exits;
- physical actions;
- blocking needs;
- action/reaction sequence;
- narration-to-action relation;
- protected silences;
- transition logic.

Create:
`AUDIO_STAGING_SCRIPT.md/json`

### STEP 5 — CAST / VOICE LOCK
Owner: Role 3.
Define per character:
- voice ID/provider profile if selected;
- age/perceived age range;
- vocal weight/timbre;
- normal tempo;
- articulation;
- status behavior;
- emotional restraint range;
- intimacy distance law;
- forbidden caricatures;
- pronunciation.

Create:
`CAST_MAP.json`
`CHARACTER_VOICE_BIBLE.json`

Do not batch-render a major character before sample approval.

### STEP 6 — PERFORMANCE SCORE
Owner: Role 3.
For every important line/block define:
`STATE_IN / HEARD_EVENT / WANT / TACTIC / SUBTEXT / RESPONSE_IMPULSE / STATUS / ENERGY / TEMPO / LISTENING_STATE / REPLY_MODE / BREATH_FUNCTION / PROXIMITY / BODY_STATE / FORBIDDEN_PERFORMANCE / STATE_OUT`.

Create:
`ACTOR_DIRECTOR_SCORE.json`

### STEP 7 — PAUSE / BREATH / RHYTHM PASS
Owner: Role 3.
Mark only story-functional pauses and vocal reactions.
Create overlap/interruption policy.

Create:
`RHYTHM_PAUSE_BREATH_PLAN.json`

### STEP 8 — ACOUSTIC / POINT-OF-AUDITION MAP
Owner: Role 7.
Define room/materials/resonance/noise floor and listener viewpoint.
Map all relevant people/objects.

Create:
`ACOUSTIC_PASSPORT.json`
`LISTENER_POINT_OF_AUDITION.json`
`BLOCKING_SPATIAL_MAP.json`

### STEP 9 — FOLEY / HUMAN TEXTURE PASS
Owner: Role 5.
Select only useful embodied details.

For eating/drinking, determine mouth/body state and whether speech timing must shift.
Protect against excessive mouth detail on headphones.

Create:
`FOLEY_CAUSALITY_GRAPH.json`
`FOLEY_PERFORMANCE_SCORE.json`
`MICROTEXTURE_PLAN.json`
`FOOD_DRINK_PLAN.json` if relevant.

### STEP 10 — SFX / PROCEDURAL SOUND PASS
Owner: Role 6.
Every important cue gets:
- cause;
- physical class;
- story function;
- literal meaning;
- possible extended meaning;
- forbidden implications;
- audibility/proximity;
- asset strategy: source/library/generate/record/procedural/layer;
- sonic identity requirements.

Create:
`SFX_CUE_SHEET.json`
`PROCEDURAL_SOUND_SPEC.json`
`ASSET_REGISTRY.json`

### STEP 11 — AMBIENCE PASS
Owner: Role 7.
Build layered ambience:
`ROOM_TONE / ENVIRONMENTAL_BED / DISTANT_ACTIVITY / WEATHER_MECHANICAL / OCCASIONAL_WORLD_EVENTS / STORY_EXCEPTIONS`.

Avoid short obvious loops. Suppress ambience when attention requires it.

Create:
`AMBIENCE_ARCHITECTURE.json`

### STEP 12 — MUSIC PASS
Owner: Role 8.
Map story value change before music.
Create no-music windows and anti-spoiler implications.

Create:
`MUSIC_DRAMATURGY.json`
`THEME_REGISTRY.json`
`MUSIC_CUE_SHEET.json`

### STEP 13 — RENDER BLOCK COMPILATION
Owner: Role 4.
Choose:
`TTD_BLOCK / ISOLATED_TTS / NARRATION_BLOCK / VOCALIZATION_BLOCK / PERFORMANCE_SOUND`.

Isolate:
- clue-critical speech;
- unique media processing;
- pronunciation risk;
- lines likely to need selective rerender;
- post-chain boundary changes.

Create:
`RENDER_BLOCK_PLAN.json`

### STEP 14 — PROVIDER DRY RUN
Owner: Role 4.
Compile psychology into playable behavior.
Generate provider requests with:
- exact text;
- character/voice;
- scene context packet;
- heard event;
- objective/tactic;
- playable behavior;
- energy/tempo/breath/reply mode;
- pronunciation;
- take hypothesis;
- output format;
- request hash;
- selective regeneration boundary.

No live calls until dry-run gates pass.

Create:
`PROVIDER_REQUESTS_DRY_RUN.json`

### STEP 15 — PILOT SAMPLE
Owners: 3 + 4 + 9 + 10.
Before full book/episode production, render the hardest 3–5 minutes or project-defined pilot.
Test acting, space, Foley, music, mix and AI visibility.

Gate:
`PILOT_SAMPLE_PASS`.

### STEP 16 — FULL DIALOGUE RENDER
Owner: Role 4.
For each block:
`GENERATED → REVIEW_PENDING → ACCEPTED → LOCKED`.
Use diagnostic alternate takes only.

Create:
`TAKE_REGISTRY.json`

### STEP 17 — ASSET RENDER / LOCK
Owners: 5/6/7/8.
Source/generate/record required assets.
Recurring important assets receive fixed IDs and are not casually regenerated.

### STEP 18 — EDIT FIRST
Owner: Role 4.
For every defect ask whether trim, pause, overlap, breath, room tone, clip gain, crossfade or perspective adjustment solves it.
Rerender only when the actual performance/voice/pronunciation/synthesis is wrong.

Create:
`EDIT_DECISION_LOG.json`

### STEP 19 — REAL ALIGNMENT / TIMELINE
Owner: Role 4.
Ingest provider timestamps/alignment for locked dialogue.
Resolve semantic anchors into actual sample positions.

Create:
`RESOLVED_TIMELINE.json`

### STEP 20 — MIX ACTION SCORE
Owner: Role 9.
For each dense beat audit:
`TIME / FREQUENCY / LEVEL / STEREO / DEPTH`.
Assign foreground owner and write only necessary automation.

Create:
`MIX_ACTION_SCORE.json`

### STEP 21 — PREMIX / FINAL MIX
Owner: Role 9.
Minimum stems:
`DIALOGUE / CLUE_SFX / SFX / FOLEY / AMBIENCE / MUSIC`.
Optional subgroups as required.

Check acoustic coherence across dialogue/Foley/SFX.
Check mono and phone before mastering.

### STEP 22 — MASTER
Owner: Role 9.
Create platform-appropriate master(s), preserve tails, silence and microdynamics.
Never repair story/performance problems through mastering.

### STEP 23 — MACHINE QC
Owner: Role 10.
Run exact-text, hash, duration, silence, missing cue, stem, clipping/peak/loudness, mono, routing and artifact checks.

### STEP 24 — HUMAN LISTENING QC
Owner: Role 10.
At minimum evaluate:
- believe the people?
- understand the scene?
- feel the space?
- emotional response earned rather than instructed?
- music helping or manipulating?
- microtexture distracting/repulsive?
- AI cadence noticeable?
- want to continue?

### STEP 25 — SELECTIVE REPAIR
Route defect to smallest owner/artifact.
Do not reopen whole project because of local error.

### STEP 26 — RELEASE
Required:
`AUTHORITY_PASS + TEXT/PERFORMANCE_PASS + ASSET_PASS + MIX_PASS + PLAYBACK_PASS + HUMAN_LISTEN_PASS`.

Create:
`RELEASE_GATE.json`
`MASTER_LOCK.json`

## E. Production batch strategy
Never manufacture an entire season/book before the production style is validated.
Recommended:
`hardest sample → first episode/chapter → 2–3 unit pilot batch → production batch`.

## F. Repair severity
`FATAL / MAJOR / MEDIUM / POLISH`.

FATAL examples:
wrong source, missing story-critical line, wrong speaker, impossible clue order, broken master.

MAJOR examples:
false emotional coding, character reset, unintelligible dialogue, wrong sound causality, music masking, severe AI cadence.

MEDIUM examples:
weak rhythm, repetitive ambience, small spatial mismatch, local Foley over-density.

POLISH examples:
minor trim, local texture balance, harmless tonal refinement.
