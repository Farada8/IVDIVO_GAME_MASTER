# AMSI-93 — EXTERNAL MATHEMATICAL REVIEWER PACKET

Status: **READY_FOR_REVIEW / NOT YET EXTERNALLY REVIEWED**

## Reviewer question

Is there a mathematically nontrivial contribution beyond established abstraction, predictive-state, causal-abstraction, model-reduction and resource-complexity theories?

## Review order

1. `FORMAL_CORE_v7_MINIMAL.md`
2. `RUN3_MASTER_REPORT.md`
3. prior-art/novelty evidence in the full Drive package
4. Run2 proof pack in the full Drive package
5. `formal/AbsoluteMathTargets.lean`
6. `RESULTS_AMSI65_96.md`
7. source/tests/contracts in the full Drive ZIP
8. Red Team / release gate in the full Drive package

## Questions for reviewer

### Mathematical
- Are P1–P11 correct under their stated assumptions?
- Is any theorem nontrivial and not already standard?
- Is `d*(K, epsilon, A, M)` merely convenient optimization notation or does a useful new theorem class arise?
- Does recursive-state gating add genuine mathematical content beyond PSR/causal-state sufficiency?
- Does Construction Spectrum add anything beyond ordinary multi-objective/resource complexity?

### Prior art
- Is there an existing framework already combining causal abstraction, predictive state, resource constraints and proof certificates?
- Do projected causal abstraction or categorical causal abstraction subsume the proposed semantic/intervention layer?
- Do abstraction-carrying/certifying formal methods subsume Promotion Certificate methodology?

### Engineering/scientific
- Is the cross-domain benchmark protocol useful despite component non-novelty?
- Which additional negative controls are needed?
- What result would justify publication as a method/protocol rather than internal tooling?

## Evidence boundaries

Reviewer must not infer:
- physical universality;
- market utility;
- novelty from terminology;
- formal verification from uncompiled Lean targets;
- real self-improvement from synthetic archive simulation.
