# SYNTHESIS + PATH TO GOAL — AMSI-33..64

## What changed

Run1 turned the mathematical formalism into an executable falsification engine.

Run2 attacks the first 32 concrete engineering blockers from the prior backlog.

The biggest improvement is that **“state” is now operationally testable as a recursive object**, not just a quotient or a predictive summary.

### Recursive-state positive control
A finite POMDP belief filter updates exactly online and matches full-history recomputation.

### Recursive-state negative control
A history mean has a collision: two histories share the same summary but the same next symbol produces two different next summaries. Therefore no deterministic update \(U(Z,a)\) can exist for that state definition.

This gives a powerful pair:
- exact positive recursive-state fixture;
- explicit recursive-state no-go witness.

## Scalable solver progress

The exact Markov fixture now has three independent solvers/checks:
- exhaustive reference;
- exact partition refinement;
- output-label-aware bounded branch search.

All agree on \(6\to3\). The branch search used only 13 completed candidates on the fixture.

But general approximate aggregation is still exponential and the MILP/SAT backend is not yet real.

## Exact tolerance boundary

The perturbed fixture yields:

\[
4 \xrightarrow{\varepsilon=0.03} 3 \xrightarrow{\varepsilon=0.05} 2.
\]

The finite phase-boundary theorem explains why the state-count function is piecewise constant: changes can only occur at one of the finitely many candidate defects.

## Statistical discipline improved

A planted conditional-dependence fixture gave \(CMI\approx0.6041\) bits with conditional permutation \(p\approx0.00826\), and bootstrap interval approximately \([0.568,0.649]\).

The engine now returns `HOLD` whenever uncertainty crosses a threshold.

## Approximate-dynamics discipline improved

For the contractive two-state kernel control:

\[
\alpha=0.7,\qquad\delta=0.01,
\]

the geometric error upper bound approaches:

\[
\frac{0.01}{1-0.7}=0.03333\ldots
\]

instead of silently extrapolating one-step accuracy.

## Construction theory improved

Locality is now explicitly source/target/task-relative. Using graph diameter as a universal lower bound is wrong when the output location/task does not require diameter-pair information transfer. Resource complexity remains a Pareto object.

## Proof layer

A new proof pack records 11 statements, including context refinement, point-separating no-compression, tolerance monotonicity, finite phase-boundary theorem, incremental context refinement, signature-extension revocation, contraction error bound, arity/locality lower bounds, and recursive-update collision no-go.

These are derivations under assumptions; novelty is not claimed.

## Self-improvement layer

The local SQLite research harness proved that five jobs can be queued durably, executed immediately one after another, checkpointed as DONE and recovered from persisted state. This removes deliberate hour-scale gaps inside an externally running process.

It does not remove ChatGPT Automation’s product scheduling limit and does not itself call a model. For real continuous AI research, the executor must be an external API agent process.

OpenAI Agents SDK documentation supports agent/tool loops, permits `max_turns=None`, and documents durable integrations such as Dapr, Temporal, Restate and DBOS.

## Parallel system integration

Do not duplicate SI-0012 Cycle4 governor/transaction/evidence infrastructure. Do not import draft code either.

Use capability negotiation:
- CURRENT/MERGED → external generic capability;
- DRAFT/WORKING → fail-closed fallback.

## Current path to goal

1. **Discover state, don’t assume it:** implement sample-based controlled PSR / recursive latent-state discovery.
2. **Scale feasibility search:** build real optimization backends and prove solver certificates against the small exact oracle.
3. **Calibrate uncertainty:** finish kNN/neural CMI and uncertainty-aware approximate closure.
4. **Settle construction interaction:** build exact small schedulers for locality×arity before stronger hierarchy theorems.
5. **Run open-ended method improvement:** compare archive/descendant-potential search against current-score hill climbing, random parent selection and diversity archive.
6. **Cross-domain validation:** survive DFA, nonregular language, Markov/MDP, POMDP/PSR, LTI and spatial/distributed controls.
7. **Novelty decision:** if mathematics reduces to established theories, retain/publish the engineering benchmark/protocol contribution rather than inventing a “new field”.

## Strongest current goal statement

> Build a system that searches for Promotion, tries to falsify it, certifies exactly what survived, and improves its own search methods without self-promoting unsupported claims.
