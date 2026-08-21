# WAVE11 — ENGINEERING MODULES / CONTRACTS / PROOFS / PROTOCOLS

## Modules
### `provider_evidence_intake.py`
Consumes only secret-free upstream evidence. Validates canonical AUTH_PROVIDER, exact GitHub run/attempt/source lineage, optional separate snapshot equality/freshness, inventory compilation and optional prior-snapshot repeatability. Returns deterministic `intake_hash`. Provider calls=0; synthesis=0; dispatch=false; auto-lock=false.

### `provider_execution_state.py`
Routes admissible provider evidence through `NO_ADMISSIBLE_PROVIDER_EVIDENCE -> AUTH_PROVIDER_VERIFIED -> INVENTORY_READY/CAPABILITY_DRIFT_REVALIDATION_REQUIRED -> AUDITION_REQUIRED`. It does not own human lock, pronunciation lock, pre-spend GO or paid dispatch.

### `.github/workflows/elevenlabs-provider-evidence-intake.yml`
Read-only `workflow_run` consumer for the exact upstream provider workflow. Downloads only the triggering run's named artifact, locates exactly one receipt and one snapshot, validates with current trusted default-branch code, publishes one secret-free intake artifact.

## Contracts
- `contracts/PROVIDER_EVIDENCE_INTAKE_CONTRACT_v1.md`
- `contracts/WORKFLOW_RUN_LINEAGE_CONTRACT_v1.md`
- `contracts/PROVIDER_EXECUTION_STATE_CONTRACT_v1.md`

## Proof obligations
- valid current packet -> PASS intake + inventory + repeatability-required state;
- wrong transaction/source -> fail;
- stale packet -> hold;
- packet/snapshot drift -> fail;
- secret-shaped key -> fail before intake;
- same-account second snapshot -> repeatability observation;
- cross-account second snapshot -> fail;
- capability drift -> revalidation, no substitution;
- resolver never creates human/spend authority;
- workflow trigger/read permissions/exact run binding/no secret/no synthesis are statically regressed.

## Security proof boundary
The workflow artifact is data, never executable authority. Wave11 checks out trusted current default-branch code and executes repository validators, not scripts from the downloaded artifact. `workflow_run` privilege must not be used to grant write permissions or run untrusted artifact code.

## Self-Improvement protocol
`protocols/PROVIDER_EVIDENCE_SELF_IMPROVEMENT_PROTOCOL_v1.md` defines earliest-cause repair and stop law. One real event can validate that lineage but cannot promote cross-project/global authority by itself.

## Implementation defect caught by Red Team
Initial execution-state code briefly accepted caller booleans for human lock/pre-spend progression. This was rejected as evidence laundering and removed before CI. Final code cannot represent those transitions; it stops at `AUDITION_REQUIRED` and delegates later authority to existing receipt-based systems.
