# ROOM917 RU — ELEVENLABS AUTH HANDOFF v1.0

Date: 2026-08-22

Status: **ONE EXTERNAL MANUAL AUTH STEP REQUIRED**

Scope: ElevenLabs provider authentication for RU casting only. No story/script change. No paid render authorization.

## Proven state

`AUDIO_PRODUCTION/ROOM917/RU_PILOT/provider/RU_NATIVE_VOICE_DISCOVERY.json` is present in `main` and currently reports:

- `HOLD_PROVIDER_AUTH_REQUIRED`
- `candidate_count = 0`
- `paid_synthesis_calls = 0`
- `full_e01_render_allowed = false`

The public/unauthenticated discovery experiment is rejected. Live provider probes returned HTTP 401 for filtered discovery and pagination. See:

`AUDIO_PRODUCTION/ROOM917/RU_PILOT/ROOM917_RU_PROVIDER_AUTH_GATE_RECEIPT_v1.0.json`

## Manual action — do not paste the key into ChatGPT

### 1. Create/reuse a restricted ElevenLabs API key

In ElevenLabs:

1. Log in.
2. Open **Developers → API Keys**.
3. Create a key for ROOM917 automation, for example `ROOM917_GITHUB_DISCOVERY`.
4. Keep the key restricted. Enable only the API capabilities needed for voice/Voice Library discovery at this stage.
5. Use an expiry/usage restriction if appropriate for the account.
6. Copy the full key once when ElevenLabs shows it.

Security rule: the key is a secret. Never put it in a GitHub file, Google Drive document, issue, commit, log, or chat message.

### 2. Store it only as a GitHub Actions repository secret

Repository:

`Farada8/IVDIVO_GAME_MASTER`

GitHub UI:

**Settings → Secrets and variables → Actions → New repository secret**

Name exactly:

`ELEVENLABS_API_KEY`

Value:

paste the ElevenLabs key there.

Do not store the value anywhere else in the repository.

## What happens next automatically / safely

Run workflow:

`.github/workflows/room917-ru-voice-discovery.yml`

Expected zero-spend behavior:

1. Authenticated filtered request to ElevenLabs Voice Library.
2. Filter target: Russian + professional + notice period >= 365 days; exclude live-moderated/custom-rate candidates according to current workflow policy.
3. Write `RU_NATIVE_VOICE_DISCOVERY.json`.
4. Rank candidates separately for ELENA / JULIAN / MINA / CATE.
5. Upload a recoverable GitHub Actions artifact.
6. Publish a deterministic evidence branch before optional publication to `main`.
7. Keep `paid_synthesis_calls = 0` during discovery.

## Required readback before any paid canary

The snapshot must satisfy all of these:

- status = `PASS_CANDIDATES_FOUND`
- non-zero candidate list
- `ru_verified = true` for any bound production candidate
- professional category
- configured minimum notice period policy >= 365 days
- provider identity preserved in snapshot
- no historical diagnostic voice IDs used as production bindings

Then:

1. Preview the role-ranked candidates.
2. Shortlist up to 3 voices per role.
3. Record preview-listen result and provider identity check.
4. Create `ROOM917_RU_S0_NATIVE_BINDINGS.json` only after that evidence exists.
5. Paid S0 still requires explicit `confirm_spend=YES`.
6. Run only 4 or 6 bounded canary blocks.
7. Machine QC → human/founder credibility listen → selective recast/repair → CAST LOCK.
8. Full E01 remains forbidden until CAST LOCK.

## Current provider facts

Official ElevenLabs documentation states that API keys authenticate API requests and should be kept secret. API keys can be scope-restricted and usage-limited. Voice Library documentation also states that Voice Library voices are not available through the API to free-tier users.

The endpoint reference may display `xi-api-key` as optional for `GET /v1/shared-voices`, but ROOM917 live provider probes on 2026-08-22 demonstrated that the unauthenticated access available to our workflow is not sufficient for reliable filtered/paginated production discovery. Production policy therefore follows live evidence and fails closed.

## Hard rules

- NEVER paste `ELEVENLABS_API_KEY` into ChatGPT.
- NEVER commit the key.
- NEVER put the key in Drive.
- NEVER print the key in Actions logs.
- NO paid S0 merely because auth succeeds.
- NO full E01 render before CAST LOCK.
- NO story or dialogue rewrite to compensate for provider/voice failure.
