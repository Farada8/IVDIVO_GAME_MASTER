# IVDIVO — AUDIO PROJECT OVERLAY TEMPLATE v1.1

**Status:** CURRENT TEMPLATE / instantiate per project  
**Parent authority:** `CURRENT_IVDIVO_AUDIO_PRODUCTION_AUTHORITY.md` + current Drive router  
**Designed for:** v3.3 consolidated audio authority and later compatible releases

> This template binds the universal audio-production system to one active project. It never creates or overrides story canon.

---

## 0. PROJECT / BUILD IDENTITY

**PROJECT_ID:**  
**TITLE:**  
**BOOK_OR_EPISODE:**  
**ACTIVE_BRANCH:**  
**STORY_STATUS:**  
**AUDIO_STATUS:**  
**DELIVERY_MODE:** NARRATED AUDIOBOOK / MULTI-VOICE AUDIOBOOK / DRAMATIZED AUDIOBOOK / FULL AUDIO DRAMA  
**PRIMARY_LANGUAGE:**  
**EDITORIAL_LANGUAGE:**  
**RELEASE_TARGETS:**  
**BUILD_ID:**  
**BUILD_MODE:** LIVE / DRY_RUN / MIXED  
**BUILD_MANIFEST_PATH:**

---

## 1. SOURCE AUTHORITY / PROTECTED TEXT

**SOURCE_FILE:**  
**SOURCE_VERSION:**  
**SOURCE_HASH_SHA256:**  
**TEXT_PROTECTION_MODE:** EXACT / ADAPTATION_AUTHORIZED / OTHER  
**UNIVERSAL_AUTHORITY_VERSION:**  
**PROJECT_OVERLAY_VERSION:**  
**VOICE_BINDING_LEDGER_VERSION:**  
**ACOUSTIC_IDENTITY_LEDGER_VERSION:**

Current authority chain:
1. Founder’s newest direct instruction.
2. Locked project/story authority.
3. Current universal audio authority.
4. This project overlay.
5. Current voice/pronunciation/acoustic locks.
6. Director Score / manifests / accepted assets.
7. Working production artifacts.

**CURRENT PROJECT AUTHORITY FILE(S):**  
**CURRENT SCRIPT/MANUSCRIPT SOURCE:**  
**CURRENT PRODUCTION MASTER:**  
**LAST VERIFIED:**

Fail closed if active branch, source hash/version or text-protection mode is ambiguous.

---

## 2. STATUS MAP / BLACKLIST

### CANON
-

### WORKING
-

### OPTION
-

### UNKNOWN
-

### REFERENCE ONLY
-

### SUPERSEDED
-

### REJECTED
-

### FORBIDDEN_BRANCHES_OR_TOKENS
-

Never infer current facts from a superseded branch.

---

## 3. DELIVERY CONTRACT / ADAPTATION LAW

**MODE:**  
**NARRATOR_PRESENT:** YES / NO  
**SPOKEN_TEXT_MAY_CHANGE:** YES / NO  
**ADAPTATION_DIFF_REQUIRED:** YES / NO  
**SFX_DENSITY:**  
**MUSIC_SCOPE:**  
**SPATIAL_SCOPE:**  
**TARGET_EPISODE/CHAPTER_LENGTH:**

For any authorized adaptation track:

`SOURCE_TEXT -> PERFORMANCE_VERSION -> REASON -> MEANING_CHANGE -> APPROVAL_REQUIRED`

Never hide adaptation inside actor/TTS direction.

---

## 4. LISTENER CONTRACT

For every important beat define:

**LISTENER_MUST_UNDERSTAND:**  
**LISTENER_MAY_FEEL:**  
**LISTENER_MUST_WAIT_FOR:**  
**FOCUS_OWNER:**  
**SECONDARY_SUPPORT:**  
**SUPPRESS:**  
**DANGEROUS_MISUNDERSTANDING:**  
**COMPREHENSION_CRITICAL:** YES / NO

Project-level listener promise:
-

---

## 5. DRAMATIC FORCE MAP

Track only forces earned by the story.

Useful fields:

`STATE_IN -> PRESSURE -> TURN -> STATE_OUT`

Possible forces:
`trust / distrust / desire / attraction / fear / suspicion / control / vulnerability / shame / knowledge / uncertainty / isolation / connection / urgency / grief / hope`

Project-specific force map:
-

---

## 6. CAST + VOICE BINDING LEDGER

For each recurring character:

**CHARACTER_ID:**  
**CHARACTER_NAME:**  
**STORY_FUNCTION:**  
**PERCEIVED_AGE:**  
**TIMBRE/WEIGHT:**  
**NORMAL_TEMPO:**  
**ARTICULATION:**  
**STATUS_BEHAVIOR:**  
**INTIMACY_BEHAVIOR:**  
**EMOTIONAL_RESTRAINT:**  
**HUMOR_PATTERN:**  
**LIE/CONCEALMENT_BEHAVIOR:**  
**SILENCE_STYLE:**  
**STRESS/FATIGUE_BEHAVIOR:**  
**PRONUNCIATION_NOTES:**  
**FORBIDDEN_CLICHES:**

Voice binding:

**PROVIDER:**  
**VOICE_ID:**  
**STATUS:** CANDIDATE / SMOKE_ONLY / APPROVED / LOCKED / SUPERSEDED  
**LOCKED_AT:**  
**LOCKED_BY_BUILD_ID:**  
**SAMPLE_EVIDENCE:**  
**PRONUNCIATION_VERSION:**  
**ALLOWED_SUBSTITUTION_POLICY:**

Any dispatched request that conflicts with a LOCKED binding fails closed unless an approved superseding binding exists.

---

## 7. PRONUNCIATION LOCKS

| TERM | REQUIRED PRONUNCIATION | PROVIDER FORM IF NEEDED | STATUS | NOTES |
|---|---|---|---|---|
| | | | | |

Include names, places, numbers, abbreviations, technical terms and recurring phrases.

---

## 8. PERFORMANCE DIRECTOR SCORE

For each important spoken/reactive unit:

`STATE_IN -> HEARD_EVENT -> RESPONSE_IMPULSE -> ENTRY_TRIGGER -> WANT -> TACTIC -> SUBTEXT -> PLAYABLE_BEHAVIOR -> LINE -> STATE_OUT -> NEXT_ENTRY_IMPULSE`

Playable behavior fields:
- reply speed;
- projection;
- phrase-ending behavior;
- breath function;
- hesitation;
- emphasis;
- orientation;
- distance;
- interruption pressure;
- withholding;
- listening activity;
- status change;
- body condition.

Do not send vague directions such as only “sad”, “sexy”, “cinematic” or “mysterious”. Translate psychology into playable behavior.

---

## 9. SILENT REACTION ANCHORS

When a dramaturgically necessary reaction has no spoken provider line, create:

**ANCHOR_ID:**  
**CHARACTER_ID:**  
**STATE_IN:**  
**TRIGGER_EVENT:**  
**SILENT_ACTION:**  
**OPTIONAL_BREATH_OR_FOLEY_REFS:**  
**SILENCE_POLICY:**  
**STATE_OUT:**  
**SEMANTIC_ANCHOR:**

Silent anchors do not count as spoken-text coverage unless a separate PERFORMANCE_SOUND request is explicitly attached.

---

## 10. MICROPHONE CHOREOGRAPHY / BLOCKING / PROXIMITY

For every important beat define:

**LISTENER_POINT_OF_AUDITION:**  
**CHARACTER_POSITION:**  
**ORIENTATION:**  
**DISTANCE:**  
**MOVEMENT_BEFORE_LINE:**  
**MOVEMENT_DURING_LINE:**  
**MOVEMENT_AFTER_LINE:**  
**PROJECTION_MODE:** close / conversational / across-room / through-medium / other  
**PROXIMITY_CHANGE:**  
**BODY_STATE:**  
**OCCLUSION:**  
**STEREO_INTENT:**  
**MONO-SAFE REQUIREMENT:**

A close confidential line and a line called across a room are different performances, not merely different gains.

---

## 11. ACOUSTIC PASSPORT / SPATIAL MAP

Per recurring space/location:

**SPACE_ID:**  
**PHYSICAL_SIZE:**  
**MATERIALS:**  
**EARLY_REFLECTION_CHARACTER:**  
**REVERB/DECAY CHARACTER:**  
**NOISE_FLOOR:**  
**DISTINCTIVE_BACKGROUND:**  
**LISTENER_P.O.A.:**  
**OCCLUSION/DOOR/WALL BEHAVIOR:**  
**STEREO_INTENT:**  
**MONO_FOLDDOWN_RISK:**  
**FORBIDDEN_FALSE_CLUES:**

---

## 12. FOLEY / BODY MICROTEXTURE

For every required performed action:

**FOLEY_ID:**  
**CAUSAL_ACTION:**  
**BODY/OBJECT SOURCE:**  
**MATERIAL:**  
**PERFORMER_STATE:**  
**TIMING RELATIVE TO SPEECH:**  
**DISTANCE/PROXIMITY:**  
**FOREGROUND/BACKGROUND:**  
**STORY_FUNCTION:**  
**MUST_NOT_MASK:**  
**LOCK_STATUS:**

Foley exists for body/action causality, not to fill silence.

---

## 13. SFX / CLUE / PROCEDURAL AUDIO

For each sound asset:

**ASSET_ID:**  
**STORY_FUNCTION:**  
**PHYSICAL_SOURCE:**  
**MATERIAL:**  
**DISTANCE:**  
**SPACE:**  
**DURATION:**  
**ONE_SHOT/LOOP:**  
**FOREGROUND/BACKGROUND:**  
**CLUE/NON_CLUE:**  
**MUST_BE_DISTINCT_FROM:**  
**GENERATION/RECORDING PROMPT:**  
**NEGATIVE PROMPT:**  
**MIX_PRIORITY:**  
**BLIND_TEST_QUESTION:**  
**STATUS:** WORKING / APPROVED / AUDIO_CANON_ASSET

For clue-critical sounds select for comprehension, physical believability, memorability and causal consistency—not maximum drama.

---

## 14. ACOUSTIC IDENTITY LEDGER

Use for any cross-domain identity that must remain stable across dialogue/SFX/music/device playback.

**IDENTITY_ID:**  
**TYPE:** timbre / pitch / rhythm / mechanism / device / other  
**SOURCE_ASSET:**  
**PITCH_IDENTITY if applicable:**  
**ALLOWED_VARIATION:**  
**FORBIDDEN_VARIATION:**  
**DEPENDENT_CUES:**  
**STATUS:**

---

## 15. AMBIENCE ARCHITECTURE

Ambience defines:
`PLACE / SIZE / MATERIAL / TIME / WEATHER / ACTIVITY / DISTANCE`

It must not invent plot.

Project ambience/room-tone registry:
-

---

## 16. MUSIC DRAMATURGY

Before any cue:

**VALUE_ALREADY_CHANGED:**  
**WHY_MUSIC_NOT_SILENCE:**  
**FOCUS_OWNER:**  
**CLUE_MASKING_RISK:**  
**FALSE_ROMANCE/GUILT/FEAR_IMPLICATION_RISK:**  
**CUE_FUNCTION:** BUTTON / TRANSITION / AFTERMATH / THEME RETURN / OTHER  
**NO_MUSIC_WINDOWS:**

Project music law:
-

---

## 17. RENDER BLOCK / PROVIDER COMPILATION

For each provider-bound block:

**BLOCK_ID:**  
**TEXT_UNIT_IDS:**  
**CHARACTER_ID:**  
**EXACT_TEXT:**  
**TEXT_HASH if required:**  
**VOICE_BINDING:**  
**PERFORMANCE_OBJECTIVE:**  
**TACTIC:**  
**SUBTEXT:**  
**STATUS:**  
**ENERGY:**  
**TEMPO:**  
**BREATH:**  
**PROXIMITY:**  
**ENTRY_TRIGGER:**  
**CRITICAL_WORD/CLUE:**  
**POST_CHAIN / ACOUSTIC_DOMAIN if applicable:**  
**DRY_RUN_REQUEST:**  
**PROVIDER_PREFLIGHT_STATUS:**

Important clue lines or differing post-processing/acoustic domains must be isolated when required by the current provider/machine contract.

---

## 18. TAKE / ASSET PROVENANCE

For reused material record:

**REUSED_FROM_BUILD_ID:**  
**ORIGINAL_TAKE_OR_ASSET_ID:**  
**PROVENANCE_CHAIN:**  
**REUSE_REASON:**  
**CURRENT_COMPATIBILITY_CHECK:**

A copied file with no provenance is not a locked reusable asset.

---

## 19. ALIGNMENT / TIMELINE

Provider-specific raw alignment must be normalized before internal timing decisions.

Track:
- RAW_ALIGNMENT;
- NORMALIZED_ALIGNMENT;
- SEMANTIC_ANCHORS;
- protected silence;
- silent reaction anchors;
- Foley/SFX/music relative anchors;
- resolved timeline version.

**TIMELINE_LOCK** only after all required upstream dialogue/assets for that timeline are locked.

---

## 20. MIX ACTION / CAUSAL OVERLAP / STEREO QC

Universal focus priority:
1. spoken clue / human action;
2. evidence sound required for causality;
3. body/action and room orientation;
4. protected emotional silence;
5. music.

Track:

**FOCUS_OWNER:**  
**SECONDARY_SUPPORT:**  
**SUPPRESS:**  
**CAUSAL_OVERLAP_PROFILE:**  
**SOURCE_STEREO_INTENT:**  
**STEM_STEREO_INTENT:**  
**STEREO_INTEGRITY_RESULT:**  
**MONO_FOLDDOWN_RESULT:**  
**PHONE_RESULT:**  
**LOW_VOLUME_RESULT:**  
**1.25X_RESULT:**

Critical clues may not depend on stereo alone.

---

## 21. MASTER PRODUCTION DAG / GATES

Track status explicitly:

- [ ] AUTHORITY_PASS
- [ ] DRAMATURGY_PASS
- [ ] STAGING_PASS
- [ ] PERFORMANCE_PLAN_PASS
- [ ] SOUND_PLAN_PASS
- [ ] MUSIC_PLAN_PASS
- [ ] DRY_RUN_PASS
- [ ] PROVIDER_PREFLIGHT_PASS
- [ ] HARD_PILOT_PASS
- [ ] DIALOGUE_LOCK
- [ ] ASSET_LOCK
- [ ] TIMELINE_LOCK
- [ ] MIX_PASS
- [ ] MASTER_TECH_PASS
- [ ] MACHINE_QC_PASS
- [ ] HUMAN_LISTEN_PASS
- [ ] MANUAL_REVIEW_RESOLVED
- [ ] RELEASE_GO
- [ ] MASTER_LOCK

Allowed `NOT_APPLICABLE` only with explicit delivery-mode/project reason.

Independent branches may run in parallel when their own upstream gates pass. They must converge before consumer stages requiring both.

---

## 22. QC / RELEASE FAIL-CLOSED

No DRY_RUN build may release.

Required conditions before release:
- current source/branch/protected text verified;
- voice bindings valid;
- provenance valid for reused assets;
- required LIVE evidence present;
- normalized alignment used;
- mandatory MANUAL_REVIEW resolved;
- open FATAL = 0;
- open MAJOR = 0;
- clue comprehension passes;
- stereo/mono/source-vs-stem integrity passes where applicable;
- human listen passes when required by release gate.

---

## 23. DEFECT REGISTER

For every defect record:

**BLOCK/TIMESTAMP:**  
**LAYER:** authority / source / voice binding / acting / pronunciation / text / edit / rhythm / proximity / Foley / SFX / ambience / processing / music / spatial / mix / mastering / QC / packaging  
**SEVERITY:** FATAL / MAJOR / MEDIUM / POLISH  
**EARLIEST_CAUSE:**  
**DOWNSTREAM_DAMAGE:**  
**PROTECTED_WORKING_MATERIAL:**  
**SMALLEST_HIGH_LEVERAGE_FIX:**  
**RETEST_REQUIRED:**  
**STATUS:** OPEN / MANUAL_REVIEW / RESOLVED

Fix the earliest responsible layer, not the loudest symptom.

---

## 24. CURRENT PRODUCTION STATUS

**LAST_COMPLETED_ARTIFACT:**  
**CURRENT_BLOCKER:**  
**HIGHEST_UNBLOCKED_NEXT_OBLIGATION:**  
**NEXT_GATE:**  
**OWNER/ROLE:**  
**EXPECTED_OUTPUT:**

---

## 25. CONTINUATION COMMAND

When Founder says `и / дальше / продолжай / делай / работай`:

1. restore CURRENT universal authority and this project’s authority;
2. verify source/version/hash/branch and overlay;
3. identify last completed artifact and open gates;
4. execute highest unblocked production obligation;
5. do not reopen locked story without new evidence;
6. save/version result and update production status;
7. report `DONE / STATUS / EXACT NEXT ACTION`.

**NO SILENT CANON CHANGES. FAIL CLOSED ON AUTHORITY AMBIGUITY.**
