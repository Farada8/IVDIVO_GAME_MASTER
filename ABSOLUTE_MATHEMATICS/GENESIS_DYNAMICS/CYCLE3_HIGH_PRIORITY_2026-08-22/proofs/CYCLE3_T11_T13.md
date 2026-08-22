# GENESIS DYNAMICS CYCLE3 — T11–T13

## T11 — Exact squaring orbit in a finite monogenic semigroup
Let x generate a finite monogenic semigroup with index i and period p. Write p=2^a q with q odd. Under peer squaring D^k(x)=x^(2^k). Then the exact tail is

mu = max(ceil(log2 i), a)

and the eventual cycle length is 1 if q=1, otherwise ord_q(2).

Reason: before 2^k>=i the orbit is in the distinct preperiodic region; before k>=a the 2-adic valuation of 2^k mod p still changes; after both thresholds, modulo the odd part q the map is multiplication by 2, hence purely periodic with multiplicative-order period. Checked by brute orbit construction for every 1<=i,p<=34: 1,156 pairs, 0 mismatches.

Status: KNOWN/DERIVED from standard monogenic-semigroup power periodicity; no novelty claim.

## T12 — Generator derivative identity
Assume differentiable associative F with identity e and additive generator phi such that phi(F(x,y))=phi(x)+phi(y). Differentiating in y at e gives

phi'(x) = phi'(e) / partial_2 F(x,e).

Hence up to positive scale:

phi(x)=C integral dt / partial_2 F(t,e).

Cycle3 finite-difference controls recover identity for addition, log x for multiplication, -log(1-x) for probabilistic OR, and log(1+lambda x)/lambda for x+y+lambda xy.

Status: derived corollary of known additive-generator representation.

## T13 — Relative diagonal identifiability
Unrestricted operation identity cannot be inferred from D(x)=F(x,x). But if a parametric family F_theta is explicitly preregistered and theta -> D_theta is injective, diagonal data can identify theta relative to that family.

For F_lambda(a,b)=a+b+lambda ab, D_lambda(x)=2x+lambda x^2, so lambda=(D_lambda(x)-2x)/x^2 for nonzero x.

Therefore relative family identification != unrestricted operation identification.
