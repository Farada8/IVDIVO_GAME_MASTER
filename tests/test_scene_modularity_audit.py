from tools.scene_modularity_audit import audit


def test_strong_causal_block_detects_dependencies():
    data={"initial_state":[],"scenes":[
        {"scene_id":"S1","requires":[],"provides":["KEY"]},
        {"scene_id":"S2","requires":["KEY"],"provides":["ACCESS"]},
        {"scene_id":"S3","requires":["ACCESS"],"provides":["PROOF"]},
    ]}
    r=audit(data)
    assert r["delete_tests"][0]["essential_by_declared_dependency"] is True
    assert r["swap_tests"][0]["verdict"] == "SWAP_BREAKS_DECLARED_CAUSALITY"


def test_modular_filler_surfaces_review():
    data={"scenes":[
        {"scene_id":"S1","requires":[],"provides":[]},
        {"scene_id":"S2","requires":[],"provides":[]},
        {"scene_id":"S3","requires":[],"provides":[]},
    ]}
    r=audit(data)
    assert "NO_SCENE_HAS_DECLARED_DOWNSTREAM_DEPENDENCY" in r["issues"]
    assert r["status"] == "REVIEW"


def test_parallel_montage_is_not_false_failed_for_reordering():
    data={"scenes":[
        {"scene_id":"M1","structure_kind":"PARALLEL_OR_MONTAGE","requires":[],"provides":["A"]},
        {"scene_id":"M2","structure_kind":"PARALLEL_OR_MONTAGE","requires":[],"provides":["B"]},
    ]}
    r=audit(data)
    assert r["swap_tests"][0]["verdict"] == "LEGITIMATELY_REORDERABLE_PARALLEL"
