# SI-0014 Genuine Interruption Ledger Contract v1.0

**Status:** CANDIDATE ENGINEERING CONTRACT / SI-0014 READY_FOR_PILOT support  
**Authority effect:** NONE. Self-Improvement v2 remains CURRENT.  
**Runtime:** `tools/ivdivo_interruption_learning.py` schema `ivdivo.interruption_learning/1.1`.

## Purpose
Prevent evidence inflation when one physical interruption affects multiple projects, while preserving exact project-slice recovery evidence and backward compatibility with earlier Run33 learning rows.

## Identity model
A recovery record has two different identities:

- `incident_id` — one physical/session interruption event. It is counted at most once toward the SI-0014 genuine-event threshold.
- `recovery_id` — one project/work-unit recovery slice inside that incident. Multiple recovery slices may share one `incident_id`.

Legacy rows may provide only `event_id`; then `incident_id := event_id`. When `recovery_id` is absent it is deterministically derived from `incident_id + project_id + work_unit`.

## Core invariants
1. One physical interruption counts once, regardless of how many project slices are recovered.
2. `recovery_id` must be unique; duplicate recovery slices are rejected.
3. One `incident_id` may not mix `real_interruption=true` and `false` rows.
4. A project slice qualifies only when the interruption is real, readback is complete, and `false_resume=false`.
5. An explicit `qualifying_recovery=true` cannot override missing readback, synthetic provenance, or false resume.
6. Any observed false resume blocks promotion review, including a synthetic safety fixture.
7. Synthetic/controlled events may block for safety but never satisfy genuine-event thresholds.
8. Unknown telemetry is `null`, not `0`. A real numeric zero must be explicitly present in evidence.
9. Promotion output is advisory only. The runtime never changes SI registry status or Founder authority.
10. SI-0014 review threshold remains at least 3 genuine interruption incidents across at least 2 distinct projects with zero false resume.

## Required recovery-slice fields
- `event_id` — retained compatibility identifier;
- `project_id` or alias `project_slice_id`;
- `work_unit`;
- `recovery_decision`.

Recommended v1.1 fields:
- `incident_id`;
- `recovery_id`;
- `real_interruption`;
- `project_slice_readback_complete`;
- `qualifying_recovery`;
- `false_resume`;
- `false_stop`;
- evidence/provenance notes.

Optional telemetry fields are nullable:
- `duplicate_work_units_avoided`;
- `writes_reconciled`;
- `checkpoint_bytes`;
- `checkpoint_tool_calls`;
- `recovery_tool_calls`.

## Promotion counter semantics
The promotion counter uses **distinct qualified `incident_id` values**, not row count.

`genuine_incidents = COUNT(DISTINCT incident_id WHERE qualifying_recovery=true)`

`distinct_projects = COUNT(DISTINCT project_id WHERE qualifying_recovery=true)`

Decision law:
- any false resume -> `HOLD`;
- zero qualified genuine incidents -> `HOLD`;
- genuine incidents < 3 or projects < 2 -> `CONTINUE_PILOT`;
- qualified recovery false-stop rate > 10% -> `NARROW`;
- otherwise -> `ELIGIBLE_FOR_PROMOTION_REVIEW`.

`ELIGIBLE_FOR_PROMOTION_REVIEW` is not promotion.

## Backward compatibility
Run33 legacy events with unique `event_id` and no `incident_id` continue to behave as independent incidents. Existing three-real-event/two-project fixtures still become `ELIGIBLE_FOR_PROMOTION_REVIEW`.

## Required proofs
- P1: same incident + two projects => genuine incident count = 1, project count = 2.
- P2: same incident + three projects => genuine incident count remains 1.
- P3: three independent legacy incidents across two projects => review eligible.
- P4: duplicate recovery_id => reject.
- P5: same incident mixing real/synthetic => reject.
- P6: incomplete readback => does not qualify.
- P7: false resume => HOLD.
- P8: synthetic events alone => cannot satisfy threshold.
- P9: explicit qualification cannot bypass hard safety prerequisites.
- P10: three genuine incidents in one project => project-diversity gate remains unmet.
- P11: omitted telemetry => null.
- P12: explicitly observed numeric zero => zero, not null.
- P13: partially known telemetry aggregates only known rows.
- P14: inherited `tests/test_session_resilience_run33.py` remains green.

## Current real evidence interpretation
The 2026-08-22 browser-closure incident currently has two recovered project slices:
- `IVDIVO_SELF_IMPROVEMENT`;
- `BUSINESS_ENGINEERING`.

Under this contract it is exactly **1 genuine incident / 2 distinct projects / zero false resume**, therefore `CONTINUE_PILOT`. It must not become 2/3 merely because two projects were recovered.

## Rollback
If v1.1 regresses inherited Run33 behavior or misclassifies real incidents, revert the runtime/test/ledger delta and preserve the previously merged SI-0014 READY_FOR_PILOT state. Do not alter unrelated project authority.
