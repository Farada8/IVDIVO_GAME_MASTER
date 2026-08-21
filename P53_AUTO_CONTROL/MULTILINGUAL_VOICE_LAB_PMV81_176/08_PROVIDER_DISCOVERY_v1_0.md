# BODYGUARD — ELEVENLABS PROVIDER DISCOVERY — 2026-08-21 v1.0

**STATUS:** CURRENT PUBLIC-CONTRACT DISCOVERY / AUTHENTICATED ACCOUNT PREFLIGHT PENDING

## Current documented capabilities used by this lab

- Text-to-Speech with timestamps: line audio + alignment available through current ElevenLabs API contract.
- Voice Design remains a preview-then-create workflow; preview is not voice lock.
- Current Voice Design documentation includes `eleven_multilingual_ttv_v2` and `eleven_ttv_v3`; newest is not assumed best without A/B evidence.
- Eleven v3 supports broad multilingual generation including RU/EN/ES/DE/IT.
- Text-to-Dialogue with timestamps exists and accepts ordered text/voice inputs with alignment/segments.

## Production change caused by discovery

Text-to-Dialogue is now a **candidate render mode** for conversational continuity. It is not permitted to replace isolated TTS automatically.

Use isolated TTS when any of these matter:
- clue-critical exact line;
- different post-chain/acoustic domain;
- pronunciation risk;
- selective regeneration;
- protected performance line;
- threat/media/V.O./comms isolation.

Current RU compiler therefore produced:
- 35 TTD candidate blocks;
- 37 isolated TTS blocks;
- 190/190 source-line coverage.

## Account/runtime gate

Public documentation cannot prove what the user's authenticated account can access. Before paid generation, perform authenticated read-only model/capability discovery without persisting or printing the API key.

Current run: API key unavailable; billable calls = 0.
