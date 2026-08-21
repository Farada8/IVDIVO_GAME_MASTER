# NEXT RESEARCH PROMPTS P177–P192

## G — Reactor Validation and Scientific Method

### P177 — GROUND-TRUTH BENCHMARK REGISTRY v2
Create a versioned benchmark registry covering exact positive, approximate, negative, adversarial and no-finite-state fixtures. Every detector/theorem candidate must declare which registry entries it is expected to pass/fail before execution.

### P178 — NULL/TARGET COMPATIBILITY AUTOMATION
For every null model, automatically inventory preserved invariants. Reject a null if it preserves the target property by construction or destroys unrelated structure that makes rejection trivial.

### P179 — DETECTOR SELECTIVITY SCORE
Define detector selectivity using true positives, false positives across scales and explicit NO-BOUNDARY controls. Penalize detectors that return a preferred scale on every dataset.

### P180 — PREREGISTERED GATES ENGINE
Before numerical experiments write immutable metrics, thresholds, sample splits, null families, allowed follow-ups and stopping rules. After results, store all deviations explicitly instead of silently retuning.

### P181 — CROSS-DOMAIN TRANSFER GATE
A claimed general Promotion criterion must be calibrated on at least four distinct domains: symbolic, finite stochastic, continuous/LTI and spatial dynamical. Report domain-specific failures rather than averaging them away.

### P182 — FINITE-SIZE / SAMPLE-SIZE AUDIT
Repeat every empirical order/state discovery across system sizes and sample sizes. Distinguish genuine scale behavior from finite-size saturation, estimator bias and data-limited apparent state dimension.

### P183 — UNCERTAINTY CALIBRATION
Attach confidence intervals/posterior uncertainty to closure defects, state dimensions and boundary scores. Test coverage on planted benchmarks. Reject threshold-based discoveries whose uncertainty crosses the decision gate.

### P184 — ADVERSARIAL REACTOR TOURNAMENT
Generate adversarial systems designed to fool each historical detector: spectral gap, predictability, causal locality, domain geometry, one-step PDE fit, memory threshold and regime clustering. Score whether the current Reactor correctly refuses Promotion.

## H — Novelty, Formalization and Grand Red Team

### P185 — TERMINOLOGY CROSSWALK v3
Create an exact table mapping every surviving project term to established concepts: quotient/congruence, contextual equivalence, causal state, PSR, bisimulation, lumpability, semiconjugacy, minimal realization, abstract interpretation, RG and process grammar. Label EXACT/PARTIAL/RESIDUE.

### P186 — PROMOTION RECORD NOVELTY AUDIT
Search mathematics, control, formal methods, complex systems and coarse-graining literature for frameworks already combining state equivalence, closure error, micro/history sufficiency, resource cost, recursive composition and flattenability. Identify true residue.

### P187 — ABSOLUTE NUMBER TERMINOLOGY DECISION
Attempt to remove the term 'absolute number' completely. If every operational property translates into established minimal-state/equivalence language, retire the term. Retain it only if a precise invariant remains that is not branding.

### P188 — THEOREM NOVELTY AUDIT
For each proved/project theorem, search prior literature for exact or stronger results. Mark ORIGINAL-UNKNOWN, KNOWN, COROLLARY or REPHRASING. Do not publish novelty claims without this audit.

### P189 — PUBLISHABLE CORE CANDIDATE
Draft a paper skeleton containing only statements that survived benchmarks and novelty audit. Separate established background, new theorems if any, computational protocol and negative results. If no novel theorem remains, state that explicitly.

### P190 — PROOF-ASSISTANT FORMALIZATION
Formalize the exact quotient/congruence theorem, Promotion composition theorem, context-refinement theorem and admissibility flattening theorem in Lean/Coq/Isabelle or a precise pseudo-formal specification. Use failures to expose hidden assumptions.

### P191 — GRAND RED TEAM v4
Attack Formal Core v3.0 from scratch. For each component output KEEP / MERGE / REDEFINE / REJECT / PROVE, with a smallest counterexample or literature precedent whenever possible. Preserve all negative results.

### P192 — RESEARCH ROADMAP AFTER v4
Using only what survives P129–P191, build the next prioritized research roadmap. Rank questions by falsifiability, theorem value, novelty uncertainty and cross-domain leverage. Require at least half of the highest-priority tasks to be negative/control/Red-Team work.
