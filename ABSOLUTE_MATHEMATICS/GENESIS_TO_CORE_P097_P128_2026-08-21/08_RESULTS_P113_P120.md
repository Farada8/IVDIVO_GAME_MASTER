# DETAILED RESULTS P113–P120

## P113 — TEMPORAL GENESIS VS STATIC DIFFERENCE

**STATUS:** DERIVED

### Strongest supported claim
Temporal growth distinguishes ordering dynamics from a merely different static state.

### Evidence
Fresh Ising control: low-T median L_wall grew from 2.00 to 58.56; high-T only from 2.03 to 2.97.

### Red Team
Finite-size saturation and model-specific dynamics prevent reading the fitted growth exponent as a universal order constant.

### Decision
KEEP temporal genesis tests; static shuffle difference is insufficient.

## P114 — DYNAMIC SCALE L(t) AS ORDER COORDINATE

**STATUS:** HYPOTHESIS

### Strongest supported claim
L(t) is useful as a dynamical scale coordinate for coarsening but should not be called an intrinsic order level.

### Evidence
Low-T Ising shows strong growth and high-T remains near microscopic scale in the fresh control.

### Red Team
Different morphologies/processes can share the same L(t); finite-size saturation destroys strict monotonicity.

### Decision
Use L(t) as one macro coordinate, not Ord(W).

## P115 — DISCRETE OBJECT PRIMITIVE GRAND REVIEW

**STATUS:** FAILED

### Strongest supported claim
No tested localized object definition has passed the project's strong primitive criterion across scales and controls.

### Evidence
v1.7 square blocks were confounded by averaging; v1.7b causal locality reduced to geometry; v1.8 domains failed geometry-matched excess autonomy; v1.9 wall segments failed dynamic closure/causal channeling.

### Red Team
This does not imply objects can never be emergent primitives in other systems.

### Decision
PERMANENT anti-pattern: natural-looking geometry + predictability + locality is not enough.

## P116 — FIELD + LAW PRIMITIVE REVIEW

**STATUS:** HYPOTHESIS

### Strongest supported claim
State+generator is a stronger candidate primitive concept than object identity, but v1.10 did not establish deterministic closure.

### Evidence
v1.10 recovered the qualitative +phi -phi^3 +Laplacian structure and useful rollout, yet held-out derivative R² remained moderate.

### Red Team
Allen-Cahn/Model-A field structure is established physics, so recovery is a positive control rather than novelty.

### Decision
KEEP state+generator as framework candidate; require stochastic/ensemble closure.

## P117 — STOCHASTIC CLOSURE FAILURE REVIEW

**STATUS:** FAILED

### Strongest supported claim
Simple state+Gaussian-noise closure is insufficient for the tested coarse Ising field.

### Evidence
v1.11 residual was heteroscedastic, spatially correlated and heavy-tailed; simple iid/heteroscedastic/AR noise improved only some short horizons.

### Red Team
A more expressive unresolved-process model may still close the coarse dynamics.

### Decision
Require residual-shape, spatial-covariance, memory and ensemble-rollout gates.

## P118 — MEMORY DIMENSION IS CONTEXT-RELATIVE

**STATUS:** DERIVED

### Strongest supported claim
Memory dimension is relative to the coarse map, tolerance, target and model family.

### Evidence
v1.12: one lag nearly whitened b=2, b=4 was threshold-sensitive, and b=8 retained memory through four lags.

### Red Team
Raw lag count is not intrinsic state dimension.

### Decision
KEEP d_M(B;epsilon,delta,K), reject universal d_M.

## P119 — HISTORY COMPRESSION VS STATE COMPLETION

**STATUS:** DERIVED

### Strongest supported claim
History can be compressible without the compressed history variable completing the state.

### Evidence
v1.13 one recursive latent coordinate reproduced much of raw-lag rollout behavior but residual ACF remained too high, especially at strong compression.

### Red Team
The tested exponential memory family was narrow.

### Decision
KEEP separate HistoryCompressibility and StateCompletion metrics.

## P120 — REGIME STATE — PREDICTION VS CLOSURE

**STATUS:** HYPOTHESIS

### Strongest supported claim
A persistent K=2 regime variable carries predictive information but still does not complete the macro state.

### Evidence
Previous Batch32 found modest K=2 prediction gains and strong regime persistence, but within-regime residual ACF stayed high; regime+memory helped more than regime alone.

### Red Team
Regimes can be smooth stage proxies or mixture-regression artifacts.

### Decision
Do not promote r_t; continue only under stronger null/identifiability tests.
