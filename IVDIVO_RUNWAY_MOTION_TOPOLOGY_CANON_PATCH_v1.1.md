# IVDIVO — RUNWAY MOTION TOPOLOGY + HAND CONTINUITY CANON PATCH

**Version:** 1.1  
**Established:** 2026-08-18  
**Status:** CANON / UNIVERSAL PRODUCTION PATCH  
**Amends:** `IVDIVO_VISUAL_PRODUCTION_CANON_AND_RUNWAY_OS_v1.0.md`  
**Scope:** Runway / AI image-to-video / first-last-frame interpolation / short-form production / motion covers / trailers.

## WHY THIS PATCH EXISTS

Two production failures exposed missing gates:

1. **DISTANT FACE MAGNIFICATION FAILURE** — a small low-detail face in a still was enlarged by a camera push-in. The video model invented facial detail, changing age/identity.
2. **HAND FUNCTION / TOPOLOGY FAILURE** — first/last-frame interpolation forced a writing hand to change position/function. The hand jerked, duplicated and temporarily became anatomically impossible.

These are not cosmetic defects. They are production-invalid continuity failures.

---

## 1. MOTION TOPOLOGY GATE — REQUIRED BEFORE EVERY A→B GENERATION

Before using two stills as FIRST FRAME and LAST FRAME, compare them object-by-object.

Check:
- same character identity and apparent age;
- same wardrobe family;
- same lens/perspective family;
- same room geometry;
- same visible props;
- same hand count and approximate hand pose;
- same hand-to-object contact relationships;
- same telephone/base/cable relationships;
- same tool/cable topology;
- same dominant light sources;
- plausible physical path from A to B.

### HARD FAIL
Do NOT interpolate A→B if the transition requires the model to invent an intermediate state for:
- picking up or putting down a telephone receiver;
- releasing one object and grasping another;
- writing → stopping → re-gripping a pen;
- crossing hands;
- hands moving behind/through props;
- large hand rotation with fingers occluded;
- two people touching/separating;
- complex cable/tool relocation;
- face going from tiny/unclear to medium/close.

If HARD FAIL:
1. create a controlled intermediate still, OR
2. animate A and B separately and cut in edit.

Never solve topology mismatch by adding more prompt text.

---

## 2. HAND FUNCTION LOCK

Every visible hand must have one declared function for the shot.

Examples:
- `ELENA_RIGHT_HAND = resting on pen over plan; grip unchanged`
- `ELENA_LEFT_HAND = resting on paper; no lift`
- `JULIAN_BOTH_HANDS = holding book; grip unchanged`
- `PHONE_HANDSET = remains in cradle`

For a 2–4 second production shot, prefer:
- eye movement;
- small head turn;
- breathing;
- tiny posture shift;
- subtle camera movement;

instead of hand choreography.

A hand may perform **one small motivated action only** if the source image clearly contains enough anatomical information.

---

## 3. FROZEN-ZONE PROMPT RULE

Image-to-video prompts must explicitly freeze high-risk regions when they are not the subject of the shot.

Recommended language:

`Keep both hands anatomically stable and attached to their current objects. No finger reconfiguration, no grip change, no hand duplication, no hand crossing, no object pickup or release.`

For telephones:

`The handset remains fully seated in the cradle. The telephone stays fixed on the desk. No hand touches the receiver.`

For documents:

`Papers remain in the same order and position. Do not generate new readable text.`

For faces:

`Do not move the camera closer to any low-detail distant face. Keep distant faces the same size in frame; no new facial detail is revealed.`

---

## 4. DISTANT FACE MAGNIFICATION LAW

A source face that is small, soft, partially hidden or below reliable identity detail may not become larger during the generated shot.

Forbidden:
- push-in toward a tiny face;
- digital zoom that turns a distant figure into a medium shot;
- first/last interpolation where the same face changes greatly in pixel size;
- asking the model to “preserve identity” when the source does not contain enough identity information.

Allowed:
- lateral drift;
- static camera with environmental motion;
- pull-back;
- push toward an object while keeping the face distant;
- rear/over-shoulder silhouette.

---

## 5. BRIDGE-FRAME LAW

For character scenes, preferred production is:

`LOCKED STILL A → CONTROLLED BRIDGE STILL B → RUNWAY A→B → EDIT`

The bridge still must change only **one dramatic variable** whenever possible:
- gaze;
- head angle;
- focus of attention;
- small body lean;
- expression intensity.

Do not change simultaneously:
face + hands + prop + camera angle + lighting.

If more than one high-risk variable changes, split into separate shots.

---

## 6. 8-SECOND KEYFRAME APP RULE

If the Runway keyframe app forces an 8-second generation, **8 seconds is source material, not mandatory edit duration**.

Production may use only the clean 1.5–4 second interval.

Do not keep defective tail/head footage merely because the generation length is fixed.

Status examples:
- `PASS FULL`
- `PASS PARTIAL 00:00–00:03.2`
- `SALVAGE PARTIAL`
- `REJECT FULL`

---

## 7. FRAME-BY-FRAME MOTION QC

No generated clip is approved by watching it once at normal speed.

Inspect at least every ~0.25–0.5 sec for:
1. face identity / apparent age;
2. eyes / mouth;
3. hands / fingers;
4. hand-object contact;
5. telephone / cables / tools;
6. object teleportation;
7. architecture;
8. lights / shadows / reflections;
9. duplicate limbs/bodies;
10. unexpected story-significant anomaly.

A single obvious hand duplication, impossible grip, morph or unexplained clue can invalidate the full shot.

---

## 8. PROMPT COMPILER UPDATE

Before writing a Runway prompt, output internally:

`SHOT FUNCTION`  
`FIRST FRAME`  
`LAST FRAME`  
`MOTION TOPOLOGY = PASS/FAIL`  
`VISIBLE HANDS + FUNCTIONS`  
`HIGH-RISK OBJECTS`  
`FACE SCALE CHANGE`  
`ONE CHARACTER ACTION`  
`ONE CAMERA ACTION`  
`FROZEN ZONES`  
`END STATE`  
`QC FAILURE CONDITIONS`

Only then write the motion prompt.

### Universal prompt structure

`Continuous shot. [ONE camera movement]. [ONE low-risk subject change, preferably gaze/head/posture]. Keep [hands/high-risk props] anatomically and physically locked to their current objects throughout the transition. No grip change, no hand duplication, no finger reconfiguration, no object pickup/release. Preserve exact character identity, apparent age, wardrobe, room geometry, prop positions and motivated lighting. [Secondary environmental motion only]. No new people, no new objects, no readable generated text, no unexplained light, no supernatural effects unless explicitly canonical.`

---

## 9. RED TEAM ADDITIONS

For every proposed A→B pair ask:
- What must each visible hand do between A and B?
- Does the hand keep the same object/contact?
- Is a hidden intermediate grip required?
- Does any face become materially larger?
- Does camera motion force the model to invent detail?
- Can the same dramatic beat be achieved by moving only eyes/head/camera?
- Would an intermediate still eliminate the risky transformation?

If the answer exposes uncertain anatomy/topology, do not render the pair yet.

---

## 10. PRODUCTION LAW

**A stable simple shot is more valuable than an ambitious defective shot.**

AI video is not trusted to invent missing physical transitions. We pre-design those transitions in stills, then ask the model to animate the smallest possible change.
