# GENESIS RESIDUAL SEARCH ENGINE — SYNTHESIS

## Core principle

A whole becomes a peer:

\[
x_{n+1}=S_n=\sum_{i=1}^n x_i.
\]

Because the new object is included once in the next whole,

\[
S_{n+1}=S_n+x_{n+1}=2S_n,
\]

hence

\[
S_{n+k}=2^kS_n.
\]

This proves growth under repeated peer-promotion.

## But growth is not yet strong genesis

If the promoted whole is already constructible from the old signature,

\[
g\in Cl_\Sigma(X),
\]

then

\[
Cl_\Sigma(X\cup\{g\})=Cl_\Sigma(X).
\]

Therefore sum-promotion is representational genesis, not automatically a new algebraic generator.

## Two search modes

### SYMMETRIC_GENESIS
If peer identity is genuinely exchangeable/permutation-invariant, use the elementary symmetric ladder `e1,...,en`.

### SUBSET_GENESIS
If roles matter, use interaction terms indexed by subsets: `xi`, `xi*xj`, `xi*xj*xk`, ... and search order by order.

## Residual search

For each interaction order k, fit a cumulative model on orders <=k and evaluate held-out residual.
The next-order gain is `Delta_(k+1)=R_k-R_(k+1)`.
If the gain is material and survives hidden/adversarial tests, order k+1 contains useful structure.
If residual remains large after the declared basis is exhausted, that residual becomes a **candidate unknown**, not a discovery claim.

## Experimental results

- `sum`: order 1 sufficient.
- `symmetric_pair`: order 2 collapses test RMSE from about 0.779 to numerical zero.
- `symmetric_triple`: order 3 collapses RMSE from about 0.409 to numerical zero.
- `full_product`: order 4 collapses RMSE from about 0.116 to numerical zero.
- `specific_pair = x1*x2`: symmetric ladder remains around RMSE 0.34, while subset mode reaches ~1e-12 at order 2.
- `mixed`: symmetric ladder fails (~0.87–0.89); subset mode reaches numerical zero at order 3.

## Strongest formulation

`Unknown_B = Observed - Projection_B(Observed)`, where B is a declared, tested interaction basis.

Then test whether the residual is real rather than noise, enlarge the basis minimally, test hidden data, search prior art, and only then propose a new operator/primitive.

Current classification: **ENGINEERING_SYNTHESIS / NOVELTY_UNVERIFIED**.