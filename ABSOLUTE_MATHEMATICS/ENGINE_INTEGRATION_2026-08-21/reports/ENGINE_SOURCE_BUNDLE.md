# ABSOLUTE MATH ENGINE v0.1 — SOURCE BUNDLE

The complete executable source tree is mirrored in the Drive ZIP. This GitHub review bundle records the implemented modules and interfaces under the candidate branch.

## Modules
- `models.py` — ContextContract, PromotionProblem, PromotionDecision, EvidenceRecord, ImprovementProposal.
- `context.py` — behavioral partitions, point-separating no-go, minimum context bases.
- `partition.py` — reference finite partition enumeration, output consistency, lumpability defect, minimum epsilon partition.
- `information.py` — entropy, MI, conditional MI, history/micro sufficiency gate.
- `closure.py` — TV, Dobrushin coefficient, rollout error, contractive bound, closure metadata.
- `construction.py` — locality/arity lower bounds, construction spectrum, Pareto dominance.
- `evidence.py` — EvidenceLedger, ClaimLedger, evidence-scope caps and SHA snapshots.
- `experiments.py` — immutable preregistration IDs/hashes and explicit deviations.
- `benchmarks.py` — mandatory positive/negative/adversarial benchmark registry.
- `si_bridge.py` — fail-closed SI-0012 bridge; only candidate feedback, external promotion required.
- `self_improvement.py` — lineage archive, regression-aware promotion gate, bounded descendant-potential/novelty priority.
- `pipeline.py` — end-to-end finite Markov no-go -> exact/approximate Promotion reference flow.

## Central engine law
`AUTHORITY -> CONTEXT -> NO-GO -> CANDIDATE -> CLOSURE -> SUFFICIENCY -> CONSTRUCTION -> EVIDENCE -> IMPROVEMENT`

## Self-improvement law
`OBSERVE -> ROOT CAUSE -> PROPOSE -> SANDBOX -> BENCHMARK -> ARCHIVE -> HOLD/CANDIDATE -> VERIFY`

## Evidence boundary
This source is a WORKING engineering candidate. It does not prove scientific novelty or real longitudinal recursive self-improvement. Exact finite partition enumeration is deliberately a ground-truth/reference solver and is not claimed scalable.

## Full reproducible source
Drive mirror `ENGINE_INTEGRATION_SELF_IMPROVEMENT_32X64_2026-08-21` contains `ABSOLUTE_MATH_ENGINE_INTEGRATION_32X64.zip`, complete Python modules, tests, fixtures, contracts, 32 run cards/results, next 64, state, Red Team and SHA-256 manifest.