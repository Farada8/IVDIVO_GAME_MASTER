# IVDIVO — ELEVENLABS PROVIDER ADAPTER CONTRACT v1.0

**Status:** IMPLEMENTATION CONTRACT / PROVIDER-SPECIFIC, BELOW UNIVERSAL CANON  
**Purpose:** translate IVDIVO production intent into ElevenLabs-compatible requests without making ElevenLabs the source of story or directing authority.

This contract deliberately avoids hard-coding unstable API endpoint details. Before live production, the implementation engineer must verify the current official ElevenLabs API contract. Universal fields and behavior remain owned by IVDIVO.

## 1. Adapter boundary
Input:
`LOCKED_RENDER_BLOCK + PERFORMANCE_STATE + PRONUNCIATION + TAKE_POLICY + OUTPUT_REQUIREMENTS`.

Output:
`PROVIDER_REQUEST + REQUEST_HASH + PROVIDER_RESPONSE_METADATA + AUDIO_FILE + ALIGNMENT_IF_AVAILABLE`.

The adapter does not invent dialogue, clues, performance objectives, music placement or story context.

## 2. Supported logical block types
- `TTD_BLOCK` — multi-character conversational block where mutual response matters and provider capability supports it.
- `ISOLATED_TTS` — one critical line/turn requiring precise voice/performance control.
- `NARRATION_BLOCK` — narrator passage.
- `VOCALIZATION_BLOCK` — nonlexical vocal performance when supported/appropriate.
- `PERFORMANCE_SOUND` — breath/laugh/cry/effort or other human nonverbal sound, only when story-earned.

## 3. Clean-first rule
Dialogue master is generated clean.
Do not bake into clean dialogue:
- ambience;
- music;
- Foley;
- clue SFX;
- room reverb that belongs to scene acoustics;
- telephone/radio/device degradation unless the provider output is intentionally a replaceable special layer and a clean source is also retained.

Preferred chain:
`CLEAN HUMAN PERFORMANCE → ACCEPT/LOCK → POST PROCESSING / ACOUSTIC STAGING`.

## 4. Provider instruction compiler
Internal fields:
`SUBTEXT / FEAR / DESIRE / STATUS / KNOWLEDGE`.

Compile to actionable behavior:
- response speed;
- projection;
- hesitation;
- phrase-ending behavior;
- energy;
- tempo;
- restraint;
- proximity intent;
- listening/interruptibility;
- breath function.

Do not send vague direction such as `sexy`, `cinematic`, `mysterious`, `sad` when a playable behavior can express the same intent.

## 5. Context packet
Each request gets the smallest sufficient packet:
- scene objective;
- immediately previous event;
- what speaker just heard;
- partner action/context;
- current relationship/status;
- physical body state;
- expected next interaction.

Never send future plot solution or irrelevant franchise lore.

## 6. Text authority
For exact-text mode:
- `exact_text` is immutable;
- request builder must hash exact text;
- returned/transcribed text must be checked against source where feasible;
- any missing/duplicated/reordered word is a failure for protected text.

For authorized adaptation mode:
- use separately approved `performance_text`;
- retain immutable source and adaptation diff.

## 7. Pronunciation gate
Before full render:
- names;
- invented terms;
- foreign words;
- abbreviations;
- numbers/dates;
- emotionally exposed proper nouns;
- repeated clue words
must pass pronunciation sample where risk exists.

Store pronunciation rule/version in `PRONUNCIATION_MAP`.

## 8. Take policy
Default:
`TAKE_A = baseline`.
Additional takes only when there is a diagnosed hypothesis:
`TAKE_B = one-variable change`.

Critical line policy may request 2–3 diagnostic takes before lock.
Never reroll accepted material randomly.

## 9. Selective regeneration boundary
Every request carries `regen_boundary`.
A failure inside block X may not invalidate locked block Y unless continuity evidence proves dependency.

## 10. Alignment
If provider returns alignment/timestamps, store them as provider evidence.
If not, use separate alignment stage.

No final absolute production timeline before accepted/locked audio alignment exists.

## 11. Output format
Preferred production master dialogue format:
- lossless WAV;
- 48 kHz where provider path supports it;
- retain provider-original quality before downstream conversions.

Exact live request parameters are implementation-specific and must be verified against current provider documentation before call.

## 12. SFX / music separation
If ElevenLabs is used for SFX/music generation, treat those as independent asset requests.
Do not ask one provider call to improvise dialogue + ambience + Foley + score into a final mixed scene.

Every generated asset receives:
`ASSET_ID / PROMPT / NEGATIVE_PROMPT / STORY_FUNCTION / SOURCE_PROVIDER / REQUEST_HASH / VERSION / STATUS`.

## 13. Provider failure policy
Possible failures:
`HTTP/API / VOICE_DRIFT / TEXT_MISMATCH / PRONUNCIATION / ACTING / TAG_OVERPLAY / TIMING / SYNTHESIS_ARTIFACT / ALIGNMENT / FILE_FORMAT`.

Route to smallest repair:
- request adjustment;
- new diagnostic take;
- isolated rerender;
- post edit;
- different provider/backend if necessary.

Provider failure may not rewrite story canon.

## 14. Security
Never commit API keys/secrets to GitHub or Drive documents.
Use environment variables / secret manager in execution environment.
Logs must redact credentials and authorization headers.

## 15. Live-call gate
Before any live request:
`AUTHORITY_PASS + PERFORMANCE_PLAN_PASS + RENDER_BLOCK_COVERAGE_PASS + PRONUNCIATION_GATE + REQUEST_HASH_PASS + PROVIDER_CONTRACT_CURRENT`.

If current API capability is uncertain, stop and audit official documentation before live calls.
