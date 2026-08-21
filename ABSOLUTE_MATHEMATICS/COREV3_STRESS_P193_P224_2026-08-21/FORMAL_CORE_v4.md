# ABSOLUTE MATHEMATICS — FORMAL CORE v4.0

## Status
Research framework / theorem-and-benchmark program. Not an established new field.

## Module I — SEMANTIC STATE

A macro state is defined relative to a context family K.

Exact behavioral equivalence:
\[
x\sim_K y
\iff
\forall k\in K,\ \mathrm{Law}(Obs_k|x)=\mathrm{Law}(Obs_k|y).
\]

If K contains interventions/actions, passive observational equivalence is insufficient.

Context enlargement refines the partition:
\[
K_1\subseteq K_2
\Rightarrow
\sim_{K_2}\subseteq\sim_{K_1}.
\]

Primary comparator for state discovery:
- causal states / predictive equivalence;
- PSR/Hankel rank;
- bisimulation / MDP homomorphism when actions are present;
- minimal realization in realization-theoretic classes.

The Reactor must allow:
\[
\boxed{NO\ FINITE\ UPPER\ STATE}.
\]

## Module II — DYNAMIC CLOSURE

Deterministic exact:
\[
B\circ F = G\circ B.
\]

Finite stochastic exact:
ordinary lumpability / probabilistic-bisimulation-style aggregation, with terminology matched to the preserved property.

Approximate closure must include:
\[
(D,\ metric,\ normalization,\ horizon,\ stability/mixing).
\]

One-step fit is insufficient.

A candidate autonomous state Z should also satisfy, approximately:
\[
I(Future;History|Z)\approx0,
\qquad
I(Future;Micro|Z)\approx0.
\]

Recursive updateability is required for an online state:
\[
Z_{t+1}=U(Z_t,Observation/Action_{t+1})
\]
or via an explicit estimator/filter state.

## Module III — CONSTRUCTION / HIERARCHY

Semantic state and construction depth are distinct.

Depth is always:
\[
Ord_A(x,y)
\]
relative to admissibility A.

If A is closed under well-typed composition:
\[
Ord_A(x,y)\in\{0,1,\infty\}.
\]

Nontrivial depth therefore requires explicit constraints:
- locality;
- bounded arity;
- resource/time/memory/communication;
- typing;
- other independently justified restrictions.

Use an Order Spectrum:
\[
Spec(x,y)=\{Ord_A(x,y)\}_{A\in\mathfrak A}.
\]

Each A must declare the coordinate/symmetry group under which it is intended to be invariant.

## Module IV — GENERATIVITY / GENESIS

R-Rise: representational quotient/factor only.

Resource Rise: same unbounded extensional closure, improved budgeted reach.

G-Rise_L: new generator relative to an explicit definability language/closure schema L.

No context-free G-Rise claim is permitted until invariance under declared language extensions is proved.

Macro autonomy requires a micro/oracle delegation budget. Hidden calls to the lower simulator do not count as closed upper dynamics under the autonomous-Promotion interpretation.

Genesis:
- typed process graph;
- feedback represented by SCC modules;
- condensation DAG between modules;
- noncommutative operator words;
- normal form only if confluence/Church-Rosser conditions are established.

## Promotion Record v4

\[
\mathfrak P=(S,D,H,G)
\]

### S — Semantic State
- coarse map B;
- context/intervention family K;
- equivalence/state representation;
- predictive rank/dimension;
- identifiability/isomorphism class.

### D — Dynamic Closure
- exact/approx generator;
- defect metric and normalization;
- validated horizon;
- stability/mixing;
- residual history gain;
- residual micro gain;
- recursive update rule.

### H — Hierarchy / Construction
- admissibility A;
- depth;
- resource cost;
- flattenability;
- symmetry/invariance;
- robustness across admissibility families.

### G — Generativity / Genesis
- R/Resource/G-Rise_L classification;
- definability language;
- delegation/oracle budget;
- genesis program/process graph;
- confluence/nonconfluence status.

## Permanently rejected shortcuts

1. Numeral base or representation change = order rise.
2. Compression = Promotion.
3. Passive prediction alone = intervention-safe state.
4. Single-target prediction = primitive.
5. Hidden-state/entity count = predictive order.
6. Natural geometry/domain/wall = primitive.
7. One-step PDE fit = closed generator.
8. Pure quotient = G-Rise.
9. Promotion-step count = intrinsic order.
10. More compression = more memory universally.
11. Preferred detector scale = natural boundary.
12. Finite upper state must exist.
13. Canonical coordinates follow from minimality.
14. G-Rise is language-independent by default.
15. Unique genesis normal form exists without confluence.

## Current narrow research residue

Potentially project-specific value is limited to a unified falsification-first Promotion protocol combining context/intervention-aware state equivalence, exact/approximate dynamic closure, history/micro sufficiency, recursive updateability, admissibility-relative hierarchy and flattening, resource vs generator novelty, delegation/autonomy checks, genesis-process diagnostics, and cross-domain ground-truth benchmark gating.

Novelty of this combined protocol remains unverified.
