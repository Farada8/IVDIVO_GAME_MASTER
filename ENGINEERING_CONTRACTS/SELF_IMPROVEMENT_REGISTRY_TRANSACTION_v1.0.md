# IVDIVO — SELF-IMPROVEMENT REGISTRY TRANSACTION CONTRACT v1.0

**Status:** ENGINEERING CANDIDATE / H01-H05 tranche  
**Date:** 2026-08-21  
**Authority scope:** Self-Improvement registry lifecycle only. Never story canon.

## 1. Problem
The registry family is intentionally split into a compatibility base plus extension shards. Concurrent whole-file rewrites of the monolithic base create lost-update and stale-write risk. A registry mutation therefore needs a transactional engineering boundary.

## 2. Current registry family
- Base/read model: `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json`
- Family pointer: `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY_FAMILY.json`
- Concurrent write surface: `31_IDEAS/REGISTRY_EXTENSIONS/*.json`
- Read-only family invariant: `tools/validate_improvement_registry_refs.py`
- Transaction tool candidate: `tools/ivdivo_registry_transaction.py`

## 3. Register-candidate contract
Input:
- exact candidate JSON;
- exact current registry-family pointer;
- optional expected family SHA for stale-base protection.

Required execution:
`READ FAMILY -> VERIFY EXPECTED SHA -> VALIDATE CANDIDATE -> COLLECT BASE+EXTENSIONS -> SEMANTIC DEDUPE -> LOCK -> SNAPSHOT -> WRITE SHARD ATOMICALLY -> UPDATE FAMILY POINTER ATOMICALLY -> READBACK -> COMMIT MANIFEST`

Failure path:
`ANY POST-SNAPSHOT FAILURE -> BYTE-PRESERVING RESTORE OF FAMILY + PREVIOUS SHARD STATE -> ROLLED_BACK_ON_ERROR`.

## 4. Hard invariants
1. `candidate_id` is unique across base and all extensions.
2. Existing same ID + same semantic record = `NOOP_EXISTING`.
3. Existing same ID + different semantic record = `DUPLICATE_ID_CONFLICT` and no write.
4. Unknown lifecycle state fails before write.
5. Missing provenance fails before write.
6. `VERIFIED_CURRENT` requires verification evidence and application targets.
7. `HOLD_WITH_TRIGGER` requires a hold trigger.
8. Terminal records require a reason.
9. An expected family SHA mismatch returns `STALE_BASE`; it is not force-overwritten.
10. Candidate registration never promotes story/project canon.

## 5. Transaction snapshot
Every mutating transaction creates a snapshot under:
`31_IDEAS/.registry_txn_snapshots/<txn_id>/`

Snapshot contains:
- exact pre-write family bytes;
- exact prior shard bytes when a shard existed;
- manifest with pre-write hashes and transaction identity.

A failed transaction must restore those bytes exactly. An explicit rollback uses the same snapshot.

## 6. Concurrency model
The tool uses an exclusive family lock for the short critical section. The lock is an engineering guard, not a distributed lease across arbitrary providers. GitHub repository writes still require the project-wide rule:
`FRESHNESS_SWEEP -> CURRENT HEAD -> BRANCH -> PR -> REBASE IF MAIN ADVANCES -> NO FORCE OVERWRITE`.

## 7. Deterministic compaction contract
Compaction is a build/read model, not a lifecycle promotion.

Required:
- load base + all extensions;
- fail on duplicate IDs;
- sort candidates deterministically by `candidate_id`;
- emit canonical JSON;
- emit manifest containing base hash, extension hashes, family hash, candidate count, output hash and readback status;
- re-open output and verify unique sorted IDs/count.

Compaction must never silently replace the current family pointer until a separate promotion transaction proves rollback/readback and current consumers are compatible.

## 8. Evidence classes
A passing unit/regression test is `MACHINE_TEST / INTERNAL_EVIDENCE`.
It can prove deterministic transaction behavior under the tested fixtures.
It cannot prove:
- literary quality;
- Founder approval;
- story lock;
- human signal;
- provider success;
- market performance;
- safe behavior under every real multi-writer GitHub race.

## 9. Promotion gate
SI-0010 may move from DEVELOPING to READY_FOR_PILOT after:
- transaction tool exists;
- deterministic regression fixtures pass;
- registry-family invariant passes;
- CI runs on repository checkout.

Promotion beyond candidate/pilot requires at least one real registry write operation on a non-canon improvement candidate, followed by GitHub/Drive readback and no lost update.

## 10. Rollback law
Rollback is a first-class result, not a failure to hide.
If the tool cannot prove a complete write, the correct state is the old bytes plus an explicit failed/rolled-back transaction record.

**Atomicity before convenience. Provenance before promotion. Registry state never outranks story authority.**
