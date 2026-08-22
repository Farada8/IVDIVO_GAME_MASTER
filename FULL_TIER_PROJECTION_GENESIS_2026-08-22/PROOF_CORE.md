# Proof Core

## Formal tier
For `n` peers, the nonempty subset tier has rank sizes `C(n,k)` and total `2^n-1`.

## Semantic quotient
For a synthesis map `A_F`, identify subsets `S~T` when `A_F(S)=A_F(T)`. Hence semantic size is `|Im A_F| <= 2^n-1`.

## Additive repeated promotion
Let the original peers be formally independent generators `e_i`, let `u=sum e_i`, and promote whole peers `g_j=2^(j-1)u`, j=1..k. Any subset of the `n+k` peers has coefficient vector `epsilon+t*1`, with `epsilon in {0,1}^n` and `t in {0,...,2^k-1}`. Equality between two such representations can only be identical, or the boundary relation `(epsilon=1,t)=(epsilon=0,t+1)`. Therefore distinct nonzero semantic vectors are

`N_sem(n,k)=2^(n+k)-2^k`

and exact formal redundancy is

`N_red(n,k)=2^k-1`.

The implementation exhaustively checks this formula for n=2..5 and k=1..4.

## Symmetric absolute projection
For scalar unlabeled peers, `P_V=(e1,...,en)` with elementary symmetric polynomials. By Viète,

`prod_i(z-x_i)=z^n-e1*z^(n-1)+e2*z^(n-2)-...+(-1)^n en`,

so the projection determines the peer multiset up to permutation. This is classical mathematics; the project uses it as a candidate lossless symmetric projection between Genesis tiers.

## Linear no-free-compression bound
If the full tier is an arbitrary free vector in `R^(2^n-1)`, an exact linear projection to `R^m` must have `m >= 2^n-1`. Compression therefore requires additional structure such as symmetry, sparsity, known synthesis law, or task-relative equivalence.

## Claim ceiling
The Boolean lattice, elementary symmetric functions and Viète map are known. The repeated-promotion redundancy formula is project-derived and novelty-unverified. The main engineering object is the three-stage distinction `FORMAL TIER -> SEMANTIC QUOTIENT -> CERTIFIED PROJECTION`.
