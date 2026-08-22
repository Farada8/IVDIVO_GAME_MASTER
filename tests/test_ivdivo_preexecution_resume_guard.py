from tools.ivdivo_preexecution_resume_guard import guard_resume


def agg(project='D01', nxt='WRITE_E97'):
    return {'portfolio_frontier': {'active_project': {'project_id': project, 'next_unblocked_obligation': nxt}}}


def test_stale_d01_is_blocked():
    p={'project_id':'D01','next_safe_action':'FOUNDER_LOCK_DECISION'}
    assert guard_resume(agg(), p)['decision']=='STOP_REBASE_REQUIRED'


def test_matching_d01_executes():
    p={'project_id':'D01','next_safe_action':'FOUNDER_LOCK_DECISION'}
    assert guard_resume(agg(nxt='FOUNDER_LOCK_DECISION'), p)['decision']=='EXECUTE'


def test_unrelated_project_is_not_active():
    p={'project_id':'D09','next_safe_action':'FOUNDER_APPROVAL_OR_LOCK_D09_SEASON'}
    assert guard_resume(agg(), p)['decision']=='PROJECT_NOT_ACTIVE'


def test_missing_project_state_fails_closed():
    assert guard_resume(agg(), None)['decision']=='STOP_NO_PROJECT_STATE'


def test_missing_aggregate_frontier_fails_closed():
    assert guard_resume({}, {'project_id':'D01','next_safe_action':'X'})['decision']=='STOP_NO_PROJECT_FRONTIER'
