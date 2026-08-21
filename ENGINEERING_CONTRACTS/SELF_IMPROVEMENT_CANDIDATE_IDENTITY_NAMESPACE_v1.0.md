# SELF-IMPROVEMENT CANDIDATE IDENTITY + NAMESPACE CONTRACT v1.0

**Status:** ENGINEERING CONTRACT / CANDIDATE ENFORCEMENT  
**Date:** 2026-08-21  
**Authority boundary:** identity/routing only; never story canon or Founder authority.

## Problem

`SI-xxxx` is a global identity, not a filename-local label. Parallel dialogs created distinct mechanisms under the same IDs because assignment used partial visibility. A validator that reads only base + `REGISTRY_EXTENSIONS` can remain green while `PENDING` contains a semantic collision.

Observed production defects:
- canonical `SI-0009` = Reconciled Recovery State v2;
- pending `SI-0009` = audio post-render repair compiler;
- canonical `SI-0010` = registry shard/compaction transaction;
- pending `SI-0010` = volatile session checkpoint.

## Required discovery surface

Before assigning or promoting any `SI-xxxx`, scanner MUST inspect:
1. `31_IDEAS/CURRENT_IMPROVEMENT_REGISTRY.json`;
2. every JSON shard under `31_IDEAS/REGISTRY_EXTENSIONS/`;
3. every active candidate JSON under `31_IDEAS/PENDING/`;
4. configured reservation/migration-debt records;
5. any future candidate-bearing root added to the identity-root manifest.

Partial visibility is `DISCOVERY_ONLY` and cannot allocate a global ID.

## Identity states

- `UNIQUE` — one active semantic candidate owns the ID.
- `DUPLICATE_SAME_MECHANISM` — identical semantic fingerprint exists in multiple active records; cleanup required.
- `ID_COLLISION_DIFFERENT_MECHANISM` — same ID, different semantic fingerprints; FATAL for promotion/compaction.
- `TRACKED_MIGRATION_DEBT` — exact known collision is bound to source paths and repair locator; dependency-independent work may continue, but promotion is blocked.
- `REDIRECT` — historical ID migration marker; not an active candidate.
- `DANGLING_REDIRECT` — redirect target absent; FAIL.

## Semantic fingerprint

The default identity fingerprint is SHA-256 of canonical JSON over:
`title + candidate_type + scope + problem_or_opportunity + proposed_mechanism + dedupe_relation`.

Status, timestamps and evidence additions do not create a new semantic candidate by themselves.

## Allocation law

`DISCOVER ALL ROOTS -> VALIDATE -> GROUP BY ID -> CLASSIFY -> RESOLVE/TRACK DEBT -> COMPUTE NEXT FREE -> RESERVE/WRITE -> READBACK -> RE-AUDIT`.

Never choose “next number” from memory, recent PRs, or one directory.

## Migration law

For true collision:
1. preserve the already-established canonical owner unless newer authority explicitly says otherwise;
2. assign a globally free ID to the displaced mechanism;
3. write the migrated candidate with preserved evidence and an explicit identity-migration provenance entry;
4. replace the old pending record with `CANDIDATE_ID_REDIRECT` or another durable tombstone;
5. update registry-family/index surfaces transactionally when concurrency permits;
6. read back and re-run global identity audit.

Migration changes identity only. It MUST NOT increase scope, status or evidence class.

## Tracked-debt law

A known parallel repair may be tracked only when:
- candidate ID is exact;
- expected colliding source paths are exact;
- a concrete repair locator exists;
- promotion/current mutation is blocked;
- any change in the colliding source set converts the result to FAIL.

Tracked debt is never clean PASS evidence.

## Acceptance

A production-ready namespace gate requires:
- true-collision negative fixture;
- same-mechanism duplicate fixture;
- redirect fixture;
- dangling redirect fixture;
- tracked-debt exact-match fixture;
- new/untracked collision fixture;
- next-free reservation fixture;
- real repository audit;
- GitHub readback;
- no semantic loss in migrated candidates.

## Current repair routing

- Keep canonical `SI-0009` Recovery State v2.
- Migrate audio post-render candidate to `SI-0015`.
- PR #108 owns the pending `SI-0010` -> `SI-0014` Session Resilience migration; do not duplicate its implementation.
- Freshness/authority-chain and evidence-class candidates receive IDs only after the global audit confirms availability.
