# NEXT RESEARCH PROMPTS P129–P144

## A — Exact / Approximate Promotion Theorem Program

### P129 — PROMOTION RECORD MINIMAL AXIOMS
Take Formal Core v3.0 and ask which fields of the Promotion Record are logically independent. For each proposed field B,K,A,E,Gamma,D,C,M,Gmicro,R,F,N construct a fixture where removing only that field causes a false positive or prove it redundant. Output a minimal axiom schema, not a richer checklist by default.

### P130 — STOCHASTIC FACTOR MAP
Generalize deterministic semiconjugacy to Markov kernels. Define when a coarse map B turns a microscopic Markov process into an exact Markov factor. Crosswalk with ordinary/exact lumpability and probabilistic bisimulation. Prove the finite-state condition and test it on planted chains.

### P131 — NORMALIZED APPROXIMATE COMMUTATION DEFECT
Define a dimensionless closure defect that remains interpretable across state scales, units and target variances. Compare absolute RMSE, relative error, Wasserstein distance, KL-style predictive discrepancy and operator norms. Reject metrics that change materially under irrelevant rescaling.

### P132 — STOCHASTIC MULTISTEP ERROR BOUNDS
Derive multistep predictive-distribution error bounds from one-step kernel discrepancy plus contraction/mixing assumptions. Establish at least one positive theorem for finite Markov chains and construct a counterexample when the contraction assumption is removed.

### P133 — INTERVENTION-PRESERVING PROMOTION
Extend contextual equivalence from passive observation to interventions/actions. Define x~y only when every admissible intervention context yields the same observable law. Compare with bisimulation, MDP homomorphisms and PSRs. Test whether passive predictive equivalence can merge states that active interventions must split.

### P134 — CONTEXT FAMILY LATTICE
Treat admissible context families as an inclusion poset. Prove how behavioral partitions refine as contexts are added. Study whether there are minimal context bases that generate the same equivalence. Compute examples where one extra intervention doubles the required macro-state size.

### P135 — SIGNATURE EXTENSION BREAKS CONGRUENCE
Start with a quotient that is a congruence for a limited algebraic signature. Add one new operation and test whether the quotient remains well-defined. Characterize when a Promotion survives signature/context extension and when a previously valid order boundary must be revoked.

### P136 — NO-FINITE-PROMOTION CERTIFICATE
Develop a practical certificate that a finite-state Promotion is unsupported. Use growing distinguishability ranks/classes, nonregular symbolic controls, Hankel-rank growth and predictive-state tests. The Reactor must be able to return NO FINITE UPPER STATE.

## B — Predictive / Autonomous State Discovery

### P137 — CAUSAL-STATE RECONSTRUCTION CONTROL
Generate stochastic processes with known finite causal states. Reconstruct predictive equivalence from histories only, evaluate state recovery and future likelihood, and compare with hand-engineered macro variables. This is the primary positive control for autonomous-state discovery.

### P138 — PSR RANK CONTROLLED SYSTEMS
Use controlled dynamical systems with known system-dynamics matrix rank. Recover a predictive state representation from action-observation histories. Compare PSR rank to hidden-state count and to the project's proposed minimal autonomous state dimension.

### P139 — HIDDEN STATE VS PREDICTIVE DIMENSION
Construct HMM/POMDP examples where many hidden states are predictively redundant and examples where predictive dimension differs from naive latent-state count. Prove that 'number of hidden causes' is not the same as minimal predictive order.

### P140 — INFINITE PREDICTIVE STATE NEGATIVE SUITE
Expand beyond a^n b^n to several nonregular/nonfinite-memory processes. Track distinguishability/Hankel rank with horizon and sample size. Calibrate when finite-data saturation is false evidence for a finite upper state.

### P141 — PREDICTIVE INFORMATION BOTTLENECK FRONTIER
Compute the tradeoff I(Past;Z) versus I(Z;Future) for benchmark processes. Compare the information-bottleneck frontier with exact causal-state size, rollout closure and micro/history gain. Test whether the frontier provides a better compression coordinate than raw state dimension.

### P142 — NONLINEAR HISTORY/MICRO GAIN TEST
For each candidate macro state use flexible nonlinear comparators to estimate extra future information from deeper history and microstate. Use nested cross-validation and conditional-information estimators. Promotion fails if either gain remains stable and material.

### P143 — RECURSIVE STATE UPDATE GATE
A valid autonomous state should be recursively updateable from its current value and the next observation/action, not recomputed from the full past. Test recursive calculability on learned state representations and quantify update inconsistency.

### P144 — STATE ISOMORPHISM / IDENTIFIABILITY BENCHMARK
Fit multiple independently parameterized state models to the same process. Determine whether successful minimal states are related by invertible/isomorphic transformations. Separate behavioral uniqueness, dimension uniqueness, coordinate uniqueness and model nonidentifiability.
