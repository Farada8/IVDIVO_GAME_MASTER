# NEXT GATE — AUTHENTICATED READ-ONLY SNAPSHOT

Do not spend credits yet.

## Required runtime action
Run:

`python audio/studio/elevenlabs_snapshot_acquirer.py --out <secret-free-snapshot.json>`

in a trusted runtime where `ELEVENLABS_API_KEY` is available as an ephemeral environment secret.

## Required PASS evidence
The resulting file must pass `ProviderSnapshotContract` and show:
- authenticated capture;
- credential_persisted=false;
- required four read-only endpoint families with HTTP 200 evidence;
- current model inventory including the required TTS/dialogue model capability;
- current voice inventory;
- secret-free account fingerprint;
- snapshot hash;
- age <= 6 hours when consumed by controlled paid dispatch.

## If blocked
If credential access is unavailable or invalid, persist only `HOLD_EXTERNAL_CREDENTIAL`. Do not create substitute voice IDs, model claims, quota values or fake account evidence.

## After PASS
Only then execute Wave9 provider repeatability/model capability/real voice inventory work. Paid canary remains downstream of voice + pronunciation + pre-spend locks.
