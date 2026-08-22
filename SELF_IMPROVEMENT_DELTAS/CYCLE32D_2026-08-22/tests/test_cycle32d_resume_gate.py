import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(ROOT))
from cycle32d_resume_gate import select_next_obligation


def test_d01_stale_blocks():
    agg={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"E97_DRAFT"}}}
    pr={"project_id":"D01","terminal_frontier":{"next_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01","do_not_generate":"E121"}}
    r=select_next_obligation(agg,pr)
    assert r["decision"]=="STOP_REBASE_REQUIRED"
    assert r["selected_next_action"] is None


def test_d01_match_executes():
    agg={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}}
    pr={"project_id":"D01","terminal_frontier":{"next_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}
    r=select_next_obligation(agg,pr)
    assert r["decision"]=="EXECUTE"
    assert r["selected_next_action"]=="FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"


def test_d09_not_active():
    agg={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"X"}}}
    pr={"project_id":"D09","next_safe_action":"FOUNDER_APPROVAL_OR_LOCK_D09_SEASON"}
    assert select_next_obligation(agg,pr)["decision"]=="PROJECT_NOT_ACTIVE"


def test_d04_not_active():
    agg={"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"X"}}}
    pr={"project_id":"D04","next_action":"REAL_HUMAN_BLIND_TRANSFER_LISTEN_RESPONSE"}
    assert select_next_obligation(agg,pr)["decision"]=="PROJECT_NOT_ACTIVE"


def test_no_project_frontier_stops():
    agg={"portfolio_frontier":{"active_project":{"project_id":"D01"}}}
    pr={"project_id":"D01"}
    assert select_next_obligation(agg,pr)["decision"]=="STOP_NO_PROJECT_FRONTIER"
