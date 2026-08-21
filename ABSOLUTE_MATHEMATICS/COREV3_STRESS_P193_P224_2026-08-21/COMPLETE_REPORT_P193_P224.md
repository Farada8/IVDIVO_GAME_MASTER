# COMPLETE REPORT — P193–P224

## Status distribution

- **COUNTEREXAMPLE: 4**
- **DERIVED: 22**
- **KNOWN: 5**
- **NOVELTY_UNVERIFIED: 1**

## Sequential results

| ID | Topic | Status | Core result |
|---:|---|---|---|
| 193 | PROMOTION RECORD FIELD-INDEPENDENCE AUDIT | **DERIVED** | Promotion Record separates behavioral/context validity, dynamic closure, sufficiency/autonomy, and hierarchy/generativity failure axes. |
| 194 | STOCHASTIC PROMOTION = LUMPABILITY / BISIMULATION? | **KNOWN** | Exact finite-Markov aggregation belongs to established lumpability/bisimulation theory. |
| 195 | UNIT-INVARIANT CLOSURE DEFECT | **DERIVED** | Raw closure error is unit-dependent; normalized metrics are required for cross-scale comparison. |
| 196 | APPROXIMATE STOCHASTIC ROLLOUT | **DERIVED** | Near-lumpability produces nonzero multistep error whose behavior depends on mixing/contraction. |
| 197 | INTERVENTION-PRESERVING STATE | **DERIVED** | Passive observational equivalence can fail once actions/interventions are admitted. |
| 198 | CONTEXT FAMILY LATTICE | **DERIVED** | Adding contexts refines/preserves behavioral partitions and can increase required state size. |
| 199 | SIGNATURE EXTENSION REVOCATION | **COUNTEREXAMPLE** | A quotient valid for one operation signature can fail after a capability/operation extension. |
| 200 | NO FINITE UPPER STATE CERTIFICATE | **DERIVED** | Reactor must allow NO FINITE UPPER STATE. |
| 201 | HANKEL / PSR RANK AS STATE DIMENSION CONTROL | **KNOWN** | Predictive/Hankel rank is an established dynamical-state comparator. |
| 202 | HIDDEN STATE COUNT IS NOT ORDER | **DERIVED** | Hidden/ontological component count is not minimal predictive state complexity. |
| 203 | CAUSAL STATE / PSR AUTHORITY MERGE | **KNOWN** | Minimal predictive-state core overlaps established causal-state/PSR theory. |
| 204 | RECURSIVE STATE UPDATE REQUIREMENT | **DERIVED** | Online autonomous state requires recursive update or an explicit estimator/filter state. |
| 205 | BEHAVIORAL UNIQUENESS VS COORDINATE UNIQUENESS | **KNOWN** | Minimal behavior can be unique up to isomorphism/similarity without unique coordinates. |
| 206 | MICRO/HISTORY SUFFICIENCY AS CONDITIONAL TEST | **NOVELTY_UNVERIFIED** | Strong Promotion gate can require low extra future information from history and microstate conditional on macrostate. |
| 207 | FINITE-DATA FALSE SATURATION | **DERIVED** | Finite sample/horizon saturation cannot establish finite true predictive state. |
| 208 | STATE DISCOVERY PRIORITY DECISION | **DERIVED** | Direct predictive-state reconstruction should be primary comparator; hand-designed states remain candidates. |
| 209 | LOCALITY-RELATIVE ORDER | **DERIVED** | Locality can create nontrivial construction depth even when unrestricted depth is one. |
| 210 | BOUNDED-ARITY ORDER | **DERIVED** | Bounded arity yields admissibility-relative depth ceil(log_b N). |
| 211 | RESOURCE-BUDGET DEPTH | **DERIVED** | Resource constraints can create major effective depth/reach differences without changing mathematical reachability. |
| 212 | COMPOSITION-CLOSURE AUTO-REJECTION | **DERIVED** | Endpoint depth >1 is invalid if admissible maps are closed under well-typed composition. |
| 213 | ORDER SPECTRUM INSTEAD OF SCALAR | **DERIVED** | Order should be represented as a spectrum/vector over admissibility classes. |
| 214 | ADMISSIBILITY COORDINATE INVARIANCE | **DERIVED** | Admissibility-based order should respect declared irrelevant symmetries/coordinate changes. |
| 215 | CONTEXT VS ADMISSIBILITY SEPARATION | **DERIVED** | K determines what states may merge; A determines which construction paths count. |
| 216 | ROBUST BOUNDARY DEFINITION | **DERIVED** | Robust boundary requires stability across contexts/admissibility plus NO-BOUNDARY controls. |
| 217 | R-RISE FORMALIZATION | **KNOWN** | R-Rise is quotient/factor/abstraction taxonomy, not new extensional generativity. |
| 218 | RESOURCE RISE FORMALIZATION | **DERIVED** | Resource Rise is distinct from representational and generator novelty in cost-bounded problems. |
| 219 | G-RISE LANGUAGE RELATIVITY | **COUNTEREXAMPLE** | Same operator changes primitive/definable status when language admits multiplication/iteration. |
| 220 | DEFINABILITY CLOSURE HIERARCHY | **DERIVED** | Novelty can disappear as iteration/recursion/oracle closure is strengthened. |
| 221 | MINIMAL GENERATOR EXTENSION ENCODING RED TEAM | **COUNTEREXAMPLE** | Exact minimal generator extension is vocabulary/encoding dependent. |
| 222 | ORACLE / MICRO-DELEGATION RED TEAM | **DERIVED** | Macro generator that delegates essential transitions to micro simulator is not autonomous under this Promotion criterion. |
| 223 | GENESIS REWRITE NONCONFLUENCE | **COUNTEREXAMPLE** | Unique genesis normal form cannot be assumed without confluence. |
| 224 | FEEDBACK MODULES + GRAND SYNTHESIS v4 | **DERIVED** | Core decomposes into Semantic State, Dynamic Closure, Construction/Hierarchy, Generativity/Genesis. |

## Fresh quantitative anchors

- Exact Markov lumpability defect: **0.0**.
- Matched perturbed defect: **0.025000000000000133**.
- Perturbed projected-vs-macro TV rollout: `{1:0.0041667,2:0.0067208,4:0.0088380,8:0.0096478,16:0.0097236}`.
- Unit-rescaling: raw RMSE changes by 1000× while NRMSE stays ≈ **0.1991**.
- Intervention counterexample: passive states same under action 0, separated by action 1.
- Context refinement: one independent bit-context gives 2 classes; two give 4 singleton classes.
- Signature-extension counterexample witness on Z4 parity quotient: `(0,2,h(0)=0,h(2)=1)`.
- 4 hidden HMM states have finite Hankel rank **2** in the fixture.
- Predictive class growth: regular mod-3 stays `3,3,3,3,3`; nonregular `a^n b^n` grows `5,9,17,33,65`.

## Synthesis

The program now separates four different questions that were mixed in the original notion of order:
1. **What counts as the same state?**
2. **Does the reduced state evolve autonomously?**
3. **How hard is construction under declared constraints?**
4. **Is there genuine generator novelty relative to a declared definability language?**

Formal Core v4 records these as S/D/H/G modules rather than one scalar order.
