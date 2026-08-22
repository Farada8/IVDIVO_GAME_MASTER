import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNTIME = ROOT / "runtime"
if str(RUNTIME) not in sys.path:
    sys.path.insert(0, str(RUNTIME))

from monetization_ladder import MonetizationEvidence, route

STATE = ROOT / "20_MONETIZATION_LADDER_STATE.json"


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


def test_p_ew03_and_p_ew04_authority_is_pinned():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["inputs"]["article50_p_ew03_merge_sha"] == "3f65b522c59a7cdc988cbae893c1d54651eab6e6"
    assert state["inputs"]["dpp_p_ew04_merge_sha"] == "8797476c45ac38bc9eb9bfbe8a3b1d9c27f1a7d7"


def test_no_commercial_winner_is_fabricated():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["p_ew05"]["decision"] == "NO_COMMERCIAL_WINNER_YET"
    assert state["proof_boundary"]["buyer_demand"] == "UNPROVEN"
    assert state["proof_boundary"]["wtp"] is None
    assert state["proof_boundary"]["transactions_from_bridge"] == 0


def test_strategic_primary_is_not_monetization_proof():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert state["p_ew05"]["strategic_primary"] == "OW-01"
    assert state["p_ew05"]["strategic_primary_reason"] == "EARLY_WAVE_PORTFOLIO_LOGIC_NOT_MONETIZATION_PROOF"


def test_cf01_and_cf03_only_promote_internally_from_m0_to_m1():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    assert sorted(state["p_ew05"]["internal_promotions"]) == ["CF-01:M0->M1", "CF-03:M0->M1"]
    assert state["p_ew05"]["kills"] == []


def test_price_remains_null_for_all_wip():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    for oid in ("OW-01", "CF-01", "CF-03"):
        assert state["current_routes"][oid]["price"] is None
        assert state["current_routes"][oid]["wtp"] is None
