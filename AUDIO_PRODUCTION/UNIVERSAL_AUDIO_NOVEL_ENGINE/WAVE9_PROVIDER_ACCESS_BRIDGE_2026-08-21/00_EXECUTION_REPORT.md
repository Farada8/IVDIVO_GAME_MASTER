# IVDIVO Audio Novel Engine — Wave9 Provider Access Bridge

Date: 2026-08-21
Status: WORKING / OPERATIONAL_BRIDGE_CODED / EXTERNAL_SECRET_AND_MANUAL_RUN_REQUIRED
Authority effect: NONE until merge; no provider evidence exists until a real workflow run succeeds.

## Fresh authority consumed

- current main at branch cut: `9a3467ef798b2cce840fbb37df6d8a9130d2c66a`
- merged Wave9 trust boundary / PR #132
- canonical runtime: `audio/studio/runtime`
- exact current dependency: authenticated provider access -> first real secret-free provider snapshot

## Why this bridge exists

The engine is correctly blocked on external provider evidence. Building another generic audio engine would be false progress. This bridge converts the external dependency into one bounded operational action without relaxing any evidence law.

## Implemented

1. `.github/workflows/elevenlabs-provider-snapshot.yml`
   - manual `workflow_dispatch` only;
   - reads `ELEVENLABS_API_KEY` only from GitHub Actions Secrets;
   - fails closed when the secret is absent;
   - runs the existing read-only `elevenlabs_snapshot_acquirer.py`;
   - issues no TTS/TTD synthesis request;
   - uploads the secret-free snapshot as a workflow artifact;
   - downloads the same artifact for readback;
   - builds a durable AUTH_PROVIDER receipt;
   - uploads a final secret-free evidence bundle.

2. `audio/studio/provider_snapshot_receipt.py`
   - validates source and readback snapshots independently;
   - requires production ElevenLabs ProviderSnapshotContract;
   - requires identical logical snapshot hashes;
   - requires identical raw file SHA-256 after durable readback;
   - binds GitHub Actions artifact identity/source/run transaction;
   - emits `CONTENT_HASH_VERIFIED` durable receipt;
   - validates the completed payload with canonical `validate_provider_auth_receipt`.

3. `audio/studio/tests/test_provider_snapshot_receipt.py`
   - positive identical write/readback path;
   - mutation/readback drift fail-closed path.

## Security boundary

Never store or paste `ELEVENLABS_API_KEY` in Git, Drive, ChatGPT, generated documents or artifacts. Configure it only as a GitHub Actions repository secret (or later an environment secret if an approval environment is introduced). GitHub documents that Actions secrets are explicitly injected into workflows and should be least-privilege; artifact upload/download provides digest validation. The engine additionally validates its own logical/file hashes.

## Evidence ceiling at code time

- real provider account reads: 0
- paid synthesis calls: 0
- real voice inventory claims: 0
- real model inventory claims: 0
- human review claims: 0
- voice locks: 0
- story mutations: 0

## Exact next external action after merge

1. Configure repository secret `ELEVENLABS_API_KEY` in GitHub without exposing it in chat/repo/Drive.
2. Manually run workflow `ElevenLabs Provider Snapshot Evidence`.
3. Require SUCCESS.
4. Read back the final `elevenlabs-provider-auth-evidence-*` artifact.
5. Verify `AUTH_PROVIDER = PASS` and freshness <= 6h.
6. Only then proceed to bound current model/voice inventory and casting prompts.
