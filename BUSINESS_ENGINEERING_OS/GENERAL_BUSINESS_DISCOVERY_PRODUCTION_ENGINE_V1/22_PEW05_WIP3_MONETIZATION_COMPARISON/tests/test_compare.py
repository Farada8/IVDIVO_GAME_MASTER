import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pew05_compare", ROOT / "02_compare.py")
mod = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(mod)


def test_all_three_route_to_m1_without_wtp_promotion():
    result = mod.compare()
    assert result["all_three_route_m1"] is True
    assert set(result["routes"]) == {"OW-01", "CF-01", "CF-03"}
    for item in result["routes"].values():
        assert item["route"] == mod.EXPECTED_M1
        assert item["buyer_demand_proven"] is False
        assert item["wtp"] is None
        assert item["price"] is None
        assert item["transactions"] == 0
        assert item["external_action_authorized"] is False


def test_portfolio_roles_stay_wip3():
    p = mod.compare()["portfolio_decision"]
    assert p["PRIMARY"] == "OW-01"
    assert p["PILOT_A"] == "CF-01"
    assert p["PILOT_B"] == "CF-03"
    assert p["wip_count"] == 3
    assert p["add_fourth_opportunity"] is False


def test_equal_route_does_not_claim_equal_evidence_strength():
    result = mod.compare()
    assert result["evidence_strength_equal"] is False
    assert result["routes"]["OW-01"]["fixture_plane"] == "REAL_PUBLIC_PLUS_INTERNAL_ENGINEERING"
    assert result["routes"]["CF-01"]["fixture_plane"] == "SYNTHETIC_INTERNAL_ENGINEERING"
    assert result["routes"]["CF-03"]["fixture_plane"] == "SYNTHETIC_INTERNAL_ENGINEERING"


def test_next_frontier_is_internal_p_ew06():
    assert mod.compare()["next_frontier"] == "P-EW06_FIXED_SCOPE_DIAGNOSTIC_DELIVERY_SPECS_CF01_CF03"


def test_proof_boundary_remains_fail_closed():
    proof = mod.compare()["proof_boundary"]
    assert proof["buyer_demand_proven"] is False
    assert proof["wtp"] is None
    assert proof["price"] is None
    assert proof["transactions"] == 0
    assert proof["profitability_proven"] is False
    assert proof["external_action_authorized"] is False
