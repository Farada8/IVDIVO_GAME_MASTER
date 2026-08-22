# RUN4 — 32 sequential results (AMSI-177..208)

| ID | Verdict | Key result |
|---|---|---|
| AMSI-177 | PASS_REAL_BENCHMARK | Weighted Max-Cut objective benchmark with exact small-graph optima, train/hidden split and equal policy budgets. |
| AMSI-178 | **FAIL_DESCENDANT_ADVANTAGE** | Hidden descendant-aware mean 0.9958535 < current-score 0.9965208; Δ=-0.0006673. |
| AMSI-179 | PASS_BASELINE | Random parent hidden mean 0.9785164, materially below current-score. |
| AMSI-180 | NO_ADDED_VALUE | Current simple diversity policy is identical to current-score on this genotype/search setup. |
| AMSI-181 | PASS_NO_LARGE_GOODHART_SIGNAL | Current mean train-hidden gap ~0.00310, max ~0.00881; hidden family blind but same distribution family. |
| AMSI-182 | PROXY_NOT_VALIDATED | Current descendant-potential statistic is not validated prospectively; retrospective calibration is inconsistent. |
| AMSI-183 | PASS_DOSE_RESPONSE | Search budgets 4/8/12/20 evaluated with train, hidden and archive-size outputs. |
| AMSI-184 | **REAL_TASK_NOT_SUPPORTED** | Run3 synthetic descendant-policy support is not promoted to real-task evidence. |
| AMSI-185 | PASS_AUTHORITY_RESOLVED | Cycle6 #128 merged; Cycle5 #110 remains draft/provenance only. |
| AMSI-186 | PASS_MERGED_CAPABILITY | Run33 #108 merged; durable reconciler now a main generic dependency. |
| AMSI-187 | PASS_LIVE_GITHUB_CAS | Fresh blob update PASS; intentional stale blob update HTTP 409; stale bytes did not land; repaired via fresh SHA. |
| AMSI-188 | PASS_LIVE_DRIVE_READBACK | 294-byte Drive probe exact readback, SHA256 9fa1a758...a28f7. |
| AMSI-189 | PASS_LIVE_REPAIR | Controlled Drive-success/GitHub-stale-write partial failure repaired without force overwrite; final transaction complete. |
| AMSI-190 | PASS_CHECKPOINT_LINEAGE | Hash-bound checkpoint lineage resumes only under matching authority/source identity. |
| AMSI-191 | PASS_CHAOS_RESUME | Stale handoff/main drift -> REFRESH_AUTHORITY; matching authority -> RESUME. |
| AMSI-192 | PASS_LIMITED_DURABILITY | Durable research runtime supported for reversible GitHub/Drive artifact workflow only. |
| AMSI-193 | **BLOCKED_RUNTIME_UNAVAILABLE** | No Lean/Lake/Coq/Docker/Podman; pinned Lean 4.33.0; installation unavailable in current runtime. |
| AMSI-194 | PARTIAL_SOURCE_PROOFS_READY | Four zero-sorry Lean source proof targets prepared but not compiled. |
| AMSI-195 | **BLOCKED_NOT_MACHINE_FORMALIZED** | Finite phase-boundary theorem specified, not Lean-verified. |
| AMSI-196 | **BLOCKED_NOT_MACHINE_FORMALIZED** | Contractive accumulated-error theorem specified, not Lean-verified. |
| AMSI-197 | **BLOCKED_NOT_MACHINE_FORMALIZED** | Signature-extension revocation specified, not Lean-verified. |
| AMSI-198 | PASS_PROPERTY_CROSSCHECK | Exhaustive small property controls agree with context-refinement and recursive-collision theorem cores. |
| AMSI-199 | PASS_REFERENCE_DEPENDENCIES | Proof dependency graph created; compiled import/axiom minimization still pending. |
| AMSI-200 | **HOLD_FORMAL_RELEASE** | Replay package prepared; formal release blocked until actual Lean cold replay and complex proofs. |
| AMSI-201 | PASS_ESTABLISHED_BASELINE | Exact MDP probabilistic bisimulation recovers blocks {0,1}/{2,3}. |
| AMSI-202 | PASS_EXACT_PLUS_LOSSY_COUNTEREXAMPLE | Exact do(X) preservation TV=0; forgotten intervention variable produces TV=0.6. |
| AMSI-203 | PASS_PRIOR_ART_BASELINE | Small CIB-style objective reproduces compression/causal-information tradeoff. |
| AMSI-204 | PASS_WITH_THRESHOLD_SENSITIVITY | Predictive rank@0.05: 3 at T=5k -> 2 at T=20k (planted dimension); rank@0.01 remains 6. |
| AMSI-205 | PASS_LTI_IDENTIFICATION | One-step RMSE ~0.005005; reachability/observability diagnostics expose nonminimal ambient state. |
| AMSI-206 | PASS_EXACT_RESOURCE_BASELINE | 4-bit Equality/IP mod2 each require 16 exact one-way message classes -> 4 bits despite one-bit output. |
| AMSI-207 | PASS_REAL_OBSERVATIONAL_PILOT | Nile 1871–1970: AR(4) held-out RMSE ~115.754, residual ACF1 ~-0.195; observational only, closure not established. |
| AMSI-208 | PASS_INCREMENTAL_FAILURE_VALUE | Integrated gates catch three false acceptances missed by simple one-gate protocols: recursive/history, intervention, horizon/stability. |

## Regression

- **99/99 warm PASS**
- **99/99 final cold ZIP replay PASS**
- ZIP SHA256: `4d4d6aa89b49dd4696dcc06e2268a5934db721e69330203dae8bffa37236ab49`

Strong scientific release remains **HOLD**.
