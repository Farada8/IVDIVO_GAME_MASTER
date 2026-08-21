# RUN35 — PARALLEL DEDUPE + FATAL REPAIR

## Fresh main at Run35 branch creation
`0a3fcaa37b7774382013230e5eacc26b61e175c1` — Self-Improvement Cycle6 integration.

## Merged/current relevant mechanisms
### SI-0012
Prompt Router / Meta-Orchestrator compatibility runtime. Owns state normalization, authority-vs-working-frontier routing, Prompt IR, guards, compact single-store transaction/readback semantics and routing telemetry.

### SI-0014
Session Resilience + Durable Recovery. Owns checkpoint resume/rebase/recovery, multi-store reconciliation, ambiguous external-side-effect quarantine, checkpoint lineage and interruption-learning advisory metrics.

### Audio provider snapshot hardening
Owns authenticated/fresh provider capability evidence before paid audio dispatch. It is a domain authorization layer, not a transaction-recovery replacement.

### Cycle6
Merged evidence-convergence review explicitly recommends SI-0012 + SI-0014 convergence at a versioned transaction interface and warns against a second durable-write runtime.

## Open parallel work reviewed
- PR #130 B03 Smith Cycle32 / project routing.
- PR #129 Absolute Mathematics Run3 — isolated/draft research.
- PR #126 Audio Novel Engine Wave8 v2 — documentation/state reconciliation, external provider gate remains.
- PR #125 MF-C03 book-domain QA disposition.
- PR #119 Production proof-chain candidates.
- PR #118 NMM project-specific audio integration.

Run35 does not import their draft mechanisms as CURRENT authority.

## FATAL: PR #130 registry identity collision
### Discovery
PR #130 branch registry family was cut from a stale view that stopped at SI-0013. It therefore created a new `SI-0014_PROJECT_SLICE_FRESHNESS_ASSERTION.json`.

Current main already owns:
`SI-0014 = Session Resilience + Durable Recovery Stack`.

This is not a naming nit. A cold-start agent could resolve the same candidate ID to two unrelated mechanisms.

### Repair performed on PR #130 branch
1. Fresh main registry-family read confirmed SI-0014 ownership.
2. Open-PR search for `SI-0015` found no reservation.
3. Cycle6 evidence confirmed SI-0015 had only been computed as next-unreserved, not allocated.
4. Created `SI-0015_PROJECT_SLICE_FRESHNESS_ASSERTION.json`.
5. Updated historical SI-0008 collision redirect to point to SI-0015 and protect SI-0014.
6. Rebuilt branch registry-family pointer from fresh main + SI-0015 delta.
7. Extended candidate-ID freshness law: base registry + all extension shards + open-PR reservations.
8. Deleted colliding SI-0014 project-slice file.
9. Updated PR #130 body so metadata no longer teaches the stale identity.

### Current PR #130 story boundary
The registry repair does not authorize B03 manuscript prose or resolve its Founder family-continuity decision gate.

## Dedupe result for Run35
Decision: `MERGE_AT_INTERFACE / KEEP_EXISTING_RUNTIMES`.

Do not:
- create SI-0016 just for the interface;
- create a second transaction writer;
- copy SI-0014 planner logic into SI-0012;
- make interruption telemetry a new authority.

Do:
- add a versioned compatibility facade;
- map SI-0012 legacy transaction results into shared vocabulary;
- delegate SI-0014 multi-store decisions;
- add evidence qualification before interruption-learning metrics;
- keep promotion advisory-only.
