# DETAILED RESULTS P097–P104

## P097 — ORIGINAL ORDER HYPOTHESIS — AXIOM AUDIT

**STATUS:** DERIVED

### Strongest supported claim
The original whole→unit intuition becomes nontrivial only after specifying equivalence/context, operation compatibility, dynamic closure, recursive reuse and rise type.

### Evidence
The entire reactor history repeatedly produced false positives whenever any one of those gates was omitted: pure compression, predictive blocks, natural domains and wall locality all passed weaker criteria but failed stronger closure/selectivity tests.

### Red Team
This is a framework synthesis, not a theorem saying those gates are uniquely necessary in all mathematical settings.

### Decision
KEEP the intuition only as a motivating schema, not as a definition of order.

### Formal anchor
`S_n --B--> e_(n+1) is a candidate Promotion only relative to contexts and generators.`

## P098 — NUMBER VS NUMERAL REPRESENTATION

**STATUS:** DERIVED

### Strongest supported claim
Numeral base and mathematical value must be strictly separated; changing representation cannot by itself create an order transition.

### Evidence
A value has many numeral encodings; all algebraic/dynamic controls in the project are invariant under relabeling of symbols when the underlying structure is unchanged.

### Red Team
Cardinality/base can matter when it changes the actual state space or allowed operations, but then the cause is structural, not notation.

### Decision
REJECT all order arguments based solely on base-4/base-16 notation changes.

## P099 — WHOLE-TO-UNIT AS QUOTIENT

**STATUS:** KNOWN

### Strongest supported claim
Treating many lower realizations as one upper unit is mathematically a quotient/factor construction once an equivalence relation is specified.

### Evidence
The Z12→Z3 control preserved both addition and multiplication under q(x)=x mod 3; established quotient/congruence theory supplies the general condition.

### Red Team
A quotient may preserve only selected operations/contexts and need not be canonical across context families.

### Decision
MERGE with congruence/contextual-equivalence language.

### Formal anchor
`X_(n+1)=X_n/~_K`

## P100 — CONTEXT-FREE ABSOLUTE NUMBER RED TEAM

**STATUS:** COUNTEREXAMPLE

### Strongest supported claim
A nontrivial context-free compressed 'absolute number' cannot generally preserve every possible behavior: enlarging the admissible context can split any coarse equivalence.

### Evidence
Predictive/contextual equivalence is explicitly context-relative; causal-state and PSR constructions define sufficiency relative to future observations/tests rather than all conceivable properties.

### Red Team
The full microstate is trivially context-complete but destroys the intended compression. Special classes may have canonical minimal realizations up to isomorphism.

### Decision
REDEFINE as A_K^dyn(W), a minimal sufficient representative relative to declared contexts/dynamics.

### Formal anchor
`K1⊂K2 => ~_(K2) refines ~_(K1)`

## P101 — PREDICTIVE STATE CROSSWALK

**STATUS:** KNOWN

### Strongest supported claim
Minimal predictive state is already established in important stochastic-process and controlled-dynamics frameworks.

### Evidence
Causal states are minimal sufficient statistics of histories for futures; PSRs represent state through predictions of observable tests.

### Red Team
The project still needs a crosswalk for interventions, composition, admissibility and G-Rise, which are not exhausted by predictive sufficiency.

### Decision
MERGE predictive-state core with established theory; keep project-specific Promotion record around it.

## P102 — CONGRUENCE / OPERATION COMPATIBILITY GATE

**STATUS:** KNOWN

### Strongest supported claim
Operation-compatible equivalence is mandatory for well-defined quotient operations.

### Evidence
Positive control: Z12→Z3 preserved + and ×. Negative witness for a noncongruence partition on Z3: [0, 1, 0, 1, 0, 2].

### Red Team
Compatibility is signature-dependent: adding a new operation may invalidate an old quotient.

### Decision
PROMOTE congruence/compatibility to a hard gate for algebraic Promotion.

### Formal anchor
`[f(x)] must be independent of representative x.`

## P103 — EXACT DYNAMIC PROMOTION AS FACTOR MAP

**STATUS:** KNOWN

### Strongest supported claim
Exact deterministic dynamic Promotion is naturally a factor/semiconjugacy B∘F=G∘B.

### Evidence
Fresh exact linear factor control had max defect 0.0.

### Red Team
Semiconjugacy guarantees preserved factor dynamics but not minimality, novelty, resource gain or non-flattenable hierarchy.

### Decision
MERGE exact commuting-square language with factor-map/semiconjugacy terminology.

## P104 — APPROXIMATE PROMOTION ERROR PROPAGATION

**STATUS:** DERIVED

### Strongest supported claim
Approximate one-step closure must be paired with a stability bound; small local defect alone does not guarantee long rollout.

### Evidence
Approximate linear control one-step RMSE=0.0997; rollout defects over 1/2/4/8/16 steps were {'1': 0.09972423131487225, '2': 0.16953126204050306, '4': 0.2458211930219575, '8': 0.2619769768330904, '16': 0.15674281920018654}. A recursive Lipschitz bound was also computed.

### Red Team
The simple bound can be loose and depends on the chosen norm/stability constant.

### Decision
KEEP epsilon_delta/horizon-indexed closure defect, not one-step R² alone.

### Formal anchor
`e_(t+1) <= eps + L e_t`
