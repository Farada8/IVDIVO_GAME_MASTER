import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from monetization_ladder import MonetizationEvidence, route

STATE = ROOT / "20_MONETIZATION_LADDER_STATE.json"
P3 = ROOT / "19_AI_ACT_ART50_TECHNICAL_TRANSPARENCY_PACK" / "03_MACHINE_STATE.json"
P4 = ROOT / "20_DPP_REGISTRY_PREFLIGHT" / "03_MACHINE_STATE.json"
P5 = ROOT / "22_PEW05_WIP3_MACHINE_STATE.json"
CURRENT = ROOT.parent / "CURRENT_GENERAL_BUSINESS_ENGINE.md"


def evidence(oid):
    return MonetizationEvidence(
        opportunity_id=oid,
        technical_artifact=True,
        nontrivial_delta=True,
        buyer_role_plausible=True,
        paid_diagnostic_transactions=0,
        paid_implementation_transactions=0,
        paid_recurring_cycles=0,
        independent_customer_contexts_same_workflow=0,
        external_action_authorized=False,
    )


def test_all_three_wip_routes_are_m1_not_m2():
    for oid in ("OW-01", "CF-01", "CF-03"):
        r = route(evidence(oid))
        assert r["disposition"] == "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN"
        assert r["evidence"]["paid_diagnostic_transactions"] == 0


def test_m1_does_not_authorize_external_action():
    for oid in ("OW-01", "CF-01", "CF-03"):
        assert route(evidence(oid))["proof_boundary"]["external_action_authorized"] is False


def test_current_state_records_all_three_as_m1():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["p_ew05"]["m1_count"] == 3
    assert state["p_ew05"]["m2_or_higher_count"] == 0
    for oid in ("OW-01", "CF-01", "CF-03"):
        assert state["current_routes"][oid]["technical_artifact"] is True
        assert state["current_routes"][oid]["nontrivial_delta"] is True
        assert state["current_routes"][oid]["route"] == "M1_FIXED_SCOPE_DIAGNOSTIC_SPEC_READY_NOT_WTP_PROVEN"
        assert state["current_routes"][oid]["price"] is None
        assert state["current_routes"][oid]["wtp"] is None


def test_p_ew03_and_p_ew04_authority_is_closed_and_pinned():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    p3 = json.loads(P3.read_text(encoding="utf-8"))
    p4 = json.loads(P4.read_text(encoding="utf-8"))
    assert state["inputs"]["article50_p_ew03_merge_sha"] == "3f65b522c59a7cdc988cbae893c1d54651eab6e6"
    assert state["inputs"]["dpp_p_ew04_merge_sha"] == "8797476c45ac38bc9eb9bfbe8a3b1d9c27f1a7d7"
    assert p3["status"] == "ENGINEERING_PASS_CI_SUCCESS_M1_ELIGIBLE_NOT_WTP_PROVEN"
    assert p3["engineering_proof"]["dedicated_ci"] == "SUCCESS"
    assert p4["status"] == "ENGINEERING_PASS_CI_SUCCESS_M1_ELIGIBLE_NOT_WTP_PROVEN"
    assert p4["engineering_proof"]["dedicated_ci"] == "SUCCESS"


def test_no_commercial_winner_or_external_authorization_is_fabricated():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    p5 = json.loads(P5.read_text(encoding="utf-8"))
    assert state["p_ew05"]["decision"] == "NO_COMMERCIAL_WINNER_YET"
    assert state["proof_boundary"]["buyer_demand"] == "UNPROVEN"
    assert state["proof_boundary"]["wtp"] is None
    assert state["proof_boundary"]["transactions_from_bridge"] == 0
    assert state["external_action"]["authorized"] is False
    assert p5["decision"]["market_winner_proven"] is False
    assert p5["proof_boundary"]["external_action_authorized"] is False


def test_test_sequence_is_not_market_ranking():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    p5 = json.loads(P5.read_text(encoding="utf-8"))
    assert state["p_ew05"]["next_real_world_test_sequence"] == ["OW-01", "CF-01", "CF-03"]
    assert state["p_ew05"]["sequence_is_market_ranking"] is False
    assert p5["decision"]["next_bounded_wtp_test_candidate"] == "OW-01"
    assert p5["decision"]["next_sequence_is_market_ranking"] is False


def test_current_pointer_no_longer_routes_to_stale_pew03():
    text = CURRENT.read_text(encoding="utf-8")
    assert "P-EW01–P-EW05 INTERNAL ENGINEERING CLOSED" in text
    assert "P-EW03 = PASS_ENGINEERING" in text
    assert "P-EW04 = PASS_ENGINEERING" in text
    assert "P-EW05 = INTERNAL_DECISION_ALL_M1" in text
    assert "EXTERNAL_ACTION_AUTHORIZED = FALSE" in text
    assert "P-EW03 = NEXT" not in text
