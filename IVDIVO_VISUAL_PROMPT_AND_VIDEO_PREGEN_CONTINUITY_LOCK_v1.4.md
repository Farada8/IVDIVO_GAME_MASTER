# IVDIVO — VISUAL PROMPT + VIDEO PRE-GENERATION CONTINUITY LOCK v1.4

**Established:** 2026-08-18
**Status:** CANON / UNIVERSAL VISUAL-VIDEO PRODUCTION STANDARD
**Applies to:** prompt writing, reference selection, image generation, intermediate still generation, image-to-video, keyframes, Runway/Kling workflows, trailers, Reels, covers, and all future visual production.

## WHY THIS PATCH EXISTS
Recent ROOM 917 tests showed that continuity failures begin BEFORE video generation. A pair can appear “close enough” while actually containing different character identity, hairstyle, wardrobe, body details, prop positions, camera geometry or background state. Once those contradictions enter the source images, no video prompt can reliably repair them.

Therefore continuity must be locked at the PROMPT AND STILL-GENERATION STAGE, not only at animation stage.

## PRIMARY LAW — CONTINUITY BEFORE PROMPT
Before writing a prompt for a new still, intermediate frame, or video pair, define the exact continuity state that must survive.

A prompt may not be written until the source/reference images pass the continuity gate below.

## CHARACTER CONTINUITY LOCK
For every recurring character in a continuous scene, verify and lock:
- exact face identity;
- apparent age;
- face width / jaw / nose / eye shape / hairline;
- exact hairstyle, parting, bun/ponytail/loose strands, hair volume and length;
- hair colour and texture;
- skin presentation;
- body proportions and apparent height;
- exact wardrobe family;
- exact garment cut, neckline, sleeves, jacket/shirt state;
- belt, waistband, trouser/skirt cut, pockets, seams and visible fasteners;
- jewellery/accessories;
- shoes if visible;
- wounds, wetness, dirt, makeup or other scene-state details.

“Same person in black clothes” is NOT sufficient continuity.

If face, hair or wardrobe materially differs, the images belong to different visual states unless the story explicitly establishes a change.

## HAIR IS CONTINUITY, NOT DECORATION
Hairstyle must be treated like wardrobe and props.
Reject or remake a pair if, without story reason:
- hair changes from tied to loose;
- bun height/shape changes materially;
- fringe/parting changes;
- curls/volume/length change;
- loose strands appear/disappear enough to read as a different styling;
- hairline or colour shifts.

Do not ask a video model to morph one hairstyle into another during a continuous scene.

## FACE IDENTITY GATE
Before using two stills as adjacent states, compare the face directly.
Reject or remake if the viewer could reasonably read them as different actors because of changes in:
- jaw shape;
- cheek width;
- nose bridge/tip;
- eye spacing/shape;
- brow shape;
- lips;
- hairline;
- apparent age;
- skin texture.

A prompt phrase such as “preserve identity” cannot recover identity that already differs in the source stills.

## WARDROBE DETAIL GATE
For continuous action, compare clothing at DETAIL LEVEL, not category level.
Lock:
- exact top/jacket/shirt/turtleneck;
- collar/neckline;
- buttons/zippers;
- cuffs/sleeves;
- belt and buckle;
- trouser/skirt cut;
- waistband height;
- pockets and seams;
- visible fabric texture;
- accessories.

If any of these materially changes between adjacent stills, reject the pair unless the costume change itself is the story beat.

## FULL VISUAL STATE PACKET
Before generating a still intended for video continuity, define:

`CHARACTER IDENTITY + HAIR + WARDROBE + BODY STATE + HAND STATE + PROP STATE + LOCATION + CAMERA + LIGHT + ACTION POSITION`

This packet is the continuity anchor.

Every intermediate still must inherit the same packet and change ONLY the intended micro-action.

## PROMPT WRITING LAW
Every prompt for a continuity still must explicitly separate:
1. WHAT MUST REMAIN IDENTICAL;
2. WHAT SINGLE ELEMENT MAY CHANGE;
3. HOW FAR THAT CHANGE progresses in this frame.

Template:

`Use Image 1 as the exact continuity base. Preserve the exact face identity, apparent age, hairstyle, hair arrangement, wardrobe including belt/waist/pockets/seams, body proportions, hand topology, props, room geometry, camera position, lens perspective and lighting. Use Image 2 only as a final-state reference. Create the immediately following moment. Change only [ONE MICRO-ACTION] by a small amount. Do not redesign face, hair, clothing, body, props, background or camera.`

## STILL SEQUENCE LAW
For complex motion, build:

`A → B → C → D`

Each next frame is generated from the PREVIOUS approved frame, while the final frame may be used only as a directional reference.

Do not assemble a continuity chain from four independently generated variants unless each one passes full identity/hair/wardrobe/object/camera compatibility.

## PRE-FLIGHT ORDER FOR ALL PAIRS
Before proposing ANY two frames for animation, inspect in this order:
1. face identity;
2. apparent age;
3. hairstyle/hair state;
4. exact wardrobe and clothing details;
5. body proportions;
6. camera/lens/crop;
7. background/location geometry;
8. props and object positions;
9. hands/fingers/contact;
10. lighting/shadows;
11. only then: intended movement.

If any earlier item fails, do not discuss motion yet.

## PROMPT-GENERATION GATE
The assistant/studio must NOT write or recommend a Runway/Nano Banana/Gen-4 video or intermediate-still prompt merely because the two images are aesthetically similar.

First state internally or in the audit:
`FACE PASS / HAIR PASS / WARDROBE PASS / CAMERA PASS / LOCATION PASS / PROP PASS / HAND PASS / LIGHT PASS`.

If any item is FAIL or QUESTION, the pair is not approved for continuous generation.

## REFERENCE IMAGE LAW
A reference image is not automatically safe just because it depicts the correct character or desired final pose.
A reference can contaminate the result with:
- a different face generation;
- different hairstyle;
- different wardrobe;
- different belt/pockets;
- different camera/lens;
- different lighting;
- different room state.

Therefore reference images must also pass continuity compatibility. If the final reference conflicts with the source, first remake a compatible final frame; do not use the conflicting image to steer intermediates.

## ROOM 917 LESSON — FRAMES 12/13
Frames 12 and 13 are **REJECTED AS A CONTINUOUS PAIR**.
The mismatch is not limited to hand movement. It includes visible differences in Elena’s wardrobe details and hair/identity presentation, plus smaller framing/background differences. The generated intermediate variants therefore cannot be trusted as a clean physical sequence.

Correct approach:
- choose one approved continuity anchor for Elena and Julian;
- remake the start and end states within the SAME identity, hair, wardrobe, camera and location packet;
- then create B/C intermediates from the previous approved still;
- only after still continuity passes, animate adjacent pairs.

## FINAL LAW
**CONTINUITY IS CREATED BEFORE VIDEO.**

The production order is:

`LOCK IDENTITY → LOCK HAIR → LOCK WARDROBE → LOCK CAMERA/LOCATION/PROPS → WRITE PROMPT → GENERATE STILL SEQUENCE → AUDIT → ANIMATE.`

Do not ask the model to repair contradictions that the production pipeline allowed into the source images.
