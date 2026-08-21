# NEXT 64 PROMPTS — P225–P288

## A — Semantic State / Intervention

### P225 — INTERVENTIONAL CAUSAL-STATE CONTROL
Construct a controlled stochastic process where passive causal states merge histories that action-conditioned futures must split. Compare passive causal states, controlled predictive state and MDP bisimulation. Quantify state-size increase caused by intervention contexts.

### P226 — MINIMAL CONTEXT BASIS
Given a finite family of observation/intervention contexts, find the smallest subfamily inducing the same behavioral partition as the full family. Study uniqueness/nonuniqueness of context bases and complexity of finding them.

### P227 — CONTEXT-STATE FRONTIER
For growing context families compute macro-state size, predictive accuracy and intervention fidelity. Build a Pareto frontier showing the price of asking more questions of the system.

### P228 — ACTION-ABSTRACTION HOMOMORPHISM
Allow both state and action aggregation. Compare project Promotion with MDP homomorphism conditions and test whether action abstraction permits smaller exact upper models than state-only bisimulation.

### P229 — OBSERVATION-MAP DEPENDENCE
Fix dynamics and vary only the observation map. Measure how causal/predictive state partitions change. Determine which state properties are invariant to observation refinement and which are observer-relative.

### P230 — CONTEXT EXTENSION STRESS
Start from a valid quotient and add contexts one at a time until it fails. Record the first separating context and construct a minimal revocation certificate.

### P231 — PASSIVE VS CONTROLLED PSR
On a small POMDP compare an uncontrolled PSR learned under a fixed behavior policy with an action-conditioned PSR. Test policy-transfer failure of passive predictive state.

### P232 — SEMANTIC STATE GRAND RED TEAM
Attack Module I of Formal Core v4. Search for redundancy with causal states, bisimulation, PSR and sufficient-statistic theory. Output KEEP/MERGE/REDEFINE/REJECT and exact literature precedents.

## B — Dynamic Closure / Approximation

### P233 — CONTRACTIVE STOCHASTIC ERROR THEOREM
For finite Markov macro kernels with Dobrushin coefficient alpha<1, derive a multistep total-variation error bound from one-step aggregation defect. Verify on planted near-lumpable chains.

### P234 — NONCONTRACTIVE ERROR COUNTEREXAMPLE
Construct a macro process with one-step defect as small as desired but long-horizon error large because contraction/mixing fails. Use it to falsify any horizon-free epsilon-Promotion claim.

### P235 — METRIC INVARIANCE BENCHMARK
Compare normalized RMSE, Wasserstein, total variation, KL/JS and operator-norm closure defects on rescaled/reparameterized fixtures. State the symmetry/invariance class of each metric.

### P236 — APPROXIMATE BISIMULATION CROSSWALK
Map project approximate Promotion to epsilon/delta probabilistic bisimulation, bisimulation metrics and quasi-lumpability. Identify any exact mathematical residue not already standard.

### P237 — RESIDUAL HISTORY CMI
Estimate conditional mutual information between future and deeper history given candidate macro state on synthetic processes with known Markov order. Calibrate estimator bias before using it as a Promotion gate.

### P238 — RESIDUAL MICRO CMI
Construct systems where coarse state is predictively sufficient and systems where hidden micro detail retains future information. Evaluate conditional micro-information tests and their finite-sample false positives.

### P239 — RECURSIVE FILTER STATE
For a partially observed Markov system, compare full history, belief state and learned recursive predictive state. Require identical/near-identical future laws and online recursive updateability.

### P240 — DYNAMIC CLOSURE GRAND RED TEAM
Attack Module II of Formal Core v4 with exact, approximate, stochastic, nonstationary and partially observed counterexamples. Produce a minimal closure protocol.

## C — State Dimension / Identifiability

### P241 — HANKEL RANK RECOVERY SUITE
Generate processes with planted predictive ranks 1–8. Estimate finite Hankel rank across sample sizes/noise levels. Build confidence rules for finite-rank claims.

### P242 — FALSE LOW-RANK FINITE DATA
Generate infinite-rank or growing-rank processes whose finite Hankel matrices appear low rank. Measure how often standard thresholding falsely declares finite state.

### P243 — HIDDEN-STATE REDUNDANCY FAMILY
Build HMM families with arbitrarily many behaviorally redundant hidden states but fixed predictive rank. Use them to permanently separate latent ontology size from predictive state complexity.

### P244 — MINIMAL REALIZATION CROSS-DOMAIN
Compare minimality/uniqueness notions for DFA, HMM/PSR, LTI, analytic nonlinear systems and Markov quotients. Create a table of exact assumptions behind uniqueness up to isomorphism.

### P245 — STATE ISOMORPHISM TEST
Given two learned macro representations, develop practical tests for whether they encode the same predictive state up to invertible transformation. Include failure cases with nonidentifiability.

### P246 — CANONICAL REPRESENTATIVE COST
Compare canonicalization conventions—ordered classes, minimal basis, balanced realization, MDL encoding—and show which are mathematical invariants versus display/coordinate choices.

### P247 — STATE DIMENSION VS CONTEXT
For one system compute minimal predictive dimension under progressively richer observation/intervention families. Test monotonicity and identify discontinuous jumps.

### P248 — STATE-DIMENSION GRAND RED TEAM
Attack every attempt to call one dimension 'absolute'. Require explicit dependence on context, model class, estimator and tolerance.

## D — Hierarchy / Admissibility

### P249 — LOCALITY DEPTH ON GRAPHS
Generalize the path locality lower bound to arbitrary graphs using graph distance/diameter. Compute exact or bounded depth for trees, grids and expanders under radius-r local composition.

### P250 — ARITY-LOCALITY COMBINED DEPTH
Study construction depth when each node has bounded arity and bounded spatial radius. Derive lower/upper bounds and identify which constraint dominates.

### P251 — COMMUNICATION-COMPLEXITY ORDER
Define admissibility via communication bits/messages between modules. Relate Promotion depth to communication complexity and build examples where state is simple but distributed construction is expensive.

### P252 — MEMORY-BUDGET ORDER
Define admissible transformations with bounded working memory. Compare one-pass, streaming and unrestricted transformations. Determine whether resulting depth/reach adds a useful order-spectrum coordinate.

### P253 — TYPE-SAFE NONFLATTENABILITY
Construct a many-sorted system where staged maps are well typed but the direct composite is not an admissible primitive transformation. Distinguish genuine typing constraints from arbitrary type engineering.

### P254 — ADMISSIBILITY NATURALNESS SCORE
Propose criteria for whether an admissibility class is independently motivated: invariance, physical locality, implementation cost, closure properties and external use. Test against contrived hierarchy-rescue constraints.

### P255 — ORDER SPECTRUM PARETO DOMINANCE
For multiple admissibility classes define dominance between two endpoints/hierarchies using depth, closure defect and resource cost. Study partial rather than total ranking.

### P256 — HIERARCHY GRAND RED TEAM
Attack Module III of Formal Core v4. Try to make every nontrivial depth disappear by changing admissibility while preserving the stated application. Record which boundaries survive.

## E — Generativity / Definability

### P257 — FINITE-TERM VS ITERATIVE G-RISE
Build a library of candidate operators and classify them under finite-term closure, iteration and recursion. Quantify how many 'new generators' disappear as closure language strengthens.

### P258 — CONSERVATIVE LANGUAGE EXTENSION
Define a class of conservative language extensions and ask which G-Rise_L claims survive them. Search for a quotient notion of generator novelty invariant under definitional extension.

### P259 — RESOURCE MACRO VS GENERATOR NOVELTY
Construct operators with huge resource speedup but no new extensional closure. Compare their classification under R-Rise, Resource Rise and G-Rise_L.

### P260 — ORACLE DELEGATION SCALE
Define quantitative autonomy by the number/cost of lower-level oracle calls per macro step. Study thresholds from fully autonomous to fully delegated models.

### P261 — COMPILER EXPANSION TEST
A macro instruction may expand to a long lower-level program. Determine when this is merely compression/resource rise versus when the upper language supports genuinely new closed operations.

### P262 — MINIMAL GENERATOR SET NONUNIQUENESS
Construct algebras/computation systems with multiple inequivalent minimal generating sets of the same size. Use them against claims of a unique generator basis.

### P263 — DEFINABILITY UNDER REPRESENTATION CHANGE
Test whether generator novelty is preserved under computable/isomorphic recodings of state. Identify pathologies where a recoding makes an operation trivial or complex.

### P264 — GENERATIVITY GRAND RED TEAM
Attack Module IV generativity taxonomy. Crosswalk with universal algebra, clone theory, computability and programming-language definability. Preserve only distinctions that survive exact precedent audit.

## F — Genesis / Process Grammar

### P265 — TYPED GENESIS SIGNATURE
Specify formal domains/codomains for closure, quotient, interaction, abstraction, substitution, replication and feedback operators. Reject ill-typed genesis words automatically.

### P266 — PAIRWISE COMMUTATION TABLE
For every pair of genesis operators in the typed signature, search for theorem conditions under which they commute and minimal counterexamples when they do not.

### P267 — GENESIS CRITICAL PAIRS
Use term-rewriting critical-pair analysis to diagnose confluence of genesis rewrite rules. Compute examples where Knuth-Bendix-style completion succeeds or fails.

### P268 — SCC MODULE INTERFACES
For cyclic genesis modules define their input/output interface and internal state equivalence. Test whether replacing an SCC by its interface behavior preserves the condensation-level process.

### P269 — GENESIS PROGRAM MINIMIZATION
Search for the shortest typed genesis program generating a target fixture under a fixed language. Compare exact length, MDL and resource-weighted costs.

### P270 — GENESIS EQUIVALENCE UP TO REWRITE
Define equivalence classes of genesis programs under proved sound rewrite rules. Test transitivity, decidability on finite grammars and nonconfluent cases.

### P271 — FEEDBACK COMPLEXITY BENCHMARK
Compare SCC count, feedback vertex set, recurrence complexity and interface complexity on synthetic process graphs. Determine which metrics correlate with real state/closure difficulty.

### P272 — GENESIS GRAND RED TEAM
Attack the entire genesis-number idea. If process grammar/rewriting theory already supplies the machinery, decide whether a distinct project invariant remains.

## G — Cross-Domain Reactor Benchmarks

### P273 — DFA MINIMIZATION BENCHMARK
Use regular languages with known minimal automata to benchmark exact future-equivalence recovery, canonical quotient size and no-overcompression.

### P274 — NONREGULAR NEGATIVE BENCHMARK
Use multiple nonregular languages/processes to benchmark NO FINITE UPPER STATE decisions and false finite-state rates.

### P275 — MARKOV LUMPABILITY BENCHMARK v2
Generate exact, near and deliberately nonlumpable finite chains with hidden partitions. Recover partitions from samples and calibrate defect uncertainty.

### P276 — MDP BISIMULATION BENCHMARK
Generate controlled finite MDPs with planted state/action abstractions. Compare passive predictive merging with intervention-preserving bisimulation/homomorphism recovery.

### P277 — LTI REALIZATION BENCHMARK v2
Generate nonminimal LTI systems with varying controllability/observability defects and noise. Recover minimal order and similarity-invariant behavior.

### P278 — CELLULAR AUTOMATON BLIND COARSE SEARCH
Blind-search local coarse maps/time rescalings on known factorable and nonfactorable CA fixtures. Score exact closure and false positives.

### P279 — ISING PREDICTIVE-STATE BENCHMARK
Infer predictive states from coarse Ising history without hand-specified domain/wall/regime variables. Compare closure and state dimension with the established hand-designed candidates.

### P280 — FOUR-DOMAIN TRANSFER GATE
Require any claimed general Promotion criterion to pass symbolic, finite stochastic/controlled, continuous realization and spatial dynamical benchmarks with domain-specific reporting.

## H — Novelty / Automation / Publication

### P281 — PROMOTION RECORD LITERATURE AUDIT v2
Search formal methods, control, state abstraction, model reduction, computational mechanics and complex systems for frameworks that already combine the four Formal Core v4 modules.

### P282 — THEOREM PRIOR-ART AUDIT
For every T/C result in Formal Core v4 search exact or stronger prior theorems. Classify as KNOWN, COROLLARY, REPHRASING or POSSIBLY NEW.

### P283 — BENCHMARK REGISTRY MACHINE SCHEMA
Create a machine-readable registry with planted truth, domains, metrics, expected verdict, sample sizes and failure modes. Make it mandatory for new Reactor detectors.

### P284 — CLAIM LEDGER MACHINE SCHEMA
Create an append-only claim ledger linking each theorem/hypothesis to assumptions, evidence, counterexamples, literature precedents, superseded versions and next falsifiers.

### P285 — AUTOMATIC RED-TEAM ROUTER
Encode routing rules: every state claim triggers history/micro/intervention tests; hierarchy triggers flattening; G-Rise triggers language audit; detector triggers NO-boundary nulls.

### P286 — PROOF-ASSISTANT CORE
Formalize the exact context-refinement, congruence, flattening, bounded-arity/locality and semiconjugacy-composition results in a proof assistant or executable formal specification.

### P287 — PUBLISHABLE CORE DECISION
Draft a paper outline using only results that survive theorem prior-art and benchmark audits. If the result is a methodology rather than new mathematics, label it accordingly.

### P288 — GRAND SYNTHESIS v5 + NEXT ROADMAP
After P225–P287, rebuild the smallest Formal Core v5, run Grand Red Team, and generate the next research program with at least 50% negative/control tasks.
