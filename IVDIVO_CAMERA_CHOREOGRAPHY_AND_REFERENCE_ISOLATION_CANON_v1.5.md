# IVDIVO — CAMERA CHOREOGRAPHY + REFERENCE ISOLATION CANON v1.5

**Established:** 2026-08-18
**Status:** CANON / UNIVERSAL VISUAL-VIDEO PRODUCTION STANDARD
**Applies to:** Nano Banana / Gen-4 image generation, Runway/Kling image-to-video, keyframe workflows, trailers, Reels, covers, and all continuous visual scenes.

## PRIMARY LAW
Do not use every available image as an equal reference. Conflicting references can contaminate face identity, hairstyle, wardrobe, camera, lighting and props.

For a continuous scene, assign references by FUNCTION:
- IDENTITY REFERENCE — exact face;
- HAIR REFERENCE — exact hairstyle/hair state;
- WARDROBE REFERENCE — exact clothing state;
- LOCATION REFERENCE — room/architecture/props;
- CAMERA/COMPOSITION REFERENCE — desired angle/lens/crop;
- FINAL POSE REFERENCE — only when continuity-compatible.

If one image serves multiple functions, that is preferred. If references conflict, resolve the conflict before generation.

## CAMERA CHOREOGRAPHY LAW
Camera movement is a story action and must be staged with the same continuity discipline as character movement.

Do NOT combine:
- large character movement;
- large camera movement;
- hand/object interaction;
all in one interpolation.

Preferred design:
1. create a stable continuity anchor frame;
2. create a second still from a nearby camera position while preserving exact identity/hair/wardrobe/location/props;
3. keep character action minimal across the camera move;
4. animate the close camera states;
5. create separate character-action shots when the action itself is complex.

## SAFE CAMERA MOVE STANDARD
For short AI video, prefer one camera action per shot:
- 5–15° lateral arc/orbit;
- subtle dolly-in/dolly-out;
- small lateral truck;
- slow rack-focus when source topology supports it;
- minor height change.

Avoid demanding 30–90° viewpoint changes inside one interpolation unless a full sequence of compatible camera-position stills exists.

## CAMERA KEYFRAME SEQUENCE
For a controlled moving-camera shot, build:
`CAM A → CAM B → CAM C`
where each next camera position is close and physically obvious.

Example romantic two-shot:
- CAM A: 3/4 two-shot, Elena left, Julian right, both nearly still.
- CAM B: camera 8–10° to the side and slightly closer, same faces/hair/wardrobe/pose.
- CAM C: another 8–10° lateral shift, still same continuity packet.

Characters may add only micro-motion: eyes, breathing, tiny head change. Hand contact or major body movement is a separate micro-sequence.

## REFERENCE ISOLATION
Do not load several contradictory stills merely because they feature the same characters.
Before generation, choose the smallest reference set that fully locks the desired state.

Recommended maximum functional set:
- one best continuity/base image;
- one clean identity/hair reference per character only if needed;
- one compatible camera/composition target if needed.

Additional images are allowed only if they add non-conflicting information.

## STILL CREATION FOR VIDEO
When generating new photographs specifically for video, design them as storyboard/keyframe assets, not standalone posters.
Each still must declare:
`SHOT ID / CAMERA POSITION / CHARACTER STATE / HAIR / WARDROBE / HAND STATE / PROP STATE / LOCATION / LIGHT / NEXT INTENDED MOTION`.

A beautiful still that cannot connect cleanly to the previous/next state is not a production keyframe.

## PROMPT TEMPLATE — NEW CAMERA ANGLE, SAME CONTINUITY
`Use Image 1 as the exact continuity master for both characters, hairstyle, wardrobe, body proportions, room, props and lighting. Re-create the same immediate moment from a camera position approximately [X] degrees [left/right] of the source and [slightly closer/farther/lower/higher]. Preserve exact face identity, apparent age, hair arrangement, garment details, belt/waist/pockets/seams, hand state and all object positions. The characters remain almost motionless; only natural breathing and a tiny eye/head adjustment are allowed. This is a camera-position change, not a costume, pose or scene redesign.`

## PRODUCTION ORDER
`LOCK CONTINUITY MASTER → CHOOSE CAMERA PATH → GENERATE CLOSE CAMERA KEYFRAMES → AUDIT → ANIMATE CAMERA MOVE → CUT TO SEPARATE CHARACTER-ACTION SHOT.`

## FINAL LAW
**MOVE THE CAMERA OR MOVE THE ACTORS — DO NOT ASK THE MODEL TO SOLVE BOTH COMPLEXLY AT ONCE.**
Small actor micro-motion may accompany a camera move, but complex touch, object handling or body repositioning must be staged separately.
