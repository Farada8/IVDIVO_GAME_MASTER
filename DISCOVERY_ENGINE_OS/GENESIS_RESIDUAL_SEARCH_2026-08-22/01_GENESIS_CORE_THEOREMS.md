# GENESIS CORE — FORMAL STATEMENTS v1

## G1 — Peer Genesis Growth Theorem

Let `(M,+,0)` be a commutative monoid and `S_n=x_1+...+x_n`. Define `x_(n+1):=S_n` and include the new object once in the next whole. Then `S_(n+1)=S_n+S_n`; in an additive abelian group/vector space, `S_(n+1)=2S_n`. By induction, `S_(n+k)=2^k S_n` and `x_(n+k)=2^(k-1) S_n` for `k>=1`.

This proves growth under repeated peer-promotion, not creation of a new independent degree of freedom.

## G2 — No-New-Generator Theorem

Let `Cl_Sigma(X)` be closure under an operation signature `Sigma`. If `g in Cl_Sigma(X)`, then `Cl_Sigma(X union {g}) = Cl_Sigma(X)`. Every term using `g` can substitute the old term over `X` that defines `g`.

Corollary: `g=sum_i x_i` is a new named/represented object, but not a new algebraic generator under ordinary addition.

## G3 — Symmetric Genesis Completeness (known mathematics)

For variables `x_1,...,x_n`, the elementary symmetric polynomials `e_k` form a complete generating family for symmetric polynomials: every polynomial invariant under arbitrary permutations of peers can be expressed as a polynomial in `e_1,...,e_n`.

This is known mathematics, not a new theorem.

## G4 — Symmetry Limitation

The symmetric ladder is not complete for arbitrary non-symmetric laws. Example: `f(x1,x2,x3)=x1*x2` is not permutation-invariant, while every function of `e1,e2,e3` is. Therefore two search modes are required: `SYMMETRIC_GENESIS` when peer symmetry is justified and `SUBSET_GENESIS` when identities/roles matter.

## Genesis criterion

- Representational Genesis: `g in Cl_Sigma(X)` but `g` is promoted to a new peer symbol/state/object.
- Structural Genesis relative to observables: adjoining `g` enlarges distinguishable/predictive structure relative to a declared test family.
- Strong Generator Genesis: `g notin Cl_Sigma(X)`, requiring richer operations/signature, external input/oracle, or a newly admitted primitive.