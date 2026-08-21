# DETAILED RESULTS P233–P240

## P233 — CONTRACTIVE STOCHASTIC ERROR THEOREM

**STATUS:** DERIVED

### Strongest supported claim
Under contraction, repeated approximate stochastic aggregation errors are bounded by a geometric series rather than growing without limit.

### Evidence
The P193–P224 near-lumpable fixture had macro Dobrushin coefficient below 1 and projected-vs-macro TV error saturated near 0.0097 despite nonzero one-step defect.

### Limitations / Red Team
A full theorem must define precisely how the per-step defect enters the Markov-kernel comparison; constants depend on the chosen norm/coupling formulation.

### Decision
KEEP the theorem target: horizon bounds require contraction/mixing assumptions.

### Formal anchor
`e_t <= epsilon * sum_{j=0}^{t-1} alpha^j when alpha<1`

## P234 — NONCONTRACTIVE ERROR COUNTEREXAMPLE

**STATUS:** COUNTEREXAMPLE

### Strongest supported claim
Arbitrarily small one-step stochastic defect does not imply useful long-horizon Promotion when contraction fails.

### Evidence
Fresh 2-state counterexample with one-step epsilon=0.01 grows TV error from 0.010 at t=1 to 0.993 at t=500; approximate kernel has Dobrushin coefficient 1.0.

### Limitations / Red Team
This is a constructed worst-case fixture, not typical mixing dynamics.

### Decision
Permanently reject horizon-free epsilon-Promotion claims.

## P235 — METRIC INVARIANCE BENCHMARK

**STATUS:** DERIVED

### Strongest supported claim
Closure metrics have different invariance classes; raw RMSE is not unit-invariant, while variance-normalized RMSE is invariant to simple scalar rescaling in the tested fixture.

### Evidence
P193–P224 rescaling changed raw RMSE by 1000× while NRMSE stayed constant. TV is natural for discrete probability laws; Wasserstein depends on a state-space metric; KL/JS depend on distributions/support rather than physical units.

### Limitations / Red Team
No single metric is universally appropriate.

### Decision
Every defect must declare its metric, normalization and invariance target.

## P236 — APPROXIMATE BISIMULATION CROSSWALK

**STATUS:** KNOWN

### Strongest supported claim
Approximate Promotion in stochastic transition systems substantially overlaps approximate probabilistic bisimulation, bisimulation metrics and near/quasi-lumpability.

### Evidence
Published work develops exact lumpability and approximate behavioral metrics/bounds for probabilistic systems.

### Limitations / Red Team
The project may still combine these with history/micro sufficiency and hierarchy/generativity modules.

### Decision
MERGE approximate stochastic closure with established terminology before any novelty claim.

## P237 — RESIDUAL HISTORY CMI

**STATUS:** DERIVED

### Strongest supported claim
Conditional mutual information is a stronger nonlinear diagnostic of missing history than residual autocorrelation alone in discrete controls.

### Evidence
Fresh second-order process: I(next; lag2 | current)≈0.3021 bits, while after conditioning on the sufficient two-step state the deeper-history CMI falls to 2.11e-05 bits.

### Limitations / Red Team
Finite-sample CMI is biased and high-dimensional estimation is difficult; significance calibration is mandatory.

### Decision
Add calibrated CMI/history-gain as a semantic sufficiency gate.

## P238 — RESIDUAL MICRO CMI

**STATUS:** DERIVED

### Strongest supported claim
Conditional micro-information cleanly distinguishes an insufficient coarse state from a sufficient augmented state in a planted control.

### Evidence
With hidden micro bit omitted, I(Future;Micro|Macro)≈0.7144 bits; after the relevant micro bit is included, an irrelevant extra micro feature gives only 1.09e-05 bits.

### Limitations / Red Team
Real continuous high-dimensional systems require careful estimators and capacity controls.

### Decision
Keep micro-gain/CMI as a hard autonomy test.

## P239 — RECURSIVE FILTER STATE

**STATUS:** KNOWN

### Strongest supported claim
Belief state is an exact recursively updateable sufficient state for a known POMDP/HMM model, providing a canonical positive control for recursive state.

### Evidence
Fresh two-state HMM filter recomputed from full history and updated recursively had maximum numerical discrepancy 0.0.

### Limitations / Red Team
Belief state dimension and identifiability rely on a model; learned PSRs can avoid explicit latent-state semantics.

### Decision
Add belief-filter and controlled-PSR fixtures to the benchmark registry.

## P240 — DYNAMIC CLOSURE GRAND RED TEAM

**STATUS:** DERIVED

### Strongest supported claim
The Dynamic Closure module can be reduced to five mandatory elements: behavioral defect metric, horizon/stability, history sufficiency, micro sufficiency, and recursive updateability.

### Evidence
P233–P239 show independent failure modes: noncontractive accumulation, unit-dependent metrics, missing history, missing micro information, and nonrecursive/offline summaries.

### Limitations / Red Team
Nonstationary/adaptive systems may require an explicit time/regime variable as part of state.

### Decision
Formal Core should use this minimal closure protocol rather than a larger unstructured checklist.
