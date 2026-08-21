# IVDIVO AUDIO — SHARED MUSICAL FACT + MOTIF CONTRACT v1.0

**Status:** CURRENT UNIVERSAL AUDIO CONSISTENCY GATE  
**Established:** 2026-08-21  
**Scope:** plot-relevant pitched sounds, hummed/sung fragments, bells/tones, leitmotifs, clue intervals and musical identities that cross voice, performance-sound, SFX/procedural and music-provider paths.  
**Parent authority:** current IVDIVO Audio Production Authority / Studio v3.3.  
**Story authority:** unchanged; this contract preserves a story fact, it does not invent one.

## 1. Problem class

If the listener must recognize that two or more pitched events are the same melody, continuation, interval, warning tone, clue family or transformed motif, independent generation by separate provider paths is unsafe.

A voice hum, a TTS/performance audio tag, a generated SFX and a music cue may each sound plausible in isolation while being mutually incompatible as one story fact.

Therefore:

> **If story inference depends on musical identity, musical identity must be specified once and inherited by every generating/rendering path.**

Independent unconstrained generation of the related pitched events is a FAIL.

## 2. Required object

Create one `MUSICAL_FACT_CONTRACT` before provider generation whenever the fact is clue-bearing, identity-bearing, continuity-bearing or payoff-bearing.

Minimum fields:

```yaml
musical_fact_id:
project_id:
story_function:
listener_must_infer:
source_story_authority:
source_story_hash_or_revision:

identity:
  tonal_reference:
  reference_pitch_hz_or_midi:
  interval_sequence:
  rhythmic_cell:
  contour:
  tempo_or_relative_timing:
  mode_or_tonal_center_if_relevant:
  articulation_if_story_relevant:

bindings:
  voice_or_hum_events: []
  performance_sound_events: []
  sfx_or_procedural_events: []
  music_events: []

variation_policy:
  exact_elements: []
  allowed_transformations: []
  forbidden_transformations: []
  pitch_tolerance_cents:
  rhythm_tolerance:

verification:
  method:
  rendered_asset_hashes: []
  measured_pitch_or_interval_evidence: []
  result:

status:
```

Do not require tonal fields that are meaningless to the actual fact. Do require enough information to prove the relationship the listener is expected to hear.

## 3. Story-function classes

Use the gate when the pitched relationship functions as any of:
- `CLUE_IDENTITY`;
- `MELODY_CONTINUATION`;
- `CALL_RESPONSE`;
- `CHARACTER_MEMORY_ANCHOR`;
- `LOCATION_OR_SYSTEM_IDENTITY`;
- `WARNING_OR_INTERFACE_CODE`;
- `LEITMOTIF_PAYOFF`;
- `TRANSFORMATION_RECOGNITION`;
- `PITCHED_OBJECT_IDENTITY`;
- another explicitly declared listener inference.

Decorative background music with no listener inference does not automatically require this contract.

## 4. Compilation law

The production order for a shared musical fact is:

`LOCKED STORY FACT -> MUSICAL_FACT_CONTRACT -> PITCH/RHYTHM REFERENCE ASSET OR MACHINE SPEC -> PROVIDER-SPECIFIC BINDINGS -> GENERATION/RECORDING -> ALIGNMENT -> MUSICAL FACT VERIFICATION -> ACCEPT/REPAIR -> MIX`

The contract must be upstream of:
- actor/voice instructions when a performer hums/sings/imitates the fact;
- performance-sound generation;
- pitched SFX/procedural generation;
- music-generation prompts that quote, answer or harmonically complete the fact.

## 5. Provider independence

ElevenLabs or any other provider is an execution backend, not musical authority.

If a provider cannot accept a sufficiently constrained pitch/melody reference, use a controllable method instead: performed/recorded source, procedural synthesis, MIDI/instrument render, verified reference asset or another backend capable of preserving the required identity.

Do not force a generative backend to perform a clue it cannot reliably preserve.

## 6. Verification gate

Before an asset can be accepted as a story-bearing musical fact:
1. confirm every bound event points to the same `musical_fact_id`;
2. measure or otherwise verify the required pitch/interval/rhythm relationship;
3. confirm allowed transformation only;
4. confirm no provider/path silently changed the identity;
5. listen in assembled causal context;
6. confirm mono/headphone/target playback does not destroy the inference where relevant.

Aesthetic similarity is not enough when exact interval/melody continuity is the clue.

## 7. Repair law

On FAIL, repair the smallest failing asset or binding.

Do not rewrite locked story, dialogue or clue order merely because one musical asset missed the contract.

`FAILED MUSICAL FACT -> IDENTIFY FAILED BINDING/ASSET -> REGENERATE/REPERFORM THAT ASSET -> REVERIFY SHARED CONTRACT -> SELECTIVE MIX REGRESSION`

Previously accepted unrelated dialogue/Foley/ambience/mix assets remain locked.

## 8. Recurring asset law

Once a musical identity is accepted:
- store the reference spec/asset and hash;
- reuse or derive from that locked source rather than independently reinventing it per episode;
- version intentional evolution explicitly;
- preserve project-specific identity inside the project overlay/ledger.

## 9. Cross-project law

The **contract mechanism** is universal. Actual melodies, interval patterns, pitches, motifs and clue identities are project-specific and must never transfer between projects merely because this universal gate exists.

## 10. Acceptance criteria

PASS only when:
- the story-required relationship is explicit;
- all provider/render paths inherit one contract;
- required identity is verified after render;
- the listener inference survives assembled context;
- there is no unresolved FATAL/MAJOR musical-fact inconsistency.

FAIL CLOSED when the listener is expected to recognize a musical relationship that the pipeline has no technical means to preserve or verify.

**ONE STORY FACT -> ONE SHARED MUSICAL CONTRACT -> MANY BOUND RENDER PATHS -> ONE VERIFIED LISTENER INFERENCE.**
