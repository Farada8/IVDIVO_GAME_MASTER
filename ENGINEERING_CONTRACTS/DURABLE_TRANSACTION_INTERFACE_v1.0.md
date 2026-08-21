# DURABLE TRANSACTION INTERFACE v1.0

Status: WORKING ENGINEERING CONTRACT — NOT STORY CANON — NOT SELF-IMPROVEMENT PROMOTION

## Purpose
Converge SI-0012 single-store stale-hash/readback transaction semantics and SI-0014 multi-store interruption recovery at one versioned interface without replacing either runtime.

## Authority boundary
- Founder/project/story authority remains above all transaction/checkpoint state.
- SI-0012 remains the routing/orchestration compatibility runtime.
- SI-0014 remains the session-resilience/durable-recovery runtime.
- This interface is an adapter/facade, not a third durable-write engine.
- Provider/domain authorization gates remain independent and must pass before paid or irreversible dispatch.

## Common decision vocabulary
`STOP | REBASE_FIRST | QUARANTINE_EXTERNAL_SIDE_EFFECT | VERIFY_STORE_BEFORE_RETRY | VERIFY_READBACK | REQUIRE_EXPLICIT_DISPATCH_GATE | EXECUTE_MISSING_SAFE_ACTIONS | TRANSACTION_COMPLETE`

Legacy SI-0012 mapping:
- stale expected hash -> `STOP / STALE_REJECTED`
- no-effect mutation -> `STOP / NO_EFFECT_REJECTED`
- safe single-store write ready -> `EXECUTE_MISSING_SAFE_ACTIONS`
- readback mismatch -> `STOP / READBACK_MISMATCH`
- exact readback -> `TRANSACTION_COMPLETE`

SI-0014 mapping is delegated to `tools/ivdivo_durable_write_reconciler.py`; the interface may not silently weaken or reorder its fail-closed decisions.

## Genuine interruption evidence law
A raw field such as `real_interruption=true` is a CLAIM, not proof.

An event may be normalized to `real_interruption=true` only when a packet proves all of:
1. `controlled=false`;
2. `synthetic=false`;
3. `unplanned=true`;
4. origin is an allowed unplanned interruption class;
5. restart was observed;
6. a pre-interruption checkpoint ID exists;
7. post-restart authority readback passed;
8. recovery readback passed;
9. project state before and after are identified;
10. at least two durable source-evidence references are supplied.

Qualification classes:
- `QUALIFIED_REAL_PACKET`
- `EXCLUDED_CONTROLLED`
- `EXCLUDED_SYNTHETIC`
- `UNVERIFIED_REAL_CLAIM`

Controlled/synthetic/unverified events are forced to `real_interruption=false` before learning/promotion metrics.

The qualifier does not itself fetch or authenticate external evidence references. Source-reference existence/readback is a separate verification responsibility and must fail closed before any promotion review.

## Promotion boundary
The existing SI-0014 advisory threshold remains:
- zero false resume;
- at least 3 qualified genuine interruption/restart recoveries;
- at least 2 independent projects;
- acceptable real false-stop rate.

Meeting the threshold yields only `ELIGIBLE_FOR_PROMOTION_REVIEW`. It never auto-promotes SI-0014, SI-0012, this interface, or any project/canon state.

## Backward compatibility
- Do not delete or rename SI-0012 `plan_transaction` / `verify_readback` semantics.
- Do not replace SI-0014 durable reconciler.
- Existing callers may continue to use either runtime directly.
- New callers that need cross-runtime evidence vocabulary should use `tools/ivdivo_durable_transaction_interface.py`.

## Fail-closed invariants
- no raw `real_interruption` boolean as self-verifying evidence;
- no controlled/synthetic event may satisfy a genuine evidence threshold;
- no paid/irreversible replay from recovery state;
- no stale authority write;
- no identity mismatch repair-in-place;
- no checkpoint/transaction record as canon;
- no secret persistence;
- no automatic candidate promotion;
- no second durable transaction runtime.

## Acceptance
PASS requires:
- SI-0012 adapter parity on stale/no-effect/ready/readback cases;
- SI-0014 delegate parity on recovery/drift cases;
- controlled/synthetic masquerade regression PASS;
- incomplete genuine claim downgrade PASS;
- qualified genuine packet PASS;
- cross-project threshold remains advisory;
- old Run32/Run33 regression suites stay green;
- Self-Improvement registry integrity stays green;
- Drive mirror/readback records evidence without promotion inflation.
