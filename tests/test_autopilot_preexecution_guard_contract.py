from pathlib import Path

from tools.ivdivo_preexecution_resume_guard import guard_resume


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "IVDIVO_NARRATIVE_OS" / "13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md"
AMENDMENT = ROOT / "IVDIVO_NARRATIVE_OS" / "13A_PRE_EXECUTION_RESUME_GUARD_CANONICAL_AMENDMENT_v1.0.md"


def agg(project="D01", nxt="WRITE_E97"):
    return {
        "portfolio_frontier": {
            "active_project": {
                "project_id": project,
                "next_unblocked_obligation": nxt,
            }
        }
    }


def test_parent_canonical_control_layer_exists():
    text = PARENT.read_text(encoding="utf-8")
    assert "CANONICAL OPERATIONAL CONTROL LAYER" in text
    assert "SELECT HIGHEST UNBLOCKED OBLIGATION" in text


def test_amendment_binds_guard_before_selection():
    text = AMENDMENT.read_text(encoding="utf-8")
    guard = text.index("PRE_EXECUTION_RESUME_GUARD")
    select = text.index("SELECT HIGHEST UNBLOCKED OBLIGATION")
    assert guard < select
    assert "PROJECT-SPECIFIC PERSISTED FRONTIER > STALE AGGREGATE ROUTER POINTER" in text
    assert "does not create a second router" in text


def test_runtime_fail_closed_on_stale_pointer():
    result = guard_resume(
        agg(nxt="WRITE_E97"),
        {"project_id": "D01", "next_safe_action": "FOUNDER_LOCK_DECISION"},
    )
    assert result["decision"] == "STOP_REBASE_REQUIRED"


def test_runtime_allows_matching_project_frontier():
    result = guard_resume(
        agg(nxt="FOUNDER_LOCK_DECISION"),
        {"project_id": "D01", "next_safe_action": "FOUNDER_LOCK_DECISION"},
    )
    assert result["decision"] == "EXECUTE"


def test_runtime_requires_project_state():
    result = guard_resume(agg(), None)
    assert result["decision"] == "STOP_NO_PROJECT_STATE"
