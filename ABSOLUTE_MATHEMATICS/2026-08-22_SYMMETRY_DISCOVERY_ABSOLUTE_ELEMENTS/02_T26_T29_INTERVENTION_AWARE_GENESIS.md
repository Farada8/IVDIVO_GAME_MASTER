# T26–T29 — INTERVENTION-AWARE GENESIS

## T26 — Operational symmetry group

A symmetry relevant to next-tier promotion must preserve not only current observables/tasks but also the declared intervention structure.

Let `G_T` be the symmetry group of the task family and `G_I` the symmetry group compatible with intervention labels/actions. Define:

`G_operational = G_T ∩ G_I`.

Only permutations in `G_operational` may be quotiented away by a promotion that claims to preserve both observation and intervention capability.

## T27 — More distinguished tasks/interventions can only refine relation types

Let `H <= G` act on the same relation set `R`. Every `G`-orbit is a union of `H`-orbits, because `H` has fewer transformations available to identify points. Therefore:

`|R/H| >= |R/G|`.

So when new tasks/interventions shrink the accepted symmetry group, the number of distinguishable relation types cannot decrease.

## T28 — Four-peer addressability ladder

Start with four observationally interchangeable peers.

- no addressable role: `S4`, group size 24, relation types 4;
- one separately addressable peer: stabilizer `S3`, group size 6, relation types 7;
- two separately addressable peers: `S2`, group size 2, relation types 11;
- all four separately addressable: identity, group size 1, relation types 15.

Hence addressability refines the same formal 15-relation tier through:

`4 -> 7 -> 11 -> 15` relation types.

## T29 — Promotion invalidation/refinement law

A compressed next-tier representation certified under `(G_old, Tasks_old, Interventions_old)` must be reconsidered if new requirements produce a strict subgroup `G_new < G_old` or hidden residual exceeds the certified threshold.

The safe engine must either prove that the old projection remains sufficient under the refined requirement set or add invariants/features until sufficiency is restored.

Therefore next-tier promotion is a versioned capability contract, not permanent ontology.

## Consequence

Absolute elements should be chosen against the strongest intended capability set, not passive observations alone. Otherwise a symmetric compression can erase distinctions required by future control.
