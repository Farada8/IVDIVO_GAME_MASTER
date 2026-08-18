# IVDIVO — RUNWAY SEQUENTIAL KEYFRAME CANON PATCH v1.2

**Established:** 2026-08-18
**Status:** CANON / UNIVERSAL VISUAL-VIDEO PRODUCTION STANDARD
**Applies to:** all Runway / image-to-video / keyframe workflows across IVDIVO.

## WHY THIS PATCH EXISTS
Two practical failures exposed a deeper production rule:
1. A first/last-frame pair can look similar overall while containing different object topology (for example, the telephone is in a different place on the desk).
2. Even when character identity is close, the model may not understand a large action jump and invent intermediate anatomy, hand positions, prop movement or camera continuity.

Therefore the previous assumption “compatible A + B is enough” is too permissive.

## PRIMARY LAW — SEQUENTIAL STILL CONTINUITY
For any character/prop action more complex than a tiny glance or nearly static environmental motion, do NOT jump directly from a distant state A to state B.

Build a short photographic action chain first:

`FRAME A → FRAME B → FRAME C → FRAME D`

Each adjacent pair must be visually and physically close enough that the next state is obvious to a human viewer without explanation.

The video model should interpolate SMALL MOTION, not invent the missing action.

## FOUR-KEYFRAME MICRO-SEQUENCE STANDARD
Default for controlled character/object actions:

- **A — START STATE**: stable pose, prop positions, camera, hands.
- **B — EARLY MOTION**: only one small change begins.
- **C — LATE MOTION**: same action progresses; all fixed objects remain fixed.
- **D — END STATE**: action resolves; no topology surprise.

Example: Elena notices a telephone.
- A: Elena looking at papers. Telephone fixed at desk position X.
- B: eyes shift toward phone; hands unchanged; phone still at X.
- C: head turns slightly; hands unchanged; phone still at X.
- D: attention fully on phone; hands unchanged; phone still at X.

Do NOT use a sequence where the telephone changes position, angle, scale, base, cord routing, handset position, or desk location unless that movement is the explicit action being shown and intermediate frames prove it.

## OBJECT POSITION LOCK
Before any A→B, B→C or C→D interpolation, compare all salient objects:
- exact desk position;
- orientation;
- scale;
- base/support;
- cable routing;
- contact points;
- object count;
- surrounding furniture geometry.

If a major object appears in a different place between adjacent stills, the pair is **REJECTED FOR INTERPOLATION**.

The prompt cannot repair a topology contradiction already present in the images.

## HAND / ACTION LOCK
Adjacent stills must preserve hand topology unless the hand movement itself is tiny and explicitly staged.

Reject a pair if between adjacent stills a hand:
- changes task abruptly;
- changes grip;
- releases or acquires an object without an intermediate state;
- crosses body space drastically;
- moves behind/in front of another object in a way the model must invent;
- changes finger visibility/orientation substantially.

For risky actions create more stills, not a longer prompt.

## CAMERA LOCK
Within one micro-sequence, keep approximately constant:
- lens / perspective;
- camera height;
- camera side;
- subject scale;
- horizon;
- room geometry.

If camera motion is required, it should itself progress gradually across A/B/C/D.
Do not combine a large camera move with a large character/prop move in the same interpolation.

## GENERATION RULE
Preferred execution:

1. Create/approve A, B, C, D stills first.
2. Audit each still with Gate 1.
3. Audit every adjacent pair for topology compatibility.
4. Animate **A→B**, **B→C**, **C→D** separately.
5. Use only the clean 1–3 second portions from each generation.
6. Assemble them in the editor.

If a tool only accepts first/last frames and forces long duration, still use adjacent close pairs; do not jump A→D.

## PROMPT RULE
Prompts are secondary to source compatibility.

A strong prompt CANNOT reliably rescue:
- telephone in two different places;
- changed hand task;
- changed furniture geometry;
- changed camera perspective;
- changed cable routing;
- changed character scale;
- missing intermediate action.

When source images contradict each other, regenerate the stills.

## PRE-FLIGHT QUESTION
Before every keyframe generation ask:

> “If these two stills were consecutive storyboard panels, would a human immediately understand the tiny physical movement between them without inventing an unseen action?”

If NO → reject the pair and create intermediate still(s).

## ROOM 917 LESSON — FRAMES 32/33
The original 32→33 pairing is **REJECTED AS A DIRECT KEYFRAME PAIR** because the telephone is not in the same physical desk position/topology across the two source images. This invalidates the interpolation regardless of prompt wording.

Correct approach: remake a four-still phone-attention micro-sequence with the exact same desk, telephone, handset, cord, papers, character positions, lens and lighting. Only Elena’s eye/head attention should progress across A/B/C/D.

## FINAL LAW
**STILL CONTINUITY BEFORE VIDEO CONTINUITY.**

If the still sequence does not already make physical sense, the video model must invent the missing physics. That is exactly where AI anomalies appear.

`CREATE THE MOVEMENT IN STILLS → VERIFY → THEN ANIMATE.`
