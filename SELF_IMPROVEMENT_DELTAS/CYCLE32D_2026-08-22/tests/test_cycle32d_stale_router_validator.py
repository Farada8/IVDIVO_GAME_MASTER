import importlib.util
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "tools" / "cycle32d_stale_router_validator.py"
spec = importlib.util.spec_from_file_location("cycle32d_stale_router_validator", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(module)
validate_frontier = module.validate_frontier


def test_d01_stale_router_is_quarantined():
    aggregate = {"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"E97_DRAFT"}}}
    project = {"project_id":"D01","terminal_frontier":{"next_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01","do_not_generate":"E121"}}
    result = validate_frontier(aggregate, project)
    assert result["decision"] == "QUARANTINE"
    assert any(x["code"] == "STALE_ROUTER_POINTER" for x in result["findings"])


def test_matching_frontier_is_allowed():
    aggregate = {"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}}
    project = {"project_id":"D01","terminal_frontier":{"next_obligation":"FOUNDER_EXPLICIT_LOCK_DECISION_FOR_D01"}}
    result = validate_frontier(aggregate, project)
    assert result["decision"] == "ALLOW"


def test_different_project_is_not_applicable():
    aggregate = {"portfolio_frontier":{"active_project":{"project_id":"D01","next_unblocked_obligation":"X"}}}
    project = {"project_id":"D10","next_unblocked_obligation":"Y"}
    result = validate_frontier(aggregate, project)
    assert result["decision"] == "NOT_APPLICABLE"
