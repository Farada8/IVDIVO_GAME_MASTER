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
`INTERCEPTION_CANDIDATE != REAL_PROVIDER_INTERCEPTION_PROOF`.

A substantial external artifact may not transition toward verified completion until canonical placement, provider parent/path/resource-type readback, project START_HERE/CURRENT update and readback, legacy/duplicate-title scan, required cross-store pointer checks, and an `ArtifactPlacementReceipt` have passed. Task status and receipt are persisted as one atomic unit before DONE becomes durable.

Runtime authority on `main`:
- base placement convergence: merged PR #388, merge `b8265fe897a29147844591919fa4853aa3ba5a2c`;
- resource-type/tool-route hardening: merged PR #401, merge `e277ecb7f91fd3b9ce55464758bc531e789e2be9`;
- atomic completion/restart recovery hardening: merged PR #409, merge `654399a29324408cb0be75cae239587102090632`;
- durable live-interception evidence capture: merged PR #411, merge `e9eb2614a1448d026762360165a815a29160be25`.

Runtime components:
- `personal-ai/core/artifact_placement.py`;
- `personal-ai/core/artifact_placement_adapters.py`;
- `personal-ai/projects/artifact_completion.py`;
- `.github/workflows/artifact-placement-runtime.yml`;
- `ATOMIC_COMPLETION_RECOVERY_CONTRACT_v1.md`;
- `LIVE_INTERCEPTION_EVIDENCE_CONTRACT_v1.md`.

Verified evidence:
- provider adapters for Google Drive and GitHub = COMPLETE;
- two real cross-project positive placement canaries = 2/2 `PLACEMENT_VERIFIED`;
- Issue #395 proved DOCUMENT intent can produce FOLDER provider objects and motivated the resource-type guard;
- PR #409 exact-head 10/10 PASS; restart/reopen persistence regression = PASS;
- PR #411 validation head `073444b5d30d4f54faedd1bba189046c8feb62cf` passed 10/10 related workflows;
- PR #411 `artifact-placement-runtime` run `32570077658` = PASS;
- a bad receipt now atomically persists BLOCKED + receipt + append-only interception candidate;
- interception history survives restart/reopen and later successful retry;
- missing-receipt blocks do not masquerade as provider-failure candidates;
- every interception candidate is `promotion_proof=false` and requires independent provider confirmation.

Promotion boundary:
Self-Improvement v2 remains CURRENT. The bounded mechanism is now `HOLD_ARMED_FOR_LIVE_EVIDENCE`.

Exactly one non-simulatable requirement remains:
`Observe future real traffic where the already-installed placement/resource-type guard catches a new real persistence failure before any false DONE claim, then independently confirm provider origin/readback.`

Issue #395 does not satisfy this final gate because it triggered the resource-type repair. Tests/replays cannot satisfy it either. Do not manufacture a failure.

Older PRs #362, #372, #377 and #389 are provenance-only after #388 and must not be treated as current implementation authority.

Drive mirror authority:
`06_SELF_IMPROVEMENT / INCIDENT — ARTIFACT_PLACEMENT_PATH_DRIFT — 2026-08-22`.
