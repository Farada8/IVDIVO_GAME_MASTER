# AMSI-33..64 — 32 EXECUTION RESULTS

| ID | Status | Strongest supported claim |
|---|---|---|
| AMSI-33 | **PASS_REFERENCE** | A known finite POMDP belief state provides an exact recursively updateable positive control. |
| AMSI-34 | **PASS_REFERENCE** | Controlled future-test representations can be benchmarked against planted finite predictive rank. |
| AMSI-35 | **PASS** | Recursive updateability is now an executable gate, not a prose requirement. |
| AMSI-36 | **PASS** | A passive state can be automatically revoked by a newly admitted action context. |
| AMSI-37 | **PASS_WITH_CAP** | The engine can refuse a finite-state claim within a declared rank cap. |
| AMSI-38 | **PASS_REFERENCE** | Raw coordinate mismatch is not state disagreement when an admissible invertible map exists. |
| AMSI-39 | **PASS_HEURISTIC** | A scalable greedy context reduction heuristic can preserve the full finite behavioral partition on controls. |
| AMSI-40 | **COUNTEREXAMPLE** | History compression can fail to define any deterministic recursive update. |
| AMSI-41 | **PASS** | Exact finite Markov Promotion can be solved by refinement in relevant cases without Bell enumeration. |
| AMSI-42 | **PASS_BOUNDED** | Search can exploit observation-label structure and explicit budgets. |
| AMSI-43 | **PARTIAL_PROTOTYPE** | A fixed-k feasibility interface and witness contract now exist. |
| AMSI-44 | **PASS** | For a finite candidate family, d*(epsilon) is a nonincreasing step function and exact breakpoints can be enumerated from candidate defects. |
| AMSI-45 | **PASS** | Adding one exact context only requires splitting old equivalence blocks by the new signature. |
| AMSI-46 | **PASS** | Operation-signature extension can automatically revoke an old quotient with a compact congruence witness. |
| AMSI-47 | **PASS** | Promotion search need not discard alternative feasible representations. |
| AMSI-48 | **PASS_SMALL_SCALE** | Reference and scalable exact solvers agree on the current ground-truth fixture. |
| AMSI-49 | **PASS** | Closure metrics now declare probability/geometry/support/normalization assumptions. |
| AMSI-50 | **PASS** | Declared scalar-rescaling/relabeling invariances are executable regression tests. |
| AMSI-51 | **PASS** | Contractive one-step kernel errors admit a geometric accumulated-TV bound under declared assumptions. |
| AMSI-52 | **PASS_REFERENCE** | Validation horizon can be tied to a declared contraction tail instead of an arbitrary fixed number. |
| AMSI-53 | **PASS** | CMI gates can carry uncertainty rather than hard point-estimate thresholds. |
| AMSI-54 | **PARTIAL** | Two continuous/quantized estimators agree qualitatively on a planted dependence control. |
| AMSI-55 | **PASS** | Uncertainty crossing a threshold now yields HOLD rather than false precision. |
| AMSI-56 | **PASS** | Strong transition-law drift can automatically invalidate a stationary-generator assumption. |
| AMSI-57 | **PASS_CONTRACT** | Communication complexity is an explicit construction/resource axis, not semantic state size. |
| AMSI-58 | **PASS_CONTRACT** | Streaming memory can differ sharply for outputs of similar semantic size. |
| AMSI-59 | **PASS** | Time/space/resource tradeoffs should remain partially ordered. |
| AMSI-60 | **PASS** | Locality lower bounds are task/endpoint-relative and computable from graph distance. |
| AMSI-61 | **INCONCLUSIVE** | The elementary max of separate lower bounds is not automatically an exact joint complexity formula. |
| AMSI-62 | **PASS** | Admissibility symmetry is now testable and arbitrary label-dependent rules can be rejected. |
| AMSI-63 | **PASS_PROTOCOL** | Preregistration, external grounding and symmetry evidence can make post-hoc hierarchy rescue auditable. |
| AMSI-64 | **PASS** | Construction complexity now has a machine-readable Pareto output instead of a forced scalar order. |

## Key evidence / limitations

- **AMSI-33:** POMDP final belief `[0.1031207943,0.8968792057]`; recursive/full-history max error `0.0`. Ground-truth model, not learned state.
- **AMSI-34:** controlled predictive rank `2`; ground-truth test matrix, not sample-based PSR learning.
- **AMSI-36:** passive pair `[0,1]` revoked by action `1`: observation laws `[1,0]` vs `[0,1]`.
- **AMSI-37:** ranks `[1,2,3,4,5]` → `NO_FINITE_STATE_WITHIN_CAP` for cap 4; not a proof of global infinite state.
- **AMSI-40:** same summary `0.0` for histories `[0]` and `[0,0]`, append `1` → `0.5` vs `1/3`; deterministic recursive update impossible for this state definition.
- **AMSI-41:** exact refinement recovered `[[0,1],[2,3],[4,5]]` in 2 rounds.
- **AMSI-42:** bounded search recovered the same 3 states with defect 0 after 13 completed candidates; worst-case exponential remains.
- **AMSI-43:** `FEASIBLE_AT_MOST_K` for k=3, but backend is bounded combinatorial, not actual MILP/SAT.
- **AMSI-44:** exact breakpoints `(0,4)`, `(0.03,3)`, `(0.05,2)`.
- **AMSI-46:** addition-only parity quotient passes; adding unary `h` fails with witness `[0,2,0,1]`.
- **AMSI-48:** exhaustive/refinement/branch-bound all agree at 3 states on n=6; this is not large-scale performance evidence.
- **AMSI-50:** NRMSE scale-invariance spread about `6.94e-17`; TV relabeling preserved `0.1`.
- **AMSI-51:** `alpha=0.7`, `delta=0.01`, accumulated bound tends to `0.033333...`.
- **AMSI-52:** contraction horizons for tail `1e-3`: alpha .2→5, .5→10, .9→66, alpha 1→HOLD.
- **AMSI-53:** conditional CMI `0.6041` bits, permutation p≈`0.00826`, bootstrap 95% CI≈`[0.5675,0.6492]`.
- **AMSI-54:** Gaussian CMI≈`0.2725`, binned≈`0.2436`; kNN/neural estimators remain missing.
- **AMSI-56:** transition drift≈`0.9524` > `0.2` → DRIFT.
- **AMSI-57:** deterministic Equality n=64 benchmark lower bound 64 communicated bits for one-bit output.
- **AMSI-58:** parity exact one-pass upper bound 1 bit; palindrome prefix-distinguishability lower bound 32 bits for n=64.
- **AMSI-60:** path diameter 5; source-target locality lower bounds r=1→5, r=2→3. Diameter is not universal for free-output tasks.
- **AMSI-61:** 42 small line cases searched; no strict optimal super-max theorem established → INCONCLUSIVE.
- **AMSI-62:** degree-sequence rule passed 24 relabelings; node-0-specific rule failed.
- **AMSI-63:** contrived hierarchy rule risk HIGH: not preregistered, target-specific, ungrounded, symmetry-failing.
- **AMSI-64:** Pareto front retained candidates A/B and rejected dominated C.

All detailed per-prompt artifacts and exact test evidence are preserved in the Drive/local Run2 package.
