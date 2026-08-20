# IVDIVO AUDIO STUDIO — CANON PATCH v3.2 AUDITED

**Date:** 2026-08-20  
**Status:** CURRENT ADDITIVE CANON / AUDIT CLOSURE  
**Input audit:** `IVDIVO_STUDIO_v3_1_INDEPENDENT_AUDIT.md`  
**Applies over:** consolidated v3.1 + v2.1/v2.2/v2.3 underlying audio canon.

## Verdict
The independent audit verdict `READY WITH BLOCKERS` is accepted. No structural rewrite is required. The blockers are concentrated in provider alignment normalization, live-vs-dry-run provenance, stereo-integrity QC, and cross-domain acoustic identity. v3.2 closes those gaps additively.

## 1. Provider-neutral alignment normalization — MAJOR
Raw provider timestamp payloads are adapter-local evidence only. No downstream timeline/QC module may directly consume ElevenLabs-specific fields.

Canonical record:
`NORMALIZED_ALIGNMENT_RECORD{provider, endpoint_profile, source_schema, block_id, unit_id, unit_index, start_seconds, end_seconds, text_ref, confidence_or_quality, raw_evidence_ref}`.

Known provider schema families may include segment-style multi-speaker timing and character-array single-speaker timing. The exact external field names remain runtime provider details. `alignment_normalizer.py` must detect a supported family, normalize it, preserve raw evidence, and fail closed on unknown/invalid shapes.

New failures:
`FAIL_ALIGNMENT_SCHEMA_UNSUPPORTED / FAIL_ALIGNMENT_NORMALIZATION`.

## 2. Live / dry-run evidence invariant — MAJOR
Every build has `BUILD_MANIFEST.live_render_status = DRY_RUN | LIVE | MIXED`.

A release candidate may not be `DRY_RUN`.

Every required live block stores:
`REQUEST_ARTIFACT / PROVIDER_RESPONSE_ARTIFACT / AUDIO_ARTIFACT / RAW_ALIGNMENT_ARTIFACT_IF_ANY / REQUEST_HASH / DISPATCHED_AT`.

Reused material stores:
`REUSED_FROM_BUILD_ID / ORIGINAL_TAKE_OR_ASSET_ID / PROVENANCE_CHAIN / COMPATIBILITY_CHECK`.

New failures:
`FAIL_MISSING_LIVE_EVIDENCE / FAIL_INVALID_REUSE_PROVENANCE`.

## 3. Cross-build provenance ownership — MEDIUM
Role 01 (Executive Audio Producer / Authority Controller) owns reuse authority and build provenance. Role 04 maintains take-level execution provenance. A copied file without provenance is not a locked reusable asset.

`TAKE_RECORD` gains:
`reused_from_build_id / original_take_id / provenance_chain`.

## 4. Voice Binding Ledger — MEDIUM
Voice locks are promoted from an undefined flat field to a first-class artifact:

`VOICE_BINDING_LEDGER{ledger_version, bindings[]}`

Per binding:
`character_id / provider / voice_id / status / locked_at / locked_by_build_id / sample_evidence / pronunciation_version / substitution_policy`.

Statuses:
`CANDIDATE / SMOKE_ONLY / APPROVED / LOCKED / SUPERSEDED`.

Actually-dispatched voice IDs are checked against the ledger. New failure: `FAIL_VOICE_BINDING_DRIFT`.

## 5. Silent reaction anchor — MEDIUM
A silent dramatic reaction is not forced into a voice render block.

Add non-dispatch:
`SILENT_REACTION_ANCHOR{anchor_id, character_id, state_in, trigger_event, silent_action, breath_or_foley_refs, silence_policy, state_out, semantic_anchor}`.

It may own silence/Foley/breath/spatial cues but does not count as spoken-text coverage and does not dispatch a provider request unless a separate performance-sound asset is explicitly attached.

## 6. Manual Review issue state — MEDIUM
QC issue states may include:
`OPEN / PASS / FAIL / MANUAL_REVIEW / RESOLVED / NOT_APPLICABLE`.

Alignment metadata echo of bracket/tag characters is not proof that the tag was audibly spoken. Such cases are `MANUAL_REVIEW` unless resolved by approved signal/ASR/human evidence.

Mandatory unresolved manual review blocks release.

## 7. Stereo-intent + source-vs-stem QC — MAJOR
A stem null test proves summation consistency but not spatial fidelity.

Every source/stem where width matters declares:
`STEREO_INTENT = MONO_INTENTIONAL | NARROW | NATURAL_STEREO | WIDE | BINAURAL_OR_POSITIONAL | SOURCE_DEPENDENT`.

QC compares:
- source L/R correlation/width;
- final-stem L/R correlation/width;
- declared stereo intent;
- whether width was lost in mix or was already absent at source.

Do **not** use `correlation == 1.0` as a universal failure. Intentionally mono assets are legal.

Diagnoses:
`PASS / SOURCE_NARROWNESS / MIXER_COLLAPSE / INTENTIONAL_MONO / MANUAL_REVIEW`.

New failure/warning:
`FAIL_UNINTENDED_STEM_STEREO_COLLAPSE / WARN_SOURCE_LEVEL_NARROWNESS`.

## 8. Causal overlap profile — MEDIUM, diagnostic only
Add:
`CAUSAL_OVERLAP_PROFILE{scene_or_beat_id, total_relevant_event_pairs, overlapping_event_pairs, causal_overlap_ratio, overlap_expected, expected_reason, status}`.

There is **no universal minimum overlap ratio**. It becomes a gate only when the project overlay/staging explicitly declares that a beat class should contain simultaneous causal events. Never add fake overlaps to satisfy a metric.

## 9. Cross-domain acoustic identity — MAJOR
When voice/SFX/music assets must be recognizably the same clue, motif or signal, prose prompts are insufficient.

Add `ACOUSTIC_IDENTITY_LEDGER` with identity subtypes:
`PITCH_IDENTITY / INTERVAL_IDENTITY / RHYTHM_IDENTITY / TIMBRE_MOTIF / SIGNAL_PATTERN / MECHANICAL_SIGNATURE`.

A `PITCH_IDENTITY_ID` may define:
`REFERENCE_PITCH_OR_RELATIVE_MODE / INTERVAL_SEQUENCE / RHYTHMIC_VALUES / TOLERANCE / TRANSPOSE_POLICY / TIMBRE_INDEPENDENT / REQUIRED_ASSET_IDS`.

`SOUND_CUE` and `MUSIC_CUE` gain `acoustic_identity_ref`.

New failure:
`FAIL_CLUE_ACOUSTIC_IDENTITY_UNLINKED`.

## 10. Provider preflight — MEDIUM
`PROVIDER_CONTRACT_CURRENT` is not a connectivity test.

Before live dispatch require `PROVIDER_PREFLIGHT_PASS` verifying, without logging secrets:
- network/provider reachability;
- credential presence/acceptance;
- requested model/voice/capability availability;
- relevant quota/rate/size constraints;
- adapter support for current response schema family.

Failures are separated:
`FAIL_PROVIDER_CONNECTIVITY / FAIL_PROVIDER_CREDENTIAL / FAIL_PROVIDER_CAPABILITY`.

## 11. Seed clarification — POLISH
A provider seed is provenance/reproducibility metadata, not a guaranteed acting/determinism lever. Changing seed alone does not qualify as a controlled single-variable take hypothesis unless validated for that provider/model.

## 12. Review Priority Queue — MEDIUM
Before human review create:
`REVIEW_PRIORITY_QUEUE{unit_or_beat_id, risk_score, risk_class, reason, evidence_ref, story_criticality, required_review_action, status}`.

The queue prioritizes human effort; it does not replace a project-required continuous first-time listen.

## 13. Gate DAG — implementation correction
The studio is a dependency graph, not a blind linear chain. `DIALOGUE_LOCK` and `ASSET_LOCK` may run in parallel once their independent prerequisites are satisfied and converge before timeline/mix stages.

Stage state adds `NOT_APPLICABLE`, allowed only with an explicit authority-backed reason. No silent skipping.

## 14. Release hardening
`RELEASE_GO` requires:
- required dependency gates PASS/LOCKED or explicitly NOT_APPLICABLE;
- open FATAL = 0;
- open MAJOR = 0;
- mandatory MANUAL_REVIEW = 0;
- unresolved anchors = 0;
- missing assets = 0;
- source/hash match;
- required live evidence complete;
- voice binding valid;
- reuse provenance valid;
- required acoustic-identity links valid;
- actual master ID/version recorded.

A `DRY_RUN` build cannot release.

## 15. Accepted/modified/rejected audit recommendations
Accepted: alignment normalization, live evidence, reuse provenance, voice ledger, silent reaction anchor, manual review, stereo integrity, overlap diagnostic, acoustic identity, provider preflight, review priority queue, DAG gates, seed clarification.

Modified rather than blindly adopted:
- no blanket `corr=1.0` failure; use intent + source comparison;
- no universal causal-overlap quota;
- silent reaction is a non-dispatch anchor, not a fake voice block.

Not adopted as a current structural change:
- mandatory split of rerecording mixer and mastering engineer into two top-level studio roles. It remains a future scale split point.
