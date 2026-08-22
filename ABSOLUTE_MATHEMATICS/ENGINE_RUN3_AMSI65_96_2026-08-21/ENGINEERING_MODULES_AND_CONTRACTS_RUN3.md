# RUN3 ENGINEERING MODULES + CONTRACTS

New Run3 modules: **25**

## Modules

- `term_definability.py`
- `closure_schema.py`
- `conservative_extension.py`
- `delegation_budget.py`
- `genesis_types.py`
- `scc_genesis.py`
- `critical_pairs.py`
- `genesis_complexity_audit.py`
- `archive_store.py`
- `improvement_baselines.py`
- `descendant_validation.py`
- `diversity.py`
- `mutation_budget.py`
- `cold_extract.py`
- `rollback.py`
- `bridge_v2.py`
- `state_cas.py`
- `claim_caps.py`
- `claim_graph.py`
- `fingerprint.py`
- `handoff.py`
- `starvation_governor.py`
- `cross_domain_benchmarks.py`
- `publication_classifier.py`
- `release_gate.py`

## Contracts

- `CLAIM_SUPERSESSION_GRAPH_v1.json`
- `CROSS_DIALOG_HANDOFF_v2.json`
- `EVIDENCE_CLAIM_CAP_CONTRACT_v1.json`
- `GENESIS_TYPED_PROCESS_CONTRACT_v2.json`
- `G_RISE_LANGUAGE_CONTRACT_v2.json`
- `OPEN_ENDED_ARCHIVE_CONTRACT_v2.json`
- `RESEARCH_RELEASE_GATE_v1.json`
- `SOURCE_FINGERPRINT_CONTRACT_v1.json`
- `STARVATION_GOVERNOR_v1.json`
- `STATE_CAS_WRITE_CONTRACT_v1.json`

## Proof/review/protocol artifacts

- `formal/lean/AbsoluteMathTargets.lean`
- `formal/FORMALIZATION_STATUS.json`
- `AMSI89_PRIOR_ART_MAP.md`
- `AMSI90_NOVELTY_AUDIT.md`
- `AMSI91_FORMALIZATION_PACK.md`
- `AMSI92_CROSS_DOMAIN_BENCHMARK.md`
- `EXTERNAL_REVIEWER_PACKET.md`
- `AMSI94_PUBLICATION_DECISION.md`
- `FORMAL_CORE_v7_MINIMAL.md`
- `AMSI96_RELEASE_GATE.md`

## Runtime boundary

Generic authority/durable-write/governor capabilities are reused only when they are merged/current. Draft-only parallel code is evidence, not runtime authority. The full runnable source/tests/contracts are preserved in the Run3 ZIP mirrored to Google Drive.
