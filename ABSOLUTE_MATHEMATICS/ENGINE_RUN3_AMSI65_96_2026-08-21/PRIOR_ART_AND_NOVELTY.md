# RUN3 PRIOR ART + NOVELTY AUDIT

Status: **NOVELTY_UNVERIFIED / INTEGRATION CANDIDATE**

## Component map

| Active surface | Strong prior-art families | Run3 decision |
|---|---|---|
| Behavioral/context quotient | Myhill–Nerode, bisimulation, abstract interpretation, causal states | not novel alone |
| Minimal predictive state | causal states, Predictive State Representations | not novel alone |
| Controlled/intervention-safe state | PSRs, causal abstraction | high overlap |
| Compression preserving causal control | Causal Information Bottleneck | high overlap |
| Lossy intervention abstraction | projected/lossy causal abstractions | high overlap |
| Categorical high/low model maps | categorical causal abstraction | high overlap |
| Exact/approx aggregation | lumpability, bisimulation metrics, MDP abstraction | high overlap |
| Approximation semantics | abstract interpretation | high overlap |
| Abstraction certificates | abstraction-carrying code, certifying phase abstraction | established methodology |
| Resource-aware abstraction | rate-distortion, communication/streaming complexity | high/fragmented overlap |
| Minimal realization | LTI realization theory | established |
| Genesis/normal forms | rewriting systems, confluence, term algebras, operads | established families |
| Generator novelty | term definability / universal algebra | strongly relative to language/signature |
| Open-ended method improvement | Darwin Gödel Machine, Huxley-Gödel Machine, AlphaEvolve | high conceptual overlap |

## High-signal sources

- Cousot & Cousot, Abstract Interpretation (POPL 1977): https://doi.org/10.1145/512950.512973
- Crutchfield/Shalizi causal states/minimal representations: https://doi.org/10.1103/PhysRevE.59.275
- Predictive State Representations: https://arxiv.org/abs/1207.4167
- Geiger et al., Causal Abstraction (JMLR 2025): https://www.jmlr.org/papers/v26/23-0058.html
- D'Acunto et al., Causal Abstraction Learning (ICML 2025): https://proceedings.mlr.press/v267/d-acunto25a.html
- Simoes et al., Causal Information Bottleneck (UAI 2025): https://proceedings.mlr.press/v286/simoes25a.html
- Xia & Bareinboim, Causal Abstraction Inference under Lossy Representations (ICML 2025): https://proceedings.mlr.press/v267/xia25a.html
- Causal Abstractions, Categorically Unified: https://arxiv.org/abs/2510.05033
- Certifying Phase Abstraction: https://arxiv.org/abs/2405.04297
- Abstraction-carrying / reduced certificate work: https://arxiv.org/abs/1010.4533
- Adaptive state-action abstractions via rate-distortion (2026): https://arxiv.org/abs/2606.06123
- Darwin Gödel Machine: https://arxiv.org/abs/2505.22954
- Huxley-Gödel Machine: https://arxiv.org/abs/2510.21614
- AlphaEvolve: https://arxiv.org/abs/2506.13131

## Rejected novelty claims

- first theory of abstraction;
- first minimal predictive state;
- first causal/lossy causal abstraction;
- first abstraction certificate;
- first resource-aware abstraction;
- first self-improving archive.

## Surviving candidate contribution

`Cross-Domain Promotion Falsification & Certification Protocol`

The candidate integration simultaneously records:

`Contexts + Interventions + RecursiveState + History/Micro Sufficiency + Uncertainty-Aware Closure + Resource Pareto + Proof Obligations + Evidence Claim Ceilings + Revocation/Supersession`.

A bounded search did not locate one published framework containing every one of those axes in a single reusable protocol. That absence is **not proof of novelty**.

Current classification: **BENCHMARK/ENGINEERING METHODOLOGY CANDIDATE**. Stronger novelty requires systematic scholarly review, independent experts, formal proof replay and evidence that the integrated protocol catches useful failures missed by simpler baselines.
