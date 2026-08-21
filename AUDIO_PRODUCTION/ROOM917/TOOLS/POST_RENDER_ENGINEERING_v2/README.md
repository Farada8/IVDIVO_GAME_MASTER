# ROOM917 E01 POST-RENDER ENGINEERING v2

Status: PROJECT PILOT / executable engineering layer. Does not change locked story or authorize scale.

Pipeline:
`CURRENT_STATE -> SEMANTIC CUE LINEAGE -> LIVE/ACCEPTED TIMING -> P003A2 INTERVALS -> EVIDENCE CLASSIFICATION -> P004A SELECTIVE REPAIR CONTRACT -> PATCH RENDER -> REGRESSION GATE -> HUMAN P003B -> A/B/C -> SCALE`

Modules:
- `cue_lineage_compiler.py`: validates semantic/absolute cue lineage and forbids invented timestamps.
- `lineage_timing_resolver.py`: merges semantic lineage with ACCEPTED_ALIGNMENT/LIVE_TIMELINE only.
- `interval_classifier.py`: fail-closed evidence classification; level alone never authorizes a patch.
- `selective_repair_planner.py`: creates room-bed patch contracts only for safely authorized intervals.
- `room_bed_patch_renderer.py`: renders only authorized room-bed intervals using explicit asset+gain bindings.
- `regression_gate.py`: byte-level selective-repair regression guard; protects Scene3 and unpatched areas.
- `post_render_pipeline.py`: orchestrates timing -> existing P003A2 analyzer -> classification -> repair plan.
- `post_render_router.py`: computes next executable stage from actual evidence.
- `self_improvement_adapter.py`: converts the real ROOM917 failure/success into a bounded learning candidate.

Source-derived E01 Scene1/2 cue lineage:
`examples/ROOM917_E01_S01_S02_SEMANTIC_CUE_LINEAGE_v1.json`

Important:
- Semantic map has NO invented absolute timestamps.
- E01_S02_SIL001 remains semantic-only until exact live range is recovered.
- D003 is aggregate-proven, exact patch ranges are not.
- D004 stays candidate until direct evidence.
- D005 stays commercial hypothesis until human A/B/C.
- Domain promotion is HOLD until second-project replication.
