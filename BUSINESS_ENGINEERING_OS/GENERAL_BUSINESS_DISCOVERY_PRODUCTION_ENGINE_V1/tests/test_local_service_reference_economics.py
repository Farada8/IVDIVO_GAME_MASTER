import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "runtime" / "local_service_reference_economics.py"
spec = importlib.util.spec_from_file_location("local_service_reference_economics", MOD)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def test_positive_reference_margin_without_verified_quote_stays_hold():
    c = m.ServiceCase(retail_price=3000, delivery_cost_before_acquisition=2240)
    assert m.pre_acquisition_contribution(c) == 760
    assert m.route(c) == "REFERENCE_ONLY_HOLD"


def test_negative_contribution_routes_hold_or_drop():
    c = m.ServiceCase(retail_price=2000, delivery_cost_before_acquisition=2240)
    assert m.route(c) == "HOLD_OR_DROP"


def test_verified_subcontract_route_needs_all_controls():
    c = m.ServiceCase(
        retail_price=3200,
        delivery_cost_before_acquisition=2200,
        verified_scope_quote=True,
        competency_ok=True,
        insurance_ok=True,
        responsibility_defined=True,
    )
    assert m.route(c) == "SUBCONTRACT_ELIGIBLE"


def test_missing_insurance_blocks_subcontract_even_with_margin():
    c = m.ServiceCase(
        retail_price=3200,
        delivery_cost_before_acquisition=2200,
        verified_scope_quote=True,
        competency_ok=True,
        insurance_ok=False,
        responsibility_defined=True,
    )
    assert m.route(c) == "REFERENCE_ONLY_HOLD"


def test_direct_route_needs_verified_cost_sheet():
    c = m.ServiceCase(retail_price=3000, delivery_cost_before_acquisition=2100, direct_cost_sheet_verified=True)
    assert m.route(c) == "DIRECT_ELIGIBLE"


def test_referral_route_needs_paying_partner_and_positive_economics():
    c = m.ServiceCase(
        retail_price=100,
        delivery_cost_before_acquisition=0,
        paying_referral_partner=True,
        referral_contribution=35,
    )
    assert m.route(c) == "REFERRAL_ONLY_ELIGIBLE"


def test_referral_without_positive_contribution_stays_hold():
    c = m.ServiceCase(
        retail_price=100,
        delivery_cost_before_acquisition=0,
        paying_referral_partner=True,
        referral_contribution=-1,
    )
    assert m.route(c) == "REFERENCE_ONLY_HOLD"


def test_synthetic_middle_scenario_ceiling():
    c = m.ServiceCase(retail_price=3000, delivery_cost_before_acquisition=2240)
    assert m.acquisition_ceiling(c) == 152


def test_nonpositive_contribution_has_zero_acquisition_ceiling():
    c = m.ServiceCase(retail_price=2200, delivery_cost_before_acquisition=2240)
    assert m.acquisition_ceiling(c) == 0.0


def test_real_acquisition_cost_cannot_be_set_without_close_rate():
    assert not m.can_set_real_max_acquisition_cost(None, 700)


def test_real_acquisition_cost_cannot_be_set_without_verified_contribution():
    assert not m.can_set_real_max_acquisition_cost(0.2, None)


def test_real_acquisition_cost_requires_both_observed_inputs():
    assert m.can_set_real_max_acquisition_cost(0.2, 700)
