# IVDIVO — ELEVENLABS PROVIDER ADAPTER CONTRACT v1.1
## VERIFIED RUNTIME PROFILE — 2026-08-20

**Status:** CURRENT PROVIDER-SPECIFIC IMPLEMENTATION CONTRACT  
**Authority level:** below IVDIVO universal Audio Studio canon v3.2; cannot override story/text/performance authority.  
**Verification basis:** official ElevenLabs API documentation checked 2026-08-20.

## 0. Purpose
This contract translates provider-neutral IVDIVO render/performance objects into current ElevenLabs requests while isolating ElevenLabs-specific schemas behind an adapter boundary.

Internal chain:
`IVDIVO RENDER BLOCK → PROVIDER-SAFE PERFORMANCE PACKET → ELEVENLABS ADAPTER → RAW RESPONSE → ALIGNMENT NORMALIZER → PROVIDER-NEUTRAL RECORDS`.

No downstream timeline/QC module may read raw ElevenLabs timestamp payloads directly.

## 1. Authentication / secret law
Current ElevenLabs authentication uses `xi-api-key`.
The API key is read from environment/secret manager; never stored in GitHub/Drive/manifests/logs/hashes; never printed. Default environment variable: `ELEVENLABS_API_KEY`.

A 403 may result from IP allowlisting as well as authorization failure, so connectivity/credential diagnosis stays separate.

## 2. Current verified endpoint profiles
### `ELEVEN_TTD_TIMESTAMPS_V1`
`POST /v1/text-to-dialogue/with-timestamps`

Documented request:
- `inputs[]` with `text` + `voice_id`;
- `model_id` optional; documented default `eleven_v3`;
- optional `language_code`, `settings`, `pronunciation_dictionary_locators`, `seed`, `apply_text_normalization`.

Documented constraints:
- max 10 unique voice IDs;
- reliability guidance: total chars across inputs at or below ~2,000/request;
- max 3 pronunciation dictionary locators;
- seed 0..4294967295, best-effort determinism only.

Documented response can include `audio_base64`, `voice_segments[]`, `alignment`, `normalized_alignment`.

### `ELEVEN_TTS_TIMESTAMPS_V1`
`POST /v1/text-to-speech/{voice_id}/with-timestamps`

Documented request requires `text`; optional model currently documents default `eleven_multilingual_v2`, plus language/voice settings/pronunciation/text normalization controls.

Documented response includes `audio_base64` and character alignment arrays; `normalized_alignment` may also be present.

This structural difference from TTD is a confirmed production risk and is normalized internally.

### `ELEVEN_MODELS_V1`
`GET /v1/models` — preflight model/capability verification, including `can_do_text_to_speech` and request-length metadata where returned.

### `ELEVEN_VOICE_GET_V1`
`GET /v1/voices/{voice_id}` — verify known bound voice ID availability. A searchable list also exists at `GET /v2/voices` but is not required merely to verify a known binding.

## 3. Output format law
Current endpoint default is documented as `mp3_44100_128`.
Prefer a lossless provider format when current endpoint/account supports it, but do not hard-code an unverified `wav_48000` assumption into permanent canon. Retain provider original and convert once through documented ingest to the project’s 48 kHz production chain when needed.

## 4. Model law
Every live request explicitly records chosen `model_id`. Preflight verifies model existence and `can_do_text_to_speech=true` where required. Provider defaults are not IVDIVO production choices.

## 5. Voice binding law
Every live block checks `voice_id` against `VOICE_BINDING_LEDGER`. Preflight may call `GET /v1/voices/{voice_id}`. Mismatch/unavailable binding fails closed.

## 6. TTD constraints
Before dispatch:
- at least two turns for a conversational TTD block;
- non-empty text + voice ID each turn;
- unique voices <=10;
- chars <= configured ceiling (default verified guidance 2000);
- pronunciation locators <=3;
- voice bindings valid;
- request hash + regen boundary present.

## 7. Isolated TTS law
Use isolated timestamp TTS for clue/identity/pronunciation/high-acting-risk lines, unique processing domain, likely selective regeneration or independently controlled narration/vocalization. Do not fragment every conversation automatically.

## 8. Seed law
Seed is provenance/best-effort reproducibility metadata, not guaranteed deterministic acting and not by itself a valid controlled performance hypothesis.

## 9. Pronunciation law
TTD currently documents max 3 pronunciation dictionary locators/request. Store locator ID + version ID.

## 10. Alignment normalization boundary
Raw provider payloads are archived but never consumed directly downstream. `alignment_normalizer.py` maps supported profiles into `NORMALIZED_ALIGNMENT_RECORD`.

Unknown schema: `FAIL_ALIGNMENT_SCHEMA_UNSUPPORTED`. Malformed/non-normalizable schema: `FAIL_ALIGNMENT_NORMALIZATION`.

## 11. Live evidence
Per live request persist sanitized request JSON, request SHA-256, raw response JSON with base64 audio removed/replaced by evidence marker, decoded provider-original audio, raw alignment evidence, normalized alignment, model/profile/output metadata, dispatch timestamp and safe request IDs when available.

`BUILD_MANIFEST` truthfully classifies `DRY_RUN | LIVE | MIXED`.

## 12. Provider preflight
Before live dispatch:
`PROVIDER_CONTRACT_CURRENT + PROVIDER_CONNECTIVITY_PASS + PROVIDER_CREDENTIAL_PASS + PROVIDER_MODEL_PASS + PROVIDER_VOICE_PASS = PROVIDER_PREFLIGHT_PASS`.

Safe preflight uses read-only checks where possible; no need to spend synthesis credits merely to prove connectivity.

## 13. Clean-first law
Voice requests produce clean performance masters. Do not bake final ambience, score, Foley, clue SFX, room reverb or mastering into clean dialogue. Device processing normally stays post-chain so clean accepted source remains reusable.

## 14. Error mapping
- network/timeout → `FAIL_PROVIDER_CONNECTIVITY`
- 401/403 auth/allowlist → `FAIL_PROVIDER_CREDENTIAL`
- model/voice unavailable → `FAIL_PROVIDER_CAPABILITY`
- request validation → `FAIL_PROVIDER_REQUEST`
- unsupported timestamp shape → `FAIL_ALIGNMENT_SCHEMA_UNSUPPORTED`
- malformed timestamps → `FAIL_ALIGNMENT_NORMALIZATION`
- voice mismatch → `FAIL_VOICE_BINDING_DRIFT`
- synthesis defect → `FAIL_AI_ARTIFACT`

## 15. External/runtime facts
Endpoint paths, defaults, model IDs, voice availability, request limits, output formats, billing/tier restrictions and response shapes are runtime provider facts and must be re-verified on material adapter updates.

## 16. Verification sources
Official ElevenLabs docs checked 2026-08-20: Create dialogue with timestamps; Create speech with timing; API Authentication; List models; Get/List voices. No third-party API description controls this adapter.
