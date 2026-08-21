# IVDIVO AUDIO NOVEL ENGINE — FRESH-MAIN RECONCILIATION v2

**Date:** 2026-08-21  
**Status:** FRESH-MAIN REBASE DECISION / PORT ONLY GENUINE GAPS  
**Compared against main head at rebase:** `1e263e22bebd34722d69d32e92a9787dee7a2a3c`

## 1. Why v2 exists

The first Wave4 integration branch was created before a fast sequence of sibling-dialog commits landed on `main`. A fresh compare showed the old branch had diverged heavily. This v2 therefore re-reads the new audio/provider evidence and decides what may be ported to a branch created from current `main`.

No force-overwrite, no wholesale merge of the research branch, and no story/canon mutation are allowed.

## 2. New main evidence inspected

### Current Audio Studio router
`audio/studio/00_IVDIVO_AUDIO_STUDIO_INDEX_v3.3.md` remains the universal router. It explicitly places current provider adapter/preflight/alignment/stereo-QC programs below story authority and keeps the pipeline: provider dry run → preflight → pilot → production → locks → alignment → mix/master/QC → human listen.

### PMV112 runtime authority
Commit `f991bf0183c68282637f4db6d4c30d2aad529719` added `P53_AUTO_CONTROL/31_CURRENT_RUNTIME_AUTHORITY_INDEX_v1_4_PMV112.md` as CURRENT for the multilingual/P53 lab. It records PMV01–112 as executed-through-available-evidence and preserves hard HOLD gates for native/audio/provider/listener evidence.

Portable rule inherited: Text-to-Dialogue is candidate/experimental, not automatic authority; isolated TTS remains required where clue, post-chain, pronunciation, performance protection or selective regeneration matters.

### ElevenLabs provider discovery
Commit `f6008567bee16ea5c78c1bc9bba1ca46a9e0c413` added a BODYGUARD-specific public-contract discovery report. It confirms that public documentation cannot prove authenticated account access and requires secret-free authenticated preflight before paid generation. It does **not** provide an authenticated inventory and does not close the Lesson Zero casting gate.

### “Adapter v2” commit correctly classified
Commit `7a1c3b13493228d2627f78367bb6f96bac4031e0` did **not** replace `audio/studio/elevenlabs_adapter.py`. It added the BODYGUARD-specific metadata artifact `P53_AUTO_CONTROL/MULTILINGUAL_VOICE_LAB_PMV81_176/PRODUCTION/BODYGUARD_ELEVENLABS_ADAPTER_v2_0.json` describing discovered endpoints/render-mode policy.

Fresh readback of current `audio/studio/elevenlabs_adapter.py` still shows the existing provider primitive that compiles/dispatches TTD/TTS and persists audio/alignment evidence. It has no persistent spend/idempotency ledger or ambiguous-response reconciliation state.

## 3. Reconciliation decision matrix

| Mechanism | Fresh main finding | Decision |
|---|---|---|
| provider preflight | already current | REUSE_CURRENT |
| ElevenLabs compile/dispatch/persist | already current provider primitive | REUSE_CURRENT |
| alignment normalization | already current single authority | REUSE_CURRENT / NO DUPLICATE |
| performance compiler | already current | REUSE_CURRENT |
| microphone choreography | current v3.3 authority exists | REUSE_CURRENT; small validation helpers may not supersede it |
| TTD-vs-isolated policy | PMV112/Bodyguard now contains stronger current rule | INHERIT RULE; do not create competing provider policy |
| exact canary identity before spend | no generic production gate found | PORT |
| persistent paid-request/idempotency ledger | no equivalent current runtime found | PORT |
| ambiguous POST-response quarantine/reconciliation | no equivalent current runtime found | PORT |
| capability drift with no auto-substitution | preflight exists, expected-vs-snapshot dispatch gate still missing | PORT AROUND CURRENT PREFLIGHT |
| canonical 48 kHz WAV/PCM ingest + technical/hash passport | no equivalent current runtime gate found | PORT |
| provider error normalization | current adapter labels are local/coarse | PORT AS CROSS-MODULE CONTROL; keep provider primitive unchanged |
| performance evidence lock | no equivalent generic fail-closed lock found | PORT; machine cannot auto-lock |
| dry freeze/resume/scoped invalidation CLI | no equivalent exact control CLI found | PORT |
| earliest-cause audio repair router | universal Patch Contract exists; audio specialization missing | PORT SUBORDINATE TO PATCH AUTHORITY |
| project-specific Lesson Zero facts | must not enter universal runtime | DATA FIXTURE ONLY |
| provider mock | tests already have mocking | TEST ONLY / DO NOT PORT AS RUNTIME PROVIDER |

## 4. Files approved for fresh-main port

### Runtime/control
- `audio/studio/runtime/production_control.py`
- `audio/studio/runtime/production_control_cli.py`
- `audio/studio/runtime/provider_reconciliation.py`
- `audio/studio/runtime/audio_asset_ingest.py`
- `audio/studio/runtime/audio_repair_router.py`
- `audio/studio/controlled_provider_dispatch.py`

These wrap/reuse current provider, alignment, performance and choreography authorities. They do not replace them.

### Regression tests
- `audio/studio/tests/test_production_control.py`
- `audio/studio/tests/test_provider_reconciliation.py`
- `audio/studio/tests/test_provider_error_taxonomy_fixtures.py`
- `audio/studio/tests/test_audio_asset_ingest.py`
- `audio/studio/tests/test_audio_repair_router.py`
- `audio/studio/tests/test_controlled_provider_dispatch.py`

### Evidence/data
Wave4 reports, Drive pointers, Lesson Zero exact-identity/dependency/pronunciation fixtures and Scene2 sound-space dry contract may be ported as WORKING evidence. They are not universal canon.

## 5. Explicit non-port / protection decisions

- Do not copy Wave3 mock provider into production runtime.
- Do not create a second alignment normalizer.
- Do not replace `provider_preflight.py`, `elevenlabs_adapter.py`, `performance_compiler.py`, the v3.3 Audio Studio router or PMV112 authority.
- Do not promote BODYGUARD provider metadata into a universal authenticated capability claim.
- Do not treat public provider discovery as authenticated inventory.
- Do not change Lesson Zero story/adaptation text.
- Do not mark Narrator/Ethan/Aoife or `Ифа`/`Контакт` locked.
- Do not claim real Lesson Zero WAV/alignment, human listening or measured economics.

## 6. CI law for rebased branch

The existing Audio Studio workflow discovers the full test directory but its trigger coverage is too narrow for all top-level `audio/studio/*.py` integration changes and does not expose a `pull_request` trigger for connector readback.

The rebased branch may therefore update only the workflow trigger surface so that:
- `audio/studio/runtime/**`
- `audio/studio/*.py`
- `audio/studio/tests/**`
- the workflow itself
trigger CI on both `push` and `pull_request`.

The test commands remain the existing full Audio Studio unittest discovery. No test PASS may be claimed until GitHub Actions readback is obtained.

## 7. Current decision

**PORT_TO_FRESH_MAIN_BRANCH — YES, BOUNDED.**

Reason: new PMV112/provider-discovery commits add useful provider policy/evidence but do not duplicate the cross-cutting production controls built in Wave4. The correct integration is convergence around current primitives, not another adapter or another Audio Studio OS.

Next internal gate after port: GitHub Actions CI/readback → fix only demonstrated failures → independent diff review → merge/hold decision.

Next external gate remains: authenticated secret-free provider inventory → Narrator/Ethan/Aoife candidates → in-context `Ифа`/`Контакт` auditions → pair/multi-state gate → exactly three Lesson Zero live canary requests → durable WAV+alignment provenance.
