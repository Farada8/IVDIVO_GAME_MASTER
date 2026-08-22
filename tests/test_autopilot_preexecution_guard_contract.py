from pathlib import Path

from tools.ivdivo_preexecution_resume_guard import ProjectState, guard_resume


ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT / "IVDIVO_NARRATIVE_OS" / "13_CROSS_CONVERSATION_STATE_AND_AUTOPILOT.md"
AMENDMENT = ROOT / "IVDIVO_NARRATIVE_OS" / "13A_PRE_EXECUTION_RESUME_GUARD_CANONICAL_AMENDMENT_v1.0.md"


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
    state = ProjectState(project_id="D01", next_action="FOUNDER_LOCK_DECISION", terminal_or_decision_gate=True)
    assert guard_resume(
        active_project="D01",
        portfolio_next_action="E97",
        project_state=state,
    ) == "STOP_REBASE_REQUIRED"


def test_runtime_allows_matching_project_frontier():
    state = ProjectState(project_id="D01", next_action="FOUNDER_LOCK_DECISION", terminal_or_decision_gate=True)
    assert guard_resume(
        active_project="D01",
        portfolio_next_action="FOUNDER_LOCK_DECISION",
        project_state=state,
    ) == "EXECUTE"


def test_runtime_requires_project_state():
    assert guard_resume(
        active_project="D01",
        portfolio_next_action="E97",
        project_state=None,
    ) == "STOP_NO_PROJECT_STATE"
