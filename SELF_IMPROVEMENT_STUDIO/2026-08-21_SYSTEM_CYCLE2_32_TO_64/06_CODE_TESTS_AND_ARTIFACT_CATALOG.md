# CYCLE 2 — CODE, TESTS & ARTIFACT CATALOG

## Executable prototypes
- `state_adapter_v0_2.py` — heterogeneous persisted state -> normalized work state; fail-closed on missing/unsupported authority.
- `causality_break_detector_v0_1.py` — graph-signal detector for orphan/disconnected causal structures; not a literary Story Gate.
- `prompt_ir_compiler_v0_1.py` — RUN CARD -> structured Prompt IR contract.
- `transactional_write_through_v0_1.py` — expected-hash freshness token, no-effect rejection, readback verification, rollback.
- `registry_transaction_api_v0_1.py` — candidate lifecycle invariants and evidence/target checks.

Exact source code and the fine-grained artifact set are preserved in the Cycle 2 Drive ZIP referenced by `00_README.md` / final cycle handoff.

## Deterministic engineering tests — 12/12 PASS
- State Adapter: D09 real-gate routing PASS; incomplete state fail-closed PASS.
- Causality detector: orphan signal PASS.
- Prompt IR: missing contract rejected; valid contract accepted.
- Registry transaction: missing invariants rejected; valid HOLD accepted; VERIFIED without evidence rejected.
- Transactional write-through: commit PASS; no-effect rejected; rollback PASS; stale write rejected.

These tests prove bounded engineering behavior only. They do **not** prove literary quality, actor/audio quality, provider reliability, human preference, business ROI or market performance.

## Produced artifact contracts
`CURRENT_SURFACE_MANIFEST_v0.1.json`; `NORMALIZED_WORK_STATE_SCHEMA_v0.2.json`; `SHARED_FACT_CONTRACT_SCHEMA_v0.1.json`; `PACKAGE_MAIN_DIVERGENCE_AUDIT_v0.1.json`; `IDEA_TO_STORY_LIVE_CALIBRATION_PROTOCOL_v0.1.md`; `RELATIONSHIP_AUTHORITY_GRAPH_SCHEMA_v0.1.json`; `HUMAN_SCENE_NATURALISM_CANARY_v0.1.md`; `STORY_LOCK_READINESS_SCHEMA_v0.1.json`; `D09_STORY_LOCK_READINESS_PACKET_v0.1.json`; `STORYLOCK_TO_AUDIO_MANIFEST_SCHEMA_v0.1.json`; `VOICE_BACKEND_BINDING_CASCADE_v0.2.json`; `PERFORMANCE_INTENT_PACKET_SCHEMA_v0.1.json`; `AUDIO_SHARED_FACT_GRAPH_SCHEMA_v0.1.json`; `AUDIO_DEFECT_ROOT_CAUSE_ROUTER_v0.1.json`; `PROMPT_IR_SCHEMA_v0.1.json`; `SOURCE_PARITY_PACKET_SCHEMA_v0.1.json`; `TOOL_CALL_GUARDRAILS_v0.1.json`; `MULTI_AI_RECONCILER_SCHEMA_v0.1.json`; `ENGINE_EXTENSION_VS_NEW_GATE_v0.1.json`; `META_ORCHESTRATOR_DAG_SCHEMA_v0.2.json`; `CROSS_DOMAIN_EVIDENCE_MAP_v0.1.json`; `ONE_VARIABLE_CANARY_SCHEMA_v0.1.json`; `PRODUCTION_ECONOMICS_BASELINE_v0.1.json`; `PORTFOLIO_THROUGHPUT_POLICY_v0.1.json`; `FEEDBACK_TRIAGE_ROUTER_v0.1.json`; `SELF_IMPROVEMENT_STARVATION_AUDIT_v0.1.json`; `RULE_VALUE_AUDIT_v0.1.json`; `CONTEXT_BUDGET_COMPILER_v0.1.json`; `NEXT_CYCLE_AUTONOMOUS_ROUTER_v0.2.json`.

## Test log
```
test_adapter_d09_gate ... ok
test_adapter_fail_closed ... ok
test_causality_orphan ... ok
test_prompt_ir_missing ... ok
test_prompt_ir_ok ... ok
test_registry_missing ... ok
test_registry_valid_hold ... ok
test_registry_verified_without_evidence ... ok
test_transaction_commit ... ok
test_transaction_no_effect ... ok
test_transaction_rollback ... ok
test_transaction_stale ... ok
Ran 12 tests — OK
```

## Packaging law
Do not retroactively relabel `IVDIVO_ENGINE_v11_2_CONTINUOUS_EXECUTION_CURRENT.zip`. Selected post-package extensions require a new package build, cold-unpack regression and new checksum before a package pointer can advance.