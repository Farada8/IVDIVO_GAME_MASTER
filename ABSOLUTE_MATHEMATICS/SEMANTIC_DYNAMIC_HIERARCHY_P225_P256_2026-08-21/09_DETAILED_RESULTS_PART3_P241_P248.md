# DETAILED RESULTS P241–P248

## P241 — HANKEL RANK RECOVERY SUITE

**STATUS:** DERIVED

### Strongest supported claim
Finite Hankel rank is recoverable exactly in noiseless planted low-rank controls and is therefore a useful positive benchmark for predictive dimension.

### Evidence
Fresh suite recovered ranks [(1, 1), (2, 2), (3, 3), (4, 4)] for generic 1–4 state fixtures.

### Limitations / Red Team
Finite Hankel matrices can underestimate the rank of larger/infinite systems; noise makes thresholding nontrivial.

### Decision
Use rank recovery only with horizon/sample/noise stress and uncertainty.

## P242 — FALSE LOW-RANK FINITE DATA

**STATUS:** COUNTEREXAMPLE

### Strongest supported claim
Singular-value thresholding can falsely declare low predictive rank when real singular values are small relative to an arbitrary numerical/statistical threshold.

### Evidence
Fresh identity-like matrices had true rank N but amplitude 1/N²; for N=32, common thresholds above the amplitude return estimated rank 0 despite true rank 32.

### Limitations / Red Team
The constructed spectrum is adversarial; statistical sampling produces more complex distortions.

### Decision
Any finite-rank claim needs calibrated thresholding, sample scaling and growing-horizon tests.

## P243 — HIDDEN-STATE REDUNDANCY FAMILY

**STATUS:** DERIVED

### Strongest supported claim
Hidden-state count can grow arbitrarily while predictive rank stays fixed.

### Evidence
Fresh duplicated-HMM family: hidden states 2,4,8,16 all have finite Hankel rank 2.

### Limitations / Red Team
Predictive rank itself is not always equal to minimal discrete-state count.

### Decision
Permanently separate ontology/latent-component count from predictive-state complexity.

## P244 — MINIMAL REALIZATION CROSS-DOMAIN

**STATUS:** KNOWN

### Strongest supported claim
Minimality and uniqueness are domain-specific established concepts: DFA minimal states, predictive/causal states, LTI minimal realizations and probabilistic quotients have different assumptions and equivalence notions.

### Evidence
LTI minimal realizations are unique up to similarity when controllable and observable; causal-state minimal sufficient statistics are essentially unique up to isomorphism.

### Limitations / Red Team
Nonlinear/stochastic latent systems may not share these guarantees.

### Decision
Create a cross-domain assumption table rather than one universal minimal-realization theorem.

## P245 — STATE ISOMORPHISM TEST

**STATUS:** DERIVED

### Strongest supported claim
Two coordinate representations can encode the same state exactly under an invertible transformation, while a collapsed noninvertible representation cannot.

### Evidence
Fresh 3D invertible-coordinate test recovered the transformed state with RMSE 1.08e-15; collapsing to 2D produced reconstruction RMSE 0.578.

### Limitations / Red Team
Linear recovery tests only linear isomorphism; nonlinear invertible transformations require richer tests.

### Decision
State identity should be judged behaviorally/up to admissible isomorphism, not coordinate equality.

## P246 — CANONICAL REPRESENTATIVE COST

**STATUS:** COUNTEREXAMPLE

### Strongest supported claim
Coordinate-based canonicalization costs are not invariant under invertible rescaling and therefore cannot define an intrinsic canonical representative by themselves.

### Evidence
Fresh invertible rescalings changed mean L1/L2 coordinate costs substantially: [{'scale': 0.1, 'mean_l1': 8.095267773778296, 'mean_l2': 8.017947630069349}, {'scale': 1, 'mean_l1': 1.5956547639323337, 'mean_l2': 1.253401114753825}, {'scale': 10, 'mean_l1': 8.020845341938275, 'mean_l2': 7.942828046121051}].

### Limitations / Red Team
Some canonical forms exist in restricted theories after imposing normalization/balancing conventions.

### Decision
Separate invariant equivalence class from chosen canonical display/normal form.

## P247 — STATE DIMENSION VS CONTEXT

**STATUS:** DERIVED

### Strongest supported claim
Minimal required state size is monotone under exact context refinement and can jump discontinuously when a new independent context is admitted.

### Evidence
Fresh 3-bit fixture: [{'contexts': ['x1'], 'classes': 2, 'bits_lower_bound': 1}, {'contexts': ['x1', 'x2'], 'classes': 4, 'bits_lower_bound': 2}, {'contexts': ['x1', 'x2', 'x3'], 'classes': 8, 'bits_lower_bound': 3}, {'contexts': ['parity'], 'classes': 2, 'bits_lower_bound': 1}, {'contexts': ['x1', 'parity'], 'classes': 4, 'bits_lower_bound': 2}].

### Limitations / Red Team
Approximate representations can trade fidelity for smaller state and need not show exact monotone integer jumps.

### Decision
Report state dimension as d*(K,epsilon,model class), not a context-free scalar.

## P248 — STATE-DIMENSION GRAND RED TEAM

**STATUS:** DERIVED

### Strongest supported claim
No single state dimension is defensible as 'absolute' across changing context, model class, estimator, tolerance and finite-data horizon.

### Evidence
P225–P247 independently show context refinement, hidden-state redundancy, finite-rank threshold failure, coordinate nonuniqueness and estimator dependence.

### Limitations / Red Team
Special mathematical classes can still have a precise intrinsic minimal order relative to their fixed input/output semantics.

### Decision
Use context/model-relative dimension and retain NO FINITE STATE as a legitimate outcome.
