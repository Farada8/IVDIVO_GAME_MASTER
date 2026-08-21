# ABSOLUTE MATHEMATICS — Proof Pack v1

Status: **DERIVED mathematical statements; novelty not claimed.**

## P1 — Context refinement theorem

Define exact context equivalence:

\[
x\sim_{\mathcal K}y\iff\forall K\in\mathcal K,\; Obs_K(x)=Obs_K(y).
\]

If \(\mathcal K_1\subseteq\mathcal K_2\), then:

\[
\sim_{\mathcal K_2}\subseteq \sim_{\mathcal K_1}.
\]

**Proof.** If \(x\sim_{\mathcal K_2}y\), equality holds for every context in \(\mathcal K_2\), hence for every context in its subset \(\mathcal K_1\). ∎

Consequently the number of exact equivalence classes cannot decrease under context extension.

---

## P2 — Point-separating no-compression theorem

If \(\mathcal K\) separates points of \(X\), i.e. for every \(x\ne y\) some context distinguishes them, then any exact context-preserving representation \(B:X\to Z\) is injective.

**Proof.** Assume \(B(x)=B(y)\). A representation whose upper behavior depends only on \(B\) cannot distinguish \(x,y\), contradicting point separation. Therefore \(x=y\). ∎

Thus no nontrivial exact state compression exists.

---

## P3 — Tolerance monotonicity

Let \(\mathcal F_\varepsilon\) be the candidate representations whose defect is at most \(\varepsilon\). For \(0\le\varepsilon_1\le\varepsilon_2\):

\[
\mathcal F_{\varepsilon_1}\subseteq\mathcal F_{\varepsilon_2}.
\]

Therefore, if \(d^*(\varepsilon)\) is the minimum state count among feasible candidates:

\[
d^*(\varepsilon_2)\le d^*(\varepsilon_1).
\]

**Proof.** Every candidate satisfying the stricter threshold also satisfies the weaker threshold. Taking a minimum over a superset cannot increase the minimum. ∎

---

## P4 — Finite phase-boundary theorem

For a finite microstate set there are finitely many partitions \(B\). If each has a scalar defect \(D(B)\), then:

\[
d^*(\varepsilon)=\min_{B:D(B)\le\varepsilon}|B|
\]

is a nonincreasing step function whose changes can occur only at values in:

\[
\{D(B):B\text{ admissible}\}.
\]

**Proof.** The feasible set changes only when \(\varepsilon\) crosses one of finitely many candidate defects. Between consecutive defect values the feasible set is constant. Apply P3. ∎

---

## P5 — Incremental context refinement correctness

Let \(\Pi_{\mathcal K}\) be the partition induced by contexts \(\mathcal K\). Adding one context \(c\) can be computed by splitting each block of \(\Pi_{\mathcal K}\) according to the value of \(c\).

The resulting partition is exactly \(\Pi_{\mathcal K\cup\{c\}}\).

**Proof.** Two points remain equivalent iff they were equivalent under all old contexts and have equal \(c\)-values. This is precisely blockwise splitting by \(c\). ∎

---

## P6 — Congruence revocation under signature extension

A quotient valid for operation signature \(\Sigma\) remains valid after adding operation \(h\) iff the equivalence is also compatible with \(h\).

A single witness

\[
x\sim y,\quad h(x)\not\sim h(y)
\]

is sufficient to revoke the quotient under \(\Sigma\cup\{h\}\). ∎

---

## P7 — Contractive accumulated-error bound

Suppose in metric \(d\):

\[
d(P\mu,P\nu)\le\alpha d(\mu,\nu),\quad 0\le\alpha<1
\]

and the one-step model discrepancy is at most \(\delta\). Then recursively:

\[
e_{t+1}\le\delta+\alpha e_t.
\]

With \(e_0=0\):

\[
e_t\le \delta\sum_{j=0}^{t-1}\alpha^j=\delta\frac{1-\alpha^t}{1-\alpha}.
\]

Proof is induction on \(t\). ∎

---

## P8 — Bounded arity depth lower bound

A depth-\(h\) composition tree with fan-in at most \(b\) depends on at most \(b^h\) leaves. Therefore aggregating \(N\) independent inputs requires:

\[
h\ge\lceil\log_bN\rceil.
\]

---

## P9 — Local propagation lower bound

If information moves at most graph distance \(r\) per round, any output at vertex \(v\) depending on a source at distance \(d(u,v)\) requires:

\[
h\ge\left\lceil\frac{d(u,v)}r\right\rceil.
\]

This theorem is endpoint/task-relative. Graph diameter is only a valid substitution when the task specifically requires influence across a diameter pair or a fixed endpoint with that eccentricity.

---

## P10 — Recursive-update collision no-go

If there exist histories \(h_1,h_2\) and symbol \(a\) such that:

\[
Z(h_1)=Z(h_2)
\]

but

\[
Z(h_1a)\ne Z(h_2a),
\]

then no deterministic update rule \(U\) satisfying:

\[
Z(ha)=U(Z(h),a)
\]

exists for that state definition.

**Proof.** The same pair \((Z,a)\) would have to map to two different next states. ∎

---

## P11 — Exact minimization fixed-point statement

If a minimization operator returns a minimal representative unique up to isomorphism within a fixed semantic category, applying it again returns an isomorphic object:

\[
M(M(X))\cong M(X).
\]

This is a property of the minimization setup, not evidence for a novel universal “absolute object”.

---

## Proof boundary

These are ordinary mathematical derivations over declared assumptions. They do not by themselves establish novelty, physical universality, a context-free hierarchy of reality, or empirical truth outside the model class.
