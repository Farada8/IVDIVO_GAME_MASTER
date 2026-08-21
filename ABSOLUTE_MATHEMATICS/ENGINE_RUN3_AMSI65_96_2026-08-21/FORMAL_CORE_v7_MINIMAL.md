# AMSI-95 — FORMAL CORE v7 MINIMAL

Status: **CANDIDATE MINIMALIZATION**

Run3 removes terminology that does not currently earn operational or mathematical value.

# 1. Core problem

\[
\mathcal P=(X,\mathcal K,\varepsilon,\mathcal A,\mathcal M).
\]

- \(X\): lower-level states/realizations;
- \(\mathcal K\): required observation/prediction/intervention/operation contexts;
- \(\varepsilon\): permitted defect;
- \(\mathcal A\): admissible construction/resource model;
- \(\mathcal M\): candidate upper representation class.

A candidate abstraction/Promotion is:

\[
B:X\to Z.
\]

# 2. Exact semantic equivalence

\[
x\sim_{\mathcal K}y
\iff
\forall K\in\mathcal K:\ Law(Obs_K|x)=Law(Obs_K|y).
\]

No special new term is required where ordinary behavioral/contextual equivalence is sufficient.

# 3. Feasibility complexity

\[
d^*(\mathcal P)=\min\{Complexity(Z):B\text{ satisfies declared gates}\}.
\]

Possible outcomes:

\[
NO\_PROMOTION,\quad NO\_FINITE\_STATE,\quad EXACT,\quad APPROXIMATE,\quad RESOURCE\_ONLY,\quad INCONCLUSIVE.
\]

# 4. Recursive dynamic state

For temporal/control problems an accepted state requires either:

\[
Z_{t+1}=U(Z_t,a_t,o_{t+1})
\]

or an explicit recursive estimator/filter. Prediction alone is insufficient.

# 5. Approximate closure certificate

Record:

\[
C=(Metric,Normalization,Defect,Uncertainty,Horizon,Stability).
\]

PASS/HOLD/FAIL uses uncertainty, not point estimate alone.

# 6. Context/signature versioning

Every certificate is relative to:
- context family;
- intervention/action set;
- operation signature;
- model class;
- source/evidence hashes.

New contexts/operations may revoke an old abstraction.

# 7. Construction spectrum

Do not define one intrinsic scalar order.

Report a vector/Pareto object such as:

\[
Spec_C=(Depth,Communication,Memory,Time,Delegation).
\]

# 8. Generator novelty

Generator novelty is always language-relative:

\[
NEW\_RELATIVE\_TO\ L.
\]

The declaration must include the closure level of \(L\). Novelty that disappears under a definitional/conservative extension is not robust.

# 9. Genesis

Represent genesis as a typed process graph.

- feedback -> SCC modules;
- normal form claims require confluence evidence;
- genesis complexity is vocabulary/primitive-relative unless invariance is proved.

# 10. Evidence

Evidence and claims are separate. Evidence classes impose explicit claim ceilings. Claims are superseded/refuted through a graph; history is never overwritten.

# 11. Self-improvement

Self-improvement acts on search/proof/benchmark methods, not mathematical authority.

Candidate change:

\[
Parent\rightarrow Mutation\rightarrow Sandbox\rightarrow Hidden/HeldoutBenchmarks\rightarrow Archive\rightarrow Review.
\]

Archive selection must be compared with simple baselines.

# Removed from active core

The following are historical/project intuitions, not active foundations:

- intrinsic scalar `Ord(W)`;
- universal "Absolute Number" as a context-free unique object;
- universal 16-base hierarchy;
- promotion count as intrinsic order;
- spectral-gap-alone hierarchy;
- geometry-alone causal primitive;
- compressed history as automatically autonomous state;
- context-free generator novelty;
- unique genesis normal form without confluence.

# Current defensible thesis

> Given a declared family of behaviors/interventions, approximation tolerance, representation class and construction constraints, determine whether a nontrivial upper representation exists; if it does, certify exactly which semantic, dynamic, recursive and resource properties survive.

This is the smallest current core that remains useful after the prior-art and Red Team passes.
