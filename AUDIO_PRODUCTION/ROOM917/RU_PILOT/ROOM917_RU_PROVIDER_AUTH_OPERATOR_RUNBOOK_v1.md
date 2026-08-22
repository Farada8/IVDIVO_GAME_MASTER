# ROOM917 — RU PROVIDER AUTH OPERATOR RUNBOOK v1

**Status:** ACTIVE BLOCKER RUNBOOK / NO STORY CHANGE / NO TTS SPEND BY THIS FILE  
**Date:** 2026-08-22  
**Scope:** unblock authenticated native-Russian ElevenLabs candidate discovery, then bounded S0 audition only.

## Current proven state

- `RU_NATIVE_VOICE_DISCOVERY.json` exists in `main`.
- Its current status is `HOLD_PROVIDER_AUTH_REQUIRED`.
- `candidate_count = 0` and `paid_synthesis_calls = 0`.
- `RU_VOICE_DISCOVERY.json` reports `SKIPPED_NO_REPOSITORY_SECRET`.
- Live provider probes proved that reliable filtered/paginated production discovery requires authenticated provider access.
- No RU voice is cast-locked.
- Full E01 paid render is forbidden.

## Secret handling law

The ElevenLabs API key must **never** be pasted into chat, committed to GitHub, written into Google Drive, printed in logs, or copied into an artifact.

Preferred route: configure repository secret `ELEVENLABS_API_KEY` in GitHub Actions Secrets for `Farada8/IVDIVO_GAME_MASTER`.

An alternative authenticated provider export may be used only if its provenance and filtered query can be verified. Public website voice names are reference-only and are not binding evidence.

## After the repository secret exists

1. Run `.github/workflows/room917-ru-voice-discovery.yml`.
2. Confirm the workflow emits both:
   - `AUDIO_PRODUCTION/ROOM917/RU_PILOT/provider/RU_NATIVE_VOICE_DISCOVERY.json`
   - `AUDIO_PRODUCTION/ROOM917/RU_PILOT/provider/RU_VOICE_DISCOVERY.json`
3. Require `paid_synthesis_calls = 0` for discovery.
4. Require provider snapshot status `PASS_CANDIDATES_FOUND`; otherwise remain HOLD.
5. Require role-ranked arrays for `ELENA`, `JULIAN`, `MINA`, `CATE`.
6. Preview only the top viable candidates and shortlist **up to 3 per role**.
7. Reject any candidate that fails provider durability/identity gates or distracts with non-native Russian.
8. Do not infer cast lock from metadata ranking or one attractive preview.

## S0 binding gate

Only after authenticated snapshot + preview evidence:

- create `AUDIO_PRODUCTION/ROOM917/RU_PILOT/ROOM917_RU_S0_NATIVE_BINDINGS.json`;
- bind each role to a provider voice identity supported by the fresh snapshot;
- preserve snapshot hash/provenance;
- historical/default diagnostic IDs remain forbidden as production authority.

## Paid S0 gate

Paid synthesis is **not** authorized merely because provider auth exists.

The S0 workflow must still require all of:

- manual `workflow_dispatch`;
- `confirm_spend=YES`;
- `max_blocks` exactly `4` or `6`;
- repository secret present;
- fresh provider snapshot present;
- approved native bindings present;
- native bundle compiler PASS;
- supported audition format only (`mp3_44100_128` or allowed equivalent in current compiler);
- `full_episode_render_forbidden=true`.

S0 files are audition evidence, not final production masters. Final E01 production remains 48 kHz / 24-bit after cast lock and assembly.

## Human cast gate

For each role test:

- native Russian pronunciation;
- age/character fit;
- naturalism / absence of obvious TTS performance;
- microemotion and subtext;
- precision under pressure;
- repeat-take identity consistency.

Then run pair tests:

- Elena ↔ Mina: practical compatibility, no exposition recital;
- Elena ↔ Julian: competence friction, no alpha/seduction default;
- Cate clean line ↔ cassette context: same ordinary woman, medium degradation only in post.

Founder credibility listen remains mandatory before cast lock.

## Eleven v3 / Voice Library risk rule

Voice Library candidates must be auditioned rather than assumed suitable for Eleven v3. If a candidate/voice class fails naturalism, pronunciation, microemotion or pair chemistry across two correctly directed canary attempts, do **not** rescue it through tag stacking, story rewriting or exaggerated post-processing. Test a user-controlled native-RU IVC or Voice Design candidate for that failed role only; any new paid fallback requires separate explicit authorization.

## Resume point

`AUTH -> ZERO-SPEND DISCOVERY -> PREVIEW -> SHORTLIST <=3/ROLE -> NATIVE BINDINGS -> EXPLICIT PAID S0 -> MACHINE QC -> HUMAN/FOUNDER LISTEN -> CAST LOCK -> CONTROLLED E01 BLOCK RENDER`
