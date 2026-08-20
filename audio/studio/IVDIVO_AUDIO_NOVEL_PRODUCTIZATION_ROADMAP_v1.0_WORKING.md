# IVDIVO AUDIO NOVEL STUDIO — PRODUCTIZATION ROADMAP v1.0

**Status:** WORKING PRODUCT ROADMAP — NOT UNIVERSAL CANON  
**Current authority target:** `00_IVDIVO_AUDIO_STUDIO_INDEX_v3.3.md`  
**Goal:** one commandable production system that accepts a locked book/manuscript and can produce a professional dramatized audio work with evidence, repair, learning and distribution outputs.

## Product definition

The finished product is not a TTS wrapper and not a library of prompts.

Target user flow:

`BOOK / MANUSCRIPT -> INGEST -> AUTHORITY/CANON LOCK -> AUDIO ADAPTATION PLAN -> SCENE STATE GRAPHS -> PERFORMANCE -> MICROPHONE CHOREOGRAPHY -> WORLD SOUND -> MUSIC -> PROVIDER EXECUTION -> EDIT/ALIGN -> TIMELINE -> AUTOMIX -> MASTER -> QC/HUMAN LISTEN -> SELECTIVE REPAIR -> RELEASE PACKAGE -> LEARNING LOOP`.

The system must be resumable, inspectable, fail-closed and provider-replaceable.

## What already exists

Current repository already contains substantial authority/runtime for:
- source authority/hash and fail-closed stage gates;
- Audio Studio v3.x role/SOP/prompt contracts;
- provider preflight and ElevenLabs adapter;
- alignment normalization and live evidence;
- performance Scene State Graph runtime;
- FELT/SHOWN emotion, response/listening, rhythm/pause/breath compilation;
- body/Foley/microtexture planning;
- auditory mise-en-scene planning;
- microphone choreography / virtual radio stage planning;
- spatial/world-sound planning intent;
- music permission / semantic mix intent;
- performance QC, benchmark gate and controlled learning registry.

These are necessary but do not yet close the full book-to-master product loop.

## P0 — mandatory to obtain a real end-to-end product

### P0.1 BOOK INGEST + SOURCE NORMALIZER
Need executable input support for TXT/MD first, then DOCX/EPUB/PDF through adapters.

Outputs:
- `BOOK_INGEST_MANIFEST.json`
- `CHAPTER_MAP.json`
- `SOURCE_UNIT_MAP.json`
- normalized immutable source text;
- source SHA-256 and stable IDs.

Must preserve exact source and never silently rewrite.

### P0.2 AUDIO ADAPTATION / SCENE EXTRACTION ENGINE
A book is not already a Scene State Graph.

Need a reasoning stage that produces:
- scene boundaries;
- narrator-vs-actor allocation;
- audible vs narrated action decisions;
- protected exact text / approved adaptation diff;
- scene objectives / beat map;
- Scene State Graph seed package.

It must distinguish delivery modes NARRATED / MULTI_VOICE / DRAMATIZED / FULL_AUDIO_DRAMA.

### P0.3 PERFORMANCE EXECUTION BRIDGE
Current performance planning must be proven to survive into real provider execution.

Need:
- provider-safe performance-text/instruction compiler;
- exact-text stripping/coverage proof;
- context-window strategy for dialogue continuity;
- take hypotheses and selective rerender boundaries;
- regression test using LESSON ZERO Scene 2.

### P0.4 WORLD SOUND ASSET ENGINE
Planning exists; asset production is not yet a complete executable subsystem.

Need:
- asset request compiler for Foley/SFX/ambience/music;
- provider/library/field/procedural adapters;
- fixed `ASSET_ID` registry;
- version/hash/provenance/license metadata;
- audition-in-context gate;
- recurring sonic identity lock;
- no silent substitute when asset missing.

### P0.5 TIMELINE ASSEMBLER
After accepted dialogue and assets have real timing, need one deterministic resolved timeline.

Inputs:
- normalized alignment;
- accepted takes;
- semantic anchors;
- Foley/SFX/ambience/music cues;
- microphone choreography.

Outputs:
- sample-accurate timeline;
- overlap/transition events;
- stem event lists;
- unresolved-anchor failures.

### P0.6 ACTUAL AUTOMIX RENDERER
Current system has semantic mix intentions, but the product needs an executable renderer.

Required capabilities:
- stem assembly: DIALOGUE / CLUE_SFX / SFX / FOLEY / AMBIENCE / MUSIC;
- clip gain and fades;
- authored pauses and room-tone bridges;
- pan/width/depth automation;
- distance/off-axis filtering;
- convolution/algorithmic room staging;
- occlusion;
- ducking only with dramatic reason;
- music/dialogue/clue masking protection;
- mono-safe fallback;
- render reproducibility from manifest.

Do not bake arbitrary mastering into AutoMix.

### P0.7 MASTERING + DELIVERY RENDERER
Need target-profile mastering rather than one hard-coded loudness number.

Outputs:
- archival production master;
- platform master(s);
- chapter/episode WAVs;
- optional compressed delivery copies;
- technical report and checksums.

### P0.8 REAL AUDIO QC PROBES
Need executable post-render analysis for:
- duration/channel/sample-rate/bit-depth;
- clipping/true peak/loudness when target requires;
- silence/dropout/click risk;
- stereo collapse / mono survival;
- stem sum integrity;
- speech intelligibility proxy;
- repeated cadence/pause patterns;
- asset omissions;
- alignment/timeline coverage.

Machine QC may block technical failures but may not claim to replace human acting judgment.

### P0.9 HUMAN REVIEW / REPAIR LOOP
Need a practical review artifact/UI, not only JSON.

Reviewer must be able to mark:
- exact scene/turn/time;
- acting / pronunciation / rhythm / body / space / SFX / music / mix defect;
- severity;
- smallest repair;
- accept/lock/supersede.

Output feeds `learning_registry.py`.

## P1 — mandatory for a usable production product rather than an experiment

### P1.1 BATCH ORCHESTRATOR + RESUME
Whole books require:
- chapter/scene queue;
- dependency DAG;
- resumable runs;
- crash recovery;
- retry policy;
- selective rebuild;
- immutable accepted artifacts;
- parallel-safe work where dependencies permit.

### P1.2 COST / CREDIT / TIME PLANNER
Before paid calls estimate:
- dialogue characters/credits;
- alternate takes;
- SFX/music generation;
- expected rerender reserve;
- storage/output size;
- estimated runtime.

Track actual cost/usage per project, chapter, provider and repair.

### P1.3 PROVIDER ABSTRACTION LAYER
ElevenLabs remains one backend.

Need normalized interfaces:
- dialogue provider;
- SFX provider;
- music provider;
- speech/alignment provider;
- local/manual asset source.

Capability negotiation must fail closed instead of silently degrading quality.

### P1.4 PROJECT STATE DATABASE / INDEX
JSON artifacts remain authority/evidence, but book-scale production needs an index for:
- project/build IDs;
- chapter/scene/unit IDs;
- artifact status;
- dependency relationships;
- hashes;
- provider evidence;
- open defects;
- cost;
- locks/superseded versions.

SQLite is sufficient for a local first product if the JSON artifacts remain canonical evidence.

### P1.5 CAST + ASSET LIBRARY
Reusable registry for:
- voice identities and voice IDs;
- pronunciation samples/rules;
- room/acoustic passports;
- recurring Foley objects;
- clue/device sonic identities;
- music motifs;
- approved ambience beds.

Reuse requires compatibility/provenance checks.

### P1.6 PRODUCTION UI / CLI
Minimum viable operator experience:
- `new-project`;
- `ingest-book`;
- `plan`;
- `render-pilot`;
- `review`;
- `repair`;
- `render-chapter`;
- `render-book`;
- `status`;
- `cost`;
- `release-check`;
- `export`.

The user should not need to inspect raw JSON for normal operation.

## P2 — quality and professional consistency

### P2.1 REFERENCE / BENCHMARK SUITE
Create licensed/owned or metric-only reference fixtures representing desired professional properties:
- natural actor-to-actor reaction;
- pause/rhythm variation;
- microphone choreography;
- intelligible layered sound;
- dynamic foreground/background changes;
- music restraint;
- headphone and mono translation.

Do not clone copyrighted performances. Measure/abstract production properties.

### P2.2 CHARACTER CONTINUITY ACROSS BOOK
Need chapter-to-chapter state carryover:
- emotional residue;
- relationship/status changes;
- fatigue/injury/physical state;
- knowledge state;
- voice/performance identity;
- recurring sonic associations.

### P2.3 LONG-FORM PACING ENGINE
Scene quality alone is insufficient.

Need book-level curves for:
- density;
- silence;
- music frequency;
- sonic novelty;
- intimacy vs scale;
- narrator/actor balance;
- fatigue management.

### P2.4 SOUND SEMANTICS / FALSE-IMPLICATION RED TEAM
Automated and human audit for sounds/music that accidentally imply:
- guilt;
- romance;
- supernatural truth;
- danger;
- location/source identity;
- causality not present in canon.

### P2.5 LISTENING-FATIGUE MODEL
Track:
- mouth/microtexture repetition;
- constant ambience density;
- over-wide stereo;
- high-frequency fatigue;
- compressed dialogue;
- continuous score;
- repetitive synthetic cadence.

## P3 — commercial release product

### P3.1 DISTRIBUTION PACKAGER
Generate platform-specific package from approved master:
- chapter/episode files;
- naming;
- metadata manifest;
- cover/series references where applicable;
- checksums;
- duration table;
- release notes;
- archival stems and cue sheets.

Platform-specific technical targets must be runtime profiles, not assumed universal constants.

### P3.2 RIGHTS / LICENSE PROVENANCE
Every third-party/generated asset must record:
- origin/provider;
- account/license basis;
- generation/request ID where available;
- permitted commercial use status;
- version/hash;
- replacement history.

No release if a required asset has unknown provenance.

### P3.3 SECURITY / PRIVACY
- secrets only in environment/secret manager;
- sanitized logs;
- no manuscript leakage into unnecessary provider context;
- configurable retention of provider payloads;
- project-level export/archive controls.

### P3.4 ARCHIVE / REPRODUCIBILITY
A release must be reproducible from:
- source hash;
- authority versions;
- scene/artifact manifests;
- accepted take hashes;
- asset hashes;
- timeline;
- mix/master manifests;
- tool/runtime version.

## Product acceptance definition

The system is a **full product** only when this test works without manual JSON surgery:

1. Operator supplies a book and selects delivery mode.
2. System ingests and locks source.
3. System creates chapter/scene plan and requests only necessary approvals.
4. System produces a hard pilot.
5. Human can reject a local acting/sound/mix defect.
6. System repairs only the smallest responsible unit.
7. Accepted pilot becomes a style/quality benchmark.
8. System processes a complete chapter, then a complete book with resume/cost tracking.
9. It outputs separated stems, master, QC, release package and provenance.
10. A later production can reuse proven patterns through the controlled learning registry without silently mutating canon.

## Recommended implementation order

`BOOK INGEST -> ADAPTATION/SCENE EXTRACTION -> PERFORMANCE EXECUTION PROOF -> WORLD SOUND ASSET ENGINE -> TIMELINE ASSEMBLER -> AUTOMIX RENDERER -> MASTER/QC -> HUMAN REVIEW TOOL -> BATCH/RESUME/COST -> DISTRIBUTION/PROVENANCE`.

Do not build a polished UI before the Scene 2 and one complete chapter pass the full audio quality loop.