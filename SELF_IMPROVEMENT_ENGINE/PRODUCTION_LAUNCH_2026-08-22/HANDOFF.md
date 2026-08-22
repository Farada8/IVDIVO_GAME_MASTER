# Production Launch Handoff

Date: 2026-08-22

## Restore order

1. Read `SELF_IMPROVEMENT_ENGINE/LIBRARY_CURRENT/README.md` and current Self-Improvement authority/state surfaces.
2. Read this pack `README.md`.
3. Read `PRODUCTION_LAUNCH_QUEUE_v0.1.json`.
4. Resolve the first card whose status is `READY` or whose dependencies are proven by current persisted artifacts.
5. Execute only that smallest admissible card or bounded dependency reconciliation.
6. Persist implementation/tests/results.
7. Read back persisted artifacts before changing card state.
8. Update queue state only with evidence.

## DONE_VERIFIED production layers

`PL-00 MASTER PRODUCTION BOOTSTRAP = DONE_VERIFIED`.
- PR #287 merge `2264d7b17ce08811f0037c1ce9fd0ca622442064`.
- exact-head CI `32553543536` SUCCESS.
- Drive folder `1NY73gon6bWJRWhmxnJ9MLildINutKLLO`.

`PL-01 PROJECT STATE SYSTEM = DONE_VERIFIED`.
- PR #294 merge `566fbc00dea63e89257fe6eb4abc26e130e0a663`.
- PL-00 regression + PL-01 exact-head workflows SUCCESS.
- persisted ProjectStateManager + CLI + lifecycle/CLI tests.
- Drive folder `1kNuZY2ivHEkXHFn9D7HLujQxZf7EvGUO`, marker `PERSONAL-AI-PL01-DONE-VERIFIED-PR294`.

`PL-02 LOCAL MEMORY = DONE_VERIFIED`.
- baseline PR #299 merge `5a9337f2a416edbacdf4a85f02efdc1e27511bf9` established persistent store/search/update/invalidate/trace and audit events.
- contract-hardening PR #309 merge `d82020c7967c2c3dc1b22e4469974757d7aaf0bc` added named typed tables, SHA-256 content hashes, confidence/project/source fields, immutable versions, source-chain tracing and legacy migration.
- verified hardening head `7e947cee84fefb5467aa154546f648077aec0bbe`.
- exact-head workflows all SUCCESS: PL-00 `32555281797`, PL-01 `32555281872`, PL-02 baseline `32555281799`, PL-02 hardening `32555281777`.
- hardening Drive folder `1MhVtyPF89UPpvLvPcBeQis4wdBXmeN6C`, document `1IYlQfZOt7yI4GaQVBjDuL36yuIjvIPe9GFEO8HsAt5w`, marker `PERSONAL-AI-PL02-DONE-VERIFIED-PR309-CI4OF4`.

`PL-04 AI PROVIDER ABSTRACTION = DONE_VERIFIED`.
- baseline PR #321 merge `d5e17a9ed75b724b4e6920e71bce4388ff804196`; mandatory four-operation contract completion PR #328 merge `268a7d33c83d5551b9276b1a7a3551c76eb584fd`.
- canonical provider contract exposes generate/analyze/classify/extract plus ProviderConfig and OpenAIProvider/AnthropicProvider/OllamaProvider surfaces.
- corrective exact-head PL-00/01/02/02-hardening/04 CI 5/5 SUCCESS.
- configured credentials do not authorize spending; live provider success remains unverified and was not required.
- Drive folder `1NB6hVQVjUlK6wiSMsyrRgk0pX6bFkjgy`, document `1m9vfHsbMgrC_7hvIL2t9A1RUvTE7OdhhMImIxkwqQww`, marker `PERSONAL-AI-PL04-DONE-VERIFIED-PR321-PR328-CI5OF5-CONTRACT4OPS`.

`PL-05 AGENT EXECUTOR = DONE_VERIFIED`.
- PR #336 merge `876d0e4ca7f581be40f88b9be86f4a4da1894928`; verified head `d20b104e93e61cc87e1e180d4ea879a5e23f75c5`.
- bounded `max_steps` 1..20; only `CONTINUE:` requests another step; task lifecycle and OUTPUT memory persist; JSONL run audit persists.
- exact-head/merge-ref PL-00/01/02/02-hardening/04/05 CI 6/6 SUCCESS.
- Drive folder `1hhgo94czLN6Qz4p9qNdMjxcZvf0ih0G3`, document `1Y0Zww7H003dYjlF-CsCV9vINt76mYZPkTLizcjF7764`, marker `PERSONAL-AI-PL05-DONE-VERIFIED-PR336-CI6OF6`.
- no autonomous tool use, background work or live-provider success is implied.

`PL-11 TEST BENCHMARK RUNNER = DONE_VERIFIED`.
- PR #345 merge `7480f261e26bd2be58c10f814aa1ea27056e8a69`; refreshed verified head `8d09d5d9171a21cff9e7b8958e6496d0796ba900`.
- executable JSON baseline/candidate runner supports higher/lower-is-better metrics, positive weights, per-case regression tolerance and suite aggregate threshold.
- any critical regression forces `REJECT_CRITICAL_REGRESSION` even when aggregate gains are positive; `--enforce` returns non-zero on FAIL.
- every run persists a JSON report under `runtime/benchmarks`; invalid/non-finite/duplicate cases fail closed.
- refreshed exact-head workflows all SUCCESS: PL-00 `32557771235`, PL-01 `32557771273`, PL-02 `32557771252`, PL-02 hardening `32557771152`, PL-04 `32557771137`, PL-05 `32557771211`, PL-11 `32557771276`.
- Drive folder `1XAsNDfR3VZtUCkQRpUT2vqV9k_-lwwbL`, document `1NhxssgezKnsKrcameuzM62q3Rde7nuazNBPNTmf_aqQ`, marker `PERSONAL-AI-PL11-DONE-VERIFIED-PR345-CI7OF7`.
- PL-11 evaluates supplied measurements only; PL-12 will own patch/change promotion and rollback.

## Wave-1 foundation state

All Wave-1 cards are DONE_VERIFIED: `PL-00`, `PL-01`, `PL-02`, `PL-04`, `PL-05`, `PL-11`.

## Current READY graph

Canonical next frontier: `PL-06 Business Core = READY` — first Wave-2 real-production card.

Also READY:
- `PL-03 Source Evidence Layer`;
- `PL-08 Book Production Core`;
- `PL-10 Multi-Model Review`;
- `PL-12 Change Control`;
- `PL-13 File Ingestion`;
- `PL-15 Daily Control Panel`;
- `PL-16 Backup Recovery`;
- `PL-17 Security`;
- `PL-18 Cost Control`.

Reason for PL-06 priority: foundation execution, memory, providers, bounded agents and benchmark rejection are now verified. PL-06 is the first ready Wave-2 card and must prove a real business request can become a persisted estimate/quote without invented prices. PL-08 remains the parallel ready book-production path.

Do not re-execute DONE_VERIFIED layers unless a regression or explicit PL-12-style change-control event requires it. Preserve cumulative regression coverage.

## Stop conditions

Stop and mark `BLOCKED` instead of inventing a pass when:
- required runtime/tool is unavailable;
- secret/provider access is unavailable for a non-mock path;
- destructive action requires explicit authorization;
- current main/authority moved and changes need reconciliation;
- a required real external/human/market event has not happened.

## Handoff sentence for a new session

`Restore CURRENT Self-Improvement authority, then restore SELF_IMPROVEMENT_ENGINE/PRODUCTION_LAUNCH_2026-08-22. Wave-1 foundation PL-00/01/02/04/05/11 is DONE_VERIFIED. Continue from PL-06 Business Core; PL-03/08/10/12/13/15/16/17/18 remain dependency-admissible READY alternatives. Persist code/state/tests/readback, never invent business prices or evidence, and preserve v2 authority unless a separate promotion gate passes.`
