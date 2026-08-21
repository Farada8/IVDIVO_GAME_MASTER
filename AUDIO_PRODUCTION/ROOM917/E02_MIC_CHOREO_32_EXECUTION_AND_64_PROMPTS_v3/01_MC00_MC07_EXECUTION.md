# E02 `LENI-BIRD` — SEQUENTIAL EXECUTION MC-00…MC-07

## MC-00 MASTER DIRECTOR

**Input:** locked E02, current v3.3 audio authority, v2 choreography stack, current ROOM917 execution firewall.

**Analysis:** E02 has three distinct spatial dramaturgies: (1) evidence-work confrontation in the switchboard alcove; (2) controlled listening in Elena's hotel room; (3) a live technical test separating old switchboard from modern reception. The scene should not be staged as continuous stereo spectacle. The spatial story is about **who controls evidence, where evidence comes from, and when a person changes position because the information/status changes**.

**Execution:** establish one master rule: `STORY CAUSE -> BODY DECISION -> POSITION/ORIENTATION -> ACOUSTIC CONSEQUENCE -> FOLEY -> LISTENER INFERENCE`. Scene 1 uses restrained movement around an evidence work zone. Scene 2 reduces movement and transfers focus to the cassette/device domain. Scene 3 contains the largest justified trajectory: Mina physically separates old board from reception and later returns.

**Decision:** `HYBRID/VIRTUAL CHOREOGRAPHY PLAN`, semantic only until accepted E02 audio/alignment.

**Output:** 3-scene choreography architecture; no absolute coordinates/times; no near-ear; listener comprehension outranks motion.

**Status:** `PASS_WITH_CONSTRAINT`.

---

## MC-01 CAPTURE MODE SELECTOR

**Analysis:** Current production is AI/TTS-oriented with selective regeneration and post-render spatialization. Full real-stage capture would reduce editability and is not authorized. Pure mono/static TTS would fail the body/space goals. Pure binaural is unnecessary and could create intimacy not authorized by story.

**Execution:** select `HYBRID_STAGE` at system level: clean/selectively regenerable performances + explicit device/Foley assets + renderer-neutral virtual stage/acoustic automation. If a future human actor session occurs, it becomes an optional real-stage branch, not a prerequisite.

**Why this serves E02:** it preserves exact text and selective repair; keeps Cate's media identity controllable; lets Mina's reception movement be built without forcing all actors into one live room; keeps provider backend replaceable.

**Status:** `PASS`.

---

## MC-02 LISTENER POINT + CAPTURE TOPOLOGY

**Analysis:** E02 is Elena POV, but that does not mean literal first-person head binaural. The listener needs technical clarity and stable geography. Scene 3 works best if the listener broadly stays near Elena/old-board focus while Mina leaves; that makes distance itself evidence.

**Execution:** choose `VIRTUAL_STEREO` as default topology. Define listener point semantically, not numerically:

- S1 `LP-S1`: near the evidence-work zone, with door/threshold distinguishable from board/table.
- S2 `LP-S2`: near Elena/cassette work position but not identical to Elena's head.
- S3 `LP-S3`: remains primarily at old-board/Elena position while Mina travels toward reception and returns.

**Constraint:** no claim of left-ear/right-ear precision; no binaural promises from a stereo-only topology.

**Listener inference target:** “Mina really left this old circuit and reached the modern desk; the systems are physically separate.”

**Status:** `PASS_WITH_CONSTRAINT`.

---

## MC-03 FLOOR PLAN

**Analysis:** Script gives rooms and several source objects but not dimensions. Therefore build semantic zones and hard/soft relations only.

**Execution — Scene 1 semantic floor plan:**
- `S1_Z_BOARD`: old unpowered switchboard / evidence work.
- `S1_Z_TABLE`: evidence bags / seals / envelope work surface; may overlap operationally with board zone but keep object identity distinct.
- `S1_Z_DOOR`: alcove entrance; script-explicit door opening for Julian.
- `S1_Z_OFFICE_VECTOR`: direction toward office, inferred from Mina's stated intention; exact door/path not specified.

**Scene 2:**
- `S2_Z_DECK`: portable cassette deck / evidence source.
- `S2_Z_LISTEN`: live listener positions around device.
- `S2_Z_THRESHOLD_OPTIONAL`: optional Julian starting zone; `DIRECTORIAL_INFERENCE`, not script fact.
- room bounds/dimensions/furniture beyond explicit cassette/suitcase context remain unknown.

**Scene 3:**
- `S3_Z_OLD_BOARD`: switchboard/Elena test position.
- `S3_Z_ALCOVE_EXIT`: transition out of alcove.
- `S3_Z_LOBBY_TRANSIT`: script-explicit Mina walk through/into lobby.
- `S3_Z_RECEPTION`: modern front desk / modern phone source.
- `S3_Z_RETURN`: continuity-required path back to visual access of terminal.

**Status:** `PASS_WITH_CONSTRAINT`.

---

## MC-04 ACTOR MOVEMENT CAUSALITY

**Execution — Scene 1:**
- Julian enters because he brings “peace offerings” and joins an active evidence situation: `SCRIPT_EXPLICIT` entrance.
- A further approach toward Elena/work zone before `You knew the fourth note` is `DIRECTORIAL_INFERENCE`; use only if it sharpens confrontation.
- Physical stop on the accusation is `DIRECTORIAL_INFERENCE`; dramatically strong because status changes from social-management performance to exposed knowledge.
- Mina says she is going to the office: intention is `SCRIPT_EXPLICIT`; beginning to move is `DIRECTORIAL_INFERENCE`.
- Elena's `Stay. You are the independent witness` may arrest that movement; function = elevate Mina from colleague to formal witness.
- Envelope slide is `SCRIPT_EXPLICIT`; function = chain-of-custody/control transfer.

**Scene 2:**
- Movement should decrease when Elena orders headphones/no speech. Stillness is motivated by evidentiary attention.
- Any Julian threshold-to-listening movement is directorial, not factual; do not over-specify.

**Scene 3:**
- Mina travels to reception because Elena explicitly instructs her to do so: `SCRIPT_EXPLICIT`.
- Return to terminal proximity is `CONTINUITY_REQUIRED` by `Is that a seven?`.
- Julian closing distance at terminal discovery is optional `DIRECTORIAL_INFERENCE`; if used, purpose = control/intervention, not romance.

**Rejected:** wandering, circling, movement just to animate stereo.

**Status:** `PASS`.

---

## MC-05 BODY + HEAD ORIENTATION

**Execution:** use addressee/object orientation rather than fixed pan labels.

**S1:** Elena begins object-facing during evidence handling, then can turn toward Julian for fourth-note confrontation. Julian's orientation shifts from room/evidence entry to Elena when challenged. Mina alternates between evidence task and speakers; if she begins an exit, body can orient toward exit while head returns to Elena on `Stay`.

**S2:** Elena orients to deck during operation; live characters orient primarily toward the device during playback. Cate has no live body orientation in the room — source orientation belongs to the historical recording/device chain.

**S3:** Elena remains tool/board-facing for much of test; Mina's speaking direction changes with travel and reception task. At `Is that a seven?`, Mina must be oriented toward the revealed terminal. Julian may reorient toward Elena/terminal when control stakes rise.

**Constraint:** no degree/yaw values without a locked floor plan or renderer calibration.

**Status:** `PASS_WITH_CONSTRAINT`.

---

## MC-06 MICROPHONE TECHNIQUE — REAL STAGE

**Analysis:** no current real-stage recording authorization or mic inventory. A detailed physical mic plan would be invented evidence.

**Execution:** mark current branch `N/A`. Preserve a contingency rule only: if human actors are later recorded, doorway/distance states must be performed physically or with credible multi-mic/room capture; keep isolation backup for dialogue; do not let Foley handling contaminate irreplaceable clue lines; Cate cassette voice should be captured clean enough to derive distinct media versions from the same performer identity.

**Do not claim:** mic model, distance in cm, polar pattern, room measurement, rehearsal take.

**Status:** `NOT_APPLICABLE_CURRENTLY`.

---

## MC-07 VIRTUAL TRAJECTORY

**Execution:** define semantic keyframes, not fake XYZ/time.

**S1 keyframes:**
- `K1_JULIAN_PRE_ENTRY` -> outside/door-adjacent.
- `K2_JULIAN_DOOR_OPEN` -> threshold, `SCRIPT_EXPLICIT`.
- `K3_COFFEE_PLACE` -> work/table reach, `SCRIPT_EXPLICIT` object result; exact body path inferred.
- `K4_FOURTH_NOTE_PRESSURE` -> optional approach/stop, `DIRECTORIAL_INFERENCE`.
- `K5_MINA_OFFICE_INTENT` -> possible exit-initiation, `DIRECTORIAL_INFERENCE`.
- `K6_MINA_WITNESS_HOLD` -> returns/remains in witness zone.
- `K7_ENVELOPE_TRANSFER` -> across-table object action, `SCRIPT_EXPLICIT`.

**S2 keyframes:**
- `K8_DECK_READY` -> Elena at deck.
- `K9_LISTENING_TABLEAU` -> live bodies settle; `DIRECTORIAL_INFERENCE`.
- `K10_CATE_PLAYBACK_FOCUS` -> device owns source/focus.
- `K11_DECK_STOP` -> evidence playback ends.

**S3 keyframes:**
- `K12_MINA_LEAVES_ALCOVE` -> `SCRIPT_EXPLICIT` command/path start.
- `K13_LOBBY_TRANSIT` -> script supports walk/distant phone setup.
- `K14_RECEPTION` -> modern phone source; Mina remote.
- `K15_RETURN_TRANSIT` -> `CONTINUITY_REQUIRED`.
- `K16_TERMINAL_VISUAL_ACCESS` -> Mina near enough for `Is that a seven?`.
- `K17_JULIAN_CONTROL_POSITION` -> optional directorial approach/intervention.

**Output:** trajectory anchors ready for later alignment resolution.

**Status:** `PASS_WITH_CONSTRAINT`.
