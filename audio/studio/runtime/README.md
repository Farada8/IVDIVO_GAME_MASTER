# Runtime — WORKING v0.1

Executable extensions behind the canonical `audio/studio/orchestrator.py` stage/gate contract.

Current modules:
- `scene_state_graph.py` — multi-layer scene-state validator.
- `performance_compiler.py` — Scene State Graph -> performance/rhythm/provider-context artifacts.
- `performance_qc.py` — mechanical WAV performance/regression QC.
- `learning_registry.py` — controlled evidence-based production learning.

These modules are provider-independent and make no paid/live calls.

Pilot test:
```bash
python runtime/scene_state_graph.py SCENE_STATE_GRAPH.json --output VALIDATION.json
python runtime/performance_compiler.py SCENE_STATE_GRAPH.json OUT_DIR
python runtime/performance_qc.py candidate.wav --plan OUT_DIR/RHYTHM_PAUSE_BREATH_PLAN.json --baseline regression.json --output QC.json
```

Do not promote runtime heuristics into canon automatically. Use `learning_registry.py` and explicit review.
