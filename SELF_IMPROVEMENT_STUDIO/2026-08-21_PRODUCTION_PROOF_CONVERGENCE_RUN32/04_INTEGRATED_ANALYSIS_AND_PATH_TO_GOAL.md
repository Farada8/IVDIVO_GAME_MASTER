# INTEGRATED ANALYSIS + PATH TO GOAL v1.0

## What changed in the problem
The bottleneck is no longer “we lack enough engines.” Parallel development has produced many capable components. The new failure mode is **proof debt**: a result may exist, but different routers/mirrors can lag, evidence classes can be conflated, and candidate mechanisms can survive indefinitely without measured value.

## Evidence from this run
1. D10 gives a positive control: explicit Founder decision + Final Story Gate + persisted lock artifact -> proof PASS; semantic mirrors and routing write-through converge.
2. D01 gives a negative control: internal Final Story Gate PASS is not enough for Founder Lock -> proof HOLD.
3. D01 also exposes routing drift: project-specific/current portfolio overlay is E01–E120, while the aggregate current system state still contains E96→E97. Higher-precedence overlay prevents correct routing, but the stale aggregate is real technical debt.
4. Local deterministic tests show the four candidate modules fail closed on common integrity attacks.
5. Value scoring without measurements is itself a risk. `HOLD_FOR_MEASUREMENT` is therefore a first-class disposition.

## Severity
- FATAL: 0.
- Story MAJOR caused by this work: 0.
- System MAJOR: stale D01 aggregate frontier in `CURRENT_IVDIVO_SYSTEM_STATE.json`; mitigated by project state + `CURRENT_IVDIVO_PORTFOLIO_FRONTIER_DELTA_2026-08-21.json` v1.3.
- External blockers remain domain-specific: Human Signal, live provider/audio, market evidence.

## Engineering direction
### Keep
- SI-0012 orchestration/transaction primitives.
- Session Resilience.
- P53 evidence/gate contracts.
- Wave6 Audio post-render hardening.
- PMV multilingual provider/casting frontier.

### Add as bounded candidates
- proof chain;
- semantic/exact mirror integrity;
- routing write-through auditor;
- measurement-completeness-aware value/pruning guard.

### Prune / forbid
- new global OS without a demonstrated missing invariant;
- duplicate prompt packs for domains with active backlogs;
- automatic prompt multiplication;
- “PASS” from file existence, model agreement, or timestamps alone;
- value claims from unmeasured zero/default telemetry.

## Path toward the goal
**Phase 1 — Convergence:** make persisted authorities/mirrors agree and expose stale layers.  
**Phase 2 — Proof:** every important terminal verdict gains an explicit proof chain.  
**Phase 3 — Real pilots:** apply to D01/D10/D04/ROOM917 without changing their story authority.  
**Phase 4 — Measurement:** collect real false-positive/repair/time/provider/human telemetry through existing SI-0012 telemetry bus.  
**Phase 5 — Pruning:** retire mechanisms that create cost/noise without measurable gain.  
**Phase 6 — Packaging:** only after current post-v11.2 extensions pass integrated regression, build a genuinely new engine package; never relabel v11.2 bytes.

## Immediate portfolio truth
- D10 BLOODBOUND: Founder-locked. Do not reopen.
- D01 THE WIFE AT HIS WEDDING: E01–E120 complete, Final Story Gate PASS, **awaiting Founder explicit lock decision**. Do not self-lock or generate E121.
- D09: separate Founder lock decision remains pending.
- SMITH Book 3: do not start as active text frontier until D01 Founder decision closes per current portfolio routing.

## Promotion decision for this run
The four modules remain **CANDIDATE**. Local tests and two real-data proof applications establish technical usefulness, not production net value. Promotion needs integrated CI/readback plus measured pilot telemetry; human/provider evidence is needed only when the promoted claim depends on those classes.

## Contract-conformance lesson from persistence
Publishing the candidate exposed two schema/runtime mismatches in Routing Consistency. Both were repaired before PR: `SYSTEM_AGGREGATE` is a valid role, and aggregate event-tracking records need not carry `observed_status` when they only carry `normalized_event`. This reinforces a new engineering rule: **schema syntax PASS is insufficient; validate schemas against at least one real production payload for every modeled role/path.**
