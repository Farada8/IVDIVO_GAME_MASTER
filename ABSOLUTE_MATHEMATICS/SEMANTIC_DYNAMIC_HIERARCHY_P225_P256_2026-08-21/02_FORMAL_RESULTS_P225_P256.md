# FORMAL RESULTS / COUNTEREXAMPLES — P225–P256

## T11 — Context refinement

For exact behavioral equivalence:

\[
x\sim_K y
\iff
\forall k\in K,\ Obs_k(x)=Obs_k(y)
\]

(or equality of the corresponding observable laws).

If \(K_1\subseteq K_2\), then:

\[
\sim_{K_2}\subseteq\sim_{K_1}.
\]

Thus adding contexts cannot merge previously distinct exact equivalence classes.

---

## T12 — Context basis existence in finite families

For a finite context family K and finite state set X, at least one inclusion-minimal
subfamily inducing the same behavioral partition exists.

Such a basis need not be unique.

The fresh 3-bit fixture has four available contexts and four distinct minimum bases of size three.

---

## T13 — Contractive recursive error form

If a macro transition is contractive with coefficient \(\alpha<1\) in a metric d and each
step introduces at most epsilon discrepancy, then a recursive estimate has the form:

\[
e_{t+1}\le \epsilon+\alpha e_t
\]

and therefore:

\[
e_t\le \epsilon\frac{1-\alpha^t}{1-\alpha}.
\]

Precise applicability depends on how the one-step kernel/model discrepancy is defined.

---

## C8 — Noncontractive small-error counterexample

Let the true two-state chain leak from state 0 to absorbing state 1 with probability epsilon per step,
while the approximate chain is the identity.

One-step TV error is epsilon, but starting at state 0:

\[
TV_t=1-(1-\epsilon)^t.
\]

For epsilon=0.01 this reaches approximately 0.63 by t=100 and 0.993 by t=500.

Hence no horizon-free Promotion conclusion follows from one-step epsilon alone.

---

## C9 — Hidden-state redundancy

Duplicating behaviorally identical hidden states can increase hidden-state count arbitrarily while
leaving predictive Hankel rank fixed.

Fresh family:
2,4,8,16 hidden states all retained predictive rank 2.

---

## C10 — Coordinate-cost noncanonicality

Invertible coordinate rescalings preserve the represented state behavior while changing L1/L2 coordinate
costs. Therefore coordinate norm or raw code length cannot define an intrinsic canonical representative
without restricting the allowed coordinate/coding class.

---

## T14 — Locality lower bound

If information can move at most graph distance r per construction round, then any task requiring
dependence between locations at graph distance d needs at least:

\[
\lceil d/r\rceil
\]

rounds.

This is a resource/admissibility-relative theorem, not an intrinsic order theorem.

---

## T15 — Bounded-arity lower bound

If each composition node combines at most b independent inputs, a depth-h tree can depend on at most \(b^h\)
leaves. Combining N independent primitives therefore needs:

\[
h\ge\lceil\log_b N\rceil.
\]

A balanced b-ary tree achieves the bound when unconstrained by geometry.

---

## T16 — Combined elementary lower bound

When both independent bounded-arity and locality lower bounds apply to the same task:

\[
depth\ge
\max\left(
\lceil\log_b N\rceil,
\lceil d/r\rceil
\right).
\]

Equality is not guaranteed in arbitrary architectures.
