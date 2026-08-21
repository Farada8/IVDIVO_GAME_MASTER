# ENGINEERING MODULES + CONTRACTS — SI-0012 v0.2.0

**Status:** WORKING / PILOTING / NOT CURRENT AUTHORITY

## Runtime package
26 runtime modules total, including 16 new Cycle-4 integration modules on top of inherited SI-0012 v0.1.1.

### New Cycle-4 integration modules
- `surface_manifest.py` — current-surface/authority/frontier compiler.
- `scope_supersession.py` — scope-aware supersession/conflict resolution.
- `readiness.py` — vector readiness compiler; prevents false one-word lock.
- `fact_lock.py` — version/hash/authorized-consumer shared-fact lock.
- `evidence_lineage.py` — independent-vs-derived evidence families.
- `prompt_ir_v2.py` — compact executable task contract + equivalence controls.
- `context_budget.py` — dependency-aware context packet compiler.
- `mutation_guard.py` — expected state/path/secret/no-effect/readback guard.
- `transaction_journal.py` — multi-surface transaction state with REPAIR_REQUIRED.
- `telemetry_v2.py` — evidence-classed unified telemetry; unknowns stay null.
- `economics.py` — measured-only production economics contract.
- `package_divergence.py` — immutable package vs post-package main classifier.
- `drift_fixture.py` — live-schema drift → permanent regression fixtures.
- `learning_compiler.py` — evidence → reusable learning with leakage stripping.
- `governor.py` — meta-work starvation / information-value governor.
- `registry_compaction.py` — deterministic registry-family compaction candidate.

### Inherited runtime core retained
State Adapter, Shared Facts, Obligation DAG, Prompt IR v0.1, pre-execution guards, transaction primitives, telemetry v0.1, orchestrator and models remain as compatibility baseline.

## New machine contracts (12)
- `CURRENT_SURFACE_MANIFEST_SCHEMA_v0.2.json`
- `ECONOMICS_EVIDENCE_SCHEMA_v0.1.json`
- `EVIDENCE_LINEAGE_SCHEMA_v0.1.json`
- `LEARNING_CANDIDATE_SCHEMA_v0.1.json`
- `PACKAGE_DIVERGENCE_SCHEMA_v0.1.json`
- `PROMPT_IR_SCHEMA_v0.2.json`
- `READINESS_VECTOR_SCHEMA_v0.1.json`
- `SELF_IMPROVEMENT_GOVERNOR_SCHEMA_v0.1.json`
- `SHARED_FACT_LOCK_SCHEMA_v0.2.json`
- `TELEMETRY_EVENT_SCHEMA_v0.2.json`
- `TOOL_MUTATION_GUARD_SCHEMA_v0.1.json`
- `TRANSACTION_JOURNAL_SCHEMA_v0.1.json`

## Integration laws
- authority and freshest compatible work frontier are separate objects;
- scope-local progress cannot erase higher authority or unrelated gates;
- shared facts use version/hash + authorized consumers;
- evidence is clustered by provenance family, not model vote count;
- Prompt IR/Context Budget must preserve authority/protected facts/gates;
- mutable writes require expected state, allowed scope, secret scan and readback;
- partial writes become `REPAIR_REQUIRED`, never false PASS;
- unknown spend/time stays unknown;
- package identity is immutable;
- universal learning strips names/exact clue chains/project assets;
- one-project pilot cannot become domain authority without independent replication;
- Self-Improvement Governor can refuse more meta-work when real production evidence has higher value.

Full exact source and all schemas/tests are preserved in the versioned ZIP mirrored to Drive.