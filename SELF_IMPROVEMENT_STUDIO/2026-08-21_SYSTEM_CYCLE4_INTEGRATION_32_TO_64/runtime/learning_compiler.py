from __future__ import annotations
FORBIDDEN_KEYS={"character_names","exact_clue_chain","voice_ids","exact_melody","project_asset_ids","private_story_timing"}
def compile_learning(observation:dict)->dict:
    leak=[k for k in FORBIDDEN_KEYS if observation.get(k)]
    if leak:return {"status":"REJECT_PROJECT_LEAKAGE","leaks":sorted(leak)}
    required=("mechanism","evidence","applicability","failure_conditions","provenance")
    missing=[k for k in required if not observation.get(k)]
    if missing:return {"status":"HOLD_INCOMPLETE","missing":missing}
    return {"status":"CANDIDATE","mechanism":observation["mechanism"],"evidence":observation["evidence"],"applicability":observation["applicability"],"failure_conditions":observation["failure_conditions"],"provenance":observation["provenance"]}
