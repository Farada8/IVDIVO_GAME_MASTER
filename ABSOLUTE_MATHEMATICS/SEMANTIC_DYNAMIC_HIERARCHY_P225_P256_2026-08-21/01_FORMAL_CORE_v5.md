# ABSOLUTE MATHEMATICS — FORMAL CORE v5.0

## Status

Research framework / falsification protocol.
Not an established new mathematical field.

This version incorporates P225–P256.

---

# 1. SEMANTIC STATE

A state is never defined without a declared family of admissible questions/tests/interventions.

Let K be the context family.

\[
x\sim_K y
\iff
\forall k\in K:
\mathrm{Law}(Obs_k|x)=\mathrm{Law}(Obs_k|y).
\]

If actions are relevant, K must contain action-conditioned tests.

Passive predictive equivalence is not sufficient for control-safe abstraction.

## Context refinement

\[
K_1\subseteq K_2
\Longrightarrow
\sim_{K_2}\subseteq\sim_{K_1}.
\]

Therefore exact minimal state size may increase as the system is required to answer more questions.

## Context basis

A context basis \(K^*\subseteq K\) is any smallest subfamily inducing the same equivalence partition as K.

It need not be unique.

## State-size object

Use:

\[
d^*(K,\epsilon,\mathcal M)
\]

where:
- K = contexts/actions;
- epsilon = tolerated behavioral defect;
- M = candidate model/representation class.

No context-free scalar state dimension is assumed.

## Authority comparators

Depending on domain:
- Myhill–Nerode / DFA minimization;
- causal states;
- predictive state representations;
- probabilistic bisimulation / MDP homomorphism;
- ordinary/exact lumpability;
- minimal realization.

The Reactor must allow:

\[
\boxed{NO\ FINITE\ UPPER\ STATE}.
\]

---

# 2. DYNAMIC CLOSURE

A candidate state Z is operationally autonomous only if five gates are addressed.

## D1 — Behavioral/dynamical defect

Exact deterministic:
\[
B\circ F=G\circ B.
\]

Exact stochastic:
use the appropriate factor/lumpability/bisimulation condition.

Approximate:
report metric and normalization explicitly.

No raw-unit-dependent error may be compared across scales without justification.

## D2 — Horizon and stability

One-step error is insufficient.

If an approximate macro transition is contractive with coefficient \(\alpha<1\), a typical recursive bound has form:

\[
e_t\le \epsilon \sum_{j=0}^{t-1}\alpha^j.
\]

When contraction fails, arbitrarily small one-step defects may accumulate to order-one long-horizon error.

## D3 — History sufficiency

Require low additional future information from deeper history:

\[
I(Future;History_{past}\mid Z)\approx0
\]

or an appropriately calibrated predictive-gain analogue.

## D4 — Micro sufficiency

Require low additional future information from the hidden lower state:

\[
I(Future;Micro\mid Z)\approx0.
\]

## D5 — Recursive updateability

The state must update online:

\[
Z_{t+1}=U(Z_t,o_{t+1},a_{t+1})
\]

or through an explicit recursive estimator/filter.

A whole-history summary that must be recomputed from the complete past is not automatically an autonomous online state.

---

# 3. PREDICTIVE DIMENSION / IDENTIFIABILITY

Hidden-state count is not predictive dimension.

A system may contain arbitrarily many behaviorally redundant latent states while retaining the same predictive rank.

Use ground-truth comparators such as:
- Hankel/system-dynamics matrix rank;
- minimal DFA state count;
- causal-state cardinality;
- minimal realization order.

Finite rank estimates require:
- horizon scaling;
- sample-size scaling;
- noise calibration;
- singular-value uncertainty.

## State identity

Coordinate equality is not required.

Successful minimal states may be equivalent:
- up to permutation;
- similarity;
- invertible transformation;
- behavioral isomorphism.

A canonical representative is an extra convention unless a domain-specific canonical form theorem exists.

---

# 4. CONSTRUCTION COMPLEXITY SPECTRUM

The project should avoid using one universal scalar "Order" for construction depth.

For an admissibility class A:

\[
Ord_A(x,y)
\]

is the minimum admissible construction depth.

If A is closed under well-typed composition, finite endpoint depth flattens to one.

Nontrivial depth can arise from explicit externally grounded constraints:

- locality;
- bounded arity;
- communication;
- working memory;
- time/energy;
- typing / architecture.

## Lower-bound examples

Locality:
\[
depth\ge \left\lceil d/r \right\rceil.
\]

Bounded arity:
\[
depth\ge \lceil \log_b N\rceil.
\]

Combined:
\[
depth\ge
\max\left(
\lceil d/r\rceil,
\lceil \log_b N\rceil
\right)
\]
as a lower bound for the corresponding simple assembly/communication tasks.

## Spectrum

Represent construction complexity as:

\[
Spec_C(x,y)
=
(
Ord_{local},
Ord_{arity},
Cost_{comm},
Cost_{memory},
Cost_{time},
\dots
).
\]

Use Pareto dominance/incomparability rather than forcing a total ranking.

---

# 5. ADMISSIBILITY RED TEAM

Every admissibility class must declare:

1. external grounding;
2. invariance/symmetry group;
3. resource/physical interpretation;
4. composition-closure status;
5. whether it was specified before observing the desired hierarchy.

A heuristic naturalness rubric may aid Red Team but is not itself a mathematical invariant.

Contrived constraints designed only to forbid the direct map do not establish an objective hierarchy.

---

# 6. CURRENT PROMOTION OBJECT

The most defensible current object is:

\[
\mathfrak P=(S,D,C,G)
\]

where:

## S — Semantic State
contexts/interventions, equivalence, context basis, predictive dimension, identifiability.

## D — Dynamic Closure
defect metric/normalization, horizon/stability, history gain, micro gain, recursive update.

## C — Construction Complexity
admissibility, depth, locality/arity/communication/memory costs, flattenability, invariance.

## G — Generativity / Genesis
R-Rise, Resource Rise, G-Rise_L, delegation and genesis grammar from the previous Formal Core.

P225–P256 mostly refined S, D and C.

---

# 7. PERMANENT NEGATIVE RULES

Do not infer:

- state from hidden entity count;
- control-safe state from passive prediction;
- finite state from short finite-data rank saturation;
- canonical coordinates from minimality;
- long-horizon closure from one-step epsilon;
- intrinsic hierarchy from locality/arity/resource depth without naming the constraint;
- total order from a multidimensional cost spectrum;
- natural admissibility from a post-hoc hierarchy-saving restriction.

---

# 8. CURRENT RESEARCH PRIORITY

The next highest-value problems are:

1. controlled/interventional predictive-state reconstruction;
2. rigorous contractive/noncontractive stochastic error bounds;
3. calibrated conditional-information sufficiency tests;
4. finite/infinite predictive-rank discrimination;
5. practical state-isomorphism/identifiability tests;
6. cross-domain construction-complexity benchmarks;
7. exact novelty audit of the integrated Promotion protocol.

The historical terms "absolute number" and "order" should now be treated as project shorthand,
not as already-established context-free mathematical objects.
