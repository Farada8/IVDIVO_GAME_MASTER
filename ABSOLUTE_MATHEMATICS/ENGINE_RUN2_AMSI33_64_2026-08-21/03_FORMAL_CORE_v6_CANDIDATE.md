# ABSOLUTE MATHEMATICS — FORMAL CORE v6 CANDIDATE

Status: **research synthesis / not a claim of a new field.**

## 1. Promotion problem

Define:

\[
\mathcal P=(X,\mathcal K,\varepsilon,\mathcal A,\mathcal M)
\]

where:

- \(X\): lower/micro realization space;
- \(\mathcal K\): required observations, predictions, operations and interventions;
- \(\varepsilon\): permitted approximation defect;
- \(\mathcal A\): construction/resource admissibility;
- \(\mathcal M\): representation/generator model class.

A candidate Promotion is:

\[
B:X\to Z
\]

with an upper state \(Z\) and, where dynamics matter, a recursive update/generator.

## 2. Semantic feasibility

Exact behavioral equivalence:

\[
x\sim_{\mathcal K}y
\iff
\forall K\in\mathcal K,\;Law(Obs_K|x)=Law(Obs_K|y).
\]

Point-separating \(\mathcal K\) implies no nontrivial exact compression.

Define minimal feasible state complexity:

\[
d^*(\mathcal K,\varepsilon,\mathcal M).
\]

For fixed candidate model class:

\[
\mathcal K_1\subseteq\mathcal K_2
\Rightarrow
d^*(\mathcal K_1,0)\le d^*(\mathcal K_2,0),
\]

while:

\[
\varepsilon_1\le\varepsilon_2
\Rightarrow
d^*(\mathcal K,\varepsilon_2,\mathcal M)
\le
d^*(\mathcal K,\varepsilon_1,\mathcal M).
\]

So richer required semantics make exact compression harder; larger tolerated error cannot make the optimum state-count problem harder.

## 3. Dynamic autonomy

A state claim is incomplete without:

\[
Z_{t+1}=U(Z_t,o_{t+1},a_{t+1})
\]

or an explicit recursive estimator.

Autonomy gates:

\[
I(Future;History\mid Z)\approx0,
\]

\[
I(Future;Micro\mid Z)\approx0,
\]

plus recursive-update consistency and long-horizon closure.

## 4. Approximate closure

A closure result is the tuple:

\[
(D,\ Metric,\ Normalization,\ Horizon,\ Stability,\ Uncertainty).
\]

PASS requires the uncertainty interval to lie entirely inside the tolerance. If the interval crosses the tolerance, verdict is HOLD.

Under TV contraction coefficient \(\alpha<1\) and one-step defect \(\delta\):

\[
e_t\le\delta\frac{1-\alpha^t}{1-\alpha}.
\]

## 5. Finite phase boundary

For a finite candidate representation family:

\[
d^*(\varepsilon)=\min_{B:D(B)\le\varepsilon}|B|
\]

is a nonincreasing step function with breakpoints among candidate defects \(D(B)\).

Fresh Run2 fixture:

\[
d^*(\varepsilon)=
\begin{cases}
4,&0\le\varepsilon<0.03,\\
3,&0.03\le\varepsilon<0.05,\\
2,&\varepsilon\ge0.05.
\end{cases}
\]

This is a finite optimization property. Generic representation phase transitions have established prior art.

## 6. Construction complexity

Semantic state complexity and construction complexity remain distinct. Report:

\[
Spec_C=(Depth,Communication,Memory,Time,\ldots)
\]

under declared admissibility. Use Pareto dominance, not a universal scalar `Ord`.

## 7. Context/signature revocation

A Promotion certificate is versioned to context family, operation signature, model class and source hashes.

Adding one context may split behavioral classes. Adding one operation \(h\) may revoke a congruence if:

\[
x\sim y,\qquad h(x)\not\sim h(y).
\]

Therefore Promotion is not permanently valid independent of future capabilities.

## 8. Proof certificate

A complete candidate Promotion should have machine gates:
1. AUTHORITY
2. CONTEXT
3. NO_GO
4. CLOSURE
5. HISTORY_SUFFICIENCY
6. MICRO_SUFFICIENCY
7. RECURSIVE_UPDATE
8. CONSTRUCTION
9. EVIDENCE

The certificate is hash-bound to source/evidence references.

## 9. Feasibility surface

The current central object is:

\[
\boxed{\mathfrak F(\mathcal K,\varepsilon,\mathcal A,\mathcal M)}
\]

whose outputs include Verdict, \(d^*\), Closure, ParetoConstruction and ProofCertificate.

Possible verdicts:
`NO_PROMOTION`, `NO_FINITE_STATE`, `EXACT`, `APPROXIMATE`, `RESOURCE_ONLY`, `INCONCLUSIVE`.

## 10. Self-improvement

The engine improving the engine is a separate optimization problem. It maintains a lineage archive of algorithms/workflows and evaluates candidate mutations under hidden/held-out benchmarks, protected regression axes, cross-domain transfer and evidence-class limits.

The archive may preserve worse immediate nodes if they are useful stepping stones. No current benchmark score is treated as a proof of future metaproductivity.

## Current thesis

The strongest defensible project thesis is not:

> everything has an absolute integer order.

It is:

> given required semantics, tolerated error, candidate representations and construction constraints, determine whether a nontrivial upper state exists, how autonomous it is, what it costs to realize, and what evidence can legitimately support that conclusion.
