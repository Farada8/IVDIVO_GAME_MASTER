# GENESIS RESIDUAL EXPERIMENT SUMMARY

All experiments use held-out test data.

| System | Symmetric ladder | Subset ladder | Verdict |
|---|---:|---:|---|
| `sum` | order 1 -> numerical zero | order 1 -> numerical zero | ORDER1 |
| `symmetric_pair` | RMSE ~0.779 -> ~0 at order 2 | ~0.780 -> ~0 at order 2 | ORDER2 |
| `symmetric_triple` | ~0.409 -> ~0 at order 3 | ~0.413 -> ~0 at order 3 | ORDER3 |
| `full_product` | ~0.116 -> ~0 at order 4 | ~0.116 -> ~0 at order 4 | ORDER4 |
| `specific_pair=x1*x2` | remains ~0.34 even through order 4 | -> ~1e-12 at order 2 | SYMMETRIC FAIL / SUBSET ORDER2 |
| `mixed` | remains ~0.87-0.89 | ~0.879 -> 0.188 -> ~0 at order 3 | SYMMETRIC FAIL / SUBSET ORDER3 |

Peer-growth control starting from `[1,2,3,4]` creates peers `10,20,40,80`; total sums become `20,40,80,160` exactly as G1 predicts.

Local regression: **8/8 PASS**.

Strong result: residual-order search can recover the planted interaction order when the declared basis matches the symmetry/identity structure. A persistent residual means the basis is incomplete or wrong; it does not by itself prove a new law.