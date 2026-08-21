# DETAILED RESULTS P225–P232

## P225 — INTERVENTIONAL CAUSAL-STATE CONTROL

**STATUS:** DERIVED

### Strongest supported claim
A passive predictive partition can be too coarse for control: admissible interventions can split states that are passive-future equivalent.

### Evidence
The prior P197 MDP fixture already gives an exact witness: two states behave identically under passive action 0 but action 1 sends them to different observable classes.

### Limitations / Red Team
This is not project novelty; action-conditioned equivalence is standard in bisimulation/MDP abstraction and PSR theory.

### Decision
KEEP interventional context as a mandatory semantic-state gate whenever the state is intended for control.

### Formal anchor
`s~_K t iff every admissible action/test context yields the same observable law`

## P226 — MINIMAL CONTEXT BASIS

**STATUS:** DERIVED

### Strongest supported claim
A full context family can have smaller nonunique bases that induce exactly the same behavioral partition.

### Evidence
Fresh 3-bit fixture: 4 available contexts generate 8 singleton classes, but minimum basis size is 3; four distinct minimum bases were found: [['x1', 'x2', 'x3'], ['x1', 'x2', 'parity'], ['x1', 'x3', 'parity'], ['x2', 'x3', 'parity']].

### Limitations / Red Team
Brute-force basis search is combinatorial and exact only in finite explicit context families.

### Decision
Introduce ContextBasis(K) as an optimization object, but do not assume uniqueness.

## P227 — CONTEXT-STATE FRONTIER

**STATUS:** DERIVED

### Strongest supported claim
Richer context families can increase required macro-state size, creating a context-complexity/state-size frontier.

### Evidence
Fresh fixture: x1 gives 2 classes; x1+x2 gives 4; x1+x2+x3 gives 8. The lower bound on binary state dimension rises 1→2→3 bits.

### Limitations / Red Team
Approximate predictive models may trade state size against tolerated error rather than jump exactly.

### Decision
KEEP a Pareto frontier over context richness, state complexity and preservation defect.

## P228 — ACTION-ABSTRACTION HOMOMORPHISM

**STATUS:** KNOWN

### Strongest supported claim
State/action abstraction with exact behavioral preservation is established through MDP homomorphisms and bisimulation-style abstractions.

### Evidence
Current MDP abstraction literature explicitly distinguishes state abstraction and homomorphism/bisimulation; action aggregation can be part of homomorphic models.

### Limitations / Red Team
Whether action abstraction permits a smaller exact model is application-dependent.

### Decision
MERGE this line with established MDP homomorphism theory; use it as a benchmark, not project novelty.

## P229 — OBSERVATION-MAP DEPENDENCE

**STATUS:** DERIVED

### Strongest supported claim
Minimal behavioral state is observer-relative: changing only the observation map can coarsen or refine the predictive partition even when latent dynamics are unchanged.

### Evidence
The finite context fixtures show distinct partitions from x1, x2 and parity observation maps over the same 3-bit state space.

### Limitations / Red Team
Some invariant latent system properties remain unchanged, but state equivalence defined by observations does not.

### Decision
State claims must declare the observation/context map.

## P230 — CONTEXT EXTENSION STRESS

**STATUS:** DERIVED

### Strongest supported claim
A valid Promotion can be revoked by one newly admitted context; the first separating context is a compact revocation certificate.

### Evidence
In the controlled fixture, passive action 0 validates merging the two source states, while adding action 1 immediately separates them.

### Limitations / Red Team
A different application may never admit the separating context.

### Decision
Store the smallest known separating observation/action when a Promotion is revoked.

## P231 — PASSIVE VS CONTROLLED PSR

**STATUS:** KNOWN

### Strongest supported claim
Controlled PSRs represent state by action-conditioned predictions; a predictive state learned only under one fixed behavior policy need not transfer to new actions.

### Evidence
Predictive-representation literature explicitly defines tests as action-observation sequences; MDP abstraction likewise requires equivalence across actions.

### Limitations / Red Team
The batch did not train a full spectral PSR implementation.

### Decision
Use controlled PSR as the authority comparator for intervention-safe predictive state.

## P232 — SEMANTIC STATE GRAND RED TEAM

**STATUS:** NOVELTY_UNVERIFIED

### Strongest supported claim
Most of Semantic State Module is already covered by causal states, PSRs, bisimulation/homomorphism and sufficient-statistic ideas; the remaining project-specific residue is the explicit context-basis/frontier/revocation protocol inside a larger Promotion audit.

### Evidence
P225–P231 map passive prediction to established predictive-state theory and action-safe equivalence to established controlled abstraction.

### Limitations / Red Team
A literature-wide novelty proof for the combined protocol has not been completed.

### Decision
MERGE core mathematics with established theory; keep only the falsification protocol as a novelty candidate.
