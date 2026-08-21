# ENGINEERING MODULES + CONTRACTS — RUN2

**New Run2 math-domain modules:** 34

## New modules

- `belief_state.py`
- `controlled_psr.py`
- `recursive_update.py`
- `revocation.py`
- `rank_growth.py`
- `state_isomorphism.py`
- `context_basis_approx.py`
- `state_red_team.py`
- `refinement.py`
- `branch_bound.py`
- `kblock_feasibility.py`
- `phase_boundary.py`
- `incremental_context.py`
- `congruence.py`
- `ensemble.py`
- `scalability.py`
- `metrics.py`
- `metric_invariance.py`
- `stochastic_bounds.py`
- `horizon_policy.py`
- `cmi_uncertainty.py`
- `continuous_cmi.py`
- `confidence_gate.py`
- `nonstationarity.py`
- `resource_models.py`
- `pareto.py`
- `graph_depth.py`
- `arity_locality_search.py`
- `symmetry.py`
- `admissibility_audit.py`
- `construction_report.py`
- `known_resource_benchmarks.py`
- `certificate.py`
- `capability_adapter.py`

## Contracts / machine protocols

- `CONSTRUCTION_SPECTRUM_CONTRACT_v2.json`
- `CONTINUOUS_RESEARCH_LOOP_CONTRACT_v1.json`
- `NO_FINITE_STATE_PROTOCOL_v1.json`
- `PARALLEL_CAPABILITY_DEPENDENCY_v1.json`
- `PROMOTION_CERTIFICATE_SCHEMA_v1.json`
- `RECURSIVE_STATE_CONTRACT_v1.json`
- `SCALABLE_PROMOTION_SOLVER_CONTRACT_v1.json`
- `UNCERTAINTY_AWARE_CLOSURE_CONTRACT_v1.json`

## Generic infrastructure boundary

Do not duplicate or silently import generic Self-Improvement mechanisms from working/draft branches.

- SI-0012 Cycle4 generic capabilities are consumed only after MERGED/CURRENT capability resolution.
- Run33 durable multi-store reconciliation is consumed only after MERGED/CURRENT capability resolution.
- Until then, `capability_adapter.py` returns fail-closed fallback/HOLD.

## Proof/evidence surfaces

- `proofs/PROOF_PACK_v1.md`
- `proofs/PROOF_OBLIGATIONS_v1.json`
- `contracts/PROMOTION_CERTIFICATE_SCHEMA_v1.json`
- `engine/absolute_math_engine/certificate.py`
- `reports/EXPERIMENT_EVIDENCE_AMSI33_64.json`
- `reports/TEST_REPORT_RUN2.json`

## Continuous research surface

`daemon/research_loop.py` is a durable SQLite queue/checkpoint harness:
- immediate job chaining;
- persisted job/result hashes;
- failure state;
- recovery of interrupted RUNNING jobs.

It is executor-agnostic and does not itself call OpenAI or any model.
