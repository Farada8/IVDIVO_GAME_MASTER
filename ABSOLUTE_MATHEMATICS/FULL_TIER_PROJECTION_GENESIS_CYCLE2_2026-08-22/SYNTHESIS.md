# FULL TIER PROJECTION GENESIS — CYCLE2 SYNTHESIS

## Main result

A lossless "absolute projection" does not create new information. It can still create a new working tier if it preserves all declared future tasks/interventions while reducing representation/construction cost or changing the admissible operation language.

The correct object is therefore:

**MINIMAL SUFFICIENT INVARIANTS relative to (G, Tasks, Interventions)**,

where G is the declared symmetry group.

## Benchmark result

- Fully symmetric target: VIETA hidden RMSE ≈ 1.38e-13; SUM and FULL linear raw-coordinate models fail because the target contains symmetric pair interactions not exposed as linear coordinates.
- Fully role-sensitive target: FULL hidden RMSE ≈ 4.87e-13; VIETA hidden RMSE ≈ 1.80 and therefore loses required role identity.
- Block-symmetric target: BLOCK_VIETA hidden RMSE ≈ 2.76e-13; full S4 symmetry loses which values belong to which block.

This establishes the expected hierarchy: full peer symmetry permits a full permutation-invariant projection; role-sensitive tasks require labels; intermediate block symmetry permits blockwise invariants.

## Viète dynamics

For `V(x,y)=(x+y,xy)`, the full line `(x,0)` is fixed. The transverse multiplier is `x`, so `|x|<1` is locally attracting normal to the line and `|x|>1` is repelling. There are no nontrivial real 2-cycles.

The recursion can therefore stabilize or diverge while still adding no exogenous information.

## Self-improvement adversarial fixture

A co-moving training manifold makes the role-sensitive target look almost like a function of SUM: SUM train RMSE ≈ 0.00123. On hidden independent-role states its RMSE rises to ≈ 1.79. FULL remains ≈ 3.9e-06 hidden. The naive smallest-dimensional train-fit policy chooses SUM; the evidence-first hidden-role policy chooses FULL.

Disposition: `LOCAL_KEEP`, no global promotion.

## Next target

Learn or declare a subgroup `G <= S_n`, then search for the smallest G-invariant projection sufficient for required tasks and interventions. This is the most precise current mathematical interpretation of "absolute elements of the next tier".

Strong genesis remains reserved for cases where something beyond deterministic reparameterization appears: external input, a new primitive/operation language, resource-relative generativity, or a reproducible residual outside the old closure.
