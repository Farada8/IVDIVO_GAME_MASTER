# ABSOLUTE MATHEMATICS ENGINE — NEXT 64 (AMSI-33…AMSI-96)

## A — Recursive Predictive State
AMSI-33 Belief-state plugin contract — implement a finite HMM/POMDP belief-state adapter as a ground-truth recursively updateable state plugin.
AMSI-34 Controlled PSR ground-truth fixture — create controlled PSR fixtures with planted system-dynamics rank and exact action-observation tests.
AMSI-35 Recursive update consistency gate — compare online recursive state updates to full-history recomputation and fail on divergence.
AMSI-36 Passive-to-controlled revocation — detect when passive state becomes invalid under new intervention contexts.
AMSI-37 NO-FINITE-STATE rank growth — implement horizon/sample rank-growth diagnostics that can return NO_FINITE_STATE.
AMSI-38 State isomorphism plugin — compare learned states up to permutation/linear/nonlinear invertible transforms.
AMSI-39 Context-basis approximation — scalable approximate context-basis search with epsilon/revocation checks.
AMSI-40 Recursive-state Red Team — attack offline summaries that predict well but cannot update recursively.

## B — Scalable Promotion Search
AMSI-41 Partition refinement solver — replace Bell-number enumeration where exact refinement applies.
AMSI-42 Branch-and-bound partition search — use lower bounds on defect/state count.
AMSI-43 MILP/SAT feasibility prototype — encode finite Promotion feasibility under fixed block count where practical.
AMSI-44 Phase-boundary scanner — scan epsilon and report intervals where optimal state count changes.
AMSI-45 Context-extension incremental update — update quotient when one context is added.
AMSI-46 Signature-extension incremental audit — revalidate congruence under new operations.
AMSI-47 Candidate ensemble search — retain multiple near-optimal partitions for later tests.
AMSI-48 Scalability benchmark — compare reference/scalable solvers as state count grows.

## C — Approximate Closure & Statistics
AMSI-49 Metric registry — typed TV/Wasserstein/JS-KL/normalized-RMSE/operator metrics.
AMSI-50 Metric invariance tests — test unit/rescaling/relabeling invariances.
AMSI-51 Dobrushin kernel bound — finite Markov contraction bound with explicit discrepancy semantics.
AMSI-52 Mixing-time horizon policy — derive horizons from mixing/metastability rather than arbitrary length.
AMSI-53 CMI uncertainty engine — permutation/bootstrap calibration for history/micro gates.
AMSI-54 Continuous CMI benchmark — compare kNN/neural/discretized estimators on planted nonlinear states.
AMSI-55 Confidence-aware Promotion gate — HOLD when uncertainty intervals cross thresholds.
AMSI-56 Nonstationarity detector — detect drift/regime invalidating a stationary macro-generator.

## D — Construction / Resource Engineering
AMSI-57 Communication-cost adapter.
AMSI-58 Streaming-memory adapter.
AMSI-59 Time-space Pareto surface.
AMSI-60 Local graph-depth solver.
AMSI-61 Arity-locality interaction.
AMSI-62 Admissibility symmetry checker.
AMSI-63 Post-hoc hierarchy detector.
AMSI-64 Construction spectrum reporter.

## E — Generativity / Genesis
AMSI-65 Finite term definability checker.
AMSI-66 Closure-schema ladder: finite-term / iteration / recursion / oracle.
AMSI-67 Conservative extension audit.
AMSI-68 Micro-delegation budget.
AMSI-69 Typed genesis validator.
AMSI-70 SCC genesis module.
AMSI-71 Critical-pair checker for nonconfluence.
AMSI-72 Genesis complexity Red Team.

## F — Self-Improvement Engine
AMSI-73 Archive persistence contract — persist lineage hashes, evidence and failure reasons.
AMSI-74 Current-score baseline — compare archive selection with pure hill climbing.
AMSI-75 Random-parent baseline.
AMSI-76 Descendant-potential calibration — test whether proxy predicts useful descendants.
AMSI-77 Diversity metric — prevent archive collapse to one lineage.
AMSI-78 Mutation budget — cap files/functions/tokens/tools changed.
AMSI-79 Cold extraction regression.
AMSI-80 Automatic rollback fixture.

## G — Evidence / Authority / Operations
AMSI-81 SI-0012 live bridge pilot.
AMSI-82 Bridge version drift fixture.
AMSI-83 Transaction-guarded math state write.
AMSI-84 Evidence-class claim cap.
AMSI-85 Claim supersession graph.
AMSI-86 Source fingerprint manifest.
AMSI-87 Cross-dialog handoff contract.
AMSI-88 Starvation guard — stop meta-research when real experiment/production has higher expected information gain.

## H — Science / Novelty / Release
AMSI-89 Prior-art map exact components.
AMSI-90 Integrated protocol novelty audit.
AMSI-91 Theorem formalization pack.
AMSI-92 Cross-domain benchmark pack.
AMSI-93 Scientific reviewer packet.
AMSI-94 Publication contribution decision.
AMSI-95 Formal Core v6 minimalization.
AMSI-96 Release gate v1.

## Priority front
AMSI-33, AMSI-41, AMSI-49, AMSI-73, AMSI-81, AMSI-89.

These are evidence-derived engineering/research run cards. They are not authorization to bypass authority gates or to promote the engine to CURRENT automatically.