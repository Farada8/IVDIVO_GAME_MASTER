# DETAILED RESULTS P105–P112

## P105 — RESOURCE RISE WITHOUT G-RISE

**STATUS:** DERIVED

### Strongest supported claim
Resource Rise can be exponentially large while extensional generativity remains unchanged.

### Evidence
Successor-only reach under description budget K grows linearly, while a doubling macro reaches 2^K in the toy resource model; the generated natural-number domain itself is not enlarged.

### Red Team
The amount of speedup is cost-model dependent.

### Decision
KEEP Resource Rise as a separate axis from G-Rise.

### Formal anchor
`Reach_K(O_macro) can strictly contain Reach_K(O_base) while Closure is unchanged.`

## P106 — G-RISE DEFINABILITY AUDIT

**STATUS:** INCONCLUSIVE

### Strongest supported claim
G-Rise cannot be made representation-independent without first fixing an admissible generator language or definability notion.

### Evidence
Toy closure with addition vs addition+multiplication reached different bounded-term closures, illustrating that operator novelty and extensional/resource novelty can diverge.

### Red Team
Definability changes if recursion/iteration/macros/oracles are admitted.

### Decision
REDEFINE G-Rise as G-Rise_L relative to an explicit language/admissibility class.

## P107 — MINIMAL GENERATOR EXTENSION CANONICALITY

**STATUS:** COUNTEREXAMPLE

### Strongest supported claim
A canonical minimal generator extension ΔΓ_min generally depends on encoding and primitive vocabulary.

### Evidence
The same operation can be primitive in one language and definable macro/recursion in another; resource complexity also changes under primitive choice.

### Red Team
Kolmogorov-style invariance only controls description differences up to additive constants between universal languages, insufficient for exact finite minimal-extension identity.

### Decision
KEEP minimal extension only relative to a declared coding/language.

## P108 — GENESIS ALGEBRA NONCOMMUTATIVITY

**STATUS:** DERIVED

### Strongest supported claim
Genesis operations are genuinely order-sensitive; closure and quotient need not commute.

### Evidence
Fresh graph witness: Q(C({b}))=['ab'] while C(Q({b}))=['ab', 'c'].

### Red Team
One witness does not determine the best global formalism.

### Decision
KEEP noncommutative genesis words; investigate rewriting/operadic/process-grammar formalisms.

### Formal anchor
`Q∘C != C∘Q`

## P109 — GENESIS DAG VS FEEDBACK

**STATUS:** DERIVED

### Strongest supported claim
A literal DAG cannot represent feedback genesis; SCC condensation provides a canonical DAG of cyclic modules.

### Evidence
Fresh feedback graph condensed to SCCs [['f'], ['d', 'e'], ['a', 'b', 'c']] with DAG edges [[1, 0], [2, 1]].

### Red Team
Internal SCC dynamics still require richer descriptors than a node label.

### Decision
REDEFINE Genesis DAG as process graph + SCC-condensation DAG.

## P110 — SCALAR ORDER VS PARTIAL ORDER / SPECTRUM

**STATUS:** DERIVED

### Strongest supported claim
Generative capability is naturally partially ordered; scalar order is not intrinsic when closures are incomparable.

### Evidence
Fresh set control had A⊄B and B⊄A while both A,B⊂C.

### Red Team
A scalar can still summarize within a chain or after choosing a utility/cost functional.

### Decision
KEEP closure-poset and order-spectrum; reject universal scalar order.

### Formal anchor
`O_A <= O_B iff Closure(A) subseteq Closure(B)`

## P111 — RECURSIVE PROMOTION AND FLATTENING

**STATUS:** DERIVED

### Strongest supported claim
Exact recursive Promotion is flattenable whenever admissible maps are closed under composition.

### Evidence
This follows by composing commuting maps; the previous exact 8→4→2 Markov fixture also admitted direct 8→2 closure.

### Red Team
Nontrivial depth requires independently justified non-composition-closed constraints such as locality, arity or resource bounds.

### Decision
PROMOTE flattening theorem to permanent Red-Team gate.

### Formal anchor
`Ord_A(x,y)∈{0,1,∞} if A is composition-closed.`

## P112 — BOUNDARY DETECTOR SELECTIVITY

**STATUS:** FAILED

### Strongest supported claim
A scale detector that always returns a best score is nonselective evidence for hierarchy.

### Evidence
Fresh smooth unplanted signal produced scale scores {'2':303.7443,'4':139.9030,'8':57.9301,'16':17.4102,'32':4.2089,'64':4.2035} and still had a nominal best scale 2.

### Red Team
This does not invalidate all boundary detectors; it invalidates uncalibrated ranking-as-discovery.

### Decision
Require null/geometry-matched selectivity and rejection option 'NO BOUNDARY'.
