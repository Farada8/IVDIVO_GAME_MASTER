# ABSOLUTE MATHEMATICS — RUN4 / AMSI-177..208

Status: **WORKING RESEARCH RUNTIME CANDIDATE / NOT CURRENT**

Run4 executes exactly 32 high-information tasks across four fronts:

1. AMSI-177..184 — real algorithmic self-improvement benchmark;
2. AMSI-185..192 — durable GitHub/Drive authority and recovery;
3. AMSI-193..200 — formal proof/replay frontier;
4. AMSI-201..208 — established-domain and real-data validation.

## Regression

- warm: **99/99 PASS**;
- final cold ZIP replay: **99/99 PASS**;
- final ZIP SHA256: `4d4d6aa89b49dd4696dcc06e2268a5934db721e69330203dae8bffa37236ab49`.

## Major negative result

The Run3 synthetic descendant-potential advantage did **not** transfer to the real weighted Max-Cut benchmark.

Hidden mean approximation ratio:
- current-score parent policy: `0.9965207913`;
- descendant-aware: `0.9958535172`;
- delta descendant-current: `-0.0006672741`;
- random-parent: `0.9785163759`.

Verdict: `REAL_TASK_NOT_SUPPORTED` for the current descendant-potential heuristic. It is no longer a default self-improvement policy.

## Live durability evidence

Run33 PR #108 is merged and `main/tools/ivdivo_durable_write_reconciler.py` is a merged generic dependency.

Run4 performed a branch-only GitHub CAS pilot:
- correct blob-SHA update succeeded;
- intentional reuse of the old blob SHA returned HTTP 409;
- stale bytes did not land;
- recovery used the fresh SHA and readback.

Drive probe:
- 294 bytes;
- expected/readback SHA256 `9fa1a7580242ef7b3d6f59e07a242c6e2223cf1e8db8fb1846f4fd30447a28f7`;
- exact bytes PASS.

Controlled two-store partial failure was repaired without force overwrite.

Durability claim ceiling: reversible GitHub/Drive research artifacts only; no paid/irreversible/provider replay.

## Formal proof status

Pinned Lean: `leanprover/lean4:v4.33.0`.

Four source-level theorem targets contain no `sorry`, but the current runtime has no Lean/Lake/Coq/Docker and the toolchain could not be installed here. Therefore no theorem is claimed machine-verified. Formal release remains HOLD.

## Cross-domain / scientific evidence

- exact MDP bisimulation: 4 states -> 2 blocks;
- causal abstraction: exact intervention-preserving control + lossy counterexample with TV 0.6;
- CIB-style small control reproduces compression/causal-information tradeoff;
- sample predictive matrix approaches planted rank 2 at threshold .05 as T rises to 20k, but rank remains threshold-sensitive;
- LTI identification recovers planted dynamics and exposes nonminimal coordinates;
- exact deterministic communication controls show one-bit output can require 4 input bits of one-way message identity;
- real statsmodels Nile data: AR(4) best held-out RMSE ≈ 115.754, residual ACF1 ≈ -0.195; observational-only, closure not established.

## Current contribution class

`BENCHMARK_PROTOCOL + ENGINEERING_SYNTHESIS`.

The active candidate is a fail-closed cross-domain abstraction falsification/certification protocol, not a new mathematical field.

## Next bank

Run4 derives AMSI-225..288 while preserving all earlier unexecuted banks.
Priority front: `225, 233, 241, 249, 257, 265, 273, 281`.

Google Drive full package folder:
`ENGINE_RUN4_AMSI177_208_REAL_SELF_IMPROVEMENT_FORMAL_SCIENCE_2026-08-21`
(folder ID `1glNILD5L8Pj3M1wG1wls3EoOmfNArfA4`).
