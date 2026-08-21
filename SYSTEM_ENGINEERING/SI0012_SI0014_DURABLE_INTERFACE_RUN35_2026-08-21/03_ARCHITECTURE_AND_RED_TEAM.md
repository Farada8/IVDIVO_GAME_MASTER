# RUN35 — ARCHITECTURE + RED TEAM

## 1. Problem
IVDIVO already has two useful transaction surfaces:
- SI-0012: compact single-store stale-hash/write/readback semantics inside orchestration;
- SI-0014: multi-store reconciliation, ambiguous external-side-effect quarantine, checkpoint lineage and interruption learning.

Building a third runtime would create ownership ambiguity. The correct move is an adapter interface.

## 2. Architecture

`PROJECT/DOMAIN AUTHORITY`
→ `SI-0012 ROUTING / TASK IR / GUARDS`
→ `DURABLE TRANSACTION INTERFACE v1`
→ either:
  - `SI-0012 LEGACY SINGLE-STORE ADAPTER`, or
  - `SI-0014 MULTI-STORE RECONCILER`
→ `READBACK`
→ `INTERRUPTION EVIDENCE QUALIFIER`
→ `SI-0014 ADVISORY LEARNING SUMMARY`
→ `PROMOTION REVIEW GATE` only when evidence threshold is met.

Paid/provider actions additionally require their own domain authorization gate. Recovery state never substitutes for provider authorization.

## 3. Common vocabulary
- STOP
- REBASE_FIRST
- QUARANTINE_EXTERNAL_SIDE_EFFECT
- VERIFY_STORE_BEFORE_RETRY
- VERIFY_READBACK
- REQUIRE_EXPLICIT_DISPATCH_GATE
- EXECUTE_MISSING_SAFE_ACTIONS
- TRANSACTION_COMPLETE

The facade maps legacy SI-0012 decisions into this vocabulary and delegates SI-0014 decisions without reimplementing the planner.

## 4. Genuine interruption qualification
Raw telemetry is not allowed to self-certify `real_interruption`.

Required proof dimensions:
1. not controlled;
2. not synthetic;
3. unplanned;
4. recognized unplanned origin;
5. restart observed;
6. pre-interruption checkpoint exists;
7. post-restart authority readback PASS;
8. recovery readback PASS;
9. project state before identified;
10. project state after identified;
11. multiple durable evidence refs supplied.

Classification:
- QUALIFIED_REAL_PACKET
- EXCLUDED_CONTROLLED
- EXCLUDED_SYNTHETIC
- UNVERIFIED_REAL_CLAIM

Only QUALIFIED_REAL_PACKET becomes `real_interruption=true` before the existing learning summarizer.

## 5. Parallel development reconciliation
Cycle6 is MERGED_CURRENT and explicitly requests SI-0012↔SI-0014 convergence at the transaction interface.
Open audio work uses independent provider gates and is compatible.
Open B03 PR #130 is project/story engineering and must not own SI-0014 identity.

## 6. FATAL found in PR #130
### Defect
B03 branch created `SI-0014_PROJECT_SLICE_FRESHNESS_ASSERTION.json` because its branch registry family was stale and omitted current SI-0014 Session Resilience.

### Severity
FATAL integrity defect: one candidate ID mapped to two independent mechanisms.

### Repair
- fresh main registry read;
- open-PR reservation search;
- SI-0015 proven unallocated at repair time;
- Project-slice Freshness migrated to SI-0015;
- live SI-0014 preserved;
- colliding file deleted;
- historical SI-0008 redirect corrected;
- PR body corrected;
- registry-family law expanded to include open-PR reservations.

### Learning
Candidate-ID allocation is itself a durability/freshness transaction. Branch-local “next free ID” is never authority.

## 7. Red Team
### FATAL
- duplicate registry identity: FOUND in PR130, REPAIRED BEFORE MERGE.
- facade silently replaces SI-0012 or SI-0014 runtime: NOT PRESENT by design.
- controlled/synthetic event satisfies real evidence threshold: regression coverage added.

### MAJOR
- raw `real_interruption=true` self-certifies a genuine event: existing vulnerability; PATCHED by qualification layer.
- source refs are merely strings: still a limitation. Qualifier explicitly does not claim existence/authentication; future verifier adapter required.
- provider authorization conflated with replay safety: prohibited by contract.
- breaking old SI-0012 transaction callers: avoided by additive adapter; parity regression added.

### MEDIUM
- qualification packet may be verbose: measure overhead on real events before promotion.
- multiple allowed origin labels could drift: centralize/version after first genuine events.
- two models may classify narrative incident descriptions differently: future bounded parity trial needed.

### POLISH
- add CLI/report rendering only after evidence pipeline proves useful; no extra UI now.

## 8. Acceptance path
1. new 17-test convergence suite PASS;
2. inherited Run32/Run33 session regressions PASS;
3. registry transaction regressions PASS;
4. Self-Improvement integrity PASS;
5. Drive mirror + content readback PASS;
6. latest-main semantic delta check;
7. no overlapping shared-state overwrite;
8. merge only if fresh and green.

## 9. Promotion boundary
Run35 can establish interface engineering evidence. It cannot fabricate the three genuine SI-0014 recoveries. Meeting the future threshold remains advisory review eligibility, never automatic promotion.
