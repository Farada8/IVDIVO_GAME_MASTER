# T22–T25 — MINIMAL ABSOLUTE ELEMENTS

## T22 — Five non-equivalent size notions

For a tier built from n scalar peers, the following quantities are different and must not be substituted:

1. Formal relation count: N_formal = 2^n - 1.
2. Relation-type count under symmetry: N_type(G) = |B_n* / G|.
3. Universal invariant/separating generator count.
4. Task/intervention-sufficient feature count N_task(G,T,I).
5. Intrinsic state dimension.

There is no general equality between these five numbers.

---

## T23 — Task sufficiency can be strictly smaller than relation-type count

Cycle benchmark for four peers:

- Full S4 symmetry: 15 formal relations -> 4 relation types -> 2 task-sufficient orbit features for T=e1+0.7e2.
- Block symmetry S2 x S2: 15 -> 8 -> 4.
- Labeled roles: 15 -> 15 -> 4 singleton coordinates for the tested role task.
- Cycle-graph task: discovered D4 symmetry gives 15 -> 5 -> 1 adjacent-pair orbit feature.

Therefore N_task is a property of the declared task/intervention family, not of the tier alone.

---

## T24 — Adding required tasks cannot reduce the minimum sufficient feature count

Let T1 be a subset of T2. Every representation sufficient for all tasks in T2 is also sufficient for T1. Hence the feasible representation family for T2 is a subset of that for T1.

Therefore:

N_task(G,T1,I) <= N_task(G,T2,I).

Cycle control:
- one S4-symmetric task using e1,e2: minimum 2;
- after adding a triple-sum task e3: common minimum 3.

This is a monotonicity result, not a novelty claim.

---

## T25 — Universal state reconstruction and task sufficiency are different goals

For four unlabeled scalar peers under S4, the full multiset can be reconstructed from (e1,e2,e3,e4). Thus four invariant coordinates form a classical universal state representation up to permutation.

But a single downstream task may require only e1,e2, or even one invariant.

Therefore:

minimal absolute elements for a task != minimal coordinates for universal state reconstruction.

Two promotion contracts are required:

### UNIVERSAL PROMOTION
Preserve all distinctions needed to reconstruct the declared semantic quotient.

### TASK PROMOTION
Preserve only a preregistered task/intervention family.

A TASK projection can be smaller but becomes invalid when future tasks expand.

---

# Absolute Element Certificate v1

A next-tier promotion records:

- source peer count n;
- formal relation count 2^n-1;
- discovered/declared symmetry group G;
- relation orbit count;
- target mode: UNIVERSAL or TASK;
- invariant/separating generator family if universal;
- declared task/intervention family if task-specific;
- selected absolute elements;
- hidden symmetry-breaking tests;
- reconstruction or task residual;
- intrinsic-dimension estimate;
- resource/complexity gain;
- invalidation rule when G, tasks, or interventions change.

This makes "absolute element" a testable contract rather than a fixed formula.
