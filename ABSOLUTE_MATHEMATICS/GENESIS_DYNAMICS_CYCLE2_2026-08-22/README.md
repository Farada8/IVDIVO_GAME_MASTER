# GENESIS DYNAMICS — CYCLE2 OPERATOR SEARCH

Status: **WORKING RESEARCH/ENGINEERING CANDIDATE — NOT MERGED**

## Core equation

\[
S_{n+1} = F(S_n,S_n) = D(S_n).
\]

Cycle2 separates:
1. diagonal dynamics `D`;
2. full binary operation `F`;
3. a possible linearizing coordinate `phi`;
4. residual unexplained structure.

## Strongest mathematical synthesis

For the established Aczél class

\[
F(x,y)=\phi^{-1}(\phi(x)+\phi(y)),
\]

peer promotion gives

\[
\boxed{\phi(S_{n+1})=2\phi(S_n)}.
\]

So the original doubling intuition survives exactly in a suitable additive-generator coordinate, under the theorem's assumptions.

## No-go

`D(x)=x∘x` does **not** identify `∘`.

n=3 exhaustive control:
- 63 labeled commutative semigroups;
- 12 isomorphism classes;
- 19 distinct diagonal maps;
- 10 ambiguous diagonals;
- max 9 labeled operations sharing one diagonal.

## Search demonstration

Unknown planted law:

`F(a,b)=a+b+0.37ab`.

Fixed dictionary hidden RMSE: `0.1350`.

Synthesized:
`lambda=0.369926`,
hidden RMSE `0.0098`,
associativity defect at numerical precision.

Prior art downgrades it to **REDISCOVERY**: coordinate-scaled multiplicative formal group law.

## Self-improvement

Diagonal-only operator ID accuracy: `0.667`.
Mixed-probe ID accuracy: `1.000`.

`MIXED_PROBE_BEFORE_OPERATION_ID = LOCAL_KEEP`; global promotion = false.

## Workflow

`Peer trajectory -> D -> regime -> identifiability audit -> mixed probes -> F -> algebraic gates -> linearizer -> hidden residual -> prior art -> application`.

32 sequential Cycle2 tasks completed. 64 next tasks derived.
