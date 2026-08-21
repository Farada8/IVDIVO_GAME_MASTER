# ABSOLUTE MATHEMATICS — NEXT 64 RESEARCH PROMPTS (P033–P096)

Generated from completed Batch32. Each prompt attacks a concrete unresolved dependency in Formal Core v2.0.

## A. Regime identifiability and generator switching

### P033 — IDENTIFIABLE K=2 SWITCHING GENERATOR
Freeze the current Ising fixture and fit an identifiable two-regime switching generator using only present/past macro observables. Use train/validation/test by trajectory. Compare against K=1 and K=3 with BIC/AIC and held-out likelihood. PASS only if K=2 improves prediction, regime persistence, and within-regime residual closure simultaneously. Report label-switching/identifiability caveats.

### P034 — REGIME LABEL STABILITY BOOTSTRAP
Bootstrap whole trajectories, refit the K=2 regime model, align labels by generator distance, and measure cluster/generator stability. Require coefficient and regime-boundary stability across resamples. If labels/generators rotate substantially, classify regime structure as unstable mixture modeling rather than state discovery.

### P035 — REGIME WITHOUT ORDER-PARAMETER PROXIES
Residualize all regime features against global magnetization, |m|, field variance and time. Discover regimes using only residual feature content. Compare to the original regime model. PASS only if predictive and closure gains survive removal of obvious phase-order proxies.

### P036 — REGIME RUN-LENGTH NULL
Generate surrogate regime sequences preserving label frequencies and empirical run-length distribution but severing their alignment to macro-state. Refit experts under those surrogate labels. Test whether real inferred regimes outperform this stronger null on held-out prediction and residual whitening.

### P037 — REGIME-CONDITIONAL NOISE LAW
Fit one drift law per regime, then characterize residual variance, tails, spatial covariance and temporal memory separately inside each regime. Determine whether regime conditioning makes the unresolved process substantially simpler. Reject regime-as-state if only mean prediction improves.

### P038 — REGIME-SPECIFIC MEMORY KERNEL
Estimate a minimal one- or two-parameter memory kernel separately within each inferred regime. Compare with a global memory kernel under equal parameter count. PASS only if regime-specific kernels reduce residual ACF and improve rollout without unstable parameter estimates.

### P039 — REGIME TRANSFER ACROSS TEMPERATURE
Learn the regime representation at low T and freeze it. Apply to nearby low-T values and to high T. Fit only regime-specific generator coefficients at target T. Determine whether regime semantics persist, deform smoothly, or collapse across the phase transition.

### P040 — SWITCHING GENERATOR ADVERSARIAL CONTROL
Construct a synthetic process with smooth continuously varying coefficients but no discrete regimes. Apply the K=1/2/3 switching pipeline. It must reject discrete regimes or flag approximation-only behavior. Otherwise the detector is nonselective.

## B. Minimal predictive/autonomous state

### P041 — STRONG MICRO COMPARATOR
For the best macro-state, train a nonlinear micro-enriched comparator with raw local spin patches, using nested cross-validation and matched capacity. Measure held-out predictive gain beyond macro state. Promotion fails if micro access yields a material stable gain.

### P042 — CONDITIONAL HISTORY GAIN
Estimate how much additional predictive power is obtained from lagged macro-history after conditioning on the current candidate state. Use one, two and four lags with capacity control. PASS only when all deeper history gains are below a predeclared tolerance.

### P043 — EMPIRICAL PREDICTIVE EQUIVALENCE
Cluster histories by estimated future-distribution similarity rather than current-state geometry. Compare the resulting predictive classes with the project macro-state. Quantify mutual recoverability and predictive loss. Treat causal-state/PSR literature as authority for established analogues.

### P044 — STATE DIMENSION PARETO CURVE
For dimensions d=1..16, fit constrained candidate states and record prediction error, residual memory, micro gain, rollout error and description complexity. Identify the Pareto frontier rather than a single R² optimum. Do not call an elbow intrinsic without null calibration.

### P045 — SAMPLE-SIZE STATE-DIMENSION NULL
Repeat the state-dimension curve on synthetic processes with known state dimension at multiple sample sizes. Measure spurious elbows and overestimation/underestimation rates. Use this to calibrate any later claim of a natural state dimension.

### P046 — MINIMAL STATE UNIQUENESS
Fit several independently parameterized minimal-state models at the same dimension. Test whether their states are related by invertible transformations on held-out data. Separate uniqueness of behavior, uniqueness up to isomorphism, and coordinate non-identifiability.

### P047 — CANONICALIZATION COST
Compare three ways to choose a canonical representative: lexicographic convention, minimum-description-length representative, and predictive-state basis. Measure which properties are invariant and which are convention dependent. Do not conflate canonical with unique.

### P048 — STATE COMPLETION FAILURE MODES
Create a taxonomy of ways a candidate state can fail: hidden memory, hidden micro information, regime heterogeneity, nonstationarity, insufficient context class, non-identifiability, and rollout instability. Build one synthetic fixture for each failure and require the Reactor to diagnose the correct cause.

## C. Coarse-graining, memory and stochastic closure

### P049 — MEMORY DEFECT VS SCALE
Across a dense grid of coarse scales, estimate residual memory with confidence intervals and matched model capacity. Plot memory defect against compression and prediction error. Treat any monotonic pattern as empirical only until theorem assumptions are identified.

### P050 — CONDITIONAL MUTUAL INFORMATION MEMORY
Replace simple residual ACF with conditional mutual information I(Past;Future|CurrentState). Estimate with multiple estimators and synthetic calibration. Determine whether the closure conclusions survive a stronger nonlinear memory metric.

### P051 — SPATIAL MEMORY KERNEL
Estimate residual spatial covariance as a function of distance and orientation. Fit the smallest spatial kernel that explains it. Test whether adding this kernel improves ensemble rollout beyond the local Gaussian closure rejected in v1.11.

### P052 — HEAVY-TAIL NOISE FAMILY
Compare Gaussian, Student-t, Gaussian-mixture and empirical-resampling residual models after conditioning on macro state. Use held-out log-likelihood and ensemble statistics. Reject any noise family that improves fit but destabilizes long rollout.

### P053 — MEMORY-KERNEL VS MARKOV EMBEDDING
Compare an explicit finite memory-kernel model with an augmented Markov state of equal effective dimension. Evaluate prediction, residual whitening, rollout and interpretability. Determine whether memory is better represented as history dependence or hidden state.

### P054 — COMPRESSION-MEMORY MONOTONICITY CONDITIONS
Search mathematically for restricted classes of nested Markov partitions where stronger compression provably cannot reduce lumpability quality. If no theorem is found, identify the minimal counterexample breaking each proposed assumption.

### P055 — QUASI-LUMPABILITY CALIBRATION
Generate finite Markov chains with known quasi-lumpability epsilon. Estimate the coarse model from finite samples and test whether the Reactor recovers epsilon with calibrated uncertainty. This becomes an approximate-closure ground truth benchmark.

### P056 — SCALE/NOISE RENORMALIZATION
Track how fitted drift, noise amplitude, tail index, spatial correlation and memory kernel change with coarse scale. Test for reproducible scaling relations. Do not claim universality unless the relations transfer across distinct systems.

## D. Promotion, composition and non-flattenability

### P057 — COMMUTATION DEFECT BENCHMARK SUITE
Build a benchmark library containing exact homomorphism, exact lumpability, approximate lumpability, noncongruence, future-target-only predictor and identity/constant maps. Compute a normalized commutation defect for each and verify correct ranking.

### P058 — MULTI-CONTEXT PROMOTION TEST
Define at least five admissible observation/intervention contexts. A candidate coarse state must preserve behavior across all of them, not just one target. Measure context-wise defects and reject Promotion if one essential context splits the equivalence classes.

### P059 — RECURSIVE MACRO COMPOSITION
Take validated macro states as inputs to a second-level operation without reopening microstates. Compare the second-level result to direct micro simulation. Quantify the additional defect introduced by recursive macro-only composition.

### P060 — FLATTENING SEARCH ALGORITHM
Given a staged Promotion chain, automatically search for a direct map satisfying the same endpoint behavior. If found, mark the hierarchy flattenable. Report computational/resource constraints separately from mathematical nonexistence.

### P061 — BOUNDED-ARITY DEPTH
Formalize depth under a maximum composition arity b. Derive exact depth for N independent primitives and test robustness when interactions are added. Keep the result explicitly relative to the arity constraint.

### P062 — LOCALITY-CONSTRAINED DEPTH
Define an admissibility class using spatial locality radius r. Determine when direct coarse maps violate locality while staged maps remain local. Test whether the resulting depth is stable under coordinate-preserving transformations and small perturbations.

### P063 — ADMISSIBILITY INVARIANCE AUDIT
For each proposed admissibility rule, apply equivalent reparameterizations, relabelings and unit changes. Reject rules whose depth changes under irrelevant coordinate choices. Keep only physically/computationally grounded invariants.

### P064 — ORDER SPECTRUM DOMINANCE
Compute Ord_A for a family of independently motivated admissibility classes. Define Pareto dominance over depth, closure defect and resource cost. Test whether any boundary remains robust across most classes rather than appearing only under one hand-picked constraint.

## E. Theorem and counterexample program

### P065 — FORMALIZE NO-FREE-GENERATIVITY IN MANY-SORTED ALGEBRAS
Extend T1 from single-sorted algebras to many-sorted/typed algebras and partial operations where appropriate. State exact assumptions and give a structural-induction proof or counterexample.

### P066 — RESOURCE-RISE THEOREM
Formalize resource-bounded reachability Reach_K and prove conditions under which adding macros leaves extensional closure unchanged while strictly increasing Reach_K. Give at least one exponential speedup example and one no-speedup counterexample.

### P067 — G-RISE DEFINITION STRESS TEST
Define DefClosure(Gamma) precisely. Construct examples where a seemingly new operator is definable by composition, parameterization, oracle access or coding tricks. Refine G-Rise until these false positives are excluded.

### P068 — GENERATOR-EXTENSION MINIMALITY
Study DeltaGamma_min = argmin complexity extension required to generate an otherwise unreachable behavior. Compare description-length choices and show where the minimizer is nonunique or encoding dependent.

### P069 — COMPOSITION-CLOSED ADMISSIBILITY WITH COSTS
Extend T2 to transformations carrying resource annotations. Determine when composition closure of maps does not imply closure of cost-bounded admissibility. Separate categorical reachability depth from resource-constrained depth.

### P070 — APPROXIMATE FLATTENING THEOREM
For epsilon-compositional Promotions, derive an upper bound on direct composite defect in terms of per-stage defects and Lipschitz/stability constants. Identify cases where errors explode and staged representation remains preferable despite flattenability.

### P071 — ORDER BOUNDARY STABILITY THEOREM TARGET
Formulate sufficient conditions for an approximate boundary to persist under small perturbations of dynamics and observation map. Prove for a restricted finite-state class or produce a counterexample showing why no general theorem holds.

### P072 — CANONICAL PREDICTIVE QUOTIENT THEOREM TARGET
Determine conditions under which behavioral equivalence admits a finite minimal quotient unique up to isomorphism. Crosswalk directly to Myhill-Nerode, causal states and minimal deterministic/probabilistic automata. Mark all project-specific residue.

## F. Cross-domain validation suite

### P073 — RULE-90 BLIND RECOVERY
Hide the known even-site Rule-90 coarse map from the Reactor. Give only trajectories and a restricted search class. Test whether it rediscovers an exact B satisfying B F² = F B, with held-out verification.

### P074 — HARD CELLULAR-AUTOMATON COARSE GRAIN
Select nontrivial elementary CA rules from different Wolfram classes. Search local coarse maps and time rescalings. Compare found hierarchies with Israeli–Goldenfeld-style coarse-graining and report exact/approximate closure.

### P075 — EXACT LUMPABLE MARKOV RECOVERY
Generate random lumpable chains with hidden partitions. Infer the partition from trajectories only. Measure partition recovery, transition-matrix error and false-positive rate across sample sizes.

### P076 — QUASI-LUMPABLE MARKOV RECOVERY
Perturb exact lumpable chains by controlled epsilon. Determine whether inferred macro partitions degrade smoothly and whether estimated closure defect tracks planted epsilon.

### P077 — SYMBOLIC MYHILL-NERODE RECOVERY
Use several regular languages with known minimal DFA sizes. From labeled strings only, recover future-equivalence classes and compare to exact Myhill-Nerode states. This is a canonical positive control for predictive quotient discovery.

### P078 — NONREGULAR SYMBOLIC NEGATIVE CONTROL
Use a nonregular language/process whose exact finite predictive quotient does not exist. The Reactor must avoid falsely declaring a finite absolute state merely because finite data admit a small approximate automaton.

### P079 — LTI MINIMAL REALIZATION RECOVERY
Generate nonminimal state-space systems with hidden unobservable/uncontrollable modes. Recover input-output behavior and test whether the pipeline identifies the minimal order and equivalence up to similarity.

### P080 — STOCHASTIC HMM/PSR CROSSWALK
Generate finite HMMs with known predictive-state rank. Compare hidden-state count, PSR rank, causal/predictive equivalence and project minimal autonomous state. Identify cases where hidden-state dimension is not the predictive-state dimension.

## G. Novelty, canonicality and theory boundaries

### P081 — FULL TERMINOLOGY CROSSWALK
Create a theorem-by-theorem crosswalk between project terms and established concepts: congruence, quotient, bisimulation, lumpability, sufficient statistic, causal state, PSR, minimal realization, RG/coarse-graining, operads/categories. Label EXACT, PARTIAL or PROJECT-SPECIFIC.

### P082 — NOVELTY SEARCH: PROMOTION RECORD
Search literature for frameworks that jointly track coarse map, dynamic closure, memory defect, micro gain, admissibility, recursive reuse and flattenability. Determine whether the combined Promotion Record is already standard under another name.

### P083 — NOVELTY SEARCH: ORDER SPECTRUM
Search for existing notions of spectra/posets of coarse-graining depth under resource/locality constraints. Compare with hierarchical complexity, multiscale decompositions and categorical factorizations.

### P084 — ABSOLUTE NUMBER RED TEAM
Attempt to eliminate the term 'absolute number' entirely by translating every proposed property into established state/equivalence/minimal-description language. Keep the term only if a mathematically distinct invariant remains.

### P085 — COORDINATE-INVARIANCE REQUIREMENTS
List every project quantity and test whether it is invariant under relabeling, similarity transforms, unit changes, monotone reparameterization and admissible isomorphism. Reject or redefine coordinate-dependent candidates.

### P086 — CONTEXT-RELATIVITY THEOREM AUDIT
Prove that enlarging the admissible context family can only refine behavioral equivalence classes under the stated definition. Quantify how minimal state size can increase with context richness.

### P087 — CANONICALITY VS MDL
Investigate whether minimum description length can choose a useful representative without being representation-language dependent. Construct coding-language counterexamples and specify what invariance class, if any, is defensible.

### P088 — FORMAL CORE NOVELTY VERDICT v3
After P081–P087, issue a strict novelty verdict for every remaining Formal Core object. Categories: established, recombination/framework, theorem target, computational methodology, or unsupported branding.

## H. Autonomous research engine and grand falsification

### P089 — BENCHMARK REGISTRY
Create a machine-readable registry of all positive, negative and adversarial fixtures with planted truth, metrics, gates and expected failure modes. No new theorem may be promoted unless it passes the registry.

### P090 — CLAIM LEDGER
Maintain a claim ledger with status KNOWN/DERIVED/HYPOTHESIS/COUNTEREXAMPLE/FAILED/INCONCLUSIVE/NOVELTY_UNVERIFIED. Each claim must link evidence, assumptions, falsifiers and superseded versions.

### P091 — AUTOMATIC COUNTEREXAMPLE FIRST
Modify Research Director policy so every attractive theorem target first spawns a Counterexample task before proof development. Measure whether this reduces wasted cycles and post-hoc redefinitions.

### P092 — NULL/TARGET COMPATIBILITY CHECKER
For every proposed null model, explicitly list the invariants it preserves. Reject nulls that preserve the very invariant defining the claim being tested. Automate this as a pre-experiment gate.

### P093 — PREREGISTRATION ARTIFACT
Before each computational experiment, write metrics, thresholds, sample split, null families and allowed follow-ups into an immutable preregistration file. After results, prohibit silent threshold changes.

### P094 — INDEPENDENT RED-TEAM ROTATION
Run at least two differently prompted Red-Team agents on major claims. Compare overlap/disagreement. A claim cannot move to DERIVED if all serious objections come only from the same reasoning template.

### P095 — MONTHLY GRAND FALSIFICATION
Ignore incremental progress and attack the entire current Formal Core using the benchmark registry, literature audit and theorem counterexamples. Output KEEP/MERGE/REDEFINE/REJECT/PROVE with explicit changes to authority state.

### P096 — ABSOLUTE MATHEMATICS RESEARCH ROADMAP v3
Synthesize all surviving results into a prioritized roadmap ranked by falsifiability, foundational impact, cross-domain transfer and proof tractability. Select the next 32 questions automatically, but require at least 40% to be negative/control/Red-Team tasks.
