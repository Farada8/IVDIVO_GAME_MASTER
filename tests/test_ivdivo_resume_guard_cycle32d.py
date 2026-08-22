import importlib.util
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("ivdivo_resume_guard", ROOT/"tools"/"ivdivo_resume_guard.py")
MOD=importlib.util.module_from_spec(SPEC); assert SPEC and SPEC.loader; SPEC.loader.exec_module(MOD)
gate_resume=MOD.gate_resume


def test_stale_d01_quarantined():
    aggregate={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"E97_DRAFT"}}}
    project={"project_id":"D01","terminal_frontier":{"next_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01","do_not_generate":"E121"}}
    assert gate_resume(aggregate,project)["decision"]=="STOP_REBASE_REQUIRED"


def test_matching_d01_executes_project_frontier():
    aggregate={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}}
    project={"project_id":"D01","terminal_frontier":{"next_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}
    out=gate_resume(aggregate,project)
    assert out["decision"]=="EXECUTE"
    assert out["selected_next_action"]=="FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"


def test_d09_nonactive_no_false_quarantine():
    aggregate={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"X"}}}
    project={"project_id":"D09","next_safe_action":"FOUNDER_APPROVAL_OR_LOCK_D09_SEASON"}
    assert gate_resume(aggregate,project)["decision"]=="PROJECT_NOT_ACTIVE"


def test_d04_nonactive_no_false_quarantine():
    aggregate={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"X"}}}
    project={"project_id":"D04","next_action":"REAL_HUMAN_BLIND_TRANSFER_LISTEN_RESPONSE"}
    assert gate_resume(aggregate,project)["decision"]=="PROJECT_NOT_ACTIVE"


def test_missing_project_frontier_fails_closed():
    aggregate={"portfolio_frontier":{"active_project":{"project_id":"D01"}}}
    project={"project_id":"D01"}
    assert gate_resume(aggregate,project)["decision"]=="STOP_NO_PROJECT_FRONTIER"
