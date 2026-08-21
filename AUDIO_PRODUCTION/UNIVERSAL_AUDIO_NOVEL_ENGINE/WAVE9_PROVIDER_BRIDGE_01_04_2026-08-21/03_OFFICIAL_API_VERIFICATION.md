# OFFICIAL ELEVENLABS API VERIFICATION — 2026-08-21

Checked against current official ElevenLabs documentation before freezing the acquirer contract.

## Read-only snapshot endpoints
- `GET /v1/user` — account identity/subscription envelope; raw `user_id` must not persist, only a one-way SHA-256 fingerprint.
- `GET /v1/user/subscription` — tier/status/usage/quota evidence.
- `GET /v1/models` — current model inventory and TTS capability fields.
- `GET /v2/voices` — current user-visible voice inventory; pagination uses `has_more` and `next_page_token`; `page_size` max 100.

## Existing render endpoints reverified
- `POST /v1/text-to-dialogue/with-timestamps` — dialogue plus timing; default model `eleven_v3`; maximum 10 unique voice IDs; ElevenLabs recommends total dialogue input at or below 2,000 characters for reliable generation.
- `POST /v1/text-to-speech/{voice_id}/with-timestamps` — single-voice speech with alignment.

## Engineering consequence
The current repository adapter endpoint choices remain compatible with official API documentation. Wave9 provider hardening therefore does not replace the provider adapter. It adds authenticated account/capability acquisition and stronger evidence validation in front of paid dispatch.

## Evidence law
Documentation confirms endpoint contracts. It does not prove this account's current voices, plan, quota, model access or live provider behavior. Those remain blocked until an authenticated read-only snapshot is actually acquired.
