from tools.ivdivo_preexecution_resume_guard import guard_resume


def test_stale_active_project_requires_rebase():
    aggregate = {"portfolio_frontier": {"active_project": {"project_id": "D01", "next_unblocked_obligation": "E97_DRAFT"}}}
    project = {"project_id": "D01", "terminal_frontier": {"next_obligation": "FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}
    result = guard_resume(aggregate, project)
    assert result["decision"] == "STOP_REBASE_REQUIRED"


def test_matching_project_frontier_executes():
    aggregate = {"portfolio_frontier": {"active_project": {"project_id": "D01", "next_unblocked_obligation": "FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}}
    project = {"project_id": "D01", "terminal_frontier": {"next_obligation": "FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}
    result = guard_resume(aggregate, project)
    assert result == {
        "decision": "EXECUTE",
        "project_id": "D01",
        "next_action": "FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01",
    }


def test_non_active_project_is_not_quarantined():
    aggregate = {"portfolio_frontier": {"active_project": {"project_id": "D01", "next_unblocked_obligation": "X"}}}
    project = {"project_id": "D09", "next_safe_action": "FOUNDER_APPROVAL_OR_LOCK_D09_SEASON"}
    result = guard_resume(aggregate, project)
    assert result["decision"] == "PROJECT_NOT_ACTIVE"


def test_missing_project_state_fails_closed():
    aggregate = {"portfolio_frontier": {"active_project": {"project_id": "D01", "next_unblocked_obligation": "X"}}}
    result = guard_resume(aggregate, None)
    assert result["decision"] == "STOP_NO_PROJECT_STATE"


def test_missing_aggregate_frontier_fails_closed():
    aggregate = {"portfolio_frontier": {"active_project": {"project_id": "D01"}}}
    project = {"project_id": "D01", "next_safe_action": "X"}
    result = guard_resume(aggregate, project)
    assert result["decision"] == "STOP_NO_PROJECT_FRONTIER"
