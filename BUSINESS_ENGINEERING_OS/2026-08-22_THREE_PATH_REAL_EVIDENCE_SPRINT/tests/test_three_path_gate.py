import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("three_path_gate", ROOT / "engine" / "three_path_gate.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def test_direct_real_lead_not_primary():
    p = {"kind": "DIRECT_SERVICE", "real_lead_signal": True, "reply_observed": False, "quote_request_observed": False, "order_observed": False}
    assert MOD.route_path(p) == "CONDITIONAL_FRONT_RUNNER_REAL_LEAD_SIGNAL"
    assert MOD.may_promote_primary(p) is False


def test_direct_order_can_cross_promotion_gate():
    p = {"kind": "DIRECT_SERVICE", "real_lead_signal": True, "order_observed": True}
    assert MOD.may_promote_primary(p) is True


def test_procurement_without_current_pack_holds():
    p = {"kind": "PROCUREMENT", "current_pack_acquired": False, "capability_join_ready": False}
    assert MOD.route_path(p) == "EXPLORE_CURRENT_PACK_FIRST"
    assert MOD.may_promote_primary(p) is False


def test_historical_pack_cannot_substitute_for_current_pack():
    p = {"kind": "PROCUREMENT", "current_pack_acquired": False, "historical_pack_present": True, "capability_join_ready": True}
    assert MOD.route_path(p) == "EXPLORE_CURRENT_PACK_FIRST"


def test_procurement_current_pack_and_join_can_advance():
    p = {"kind": "PROCUREMENT", "current_pack_acquired": True, "capability_join_ready": True}
    assert MOD.may_promote_primary(p) is True


def test_sme_public_support_without_real_workflow_holds():
    p = {"kind": "SME_IMPLEMENTATION", "real_workflow_packet": False, "operator_pain_observed": False}
    assert MOD.route_path(p) == "HOLD_REAL_WORKFLOW_PACKET_REQUIRED"
    assert MOD.may_promote_primary(p) is False


def test_sme_workflow_without_pain_still_holds():
    p = {"kind": "SME_IMPLEMENTATION", "real_workflow_packet": True, "operator_pain_observed": False}
    assert MOD.route_path(p) == "HOLD_OPERATOR_PAIN_EVIDENCE_REQUIRED"


def test_sme_real_pilot_request_can_cross_promotion_gate():
    p = {"kind": "SME_IMPLEMENTATION", "real_workflow_packet": True, "operator_pain_observed": True, "pilot_request_observed": True}
    assert MOD.may_promote_primary(p) is True


def test_unknown_path_fails_closed():
    assert MOD.route_path({"kind": "UNKNOWN"}) == "HOLD_UNKNOWN_PATH"
