# IVDIVO — TRANSCRIPT RECOVERY SPRINT 2 — 32 PROMPTS

**Status:** EXECUTED SEQUENTIALLY after freshness/rebase.  
**Date:** 2026-08-21  
**Rule:** each may return ACCEPT / EXTEND / ALREADY_IMPLEMENTED / HOLD_FOR_REAL_EVIDENCE / REJECT. Evidence-backed NO-OP is valid.

## N01 — Reconciled Recovery State v2 Rebase
Rebase existing SI-0009 state model against current main, PR #67, registry-family work and sibling self-improvement deltas. Determine extend/replace/no-op; do not create a parallel authority.

## N02 — Authority Taxonomy Hardening
Define finite authority classes for recovered direct Founder directives, project canon, domain authority, state pointers, candidates, external findings and model claims. Specify illegal promotions.

## N03 — Verification State Machine
Define lifecycle for persistence/lock/PASS/render/human/market claims from UNCHECKED to terminal evidence-backed dispositions; require evidence refs where needed.

## N04 — Multi-Project Partitioning
Design partitioning for transcripts containing several books, audio projects, system work and research. Prevent cross-project leakage while allowing explicit universalization.

## N05 — Conflict Graph + Resolution
Model contradicts/supersedes/duplicates/depends_on relations and deterministic resolution using authority, chronology/currentness and Founder choice.

## N06 — Unknown Contract
Define explicit unknown types and what each blocks. Separate unavailable evidence, missing exact detail, incomplete transcript, unresolved chronology and project identity.

## N07 — INGESTION_COMPLETE Contract
Red-Team legal conditions for RECOVERY COMPLETE and auto-continuation. Prove completion cannot bypass Founder/human/provider gates.

## N08 — v1→v2 Migration Contract
Specify how immutable Recovery Ledger v1 feeds Reconciled Recovery State v2 without mutating source evidence or losing hash/turn lineage.

## N09 — Claim→Evidence Registry
Create claim-type/evidence-class matrix for SAVED/CREATED/UPDATED, LOCK, PASS, MERGED, RENDERED, HUMAN APPROVED, MARKET VALIDATED and CURRENT AUTHORITY.

## N10 — Founder Lock Evidence
Define exactly what proves Founder approval/lock and what does not. Separate READY_FOR_LOCK, RECOMMENDED_LOCK, APPROVED and LOCKED.

## N11 — Automated Test PASS Evidence
Define minimum reproducible proof for machine PASS: source/test identities, invocation/environment, counts, exit status and logs.

## N12 — Provider Execution Evidence
Define proof for real provider execution and asset identity. Separate dry-run/request compilation from provider output.

## N13 — Human Evidence Protocol
Define proof for reader/listener/editor evidence tied to exact stimulus/build; prohibit model review from being labeled Human Signal.

## N14 — Market Evidence Protocol
Define minimum provenance for retention/conversion/sales/platform behavior; prohibit forecasts, model estimates and anecdotes from becoming market evidence.

## N15 — Persistence Verification Adapter
Specify provider-neutral adapters for GitHub, Drive and other persisted stores: locator, expected identity, read action, currentness, result, evidence_ref.

## N16 — Supersession/Currentness Verifier
Define how to prove CURRENT vs merely existing, including current pointer, superseded-by, newer project gate and incompatible branch.

## N17 — Nested Role-Marker Parser Red Team
Test role labels inside code fences, quotes, embedded transcripts and examples so quoted Assistant/User lines do not become outer turns.

## N18 — Markdown/Code/JSON False-Role Fixtures
Expand adversarial fixtures across fenced code, indented code, blockquotes, JSON strings, YAML and Markdown examples.

## N19 — RU/UA Role + Directive Coverage
Test Russian/Ukrainian user/assistant/founder aliases and imperative/work-claim vocabulary without granting authority by keyword alone.

## N20 — Malformed/Partial Transcript Behavior
Define fail-closed behavior for missing role labels, truncation, duplicate turns, partial exports and unknown completeness.

## N21 — Fake Artifact Reference Fixtures
Test filenames/IDs/URLs in examples, code and quotes. Preserve possible references as UNVERIFIED without converting them into persistence proof.

## N22 — Large-Corpus Checkpoint/Resume
Design chunk identity, overlap validation, findings hashes, tail processing and source-hash invalidation for very large corpora.

## N23 — Interrupted Recovery Resume
Define restart after recovery ends mid-ingestion: reusable checkpoints and what must be revalidated.

## N24 — Property/Fuzz Invariant Suite
Specify invariants: no transcript self-promotion, no secret persistence, no completion with material unknown/conflict, no write success without readback.

## N25 — Recovery Write Transaction
Design journal with preconditions, content fingerprint, prior pointer, intended targets, result, readback, rollback and partial-write repair.

## N26 — Idempotent Chat-Only Persistence
Define stable idempotency key so rerunning the same recovery corpus cannot create duplicate candidates/artifacts.

## N27 — GitHub Stale-Write/Rebase
Formalize stale-SHA behavior: re-read/rebase/no-op/branch+PR; never force-overwrite by default.

## N28 — Google Drive Revision Control
Formalize revisionId/writeControl flow, conflict recovery, readback and safe append/update behavior for native Docs.

## N29 — Partial-Write Repair
Design recovery when some GitHub/Drive writes succeed and others fail; preserve sibling progress and repair only touched surfaces.

## N30 — Two-Chat Concurrency Simulation
Design deterministic simulation of two dialogs updating independent and overlapping state; prove no lost update and correct rebase.

## N31 — Atomic/Sharded Improvement Registry
Reconcile monolithic registry limitations with current registry-family extensions; choose canonical future transaction model without duplicate IDs.

## N32 — Registry Compaction Builder
Specify safe compaction of base+extensions into deterministic canonical JSON with input SHAs, unique-ID validation, output hash, rollback and readback.
