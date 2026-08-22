import importlib.util
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("c10", ROOT / "runtime/cycle10_governance.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_normal_envelope_passes():
    out = m.meta_wip_limiter(1, 2)
    assert out == {"status": "PASS_WIP_BOUNDED", "exception_used": False}


def test_overflow_fails_closed():
    out = m.meta_wip_limiter(2, 3)
    assert out == {"status": "STOP_WIP_LIMIT", "exception_used": False}


def test_founder_switch_is_explicit_exception():
    out = m.meta_wip_limiter(2, 3, founder_switched=True)
    assert out["status"] == "PASS_WIP_EXCEPTION"
    assert out["exception_used"] is True
    assert out["reason"] == "FOUNDER_SWITCH"


def test_prerequisite_is_explicit_exception():
    out = m.meta_wip_limiter(2, 3, prerequisite=True)
    assert out["status"] == "PASS_WIP_EXCEPTION"
    assert out["reason"] == "PREREQUISITE"


def test_production_blocked_is_explicit_exception():
    out = m.meta_wip_limiter(2, 3, production_blocked=True)
    assert out["status"] == "PASS_WIP_EXCEPTION"
    assert out["reason"] == "PRODUCTION_BLOCKED"


def test_existing_production_return_contract_unchanged():
    assert m.production_return(False, "book") == "RETURN_TO_PRODUCTION"
    assert m.production_return(True, None) == "HOLD_NO_RETURN_TARGET"
    assert m.production_return(True, "audio") == "META_BOUNDED_THEN_RETURN"
