# GENESIS DYNAMICS — CYCLE2 PROOF LAYER

## G6 — Finite Associative Peer-Genesis Is Eventually Periodic

Let `(S,∘)` be a finite semigroup and `D(s)=s∘s=s²`. By associativity, `D^k(s)=s^(2^k)`. Because `S` is finite, the sequence `s,s²,s⁴,s⁸,...` repeats. Therefore every diagonal peer-genesis orbit is eventually periodic.

**Claim class:** known/derived from standard finite semigroup and power-map dynamics, not new theorem novelty.

## G6b — Exact cyclic-group squaring orbit

If an element has order `m=2^a q` with q odd, then under `D(g)=g²` the exact tail length is `a=v2(m)`. If `q=1`, the orbit reaches identity and stays fixed. If `q>1`, the eventual cycle length is `ord_q(2)`.

## G7 — Diagonal Non-Identifiability No-Go

Peer promotion observes only `D(x)=x∘x`. A general binary operation on an n-element set has `n²` table entries; fixing the diagonal leaves `n^(n²-n)` operations. Under commutativity, fixing the diagonal leaves `n^(n(n-1)/2)` possible tables before further algebraic constraints.

Even commutativity+associativity do not make the diagonal sufficient. Exhaustive n=3 Cycle2 enumeration found 63 labeled commutative associative tables, 12 isomorphism classes, 19 diagonal maps, 10 ambiguous diagonals, and as many as 9 labeled operations sharing one diagonal.

Therefore `D(x)=x∘x` does not identify `∘` without mixed probes or stronger identifiable assumptions.

## G8 — Mixed-Probe Reconstruction

For a finite commutative table, the diagonal plus all unordered mixed probes `a∘b` for `a<b` fully reconstructs the table. The additional entry count is `n(n-1)/2`. For a general noncommutative operation it is `n²-n`.

## G9 — Linearizing-Coordinate Peer Doubling

A classical Aczél-type associativity theorem gives, under appropriate real-interval continuity and strict monotonicity/cancellativity assumptions,

`F(x,y)=phi^{-1}(phi(x)+phi(y))`.

Then peer promotion satisfies

`phi(S_{n+1}) = phi(F(S_n,S_n)) = 2 phi(S_n)`, hence `phi(S_{n+k})=2^k phi(S_n)`.

This is the strongest precise formulation of the original doubling intuition: literal doubling need not occur in the original coordinate, but exact doubling occurs in an additive-generator coordinate for this established class.

Controls:
- addition -> `phi(x)=x`;
- multiplication on positive reals -> `phi(x)=log x`;
- probabilistic OR `x+y-xy` -> `phi(x)=-log(1-x)`;
- `x+y+lambda xy` -> `phi(x)=log(1+lambda x)` where defined.

## G10 — Idempotent operations cannot have a nontrivial strict additive generator

If `F(x,x)=x` for every x and an injective coordinate satisfies `phi(F(x,y))=phi(x)+phi(y)`, then `phi(x)=2phi(x)`, so `phi(x)=0` for every x, contradicting injectivity on a non-singleton domain. Hence everywhere-idempotent operations such as max/min are a distinct Genesis regime.

## Cycle2 split

1. **Diagonal dynamics:** what does `D(x)=x∘x` do?
2. **Operation identification:** what is the off-diagonal law `a∘b`?
3. **Coordinate linearization:** is there a `phi` in which peer promotion becomes exact doubling?

Only task 1 can be solved from pure self-promotion trajectories. Tasks 2 and 3 require mixed or structural evidence.
