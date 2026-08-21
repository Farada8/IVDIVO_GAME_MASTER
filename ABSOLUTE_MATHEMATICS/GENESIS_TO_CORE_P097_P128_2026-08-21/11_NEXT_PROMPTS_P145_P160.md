# NEXT RESEARCH PROMPTS P145–P160

## C — Admissibility, Hierarchy and Order Spectrum

### P145 — LOCALITY-RELATIVE ORDER
Define admissibility by a maximum spatial interaction radius. Compute shortest Promotion depth under locality and compare with unrestricted flattening. Test robustness under translations, rotations and coordinate-preserving relabelings.

### P146 — BOUNDED-ARITY ORDER
Define admissibility by maximum operator arity. Prove depth bounds for assembling N primitives and determine how interactions change them. Keep all conclusions explicitly relative to the arity budget.

### P147 — RESOURCE-BUDGET ORDER
Define admissible transformations by time/description/communication cost. Distinguish map existence from map affordability. Build examples where mathematical depth is 1 but resource-constrained depth is logarithmic or linear.

### P148 — TYPE-CONSTRAINED ORDER
Use many-sorted/typed systems where intermediate representations have types not directly constructible from the base type. Determine whether typed non-flattenability yields a meaningful order spectrum or merely reflects arbitrary type design.

### P149 — ADMISSIBILITY COMPOSITION-CLOSURE CHECKER
Given a proposed admissibility class A, automatically test whether it is closed under well-typed composition. If yes, invoke the flattening theorem and reject any claimed finite depth >1. Store counterexamples to closure when no.

### P150 — ORDER SPECTRUM COMPUTATION
For the same endpoint transformation compute Ord_A across locality, arity, time, memory and communication constraints. Represent the result as a spectrum/vector rather than one integer. Study dominance and robustness of boundaries across A.

### P151 — ROBUST ORDER BOUNDARY
Define a boundary as robust only if it survives a specified family of independently justified admissibility classes and perturbations. Develop a stability score and adversarial controls where a boundary exists under only one hand-picked A.

### P152 — ADMISSIBILITY COORDINATE INVARIANCE
Audit each admissibility rule under unit changes, basis changes, relabelings, similarity transforms and graph isomorphisms. Reject constraints whose resulting order changes under mathematically irrelevant coordinates.

## D — Representational, Resource and Genuine Generativity

### P153 — R-RISE FORMAL CALCULUS
Formalize representational rise as quotient/factor formation with no claim of new extensional closure. Define composition laws for R-Rise and prove what invariants can and cannot change under pure quotienting.

### P154 — RESOURCE RISE THEOREM FAMILY
Formalize Reach_K under several cost models. Prove examples of polynomial/exponential speedup from reusable macros without extensional novelty. Identify cost models under which the apparent speedup disappears.

### P155 — G-RISE RELATIVE TO LANGUAGE
Define G-Rise_L using a fixed generator language L and DefClosure_L. Construct pairs of languages in which the same candidate operator changes status from primitive to definable. Determine which statements are invariant under conservative language extensions.

### P156 — DEFINABILITY WITH ITERATION / RECURSION
Separate finite term definability, iteration, primitive recursion, general recursion and oracle definability. Classify candidate generator extensions at each level. Prevent 'new generator' claims that vanish when the allowed closure schema changes.

### P157 — MINIMAL GENERATOR EXTENSION MDL
Study DeltaGamma_min under explicit coding languages and MDL/Kolmogorov-inspired costs. Quantify encoding sensitivity and find only invariants that survive admissible recodings within bounded overhead.

### P158 — GENERATOR NOVELTY UNDER MACROS
Construct macro systems that make a complex lower-level operation one symbol upstairs. Decide whether this is Resource Rise, R-Rise or G-Rise_L under different languages. Turn the ambiguity into an explicit classification algorithm.

### P159 — ORACLE / EXTERNAL CONTEXT RED TEAM
Test G-Rise claims when the upper generator is allowed to call an oracle, database or lower-level simulator. Distinguish genuinely internal upper dynamics from hidden delegation back to the microlevel.

### P160 — CROSS-DOMAIN GENERATIVITY BENCHMARK
Apply R-Rise/Resource-Rise/G-Rise_L classification to automata, algebraic quotients, Markov aggregation, LTI model reduction, CA coarse-graining and program macros. Search for a single taxonomy that does not misclassify established cases.
