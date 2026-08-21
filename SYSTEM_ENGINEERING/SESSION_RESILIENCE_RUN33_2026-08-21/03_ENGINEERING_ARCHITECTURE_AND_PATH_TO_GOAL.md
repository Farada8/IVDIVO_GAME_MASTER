# RUN33 — ENGINEERING ARCHITECTURE + PATH TO GOAL

Date: 2026-08-21
Candidate: `SI-0014 — Session Resilience + Durable Recovery Stack`

## 1. Architecture layers

### Layer A — Authority / continuation
Existing Cross-Conversation Autopilot and project state answer:
`WHAT PROJECT/FRONTIER IS CURRENT?`

### Layer B — Volatile checkpoint (18C)
Answers:
`WHAT DID THIS SESSION BELIEVE WAS THE LAST VERIFIED FRONTIER AND NEXT ACTION?`

Outputs:
`RESUME_EXACT / REBASE_FIRST / RECOVER_VOLATILE_FIRST / STOP`.

### Layer C — Durable transaction reconciliation (18D)
Answers:
`FOR EACH INTERRUPTED SIDE EFFECT, WHAT CAN BE PROVED AND WHAT MAY SAFELY HAPPEN NEXT?`

It separates:
- intent;
- idempotency identity;
- effect risk;
- observed side-effect state;
- intended vs observed artifact identity;
- readback proof.

### Layer D — Asset/provider domain authorities
Existing systems own actual:
- Drive/GitHub/provider execution;
- asset bytes;
- paid credits;
- audio/image/text QC;
- take/voice/canon locks.

18D never substitutes for these layers.

### Layer E — Checkpoint lineage
Provides one auditable recovery head per work unit and prevents checkpoint explosion/ambiguous histories.

### Layer F — Self-Improvement evidence
Interruption learning summarizes real recovery outcomes and overhead, but can only recommend promotion review.

## 2. Core state machine

`BLOCKERS? -> STOP`

`AUTHORITY/STATE DRIFT? -> REBASE_FIRST`

`FAILED ACTION? -> STOP`

`CONFIRMED IDENTITY MISMATCH? -> STOP`

`STARTED_UNKNOWN + PAID/IRREVERSIBLE? -> QUARANTINE`

`STARTED_UNKNOWN + REVERSIBLE? -> VERIFY STORE`

`CONFIRMED WITHOUT READBACK? -> VERIFY READBACK`

`NOT_STARTED + PAID/IRREVERSIBLE? -> EXPLICIT DISPATCH GATE`

`ONLY SAFE NOT_STARTED? -> EXECUTE MISSING SAFE ACTIONS`

`ALL TERMINAL + VERIFIED? -> TRANSACTION COMPLETE`

## 3. Why idempotency is not enough
An idempotency key identifies intended repetition. It does not prove the previous request was accepted, the artifact is correct, the correct identity is bound, or the write was read back. Therefore:

`SAME KEY != SAFE RETRY`.

The key is a lookup/reconciliation handle.

## 4. Multi-store transaction example
Logical output should exist in GitHub and Drive.

If:
- GitHub = RECONCILED + readback + matching commit/blob identity;
- Drive = NOT_STARTED;

then only Drive is returned as `EXECUTE_MISSING_SAFE_ACTIONS`.

If Drive = STARTED_UNKNOWN, the answer changes to `VERIFY_STORE_BEFORE_RETRY`.

If the ambiguous action is a paid provider call, answer becomes `QUARANTINE_EXTERNAL_SIDE_EFFECT`.

## 5. Checkpoint lineage
Each active work unit has one current head.

`root(g0) -> child(g1) -> child(g2)`.

A historical real incident may be retained as `AUDIT_KEEP`. Ordinary old checkpoints become `GC_ELIGIBLE`.

Validation itself rejects:
- duplicate roots;
- multiple ACTIVE heads;
- duplicate checkpoint hashes;
- cross-work parents;
- cycles/generation mismatch.

## 6. Self-Improvement promotion logic
Synthetic tests can prove deterministic mechanics and expose safety regressions. They cannot satisfy real production evidence thresholds.

SI-0014 remains READY_FOR_PILOT until at least:
- 3 real interruption recoveries;
- 2 independent projects;
- zero false resume;
- acceptable false-stop rate measured on real incidents;
- GitHub/Drive durable readback;
- no unacceptable checkpoint overhead.

Even then output is `ELIGIBLE_FOR_PROMOTION_REVIEW`, not automatic promotion.

## 7. Registry-integrity lesson
Run33 discovered that candidate identity itself is a concurrency problem.

New law:
`FULL REGISTRY FAMILY READ -> PROVE ID UNUSED -> REGISTER`.

Partial visibility is never sufficient for a new SI number.

## 8. Red Team repairs
Run33 found and repaired:
1. **FATAL provenance:** Session Resilience incorrectly reused SI-0010 -> migrated to SI-0014.
2. **MAJOR transaction precedence:** FAILED could be bypassed by unstarted work -> FAILED moved earlier.
3. **MAJOR lineage:** pre-existing multiple roots/ACTIVE heads not rejected -> validator strengthened.
4. **MAJOR telemetry:** synthetic false-stop fixtures could distort promotion rate -> real-event denominator separated.
5. **CI infrastructure:** inherited pytest test invoked without pytest dependency -> workflow repaired.

## 9. What Run33 deliberately does not solve
- browser-session restoration itself;
- distributed two-phase commit across GitHub/Drive/providers;
- provider-specific idempotency contracts;
- network partition guarantees;
- automatic paid-action replay;
- automatic canon/project-state mutation;
- automatic Self-Improvement promotion.

Trying to solve those here would create unsafe scope inflation.

## 10. Path to goal

### Immediate integration
1. finish Run33 CI;
2. persist proof report;
3. mirror Run33 reports to Drive + readback;
4. fresh-read current main;
5. reconcile overlapping files;
6. rebase branch onto exact current main;
7. rerun Run33 + Self-Improvement CI;
8. full PR diff Red Team;
9. merge exact head only if green;
10. read back main and Drive.

### Pilot phase
11. instrument next genuine interrupted GitHub/Drive workflow;
12. record checkpoint and transaction identities;
13. verify only missing safe side is replayed;
14. log duplicate work avoided / reconciliation cost;
15. repeat across another independent project.

### Promotion phase
16. aggregate real evidence;
17. compare checkpoint cadence/overhead alternatives;
18. decide PROMOTION_REVIEW / NARROW / HOLD / ROLLBACK;
19. only after mature evidence, include in a future tested engine ZIP.

## Final engineering principle
**RECOVERY QUALITY IS NOT HOW MUCH STATE WE SAVE. IT IS HOW PRECISELY WE CAN PROVE WHAT MAY HAPPEN NEXT WITHOUT DUPLICATING OR CORRUPTING WORK.**
