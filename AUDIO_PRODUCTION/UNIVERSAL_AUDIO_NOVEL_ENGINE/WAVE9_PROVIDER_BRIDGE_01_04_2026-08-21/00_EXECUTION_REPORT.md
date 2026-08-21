# AUDIO NOVEL ENGINE — WAVE9 PROVIDER BRIDGE 01–04

**Status:** WORKING / CODED / EXTERNAL-CREDENTIAL HOLD  
**Date:** 2026-08-21  
**Authority effect:** NONE until review/CI/merge.  

## Why this run exists
Wave8 identified the next highest-information frontier as authenticated, secret-free provider evidence. This run executed Wave9 prompts 01–04 to the real boundary instead of opening another broad architecture cycle.

## 01 — PROVIDER ACCESS SURFACE INVENTORY
**STATUS: PASS**

Observed admissible paths:
1. Existing repository adapter: `audio/studio/elevenlabs_adapter.py` performs provider POSTs only when runtime env `ELEVENLABS_API_KEY` exists; the key is used as `xi-api-key` and is not written by the adapter.
2. Existing GitHub Actions workflow is offline/unit-test oriented and does not currently inject or use ElevenLabs credentials.
3. Current conversation/plugin surface has no ElevenLabs/speech-synthesis connector capable of authenticated account reads.
4. Admissible production path: ephemeral secret injection in a trusted runtime, then persist only redacted provider evidence.
5. GitHub/Drive/chat are forbidden secret stores for this workflow.

## 02 — SECRET INGEST BOUNDARY
**STATUS: PASS_ENGINEERING**

Contract:
- secret name: `ELEVENLABS_API_KEY`;
- acquisition: runtime environment only;
- never persist: API key, bearer/auth headers, cookies, passwords, tokens or raw user ID;
- persist: only hashed account fingerprint, read-only endpoint provenance, model/voice inventory, non-secret plan/quota fields and canonical snapshot hash;
- missing/invalid credential => fail closed before paid synthesis;
- provider snapshot acquisition issues read-only GETs only and performs no paid TTS/TTD request.

## 03 — ACCOUNT SNAPSHOT SCHEMA FREEZE
**STATUS: PASS_ENGINEERING / CI_PENDING**

Implemented:
- `audio/studio/runtime/provider_snapshot_contract.py`;
- `audio/studio/provider_snapshot_contract.py` import shim;
- `audio/studio/elevenlabs_snapshot_acquirer.py`;
- `audio/studio/tests/test_provider_snapshot_contract.py`;
- hardened `audio/studio/controlled_provider_dispatch.py` capability gate;
- hardened dispatch regression fixtures.

New production snapshot requirements:
- schema `ivdivo.provider_snapshot/1.0`;
- provider = ElevenLabs;
- `status=PASS` plus `authentication.state=AUTHENTICATED`;
- authentication method = runtime xi-api-key;
- `credential_persisted=false`;
- production capture method + exact capture engine identity;
- successful provenance for `/v1/user`, `/v1/user/subscription`, `/v1/models`, `/v2/voices`;
- SHA-256 account fingerprint; raw provider user ID is discarded;
- explicit model and voice maps;
- canonical snapshot hash;
- 6-hour freshness gate before capability PASS in controlled live dispatch;
- missing voice/model still blocks with no automatic substitution.

Important limitation: this is a process/provenance integrity contract, not a cryptographic proof against a malicious operator hand-forging a JSON file. The trusted production path is the paired read-only acquirer plus controlled dispatch.

## 04 — ACCOUNT SNAPSHOT ACQUISITION
**STATUS: HOLD_EXTERNAL_CREDENTIAL**

No authenticated ElevenLabs credential is available to this conversation/runtime and no ElevenLabs connector is installed. Therefore no account snapshot, voice inventory, model inventory, quota evidence or provider request ID was fabricated.

Provider calls from this conversation: **0**.  
Paid synthesis calls: **0**.  
External human claims: **0**.

## Current API verification
Official ElevenLabs documentation checked on 2026-08-21 confirms:
- `GET /v1/user`;
- `GET /v1/user/subscription`;
- `GET /v1/models`;
- paginated `GET /v2/voices` using `has_more` + `next_page_token`;
- `POST /v1/text-to-dialogue/with-timestamps` with default `eleven_v3`, up to 10 unique voices and recommended total dialogue text <= 2,000 characters per request;
- `POST /v1/text-to-speech/{voice_id}/with-timestamps`.

## Engineering defect found and repaired in branch
Before this patch, controlled dispatch treated a snapshot with `status=PASS` plus matching voice/model IDs as sufficient capability evidence. That was weaker than the architecture claimed: schema/authentication/provenance/hash/freshness were not verified there.

This branch closes that specific static hole. A legacy `{status: PASS, voices: ..., models: ...}` file must no longer authorize capability PASS.

## Test evidence
- ProviderSnapshotContract isolated local regression: 6/6 PASS before strengthening; strengthened suite expanded with capture-engine/source-coverage/credential-persistence cases.
- GitHub CI for the fresh branch/PR is required before merge. No historical CI is relabeled as current proof.

## Next unlock
Run the read-only snapshot acquirer in a trusted environment where `ELEVENLABS_API_KEY` exists ephemerally:

`python audio/studio/elevenlabs_snapshot_acquirer.py --out <secret-free-snapshot.json>`

Then read back and validate that snapshot before any paid canary request.
