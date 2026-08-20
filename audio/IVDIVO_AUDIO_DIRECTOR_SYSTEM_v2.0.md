# IVDIVO AUDIO DIRECTOR SYSTEM v2.0

**Date:** 2026-08-20  
**Status:** CANON / SYSTEM ARCHITECTURE  
**Depends on:** Universal Audio Production Canon + v2.0 Addendum.

## Mission

Convert a locked story/script into a complete production-ready audio direction package and provider-safe render plan without casual story rewriting.

## Input contract

Required:
- active project/branch authority;
- locked source script and hash;
- delivery mode;
- character/relationship/continuity data;
- voice/cast bible when available;
- pronunciation dictionary;
- project Audio Overlay;
- Sound Bible / recurring asset registry;
- Acoustic Passports when available;
- prior accepted takes/assets for continuity.

Optional:
- platform loudness/export target;
- romance/mystery/youth production overlay;
- previous episode state-out data;
- audience/listener evidence.

## Output contract

Per episode/chapter:
1. `authority_manifest.json`
2. `story_audio_analysis.json`
3. `audio_dramaturgy.json`
4. `attention_map.json`
5. `actor_director_score.json`
6. `blocking_proximity.json`
7. `audio_composition_score.json`
8. `acoustic_sound_plan.json`
9. `music_score.json`
10. `render_block_plan.json`
11. `provider_requests/`
12. `take_registry.json`
13. `asset_registry.json`
14. `resolved_timeline.json`
15. `automix_manifest.json`
16. `qc_report.json`
17. `selective_repair_list.json`
18. `release_master.*`

## Subsystem A — Dramatic Audio Director

Responsibilities:
- scene audio arc;
- listener focus hierarchy;
- tension/emotional temperature;
- information priority;
- escalation/reversal/recognition/aftermath;
- episode and season audio arc;
- listener-next-question.

Core structures:

```json
{
  "scene_id": "S01",
  "start_state": "controlled",
  "attention_target": "dialogue",
  "tension": 3,
  "emotional_temperature": 2,
  "information_priority": ["relationship", "location"],
  "turns": [],
  "end_state": "uneasy",
  "next_listen_question": "What did the character hide?"
}
```

## Subsystem B — Performance Director

For each important line/block derive:
- immediate want;
- why now;
- resistance;
- tactic;
- status before/after;
- subtext;
- unsaid/unsayable;
- emotional floor;
- energy;
- tempo;
- breath/pause;
- listening state;
- next-entry impulse;
- forbidden performance;
- performance continuity state-in/state-out.

Additional controls:
- reply mode;
- interruption trigger;
- overlap purpose;
- vocal texture continuity;
- aftermath persistence;
- take-purpose hypothesis.

## Subsystem C — Blocking & Proximity Director

Tracks:
- character position;
- orientation;
- partner distance;
- mic/listener perspective;
- movement path;
- off-axis state;
- occlusion;
- contact/touch events;
- proximity category;
- intimacy/withdrawal changes.

No spatial automation without physical cause.

## Subsystem D — Audio Composition Director

Creates the semantic-time score for:
- dialogue/narration;
- silence;
- ambience;
- Foley;
- action SFX;
- clue/evidence SFX;
- processing;
- music;
- spatial movement;
- transitions;
- montage.

Tracks density/rhythm curves:
- sound density 0–10;
- speech tempo;
- response latency;
- pause density;
- overlap density;
- movement activity;
- music intensity;
- stereo activity.

Uses semantic anchors before accepted render timing.

## Subsystem E — Sound World Director

Maintains:
- location Acoustic Passports;
- room-tone library;
- Foley causality graph;
- object audio IDs;
- recurring clue/evidence assets;
- device/media authenticity profiles;
- environmental identity;
- character physical sound signatures when story-earned.

Every cue carries `story_function`, `physical_source`, `distance`, `space`, `priority`, `mono_critical`, and `negative_implications`.

## Subsystem F — Music Dramaturgy Director

Creates:
- cue function;
- entry/exit cause;
- instrumentation;
- intensity;
- dialogue policy;
- motif/theme reference;
- forbidden implication list;
- no-music windows.

Music is never permitted to reveal a story answer prematurely.

## Subsystem G — Provider Performance Compiler

Transforms internal direction into provider-safe instructions:

`psychology → playable behavior → provider instruction`.

It decides:
- multi-speaker dialogue block vs isolated TTS;
- context window;
- voice ID/model;
- pronunciation refs;
- tag budget;
- seed/provenance metadata where supported;
- take count and explicit difference between takes;
- whether a critical line must remain isolated;
- whether processing must occur after clean voice render.

Provider prompts must never contain unnecessary internal canon or proprietary reasoning.

## Subsystem H — Edit / Mix / QC Director

Editing order:
1. diagnose earliest failing layer;
2. edit-before-regenerate when words/identity/intention are good;
3. selective regenerate only failing block/turn;
4. lock accepted material.

Mix responsibilities:
- spatial continuity;
- masking control;
- dialogue/clue priority;
- emotional density contrast;
- dynamic/proximity preservation;
- mono/mobile survivability;
- mastering targets without flattening authored dynamics.

QC dimensions:
- authority/provenance;
- exact text;
- speaker/voice binding;
- pronunciation;
- performance meaning;
- scene comprehension;
- cue/clue causality;
- music policy;
- AI artifacts;
- technical integrity;
- mono/mobile/low-volume/1.25x;
- human content/performance/sound/emotional/blind listening.

## State machine

```text
SOURCE_LOCKED
→ DIRECTED
→ COMPILED
→ RENDER_CANDIDATE
→ ACCEPTED
→ LOCKED
→ MIXED
→ QC_CANDIDATE
→ SELECTIVE_REPAIR (if required)
→ RELEASE_CANDIDATE
→ MASTER_LOCK
```

Good locked material is immutable by default.

## Failure classes

`AUTHORITY / STORY-COMPREHENSION / PERFORMANCE / VOICE / PRONUNCIATION / TEXT / EDIT-RHYTHM / BLOCKING / SFX / FOLEY / AMBIENCE / PROCESSING / MUSIC / MIX / MASTER / PROVIDER_ARTIFACT / AI_ARTIFACT`.

## Universal production sequence

```text
RESTORE AUTHORITY
→ LOAD PROJECT OVERLAY
→ STORY AUDIO ANALYSIS
→ AUDIO DRAMATURGY
→ ATTENTION MAP
→ PERFORMANCE STATE
→ BLOCKING/PROXIMITY
→ AUDIO COMPOSITION
→ SOUND WORLD
→ MUSIC DRAMATURGY
→ PROVIDER COMPILATION
→ CLEAN RENDER
→ TAKE LOCK
→ EDIT
→ TIMELINE RESOLVE
→ SOUND/MUSIC ASSEMBLY
→ AUTOMIX
→ QC
→ SELECTIVE REPAIR
→ MASTER LOCK
```

## Design prohibition

Do not build 30–40 separate services merely because 30–40 fields exist. The eight subsystems are logical responsibilities and may share implementation modules.
