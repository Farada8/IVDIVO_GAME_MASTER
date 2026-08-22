# T22–T25 — MINIMAL ABSOLUTE ELEMENTS

## T22 — Five non-equivalent size notions

For a tier built from n scalar peers, the following quantities are different and must not be substituted:

1. Formal relation count: `N_formal = 2^n - 1`.
2. Relation-type count under symmetry: `N_type(G) = |B_n* / G|`.
3. Universal invariant/separating generator count.
4. Task/intervention-sufficient feature count `N_task(G,T,I)`.
5. Intrinsic state dimension.

There is no general equality between these five numbers.

## T23 — Task sufficiency can be strictly smaller than relation-type count

Cycle benchmark for four peers:

- Full `S4` symmetry: `15 -> 4 -> 2` for `T=e1+0.7e2`.
- Block symmetry `S2 x S2`: `15 -> 8 -> 4`.
- Labeled roles: `15 -> 15 -> 4` singleton coordinates for the tested role task.
- Cycle-graph task: discovered `D4` symmetry gives `15 -> 5 -> 1` adjacent-pair orbit feature.

Therefore `N_task` is a property of the declared task/intervention family, not of the tier alone.

## T24 — Task-family monotonicity

Let `T1 subset T2`. Every representation sufficient for all tasks in `T2` is also sufficient for `T1`. Hence:

`N_task(G,T1,I) <= N_task(G,T2,I)`.

Cycle control: one S4-symmetric task using `e1,e2` has minimum 2; after adding a triple-sum task `e3`, the common minimum becomes 3.

## T25 — Universal state reconstruction vs task sufficiency

For four unlabeled scalar peers under `S4`, the full multiset can be reconstructed from `(e1,e2,e3,e4)`, a classical universal representation up to permutation. But a single downstream task may require only `e1,e2`, or one invariant.

Therefore:

`minimal task absolute elements != minimal universal state coordinates`.

### UNIVERSAL PROMOTION
Preserve all distinctions needed to reconstruct the declared semantic quotient.

### TASK PROMOTION
Preserve only a preregistered task/intervention family.

A TASK projection can be smaller but becomes invalid when future tasks expand.

## Absolute Element Certificate v1

A next-tier promotion records:

- source peer count;
- formal relation count;
- symmetry group;
- relation-orbit count;
- promotion mode;
- invariant/separating generator family if universal;
- declared task/intervention family if task-specific;
- selected absolute elements;
- hidden symmetry-breaking tests;
- reconstruction/task residual;
- intrinsic-dimension estimate;
- resource/complexity gain;
- invalidation rule when symmetry/tasks/interventions change.
