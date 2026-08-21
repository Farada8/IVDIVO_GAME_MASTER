# AUDIO NOVEL ENGINE — WAVE9 PROVIDER BRIDGE 01–04

**Status:** CODE READY / FRESH CI REQUIRED / EXTERNAL CREDENTIAL HOLD  
**Authority effect:** NONE until review/CI/merge.

## Result
Wave9 prompts 01–04 were executed to the real evidence boundary.

- **WAVE9-01 — PASS:** provider access surface inventoried. Existing ElevenLabs adapter uses runtime-only `ELEVENLABS_API_KEY`; no provider-account connector exists in the current ChatGPT integration surface.
- **WAVE9-02 — PASS_ENGINEERING:** secret boundary frozen. Provider credentials may exist only ephemerally in a trusted runtime; API keys/auth headers/cookies/tokens/raw provider user ID may not persist.
- **WAVE9-03 — CODED / CI REQUIRED:** added `ProviderSnapshotContract`, read-only ElevenLabs snapshot acquisition, controlled-dispatch enforcement, and regression tests.
- **WAVE9-04 — HOLD_EXTERNAL_CREDENTIAL:** no authenticated credential is available here, so no account inventory/quota/voice/model evidence is fabricated.

## Concrete defect repaired
Before this patch, `controlled_provider_dispatch.py` accepted `status=PASS` plus matching `voices`/`models` as capability evidence even though the architecture described the artifact as authenticated. Schema, authenticated capture, provenance, source coverage, canonical hash and freshness were not enforced at that boundary.

The patch now requires a secret-free provider snapshot with:
- schema `ivdivo.provider_snapshot/1.0`;
- authenticated runtime capture;
- `credential_persisted=false`;
- capture-engine identity;
- HTTP-200 evidence for `/v1/user`, `/v1/user/subscription`, `/v1/models`, `/v2/voices`;
- hashed account fingerprint;
- explicit model/voice maps;
- canonical snapshot hash;
- max age 6 hours before live capability PASS;
- no automatic voice substitution.

## Trusted acquisition path
`python audio/studio/elevenlabs_snapshot_acquirer.py --out <secret-free-snapshot.json>`

The acquirer issues read-only account/capability GETs only. No paid TTS/TTD call is issued by the acquirer.

## Evidence boundary
Provider calls from this conversation: **0**.  
Paid synthesis calls: **0**.  
Human listening claims: **0**.  
Real provider snapshot: **not yet acquired**.

The prior v1 branch/PR #121 passed Audio Studio Runtime Tests run #103, but its base moved rapidly. This v2 branch was recreated from the newer `main` and requires its own fresh PR CI before merge.
