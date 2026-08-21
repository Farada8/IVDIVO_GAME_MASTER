# SPRINT 3 — SYNTHESIS AND DECISIONS

**Status:** WORKING R&D EVIDENCE / NOT STORY CANON / NOT AUTOMATIC CURRENT ENGINE AUTHORITY.

## 1. What changed from Sprint 2
Sprint 2 established that the primary gap was semantic reconciliation rather than a larger first-pass extractor. Sprint 3 confirms that finding after fresh rebase and narrows the operational frontier further:

`VERIFIED v1 EXTRACTION -> SI-0009 SEMANTIC CANDIDATE -> CONNECTOR EVIDENCE ADAPTERS -> TRANSACTIONAL WRITE/READBACK -> REAL LARGE CORPUS PILOT -> NEXT-ACTION HANDOFF`.

The real bottleneck has moved from **mechanism invention** to **integration + real evidence + concurrency-safe persistence**.

## 2. Current recovery stack
### CURRENT / verified
- 18B Full Chat Transcript Recovery protocol.
- v1 deterministic extractor / ledger layer.
- Self-Improvement v2 authority and registry-family architecture.
- Base+extension registry family as the current concurrent visibility model.

### Candidate / not CURRENT
- SI-0009 Reconciled Recovery State v2 / completion gate (PR #67).
- SI-0010 registry shard compaction transaction.
- SI-0011 first real large corpus operational pilot.
- unified connector verification adapters.
- Sprint-3 operational contracts and adversarial fixture set.

### External/real evidence missing
- first genuine large exported/pasted prior AI transcript run through the complete recovery pipeline.

## 3. Red Team
### FATAL
0.

### MAJOR 1 — no real large-corpus production evidence
Synthetic fixtures and unit tests can harden contracts but cannot prove that real exported chats partition, reconcile and persist correctly. Promotion of semantic recovery remains blocked.

### MAJOR 2 — SI-0009 is still branch candidate
11/11 unit smoke proves the candidate gate against its fixtures, not current-main integration or production behavior. Do not relabel as VERIFIED_CURRENT before integration/adversarial/real-corpus evidence.

### MAJOR 3 — connector evidence verification is still a contract, not one executable cross-store adapter
GitHub and Drive evidence can be checked manually through available connectors, but a reusable machine adapter/harness joining those checks to recovery-state tasks is still pending.

### MAJOR 4 — prompt-cycle/WIP duplication is now a system risk
The repository contains several 32→64 cycles and sibling branches. Different domains justify parallel research, but repeated meta cycles can generate more mechanisms than the system can integrate, test, prune or package. Stale-base and duplicate-mechanism debt are visible operationally.

## 4. New laws accepted as WORKING design
1. **COMPLETE_AS_SUPPLIED != HISTORICALLY_COMPLETE_TRANSCRIPT.**
2. **TRANSCRIPT CLAIM != EVIDENCE.**
3. **PROJECT PARTITION BEFORE CANON/STATE DISPOSITION.**
4. **AUTHORITY RANK + SAME-RANK CHRONOLOGY, NOT TIMESTAMP ALONE.**
5. **API SUCCESS != PERSISTENCE COMPLETE; READBACK REQUIRED.**
6. **RERUN MUST BE IDEMPOTENT.**
7. **SOURCE MUTATION BREAKS SILENT CHECKPOINT RESUME.**
8. **REGISTRY COMPACTION MAY CHANGE STORAGE FORM, NEVER LIFECYCLE STATUS.**
9. **INGESTION_COMPLETE PERMITS HANDOFF; IT DOES NOT BYPASS THE NEXT REAL GATE.**
10. **ANOTHER 32→64 CYCLE REQUIRES A DEDUPE/INFORMATION-GAIN CHECK UNLESS FOUNDER DIRECTLY ORDERS IT; FOUNDER OVERRIDE CHANGES PRIORITY, NOT EVIDENCE CLASS.**

## 5. Why no new top-level recovery engine
The needed components fit as extensions/adapters around 18B + v1 + SI-0009 candidate. A parallel recovery engine would create:
- authority duplication;
- incompatible state schemas;
- migration debt;
- another package surface;
- harder cross-dialog reconciliation.

Decision: **EXTEND + INTEGRATE + TEST**, do not restart architecture.

## 6. Real pilot contract
The first real large transcript must produce one evidence bundle:
1. immutable source identity;
2. v1 extraction ledger;
3. source-unit/conversation partition;
4. project partitions;
5. direct Founder vs paraphrased directive separation;
6. persistence claim tasks;
7. actual Drive/GitHub verification;
8. chat-only candidate recovery;
9. unknown/conflict disposition;
10. transactional writes with idempotency keys;
11. readback/repair ledger;
12. reconstructed project frontier(s);
13. recovery-completion decision;
14. next-action resolver handoff;
15. defect/learning report.

PASS requires zero false authority promotion, zero secret persistence, no duplicate rerun effects, correct partitioning of all material items, and correct STOP/CONTINUE handoff.

## 7. Cycle-level self-improvement result
Repeated prompt multiplication should no longer be treated as progress by itself. A research cycle has value only if it does one or more of:
- consumes new real evidence;
- implements a previously designed mechanism;
- disproves/merges/prunes candidates;
- closes a production gate;
- exposes a new defect with a bounded fix/test.

If the next decisive dependency is external and the prompt queue mostly reformulates known mechanisms, default action is HOLD and wait for/seek the evidence rather than produce another abstract generation.

This does not override direct Founder instruction. It prevents the system from falsely claiming that an explicitly authorized design cycle also increased production evidence.

## 8. Promotion decisions
### ACCEPT as Sprint-3 candidate design
- completeness contract;
- source-unit + project partition contract;
- evidence-class contracts;
- unknown/conflict materiality contract;
- secret firewall;
- transaction/readback/idempotency/resume contracts;
- connector adapter interface;
- adversarial fixture catalog;
- recovery handoff contract;
- cycle dedupe + information-gain gate.

### HOLD
- SI-0009 promotion to CURRENT;
- SI-0010 compaction execution/promotion;
- SI-0012 operational pilot harness promotion;
- SI-0013 cycle-dedupe gate promotion;
- engine package refresh.

### REJECT / DO NOT DO
- new top-level recovery engine;
- another first-pass regex expansion without new parser failure evidence;
- treating PR count/model agreement as validation;
- treating synthetic fixtures as real corpus evidence;
- force-updating current state from a stale sibling branch.

## 9. Next action
The highest-information next action remains:

**FIRST REAL LARGE TRANSCRIPT END-TO-END PILOT**, using SI-0009 candidate semantics only in an explicitly candidate/test context until it passes its promotion gates.

In parallel, bounded work may implement and regression-test connector adapters, transactional persistence and adversarial fixtures. The 64 derived prompts are dependency-aware candidate work, not a mandate to run all 64 blindly.
