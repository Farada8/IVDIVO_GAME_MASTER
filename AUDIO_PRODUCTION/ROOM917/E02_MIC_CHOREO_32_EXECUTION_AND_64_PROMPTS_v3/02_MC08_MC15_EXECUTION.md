# E02 `LENI-BIRD` — SEQUENTIAL EXECUTION MC-08…MC-15

## MC-08 PERFORMANCE ↔ SPACE COMPATIBILITY

**Question:** can the intended vocal performances physically support the proposed space and movement?

**Analysis:** E02 contains three performance-space regimes: close procedural evidence work, device-mediated historical playback, and a live remote test across two hotel zones. The largest failure risk is trying to create distance or intimacy entirely in post while the take itself sounds close, static or confidential in the wrong way.

**Execution:**
- Elena procedural/evidence lines: retain controlled close-to-working-distance performance; do not add breathy intimacy.
- Julian Scene 1: social-polish entry may begin lighter; fourth-note confrontation requires a contained reduction/stop rather than a loud dramatic push.
- Mina: movement-to-reception must be supported by projection/listening behavior consistent with increasing distance; if the take stays studio-close and confidential, rerender before spatialization.
- Cate cassette: performance remains human and ordinary; medium processing supplies historical/device identity, not ghost acting.
- Julian terminal/control beat in Scene 3: if staged nearer Elena, performance must remain professional/controlling rather than romantic.

**Decision rules:** `POST_PROCESS_ONLY` allowed for modest depth/medium changes; `RERENDER_PERFORMANCE` when projection, effort, confidentiality or breath state contradicts the body path.

**Status:** `PASS_WITH_CONSTRAINT`.

---

## MC-09 NEAR-EAR DIRECTOR

**Analysis:** Technical near-ear staging would create a high-salience intimacy cue. E02 relationship authority does not warrant it, and the fourth-note confrontation could be misread as erotic proximity rather than knowledge-risk.

**Execution:**
- Elena ↔ Julian near-ear: `FORBID_NEAR_EAR`.
- Cate cassette: may be perceptually intimate because headphones/device listening can feel close, but this is **media proximity**, not a live body at the listener's ear. Keep source anchored to cassette/device domain.
- Mina remote/reception: no near-ear treatment.

**Mono fallback:** all critical relationships and evidence remain legible without ear-specific placement.

**Status:** `REJECTED_BY_STORY_FOR_ELENA_JULIAN`; otherwise `N/A`.

---

## MC-10 MOVEMENT + FOLEY COUPLER

**Analysis:** Foley must prove the same body path as dialogue. E02 has several causal object/action opportunities that can make movement intelligible without narration.

**Execution — required/likely links:**
- Julian entry ↔ alcove door action ↔ two coffee cups set on hard surface.
- Optional Julian approach ↔ minimal footsteps/cloth only if not masking the fourth-note accusation.
- Mina office-intent ↔ optional first step/weight shift; if Elena stops her, movement Foley must stop with the action.
- sealed envelope slide ↔ paper/wood contact; avoid generic paper rustle disconnected from transfer.
- Scene 2 cassette ↔ deck handling / button / transport / tape mechanism where source authority permits.
- Scene 3 Mina route ↔ footsteps/surface transitions ↔ spatial recession ↔ modern desk phone source.
- Mina return ↔ approaching footsteps must resolve before/around her ability to see terminal; do not let return footsteps mask `Is that a seven?`.

**Masking law:** clue line > causal Foley > decorative Foley.

**Status:** `PASS`.

---

## MC-11 ACOUSTIC CONSEQUENCE COMPILER

**Analysis:** No measured room geometry exists, so absolute dB/reverb-time values would be fabricated. We can still define renderer-neutral relationships.

**Execution:**
- Scene 1 alcove: compact, material, technical work space; door threshold should be distinguishable from inner evidence zone. Julian entry increases directness as he enters; do not make room unnaturally cinematic.
- Scene 2 hotel room: device playback should have a stable physical deck source plus media-domain filtering. Live listener reactions remain in room domain; Cate remains in cassette domain.
- Scene 3: Mina recession should be carried by decreasing direct level, increasing room/distance signature and changing acoustic zone; modern reception phone belongs to reception, not old-board soundfield. Return reverses this gradient continuously.

**Renderer intents:** `DISTANCE_GAIN / OFF_AXIS_CHANGE / ROOM_SEND / EARLY_REFLECTION_CHANGE / OCCLUSION_IF_DOOR_OR_THRESHOLD / WIDTH / SOURCE_DOMAIN`.

**Status:** `PASS_WITH_CONSTRAINT`.

---

## MC-12 MOVEMENT DURING SPEECH

**Execution:**
- Julian's initial social entry lines may occur `SPEAK_DURING_ENTRY` only if speech remains intelligible and coffee placement does not mask key content.
- Fourth-note accusation: Elena `SPEAK_BEFORE_OR_AS_MOVEMENT_STOPS`; the accusation should own focus.
- Mina `I am going to the office` equivalent beat: `LINE_TRIGGERS_MOVE` is valid directorial staging.
- Elena `Stay. You are the independent witness`: `LINE_INTERRUPTS_MOVE` / `MOVE_STOPS_ON_LINE`.
- Envelope transfer: prefer `LINE_TRIGGERS_OBJECT_MOVE` or `MOVE_AFTER_LINE` according to exact text rhythm.
- Scene 2 `Headphones on / no one speaks` function: movement/handling resolves, then `LISTENING_STILLNESS`.
- Scene 3 Mina travel instructions: `LINE_TRIGGERS_MOVE`; remote exchange may continue while she is physically away only where the script supports audibility/communication.
- `Is that a seven?`: movement must have resolved enough for visual access; do not combine with loud arrival Foley.

**Status:** `PASS`.

---

## MC-13 REAL-STAGE REHEARSAL

**Analysis:** No authorized real-stage actors/mics are available in current E02 production state.

**Execution:** current branch = `NOT_APPLICABLE_CURRENTLY`. Preserve future rehearsal sequence only:
`TABLE STORY -> DRY BLOCKING -> MIC BLOCKING -> FOLEY COUPLING -> TECH REHEARSAL -> PERFORMANCE TAKE`.

Future acceptance focus: Julian entry/coffee without line masking; Mina full travel path; device/listener tableau; envelope transfer; terminal discovery; false-romance guard.

**Status:** `NOT_APPLICABLE_CURRENTLY`.

---

## MC-14 SPATIAL QC

**Audit:**
1. **Geometry:** semantic zones coherent; exact dimensions intentionally unknown — PASS.
2. **Continuity:** Mina's return before visual terminal line is mandatory — PASS as planned, must be verified in future render.
3. **Head/body direction:** defined semantically — PASS_WITH_CONSTRAINT.
4. **Voice↔Foley:** key causal couplings defined — PASS.
5. **Mic pickup:** virtual stage only; real-stage mic details N/A.
6. **Intelligibility:** clue masking budget required — PASS as design.
7. **Mono survival:** no clue depends on pan — PASS as policy.
8. **Near-ear:** Elena/Julian rejected — PASS firewall.
9. **Automation smoothness:** cannot verify without live timing/render — BLOCKED downstream, not current planning failure.
10. **Room coherence:** three spatial regimes clearly separated — PASS.

**Defects found:**
- `MEDIUM`: some recovered staging statements were previously phrased as script facts though they are directorial inference; corrected by evidence-grade system.
- `OPEN`: musical fourth-note identity remains dependent on shared pitch/contour authority; cannot fabricate E02 complete-lullaby relation while E01 fourth-note pitch gate is open.

**Status:** `PASS_WITH_OPEN_DOWNSTREAM_GATES`.

---

## MC-15 MIX HANDOFF

**Execution output — semantic handoff only:**

### Spatial automation intents
- Julian: door/threshold -> evidence zone; optional confrontation stop; no near-ear.
- Mina S1: witness-hold if exit initiation is staged.
- Scene 2: live room bodies static/low movement; cassette owns media source.
- Mina S3: old-board -> lobby -> reception -> return -> terminal-visibility zone.
- Julian S3: optional control-position approach only if later director lock accepts it.

### Room-send intents
- distinct alcove / hotel-room / lobby-reception acoustic domains;
- reception phone remains in modern reception domain;
- Cate remains cassette/media-domain source.

### Foley links
- door + coffee;
- optional footsteps/stop;
- envelope slide;
- cassette handling/transport;
- Mina travel + surface transitions;
- modern phone action;
- return/terminal access.

### Mono rules
- source identity through timbre/domain/timing/depth, not pan alone;
- clue lines dry/clear enough to survive mono/mobile;
- movement evidence may simplify before critical inference.

### Timing rule
No absolute automation timecodes until accepted E02 render/alignment exists.

**Status:** `PASS_WITH_CONSTRAINT`.
