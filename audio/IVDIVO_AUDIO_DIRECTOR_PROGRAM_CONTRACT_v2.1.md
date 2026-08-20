# IVDIVO AUDIO DIRECTOR — PROGRAM CONTRACT v2.1

**Status:** CANON / IMPLEMENTATION CONTRACT  
**Scope:** Universal program architecture for all IVDIVO audio productions.

## 1. Mission

Convert a locked text/story into a production package that preserves story, character, context, human physicality, spatial reality, emotional contrast and release quality.

## 2. Required modules

- `authority_loader`
- `delivery_mode_router`
- `story_audio_analyzer`
- `scene_audio_dramaturgy`
- `character_context_engine`
- `relationship_state_engine`
- `performance_planner`
- `pause_director`
- `listening_breath_director`
- `blocking_spatial_director`
- `microtexture_planner`
- `food_drink_foley_planner`
- `foley_causality_graph`
- `ambience_architect`
- `object_audio_registry`
- `emotion_sound_director`
- `music_dramaturgy`
- `transition_montage_director`
- `render_block_compiler`
- `provider_performance_compiler`
- `providers/elevenlabs_dialogue`
- `providers/elevenlabs_sfx`
- `providers/elevenlabs_music`
- `take_registry`
- `asset_registry`
- `edit_director`
- `timeline_resolver`
- `spatial_automix`
- `masking_qc`
- `mastering_controller`
- `human_listener_gate`
- `selective_repair_controller`

## 3. Required data models

### SceneAudioState
`scene_id, start_state, end_state, focus_1, focus_2, background, suppress, tension_curve, density_curve, reversal, aftermath, next_listen_question`

### CharacterPerformanceState
`character_id, state_in, recent_memory, immediate_want, tactic, subtext, relationship_state, status_before, status_after, energy, tempo, physical_condition, listening_state, state_out, next_entry_impulse, forbidden_performance`

### PauseEvent
`pause_id, function, anchor_type, anchor_ref, duration_class, min_ms_optional, target_ms_optional, max_ms_optional, protected_from_music, protected_from_ambience, protected_from_foley`

### HumanTextureEvent
`event_id, character_id, texture_type, physical_cause, story_function, attention_priority, intensity, naturalism_profile, anchor, can_overlap_dialogue, asset_policy`

### FoodDrinkEvent
`event_id, action_chain, object, food_liquid_type, bite_sip_type, chew_policy, swallow_policy, utensil_container, intensity, story_function, negative_flags`

### SpatialState
`character_or_object, position, azimuth_optional, depth, distance_class, orientation, head_turn, occlusion, room_profile, ear_bias, movement_path, mono_critical`

### AmbienceLayer
`layer_id, type, physical_source, distance, activity_pattern, loop_policy, foreground_background, story_function, suppress_windows`

### FoleyEvent
`foley_id, character, action, object, material, cause, result, story_function, anchor, priority`

### EmotionSoundDesign
`beat_id, target_emotion, performance_strategy, silence_strategy, proximity_strategy, body_foley_strategy, ambience_strategy, spectral_dynamic_strategy, music_strategy, forbidden_shortcuts`

### MusicCue
`cue_id, function, value_change, entry_anchor, exit_anchor, theme_id, intensity, instrumentation, rhythm_density, harmonic_role, ducking, forbidden_implications`

### ProviderCompilation
`block_id, provider, model, exact_text, voices, context_summary, playable_behavior, tags, tag_budget, take_hypothesis, clean_dialogue, separate_assets, pronunciation_refs`

## 4. Required per-book/episode outputs

1. `authority_manifest.json`
2. `delivery_contract.json`
3. `story_audio_analysis.json`
4. `audio_dramaturgy.json`
5. `character_context_states.json`
6. `actor_director_score.json`
7. `pause_listening_breath_plan.json`
8. `blocking_spatial_plan.json`
9. `human_microtexture_plan.json`
10. `food_drink_foley_plan.json` when applicable
11. `foley_causality_graph.json`
12. `ambience_layers.json`
13. `object_audio_registry.json`
14. `emotion_sound_plan.json`
15. `music_dramaturgy.json`
16. `transition_montage_plan.json`
17. `render_block_plan.json`
18. `provider_requests/`
19. `take_registry.json`
20. `asset_registry.json`
21. `edit_decisions.json`
22. `resolved_timeline.json`
23. `automix_manifest.json`
24. `qc_report.json`
25. `human_listener_gate.md`
26. `selective_repair_list.json`
27. `master_lock.json`

## 5. Render-block logic

Supported block types:
- `TTD_BLOCK` — multi-speaker interaction requiring shared timing/context;
- `ISOLATED_TTS` — critical line or difficult performance requiring control;
- `NARRATION_BLOCK`;
- `VOCALIZATION_BLOCK`;
- `PERFORMANCE_SOUND`;
- `LOCKED_ASSET`;
- `FOLEY_ASSET`;
- `AMBIENCE_ASSET`;
- `MUSIC_ASSET`.

Do not generate the whole chapter/episode as one uncontrolled provider request.

## 6. Context handoff law

Each provider block receives a compact context packet derived from current canon, not from model improvisation:
- where we are;
- what just happened;
- what each speaker wants;
- what they know/do not know;
- current relationship/status;
- current physical/emotional state;
- what changes in this block;
- what must not be played.

`STATE_OUT(block N) → STATE_IN(block N+1)` unless an explicit scene/time reset exists.

## 7. Pause compilation

Before timing resolution, pause classes map to ranges, not false timestamps:
- QUICK BEAT
- NORMAL BEAT
- HELD
- RECOGNITION
- AFTERMATH
- NO_REPLY
- INTERRUPT WINDOW
- OBJECT-ACTION PAUSE

After accepted takes return alignment, Edit Director and Timeline Resolver place exact durations.

## 8. Human microtexture compilation

Microtexture planner may propose events from explicit action, inferred physical necessity or project overlay, but every synthetic event must record provenance and story function.

Fail closed if a generated microtexture could be misheard as:
- plot clue;
- injury;
- sexual action;
- illness;
- another person;
- hidden object/action;
- supernatural signal;
without source support.

## 9. Spatial compilation

Spatial planning produces automation instructions, not merely left/right pan.

Per moving source: `gain / direct-reverb ratio / early reflection ratio / HF attenuation / stereo or binaural position / occlusion / distance curve`.

Ear-specific dialogue is allowed as an authored effect, but `mono_critical=true` material must remain understandable after fold-down.

## 10. Emotion sound compiler

Emotion is compiled through a priority ladder:
`PERFORMANCE → PAUSE → BREATH/LISTENING → PROXIMITY → BODY/OBJECT FOLEY → AMBIENCE CONTRAST → SPECTRAL/DYNAMIC DESIGN → MUSIC`.

The engine must justify every non-diegetic emotional effect.

## 11. Provider/ElevenLabs adapter

Provider adapter consumes `ProviderCompilation`, never raw psychological notes.

It must:
- preserve exact text where locked;
- use fixed voice IDs when locked;
- carry pronunciation refs;
- use sparse performance tags;
- separate clean dialogue from ambience/SFX/music;
- isolate clue-critical or media-processed lines when required;
- hash request inputs;
- store returned alignment/timing with accepted takes;
- never overwrite locked takes/assets;
- support smallest-block selective regeneration.

## 12. Edit-before-regenerate controller

If words, voice identity and intention pass, test edit fixes first:
`trim / crossfade / pause edit / clip gain / room-tone bridge / overlap shift / reaction shift / consonant protection / breath removal-preservation / perspective automation`.

Regenerate only if the defect originates in voice/performance/pronunciation/provider artifact.

## 13. QC fail-closed gates

FAIL release if any applicable condition occurs:
- wrong authority/branch;
- missing/duplicated spoken text;
- context reset that changes character meaning;
- false guilt/romance/ontology signal;
- critical clue masked;
- spatial effect causes mono loss;
- microtexture invents unsupported action;
- eating/mouth texture becomes distracting/gross contrary to style;
- dialogue/SFX/music masking;
- recurring object/motif identity drift;
- voice drift;
- unnatural cadence or syllable artifact on critical line;
- unprotected reveal silence;
- music enters forbidden window;
- unresolved asset/cue;
- loudness/peak/master failure.

## 14. Definition of done

A production is done only when the system can prove:
1. source/canon integrity;
2. complete spoken coverage;
3. coherent character state continuity;
4. intentional pauses and reactions;
5. believable human/object/world sound;
6. spatial continuity;
7. music dramaturgy compliance;
8. accepted/locked take and asset provenance;
9. technical QC;
10. human listening gate;
11. final master lock.