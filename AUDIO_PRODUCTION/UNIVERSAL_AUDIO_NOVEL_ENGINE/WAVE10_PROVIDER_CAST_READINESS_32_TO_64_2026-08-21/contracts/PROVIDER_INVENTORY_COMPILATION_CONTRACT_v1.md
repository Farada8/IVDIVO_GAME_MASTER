# PROVIDER INVENTORY COMPILATION CONTRACT v1

Status: WORKING engineering contract.

## Purpose
Turn one fresh authenticated secret-free ProviderSnapshot into a normalized provider-neutral capability inventory that downstream casting code can inspect without touching provider credentials.

## Required input
- current ProviderSnapshotContract PASS;
- provider identity;
- account fingerprint;
- snapshot hash and capture time;
- explicit voice/model maps.

## Required output
- normalized model rows with model IDs and declared provider capability fields;
- normalized voice rows with real provider voice IDs and metadata hashes;
- explicit TTS-capable model IDs only where provider metadata says `can_do_text_to_speech=true`;
- source snapshot hash and account fingerprint binding;
- `selection_authority=HUMAN_OR_EXPLICIT_CAST_RULES`;
- `voice_lock=false` and `auto_substitution=false`.

## Fail/HOLD
Invalid or stale snapshot -> `HOLD_PROVIDER_SNAPSHOT`.
No voices or no explicitly TTS-capable model -> `HOLD_CAPABILITY_INCOMPLETE`.
Unknown/absent provider fields remain unknown; compiler may not infer them.

## Evidence ceiling
Inventory compilation is engineering normalization. It does not establish artistic suitability, language quality, pronunciation, cast chemistry, provider spend or release approval.
