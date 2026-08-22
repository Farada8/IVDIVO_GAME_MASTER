import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "runtime" / "pod_cost_preflight.py"
spec = importlib.util.spec_from_file_location("pod_cost_preflight", MOD)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_landscape_4x6_is_256_dpi():
    a = m.Asset(1536, 1024, False, False)
    assert round(m.effective_dpi(a, 6, 4), 1) == 256.0


def test_portrait_4x6_is_256_dpi():
    a = m.Asset(1024, 1536, True, False)
    assert round(m.effective_dpi(a, 4, 6), 1) == 256.0


def test_5x7_crop_stays_above_150():
    a = m.Asset(1024, 1536, True, False)
    assert m.effective_dpi(a, 5, 7) > 150


def test_8x12_is_below_minimum():
    a = m.Asset(1024, 1536, True, True)
    assert round(m.effective_dpi(a, 8, 12), 1) == 128.0
    assert m.route_asset(a, 8, 12) == "HOLD_RESOLUTION"


def test_board_is_not_promoted_by_resolution_alone():
    a = m.Asset(1536, 1024, False, True)
    assert m.route_asset(a, 6, 4) == "HOLD_CREATE_CLEAN_MASTER"


def test_artwork_without_provenance_stays_hold():
    a = m.Asset(1024, 1536, True, False)
    assert m.route_asset(a, 4, 6) == "HOLD_PROVENANCE"


def test_clean_provenance_small_asset_can_reach_internal_mockup_only():
    a = m.Asset(1024, 1536, True, True)
    assert m.route_asset(a, 4, 6) == "ENGINEERING_ELIGIBLE_INTERNAL_MOCKUP"


def test_poster_sensitivity_not_profit_proof():
    c = m.pre_cac_contribution(24.90, 6.54, 5.79)
    assert 10.0 < c < 10.6
    assert not m.can_claim_profitable_sku(paid_orders=0, wtp_observed=False, cac_observed=False, conversion_observed=False, contribution_after_cac_positive=None)


def test_three_card_shipping_increment_is_modeled():
    c = m.pre_cac_contribution(17.90, 1.57 * 3, 4.09, extra_shipping_usd=0.20)
    assert 6.9 < c < 7.4


def test_market_proof_requires_all_observed_fields():
    assert not m.can_claim_profitable_sku(paid_orders=10, wtp_observed=True, cac_observed=False, conversion_observed=True, contribution_after_cac_positive=True)
    assert m.can_claim_profitable_sku(paid_orders=10, wtp_observed=True, cac_observed=True, conversion_observed=True, contribution_after_cac_positive=True)


def test_cost_freshness_guard_before_announced_change():
    assert m.costs_are_fresh("2026-08-22")


def test_cost_freshness_guard_after_announced_change():
    assert not m.costs_are_fresh("2026-08-27")
