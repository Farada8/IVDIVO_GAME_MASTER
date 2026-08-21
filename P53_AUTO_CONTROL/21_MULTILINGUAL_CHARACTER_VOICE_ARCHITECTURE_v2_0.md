# IVDIVO / BODYGUARD — MULTILINGUAL CHARACTER VOICE ARCHITECTURE v2.0
## PROVIDER-NEUTRAL VOICE FAMILY + LOCALIZATION + PERFORMANCE + RELEASE SYSTEM

**STATUS:** CURRENT WORKING PRODUCTION AUTHORITY  
**SUPERSEDES:** Multilingual Character Voice Architecture v1.0  
**PROJECT SOURCE-TEXT AUTHORITY:** English Recording Master v1.6  
**FIRST PRODUCTION LOCALIZATION / PILOT MARKET:** Russian  
**PLANNED LANGUAGE FAMILY:** RU / EN / ES-ES or ES-LATAM / DE / IT  
**PRIMARY PRINCIPLE:** Character identity is canonical. Provider voice IDs are replaceable production implementations.

---

# 0. AUTHORITY CORRECTION

BODYGUARD was written and story-locked in English.

Therefore:

**ENGLISH = SOURCE-TEXT / STORY-DIALOGUE AUTHORITY.**

Russian is not allowed to silently become the source canon simply because it is produced first.

Therefore:

**RUSSIAN = FIRST PRODUCTION LOCALIZATION + FIRST VOICE-CREATION PILOT.**

Each localized edition receives its own locked text authority only after localization QA.

Authority chain:

`EN SOURCE MASTER → LOCALIZATION PACKET → LOCALE QA → P51/P52/P53 → LOCALIZED TEXT LOCK → VOICE IMPLEMENTATION → PERFORMANCE LOCK → MIX/QC → LANGUAGE RELEASE LOCK`

A localization can adapt wording for natural speech, but cannot change:
- clue facts;
- causality;
- consent/power;
- professional meaning;
- character objective/tactic;
- relationship stage;
- culprit/fair-play information;
- public/private truth state.

---

# 1. CHARACTER VOICE IDENTITY ≠ VOICE ID

Never encode character identity as:

`NAOMI = provider_voice_id_X`.

Encode:

`NAOMI_CHARACTER_VOICE_PASSPORT = canonical perceptual/performance identity`

and separately:

`NAOMI_RU_IMPLEMENTATION`
`NAOMI_EN_IMPLEMENTATION`
`NAOMI_ES_ES_IMPLEMENTATION`
`NAOMI_ES_LATAM_IMPLEMENTATION`
`NAOMI_DE_IMPLEMENTATION`
`NAOMI_IT_IMPLEMENTATION`

The same provider voice ID MAY implement multiple languages only if it passes each locale gate.

A different sibling voice MAY implement a language without changing character canon.

**VOICE ID CONTINUITY is optional. CHARACTER IDENTITY CONTINUITY is mandatory.**

---

# 2. CHARACTER VOICE PASSPORT — REQUIRED FIELDS

For every recurring character record:

- perceived age;
- gender presentation where story-relevant;
- vocal weight;
- pitch impression/range;
- texture;
- articulation;
- default tempo;
- breath behavior;
- phrase-ending behavior;
- humor rhythm;
- silence style;
- status behavior;
- authority behavior;
- intimacy behavior;
- public register;
- private register;
- stress/fatigue behavior;
- lie/concealment behavior;
- vulnerability signature;
- anger signature;
- fear signature;
- recovery signature;
- microphone/proximity behavior;
- language-flexibility observations;
- forbidden clichés/modes;
- pair-interaction identity;
- reference samples and provenance.

The passport is provider-neutral.

---

# 3. BODYGUARD LEAD PASSPORT INVARIANTS

## NAOMI PARK

Must remain:
- woman 33;
- grounded low-mezzo/alto impression;
- precise, economical;
- contemporary, not theatrical;
- authority through clarity, not aggression;
- danger makes her clearer/faster, not louder;
- private cost makes her slightly quieter, not breathy;
- dry literal humor;
- no maternal protector;
- no seductive bodyguard;
- no action-hero growl;
- no “ice queen” monotone;
- no loss of environmental awareness because of attraction.

Her intimacy signal:
**selective attention + controlled timing + respected boundary + withheld softer response.**

## ELI KWON

Must remain:
- man early 30s;
- attractive natural medium/medium-low speaking impression;
- stage-trained breath without announcer polish;
- public register warmer/polished;
- private register shorter/lower/less performed;
- musician rhythm;
- vulnerability through one rhythm/breath fracture, uncertainty, shame or costly choice;
- never helpless;
- never possessive alpha;
- never permanent charming smile;
- no trauma exhibition.

His intimacy signal:
**attention + remembering + asking rather than commanding + accepting “no” + costly choice.**

---

# 4. LANGUAGE IMPLEMENTATION LEDGER

Per character × locale:

- CHARACTER_ID
- LOCALE
- SOURCE_TEXT_AUTHORITY
- LOCALIZED_TEXT_VERSION
- PROVIDER
- ENDPOINT_PROFILE
- MODEL_ID
- LANGUAGE_CODE
- VOICE_ID
- SOURCE_TYPE:
  - SAME_MASTER
  - LANGUAGE_SIBLING_DESIGNED
  - NATIVE_LIBRARY
  - HUMAN_ACTOR
  - APPROVED_CLONE
- VOICE_BINDING_STATUS:
  - CANDIDATE
  - SMOKE_ONLY
  - APPROVED
  - PILOT_LOCKED
  - SEASON_LOCKED
  - SUPERSEDED
- PRONUNCIATION_MAP_VERSION
- PROVIDER_OUTPUT_FORMAT
- SAMPLE_EVIDENCE
- P51_RESULT
- P52_RESULT
- P53_RESULT
- NATIVE_LISTENER_RESULT
- PAIR_RESULT
- FATIGUE_RESULT
- DEVICE_RESULT
- RIGHTS/TERRITORY_RESULT
- PROVENANCE_BUILD_ID

---

# 5. LOCALE MATRIX — DO NOT TREAT “LANGUAGE” AS ONE SETTING

## RU
Target:
contemporary neutral Russian suitable for serialized audio drama.
Avoid:
Soviet/TV dubbing timbre, literary declamation, over-enunciated audiobook narration, forced English syntax.

## EN
Source authority language.
Target:
natural contemporary English consistent with locked script and existing P51 fingerprints.
Do not “translate back” from Russian.

## ES
Do not lock `ES` without region.

Branch before full cast:
- `ES-ES`
- `ES-LATAM` / likely Mexico-neutral if market evidence supports it.

Regional choice affects:
pronouns, slang, rhythm, status language, professional vocabulary and intimacy temperature.

## DE
Target:
natural spoken German, not bureaucratic calque.
Watch:
compound professional terminology, sentence-final information delay, formality.

## IT
Target:
natural contemporary spoken Italian.
Watch:
emotional warmth inflation; do not let translation make slow-burn more explicit than canon.

---

# 6. LOCALIZATION FUNCTION PACKET

Every translated line carries:

- SOURCE_LINE_ID
- SOURCE_TEXT
- STORY_FUNCTION
- OBJECTIVE
- TACTIC
- SUBTEXT
- STATUS/POWER
- CLUE_PAYLOAD
- CONSENT_PAYLOAD
- PROFESSIONAL_PAYLOAD
- P51_MARKERS
- P52_TEMPERATURE
- P53_RELATIONSHIP_FUNCTION
- HUMOR_FUNCTION
- TIMING_BURDEN
- LOCALIZATION_RISK
- WORKING_LOCALIZED_TEXT
- NATIVE_QA
- LOCK_STATUS

Translation evaluates **function equivalence**, not word-for-word sameness.

---

# 7. LISTENER CONTRACT FOR VOICE TESTS

Every audition/performance sample declares:

- LISTENER_MUST_UNDERSTAND
- LISTENER_MAY_FEEL
- LISTENER_MUST_WAIT_FOR
- FOCUS_OWNER
- SECONDARY_SUPPORT
- SUPPRESS
- DANGEROUS_MISUNDERSTANDING
- COMPREHENSION_CRITICAL

Examples:

Naomi command:
MUST UNDERSTAND = immediate movement order.
MAY FEEL = competence and trust pressure.
SUPPRESS = flirtation.
DANGEROUS MISUNDERSTANDING = angry domination.

Eli private fracture:
MUST UNDERSTAND = he remains cognitively active.
MAY FEEL = private vulnerability.
SUPPRESS = helplessness.
DANGEROUS MISUNDERSTANDING = “she must emotionally rescue him.”

---

# 8. PERFORMANCE PACKET — LANGUAGE INDEPENDENT CORE

Important turns use:

`STATE_IN → HEARD_EVENT → RESPONSE_IMPULSE → ENTRY_TRIGGER → WANT → TACTIC → SUBTEXT → PLAYABLE_BEHAVIOR → LINE → STATE_OUT → NEXT_ENTRY_IMPULSE`

Playable behavior includes:
- reply speed;
- projection;
- breath function;
- phrase-ending;
- hesitation;
- emphasis;
- orientation;
- proximity;
- interruption pressure;
- withholding;
- listening activity;
- status change;
- body condition.

Do not send providers only adjectives like “sexy”, “sad”, “cinematic”, “mysterious.”

---

# 9. MICROPHONE / PROXIMITY CHOREOGRAPHY

Voice casting must be tested at the distance the character actually inhabits.

Required lead states:
- neutral close conversational;
- professional command;
- private low-volume line;
- post-action breath recovery;
- public-facing register;
- fatigue/stress;
- pair interaction.

A close confidential line and a line projected across a stage are not “the same performance with more volume.”

Reverb/room is normally post-chain.
Performance may change projection/proximity behavior; clean source remains reusable.

---

# 10. SILENT REACTION LAW

Not every chemistry beat becomes synthetic speech.

Use non-spoken `SILENT_REACTION_ANCHOR` for:
- listening;
- decision not to answer;
- breath reset;
- physical withdrawal;
- hand release;
- attention shift;
- almost-reply;
- protected silence.

A silent anchor may own breath/Foley/spatial cues but does not count as spoken-text coverage unless an explicit performance sound is attached.

This prevents P53 micro-beats from becoming dialogue bloat.

---

# 11. P51 CROSS-LANGUAGE IDENTITY

A localized voice passes P51 only if the character remains recognizable after names are removed.

Check:
- vocabulary level;
- sentence length;
- occupational syntax;
- humor;
- argument;
- evasion;
- apology;
- affection;
- stress;
- silence;
- public/private contrast.

Attraction changes WHAT THEY NOTICE, not who they sound like.

---

# 12. P52 CROSS-LANGUAGE TEMPERATURE

Localization must not inflate intensity.

Map 1–5 temperature per source scene.
Localized version must match the intended range unless a language-specific adjustment preserves the same felt temperature.

Do not let:
- Italian/Spanish warmth automatically become confession;
- Russian brevity become cold hostility;
- German precision become emotional distance;
- English understatement disappear in translation.

---

# 13. P53 CROSS-LANGUAGE RELATIONSHIP FUNCTION

Rerun P53 after localization.

Required:
- push/pull;
- male competence + private cost;
- heroine agency + hidden cost;
- female-gaze attention;
- safe boundaries;
- 1–2 earned micro-rewards;
- after-action principle;
- choice;
- relationship delta.

Language implementation must preserve:
**privately important / professionally constrained**
during early BODYGUARD.

---

# 14. POWER / CONSENT LOCALIZATION

Consent and authority are semantic invariants.

Never weaken:
- immediate safety authority;
- client autonomy outside immediate danger;
- permission before body/equipment handling where required;
- guard/client boundary;
- refusal without punishment.

A localization that sounds more commanding, intimate or possessive than source must be revised.

---

# 15. PROFESSIONAL / CLUE LANGUAGE LOCALIZATION

Protection, stage, audio and evidence vocabulary must sound like professionals in the target language.

Do not literal-calque jargon if professionals would use a different established form.

Clue order and information density remain locked.

For audio clues:
- `left/right`;
- `four clicks/two clicks`;
- `standby/ack/GO`;
- `gateway`;
- `raw playback`;
must remain immediately distinguishable.

---

# 16. HUMOR / WORDPLAY LOCALIZATION

Preserve humor FUNCTION, not literal wording.

Classify:
- tension release;
- status play;
- private recognition;
- musician metaphor;
- dry literal humor;
- public-performance charm.

If literal translation loses function:
write a new locale-natural line that preserves story/relationship function and does not add information.

All rewritten humor passes P51/P52/P53 and clue/consent gates.

---

# 17. SAME-MASTER VS LANGUAGE-SIBLING DECISION

Test same master voice first where practical.

Score 0–10:
- native/plausible pronunciation;
- accent leakage;
- prosody;
- stress placement;
- natural phrasing;
- stable age/status;
- P51;
- P52;
- P53;
- microphone/proximity;
- pair chemistry;
- long-form fatigue;
- device translation.

Decision:
- all critical fields >=8 and no hard fail → SAME_MASTER candidate may continue;
- any FATAL/MAJOR linguistic/performance failure → LANGUAGE_SIBLING;
- uncertain → HOLD FOR NATIVE TEST.

Do not torture a mismatched voice with endless prompting.

---

# 18. PROVIDER ADAPTER LAW

Creative canon remains provider-neutral.

Provider-specific fields live in adapter/runtime:
- endpoint profile;
- explicit model_id;
- optional language_code;
- voice_id;
- output format;
- pronunciation dictionary locators;
- text normalization controls;
- seed where supported;
- alignment schema;
- billing/tier limits.

Before paid synthesis:
1. key exists without printing;
2. authenticated read-only connectivity;
3. GET models;
4. requested model exists/capability;
5. GET required voices;
6. only then billable test.

Do not hardcode unverified provider defaults into creative canon.

---

# 19. TTD VS ISOLATED TTS

Use conversational TTD where relationship/listening continuity benefits.

Use isolated TTS where:
- clue-critical;
- identity-critical;
- pronunciation-risk;
- acting-risk;
- unique post-chain;
- likely selective regeneration.

Do not isolate every line automatically; fragmentation can destroy relationship rhythm.

---

# 20. CLEAN-FIRST / ALIGNMENT LAW

Voice generation produces clean performance masters.

Do not bake in:
- ambience;
- score;
- Foley;
- clue SFX;
- final room reverb;
- master processing.

Archive:
- sanitized request;
- provider-original audio;
- raw alignment;
- normalized alignment;
- model/profile/output format;
- request/hash/provenance.

Unknown alignment schema = fail closed.

---

# 21. MULTILINGUAL TEST CASCADE

For a language edition:

`S0 READ-ONLY PROVIDER PREFLIGHT`
→ `S0B MINIMAL TECHNICAL CANARY`
→ `S1 FAIR SAME-TEXT ANCHORS`
→ `S2 SURVIVOR DISCRIMINATION`
→ `S3 FORBIDDEN-MODE / DIRECTION CHANGE`
→ `S4 PAIR TEST`
→ `PROVISIONAL PILOT LOCK`
→ `8–10 MIN FATIGUE`
→ `E01 ROUGH`
→ `NATIVE BLIND LISTENER`
→ `LANGUAGE PILOT LOCK`

Do not jump to full season.

---

# 22. ROLLOUT ORDER — REVISED COST CONTROL

Previous v1.0 shorthand “5 languages × 2 leads immediately” is too broad.

Current staged order:

## STAGE A
RU Naomi + Eli:
localization anchors → voice design → S0–S4 → RU E01 pilot → native/listener evidence.

## STAGE B
EN Naomi + Eli:
canonical English anchors → test RU/master identity → same-master or EN siblings → pair → EN E01.

## STAGE C
Spanish market fork:
business evidence chooses ES-ES vs ES-LATAM/MX before full casting.
Short zero-cost text/localization preparation may happen earlier.

## STAGE D
DE + IT:
prepare passports/localization risk maps/anchors now.
No full paid cast/render until quality + distribution case exists.

This reduces spend and avoids multiplying a flawed voice family.

---

# 23. BUSINESS / TERRITORY / RIGHTS GATE

Language quality is not sufficient for scale.

Before full-season localization/render:
- platform/distribution target;
- expected audience;
- pricing/revenue logic;
- localization cost;
- voice/provider rights;
- cloning/design consent rights;
- territory rights;
- reuse rights;
- provider migration risk;
- marketing assets;
- metadata/credits;
- human QA availability.

Scale when:
**QUALITY PASS + BUSINESS/DISTRIBUTION PASS + RIGHTS PASS.**

---

# 24. SELF-IMPROVEMENT LOOP

Every language produces evidence for the general engine.

Capture:
- recurring pronunciation errors;
- accent leakage;
- P51 drift;
- P52 inflation;
- P53 over/underheat;
- clue confusion;
- mic/proximity failures;
- TTD fragmentation or instability;
- native listener timestamps;
- fatigue;
- device failure;
- cost per accepted minute;
- regeneration rate.

Route:
`OBSERVE → EARLIEST FAILURE → MINIMAL SYSTEM PATCH → TEST → ACCEPT/HOLD/REJECT → WRITE-THROUGH → REGRESSION`.

Do not generalize one language quirk into a universal rule without repeated evidence.

---

# CURRENT PRODUCTION DECISION

**SOURCE AUTHORITY:** EN Recording Master v1.6.

**FIRST VOICE-CREATION PILOT:** RU Naomi + Eli.

**SECOND REQUIRED EDITION:** EN Naomi + Eli.

**THIRD:** Spanish after regional/business fork.

**PREPARED, NOT SCALED:** DE + IT.

**CURRENT PAID FRONTIER:** no mass synthesis. First produce and validate RU localization anchors, then create/test RU lead candidates.

**CURRENT HUMAN GATE:** native/audio evidence is required before any language voice lock.
