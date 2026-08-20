# IVDIVO AUDIO REFERENCE INTELLIGENCE AUDIT — BATCH 1 v1.0

**Date:** 2026-08-20  
**Status:** REFERENCE INTELLIGENCE / EVIDENCE FOR CANON UPDATES  
**Scope:** universal audio production, not project-specific story canon.

## Purpose
Audit newly supplied professional sources and extract reusable production mechanisms without copying source text, examples, plots, or distinctive expression.

Pipeline:
`SOURCE → ABSTRACT MECHANISM → CROSS-SOURCE CHECK → IVDIVO APPLICATION → CANON / PROGRAM / PROMPT PATCH`.

## Source weighting
Duplicates do not increase authority.

### A-TIER — DIRECT AUDIO PRODUCTION
1. David Sonnenschein — *Sound Design: The Expressive Power of Music, Voice, and Sound Effects in Cinema*.
2. Richard J. Hand & Mary Traynor — *The Radio Drama Handbook: Audio Drama in Context and Practice*.
3. Michel Chion — *Audio-Vision: Sound on Screen*.
4. Roey Izhaki — *Mixing Audio: Concepts, Practices and Tools*.
5. Ric Viers — *The Sound Effects Bible*.
6. James R. Alburger — *The Art of Voice Acting*.
7. Bob Katz — *Mastering Audio: The Art and the Science* — available copy is visually/scanned constrained; use for mastering reference with lower extraction confidence until a clean searchable edition is available.

### B-TIER — ADJACENT / SELECTIVE
- Michel Chion — *The Thin Red Line*: film-analysis reference; selective sound/narrative use only.
- *Subtitling: Concepts and Practices*: useful for timing, segmentation, accessibility and multimodal delivery; not core audio-direction authority.

### REFERENCE ONLY / NOT AUDIO-BATCH AUTHORITY
- *Words on Screen* — primarily writing/graphic text in cinema.
- *Guildmasters’ Guide to Ravnica* — worldbuilding/game reference, not audio production.
- *William Scott Ament and the Boxer Rebellion* — history, not audio production.
- *Imperial Co-operation and Transfer, 1870–1930* — history, not audio production.
- *International Human Resource Management* — management, not audio production.
- *The Jewish Daughter Diaries* — literary/reference only, not audio-production craft authority.

## Confirmed mechanisms to adopt

### M01 — LISTENER-CENTERED PRODUCTION
The listener is not the last stage of the pipeline. Listener cognition is the organizing center of writing, performance, sound, mix and QC.

IVDIVO consequence:
Every beat must define `LISTENER_MUST_UNDERSTAND / LISTENER_MAY_FEEL / LISTENER_MUST_WAIT_FOR`.

### M02 — FOUR PRIMARY CODES
Audio drama is constructed from:
`WORDS / SOUNDS / MUSIC / SILENCE`.
None is decoration by default. Their meaning comes from relation and hierarchy.

### M03 — PERSUASIVE ILLUSION, NOT TOTAL REALISM
Do not reproduce every audible physical detail. Select the most typical, evocative and causal details needed to create the listener’s mental scene.

IVDIVO consequence:
Add `EVOCATIVE_DETAIL_GATE` to Foley/SFX planning.
Reject microtexture that creates clutter without body, action, relationship, place, clue or rhythm function.

### M04 — SOUND-EFFECT SIGNIFICATION RISK
A sound can imply more than its literal physical source. Therefore SFX can accidentally signal danger, guilt, comedy, supernatural ontology, romance or status.

IVDIVO consequence:
Every important cue carries:
`LITERAL_MEANING / POSSIBLE_EXTENDED_MEANING / FORBIDDEN_IMPLICATIONS`.

### M05 — SOUND MAP FROM DRAMATIC MAP
Map dramatic forces and emotional curves before choosing sounds. Voice, ambience, effects and music then develop or counterpoint those curves.

IVDIVO consequence:
`STORY_AUDIO_ANALYSIS → DRAMATIC_FORCE_MAP → AUDIO_COMPOSITION_SCORE`.

### M06 — ORCHESTRATION / FOCUS EXCHANGE
Dialogue, effects and music should not all fight for foreground. Focus may move among them by level, frequency, density, spatial width and timing.

IVDIVO consequence:
Add `FOCUS_OWNER` and `MASKING_BUDGET` per beat.

### M07 — ACTION / REACTION SEPARATION
Useful default, not an absolute rule:
- physical action may be carried by action sound;
- emotional reaction may be carried later by music or silence.
Avoid scoring the impact twice unless deliberately earned.

### M08 — PREMIX / STEM DISCIPLINE
Dialogue, effects and music have different origins and processing needs. Keep them independently controllable through premixes/stems. Dense effect worlds may need sub-premixes.

IVDIVO consequence:
Minimum standard buses remain separated; add optional subgroups under FOLEY/SFX/AMBIENCE where density demands it.

### M09 — ACTOR MUST KNOW THE UNHEARD WORLD
Performance improves when actors know the sounds, actions and partners that may be added later, even when those elements are not physically present in the TTS/recording call.

IVDIVO consequence:
Every render block gains `OFFSCREEN_AUDIO_CONTEXT` and `PARTNER_ACTION_CONTEXT`.

### M10 — SMALL / INTIMATE AUDIO PERFORMANCE
Radio/audio acting should not compensate for lack of visuals by becoming theatrical. Close listening exposes tiny vocal detail.

IVDIVO consequence:
Default naturalism gate: reject unnecessary projection, genre acting and generalized “cinematic” emphasis.

### M11 — MIC/BLOCKING IS PERFORMANCE
Distance/orientation relative to microphone changes meaning and reality. Blocking is not only post-mix panning.

IVDIVO consequence:
`MIC_PERSPECTIVE / DISTANCE / HEAD_ORIENTATION / MOVEMENT_PATH` become mandatory for scenes where geography matters.

### M12 — THREE LISTENING MODES QA
Derived from Chion/Schaeffer framework:
- causal: what made the sound / what physical event is inferred;
- codal: what message/code is understood;
- reduced: what audible qualities the sound has independent of source/meaning.

IVDIVO consequence:
Critical cue QA must test all applicable modes:
`CAUSE_CLEAR? / MESSAGE_CLEAR? / SONIC_IDENTITY_DISTINCT?`.

### M13 — AUDIO CONTRACT IS CONTEXTUAL
A sound does not carry one fixed meaning outside context. Production creates the listener’s belief about source, meaning and relationship.

IVDIVO consequence:
No generated SFX is accepted because its filename/prompt sounds right. It must be auditioned in scene context.

### M14 — VOICE PERFORMANCE CORE
Alburger’s performance framework supports the existing IVDIVO actor model: audience, backstory, character, desires, energy, focus and risk/commitment all affect believable delivery.

IVDIVO consequence:
Do not copy the source’s branded framework into prompts. Map it to existing fields:
`AUDIENCE_TARGET / STATE_IN / BACKSTORY_ACTIVE_NOW / CHARACTER_IDENTITY / WANT / ENERGY / FOCUS / PERFORMANCE_COMMITMENT`.

### M15 — SCRIPT ANALYSIS BEFORE DELIVERY
Performance choices should come from story context, character, response to information, transitions and natural breaks rather than punctuation alone.

IVDIVO consequence:
Provider compiler receives behavior, not just emotion labels.

### M16 — BREATH SUPPORTS EXPRESSION
Breath supports loudness, softness, transitions and emotional nuance. It should not be used as random “humanization.”

IVDIVO consequence:
Retain Breath Director; add `BREATH_FUNCTION` and reject unmotivated breath tags.

### M17 — SFX TAXONOMY
Viers provides a useful production classification. IVDIVO standard categories:
- HARD_EFFECT;
- FOLEY;
- BACKGROUND / AMBIENCE;
- ELECTRONIC / PRODUCTION_ELEMENT;
- DESIGNED_EFFECT.
Project-specific `CLUE_SFX` remains an IVDIVO semantic priority class above this physical taxonomy.

### M18 — MIX AS CREATIVE STORYTELLING
Izhaki explicitly treats mixing as an art, not merely repair. Dynamics, EQ, spatial depth, automation and changing treatment can create interest and direct attention.

IVDIVO consequence:
AutoMix must support beat-aware automation rather than only static target levels.

### M19 — AUTOMATION IS NORMAL, NOT EXCEPTIONAL
Commercial mixes use automation extensively. Audio fiction likewise needs evolving levels, spatial positions, reverbs, focus and density.

IVDIVO consequence:
Add `AUTOMATION_CURVE` to resolved timeline objects for dialogue, ambience, effects and music when story state changes.

### M20 — PLAYBACK REALITY FIRST
Stereo/binaural can create location and movement, but many listeners hear audio in compromised stereo or mono during secondary activity.

IVDIVO consequence:
Spatial artistry is optional enhancement; comprehension must survive mono, phone speaker, low volume and casual listening.

## Red-team findings against IVDIVO v2.1

### MAJOR GAP 1 — too much focus on cue existence, not listener interpretation
FIX: introduce three-mode listening QA + extended-signification guard.

### MAJOR GAP 2 — microtexture could become over-literal Foley clutter
FIX: introduce persuasive-illusion / evocative-detail gate.

### MAJOR GAP 3 — provider blocks need unheard-world context
FIX: add OFFSCREEN_AUDIO_CONTEXT / PARTNER_ACTION_CONTEXT to performance compiler.

### MAJOR GAP 4 — sound/music conflict needs explicit orchestration
FIX: add FOCUS_OWNER / MASKING_BUDGET / frequency-space negotiation.

### MEDIUM GAP 5 — AutoMix needs narrative automation
FIX: beat-aware automation curves.

### MEDIUM GAP 6 — SFX taxonomy and semantic role were conflated
FIX: physical taxonomy plus independent story-criticality/classification.

## Canon verdict
`PASS WITH ADDITIONS`.
The v2.1 architecture remains valid. No foundational rewrite is required. Adopt M01–M20 through v2.2 additive authority.

## Next audit queue
Priority missing sources if later supplied:
- professional dialogue editing;
- Foley-specific production text;
- spatial/binaural audio reference;
- current audiobook production/delivery guide;
- current loudness/broadcast/platform standards;
- clean searchable Bob Katz edition;
- dedicated radio acting text.
