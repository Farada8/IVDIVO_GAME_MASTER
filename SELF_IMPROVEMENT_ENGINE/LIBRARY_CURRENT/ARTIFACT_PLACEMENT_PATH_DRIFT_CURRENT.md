# CURRENT Pointer — Artifact Placement Path Drift Pilot

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains `VERIFIED_CURRENT`.

Bounded incident/runtime package:
`SELF_IMPROVEMENT_ENGINE/INCIDENTS/2026-08-22_ARTIFACT_PLACEMENT_PATH_DRIFT/`

Failure classes now covered:
- `ARTIFACT_PLACEMENT_PATH_DRIFT`;
- `TOOL_ROUTE_MISMATCH / RESOURCE_TYPE_MISMATCH`.

Fail-closed state: `PERSISTED_BUT_MISPLACED`.

Execution law:
`FILE_EXISTS != RESULT_IS_FINDABLE`.
`RESOURCE_EXISTS != REQUEST_FULFILLED`.
`DONE_WITHOUT_DURABLE_RECEIPT = INVALID_STATE`.

A substantial external artifact may not transition toward verified completion until canonical placement, provider parent/path/resource-type readback, project START_HERE/CURRENT update and readback, legacy/duplicate-title scan, required cross-store pointer checks, and an `ArtifactPlacementReceipt` have passed. Task status and receipt are persisted as one atomic unit before DONE becomes durable.

Runtime authority on `main`:
- base placement convergence: merged PR #388, merge `b8265fe897a29147844591919fa4853aa3ba5a2c`;
- resource-type/tool-route hardening: merged PR #401, merge `e277ecb7f91fd3b9ce55464758bc531e789e2be9`;
- atomic completion/restart recovery hardening: merged PR #409, merge `654399a29324408cb0be75cae239587102090632`.

Runtime components:
- `personal-ai/core/artifact_placement.py`;
- `personal-ai/core/artifact_placement_adapters.py`;
- `personal-ai/projects/artifact_completion.py`;
- `.github/workflows/artifact-placement-runtime.yml`;
- `ATOMIC_COMPLETION_RECOVERY_CONTRACT_v1.md`.

Verified evidence:
- provider adapters for Google Drive and GitHub = COMPLETE;
- two real cross-project positive placement canaries = 2/2 `PLACEMENT_VERIFIED`;
- real Issue #395 proved DOCUMENT intent can produce FOLDER provider objects and motivated the resource-type guard;
- PR #409 final validation head `9c3ec07e93786bb3a639ae616461068ea74ec9c8` passed 10/10 related workflows;
- `artifact-placement-runtime` run `32569759436` = PASS;
- restart/reopen persistence regression = PASS against current ProjectState, Local Memory, Memory Contract Hardening and Provider Abstraction layers;
- post-merge runtime readback from `main` confirms one-write atomic task status + receipt persistence.

Promotion boundary:
Self-Improvement v2 remains CURRENT. Persistence/recovery engineering is now closed at the bounded runtime layer, but broader promotion remains HOLD for one non-simulatable requirement:

`Observe future real traffic where the already-installed placement/resource-type guard catches a new real persistence failure before any false DONE claim.`

Issue #395 does not satisfy this final gate because it triggered the resource-type repair; the next interception must occur with the guard already installed. Do not manufacture a failure to satisfy the gate.

Older PRs #362, #372, #377 and #389 are provenance-only after #388 and must not be treated as current implementation authority.

Drive mirror authority:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
