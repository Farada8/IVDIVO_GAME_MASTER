from IVDIVO_NARRATIVE_OS.tools.local_gate_router import Obligation, route


def test_human_gate_does_not_stop_independent_work():
    decision = route([
        Obligation("P003B_HUMAN_LISTEN", 1, "BLOCKED", "HUMAN_EVIDENCE_REQUIRED"),
        Obligation("AUTOPILOT_ROUTER_REGRESSION", 2, "READY"),
    ])
    assert decision.action == "CONTINUE"
    assert decision.selected_id == "AUTOPILOT_ROUTER_REGRESSION"
    assert decision.blocked_local == ("P003B_HUMAN_LISTEN",)


def test_provider_gate_does_not_stop_independent_work():
    decision = route([
        Obligation("RU_PROVIDER_AUTH", 1, "BLOCKED", "EXTERNAL_PROVIDER_REQUIRED"),
        Obligation("SOUND_BINDING_SCHEMA_QA", 2, "READY"),
    ])
    assert decision.action == "CONTINUE"
    assert decision.selected_id == "SOUND_BINDING_SCHEMA_QA"


def test_global_authority_conflict_stops():
    decision = route([
        Obligation("CANON_CONFLICT", 1, "BLOCKED", "FRONTIER_CONFLICT"),
        Obligation("DOWNSTREAM_WRITE", 2, "READY"),
    ])
    assert decision.action == "GLOBAL_STOP"
    assert decision.selected_id is None


def test_dependency_not_done_is_not_ready():
    decision = route([
        Obligation("SOURCE", 1, "BLOCKED", "MISSING_INPUT"),
        Obligation("CONSUMER", 2, "READY", dependencies=("SOURCE",)),
        Obligation("INDEPENDENT", 3, "READY"),
    ])
    assert decision.action == "CONTINUE"
    assert decision.selected_id == "INDEPENDENT"


def test_only_local_blockers_reports_no_ready_sibling():
    decision = route([
        Obligation("HUMAN", 1, "BLOCKED", "HUMAN_EVIDENCE_REQUIRED"),
        Obligation("BYTES", 2, "BLOCKED", "MISSING_INPUT"),
    ])
    assert decision.action == "LOCAL_GATE_ONLY_NO_READY_SIBLING"
