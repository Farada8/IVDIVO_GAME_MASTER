# IVDIVO — DURABLE TRANSACTION RECONCILIATION PROTOCOL v1.0

**Status:** ENGINEERING CANDIDATE / SI-0014  
**Established:** 2026-08-21  
**Parent:** `18C_VOLATILE_SESSION_CHECKPOINT_AND_RECOVERY_PROTOCOL_v1.0.md`  
**Reuses:** Self-Improvement Registry Transaction Contract v1.0, Asset Escrow v17, Cross-Conversation Autopilot v1.3.  
**Scope:** project-neutral recovery of interrupted GitHub/Drive/File Library/local/provider write sequences.

## 1. Problem

18C can prove that work was interrupted and whether pending/volatile material exists. It does not by itself decide whether a particular interrupted write should be repeated.

A multi-store production operation is not one atomic transaction. A session may disappear after:
- GitHub commit succeeded but Drive mirror did not;
- Drive object exists but readback was not completed;
- provider POST may have been accepted but response was lost;
- irreversible merge or paid generation may have started but completion is ambiguous.

Blind replay can create duplicate files, duplicate payments, duplicate provider jobs or conflicting authority states.

## 2. Primary law

`INTENT -> IDEMPOTENCY KEY -> EFFECT CLASS -> EXECUTE OUTSIDE THIS MODULE -> OBSERVE -> VERIFY IDENTITY -> READBACK -> RECONCILE`.

Recovery logic never infers that an external side effect did or did not happen merely because the previous chat ended.

## 3. Action contract

Every material action has:
- `action_id`;
- `artifact_id`;
- `store`;
- `operation`;
- `effect_class`;
- deterministic `idempotency_key`;
- `side_effect_state`;
- intended identity;
- observed identity;
- readback status.

Stores:
`GITHUB / DRIVE / FILE_LIBRARY / PROVIDER / LOCAL`.

Effect classes:
- `READ_ONLY`;
- `REVERSIBLE_WRITE`;
- `PAID_WRITE`;
- `IRREVERSIBLE_WRITE`.

Side-effect states:
- `NOT_STARTED`;
- `STARTED_UNKNOWN`;
- `CONFIRMED`;
- `RECONCILED`;
- `SUPERSEDED`;
- `FAILED`.

## 4. Deterministic idempotency

Default idempotency key:

`sha256(transaction_id + action_id + store + operation + artifact_id)`

with a stable `ivdtx:` prefix.

The key identifies an intended action, not successful completion. A repeated key requires store/provider reconciliation before retry.

## 5. Fail-closed decision order

1. **BLOCKERS** -> `STOP`.
2. **Authority/state drift** -> `REBASE_FIRST`.
3. **Confirmed identity mismatch** -> `STOP`.
4. **STARTED_UNKNOWN + PAID/IRREVERSIBLE** -> `QUARANTINE_EXTERNAL_SIDE_EFFECT`.
5. **STARTED_UNKNOWN + reversible/read-only** -> `VERIFY_STORE_BEFORE_RETRY`.
6. **Confirmed/reconciled without readback** -> `VERIFY_READBACK`.
7. **Unstarted paid/irreversible** -> `REQUIRE_EXPLICIT_DISPATCH_GATE`.
8. **Only safe unstarted actions remain** -> `EXECUTE_MISSING_SAFE_ACTIONS`.
9. **All actions terminal + verified** -> `TRANSACTION_COMPLETE`.

No lower-priority state may bypass a higher-priority gate.

## 6. Provider law

`PROVIDER REQUEST ACCEPTED != PRODUCTION ASSET ACCEPTED != TAKE/VOICE/PERFORMANCE LOCK`.

This protocol stores only reconciliation state. Provider-specific capability checks, spend ledgers, asset QC and human/Founder locks remain in their existing authorities.

A lost/ambiguous paid response is not permission to call again.

## 7. GitHub + Drive partial-write example

Intended transaction:
- `GH-REPORT` = reversible write;
- `DRIVE-REPORT` = reversible write.

If GitHub readback is verified but Drive is `NOT_STARTED`, result:
`EXECUTE_MISSING_SAFE_ACTIONS = [DRIVE-REPORT]`.

If Drive was `STARTED_UNKNOWN`, result:
`VERIFY_STORE_BEFORE_RETRY = [DRIVE-REPORT]`.

The GitHub action is not replayed.

## 8. Identity law

If an action is `CONFIRMED` or `RECONCILED`, every specified intended identity field must match observed identity.

Examples:
- GitHub blob/commit SHA;
- Drive file ID/revision/hash when available;
- provider request/asset ID;
- local content SHA-256.

Mismatch is `STOP`, not auto-repair.

## 9. Checkpoint lineage

Routine checkpoints must form a single-parent lineage per work unit.

Rules:
- one root generation `0`;
- child generation = parent + 1;
- no cross-work-unit parent;
- no duplicate checkpoint SHA;
- no multiple unexplained ACTIVE heads.

Retention:
- latest = `EPHEMERAL_RECOVERY_CURRENT`;
- incident-linked historical checkpoint = `AUDIT_KEEP`;
- routine superseded checkpoint = `GC_ELIGIBLE`.

## 10. Self-Improvement learning

Every real interruption may emit a bounded learning event:
- recovery decision;
- real interruption yes/no;
- false resume;
- false stop;
- duplicate work avoided;
- writes reconciled;
- checkpoint bytes/tool calls;
- recovery tool calls.

Promotion evidence is advisory only.

Minimum eligibility for promotion review of SI-0014:
- zero false resume;
- at least 3 real interruption recoveries;
- at least 2 independent projects;
- acceptable false-stop/overhead profile;
- GitHub/Drive readback evidence.

This is eligibility for review, never automatic promotion.

## 11. Registry-ID integrity

Before assigning a Self-Improvement candidate ID:
`READ FULL REGISTRY FAMILY -> COLLECT BASE + ALL EXTENSIONS -> PROVE ID UNUSED -> REGISTER`.

Recent chat memory, PENDING directory, search snippets or a partial file list are insufficient.

Run33 repaired a concrete violation: Session Resilience was initially written as pending `SI-0010` while the full registry already owned SI-0010 for registry compaction. The session-resilience stack is migrated to `SI-0014`.

## 12. Implementation

- `tools/ivdivo_durable_write_reconciler.py`
- `tools/ivdivo_checkpoint_lineage.py`
- `tools/ivdivo_interruption_learning.py`
- `schemas/IVDIVO_DURABLE_WRITE_TRANSACTION_SCHEMA_v1.json`
- `schemas/IVDIVO_CHECKPOINT_LINEAGE_SCHEMA_v1.json`
- `schemas/IVDIVO_INTERRUPTION_LEARNING_EVENT_SCHEMA_v1.json`

These modules are pure reconciliation/evidence logic. They do not perform external writes or calls.

## Final law

**AN INTERRUPTED ACTION IS NOT A FAILED ACTION, AND IT IS NOT A SUCCESSFUL ACTION. RECONCILE BEFORE REPLAY.**
