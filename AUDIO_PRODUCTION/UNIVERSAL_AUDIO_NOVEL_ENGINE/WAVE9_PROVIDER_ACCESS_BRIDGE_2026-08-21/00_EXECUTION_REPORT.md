# IVDIVO Audio Novel Engine — Wave9 Provider Access Bridge

Date: 2026-08-21
Status: WORKING / FRESH_MAIN_V2 / EXTERNAL_PROVIDER_RUN_REQUIRED
Authority effect: NONE until merge; real provider evidence remains absent until a live read-only workflow succeeds.

## Fresh authority consumed
- branch base main: `f9e5d17cf95a8ce7f16118a14f3da58a49975acc`
- includes merged PR #132 external-evidence trust boundary
- includes merged PR #134 cross-class release-lineage hardening
- canonical runtime remains `audio/studio/runtime`
- exact dependency remains authenticated provider access -> first real secret-free provider snapshot

## Implemented bounded operational bridge
- manual `.github/workflows/elevenlabs-provider-snapshot.yml`
- `audio/studio/provider_snapshot_receipt.py`
- `audio/studio/tests/test_provider_snapshot_receipt.py`

The workflow reads `ELEVENLABS_API_KEY` only as a GitHub Actions secret, fails closed when absent, invokes the existing read-only snapshot acquirer, uploads the secret-free snapshot, downloads it for durable readback, then validates logical snapshot hash + file SHA-256 and emits an AUTH_PROVIDER receipt accepted by the canonical trust adapter.

No TTS/TTD synthesis request is made by this workflow.

## Durability semantics
GitHub upload/download artifact supplies its own artifact digest validation. IVDIVO additionally requires:
- ProviderSnapshotContract PASS on source and readback;
- identical logical snapshot hash;
- identical raw file SHA-256;
- trusted GitHub Actions run reference;
- `CONTENT_HASH_VERIFIED` readback strength;
- final `validate_provider_auth_receipt` PASS.

This AUTH_PROVIDER receipt proves provider snapshot acquisition/readback only. It does not satisfy LIVE_AUDIO, HUMAN_REVIEW, REAL_ALIGNMENT, MEASURED_ECONOMICS, DURABLE_RECOVERY or release-lineage classes introduced/hardened by PR #132/#134.

## Evidence ceiling during engineering
- provider/account reads: 0
- paid synthesis: 0
- real model/voice inventory claims: 0
- human review: 0
- voice/pronunciation locks: 0
- story mutations: 0

## Next external action after merge
1. configure repository secret `ELEVENLABS_API_KEY` outside chat/Git/Drive;
2. manually run `ElevenLabs Provider Snapshot Evidence`;
3. require workflow SUCCESS;
4. read back `elevenlabs-provider-auth-evidence-*`;
5. verify AUTH_PROVIDER PASS and freshness <= 6h;
6. then execute bound model/voice inventory and casting evidence work.
