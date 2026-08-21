# COMPLETE REPORT — P225–P256

## Status distribution

- **COUNTEREXAMPLE: 3**
- **DERIVED: 21**
- **KNOWN: 6**
- **NOVELTY_UNVERIFIED: 2**

## Sequential verdicts

| ID | Topic | Status | Strongest result |
|---:|---|---|---|
| 225 | INTERVENTIONAL CAUSAL-STATE CONTROL | **DERIVED** | A passive predictive partition can be too coarse for control: admissible interventions can split states that are passive-future equivalent. |
| 226 | MINIMAL CONTEXT BASIS | **DERIVED** | A full context family can have smaller nonunique bases that induce exactly the same behavioral partition. |
| 227 | CONTEXT-STATE FRONTIER | **DERIVED** | Richer context families can increase required macro-state size, creating a context-complexity/state-size frontier. |
| 228 | ACTION-ABSTRACTION HOMOMORPHISM | **KNOWN** | State/action abstraction with exact behavioral preservation is established through MDP homomorphisms and bisimulation-style abstractions. |
| 229 | OBSERVATION-MAP DEPENDENCE | **DERIVED** | Minimal behavioral state is observer-relative: changing only the observation map can coarsen or refine the predictive partition even when latent dynamics are unchanged. |
| 230 | CONTEXT EXTENSION STRESS | **DERIVED** | A valid Promotion can be revoked by one newly admitted context; the first separating context is a compact revocation certificate. |
| 231 | PASSIVE VS CONTROLLED PSR | **KNOWN** | Controlled PSRs represent state by action-conditioned predictions; a predictive state learned only under one fixed behavior policy need not transfer to new actions. |
| 232 | SEMANTIC STATE GRAND RED TEAM | **NOVELTY_UNVERIFIED** | Most of Semantic State Module is already covered by causal states, PSRs, bisimulation/homomorphism and sufficient-statistic ideas; the remaining project-specific residue is the explicit context-basis/frontier/revocation protocol inside a larger Promotion audit. |
| 233 | CONTRACTIVE STOCHASTIC ERROR THEOREM | **DERIVED** | Under contraction, repeated approximate stochastic aggregation errors are bounded by a geometric series rather than growing without limit. |
| 234 | NONCONTRACTIVE ERROR COUNTEREXAMPLE | **COUNTEREXAMPLE** | Arbitrarily small one-step stochastic defect does not imply useful long-horizon Promotion when contraction fails. |
| 235 | METRIC INVARIANCE BENCHMARK | **DERIVED** | Closure metrics have different invariance classes; raw RMSE is not unit-invariant, while variance-normalized RMSE is invariant to simple scalar rescaling in the tested fixture. |
| 236 | APPROXIMATE BISIMULATION CROSSWALK | **KNOWN** | Approximate Promotion in stochastic transition systems substantially overlaps approximate probabilistic bisimulation, bisimulation metrics and near/quasi-lumpability. |
| 237 | RESIDUAL HISTORY CMI | **DERIVED** | Conditional mutual information is a stronger nonlinear diagnostic of missing history than residual autocorrelation alone in discrete controls. |
| 238 | RESIDUAL MICRO CMI | **DERIVED** | Conditional micro-information cleanly distinguishes an insufficient coarse state from a sufficient augmented state in a planted control. |
| 239 | RECURSIVE FILTER STATE | **KNOWN** | Belief state is an exact recursively updateable sufficient state for a known POMDP/HMM model, providing a canonical positive control for recursive state. |
| 240 | DYNAMIC CLOSURE GRAND RED TEAM | **DERIVED** | The Dynamic Closure module can be reduced to five mandatory elements: behavioral defect metric, horizon/stability, history sufficiency, micro sufficiency, and recursive updateability. |
| 241 | HANKEL RANK RECOVERY SUITE | **DERIVED** | Finite Hankel rank is recoverable exactly in noiseless planted low-rank controls and is therefore a useful positive benchmark for predictive dimension. |
| 242 | FALSE LOW-RANK FINITE DATA | **COUNTEREXAMPLE** | Singular-value thresholding can falsely declare low predictive rank when real singular values are small relative to an arbitrary numerical/statistical threshold. |
| 243 | HIDDEN-STATE REDUNDANCY FAMILY | **DERIVED** | Hidden-state count can grow arbitrarily while predictive rank stays fixed. |
| 244 | MINIMAL REALIZATION CROSS-DOMAIN | **KNOWN** | Minimality and uniqueness are domain-specific established concepts: DFA minimal states, predictive/causal states, LTI minimal realizations and probabilistic quotients have different assumptions and equivalence notions. |
| 245 | STATE ISOMORPHISM TEST | **DERIVED** | Two coordinate representations can encode the same state exactly under an invertible transformation, while a collapsed noninvertible representation cannot. |
| 246 | CANONICAL REPRESENTATIVE COST | **COUNTEREXAMPLE** | Coordinate-based canonicalization costs are not invariant under invertible rescaling and therefore cannot define an intrinsic canonical representative by themselves. |
| 247 | STATE DIMENSION VS CONTEXT | **DERIVED** | Minimal required state size is monotone under exact context refinement and can jump discontinuously when a new independent context is admitted. |
| 248 | STATE-DIMENSION GRAND RED TEAM | **DERIVED** | No single state dimension is defensible as 'absolute' across changing context, model class, estimator, tolerance and finite-data horizon. |
| 249 | LOCALITY DEPTH ON GRAPHS | **DERIVED** | Locality yields graph-dependent lower bounds on construction depth proportional to graph distance/communication radius. |
| 250 | ARITY-LOCALITY COMBINED DEPTH | **DERIVED** | When bounded arity and locality both apply, construction depth is at least the maximum of the separate arity and locality lower bounds. |
| 251 | COMMUNICATION-COMPLEXITY ORDER | **KNOWN** | Communication complexity supplies an established resource axis showing that a tiny final macro output can require large distributed information exchange. |
| 252 | MEMORY-BUDGET ORDER | **DERIVED** | Working-memory constraints can create a separate resource hierarchy even when the final output is tiny. |
| 253 | TYPE-SAFE NONFLATTENABILITY | **DERIVED** | Typed staged depth can be nontrivial when admissibility counts primitive typed transformations rather than their composites. |
| 254 | ADMISSIBILITY NATURALNESS SCORE | **NOVELTY_UNVERIFIED** | A useful admissibility-naturalness audit can combine external grounding, invariance, resource interpretation and non-ad-hocness, but a scalar 'naturalness score' is heuristic rather than mathematics. |
| 255 | ORDER SPECTRUM PARETO DOMINANCE | **DERIVED** | Order spectra are generally partially ordered: different tasks/hierarchies can trade locality, arity and communication costs so neither dominates. |
| 256 | HIERARCHY GRAND RED TEAM | **DERIVED** | The Hierarchy module survives Red Team only as an application-relative resource/construction object; no evidence supports a context-free intrinsic scalar order. |

## Fresh quantitative anchors

- History sufficiency control: CMI missing-memory=0.3021 bits; after sufficient 2-step state=2.11e-05 bits.
- Micro sufficiency control: missing micro CMI=0.7144 bits; irrelevant micro after full state=1.09e-05 bits.
- Recursive HMM belief filter vs full-history recomputation max discrepancy=0.0.
- Hidden-state redundancy: 2,4,8,16 hidden states all retained predictive Hankel rank 2.
- State isomorphism: invertible transform recovery RMSE=1.08e-15; collapsed representation reconstruction RMSE=0.5783.
- Minimum context basis: size 3 with 4 distinct minimum bases.
- Noncontractive error fixture: one-step epsilon=0.01; TV at t=500=0.9934.
- Graph-locality lower bounds: path32 diameter 31; grid6x6 diameter 10; binary-tree-depth4 diameter 8; complete32 diameter 1.

## Main conclusion

The project now has strong evidence that **state complexity and construction complexity are different mathematical objects**. Semantic state is determined by what futures/interventions must be preserved; construction depth is determined by the admissible architecture/resources. Mixing the two under one scalar `order` caused many of the earlier ambiguities.

Formal Core v5 therefore separates Semantic State, Dynamic Closure, Construction Complexity Spectrum and Generativity/Genesis. The next research phase should attack the interfaces between these modules rather than invent more scalar order metrics.
