# IVDIVO — CAMERA PARALLAX VERIFICATION PATCH v1.6

**Established:** 2026-08-18
**Status:** CANON / UNIVERSAL VISUAL-VIDEO PRODUCTION STANDARD
**Applies to:** still generation intended to simulate a changed camera angle, multi-view scene generation, Runway keyframe preparation, Nano Banana / Gen-4 reference workflows.

## WHY THIS PATCH EXISTS
A practical failure showed that an image model can satisfy a request for “camera moved left/right” by rotating or repositioning the characters while leaving the background effectively unchanged. This is not a camera move. It is subject re-blocking disguised as camera choreography.

## PRIMARY LAW — TRUE CAMERA MOVE REQUIRES PARALLAX
A generated alternate angle is valid only if the image proves a real camera-position change through background parallax and perspective change.

When the camera changes position while characters remain fixed in world space:
- background features shift relative to the characters;
- foreground/background overlap changes;
- doorframes, shelves, lamps, counters and wall lines change alignment behind bodies;
- visible side surfaces change in proportion;
- occlusions change naturally;
- perspective lines and relative spacing respond to the new camera position.

If the characters rotate/move but the background landmarks remain in essentially the same screen positions and relationships, mark **FAKE CAMERA MOVE / REJECT**.

## WORLD-SPACE LOCK
For camera-angle generation, characters are treated as frozen in 3D world coordinates unless the story explicitly requires simultaneous movement.

Lock:
- feet / body position in room;
- distance between characters;
- torso orientation;
- hand positions;
- face direction;
- wardrobe;
- hair;
- props.

Only the camera position and viewing angle should change.

## PARALLAX LANDMARK CHECK
Before generation, identify 3–5 visible landmarks, for example:
1. doorframe behind Julian;
2. cabinet/shelf edge behind Elena;
3. ceiling lamp position;
4. counter edge in foreground;
5. doorway / wall seam in depth.

After generation, compare where these landmarks sit relative to the characters.

At least two landmark relationships must visibly change in the physically expected direction. If not, the camera probably did not move.

## PROMPT LAW
Do not merely write “move camera 10 degrees left.” State the physical camera translation and the required parallax evidence.

Preferred language:
- “Keep both characters fixed in their exact world-space positions.”
- “Move the camera physically 40–60 cm to the left on a shallow arc around the pair.”
- “Do not rotate or reposition the characters to simulate the new view.”
- “Background parallax is mandatory.”
- “The doorframe must shift relative to Julian’s shoulder; the cabinet edge must shift relative to Elena; the ceiling lamp must move horizontally in frame according to the new viewpoint.”
- “Reconstruct newly revealed side surfaces and occlusions consistently.”

## ENDPOINT-FIRST CAMERA METHOD
If a small 8–12 degree request is too easy for the model to fake, first create a stronger verified endpoint, approximately 20–30 degrees from the master angle.

Then:
1. verify real parallax;
2. create intermediate camera views between the master and endpoint;
3. keep actors physically frozen;
4. animate adjacent camera views only.

This is safer than asking the model for multiple tiny angle changes that may be implemented as body rotation.

## CAMERA + ACTOR MOTION SEPARATION
Default production strategy:
- **Camera-motion shot:** actors nearly frozen; camera changes.
- **Actor-action shot:** camera nearly frozen; actor moves.

Combine large camera motion and large actor movement only after the continuity system is proven. Otherwise the model can hide errors by reallocating motion between camera, actor and background.

## VIDEO PREP GATE
Before a generated alternate angle can be used as a Runway keyframe, verify:
- same exact faces;
- same apparent ages;
- same hairstyle / hair volume / loose strands where visible;
- same exact wardrobe, belt, seams, pockets and fit;
- same body proportions;
- same props;
- same world-space character placement;
- real background parallax;
- plausible perspective / occlusion changes;
- no invented architecture.

## ROOM 917 LESSON
The attempted alternate-angle pair with Elena and Julian in the service/kitchen room is **REJECTED AS A TRUE CAMERA MOVE** because the background stayed effectively fixed while the characters changed pose/orientation. The generation represented actor repositioning, not camera translation.

## FINAL LAW
**CAMERA MOVEMENT IS PROVED BY PARALLAX, NOT BY A DIFFERENT LOOK AT THE ACTORS.**

If the background does not react to the requested camera translation, the camera did not truly move.
