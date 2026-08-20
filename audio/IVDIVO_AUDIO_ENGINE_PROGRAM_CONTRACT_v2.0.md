# IVDIVO AUDIO ENGINE — PROGRAM CONTRACT v2.0

**Date:** 2026-08-20  
**Status:** WORKING / IMPLEMENTATION CONTRACT  
**Purpose:** convert the Audio Director v2.0 canon into implementable program modules and machine-readable artifacts.

## 1. Program boundary

The engine does not invent a new story after `SOURCE_LOCK`. It compiles approved story into production decisions, renders through one or more providers, assembles audio, verifies, repairs selectively, and exports a master.

## 2. Required top-level commands

```bash
ivdivo-audio analyze <script>
ivdivo-audio direct <script>
ivdivo-audio compile <script>
ivdivo-audio render <production_package>
ivdivo-audio assemble <production_package>
ivdivo-audio qc <build>
ivdivo-audio repair <build>
ivdivo-audio full <script>
```

Recommended flags:

```text
--project
--episode
--delivery narrated|multivoice|drama
--style natural|intimate|prestige|mystery|romance|youth
--provider elevenlabs|other
--dry-run
--resume
--from-stage
--to-stage
--protect-text
--human-gate-required
```

## 3. Program modules

```text
audio_engine/
  authority/
    authority_guard.py
    source_hash.py
    branch_firewall.py

  analysis/
    story_audio_analyzer.py
    scene_audio_dramaturgy.py
    attention_mapper.py
    episode_audio_arc.py

  performance/
    character_state.py
    performance_director.py
    listening_actor.py
    breath_planner.py
    reply_latency.py
    overlap_planner.py
    aftermath_tracker.py

  staging/
    blocking_director.py
    proximity_director.py
    acoustic_passport.py
    microphone_perspective.py

  composition/
    audio_composer.py
    density_map.py
    rhythm_map.py
    silence_director.py
    transition_director.py
    montage_director.py

  sound/
    sound_world_director.py
    foley_causality.py
    object_audio_registry.py
    clue_asset_registry.py
    media_authenticity.py

  music/
    music_dramaturgy.py
    leitmotif_registry.py
    music_contamination_guard.py

  compiler/
    performance_compiler.py
    render_block_compiler.py
    provider_prompt_compiler.py
    tag_budget.py
    take_plan.py

  providers/
    elevenlabs_dialogue.py
    elevenlabs_tts.py
    elevenlabs_sfx.py
    elevenlabs_music.py
    elevenlabs_alignment.py
    provider_adapter.py

  edit/
    dialogue_editor.py
    edit_before_regen.py
    reaction_editor.py
    crossfade_manager.py

  timeline/
    semantic_anchor.py
    timeline_resolver.py

  automix/
    spatial_automation.py
    masking_controller.py
    dialogue_priority.py
    emotional_mix.py
    mastering_guard.py

  qc/
    authority_qc.py
    exact_text_qc.py
    speaker_binding_qc.py
    pronunciation_qc.py
    performance_qc.py
    clue_qc.py
    music_policy_qc.py
    ai_artifact_qc.py
    technical_qc.py
    mono_mobile_qc.py
    human_listening_gate.py

  repair/
    defect_router.py
    selective_regen.py
    selective_remix.py

  registry/
    take_registry.py
    asset_registry.py
    build_registry.py

  cli.py
```

## 4. Core schemas

### SceneAudioState

```json
{
  "scene_id": "S01",
  "start_state": "",
  "attention_target": "",
  "tension": 0,
  "emotional_temperature": 0,
  "information_priority": [],
  "escalation_points": [],
  "reversal": null,
  "recognition": null,
  "aftermath": null,
  "end_state": "",
  "next_listen_question": ""
}
```

### CharacterPerformanceState

```json
{
  "character": "",
  "state_in": "",
  "immediate_want": "",
  "resistance": "",
  "tactic": "",
  "subtext": "",
  "status_before": 0,
  "energy": 0,
  "tempo": "",
  "breath_policy": "",
  "listening_state": "",
  "reply_mode": "NORMAL",
  "state_out": "",
  "status_after": 0,
  "forbidden_performance": []
}
```

### AttentionState

```json
{
  "beat_id": "",
  "focus_1": "",
  "focus_2": "",
  "background": [],
  "suppress": []
}
```

### BlockingState

```json
{
  "character": "",
  "position": "",
  "orientation": "",
  "distance_to_partner": "",
  "mic_perspective": "NORMAL",
  "movement_path": [],
  "occlusion": "NONE",
  "proximity_state": "WORK",
  "contact_event": null
}
```

### AudioBeat

```json
{
  "beat_id": "",
  "story_change": "",
  "anchor_type": "AFTER_TURN",
  "anchor_ref": "",
  "density": 0,
  "rhythm": {
    "speech_tempo": "",
    "reply_mode": "NORMAL",
    "pause_density": 0,
    "overlap_density": 0
  },
  "silence_policy": null,
  "sound_events": [],
  "music_policy": "OPTIONAL"
}
```

### MusicCue

```json
{
  "cue_id": "",
  "function": "AFTERMATH",
  "entry_cause": "",
  "exit_cause": "",
  "motif_id": null,
  "instrumentation": "",
  "intensity": 0,
  "dialogue_policy": "DUCK",
  "negative_implications": []
}
```

### PerformanceCompilation

```json
{
  "render_block_id": "",
  "provider": "elevenlabs",
  "mode": "TTD_BLOCK",
  "source_turn_ids": [],
  "context_summary": "",
  "playable_direction": "",
  "provider_instruction": "",
  "tag_budget": 0,
  "take_plan": [
    {"take":"A","hypothesis":"baseline"}
  ],
  "text_protected": true,
  "pronunciation_refs": []
}
```

## 5. Provider compilation modes

- `TTD_BLOCK`: multi-speaker context-dependent dramatic beat.
- `ISOLATED_TTS`: clue line, media line, pronunciation-sensitive or performance-critical line requiring isolation.
- `VOCALIZATION`: justified non-verbal human reaction only.
- `PERFORMANCE_SOUND`: human performance-related sound not represented as spoken text.
- `LOCKED_ASSET`: previously accepted recurring audio.
- `SFX_REQUEST`: generated sound effect.
- `MUSIC_REQUEST`: generated/composed music cue.

## 6. Compilation rules for ElevenLabs

- preserve `exact_text` when text-protected;
- do not include stage-direction prose in spoken text;
- keep clue sounds, ambience, music and heavy media processing out of clean dialogue masters where practical;
- maintain voice IDs and pronunciation references;
- use enough conversational context for acting continuity;
- isolate lines whose failure would break clue, identity, relationship or canon;
- tags are sparse and implementation-only;
- provider receives playable direction, not internal psychological exposition;
- multiple takes differ by one explicit hypothesis;
- save provider request hash and response/alignment provenance.

## 7. Semantic timing contract

Before render, cues use semantic anchors only. After accepted voice timing/alignment:

```text
semantic anchors
→ accepted take timing
→ resolved timeline
→ exact cue placement
```

Regeneration of one block may shift dependent downstream timing but must not silently invalidate unrelated locked blocks.

## 8. Edit-before-regenerate controller

Decision:

```text
IF words exact AND voice identity passes AND intention passes
  AND defect is pause/trim/spacing/crossfade/reaction-placement
THEN EDIT_ONLY
ELSE SELECTIVE_RERENDER
```

Never rerender an entire episode because one block fails.

## 9. QC fail-closed gates

Production may not issue `MASTER_LOCK` if any unresolved FATAL exists.

Mandatory automated/structured gates:
- active authority and source hash;
- branch contamination;
- dialogue-unit accounting;
- exact request text;
- voice/speaker binding;
- asset-lock integrity;
- unresolved semantic anchors;
- clue-order and clue-audibility requirements;
- protected silence;
- music forbidden windows;
- mono-critical cue flags;
- missing stems/assets;
- loudness/peak/clipping;
- text/alignment verification when available;
- selective-repair register.

Mandatory human gates where relevant:
- content comprehension;
- believable performance;
- believable sound world;
- emotional result;
- AI distraction/blind listen.

## 10. Checkpointing

Every stage writes immutable/versioned artifacts plus hashes. `--resume` resumes from the latest valid checkpoint. A changed upstream artifact invalidates only dependent downstream stages.

## 11. Acceptance definition

A generic episode/chapter is production-ready when one command can consume a locked script + overlay and produce all machine-readable direction/render artifacts without manual JSON authoring. A release-ready master additionally requires the configured human gates.

## 12. Current implementation priority

1. Extend data models for v2.0 states.
2. Implement scene dramaturgy + attention + performance continuity.
3. Implement blocking/proximity + audio composition.
4. Compile into current ElevenLabs render-block/request system.
5. Preserve existing take/asset/timeline/AutoMix/selective-regeneration work.
6. Validate first on ROOM 917 E02 without rewriting story.
