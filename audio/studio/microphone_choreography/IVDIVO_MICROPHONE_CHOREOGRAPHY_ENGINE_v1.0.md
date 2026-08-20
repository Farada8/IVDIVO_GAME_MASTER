# IVDIVO — MICROPHONE CHOREOGRAPHY / VIRTUAL RADIO STAGE ENGINE v1.0

**Status:** CANON / UNIVERSAL AUDIO PERFORMANCE-SPATIAL SYSTEM  
**Date:** 2026-08-20  
**Scope:** all IVDIVO audio dramas, dramatized audiobooks, doramas, audio-first fiction, trailers and scenes where actor movement/proximity/orientation carries dramatic information.  
**Authority:** additive below locked story/project authority and current Universal Audio Studio canon.

## 0. Why this system exists

Static close-mic speech plus later pan automation is not equivalent to a radio performance in which actors physically stand, move, turn, approach, withdraw, cross behind one another, speak over a shoulder, call across a room, or come close to one side of the listener.

The production model is split into three coordinated systems:

`SYSTEM A — PERFORMANCE ENGINE` — what the actor is doing psychologically and physically.

`SYSTEM B — MICROPHONE CHOREOGRAPHY / VIRTUAL RADIO STAGE` — where the actor is, where the listener/microphone is, which way actor and head are facing, how the actor moves, what the microphone hears, and how perspective changes.

`SYSTEM C — WORLD SOUND ENGINE` — Foley, objects, ambience, environmental sound, designed SFX and music.

Then: `A + B + C → EDIT → MIX → MASTER → QC`.

System B must not be reduced to PAN.

## 1. Professional basis

The reference library supports the core production premise:
- professional radio drama benefits from performers standing and moving rather than remaining fixed at a desk;
- the microphone is central to radio performance and actors must learn technique relative to its pickup behavior;
- radio performers can experiment with live/dead areas of directional microphones;
- body movement, physical exertion and emotional state affect breathing and therefore voice;
- Foley is itself a performance and movement should retain a natural flow rather than being chopped into arbitrary isolated cues.

These mechanisms are abstracted as production rules. Reference books remain REFERENCE ONLY, not story canon.

## 2. Three capture modes

### MODE R — REAL_STAGE
Actors genuinely perform spatial blocking around one or more real microphones.

Use when:
- live ensemble interaction is valuable;
- acoustic perspective should be captured physically;
- actors can rehearse controlled mic technique;
- the location/studio acoustics are suitable.

Outputs:
`ACTOR_FLOOR_PLAN / MIC_PLAN / MOVEMENT_SCORE / REHEARSAL_CUES / SAFETY_ZONES / GAIN_PLAN / ISO_BACKUP_POLICY`.

### MODE V — VIRTUAL_STAGE
Performances are captured/generated clean and spatial choreography is recreated in post.

Use when:
- TTS/AI voices are used;
- selective regeneration is required;
- precise repeatability is required;
- the scene may need different acoustic spaces later.

Outputs:
`SOURCE_TRAJECTORIES / ORIENTATION_CURVES / DISTANCE_CURVES / SPATIAL_AUTOMATION / ROOM_SEND_AUTOMATION / OCCLUSION_AUTOMATION / BINAURAL_OR_STEREO_RENDER_PLAN`.

### MODE H — HYBRID_STAGE
Performance includes physical vocal behavior while exact geometry is imposed in post.

Recommended default for premium AI drama.

The actor/TTS is directed to call, speak while turned away, lean close, answer after movement, etc.; the post system imposes exact distance, azimuth, room response and listener-relative trajectory.

## 3. Capture topology

A choreography plan must declare a capture topology.

### MONO_CENTER_MIC
Traditional point-focused radio capture. Useful for physical proximity/off-axis changes but cannot create true left-ear/right-ear localization by itself.

### STEREO_PAIR
XY / ORTF / other declared stereo pair. Can preserve left-right movement and room width.

### BINAURAL_HEAD
Listener-relative two-ear capture. Best for literal near-ear/behind-head effects if correctly staged.

### MULTI_MIC_ISO
Multiple microphones or iso channels preserve editability while actors perform ensemble blocking.

### VIRTUAL_BINAURAL
Clean source tracks rendered through virtual point-of-audition/HRTF or equivalent binaural renderer.

### VIRTUAL_STEREO
Clean source tracks rendered through controlled stereo position/depth/acoustic automation.

A scene requiring “different ears” cannot claim that result from a single mono microphone. The topology must support the promised perception.

## 4. Listener and microphone are not the same object

Define separately:
`LISTENER_POINT_OF_AUDITION` — where the implied listener exists.
`CAPTURE_MICROPHONE` — the real or simulated pickup device.

Fields:
`LISTENER_POSITION x/y/z`
`LISTENER_ORIENTATION yaw/pitch/roll`
`MIC_POSITION x/y/z`
`MIC_ORIENTATION yaw/pitch/roll`
`MIC_POLAR_PATTERN`
`MIC_DISTANCE_REFERENCE`
`CAPTURE_TOPOLOGY`.

## 5. Actor geometry state

At every meaningful choreography keyframe:
- ACTOR_ID
- SEMANTIC_ANCHOR
- POSITION_X/Y/Z
- BODY_YAW/PITCH/ROLL
- HEAD_YAW/PITCH/ROLL
- MOUTH_SOURCE_DIRECTION
- DISTANCE_TO_LISTENER
- DISTANCE_TO_MIC
- AZIMUTH_FROM_LISTENER
- ELEVATION_FROM_LISTENER
- MIC_INCIDENCE_ANGLE
- VOICE_TO_LISTENER_ANGLE
- MOVEMENT_STATE
- MOVEMENT_SPEED
- OCCLUSION_STATE
- BODY_STATE
- PERFORMANCE_STATE
- FOLEY_LINKS
- SPEECH_UNIT_LINKS.

Body direction and head direction are separate. A person can stand to the listener’s right while speaking away from the listener.

## 6. Choreography grammar

Allowed dramatic movement verbs:
`APPROACH / WITHDRAW / CROSS_LEFT_TO_RIGHT / CROSS_RIGHT_TO_LEFT / CIRCLE_CLOCKWISE / CIRCLE_COUNTERCLOCKWISE / PASS_BEHIND / PASS_IN_FRONT / LEAN_IN / LEAN_AWAY / TURN_TOWARD / TURN_AWAY / TURN_OVER_SHOULDER / SIT / STAND / KNEEL / LIE_DOWN / RISE / ENTER / EXIT / STOP / PACE / FREEZE / MOVE_TO_OBJECT / MOVE_BETWEEN_CHARACTERS / BLOCK_PATH / RETREAT_TO_DOOR / NEAR_EAR_LEFT / NEAR_EAR_RIGHT`.

Movement is chosen from story action, not from a desire to make stereo sound busy.

## 7. Movement must have dramatic cause

Every trajectory segment requires:
`WHY_MOVE_NOW`
`WHO_OR_WHAT_CAUSES_MOVE`
`WHAT_CHANGES_IN_RELATIONSHIP_OR_TASK`
`WHAT_LISTENER_SHOULD_INFER`
`END_POSITION_FUNCTION`.

Forbidden:
- random pacing because the mix feels static;
- circling the listener for spectacle without scene cause;
- constant left/right motion;
- near-ear intimacy before the relationship earns it;
- movement contradicting Foley/object geography.

## 8. Microphone-facing performance law

Actor direction and microphone geometry must agree.

Speaking toward partner, not microphone: actor can remain physically right while head rotates toward a partner left. Consequences may include reduced direct clarity, changed reflections and no arbitrary pan jump.

Calling across room: performance must contain real projection/energy appropriate to calling. Do not take a confidential close whisper and merely add reverb.

Near-ear confidential speech: performance uses controlled low projection and proximity-aware articulation; spatial layer supplies ear-specific placement/depth. No “sexy whisper” without story justification.

## 9. Real-stage microphone technique law

For REAL_STAGE:
1. actors rehearse the mic as part of blocking;
2. no actor/object unintentionally blocks a required pickup path;
3. movement paths include stopping zones and live/dead pickup zones;
4. director monitors intelligibility while preserving physical perspective;
5. actors do not chase the microphone unless scene blocking requires it;
6. gain riding cannot compensate for fundamentally wrong physical performance;
7. close proximity requires pop/plosive control;
8. floor/wardrobe/prop noise is planned;
9. clean/iso safety channel is recommended for story-critical speech when resources permit;
10. rehearsal decides whether movement is captured live or moved to post.

## 10. Virtual-stage acoustic consequences

The compiler emits control targets, not claims of perfect physical simulation.

Per keyframe it may derive:
- distance-gain target;
- stereo/binaural azimuth/elevation;
- direct/reverberant ratio target;
- early-reflection intensity;
- high-frequency distance attenuation;
- head-turn/off-axis spectral target;
- mic-pattern attenuation;
- occlusion attenuation/filter;
- width target;
- room-send target;
- optional near-field/proximity treatment;
- Foley perspective target.

All are renderer-neutral intents unless a project overlay binds a DSP implementation.

## 11. Distance law

Distance is not merely volume. It can alter direct level, room contribution, transient clarity, high-frequency content, apparent source size, early-reflection ratio, intelligibility, and proximity effect when warranted.

A planning compiler may use simplified inverse-distance estimates; final renderer is calibrated against the acoustic passport.

## 12. Head-turn / off-axis law

`POSITION ≠ VOICE_DIRECTION`.

Track body yaw, head yaw and mouth/source direction separately.

A head turn can alter directness, high-frequency clarity, consonant presence, apparent distance, room excitation and intelligibility. Do not fake a head turn with pan.

## 13. Microphone polar-pattern law

Declare:
`OMNI / CARDIOID / SUPERCARDIOID / HYPERCARDIOID / FIGURE_8 / SHOTGUN_APPROX / CUSTOM`.

The engine may estimate pickup attenuation by incidence angle but must mark it as a planning estimate. Final behavior depends on the real/profiled microphone.

Traditional live/dead areas are represented as:
`PICKUP_ZONE: PRIMARY / SECONDARY / NULL_OR_DEAD / REAR_LOBE / OUTSIDE_SAFE`.

## 14. Near-ear / behind-listener law

Near-ear effects are high-salience and sparse.

Before use:
- story reason;
- relationship/status reason;
- listener POV;
- topology supports it;
- headphone test;
- mono-safe semantic fallback;
- no accidental ASMR/disgust;
- no critical clue only in one ear.

Use:
`EAR_TARGET LEFT|RIGHT|BOTH|NONE`
`MIN_DISTANCE_CM`
`MAX_DURATION`
`INTIMACY_OR_THREAT_FUNCTION`
`MONO_FALLBACK`.

## 15. Movement + Foley coupling

Voice trajectory and body Foley must describe the same person.

For each movement segment:
- footstep cadence follows speed;
- surface matches acoustic passport;
- cloth follows body action;
- chair/door/object cue follows geometry;
- voice distance follows the same path;
- no teleporting voice between Foley positions.

Required link:
`TRAJECTORY_SEGMENT_ID ↔ FOLEY_MOVEMENT_CHAIN_ID`.

## 16. Movement + dialogue coupling

A line may begin before movement, continue during movement, end after movement, trigger movement, be interrupted by movement, or wait for movement to complete.

Use semantic anchors:
`BEFORE_LINE / LINE_START / MID_LINE_TOKEN / LINE_END / AFTER_LINE / BEFORE_ACTION / AFTER_ACTION`.

Do not invent absolute timestamps before accepted voice alignment.

## 17. Continuous movement law

Human movement is continuous. Do not render trajectory as unrelated static pans unless story explicitly cuts.

Interpolation:
`HOLD / LINEAR / EASE_IN / EASE_OUT / EASE_IN_OUT / CURVED_PATH / CUSTOM`.

For a walk, position, distance, orientation, voice directivity, Foley cadence and room-send curves must remain causally coherent.

## 18. Crossing law

When one actor crosses another:
- preserve front/behind relation;
- avoid identity confusion;
- account for temporary occlusion if plausible;
- do not swap ears instantaneously;
- keep critical words intelligible;
- do not exaggerate Doppler at ordinary walking speed.

## 19. Doppler law

Ordinary human walking around a microphone normally does not justify audible Doppler.

Use it only when relative velocity is high enough and physically/narratively warranted.

## 20. Real-stage rehearsal protocol

A — table/story: lock objectives/tactics/relationships.  
B — dry blocking: walk scene; confirm paths, collisions, objects, turns, proximity beats.  
C — microphone blocking: test live/dead zones, intelligibility, crossings, near/far balance, plosives, room response.  
D — Foley coupling: add live footsteps/objects/doors where needed.  
E — technical rehearsal: record full scene, review headphones/mono.  
F — performance take: preserve truthful interaction inside approved spatial boundaries.

## 21. AI/TTS hybrid protocol

1. compile performance state;
2. render clean voice blocks;
3. lock believable takes;
4. ingest real alignment;
5. resolve choreography anchors to timing;
6. generate continuous trajectories;
7. couple voice trajectory to Foley;
8. apply acoustic automation;
9. render stereo/binaural/mono-safe versions;
10. QC geometry against script/listener contract.

TTS is not asked to solve exact geometric motion.

## 22. Scene model

`VirtualRadioStageScene` includes:
scene_id, mode, capture_topology, acoustic_passport_id, listener, microphones, actors, objects, trajectories, near_ear_events, protected_spatial_rules.

## 23. Microphone model

Per mic:
mic_id, position, orientation, polar_pattern, capture_role, reference_distance_m, safe_min_distance_m, pickup_zone_map optional.

## 24. Actor trajectory model

Per trajectory:
actor_id, source_track_id, trajectory_id, semantic_start_anchor, semantic_end_anchor, interpolation, keyframes[anchor, position, body_yaw_deg, head_yaw_deg, body_state, performance_state, movement_state, occlusion].

## 25. Compiled spatial keyframe

Per compiled keyframe:
actor_id, trajectory_id, anchor, distance_listener_m, azimuth_listener_deg, elevation_listener_deg, distance_mic_m, mic_incidence_deg, voice_to_listener_angle_deg, estimated_distance_gain_db, estimated_mic_pattern_gain_db, estimated_head_offaxis_hf_loss_db, recommended_room_send, recommended_pan_fallback, ear_target, intelligibility_risk, foley_links.

## 26. Mix interface

System B hands the mixer:
`SPATIAL_AUTOMATION_MANIFEST`
`ROOM_SEND_AUTOMATION`
`OCCLUSION_AUTOMATION`
`HEAD_TURN_AUTOMATION`
`MOVEMENT_FOLEY_LINKS`
`NEAR_EAR_EVENTS`
`MONO_FALLBACK_RULES`.

The mixer may refine values but may not silently contradict blocking.

## 27. QC gates

Geometry:
- no unexplained teleport;
- no wall/closed-door crossing;
- actor/object geography agrees with staging.

Voice/Foley:
- steps and voice describe same path;
- object action occurs at correct place;
- voice orientation matches intended partner.

Microphone realism:
- real-stage actor stays in required usable pickup;
- virtual pattern changes plausible;
- no impossible near-field changes.

Listener:
- critical line survives movement;
- mono preserves meaning;
- ear-specific effects do not hide story.

Performance:
- movement has action cause;
- spatial trick does not replace acting;
- romantic/threat proximity is earned.

Technical:
- no automation clicks;
- continuous interpolation;
- fallback exists;
- head-turn filter does not destroy pronunciation;
- no excessive pumping.

## 28. Failure codes

`FAIL_STAGE_GEOMETRY`
`FAIL_ACTOR_TELEPORT`
`FAIL_MIC_BLOCKING`
`FAIL_MIC_PICKUP_ZONE`
`FAIL_VOICE_FOLEY_PATH_MISMATCH`
`FAIL_HEAD_ORIENTATION_MISMATCH`
`FAIL_UNEARNED_NEAR_EAR`
`FAIL_MONO_SPATIAL_MEANING_LOSS`
`FAIL_SPATIAL_INTELLIGIBILITY`
`FAIL_SPATIAL_AUTOMATION_CLICK`
`FAIL_ROOM_DISTANCE_INCOHERENCE`
`FAIL_TRAJECTORY_UNRESOLVED_ANCHOR`
`FAIL_CAPTURE_TOPOLOGY_MISMATCH`
`FAIL_SPATIAL_TRICK_REPLACES_PERFORMANCE`.

## 29. Canon integration

Universal audio studio now uses:

`PERFORMANCE ENGINE`
→ `MICROPHONE CHOREOGRAPHY / VIRTUAL RADIO STAGE ENGINE`
→ `WORLD SOUND ENGINE`
→ `EDIT / ALIGNMENT`
→ `MIX / MASTER / QC`.

For simple narrated audiobooks, System B may be NOT_APPLICABLE.
For premium dramatized work, System B is expected unless project deliberately chooses static narration.

## 30. Core law

Do not ask only: **Where should this voice be panned?**

Ask:

**Where is the person? Who are they speaking to? Which way are body and head facing? Why are they moving now? How does microphone/listener physically receive that action? What does the movement mean dramatically?**