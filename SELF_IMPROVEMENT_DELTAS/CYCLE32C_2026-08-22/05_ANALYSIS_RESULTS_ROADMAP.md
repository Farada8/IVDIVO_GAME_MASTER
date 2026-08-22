# Cycle32C — Analysis, Results, Road to Improvement

## Result
The project does not need another generic self-improvement engine. It needs a tighter decision-control envelope around the current v2/P53/recovery/freshness stack.

### Existing strengths reused
- Self-Improvement v2 lifecycle/registry/Learning Ledger/evaluation matrix.
- P53 evidence-first autorun.
- transcript recovery.
- SI-0014 checkpoint/durable transaction recovery.
- SI-0015 project-slice freshness + typed approval-event semantics.
- selective regression and no broad reopening of locked work.
- Saga100 evidence bridge and unmerged SI-0016 scope-aware strategic-authority candidate.

### Proven/observed weaknesses
1. **Concurrent registry identity:** main may not see a candidate ID already allocated on an active branch/PR.
2. **Meta activity vs progress:** prompt/file counts can rise without changing a production decision.
3. **Freshness is vector-valued:** execution, strategy, registry, Drive, PR, project and approval frontiers can differ.
4. **Production return:** meta cycles need a hard return-to-product target.
5. **v3 evidence:** useful candidate mechanisms exist, but real prospective production promotion proof is incomplete.

## Selected repair
`DECISION_EVIDENCE_YIELD_CONTROL_PROFILE` as a local v2 extension pilot. It owns no canon, authority, registry lifecycle, checkpoint or recovery state.

## Evidence status
Supported/proven at engineering scope:
- new engine unnecessary;
- cross-branch SI-ID race exists;
- current profile changed live Cycle32C decisions;
- scope-dependent/multi-surface freshness is a real concern.

Not proven:
- universal cycle-time/cost improvement;
- literary/reader/listener quality improvement;
- market/provider improvement;
- universal superiority of v3.

## Red Team
- FATAL: 0.
- local-pilot blocking MAJOR: 0.
- global-promotion MAJOR: 2.
  - transactional cross-branch candidate reservation missing;
  - prospective heterogeneous cross-project evidence missing.

## Road to improvement
1. **Integrity:** build read-only registry collision canary across main + active registry PR heads.
2. **Prospective evidence:** run profile on one active-book continuation and one separate engineering task.
3. **Flow:** apply qualitative VOI/Cost-of-Delay only when it changes queue order.
4. **Double-loop:** recurring defect family triggers causal/model-boundary review, not another patch.
5. **Implementation:** encode deterministic subset only after pilot support; run current v2/SI-0014/SI-0015/P53 regressions.
6. **Promotion:** use existing v2 lifecycle and evidence-appropriate scope.
7. **Production return:** designed Next64 stays inactive until a concrete gap activates a group; default return is B03 P41-P48 corpus regression.

## Disposition
- New global engine: **REJECTED**.
- New SI candidate ID: **NOT ASSIGNED**.
- v3: **HOLD CANDIDATE**.
- v2: **REMAINS CURRENT**.
- Cycle32C profile: **HOLD LOCAL CANDIDATE**.
