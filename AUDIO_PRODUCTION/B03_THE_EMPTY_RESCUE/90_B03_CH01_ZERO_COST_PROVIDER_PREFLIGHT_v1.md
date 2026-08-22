# B03 CH01 — ZERO-COST PROVIDER PREFLIGHT v1

Date: 2026-08-22
Status: **API CONTRACT VERIFIED / ACCOUNT-SPECIFIC VOICE ACCESS BLOCKED / NO LIVE CALL MADE**

## Scope
Downstream audio production only. Locked B03 story text is immutable. This artifact verifies the current provider contract and defines the next paid evidence steps; it does not claim provider access, rendering, alignment quality, pronunciation success, or voice lock.

## Verified current ElevenLabs contract
- Current voice listing endpoint: `GET /v2/voices`.
- Current model listing endpoint: `GET /v1/models`.
- TTS with character timing: `POST /v1/text-to-speech/{voice_id}/with-timestamps`.
- Timing response includes both `alignment` and `normalized_alignment`.
- Default output format is `mp3_44100_128`; higher-end PCM/WAV availability depends on subscription tier.
- `model_id` is explicit; timing endpoint currently defaults to `eleven_multilingual_v2` if omitted.
- Current quality guidance identifies `eleven_v3` as flagship and recommends it for professional content/audiobooks.
- `eleven_v3` limit is 5,000 characters/request; B03 CH01 dry max block is 1,409 characters.
- Pronunciation dictionary locators are supported; Slovenian pronunciation stays fail-closed until audition/local lock.
- `seed` is best-effort deterministic only.
- `previous_text` / `next_text` and request IDs can support continuity, but accepted-take provenance remains explicit.

## Voice-source caution
ElevenLabs is replacing its Default voices. Current documentation says Default voices expire on 2026-12-31 and are only available to accounts created before March 2026. B03 must not encode old/default voice names or IDs as durable authority. Candidate IDs must be read from the actual connected account/workspace at execution time.

## Zero-cost preflight result
PASS: source/version/hash, exact-text mode, provider schema, dry compiler, output/alignment contract, model-size compatibility, bounded retry policy and secrets policy.

OPEN: authenticate, enumerate actual account voices, confirm subscription-supported output formats, bind temporary S0 IDs, verify current account quota/credit.

## Model policy
Production candidate: `eleven_v3`. Fallback comparison: `eleven_multilingual_v2` only if S0/S1 produces a concrete stability/pronunciation/alignment/long-form reason. Do not vary model family inside a fair A/B/C voice comparison.

## Next stage
`S0 TECHNICAL CANARY` only after actual provider account access, real temporary voice IDs, explicit provider-spend authorization, and immediate source/exact_text hash recheck. No bulk CH01 render and no CH02–29 provider work yet.
