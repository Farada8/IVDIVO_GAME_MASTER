from tools.ivdivo_state_convergence import audit


def A(pid, aid, cls, state, action, **kw):
    data = {
        "project_id": pid,
        "artifact_id": aid,
        "authority_class": cls,
        "state": state,
        "next_action": action,
    }
    data.update(kw)
    return data


def test_book2_stale_draft_status_is_flagged():
    result = audit({"artifacts": [
        A("B02", "draft", "PROJECT_SPECIFIC_EXECUTION_STATE_OR_DRAFT_STATUS", "ACTIVE", "READER_ADVOCATE_CONTINUOUS_READ"),
        A("B02", "final_gate", "PROJECT_SOURCE_OF_TRUTH_OR_TERMINAL_GATE", "EXTERNAL_FEEDBACK_READY", "EXTERNAL_FEEDBACK", terminal=True),
    ]})
    project = result["projects"][0]
    assert project["selected_authority"] == "final_gate"
    assert any(i["type"] == "STALE_LOWER_AUTHORITY_POINTER" for i in project["issues"])
    assert any(i["type"] == "TERMINAL_GATE_OVERRIDES_ACTIVE_POINTER" for i in project["issues"])


def test_d09_founder_gate_routes_stop_not_more_prose():
    result = audit({"artifacts": [
        A("D09", "system_state", "CURRENT_IVDIVO_SYSTEM_STATE", "FOUNDER_LOCK_DECISION_GATE", "FOUNDER_APPROVAL_OR_LOCK_D09_SEASON", terminal=True),
    ]})
    assert result["projects"][0]["status"] == "PASS"
    assert result["projects"][0]["selected_next_action"] == "FOUNDER_APPROVAL_OR_LOCK_D09_SEASON"


def test_d04_provider_gate_is_preserved():
    result = audit({"artifacts": [
        A("D04", "exec", "PROJECT_SPECIFIC_EXECUTION_STATE_OR_DRAFT_STATUS", "EXTERNAL_PROVIDER_REQUIRED", "BIND_REAL_CANDIDATE_IDS_AND_RUN_S0", terminal=True),
        A("D04", "mirror", "CURRENT_PROMPTS_AND_WORKSTATE_MIRRORS", "ACTIVE", "FULL_E01_RENDER"),
    ]})
    project = result["projects"][0]
    assert project["selected_next_action"] == "BIND_REAL_CANDIDATE_IDS_AND_RUN_S0"
    assert any(i["type"] == "STALE_LOWER_AUTHORITY_POINTER" for i in project["issues"])


def test_same_precedence_conflict_fails_closed():
    result = audit({"artifacts": [
        A("X", "a", "PROJECT_SOURCE_OF_TRUTH_OR_TERMINAL_GATE", "ACTIVE", "A"),
        A("X", "b", "PROJECT_SOURCE_OF_TRUTH_OR_TERMINAL_GATE", "ACTIVE", "B"),
    ]})
    assert result["projects"][0]["status"] == "FAIL_CLOSED"
    assert any(i["type"] == "AUTHORITY_UNRESOLVED_SAME_PRECEDENCE" for i in result["projects"][0]["issues"])


def test_source_revision_collision_requests_rebase():
    result = audit({"artifacts": [
        A("X", "a", "PROJECT_SPECIFIC_EXECUTION_STATE_OR_DRAFT_STATUS", "ACTIVE", "DO", expected_source_revision="old", observed_source_revision="new"),
    ]})
    assert any(i["type"] == "STALE_SOURCE_REVISION" and i["disposition"] == "REBASE_DO_NOT_OVERWRITE" for i in result["projects"][0]["issues"])


def test_healthy_active_state_has_no_false_positive():
    result = audit({"artifacts": [
        A("D10", "exec", "PROJECT_SPECIFIC_EXECUTION_STATE_OR_DRAFT_STATUS", "ACTIVE", "CONTINUE_CURRENT_TEXT_FRONTIER"),
    ]})
    assert result["projects"][0]["status"] == "PASS"
