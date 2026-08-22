# GENESIS DYNAMICS CYCLE2 — SYNTHESIS + RED TEAM

## Strongest mathematical formulation

The core peer-promotion equation is

`S_{n+1}=F(S_n,S_n)=D(S_n)`.

For addition, `D(s)=2s`.

For a finite associative operation, `D^k(s)=s^(2^k)` and every orbit is eventually periodic.

For the classical Aczél class of continuous strictly monotone/cancellative associative operations on suitable intervals,

`F(x,y)=phi^{-1}(phi(x)+phi(y))`,

so

`phi(S_{n+1})=2 phi(S_n)` and `phi(S_{n+k})=2^k phi(S_n)`.

This is the strongest exact return to the original intuition: the whole becoming a peer produces exact doubling in the appropriate additive-generator coordinate. It is a known representation-theorem corollary, not a new universal law.

## Critical identifiability result

Repeated whole→peer evolution reveals only the diagonal `D(x)=x∘x`, not the entire binary operation.

Exhaustive n=3 control:
- 63 labeled commutative associative operations;
- 12 isomorphism classes;
- 19 diagonal maps;
- 10 ambiguous diagonals;
- up to 9 labeled operations sharing a diagonal.

The continuous control is simpler: MAX, MIN, MEAN and RMS all satisfy `D(x)=x` but differ off diagonal.

Therefore any attempt to discover the operation itself must include mixed probes `a∘b` or additional identifiable structural assumptions.

## Operator-synthesis demonstration

A planted law `F(a,b)=a+b+0.37ab` was intentionally omitted from the fixed dictionary.

Best fixed-dictionary hidden RMSE: ~0.135.

Parametric synthesis recovered `lambda=0.369926`, hidden RMSE ~0.0098, with associativity defect at machine precision.

Prior art then downgraded the apparent discovery to **REDISCOVERY**, because

`1+lambda F(a,b)=(1+lambda a)(1+lambda b)`

is a coordinate-scaled multiplicative formal group law.

This is the desired behavior: discover a useful missing law, then refuse false novelty.

## Genesis regime taxonomy

1. additive-generator/Aczélian -> exact doubling in phi-coordinate;
2. finite power-map -> tail + cycle;
3. idempotent -> fixed diagonal;
4. self-cancelling/nil -> collapse;
5. nonassociative -> bracketing-dependent aggregate;
6. role-dependent/noncommutative -> identity/order of parts matters;
7. residual unknown -> known families/property-constrained search fail on hidden mixed probes.

## Prior art ceiling

Known overlap includes:
- finite power-map functional graphs over groups/semigroups;
- published classification of the 12 commutative semigroups of order 3;
- Aczél associativity/additive-generator representations;
- formal group laws such as `x+y+xy`;
- functional ANOVA/Hoeffding/Sobol/Möbius interaction decompositions.

Current strongest project status:

`ENGINEERING_SYNTHESIS / NOVELTY_UNVERIFIED`.

## Red Team conclusions

Rejected:
- universal literal doubling outside the original/additive coordinate;
- universal monotone growth;
- diagonal-identifies-operation;
- order-3 semigroup classification as novelty;
- `a+b+lambda ab` as a new operator family;
- good predictive fit as sufficient for a valid Genesis law;
- predictive mixed-probe fit as causal physical law;
- Aczél coordinate doubling as a new theorem.

Surviving engineering object:

**Genesis Operator Residual Certificate (GORC)**

`peer trajectory -> diagonal dynamics -> identifiability audit -> mixed probes -> operation property tests -> linearizing-coordinate search -> hidden residual -> prior art -> application transfer`.

Next blocker: learn/probe the full operation under noise and real controlled mixed experiments, then search for a linearizing coordinate or prove the candidate lies outside the known class.
