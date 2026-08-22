# FULL TIER / PROJECTION GENESIS

Fresh base main: `8ef8195cb4d3d3d7562aa9d85812dc6d2244a720`.

## Core distinction

For `n` peer elements the formal full relation tier is the nonempty Boolean lattice

`B*_n = {S subset X : S != empty}`

with rank counts `C(n,k)` and total

`|B*_n| = 2^n - 1`.

But a synthesis map `A_F : B*_n -> Y` can identify different subsets. The semantic tier is the quotient `Q_F = B*_n / ~_F`, where `S ~_F T` iff `A_F(S)=A_F(T)`.

Therefore `2^n-1` is a formal maximum, not a guarantee of that many distinct synthesized objects.

## Repeated whole-as-peer theorem

Start from `n` formally independent additive generators and repeatedly promote the current whole as a peer:

`g1=u`, `g2=2u`, `g3=4u`, ..., `gk=2^(k-1)u`, where `u=e1+...+en`.

The formal tier has `2^(n+k)-1` nonempty subsets, but the number of distinct nonzero semantic coefficient vectors is

`N_sem(n,k)=2^(n+k)-2^k`,

so the exact redundancy is

`N_red(n,k)=2^k-1`.

Controls: `(n=2,k=1): 7 formal / 6 semantic`; `(4,1):31/30`; `(4,2):63/60`; `(4,3):127/120`.

Status: project-derived theorem; external novelty unverified.

## Absolute projection candidate

For unlabeled scalar peers define the elementary symmetric projections

`P_V(x1,...,xn)=(e1,...,en)`.

By classical Viète theory,

`prod_i (z-x_i) = z^n - e1 z^(n-1) + e2 z^(n-2) - ... + (-1)^n en`,

so `(e1,...,en)` determines the entire multiset `{x1,...,xn}` up to permutation.

Thus under symmetric/known-law assumptions the full formal tier can be represented by `n` collective coordinates without losing the peer multiset. This does **not** preserve labels or arbitrary relation-specific information.

## Three layers

`Formal Tier -> Semantic Quotient -> Absolute Projection`.

The next Genesis tier should be built from the projection only after an explicit information/behavior preservation test.

## Claim ceiling

Boolean lattices/full simplices, elementary symmetric polynomials and the Viète map are known mathematics. The project-specific contribution here is the integration with repeated whole-as-peer promotion, semantic collision accounting, and fail-closed projection selection. Current status: `ENGINEERING/MATHEMATICAL SYNTHESIS; NOVELTY UNVERIFIED`.
