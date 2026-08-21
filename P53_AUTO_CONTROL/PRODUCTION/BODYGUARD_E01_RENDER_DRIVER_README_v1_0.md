# BODYGUARD E01 — Rough Render Driver v1.0

This package turns the locked E01 request manifest into a controlled ElevenLabs rough-render run.

## Inputs
- `BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json`
- `BODYGUARD_E01_CURRENT_VOICE_MAP_TEMPLATE_v1.json`
- `BODYGUARD_E01_TAKE_MANIFEST_TEMPLATE_v1.json`

## Default: dry-run

```bash
python bodyguard_e01_render_driver.py \
  --requests BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json \
  --voice-map BODYGUARD_E01_CURRENT_VOICE_MAP_TEMPLATE_v1.json \
  --take-manifest BODYGUARD_E01_TAKE_MANIFEST_TEMPLATE_v1.json
```

Dry-run validates 190 spoken blocks, exactly 1,344 spoken words, the locked spoken-sequence SHA-256, unique block IDs, exact-text hashes, voice-role coverage and 405 planned takes. It makes no provider calls.

## Before execution
Fill `voice_id` and `model_id` for every used role after blind audition. Do not put the API key into JSON or Git.

```bash
export ELEVENLABS_API_KEY="..."
```

Optional:

```bash
export ELEVENLABS_BASE_URL="https://api.elevenlabs.io"
export ELEVENLABS_OUTPUT_FORMAT="mp3_44100_128"
```

## Execute

```bash
python bodyguard_e01_render_driver.py \
  --requests BODYGUARD_E01_ELEVENLABS_ROUGH_RENDER_REQUESTS_v1.json \
  --voice-map BODYGUARD_E01_CURRENT_VOICE_MAP_TEMPLATE_v1.json \
  --take-manifest BODYGUARD_E01_TAKE_MANIFEST_TEMPLATE_v1.json \
  --output-dir renders/E01 \
  --ledger-out BODYGUARD_E01_TAKE_MANIFEST_WORKING_v1.json \
  --execute
```

Use `--limit 5` for a controlled first live-request test. Use repeated `--only-block` arguments for calibration subsets.

## Fail-closed behavior
The driver stops before network calls if count is not 190 blocks, spoken count is not 1,344, spoken SHA differs from authority, line hashes differ, voice binding is missing for execution or the take ledger does not match planned take IDs.

The driver never inserts performance directions into spoken text.

## Output
For each take: raw audio, `.meta.json` sidecar, audio SHA-256, provider request ID when returned, and updated working take ledger. Absolute timestamps remain null until edit/render alignment.

The original take-manifest template is not overwritten by default. Execution writes a `.working.json` ledger unless `--ledger-out` is supplied.

## After render
QC every take → select one passing take per block → assemble dialogue with no music → add critical SFX → process acoustic domains → stereo/mono/phone QC → blind-listener test → pickups only from repeated evidence.
