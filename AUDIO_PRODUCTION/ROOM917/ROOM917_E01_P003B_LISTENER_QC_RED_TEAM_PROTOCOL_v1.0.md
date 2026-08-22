# ROOM 917 E01 — P003B LISTENER QC / RED TEAM PROTOCOL v1.0

**Status:** `READY_FOR_EXECUTION / HUMAN_LISTEN_NOT_YET_EXECUTED`  
**Story authority:** `THE INSURABLE FIRE`  
**Scope:** already assembled E01 audio only. No story rewrite, no broad rerender, no recast-by-taste.

## 1. Purpose

P003B is the downstream human/perceptual gate for an **assembled master**. It answers only:

1. Do I believe the actor?
2. Where does it sound like AI?
3. Where is the scene dead?
4. Is the geography understandable?
5. Does the mystery work?
6. Do SFX interfere with words?

Every failure must become a **timestamped, smallest-scope repair contract**. If a region works, mark `KEEP / DO NOT TOUCH`.

## 2. Authority / do-not-touch boundaries

- Scene 3 `07:24.980–10:58.190` is protected as current `v1.3E` technical staging/continuity lineage unless a new direct listen proves regression.
- Do **not** reapply the superseded v1.2.2 near-mono / disappearing-ambience / sequential-staging campaign to Scene 3.
- Pre-Scene3 `00:00–07:24.980` has one proven aggregate MAJOR: `D003 PRE_SCENE3_ROOM_BED_CONTINUITY_UNDERCOVERAGE`; exact patch intervals are unresolved.
- P003A-2 exact interval localization remains blocked until exact full-master bytes or a trusted exact interval map is available.
- Technical metrics, scripts, manifests and written reviews can never be substituted for this human listen.

## 3. Accepted input gate

Authoritative full-master identity expected:

- file: `ROOM917_E01_FULL_EVALUATION_MASTER_24BIT_48K.wav`
- duration: `658.190 s`
- sample rate: `48 kHz`
- PCM: `24-bit`
- channels: `stereo`
- expected SHA-256: `231c501e839e8f7f6ab72e3b556da43cae495913c172f6b7648b15a2ca3f88a8`

If exact bytes or a trustworthy identified derived audition file are not accessible, return:

`P003B = WAITING_FOR_AUDIO`

Never simulate a listen.

## 4. Blind listen procedure

### Pass A — story-free

Listen to audio without Director Score, cue sheet, actor notes or defect register. Mark only moments that break:

- belief;
- comprehension;
- spatial logic;
- mystery;
- speech clarity;
- emotional pull.

### Pass B — targeted verification

Only after Pass A, inspect authority around the flagged moments and classify the actual failure layer:

`PERFORMANCE / EDIT / MIX / SOUND_ASSET / UNKNOWN`

### Pass C — translation playback

Recheck proven failures and candidate repairs on:

- stereo headphones;
- ordinary speakers / mono;
- phone/mobile proxy.

A repair is not release-safe if it works only on one playback condition.

## 5. Six Listener QC questions

### Q1 — DO I BELIEVE THE ACTOR?

Flag only audible disbelief: wrong emotional onset, no reaction to partner, generic repeated cadence, over-signalled fear/seduction, implausible breath, status mismatch, or a line that sounds performed at the listener instead of used against/with another character.

Repair order:

`EDIT/TIMING CONTEXT -> smallest failed phrase/line/turn rerender -> RECAST only after repeated directed failures`

Never recast Elena or Julian because of a mix defect. Mina/Cate remain open to genuine human cast approval.

### Q2 — WHERE DOES IT SOUND LIKE AI?

Flag synthetic prosody, repeated sentence melody, unnatural emphasis, clipped/manufactured breath, emotion resetting at line boundaries, identical pause lengths, pronunciation artifacts, over-clean isolation, or montage rhythm exposing separate generated clips.

Classify source before repair. Never solve an edit/mix artifact by regenerating all dialogue.

### Q3 — WHERE IS THE SCENE DEAD?

A scene is dead only when the listener stops receiving pressure, expectation, relationship movement, physical consequence, or a meaningful authored pause.

`QUIET != DEAD`

For Scenes 1–2, distinguish authored space from missing physical-world support. The aggregate D003 evidence authorizes investigation, not blanket fill.

For a proven physical-world gap, repair in this order:

`ROOM / WEATHER / MATERIAL IDENTITY -> BODY / FOLEY / CAUSAL ACTION -> optional restrained MUSIC only if perceptual/commercial evidence proves need`

Music never supplies evidence.

### Q4 — IS THE GEOGRAPHY UNDERSTANDABLE?

The listener should infer stable relative positions and major transitions without a floor plan.

Check:

- room identity;
- distance;
- approach/recede;
- door/lift transitions;
- telephone as separate physical route;
- coherent actor movement.

Do not demand decorative stereo width. Demand usable spatial relationships and mono-compatible dialogue.

### Q5 — DOES THE MYSTERY WORK?

The listener must perceive the intended clue strongly enough to form the intended question without the mix announcing the answer.

Check in context:

- impossible call;
- acoustic mismatch;
- routing/relay behavior;
- lullaby material;
- missing-fourth-note relationship;
- Julian's involuntary reaction.

A clue that exists in a stem but is not perceived = FAIL.  
A clue exaggerated until it explains itself = FAIL.

The fourth-note relationship remains `OPEN` until human listening confirms recognizability or source-lineage proof plus listening closes it.

### Q6 — DO SFX INTERFERE WITH WORDS?

Dialogue and clue comprehension win over decorative sound.

Flag any SFX/Foley/ambience/music that masks:

- consonants;
- names;
- clue-critical numbers;
- relational pivots;
- start/end of an important line.

Also flag the inverse defect: physical reality dropping out so completely that speech sounds pasted into a vacuum.

`CLUE_SFX` remains immune to ambience/music ducking, but its loudness must still feel natural.

## 6. Severity

- `FATAL` — essential scene meaning/clue/dialogue cannot be understood, or false spatial/mystery inference breaks the episode.
- `MAJOR` — actor belief collapses for a substantial beat; persistent AI tell; meaningful dead span; consequential geography confusion; key clue weak/overstated.
- `MEDIUM` — localized real defect damaging polish or momentary comprehension without breaking the scene engine.
- `POLISH` — optional micro-improvement. Never authorizes broad rerender.

## 7. Defect record schema

Every finding must contain:

- `TIMECODE_START–END`
- `QUESTION_CLASS`: `ACTOR_BELIEF / AI_AUDIBLE / DEAD_SCENE / GEOGRAPHY / MYSTERY / SFX_MASKING`
- `SEVERITY`
- `CONFIDENCE`: `HIGH / MEDIUM / LOW`
- `WHAT_THE_LISTENER_ACTUALLY_HEARD`
- `WHY_IT_FAILS_THIS_SCENE`
- `SMALLEST_REPAIRABLE_ASSET_OR_MIX_REGION`
- `MINIMAL_FIX`
- `DO_NOT_TOUCH_BOUNDARY`
- `REGRESSION_TEST`
- `STATUS`: `KEEP / REPAIR / HOLD`

## 8. Patch contract law

- No patch from taste alone.
- No patch from low RMS alone.
- No whole-scene rerender when one take, cue, fade, pan automation, bed region or overlap can repair the failure.
- Dialogue rerender only for proven performance/pronunciation failure.
- Mix repair preferred for spacing, masking, over-isolation, room continuity or spatial placement.
- SFX regeneration only if the sound asset itself is wrong, not when gain/timing/position is wrong.
- Story text remains locked unless listening exposes a real story/continuity error and Founder explicitly reopens writing.
- Each patch invalidates only declared downstream outputs and must pass local regression.

## 9. Relationship to RU S0 human-listen gate

`ROOM917_RU_S0_LISTEN_GATE_v1.0.json` is an **upstream CAST/CANARY gate** before full RU E01 rendering. It answers whether a selected Russian voice and pair chemistry are credible enough to proceed.

P003B is a **downstream ASSEMBLED-MASTER gate** after dialogue, editing, SFX, ambience, spatial staging and mix interact.

Therefore:

- S0 PASS does not imply P003B PASS;
- a voice may pass S0 and later fail because the assembled edit/mix creates an AI tell;
- P003B must classify the earliest audible failure layer before authorizing a recast;
- P003B must not duplicate provider discovery or casting workflow;
- only failed voice blocks/pair tests are rerun upstream when the evidence actually points to performance/cast.

## 10. Release outcomes

- `KEEP` — tested region has no audible defect.
- `REPAIR` — one or more proven defects have selective patch contracts.
- `HOLD` — evidence/audio identity/access insufficient.
- `NO-GO` — at least one FATAL or unresolved release-blocking MAJOR remains.
- `GO` — actual assembled candidate passes human listening and all blocking repairs/regressions are closed.

## 11. Current frontier

- Scene 3 v1.3E technical lineage: `PROTECTED PASS`.
- Scene 3 fourth-note perceptual lock: `OPEN`.
- Mina/Cate human cast approval: `OPEN`.
- Pre-Scene3 D003 room-bed undercoverage: `PROVEN_AT_AGGREGATE_LEVEL`, exact intervals unresolved.
- P003A-2: `BLOCKED_ON_EXACT_MASTER_BYTES_OR_TRUSTED_EXACT_INTERVAL_MAP`.
- P003B: `READY_BUT_NOT_EXECUTED`.

**Next valid action when exact master bytes become accessible:** verify identity -> blind Pass A -> timestamp only actual audible failures -> Pass B failure-layer classification -> issue smallest selective repairs -> local regression -> Pass C translation playback.

Drive operational copy: `02_P003B_LISTENER_QC_RED_TEAM_PROTOCOL — ROOM917 E01 — v1.0`, file ID `1DE-eRwLtu7H6aZ_XiQ9OnrkwUIDLmBByVAbUzpIgBgU`.
