# Live Artifact Interception Evidence Contract v1

Date: 2026-08-22
Authority effect: NONE
Self-Improvement v2 remains VERIFIED_CURRENT.

## Purpose
The final promotion gate requires a future real persistence failure to be caught by the already-installed placement/resource-type guard before any false DONE claim. This contract makes that future event durable without manufacturing a failure and without trusting chat memory.

## Atomic capture
When an ArtifactPlacementReceipt is present but its status is not PLACEMENT_VERIFIED, `complete_task_with_artifact_gate()` must atomically persist the BLOCKED task state, the failing receipt, and an append-only `artifact_placement_interceptions` event in the same `tasks.json.tmp -> replace` transaction.

Each interception candidate records:
- schema and captured_at;
- attempted_transition = DONE;
- caught_before_done = true;
- receipt status and failure list;
- provider and artifact id;
- expected/actual parent;
- expected/observed resource type;
- provider_confirmation_required = true;
- promotion_proof = false;
- promotion_review_state = UNVERIFIED_PROVIDER_ORIGIN.

## Anti-self-certification law
`INTERCEPTION_CANDIDATE != REAL_PROVIDER_INTERCEPTION_PROOF`.

Runtime/tests may create interception candidates. They MUST NOT automatically satisfy the promotion gate. A later authority pass must independently confirm that the event came from real provider traffic using provider metadata/readback and must verify that the task was BLOCKED before any false DONE claim.

## History law
Interception history is append-only at the task level. A later successful retry may move the task to DONE with a PLACEMENT_VERIFIED receipt, but it must not erase earlier interception candidates.

## Missing receipt
A missing receipt still blocks completion but does not create a provider-failure interception candidate because there is no provider observation to validate.

## Promotion boundary
This instrumentation only arms evidence capture for the remaining live gate. It does not promote Self-Improvement v2, does not turn deterministic fixtures into real-world evidence, and does not permit manufactured failures.
