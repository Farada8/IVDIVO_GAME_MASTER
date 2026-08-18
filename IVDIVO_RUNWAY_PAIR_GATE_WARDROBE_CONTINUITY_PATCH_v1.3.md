# IVDIVO — RUNWAY PAIR GATE + WARDROBE CONTINUITY PATCH v1.3

**Established:** 2026-08-18
**Status:** CANON / UNIVERSAL VISUAL-VIDEO PRODUCTION STANDARD
**Applies to:** all IVDIVO still-sequence, keyframe, image-to-video and Runway workflows.

## WHY THIS PATCH EXISTS
The ROOM 917 test using frames 12 and 13 exposed a failure that must be caught BEFORE prompt writing or image generation.

Frames can appear to show the same characters in the same scene while still being invalid as adjacent motion states. In 12→13, Elena's visible lower-garment geometry changes: belt/waist/pocket/trouser details are not continuous. Camera/framing and lighting/background details also shift. Generating intermediate frames forced the image model to reconcile incompatible clothing and scene geometry, creating a false continuity chain.

This is not a prompt problem. It is a SOURCE-PAIR SELECTION failure.

## PRIMARY LAW — PAIR GATE BEFORE PROMPT
No two stills may be proposed as adjacent video/keyframe states until they pass a side-by-side PAIR GATE.

Check, in this order:
1. SAME CHARACTER IDENTITY AND APPARENT AGE.
2. EXACT VISIBLE WARDROBE GEOMETRY.
3. SAME HAIR / ACCESSORIES.
4. SAME CAMERA SIDE / HEIGHT / LENS / SUBJECT SCALE.
5. SAME ROOM / BACKGROUND GEOMETRY.
6. SAME FIXED PROP POSITIONS AND CABLES.
7. COMPATIBLE HAND / FINGER / GRIP TOPOLOGY.
8. COMPATIBLE LIGHT SOURCES / SHADOW DIRECTION.
9. ONE SMALL, HUMAN-READABLE MOTION BETWEEN PANELS.

If any item materially fails, the pair is **REJECTED FOR INTERPOLATION** before any prompt is written.

## EXACT WARDROBE LOCK
For a continuous micro-sequence, “same wardrobe family” is NOT sufficient.

The following visible geometry must remain identical unless the wardrobe change is itself an explicitly staged action:
- belt present/absent and exact type;
- waistband height and closure;
- pockets and seams;
- trouser/jean cut and visible fabric structure;
- jacket open/closed state;
- shirt collar and cuff state;
- sleeve length/folds where salient;
- jewelry/accessories;
- shoes when visible.

Two frames where both characters are “wearing black” can still be incompatible.

A prompt cannot safely repair a wardrobe contradiction already present in the source images.

## MICRO-SEQUENCE DERIVATION LAW
For controlled motion, prefer one visual anchor and derive the sequence from it:

`A (ANCHOR) → B (child of A) → C (child of B) → D (child of C)`

An endpoint/reference image may guide the intended ACTION, but must NOT overwrite the anchor's wardrobe, room, camera, props or lighting.

If the desired endpoint has incompatible wardrobe/geometry, first REMAKE the endpoint to match the anchor. Only then build intermediate frames.

Do not construct a continuity chain from independently generated variants that each reinterpret clothing, pose or environment.

## ROOM 917 — FRAMES 12 / 13
**12→13 is REJECTED as a direct or reference-driven continuity pair.**

Reason:
- Elena's visible lower wardrobe is not continuous: belt/waist/pocket/trouser details differ;
- framing/camera relationship changes materially;
- lighting/background details are not identical enough for a controlled hand-touch interpolation;
- the intended hand action is already high risk.

The generated intermediate variants from this pair are therefore **REJECTED AS A PRODUCTION CONTINUITY CHAIN**. They may be viewed as exploratory stills only.

Correct options:
A. Use frame 12 as the visual anchor and generate the entire 4-frame hand-rise/touch sequence from frame 12 while locking its exact wardrobe, camera and room.
B. Remake frame 13 first so it matches frame 12 exactly in wardrobe/camera/room, changing only the intended final hand-contact pose; then generate intermediate descendants.

## PAIR-GATE OUTPUT REQUIREMENT
Before proposing any future pair, record mentally or explicitly:

`PAIR A/B | IDENTITY | WARDROBE | CAMERA | BACKGROUND | PROPS | HANDS | LIGHT | MOTION GAP | PASS/REJECT`

Do not recommend a pair based on dramatic usefulness before this gate passes.

## FINAL LAW
**CONTINUITY IS PIXEL-LEVEL PHYSICAL AGREEMENT, NOT THEMATIC SIMILARITY.**

If clothing, camera, room or prop geometry changes between supposedly adjacent stills, the model is being asked to invent a cut while pretending it is continuous motion.

`PAIR GATE → LOCK ONE ANCHOR → DERIVE NEAR-NEIGHBOR STILLS → AUDIT → ANIMATE.`
