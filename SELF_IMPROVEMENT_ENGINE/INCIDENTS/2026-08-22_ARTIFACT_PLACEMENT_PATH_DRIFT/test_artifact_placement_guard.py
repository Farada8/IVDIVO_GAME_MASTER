from artifact_placement_guard import (
    ArtifactPlacementInput,
    can_transition_to_done_verified,
    evaluate_artifact_placement,
)


def base(**overrides):
    data = dict(
        artifact_id="A1",
        expected_project_root_id="PROJECT",
        expected_parent_id="EXPECTED",
        actual_parent_ids=("EXPECTED",),
        start_here_updated=True,
        start_here_readback_contains_artifact=True,
        duplicate_or_legacy_conflict_resolved=True,
        cross_store_required=False,
        cross_store_pointer_verified=False,
    )
    data.update(overrides)
    return ArtifactPlacementInput(**data)


def test_happy_path_is_placement_verified():
    result = evaluate_artifact_placement(base())
    assert result["state"] == "PLACEMENT_VERIFIED"
    assert can_transition_to_done_verified(result)


def test_sibling_folder_mismatch_is_fail_closed():
    result = evaluate_artifact_placement(base(actual_parent_ids=("SIBLING",)))
    assert result["state"] == "PERSISTED_BUT_MISPLACED"
    assert "PARENT_MISMATCH" in result["failures"]
    assert not can_transition_to_done_verified(result)


def test_missing_start_here_update_blocks_done():
    result = evaluate_artifact_placement(base(start_here_updated=False))
    assert "START_HERE_NOT_UPDATED" in result["failures"]
    assert not result["done_verified_allowed"]


def test_failed_start_here_readback_blocks_done():
    result = evaluate_artifact_placement(
        base(start_here_updated=True, start_here_readback_contains_artifact=False)
    )
    assert "START_HERE_READBACK_MISSING" in result["failures"]
    assert not can_transition_to_done_verified(result)


def test_legacy_title_conflict_blocks_done():
    result = evaluate_artifact_placement(
        base(duplicate_or_legacy_conflict_resolved=False)
    )
    assert "DUPLICATE_OR_LEGACY_CONFLICT" in result["failures"]
    assert not can_transition_to_done_verified(result)


def test_required_cross_store_pointer_blocks_done():
    result = evaluate_artifact_placement(
        base(cross_store_required=True, cross_store_pointer_verified=False)
    )
    assert "CROSS_STORE_POINTER_MISSING" in result["failures"]
    assert not can_transition_to_done_verified(result)


def test_missing_artifact_is_not_persisted():
    result = evaluate_artifact_placement(base(artifact_id=""))
    assert result["state"] == "NOT_PERSISTED"
    assert not can_transition_to_done_verified(result)
