# FORMAL CORE v8 — RUN4 MINIMAL CANDIDATE

The active core is an **abstraction feasibility/certification framework**, not a claim of one intrinsic scalar order.

Define

\[
\mathcal P=(X,\mathcal K,\mathcal I,\Sigma,\varepsilon,\mathcal A,\mathcal M),
\]

where `X` is lower state, `K` required observations/predictions, `I` interventions/actions, `Σ` operation signature, `ε` allowed defect, `A` construction/resource constraints, and `M` candidate representation class.

Candidate abstraction:

\[
B:X\to Z.
\]

## Gate 1 — semantic/interventional sufficiency

Exact equivalence is relative to declared contexts and interventions:

\[
x\sim y\iff \forall K\in\mathcal K,\forall I\in\mathcal I:\ Law(Obs_K\mid do(I),x)=Law(Obs_K\mid do(I),y).
\]

Approximate variants require an explicit metric and tolerance.

## Gate 2 — recursive state

Temporal state requires an online update/filter:

\[
Z_{t+1}=U(Z_t,a_t,o_{t+1}).
\]

Prediction without recursive updateability is insufficient.

## Gate 3 — residual information

Where meaningful, test calibrated residual dependence:

\[
I(Future;History\mid Z),\qquad I(Future;Micro\mid Z).
\]

## Gate 4 — dynamics

Every approximate closure result records:

`Metric, Defect, Uncertainty, Horizon, Stability`.

## Gate 5 — construction/resources

No intrinsic scalar `Ord` is assumed. Report a Pareto/vector object such as:

\[
(Depth,Communication,Memory,Time,Delegation).
\]

## Gate 6 — versioning and revocation

Every certificate is bound to:

\[
(\mathcal K,\mathcal I,\Sigma,\mathcal M,SourceHashes).
\]

New contexts, actions or operations may revoke an old abstraction.

## Gate 7 — evidence class

Keep separate:
- formal theorem;
- synthetic control;
- cross-domain internal benchmark;
- real observational data;
- real controlled/interventional data;
- human/provider/market evidence.

No evidence class is silently promoted.

## Self-improvement is not a theorem layer

Research-method evolution is empirical engineering:

\[
Method_t\to Mutation\to HiddenEvaluation\to Archive.
\]

Run4 demonstrates why this separation matters: a descendant-aware heuristic that looked positive on a synthetic landscape failed to beat current-score selection on the real Max-Cut benchmark.

## Current external contribution candidate

**Fail-Closed Cross-Domain Abstraction Falsification and Certification Protocol.**

Its value must be tested by whether the integrated gates discover meaningful failures missed by simpler domain baselines, not by project terminology.
