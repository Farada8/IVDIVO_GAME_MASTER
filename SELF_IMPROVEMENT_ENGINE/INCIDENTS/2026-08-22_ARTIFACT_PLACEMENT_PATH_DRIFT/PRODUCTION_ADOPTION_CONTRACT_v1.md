# Artifact Placement Production Adoption Contract v1

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains VERIFIED_CURRENT.

## Defect
Post-#411 adoption audit found that the placement gate existed and was tested, but canonical task execution could bypass it:
- `BoundedAgentExecutor.run()` called `ProjectStateManager.complete_task()` directly;
- canonical strict `BoundedAgentExecutor.execute()` also called `complete_task()` directly;
- `personal-ai/run.py` exposed no artifact-gated completion route.

Therefore `GUARD_IMPLEMENTED != GUARD_ADOPTED_BY_PRODUCTION_COMPLETION_PATHS`.

## Task contract
A task that produces an external artifact declares:
`requires_artifact_placement_receipt = true`.

For such a task:
- direct `ProjectStateManager.complete_task()` MUST fail closed;
- completion MUST route through `complete_task_with_artifact_gate()`;
- no model/provider output may invent or self-certify a placement receipt;
- missing receipt => BLOCKED;
- non-verified receipt => BLOCKED + durable interception candidate;
- PLACEMENT_VERIFIED receipt => DONE subject to normal functional gates.

Tasks without the marker retain backward-compatible completion semantics.

## Agent adoption
Both Agent Executor completion paths must carry the task policy:
- compatibility `run()`;
- strict canonical `execute()`.

An agent may finish its internal reasoning/output generation while the external artifact task remains BLOCKED pending provider-backed placement evidence. Internal output persistence does not authorize external-task DONE.

## CLI adoption
Canonical CLI supports:
- `agent run ... --require-artifact-placement-receipt`;
- optional `--artifact-placement-receipt <receipt.json>` when provider evidence is already available;
- `project complete-artifact <project_id> <task_id> <receipt.json>` for later completion after external provider readback.

`project complete-artifact` is valid only for a task already declared artifact-producing.

## CI adoption
Artifact placement CI must trigger on manager, agent base/executor, CLI and production-adoption regression changes, and must run Agent Executor compatibility suites in addition to placement tests.

## Promotion boundary
Until this contract passes exact-head CI and merges, live interception is implemented but production adoption is incomplete. After merge, the remaining promotion gate is still a future real provider-backed failure caught before false DONE and independently confirmed by provider readback.
