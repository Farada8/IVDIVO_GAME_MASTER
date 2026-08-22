# G5 — GENERAL PEER-PROMOTION THEOREM

Let `(M,∘)` be a commutative semigroup and define `S_n=x_1∘...∘x_n`. Promote the whole to a new peer: `x_(n+1):=S_n`. Because the same operation forms the next whole, `S_(n+1)=S_n∘x_(n+1)=S_n∘S_n`.

Therefore the entire peer-promotion dynamics reduces to iteration of the diagonal map `D(s)=s∘s`, and `S_(n+k)=D^k(S_n)`.

Examples:
- addition: `D(s)=2s`, so `S_(n+k)=2^k S_n`;
- multiplication: `D(s)=s^2`, so `S_(n+k)=S_n^(2^k)` where exponentiation is meaningful;
- idempotent operations (`max`, `min`, set union, Boolean OR): `D(s)=s`, fixed point;
- XOR: `D(s)=0`, one-step collapse to the zero fixed point;
- modular addition: `D(s)=2s mod m`, which can generate cycles depending on modulus/seed.

Consequence: the original peer-promotion principle does not imply one universal growth law. It defines a Genesis Dynamics determined by the algebraic diagonal map. Regimes include growth, fixed point, collapse, periodic/cyclic and more general nonlinear orbit behavior.

Next research target: classify operation laws by diagonal-dynamics regime, then test whether observed natural/engineering processes are better described by one of these regimes. Current novelty status: theorem itself is an elementary derivation; the project-specific use as a discovery/search protocol remains NOVELTY_UNVERIFIED.