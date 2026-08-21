# IVDIVO MICROPHONE CHOREOGRAPHY ENGINE — PROMPT STACK v2.0

**Status:** UNIVERSAL ADDITIVE EXECUTION PROMPTS / v3.3-COMPATIBLE  
**Supersedes for new choreography planning:** `IVDIVO_MICROPHONE_CHOREOGRAPHY_PROMPT_STACK_v1.0.md`  
**Compatibility:** preserves MC-00…MC-15 functions and adds MC-16…MC-31.  
**Scope:** audio drama, dramatized audiobook, multi-voice fiction, hybrid AI/human audio production.

## Global laws

- Story/project authority outranks choreography.
- Movement must have dramatic, physical, informational, or relationship causality.
- Space is not reducible to pan/volume.
- Voice, body, Foley, object handling, room response and microphone perspective must describe one coherent body/world.
- Do not invent exact XYZ dimensions, absolute timestamps, provider evidence, or live-render results.
- Use semantic anchors until accepted live alignment exists.
- Ear-specific intimacy requires both technical topology and story authorization.
- If a clue or spoken fact conflicts with movement, Foley, music or spatial spectacle, comprehension wins.
- Fail closed on ambiguous source, geometry, identity, timing, or current execution authority.

## MC-00 MASTER DIRECTOR
Input locked scene, Listener Contract, Actor Director Score, Acoustic Passport, Foley plan, capture mode, current project state. Build one coherent choreography plan. Return `CHOREOGRAPHY_SCORE + TRAJECTORIES + CAPTURE_PLAN + SPATIAL_INTENT + FOLEY_LINKS + GATES`. Never treat motion as decoration.

## MC-01 CAPTURE MODE SELECTOR
Choose `REAL_STAGE / VIRTUAL_STAGE / HYBRID_STAGE`. Evaluate ensemble value, selective regeneration, room suitability, repeatability, provider/TTS use, real microphone availability and editability. State why the selected mode serves story and production risk.

## MC-02 LISTENER POINT + CAPTURE TOPOLOGY
Define listener/POA position and orientation first. Choose `MONO_CENTER_MIC / STEREO_PAIR / BINAURAL_HEAD / MULTI_MIC_ISO / VIRTUAL_BINAURAL / VIRTUAL_STEREO`. FAIL when promised localization exceeds topology capability.

## MC-03 FLOOR PLAN
Map room bounds, doors, windows, walls, furniture, story objects, listener/POA, microphones and actor start/end zones. If dimensions are unknown, use named semantic zones rather than fabricated metres.

## MC-04 ACTOR MOVEMENT CAUSALITY
For every move answer `WHY NOW / TRIGGER / WANT / TACTIC / STATUS CHANGE / LISTENER INFERENCE / REQUIRED END POSITION`. Reject random pacing, decorative circling and effects-first movement.

## MC-05 BODY + HEAD ORIENTATION
For every important beat define body direction, head direction, mouth/source direction and intended addressee. Turning is not the same as panning.

## MC-06 MICROPHONE TECHNIQUE — REAL STAGE
For real capture specify distance, live/dead/null zone, plosive risk, blocking risk, gain safety, iso backup, Foley interference and rehearsal marks. Return performer-readable blocking. N/A when no real-stage capture is authorized.

## MC-07 VIRTUAL TRAJECTORY
Create semantic keyframes: `ANCHOR / ZONE_OR_XYZ_IF_KNOWN / BODY_YAW_IF_KNOWN / HEAD_YAW_IF_KNOWN / MOVEMENT_STATE / PERFORMANCE_STATE / OCCLUSION / FOLEY_LINKS`. Interpolate continuously unless the scene cuts.

## MC-08 PERFORMANCE ↔ SPACE COMPATIBILITY
Check whether the vocal performance can physically support planned distance, effort, projection, confidentiality and movement. Return `PASS / RERENDER_PERFORMANCE / CHANGE_BLOCKING / POST_PROCESS_ONLY`. Never use processing to fake an incompatible performance state.

## MC-09 NEAR-EAR DIRECTOR
Use only if earned and technically supported. Define `EAR_TARGET / DISTANCE / STORY_FUNCTION / DURATION / RELATIONSHIP_STATUS / PERFORMANCE_BEHAVIOR / MONO_FALLBACK / HEADPHONE_SALIENCE_RISK`. Reject unearned intimacy or spectacle.

## MC-10 MOVEMENT + FOLEY COUPLER
Link each trajectory segment to footsteps, surface, cloth, object, door, chair and touch events. Voice and Foley must describe one continuous moving body.

## MC-11 ACOUSTIC CONSEQUENCE COMPILER
Translate geometry into renderer-neutral targets: distance gain, off-axis spectral change, room send, early reflections, occlusion, width and pan/binaural intent. Values are calibration targets unless physically measured.

## MC-12 MOVEMENT DURING SPEECH
For each relevant line choose `SPEAK_BEFORE_MOVE / SPEAK_DURING_MOVE / MOVE_AFTER_LINE / LINE_TRIGGERS_MOVE / MOVE_INTERRUPTS_LINE`. Bind to semantic anchors, not guessed timecodes.

## MC-13 REAL-STAGE REHEARSAL
When real actors/mics are used, run `TABLE STORY -> DRY BLOCKING -> MIC BLOCKING -> FOLEY COUPLING -> TECH REHEARSAL -> PERFORMANCE TAKE`. Return defects and smallest repair.

## MC-14 SPATIAL QC
Check geometry, continuity, head direction, voice-Foley coupling, mic pickup, intelligibility, mono survival, near-ear justification, automation smoothness, room coherence and topology capability. Grade `FATAL / MAJOR / MEDIUM / POLISH`.

## MC-15 MIX HANDOFF
Return renderer-neutral `SPATIAL_AUTOMATION_MANIFEST / ROOM_SEND_INTENT / HEAD_TURN_INTENT / OCCLUSION_INTENT / MOVEMENT_FOLEY_LINKS / NEAR_EAR_EVENTS / MONO_FALLBACK_RULES`. Do not invent final automation times before live alignment.

## MC-16 SOURCE + PROVENANCE LOCK
Before choreography, identify exact project authority, scene/script version, protected text, branch, current execution state, source hashes/IDs when available, and provenance class of recovered material. Return `SOURCE_LOCK PASS/FAIL`. Chat-only claims remain discovery until independently verified.

## MC-17 STORY + RELATIONSHIP FIREWALL
Check every spatial choice against clue causality, character knowledge, relationship timing, consent/intimacy state and protected story beats. Return forbidden spatial implications. Technical capability never authorizes a story implication by itself.

## MC-18 FOCUS OWNER + LISTENER COMPREHENSION
For each beat assign `FOCUS_OWNER` and `LISTENER_MUST_UNDERSTAND`. Decide which competing voice/SFX/Foley/music/movement elements must yield. A clue event may temporarily freeze or simplify blocking.

## MC-19 SILENT REACTION + STILLNESS SCORE
Treat stopping, waiting, looking, listening and withheld motion as playable actions. Map `TRIGGER -> SILENT RESPONSE -> DURATION_CLASS -> BODY_STATE -> NEXT_ENTRY_IMPULSE`. Do not add music/SFX merely because nobody speaks.

## MC-20 DEVICE-DOMAIN + OFFSCREEN SOURCE LOCALIZATION
For phones, cassette decks, radios, speakers, intercoms, doors and offscreen sources define physical source object/zone, acoustic domain, processing inheritance and listener localization. Recorded/replayed people must not float as present-room bodies.

## MC-21 CONTINUOUS BODY-PATH VALIDATOR
Track each character continuously across entrances, exits, room changes and returns. At every line/action ask whether the character can physically see, touch, hear or reach the referenced object/person from the current position. FAIL teleportation and impossible sightlines.

## MC-22 DISTANCE + PERSPECTIVE GRADIENT
Design approach/recede transitions using direct-to-reverberant ratio, spectral depth, level, occlusion and room change, not only pan. Preserve natural continuity and speech intelligibility.

## MC-23 OBJECT HANDOFF + CONTACT GEOMETRY
For evidence, cups, phones, keys, documents, tools and touch events define owner, start position, transfer path, receiving body/zone, handling sound and story function. Reject detached generic SFX that has no body/object continuity.

## MC-24 ENTRY / EXIT / DOORWAY DYNAMICS
For entrances/exits specify pre-entry audibility, door action, threshold position, approach/departure path, first/last address and resulting status shift. Avoid starting every actor at identical close-mic proximity.

## MC-25 MULTI-ROOM TRAJECTORY + SURFACE TRANSITION
For movement through connected spaces map route, floor/surface changes, acoustic transitions, offscreen intelligibility, destination source events and return path. A remote phone/voice must belong to its destination room.

## MC-26 FALSE-ROMANCE / UNEARNED-INTIMACY QC
Audit proximity, whispering, ear targeting, breath prominence, body blocking and stereo placement for unintended romantic/sexual coding. Return `PASS / REDUCE_INTIMACY / REBLOCK / FORBID_NEAR_EAR` based on current relationship authority.

## MC-27 MOVEMENT MASKING + CLUE BUDGET
For every clue/evidence line assign a masking budget. Suppress or simplify footsteps, cloth, object noise, ambience, music and spatial automation when they compete with required inference. Critical clue intelligibility must survive mono/mobile/1.25x where project policy requires.

## MC-28 MEDIA IDENTITY / SAME-PERFORMER-DIFFERENT-MEDIUM
When one character appears through multiple media, preserve performer identity while making the medium legible. Define what may change (`bandwidth/noise/room/device perspective`) and what must not (`age/person identity/core pronunciation unless story says so`).

## MC-29 SEMANTIC ANCHOR -> LIVE TIMELINE RESOLUTION
Convert semantic anchors to absolute automation only after accepted live alignment exists. Validate lineage from source unit -> rendered take -> normalized alignment -> resolved timeline. BLOCK if timing provenance is synthetic, stale or missing.

## MC-30 SELECTIVE REPAIR ROUTER
Given a demonstrated spatial/audio defect, locate earliest failed layer: `PERFORMANCE / BLOCKING / FOLEY / DEVICE DOMAIN / ACOUSTIC CONSEQUENCE / ALIGNMENT / MIX AUTOMATION / MASTER`. Prefer the smallest repair and preserve accepted downstream evidence where possible. Never rerender a whole episode by default.

## MC-31 FINAL CHOREOGRAPHY RELEASE GATE
Require source lock, topology capability, continuous body paths, relationship firewall, clue intelligibility, voice↔Foley coherence, device-domain identity, valid live timing where needed, mono/mobile survival, no open FATAL/MAJOR defects and required human listen. Return `GO / NO-GO / BLOCKED`, never aesthetic optimism.

## v2.0 acceptance rule

A project pass may execute all 32 prompts in planning/verification mode without authorizing provider spend or live render. Prompts that require unavailable real audio, live timing, real-stage capture or human listening must return `BLOCKED` or `N/A`, not fabricated completion.
