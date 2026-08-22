# B03 — PROVIDER EXECUTION BRIDGE v1

**Date:** 2026-08-22  
**Status:** CURRENT EXECUTION CONTRACT / NO LIVE CALL CLAIMED

## Purpose

Bind B03's already-complete pre-live manifests to current ElevenLabs provider surfaces without changing story or audio canon.

## Current provider surfaces

### Voice discovery / TTS
- Voice enumeration: `GET /v2/voices`.
- Model enumeration: `GET /v1/models`.
- TTS with character timing: `POST /v1/text-to-speech/{voice_id}/with-timestamps`.
- B03 production model candidate: `eleven_v3`, subject to live workspace/model preflight.

### Sound effects
- Sound generation: `POST /v1/sound-generation`.
- Current default SFX model in API reference: `eleven_text_to_sound_v2`.
- Prompt field: `text`.
- Optional controls include `duration_seconds`, `loop`, `prompt_influence`, and output format.
- B03 C0–C2 asset canaries can use this same provider context after account/auth/spend gate.
- C3 playback chain is NOT a new sound-generation job; it derives from the accepted first-caller take.

## Execution path

1. Keep API key/secret only in execution environment.
2. Authenticate provider context.
3. Enumerate real workspace voices and available models.
4. Bind temporary S0 voice candidates; do not create voice lock.
5. Recheck CH01 source SHA256 and exact-text hashes immediately before dispatch.
6. Run only four S0 TTS jobs.
7. Save response provenance, request IDs/headers where available, raw audio and alignment.
8. If S0 passes, enter S1 casting cascade.
9. In parallel, run only SFX asset canaries C0–C2 through `/v1/sound-generation` or an approved recording path.
10. Accept/reject through artifact 102; only accepted assets enter Hard Pilot assembly 103.

## MCP / agent tooling option

ElevenLabs documentation currently describes a hosted MCP server at `https://api.elevenlabs.io/v1/mcp` using OAuth sign-in for compatible MCP clients. This is an execution option, not canon authority. Use only if the active client/environment supports custom MCP connections and exposes the required voice/SFX operations.

## Cost-control law

Do not hardcode numeric credit cost into B03 authority. Current ElevenLabs documentation surfaces different cost descriptions across pages/product modes; provider account state and current response/account billing data are the execution authority. The studio rule remains: smallest S0/SFX canary first, then survivors only.

## Hard stops

- No secrets in GitHub/Drive/prompts.
- No bulk render before S0 + casting evidence.
- No claim that provider access, SFX generation, audio listening or alignment happened until real evidence exists.
- No independent regeneration of the stored first-caller playback identity.
