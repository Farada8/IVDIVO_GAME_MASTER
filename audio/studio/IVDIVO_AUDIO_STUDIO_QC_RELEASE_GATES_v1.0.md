# IVDIVO AUDIO STUDIO — QC + RELEASE GATES v1.0

**Status:** CANON / FAIL-CLOSED RELEASE STANDARD

## 1. Authority QC
PASS only if:
- active source identified;
- source hash matches production package;
- project/branch/version correct;
- required overlay loaded;
- forbidden archive branch/tokens not compiled;
- adaptation authority explicit if performance text differs.

Any failure = FATAL / NO-GO.

## 2. Spoken-text QC
Check:
- missing words;
- duplicated words;
- reordered protected words;
- wrong speaker;
- truncated line;
- accidental stage-direction speech;
- pronunciation;
- name/number/date consistency.

Exact-text protected failure = FATAL or MAJOR depending on story criticality.

## 3. Voice/cast QC
Check:
- voice ID matches cast map;
- timbre drift across blocks;
- age/identity consistency;
- narrator/character separation;
- repeated synthetic cadence;
- emotional-tag repetition;
- sudden projection/style shift.

## 4. Performance continuity QC
Every reactive line must fit:
`HEARD_EVENT / RESPONSE_IMPULSE / STATE_IN / STATE_OUT`.

Flag:
- emotional reset;
- line played without listening;
- status contradiction;
- false guilt/romance/horror coding;
- overacting;
- generic sexy/cinematic delivery;
- identical rhythm across characters.

## 5. Pause/breath QC
Flag:
- random sigh/gasp;
- repeated breath template;
- zero-gap machine cadence;
- abrupt alternation between zero-gap and long pauses;
- pause contradicting urgency/status;
- protected silence filled by score/Foley;
- silence that reads as technical dropout rather than authored pause.

## 6. Body/Foley QC
Check causal chain:
`CHARACTER → ACTION → OBJECT/MATERIAL → SOUND → RESULT`.

Flag:
- impossible or missing body state;
- footsteps with wrong weight/surface;
- object action before physical cause;
- eating while speech remains implausibly clean;
- continuous chewing/lip noise;
- Foley wall;
- Foley characterisation inconsistent with character behavior;
- object sound identity drift across scenes.

## 7. Microtexture headphone QC
On headphones/earbuds test:
- mouth texture salience;
- swallowing;
- breath closeness;
- cloth rubbing;
- touch sounds;
- repetitive chair/bed creaks.

Fail if ordinary realism becomes repulsive, fetishized, comic, distracting or tiring without story intent.

## 8. SFX/clue QC
For IMPORTANT/CLUE/PROTECTED sounds evaluate:
### CAUSAL
What source/event will listener infer?
### CODAL
If sound contains a signal/message, what exactly is decoded?
### SONIC IDENTITY
Can the cue be distinguished from neighboring cues?

Also check:
`LITERAL_MEANING / POSSIBLE_EXTENDED_MEANING / FORBIDDEN_IMPLICATIONS`.

## 9. Ambience/acoustic QC
Check:
- room exists continuously where appropriate;
- loops are not detectable;
- occasional events are not periodic machines unless physically justified;
- dialogue/Foley/SFX share coherent room acoustics;
- distance changes affect more than pan;
- room tone bridges edits cleanly;
- ambience never invents plot evidence.

## 10. Spatial QC
Check listener point of audition.
Test:
- left/right geography;
- front/back/depth;
- movement trajectory;
- occlusion;
- direct/reverb ratio;
- ear-specific intimacy/threat only when earned;
- critical meaning survives mono.

Stereo-only causality = MAJOR/NO-GO.

## 11. Music QC
Check:
- cue has story function/value change;
- no-music windows respected;
- music does not mask dialogue/clue;
- music does not pre-announce guilt, romance, danger, death, safety or supernatural truth;
- leitmotif identity remains consistent;
- music does not run continuously by default;
- emotional scene still works when score is muted.

If scene collapses without music, route upstream to performance/dramaturgy before simply increasing score.

## 12. Mix QC
Audit:
`TIME / FREQUENCY / LEVEL / STEREO / DEPTH`.

Evaluate:
`MOOD / BALANCE / DEFINITION / INTEREST / COMPREHENSION / STORY_INTENT`.

Flag:
- foreground competition;
- masking;
- static mix where story demands change;
- restless decorative automation;
- flattened depth;
- over-compression;
- lost transient clues;
- over-wide ambience;
- excessive low-mid buildup;
- brittle dialogue/music.

## 13. Technical master QC
Project/platform targets control exact numbers.
Always check:
- file format/sample rate/bit depth;
- clipping;
- sample peak / true peak where required;
- loudness where required;
- DC offset where relevant;
- clicks/dropouts;
- corrupt tails;
- accidental truncation;
- stem sum/null consistency where supported;
- start/end silence/tails;
- metadata/version identity.

## 14. Playback reality QC
Required applicable tests:
`HEADPHONES / EARBUDS / PHONE_SPEAKER / MONO / LOW_VOLUME / CASUAL_ATTENTION / 1.25x`.

Ask:
- can dialogue be understood once?
- do clue sounds survive?
- does geography remain legible?
- do body textures become distracting?
- does music swallow words?
- does protected silence read as intentional?

## 15. AI artifact QC
Flag:
`VOICE_DRIFT / UNNATURAL_CADENCE / SYLLABLE_SMEAR / WRONG_STRESS / BREATH_GLITCH / DUPLICATED_WORD / TRUNCATED_WORD / FAKE_LAUGH / TIMBRE_JUMP / SENTENCE_FINAL_THEATRICALITY / TAG_SPOKEN_ALOUD / SYNTHETIC_ROOM_RESET`.

## 16. Human listener gate
At least one first-time listener pass for pilot/final release as project requires.
Questions:
1. What happened?
2. What do you think each main character wanted?
3. What are you waiting to learn/feel next?
4. Where were you confused?
5. Where did acting sound artificial?
6. Which sound/music detail distracted you?
7. Did any sound tell you an answer too early?
8. Did any silence feel like playback failure?
9. Did you want to continue?

## 17. Severity
### FATAL
Wrong source/branch, corrupted master, missing critical line, wrong speaker in critical line, broken clue order/identity, unauthorized story rewrite.

### MAJOR
Unbelievable performance on core beat, false story implication, unintelligible dialogue, major voice drift, clue masking, impossible causality, music spoiler, mono causality failure.

### MEDIUM
Local rhythm issue, repeated ambience, over-dense Foley, minor spatial inconsistency, noncritical AI cadence.

### POLISH
Small trim, harmless balance/tone refinement.

## 18. Release decision
`GO` only if:
- all required gates PASS;
- open FATAL = 0;
- open MAJOR = 0;
- unresolved anchors = 0;
- missing required assets = 0;
- locked source/hash match;
- master ID/version recorded.

Otherwise `NO_GO / REPAIR_REQUIRED`.
