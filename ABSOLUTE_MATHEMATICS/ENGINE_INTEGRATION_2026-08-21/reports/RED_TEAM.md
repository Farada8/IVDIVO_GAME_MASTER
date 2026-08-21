# INDEPENDENT RED TEAM — Engine Integration v0.1

## MAJOR 1 — Benchmark Goodhart risk
The self-improvement archive can overfit its benchmark registry.

**Mitigation:** hidden/held-out benchmark families, cross-domain transfer, protected regression axes,
and archive diversity. Do not promote solely on one composite score.

## MAJOR 2 — Metaproductivity proxy is only a proxy
`lineage_potential` uses observed descendant performance. It is not a causal estimate of future
self-improvement potential.

**Mitigation:** label it heuristic; compare against current-score-only and random-parent baselines.

## MAJOR 3 — Exact finite learner does not scale
Bell-number partition enumeration becomes unusable quickly.

**Mitigation:** keep as oracle/ground-truth fixture only; next phase adds refinement/optimization solvers.

## MAJOR 4 — CMI estimation can lie
The implemented estimator is exact-count discrete plug-in estimation and is biased in sparse/high-dimensional data.

**Mitigation:** calibration fixtures, permutation/bootstrap, alternate estimators, uncertainty-aware HOLD.

## MAJOR 5 — SI-0012 interface drift
The bridge depends on keys emitted by SI-0012 candidate runtime.

**Mitigation:** versioned bridge contract and fail closed on missing keys.

## MAJOR 6 — Stacked math authority is not main
Latest math artifacts live on draft research branches/Drive.

**Mitigation:** new integration branch is based on fresh main and references exact source branch/SHA;
do not pretend prior research is merged runtime.

## MAJOR 7 — 20/20 tests are engineering evidence only
They do not establish mathematical novelty, natural-system truth, scientific acceptance or production utility.

## MAJOR 8 — Self-modification safety
An open-ended archive can accumulate changes that optimize benchmarks while making the system harder to inspect.

**Mitigation:** bounded mutation scope, immutable parent, rollback, forbidden paths, candidate-only writes,
human review/promotion and traceable lineage.

## Verdict
`ENGINEERING_CANDIDATE = PASS`
`AUTONOMOUS_CURRENT_PROMOTION = FAIL`
`SCIENTIFIC_NOVELTY = UNVERIFIED`
`REAL_LONGITUDINAL_SELF_IMPROVEMENT = NOT_YET_PROVEN`
