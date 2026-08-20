# IVDIVO AUDIO REFERENCE INTELLIGENCE AUDIT — BATCH 2 v1.0

**Date:** 2026-08-20  
**Status:** REFERENCE INTELLIGENCE / EVIDENCE FOR CANON UPDATE  
**Scope:** universal audio production. Not project-specific story canon.

## Purpose
Deepen the first-pass audit using the supplied professional sources, with emphasis on performance truth, Foley as performance, spatial/microphone acting, mix automation, and practical embodied sound.

Pipeline:
`SOURCE → ABSTRACT MECHANISM → CROSS-SOURCE CHECK → RED TEAM → CANON/PROMPT/PROGRAM PATCH`.

Duplicates do not increase authority.

## Sources used in this pass
### A-TIER DIRECT
- James R. Alburger — *The Art of Voice Acting*, 6th ed. — deep pass on dialogue, character analysis, listening/responding, subtext, conversational delivery, microphone/proximity.
- Ric Viers — *The Sound Effects Bible* — deep pass on Foley performance, backgrounds, footsteps, prop performance, human/household sound, layering and location texture.
- Richard J. Hand & Mary Traynor — *The Radio Drama Handbook* — cross-check on microphone blocking, performance scale, director-as-conductor, acoustics/perspective and selective effects.
- Roey Izhaki — *Mixing Audio* — cross-check on time/frequency/level/stereo/depth domains, automation and mix interest.

### SUPPORTING
- David Sonnenschein — *Sound Design* — supports focus exchange and selective orchestration already accepted in Batch 1.
- Michel Chion — *Audio-Vision* — supports perspective/listening-context principles already accepted in Batch 1.

## Accepted mechanisms

### M21 — LISTEN AND ANSWER LAW
Believable dialogue is response, not isolated line delivery.

Every performance block must know:
- what the character just heard;
- what changed because of it;
- what response impulse is created;
- whether the character answers, delays, interrupts, overlaps, refuses or redirects.

IVDIVO fields:
`HEARD_EVENT / RESPONSE_IMPULSE / LISTENING_STATE / REPLY_MODE / ENTRY_TRIGGER`.

### M22 — WHOLE-SCENE DIALOGUE CONTEXT
A dialogue actor cannot be directed only from their own lines. The performer must understand the scene, partner intention and relevant turns.

IVDIVO consequence:
Provider blocks receive a concise `SCENE_CONTEXT_PACKET` with no future spoilers.

### M23 — SUBTEXT MUST COMPILE TO BEHAVIOR
Subtext is useful internally but unsafe as a raw provider instruction.

Compile:
`SUBTEXT → PLAYABLE BEHAVIOR → PROVIDER-SAFE DIRECTION`.

Example behaviors:
`delay reply / reduce projection / avoid eye-line equivalent through off-axis voice / shorten phrase ending / hold breath / answer too quickly / lower energy / step closer / withhold emphasis`.

### M24 — CONVERSATIONAL RHYTHM IS MULTI-SOURCE
Natural dialogue rhythm comes from response timing, overlap, stepping on lines, pauses and small vocal embellishment when justified.

No random fillers. No universal overlap quota.

### M25 — PROXIMITY IS PERFORMANCE, NOT ONLY MIX
Microphone distance changes intimacy and apparent environment. Close directional capture can become warmer/more intimate; greater distance exposes more room.

IVDIVO consequence:
`MIC_DISTANCE` and `ACOUSTIC_DISTANCE` must agree unless a deliberate stylization is documented.

### M26 — FOLEY IS A PERFORMANCE
Foley is not a library-drop operation. Timing, weight, character, material and intent make it convincing.

IVDIVO consequence:
Every meaningful Foley cue gains:
`PERFORMER_INTENT / CHARACTER_WEIGHT / ACTION_TEMPO / CONTACT_FORCE / MATERIAL_RESPONSE / SYNC_TOLERANCE`.

### M27 — CHARACTERIZED FOLEY
The same action should not always sound the same for every character.

Examples of legitimate variation:
- careful vs careless object placement;
- fast vs hesitant footsteps;
- controlled vs agitated cutlery;
- deliberate vs accidental clothing movement.

Do not over-characterize trivial sounds.

### M28 — DINNER / EATING ACTION CHAIN
Food scenes may use selected knife/fork, plate, bite, chew, swallow, drink and object-return sounds to create reality and character.

Important correction:
The action chain must alter dialogue behavior when physically relevant. A character with food in the mouth cannot sound acoustically identical to clean studio speech unless the cue is intentionally omitted.

IVDIVO fields:
`MOUTH_STATE / SPEECH_ALLOWED / SPEECH_IMPAIRMENT / SWALLOW_BEFORE_LINE / BREATH_RESET / UTENSIL_STATE`.

### M29 — BACKGROUND IS LOCATION, NOT EVENT
Background/ambience creates location and surrounding environment without being tied to one foreground action.

IVDIVO consequence:
Do not classify a story-triggering gust, impact or ring as generic ambience. Physical production class and story role stay separate.

### M30 — ROOM ACOUSTICS COMMUNICATE SPACE
Acoustics and perspective tell the listener where a scene exists and how characters relate spatially.

IVDIVO consequence:
Every scene requiring geography gets a `LISTENER_POINT_OF_AUDITION` plus room acoustic passport.

### M31 — LISTENER POINT OF AUDITION
Stereo/binaural staging needs an explicit listener viewpoint.

Fields:
`LISTENER_POSITION / LISTENER_ORIENTATION / POV_MODE / HEAD_RELATIVE_POSITIONS / MOVEMENT_RELATIVE_TO_LISTENER`.

Allowed POV modes:
`OBJECTIVE_SCENE / CHARACTER_SUBJECTIVE / DEVICE_MEDIATED / TRANSITIONAL`.

### M32 — DIRECTOR-AS-CONDUCTOR MODEL
Performance, Foley, music and technical layers are coordinated as one dramatic performance.

IVDIVO consequence:
The Audio Director owns cue hierarchy and beat timing; no department may independently maximize its layer.

### M33 — MIX ACTION SCORE
Automation is not post-production decoration. Complex mixes benefit from an action score tied to story beats.

Fields:
`BEAT / FOCUS_OWNER / LEVEL_MOVE / WIDTH_MOVE / DEPTH_MOVE / REVERB_MOVE / MUTE_OR_REVEAL / MUSIC_MOVE / REASON`.

### M34 — FIVE MIX DOMAINS
Every dense beat can be audited across:
`TIME / FREQUENCY / LEVEL / STEREO / DEPTH`.

Use these domains to resolve competition before resorting to arbitrary loudness changes.

### M35 — MIX OBJECTIVES
Mix QC should evaluate:
`MOOD / BALANCE / DEFINITION / INTEREST`, plus existing IVDIVO comprehension and story-intent gates.

### M36 — MICROTEXTURE DISGUST / FATIGUE GUARD
Close mouth, chewing, swallowing, fabric and body sounds can become disproportionately salient on headphones.

Therefore every intimate microtexture has:
`REPULSION_RISK / FATIGUE_RISK / HEADPHONE_GAIN_LIMIT / REPETITION_LIMIT`.

Unless body-horror/ASMR is explicitly authorized, ordinary realism must remain below conscious fixation.

### M37 — SPEECH-WHILE-ACTING PHYSICAL CONSISTENCY
Speech must inherit current body state:
`EATING / DRINKING / WALKING / RUNNING / LYING_DOWN / CRYING_RECOVERY / COLD / EXHAUSTED / WHISPER_DISTANCE / PHONE_DEVICE`.

If a separate provider render cannot reproduce body-state continuity, solve via isolated vocalization, edit, perspective processing or selective rerender.

### M38 — NO COPY-PUNCTUATION WORSHIP
Punctuation is not acting direction. Performance timing follows thought, intention, listening and action.

IVDIVO consequence:
Provider compiler may preserve exact text while ignoring misleading punctuation rhythm, unless punctuation is semantically protected.

## Red Team against v2.2

### MAJOR GAP A — listening state existed but response trigger was under-specified
FIX: `HEARD_EVENT / RESPONSE_IMPULSE / ENTRY_TRIGGER`.

### MAJOR GAP B — Foley causality existed but Foley performance identity was under-specified
FIX: `FOLEY_PERFORMANCE_STATE`.

### MAJOR GAP C — ear-specific staging lacked explicit listener viewpoint
FIX: `LISTENER_POINT_OF_AUDITION`.

### MAJOR GAP D — food microtexture existed but physical speech consequences were not mandatory
FIX: `MOUTH_STATE / SPEECH_ALLOWED / SWALLOW_BEFORE_LINE / BREATH_RESET`.

### MEDIUM GAP E — mix automation existed but lacked a compact action-score audit across five mix domains
FIX: `MIX_ACTION_SCORE` plus `TIME/FREQUENCY/LEVEL/STEREO/DEPTH`.

### MEDIUM GAP F — intimate microtexture needed explicit headphone repulsion/fatigue protection
FIX: microtexture salience guard.

## Rejected / not adopted
- continuous ad-libbing for “naturalness”;
- automatic filler insertion on every scene;
- hard stereo separation as a default dialogue style;
- Foley for every physically possible action;
- automatic audible chewing throughout food scenes;
- provider emotion tags as substitutes for playable direction;
- making every mix constantly move just because automation is available.

## Canon verdict
`PASS WITH ADDITIVE PATCH`.
Base v2.1 + v2.2 architecture remains valid. Adopt M21–M38 through universal v2.3 additive authority.
