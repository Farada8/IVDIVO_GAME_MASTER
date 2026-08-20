# IVDIVO AUDIO PRODUCTION STUDIO OS v3.0

**Status:** CANON / UNIVERSAL PRODUCTION OPERATING SYSTEM  
**Date:** 2026-08-20  
**Scope:** all IVDIVO narrated audiobooks, multi-voice audiobooks, dramatized audiobooks, audio dramas, doramas, serial fiction, pilots, trailers and audio-first works.

This OS sits above project-specific overlays and below Founder + locked story/project authority. It operationalizes the v2.1 base canon plus v2.2/v2.3 additive audio authority.

## 0. Studio law
The studio does not generate sound because sound is available. It creates a listener-controlled dramatic experience.

Universal order:
`STORY AUTHORITY → LISTENER CONTRACT → PERFORMANCE → BODY/ACTION → SPACE → SOUND → MUSIC → MIX → QC`.

Primary dramatic codes:
`WORDS / PERFORMANCE / BODY / SOUNDS / SPACE / MUSIC / SILENCE`.

## 1. Supported delivery modes
### MODE A — NARRATED AUDIOBOOK
Narrator-dominant. Exact source preserved. Minimal transitions/music. Foley/ambience only if explicitly commissioned.

### MODE B — MULTI-VOICE AUDIOBOOK
Narrator + stable character voices. Exact source preserved. Light ambience/transitions allowed.

### MODE C — DRAMATIZED AUDIOBOOK
Narrator + characters + actor direction + ambience + selected Foley/SFX + music + spatial staging. Source text remains authoritative; spoken rewriting only if delivery mode explicitly authorizes it.

### MODE D — FULL AUDIO DRAMA
Performance script may adapt narration into action/dialogue/sound only under explicit adaptation authority. Requires adaptation diff and story-canon protection.

## 2. Ten-specialist studio
1. Executive Audio Producer / Authority Controller.
2. Audio Dramaturg & Adaptation Supervisor.
3. Casting + Performance Director.
4. Dialogue Editor + TTS/Recording Supervisor.
5. Foley & Human Microtexture Director.
6. Sound Designer + Procedural Audio Designer.
7. Ambience / Acoustic / Spatial Director.
8. Music Supervisor + Score Director.
9. Re-recording Mixer + Mastering Engineer.
10. QC / Release Supervisor + Listener Advocate.

The ten roles may be executed by humans, AI agents, or mixed teams. Responsibility remains explicit even when one person performs several roles.

## 3. Mandatory production stages
### STAGE 00 — AUTHORITY INGEST
Inputs: locked text/script, canon, version, delivery mode, project overlay, voice locks, forbidden branches.
Outputs: `AUTHORITY_MANIFEST` + source hash.
Gate: AUTHORITY_PASS.

### STAGE 01 — LISTENER + DRAMATIC ANALYSIS
Outputs:
- `LISTENER_CONTRACT` per important beat;
- `DRAMATIC_FORCE_MAP`;
- `SCENE_AUDIO_ARC`;
- comprehension-critical lines/events.
Gate: DRAMATURGY_PASS.

### STAGE 02 — AUDIO ADAPTATION / STAGING
Outputs:
- `AUDIO_STAGING_SCRIPT`;
- scene/beat IDs;
- blocking requirements;
- action/reaction separation;
- protected text and adaptation diff where authorized.
Gate: STAGING_PASS.

### STAGE 03 — PERFORMANCE DIRECTION
Outputs:
- `CHARACTER_STATE_TIMELINE`;
- `ACTOR_DIRECTOR_SCORE`;
- `RESPONSE_STATE` per reactive line;
- pause/breath/listening/overlap plan;
- body-state continuity.
Gate: PERFORMANCE_PLAN_PASS.

### STAGE 04 — SOUND WORLD
Outputs:
- `ACOUSTIC_PASSPORT`;
- `LISTENER_POINT_OF_AUDITION`;
- ambience layers;
- Foley causality/performance plan;
- human microtexture plan;
- SFX/clue registry;
- object audio IDs;
- procedural/custom sound requirements.
Gate: SOUND_PLAN_PASS.

### STAGE 05 — MUSIC DRAMATURGY
Outputs:
- music functions;
- theme/leitmotif registry where earned;
- cue entry/exit anchors;
- intensity/density;
- no-music windows;
- forbidden implications.
Gate: MUSIC_PLAN_PASS.

### STAGE 06 — PROVIDER COMPILATION
Outputs:
- render block plan;
- clean dialogue requests;
- isolated TTS/performance sounds;
- SFX/music requests;
- pronunciation gates;
- take hypotheses;
- request hashes;
- regeneration boundaries.
Gate: DRY_RUN_PASS.

### STAGE 07 — VOICE / PERFORMANCE PRODUCTION
Lifecycle:
`GENERATED → REVIEW_PENDING → ACCEPTED → LOCKED`.
Never mutate LOCKED takes. Regenerate smallest failed boundary only.
Gate: DIALOGUE_LOCK.

### STAGE 08 — ASSET PRODUCTION
Create/source/lock ambience, Foley, SFX, clue SFX, procedural sounds and music. Recurring identity sounds receive asset IDs and continuity metadata.
Gate: ASSET_LOCK.

### STAGE 09 — EDIT + ALIGNMENT
Edit before rerender where possible. Ingest real alignment. Resolve semantic anchors into real sample positions. No invented production timestamps before this stage.
Gate: TIMELINE_LOCK.

### STAGE 10 — MIX
Minimum stems:
`DIALOGUE / CLUE_SFX / SFX / FOLEY / AMBIENCE / MUSIC`.
Build beat-linked `MIX_ACTION_SCORE` after timing resolution. Audit competition across `TIME / FREQUENCY / LEVEL / STEREO / DEPTH`.
Gate: MIX_PASS.

### STAGE 11 — MASTERING
Protect dialogue intelligibility, performance microdynamics, acoustic depth, tails and authored silence. Do not flatten dramatic contrast merely to hit loudness.
Gate: MASTER_TECH_PASS.

### STAGE 12 — QC + HUMAN LISTEN
Required families:
- source/exact-text;
- speaker/voice identity;
- pronunciation;
- performance continuity;
- causal Foley/SFX;
- protected silence;
- clue identity/order;
- music implication/masking;
- spatial/mono survival;
- headphone microtexture salience;
- AI artifacts;
- loudness/peak/dropouts;
- listener comprehension/emotion.
Gate: RELEASE_GO.

## 4. Performance laws
### Response law
Every reactive line knows:
`HEARD_EVENT → RESPONSE_IMPULSE → ENTRY_TRIGGER → PLAYABLE_BEHAVIOR → LINE → STATE_OUT`.

### Listening law
A character acts while silent. Track listening state, suppressed reaction, interruption attempt, withdrawal and next-entry impulse.

### Breath law
Breath must have physical or dramatic function. Random sighs/gasps are forbidden.

### Pause law
Pause types include:
`THOUGHT / HESITATION / RECOGNITION / STATUS / REFUSAL / ATTRACTION / SHOCK / LISTENING / OBJECT_ACTION / AFTERMATH / COMIC_TIMING / INTERRUPTION_WINDOW / NO_REPLY`.

### Punctuation law
Punctuation is not acting. Preserve exact text while timing follows thought/action unless punctuation carries protected meaning.

## 5. Human body / texture laws
Human texture may include breath, swallowing, mouth state, eating/drinking, cloth, hair, seat compression, fingers on objects, steps, body shift, touch and near-touch.

Every cue must have physical cause and story function.

For food/drink:
`PICKUP → CONTAINER/UTENSIL → BITE/SIP → MOUTH_STATE → CHEW/LIQUID → SWALLOW → BREATH_RESET → SPEECH → RETURN`.
Select the minimum useful chain. If eating is audible, speech must respect body state.

Headphone guard:
`REPULSION_RISK / FATIGUE_RISK / HEADPHONE_GAIN_LIMIT / REPETITION_LIMIT`.

## 6. Foley law
Foley is performance, not asset placement.
Fields when relevant:
`PERFORMER_INTENT / CHARACTER_WEIGHT / ACTION_TEMPO / CONTACT_FORCE / MATERIAL_RESPONSE / SYNC_TOLERANCE`.

Good Foley normally disappears into the reality of the scene.

## 7. Sound-design law
A sound may be library-recorded, generated, synthesized, procedural or layered. Choice depends on story need, controllability, repeatability and realism.

Procedural sound is appropriate when behavior must vary while preserving a stable physical identity. Model cause/material/energy/interaction rather than relying only on descriptive adjectives.

## 8. Space law
Define:
`ROOM / MATERIALS / RESONANCE / NOISE_FLOOR / LISTENER_POSITION / CHARACTER_POSITION / MIC_DISTANCE / ACOUSTIC_DISTANCE / HEAD_ORIENTATION / MOVEMENT / OCCLUSION / DIRECT_REVERB_RATIO`.

Ear-specific dialogue is story-earned, sparse and mono-safe. Distance is not pan alone.

## 9. Music law
Music has a story function, not a decoration function.
Possible functions:
`IDENTITY / DESIRE / ATTRACTION / MEMORY / LOSS / THREAT / CHOICE / AFTERMATH / TRANSITION / END_BUTTON`.

Music may not prematurely tell the listener who is guilty, in love, safe, doomed or supernatural unless the story has earned that information.

## 10. Mix law
Every dense beat defines focus ownership. The mix may create focus through subtraction, level, frequency, transients, width, depth, reverb, occlusion, ducking and silence.

Mix objectives:
`MOOD / BALANCE / DEFINITION / INTEREST / COMPREHENSION / STORY_INTENT`.

## 11. Provider law
TTS/SFX/music providers are replaceable backends.

Internal psychology is compiled into playable behavior before provider requests.
Provider receives only necessary actionable context, never whole canon dumps or future mystery solutions.

## 12. Version/authority law
Every production artifact contains:
`project_id / source_version / source_hash / authority_version / overlay_version / created_at / upstream_dependencies / status`.

No stage consumes an unversioned source.

## 13. Fail-closed law
If a required gate fails, downstream automation stops.
No silent fallback, no missing-cue substitution, no reroll of locked takes, no guessed timestamps, no branch substitution.

## 14. Evidence basis
This studio model is built from IVDIVO production experience and abstracted mechanisms from professional references including *The Radio Drama Handbook*, *Sound Design*, *Mixing Audio*, *The Foley Grail*, *Designing Sound*, voice/acting references and prior IVDIVO audio-engine audits. References inform mechanisms; they are not story canon.
