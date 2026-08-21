# FORMAL RESULTS / COUNTEREXAMPLES P193–P224

## T7 — Context refinement
If K1⊆K2, then behavioral equivalence under K2 refines equivalence under K1.

## T8 — Bounded-arity balanced assembly depth
If each composition node has arity at most b and N independent primitives must be combined into one value, any balanced tree needs depth at least ceil(log_b N), and this bound is achieved by a balanced b-ary tree. This is explicitly an admissibility-relative result.

## T9 — Local communication lower bound
If information may propagate at most radius r per construction stage across a path metric, coupling endpoints at distance d requires at least ceil(d/r) stages. Unrestricted nonlocal composition removes this lower bound.

## T10 — Composition-closure flattening
If admissible typed maps are closed under composition, any finite admissible path has a one-arrow composite, so endpoint depth is 0/1/infinity.

## C4 — Passive equivalence can fail under interventions
A finite MDP fixture merges two states under the passive action but an alternative action sends them to different observable classes. Therefore passive predictive equivalence is not sufficient for control-safe abstraction.

## C5 — Signature-extension revocation
Parity on Z4 is compatible with addition mod 4 but fails compatibility after adding a unary operation h. Therefore quotient validity is relative to the operation signature.

## C6 — G-Rise language relativity
square(x) can be primitive in a weak finite-term language and definable after multiplication or iteration is admitted. Hence generator novelty requires a declared definability language.

## C7 — Genesis normal-form failure without confluence
The rewrite word AB with rules AB→C and AB→D has two distinct irreducible results. Therefore a unique genesis normal form cannot be assumed without confluence.
