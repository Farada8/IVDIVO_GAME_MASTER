# ROOM917 E01 POST-RENDER ENGINEERING ENGINE v2

**Status:** PROJECT PILOT PASS / domain-promotion HOLD pending second-project replication.

## Objective

Convert post-render audio diagnosis from documents/checklists into a fail-closed executable pipeline:

`ASSET BYTES -> CUE LINEAGE -> ACCEPTED TIMING -> SIGNAL INTERVALS -> EVIDENCE CLASSIFICATION -> SELECTIVE REPAIR CONTRACT -> PATCH RENDER -> BYTE REGRESSION -> HUMAN LISTEN -> COMMERCIAL A/B/C`

## Modules

1. `cue_lineage_compiler.py`
   - validates semantic scene/block/cue truth;
   - rejects invented absolute timings unless timing evidence is ACCEPTED_ALIGNMENT or LIVE_TIMELINE.

2. `lineage_timing_resolver.py`
   - binds semantic block identities to accepted/live timings;
   - refuses low-authority timing.

3. Existing `P003A2_MASTER_ESCROW_v1/p003a2_interval_analyzer.py`
   - remains the signal-analysis authority;
   - emits canonical `start_seconds/end_seconds`;
   - this v2 engine deliberately reuses it instead of duplicating signal code.

4. `interval_classifier.py`
   - evidence-gated classification;
   - level alone never proves a defect;
   - unresolved timing -> UNKNOWN;
   - exact protected range -> preserve.

5. `selective_repair_planner.py`
   - creates only authorized room-bed patch contracts;
   - no cross-domain guessed repairs.

6. `room_bed_patch_renderer.py`
   - requires explicit asset path and gain;
   - modifies only authorized ranges;
   - preserves source format/duration.

7. `regression_gate.py`
   - verifies Scene3 and unauthorized ranges are byte-stable;
   - positive patch must actually change an authorized range;
   - unauthorized change = FAIL.

8. `post_render_pipeline.py`
   - orchestrates timing resolver -> existing analyzer -> classifier -> repair plan.

9. `post_render_router.py`
   - computes next stage from actual artifact availability;
   - Human P003B is never simulated.

10. `self_improvement_adapter.py`
   - packages the observed defect, tests and promotion boundary for the IVDIVO Self-Improvement Engine.

## Machine contracts

All inter-module interfaces are versioned JSON contracts under `contracts/`.
Canonical interval interface is `start_seconds/end_seconds`; legacy aliases are read-only compatibility.

## ROOM917 E01 current boundary

The Scene1/2 semantic lineage is production-grounded, but absolute block timing is unresolved.
The exact full master remains byte-inaccessible in the current session. Therefore:
- semantic lineage = usable now;
- exact P003A2 production intervals = blocked;
- no production patch is authorized yet;
- synthetic tests prove the engine behavior, not E01 repair locations.

## Promotion boundary

Project pilot PASS is supported by:
- source-derived 13-block semantic lineage;
- five unit tests;
- positive synthetic end-to-end selective repair regression PASS;
- negative unauthorized-change regression FAIL as required;
- actual interface defects caught and repaired while integrating with the existing P003A2 analyzer.

Domain promotion remains HOLD until the same engine runs on a second independent locked audio project and catches/repairs a real defect without project-specific leakage.
