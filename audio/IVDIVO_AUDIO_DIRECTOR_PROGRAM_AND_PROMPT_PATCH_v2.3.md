# IVDIVO AUDIO DIRECTOR — PROGRAM + PROMPT PATCH v2.3

**Date:** 2026-08-20  
**Status:** CANON / MACHINE CONTRACT + PROMPT PATCH  
**Applies to:** all IVDIVO audio productions.  
**Authority:** additive over v2.1 base + v2.2 patch.

## 1. New/extended machine objects

### 1.1 ResponseState
```yaml
ResponseState:
  beat_id: string
  speaker_id: string
  heard_event: string
  response_impulse: ANSWER|DEFLECT|INTERRUPT|WITHHOLD|APPROACH|RETREAT|IGNORE|OTHER
  listening_state: string
  entry_trigger: semantic_anchor
  reply_mode: IMMEDIATE|QUICK|NORMAL|HELD|INTERRUPT|OVERLAP|NO_REPLY
  state_out: string
```

### 1.2 SceneContextPacket
```yaml
SceneContextPacket:
  scene_id: string
  immediate_scene_objective: string
  partner_objective: string|null
  previous_event: string
  relationship_state: string
  status_state: string
  physical_situation: string
  expected_response_opportunity: string|null
  forbidden_future_knowledge: [string]
```

### 1.3 FoleyPerformanceState
```yaml
FoleyPerformanceState:
  cue_id: string
  performer_intent: string
  character_weight: LIGHT|NORMAL|HEAVY|CUSTOM
  action_tempo: SLOW|MEASURED|NORMAL|QUICK|ABRUPT
  contact_force: 0.0-1.0
  material_response: string
  sync_tolerance: TIGHT|MEDIUM|LOOSE
  characterization_required: boolean
```

### 1.4 MouthBodyState
```yaml
MouthBodyState:
  speaker_id: string
  beat_id: string
  mouth_state: CLEAR|BITING|CHEWING|HOLDING_FOOD|DRINKING|POST_SWALLOW|DRY_MOUTH|OTHER
  speech_allowed: boolean
  speech_impairment: NONE|LIGHT|MEDIUM|STORY_SPECIFIC
  swallow_before_line: boolean
  breath_reset: NONE|SMALL|FULL|STORY_SPECIFIC
  utensil_state: NONE|IN_HAND|MOVING|RESTING
```

### 1.5 MicrotextureSalienceGate
```yaml
MicrotextureSalienceGate:
  cue_id: string
  repulsion_risk: LOW|MEDIUM|HIGH
  fatigue_risk: LOW|MEDIUM|HIGH
  headphone_gain_limit_db: number|null
  repetition_limit: integer|null
  foreground_allowed: boolean
  decision: KEEP|REDUCE|OMIT|REDESIGN
```

### 1.6 ListenerPointOfAudition
```yaml
ListenerPointOfAudition:
  scene_id: string
  listener_position: string
  listener_orientation: string
  pov_mode: OBJECTIVE_SCENE|CHARACTER_SUBJECTIVE|DEVICE_MEDIATED|TRANSITIONAL
  head_relative_positions: {entity_id: string}
  movement_relative_to_listener: [string]
  mono_safe: boolean
```

### 1.7 MixActionScore
```yaml
MixActionScore:
  beat_id: string
  focus_owner: string
  time_conflict: [string]
  frequency_conflict: [string]
  level_conflict: [string]
  stereo_conflict: [string]
  depth_conflict: [string]
  level_move: string|null
  width_move: string|null
  depth_move: string|null
  reverb_move: string|null
  mute_or_reveal: string|null
  music_move: string|null
  dramatic_reason: string
```

### 1.8 MixObjectiveQC
```yaml
MixObjectiveQC:
  master_id: string
  mood: PASS|FAIL
  balance: PASS|FAIL
  definition: PASS|FAIL
  interest: PASS|FAIL
  comprehension: PASS|FAIL
  story_intent: PASS|FAIL
  smallest_repairs: [string]
```

## 2. Compiler order patch
```text
LOCKED STORY
→ AUTHORITY CHECK
→ LISTENER CONTRACT
→ DRAMATIC FORCE MAP
→ WHOLE-SCENE CONTEXT
→ RESPONSE STATE
→ PERFORMANCE OBJECTIVE/TACTIC/SUBTEXT
→ SUBTEXT-TO-BEHAVIOR COMPILATION
→ BODY/MOUTH STATE
→ BLOCKING + LISTENER POINT OF AUDITION
→ PAUSE/BREATH/OVERLAP PLAN
→ AUDIO COMPOSITION
→ FOLEY PERFORMANCE STATE
→ MICROTEXTURE SALIENCE GATE
→ SFX/AMBIENCE/MUSIC PLAN
→ PROVIDER REQUESTS
→ DIAGNOSTIC TAKES
→ EDIT-FIRST GATE
→ ALIGNMENT/TIMELINE
→ MIX ACTION SCORE
→ AUTOMIX
→ MIX OBJECTIVE QC
→ PLAYBACK/HUMAN QC
→ MASTER LOCK
```

## 3. Prompt v2.3-A — LISTEN AND ANSWER
For each important spoken turn, identify:
- exact heard event;
- what changed in the speaker because of it;
- response impulse;
- entry trigger;
- reply mode;
- whether silence/interruption/overlap is more truthful than a clean isolated entry.

Output only `ResponseState` objects.

Reject line direction that could be written without knowing the previous turn.

## 4. Prompt v2.3-B — WHOLE-SCENE CONTEXT PACKET
Create the smallest context packet that makes a render block truthful.
Include only present-scene facts the actor needs.
Do not reveal future plot, hidden solution or audience-only knowledge.

## 5. Prompt v2.3-C — SUBTEXT TO PLAYABLE BEHAVIOR
Input internal subtext and convert it into observable vocal/physical behavior.

Allowed dimensions:
`REPLY_SPEED / PROJECTION / PHRASE_ENDING / BREATH / HESITATION / EMPHASIS / ORIENTATION / DISTANCE / INTERRUPTION / WITHHOLDING`.

Output no abstract emotion label unless paired with behavior.

## 6. Prompt v2.3-D — FOLEY PERFORMANCE DIRECTOR
For each selected Foley cue, determine:
- who performs the action;
- why now;
- weight/tempo/contact force;
- material response;
- whether the sound characterizes the person;
- sync precision required;
- whether a library asset is sufficient or a performed/custom asset is required.

Do not sonify every action.

## 7. Prompt v2.3-E — FOOD / DRINK BODY CONSISTENCY
For each eating/drinking beat:
1. choose minimal audible chain;
2. set `MouthBodyState`;
3. decide if speech can occur physically at that moment;
4. decide whether swallow/breath reset precedes the line;
5. protect against gross/headphone-heavy mouth detail;
6. keep dialogue and emotion primary unless the eating itself is story focus.

Output:
`MouthBodyState + selected Foley cues + MicrotextureSalienceGate`.

## 8. Prompt v2.3-F — LISTENER POINT OF AUDITION
Define where the listener acoustically exists.
Then place characters/objects relative to that point.

If using left/right/behind/ear-specific speech, specify:
- why the viewpoint earns it;
- motion trajectory;
- distance/reverb/spectral changes;
- mono-safe equivalent.

## 9. Prompt v2.3-G — MIX ACTION SCORE
After alignment, audit every dense beat in five domains:
`TIME / FREQUENCY / LEVEL / STEREO / DEPTH`.

Then write only necessary mix moves.
Every move must cite a story/attention reason.
No decorative automation.

## 10. Prompt v2.3-H — CONVERSATIONAL RHYTHM
Build rhythm from:
- listening;
- response latency;
- thought completion;
- interruption pressure;
- overlap opportunity;
- body/object action;
- status change.

Do not infer rhythm from punctuation alone.
For locked text, preserve words exactly and solve naturalness through timing/nonverbal reaction/edit unless adaptation is authorized.

## 11. Prompt v2.3-I — DIAGNOSTIC TAKE DESIGN
For each alternate take define one hypothesis.
Examples:
- less projected;
- quicker defensive response;
- longer held reply;
- lower energy but same tactic;
- closer proximity without romantic coding.

Never request random rerolls.

## 12. Prompt v2.3-J — EDIT BEFORE RERENDER
Diagnose defect:
`TIMING / PAUSE / OVERLAP / BREATH / LEVEL / PERSPECTIVE / PRONUNCIATION / ACTING / VOICE_IDENTITY / SYNTHESIS_ARTIFACT / SOURCE_TEXT`.

If defect is editorial, issue `EDIT_FIX`.
If defect is acting/voice/pronunciation/irreparable artifact, issue `RERENDER`.

## 13. Prompt v2.3-K — MIX OBJECTIVE QC
Evaluate final scene/master for:
`MOOD / BALANCE / DEFINITION / INTEREST / COMPREHENSION / STORY_INTENT`.

Fail if technical polish makes acting flatter, space less believable, dialogue less legible, or emotional contrast weaker.

## 14. Provider compilation extension
Provider request may now receive:
`EXACT_TEXT + CHARACTER + SCENE_CONTEXT_PACKET + HEARD_EVENT + RESPONSE_IMPULSE + OBJECTIVE + TACTIC + PLAYABLE_BEHAVIOR + BODY_STATE + TEMPO + ENERGY + BREATH + REPLY_MODE + PROXIMITY + PRONUNCIATION + TAKE_HYPOTHESIS`.

Do not send full canon prose or hidden story solutions to the provider.

## 15. New NO-GO gates
NO-GO when applicable if:
- a line lacks a response trigger in a reactive dialogue scene;
- partner context resets between adjacent blocks;
- Foley timing/weight contradicts character action;
- audible eating is present but clean speech ignores the body state implausibly;
- mouth/body microtexture becomes repulsive or fatiguing without story authorization;
- ear-specific staging has no listener viewpoint or mono fallback;
- mix conflict is treated only by loudness despite frequency/time/depth conflict;
- alternate takes are random rather than diagnostic;
- rerender is requested for a defect solvable by edit;
- punctuation forces unnatural acting against thought/action rhythm.

**v2.3 result:** additive universal machine/prompt authority.