# ABSOLUTE MATHEMATICS — FORMAL CORE v2.0

## KEEP

### Contextual / predictive equivalence
`x ~_K y` iff all admissible contexts/observations in K give the same externally relevant behavior. Dynamic stochastic version: `x ~ y` iff `P(Future|x)=P(Future|y)`.

This is retained as the behavioral basis of Promotion, but is not project novelty by itself.

### Promotion map
`B: X_micro -> Z_macro`.

A valid Promotion requires more than compression.

### Dynamic commutation / closure defect
Exact target:
`B ∘ Gamma_micro = Gamma_macro ∘ B`.

Approximate target:
`D_B = d(B Gamma_micro, Gamma_macro B) <= epsilon`.

### Minimal autonomous macro-state
Project target:
`Z* = argmin_Z C(Z)`
subject to predictive sufficiency, low history gain, low micro gain, bounded closure defect, rollout fidelity and a declared context class.

### Compression–closure frontier
Do not optimize compression alone. Track a structured record such as:
`F(B)=(compression, memory defect, prediction error, rollout error, micro gain)`.

### Rise taxonomy
- R-Rise: representational quotient/compression.
- Resource Rise: improved reach under a cost budget while extensional closure can remain unchanged.
- G-Rise: genuinely new generator not definable in the previous generator closure.

### Admissibility-relative depth
Use `Ord_A(x,y)` only together with an explicit admissibility class A.

### Order spectrum
Use `Spec_O(W)={Ord_A(W)}` over a family of independently justified admissibility classes rather than one context-free integer.

## MERGE WITH ESTABLISHED THEORY
- Future equivalence → Myhill–Nerode / contextual equivalence / causal states / predictive state representations.
- Minimal dynamical state → minimal realization / sufficient statistic / predictive state, depending on the system class.
- Quotient compatibility → congruence / homomorphism.
- Exact Markov closure → lumpability.
- Memory after coarse-graining → Mori–Zwanzig / generalized Langevin perspective.
- Regime state → switching dynamical systems / HMM / regime-switching models.
- Cellular-automaton rule hierarchy → established CA coarse-graining / renormalization analogues.

## REDEFINE

### “Absolute number”
Reject context-free wording. A defensible dynamic candidate is a minimal representative of a predictive/behavioral equivalence class sufficient for the declared context and dynamics. It need not be unique as coordinates; uniqueness may hold only up to isomorphism.

### “Primitive”
Use: `Primitive = state representation + effective generator + unresolved-process law if stochastic`.
A compressed object alone is not a primitive.

### “Order”
Represent order by a structured object containing admissibility, boundary evidence, closure defect, compression, state dimension, memory, recursive usability and flattenability.

## REJECT
1. `Ord = number of Promotion steps`.
2. `Compression => higher order`.
3. `Pure quotient => G-Rise`.
4. `Prediction on one target => primitive`.
5. `Natural-looking domain/interface => primitive`.
6. `More compression => more memory` as a universal law.
7. A unique canonical coordinate system without extra convention.
8. Spectral gap alone as an objective order boundary.

## PROVE / DEVELOP
1. No-Free-Generativity under induced operations — proved in the stated algebraic form.
2. Composition-closed admissibility collapses endpoint depth — proved under stated assumptions.
3. Characterize restricted classes where compression-memory monotonicity can hold.
4. Give invariance criteria for admissibility families.
5. Define robust approximate commutation for stochastic dynamics.
6. Build an exact crosswalk from minimal autonomous state to PSR/causal-state/minimal-realization notions.
7. Establish conditions for genuinely non-flattenable recursive Promotion.
8. Maintain a cross-domain benchmark registry so the theory cannot survive by overfitting one physical fixture.
