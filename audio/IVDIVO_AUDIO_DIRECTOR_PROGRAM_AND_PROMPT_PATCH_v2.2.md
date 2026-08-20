# IVDIVO AUDIO DIRECTOR — PROGRAM + PROMPT PATCH v2.2

**Date:** 2026-08-20  
**Status:** CANON / MACHINE CONTRACT + PROMPT PATCH  
**Applies to:** all IVDIVO audio productions.  
**Authority:** additive over `IVDIVO_AUDIO_DIRECTOR_PROGRAM_CONTRACT_v2.1.md` and `IVDIVO_AUDIO_PRODUCTION_PROMPT_STACK_v2.1.md`.

This patch translates the evidence-based v2.2 canon additions into machine-readable production fields and executable prompt passes.

---

## 1. REQUIRED NEW OBJECTS

### 1.1 ListenerContract
```yaml
ListenerContract:
  scene_id: string
  beat_id: string
  listener_must_understand: [string]
  listener_may_feel: [string]
  listener_must_wait_for: [string]
  focus_owner: DIALOGUE|CLUE_SFX|SFX|FOLEY|AMBIENCE|MUSIC|SILENCE
  secondary_support: [string]
  suppress: [string]
  comprehension_critical: boolean
```

Rule: no critical beat may proceed to sound design without a ListenerContract.

### 1.2 DramaticForceMap
```yaml
DramaticForceMap:
  scene_id: string
  forces:
    - name: POWER|TRUST|DESIRE|FEAR|CONTROL|KNOWLEDGE|ISOLATION|CONNECTION|CUSTOM
      start: 0.0-1.0
      midpoint: 0.0-1.0
      end: 0.0-1.0
      turning_anchors: [semantic_anchor]
  dominant_force_by_beat: {beat_id: force_name}
```

Rule: sound palette follows dramatic force; never invent a dramatic force solely to justify an effect.

### 1.3 Extended PerformanceBlock
Add fields:
```yaml
offscreen_audio_context: [string]
partner_action_context: [string]
object_action_context: [string]
previous_event: string
next_expected_event: string
mic_distance: CONTACT|VERY_CLOSE|CLOSE|MEDIUM|FAR|VERY_FAR
head_orientation: TOWARD_PARTNER|TOWARD_MIC|OFF_AXIS|AWAY|MOVING
movement_path: [semantic_anchor]
breath_function: NONE|PREPARE|RECOVER|SUPPRESS_EMOTION|PHYSICAL_EFFORT|HESITATION|LAUGH|CRY|OTHER
listener_target: string
performance_commitment: LOW|MEDIUM|HIGH
```

Provider law: internal psychology must be translated into playable behavior. Never send vague tags such as `be emotional`, `be sexy`, `sound cinematic`, `be mysterious` when a playable tactic is available.

### 1.4 SoundCue v2.2
```yaml
SoundCue:
  cue_id: string
  physical_class: HARD_EFFECT|FOLEY|BACKGROUND_AMBIENCE|ELECTRONIC_PRODUCTION_ELEMENT|DESIGNED_EFFECT
  story_function: ACTION|BODY|PLACE|MATERIAL|ORIENTATION|TRANSITION|MEMORY|RELATIONSHIP|STATUS|CLUE|THREAT|COMIC|EMOTIONAL_SUPPORT
  semantic_priority: NORMAL|IMPORTANT|CLUE_SFX|PROTECTED
  cause: string
  body_or_object: string|null
  action: string
  literal_meaning: string
  possible_extended_meaning: [string]
  forbidden_implications: [string]
  audibility: SUBLIMINAL|LOW|MEDIUM|FOREGROUND
  proximity: CONTACT|VERY_CLOSE|CLOSE|MEDIUM|FAR|VERY_FAR
  duration_policy: TRANSIENT|SHORT|SUSTAINED|LOOPABLE
  focus_priority: 0-100
  listener_mode_requirements:
    causal: PASS|NOT_REQUIRED
    codal: PASS|NOT_REQUIRED
    sonic_identity: PASS|NOT_REQUIRED
  start_anchor: semantic_anchor
  end_anchor: semantic_anchor|null
```

### 1.5 EvocativeDetailGate
```yaml
EvocativeDetailGate:
  cue_id: string
  identifies_action_body_object_place_status_relationship_clue_rhythm_transition: boolean
  most_evocative_useful_detail: boolean
  masks_more_important_element: boolean
  likely_false_plot_signal: boolean
  decision: KEEP|REDUCE|OMIT|REDESIGN
  reason: string
```

Fail closed: if `masks_more_important_element=true` or `likely_false_plot_signal=true`, cue cannot auto-lock.

### 1.6 MixFocusPlan
```yaml
MixFocusPlan:
  beat_id: string
  focus_owner: string
  secondary_support: [string]
  background: [string]
  masking_budget: LOW|MEDIUM|HIGH
  density: 0.0-1.0
  width: MONO|NARROW|MEDIUM|WIDE|BINAURAL_SPECIFIC
  frequency_conflicts: [string]
  dynamic_conflicts: [string]
  action_reaction_split: boolean
```

### 1.7 MixAutomationEvent
```yaml
MixAutomationEvent:
  event_id: string
  target_bus_or_asset: string
  parameter: LEVEL|PAN|WIDTH|REVERB_SEND|DELAY|EQ|FILTER|DENSITY|DUCKING|OCCLUSION|PROXIMITY|MUSIC_INTENSITY
  start_anchor: semantic_anchor
  end_anchor: semantic_anchor
  start_value: number|string
  end_value: number|string
  interpolation: STEP|LINEAR|EASE_IN|EASE_OUT|CUSTOM
  dramatic_reason: string
```

No absolute timestamp before real/synthetic alignment resolution.

### 1.8 ListeningModeQC
```yaml
ListeningModeQC:
  cue_id: string
  causal_inference_expected: string|null
  causal_result: PASS|FAIL|N/A
  codal_message_expected: string|null
  codal_result: PASS|FAIL|N/A
  sonic_identity_expected: string|null
  sonic_identity_result: PASS|FAIL|N/A
  unintended_interpretations: [string]
  action: ACCEPT|REPAIR|REPLACE|REMOVE
```

### 1.9 PlaybackRealityQC
```yaml
PlaybackRealityQC:
  master_id: string
  headphone: PASS|FAIL|N/A
  earbuds: PASS|FAIL|N/A
  phone_speaker: PASS|FAIL|N/A
  mono: PASS|FAIL|N/A
  low_volume: PASS|FAIL|N/A
  casual_attention: PASS|FAIL|N/A
  speed_1_25x: PASS|FAIL|N/A
  comprehension_failures: [string]
  spatial_failures: [string]
  release_gate: GO|NO_GO
```

---

## 2. UPDATED COMPILER ORDER

```text
LOCKED STORY
→ STORY/CANON AUTHORITY CHECK
→ SCENE CHANGE MAP
→ LISTENER CONTRACT
→ DRAMATIC FORCE MAP
→ PERFORMANCE OBJECTIVES/TACTICS
→ UNHEARD-WORLD CONTEXT
→ PAUSE/BREATH/LISTENING PLAN
→ BLOCKING/MIC PERSPECTIVE
→ SOUND CUE GENERATION
→ EVOCATIVE DETAIL FILTER
→ SIGNIFICATION AUDIT
→ MUSIC DRAMATURGY
→ MIX FOCUS / MASKING PLAN
→ PROVIDER REQUEST COMPILATION
→ TAKES / ALIGNMENT
→ SEMANTIC-ANCHOR TIMELINE RESOLUTION
→ NARRATIVE AUTOMATION
→ PREMIX/STEMS
→ MASTER
→ THREE-MODE SOUND QC
→ PLAYBACK REALITY QC
→ HUMAN LISTEN
→ MASTER LOCK
```

---

## 3. PROMPT 2.2-A — LISTENER CONTRACT

**Input:** locked scene, current canon, previous scene exit state.

For every beat, determine:
1. What must the listener understand by the end of this beat?
2. What emotion may be invited but must not be forced?
3. What question/desire should remain active?
4. Which layer owns attention?
5. Which layers must retreat?
6. What misunderstanding would damage story comprehension?

Output only structured ListenerContract objects.

Reject:
- mood-only answers;
- “make it cinematic”;
- effects without comprehension purpose;
- music as substitute for missing character action.

---

## 4. PROMPT 2.2-B — DRAMATIC FORCE MAP

Map only forces already present in story causality.

Candidate forces:
POWER, TRUST, DESIRE, FEAR, CONTROL, KNOWLEDGE, ISOLATION, CONNECTION.

For each scene:
- state at entry;
- turning point;
- state at exit;
- which force owns the climax;
- where sound should support, counterpoint or remain neutral.

Do not invent a theme to justify a leitmotif.

---

## 5. PROMPT 2.2-C — ACTOR UNHEARD-WORLD CONTEXT

For every render block, provide only information the performer needs to behave truthfully:
- what just happened;
- what the character heard;
- partner physical action;
- relevant offscreen sound/event;
- object in use;
- distance/orientation;
- what reply/action the character expects next;
- playable objective and tactic;
- breath function if any.

Do not tell the performer the audience’s future knowledge.
Do not leak mystery solutions.
Do not use abstract emotional adjectives where action is possible.

---

## 6. PROMPT 2.2-D — MICROTEXTURE / EVOCATIVE DETAIL FILTER

Audit every proposed breath, swallow, lip sound, bite, chew, sip, gulp, utensil, plate, fabric, hair, chair, bed, skin contact, footstep, packaging or similar microtexture.

For each cue answer:
- physical cause;
- story function;
- why this detail rather than five literal neighboring sounds;
- whether it competes with dialogue/clue/music;
- whether it may be mistaken for plot information;
- KEEP / REDUCE / OMIT / REDESIGN.

Hard rule: premium realism comes from selective specificity, not maximum quantity.

---

## 7. PROMPT 2.2-E — SOUND SIGNIFICATION AUDIT

For every IMPORTANT/CLUE/PROTECTED sound:
- literal physical meaning;
- likely emotional/cultural implication;
- unintended possible reading;
- forbidden reading under canon;
- whether context makes the intended reading unambiguous enough.

Examples of forbidden accidental coding may include:
GUILT, SUPERNATURALITY, ROMANCE, THREAT, COMEDY, STATUS, CLUE IMPORTANCE.

If the cue prejudges an unresolved story question, redesign it.

---

## 8. PROMPT 2.2-F — THREE LISTENING MODES QC

Evaluate critical cue in context, not by filename.

CAUSAL:
What physical source/event will a first-time listener infer?

CODAL:
If cue carries speech/code/signal, what exact message will be decoded?

SONIC IDENTITY:
Which audible traits make this cue distinguishable from nearby cues?

Return PASS/FAIL/N/A plus smallest repair.

---

## 9. PROMPT 2.2-G — AUDIO ORCHESTRATION / MASKING

For every beat, assign:
- foreground owner;
- secondary support;
- background;
- elements to suppress;
- frequency conflicts;
- transient conflicts;
- width conflicts;
- reverb-depth conflicts;
- whether action and emotional reaction should be separated.

Prefer subtraction before EQ gymnastics when two layers have equal narrative rank only because of overproduction.

---

## 10. PROMPT 2.2-H — NARRATIVE AUTOMATION

After alignment is resolved, convert semantic changes into automation.

Allowed targets:
LEVEL, PAN, WIDTH, REVERB_SEND, DELAY, EQ, FILTER, DENSITY, DUCKING, OCCLUSION, PROXIMITY, MUSIC_INTENSITY.

Every automation event requires a dramatic reason and semantic start/end anchors.
Reject continuous motion that exists only to make the mix feel busy.

---

## 11. PROMPT 2.2-I — READ-ALOUD / PERFORMABILITY GATE

Without rewriting source by default, flag only demonstrated spoken problems:
- homophone ambiguity;
- unplayable syntax;
- unclear referent;
- impossible breath grouping;
- tongue-twist/pronunciation collision;
- excessive information density;
- punctuation that creates false performance.

Output:
`TEXT_ID | PROBLEM | LISTENING FAILURE | MINIMUM REPAIR | SOURCE CHANGE REQUIRED?`

If source change is not required, solve in performance/editing instead.

---

## 12. PROMPT 2.2-J — PLAYBACK REALITY QC

Test the finished mix/master against the project-required subset:
- headphones;
- earbuds;
- phone speaker;
- mono;
- low volume;
- casual attention;
- 1.25x playback.

For each test, ask only:
- dialogue intelligibility;
- clue survival;
- scene geography;
- excessive fatigue;
- music masking;
- silence mistaken for failure;
- stereo-only causality;
- microtexture becoming distracting/repulsive;
- emotional intent surviving without overstatement.

Return smallest repair list. Do not reopen story unless a true comprehension failure traces back to text.

---

## 13. ELEVENLABS / PROVIDER COMPILATION RULE

The provider adapter receives only supported, actionable direction.

Compile from:
`EXACT_TEXT + CHARACTER + OBJECTIVE + TACTIC + STATUS + ENERGY + TEMPO + BREATH + PAUSE + PROXIMITY + UNHEARD_WORLD_CONTEXT + PRONUNCIATION + TAKE_POLICY`.

Do not send universal canon prose to provider APIs.
Do not depend on provider-specific hidden behavior for canon-critical timing or clue identity.
Selective regeneration boundary remains the smallest failed render block.

---

## 14. ACCEPTANCE GATES ADDED BY v2.2

A production is NO-GO if any critical beat has:
- no ListenerContract;
- ambiguous focus ownership that masks required dialogue/clue;
- microtexture clutter causing false plot signals;
- clue sound failing required causal/codal/sonic-identity mode;
- actor performance generated without necessary partner/offscreen context;
- spatial causality that disappears in mono;
- automation without resolved alignment anchors;
- music/SFX/dialogue competing at equal foreground priority;
- playback-reality comprehension failure;
- project overlay overriding locked story canon.

**v2.2 result:** additive machine authority. Use with v2.1 base contract and prompt stack.