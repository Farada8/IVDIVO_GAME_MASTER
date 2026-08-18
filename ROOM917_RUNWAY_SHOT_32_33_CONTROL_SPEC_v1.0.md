# ROOM 917 — RUNWAY SHOT 32→33 CONTROL SPEC

**Version:** 1.0  
**Established:** 2026-08-18  
**Status:** WORKING / PROJECT PRODUCTION CONTROL  
**Project:** ROOM 917 CALLS AT MIDNIGHT  
**Uses universal patch:** `IVDIVO_RUNWAY_MOTION_TOPOLOGY_CANON_PATCH_v1.1.md`

## PURPOSE

Create a controlled A→B keyframe transition from frame 32 to frame 33 for the desk / plans / fixed telephone sequence without repeating the hand-morphing failure seen in the previous keyframe test.

## STORY FUNCTION

Elena’s attention shifts from her work toward the fixed desk telephone / nearby anomaly. Julian remains in the same working situation. The beat is attention, not hand choreography.

## ABSOLUTE RULES

- No one picks up the phone.
- The handset stays seated in the cradle for the entire shot.
- The telephone stays fixed on the desk.
- Elena’s writing hand does not lift, re-grip, cross, duplicate or change function.
- If a pen is already in her hand, the grip remains the same.
- Julian keeps his hands attached to the existing book/documents; no page-turn if it requires re-gripping.
- No paper teleportation or newly readable text.
- No new lamp, glow or paranormal effect.
- The emotional change is carried by eyes/head/breath, not hands.

## MOTION PLAN

Preferred visible action:
1. camera makes a nearly imperceptible controlled drift;
2. Elena pauses visually and shifts only her gaze, then a very small head turn toward the telephone;
3. Julian makes only a tiny eye/head response;
4. hands remain functionally frozen;
5. telephone remains untouched.

## RUNWAY PROMPT

`Continuous restrained cinematic transition between the two existing keyframes. The dramatic change is only Elena’s attention: she keeps her writing hand anatomically stable in the same position over the existing paper, with the same pen grip and no lifting, re-gripping or finger reconfiguration, while her eyes shift first and then her head turns only slightly toward the fixed desk telephone. Julian remains in the same working posture and keeps both hands attached to the existing book or documents, with no page turn and no grip change; only a very small eye or head movement is allowed. The telephone stays completely fixed on the desk and the handset remains fully seated in the cradle for the entire shot. Keep all hands anatomically stable: no hand duplication, no extra fingers, no crossing hands, no object pickup or release. Preserve exact character identity, apparent age, wardrobe, desk geometry, paper positions, switchboard geometry and existing motivated practical lighting. Very subtle camera drift only. No new objects, no readable generated text, no new lights, no supernatural effects, no facial morphing, no object teleportation.`

## IF RUNWAY STILL FORCES HAND MOTION

Stop. Do not solve with a longer prompt.

The pair 32→33 is then MOTION-TOPOLOGY INCOMPATIBLE for direct interpolation.

Next method:
- regenerate frame 33 as a CONTROLLED BRIDGE FRAME from frame 32;
- keep both hands in exactly the same pose/contact as frame 32;
- change only Elena’s gaze/head direction;
- then animate 32→new33.

Alternative:
- animate 32 alone for 2–3 seconds with gaze/head change;
- cut to 33 separately.

## QC

Inspect the 8-second generated source at least every 0.25–0.5 seconds.

Reject if:
- writing hand jerks, doubles or changes grip;
- fingers appear/disappear;
- pen changes shape or location;
- handset lifts or vibrates into a new position;
- Julian’s book/documents change topology;
- a face changes identity/apparent age;
- papers gain salient readable AI text;
- any new light reads as a mystery clue.

Using only a clean 1.5–4 second section is allowed. The forced 8-second generation does not need to be used in full.
