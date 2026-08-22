import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
import validator

def packet():
    return json.loads((ROOT / "02_SYNTHETIC_DPP_CASES.json").read_text(encoding="utf-8"))

def cases():
    return packet()["cases"]

def by_id(cid):
    return next(x for x in cases() if x["case_id"] == cid)

def finding(result, rule_id):
    return next(x for x in result["findings"] if x["rule_id"] == rule_id)

def test_exactly_six_synthetic_cases():
    assert len(cases()) == 6

def test_complete_battery_fixture_is_preflight_ready_not_registered():
    r = validator.validate_case(by_id("BATTERY_COMPLETE_SYNTHETIC"))
    assert r["disposition"] == "READY_FOR_TEST_ENVIRONMENT_PREFLIGHT"
    assert r["gap_count"] == 0
    assert r["registry_submission_performed"] is False
    assert r["registry_registration_proven"] is False
    assert r["legal_compliance_proven"] is False

def test_imported_fixture_routes_unresolved_commodity_code():
    r = validator.validate_case(by_id("IMPORTED_MISSING_COMMODITY"))
    assert finding(r, "DPP-I02")["status"] == validator.UNKNOWN
    assert r["disposition"] == "HOLD_UNRESOLVED_EVIDENCE"

def test_supplier_provenance_gap_is_machine_readable():
    r = validator.validate_case(by_id("SUPPLIER_PROVENANCE_GAP"))
    assert finding(r, "DPP-S01")["status"] == validator.FAIL
    assert r["disposition"] == "HOLD_DATA_GAPS"
    assert any(x["owner"] == "SUPPLY_CHAIN" for x in r["chase_list"])

def test_unknown_applicability_fails_closed():
    r = validator.validate_case(by_id("APPLICABILITY_UNKNOWN"))
    assert r["disposition"] == "HOLD_APPLICABILITY_UNKNOWN"
    assert r["legal_applicability_proven_by_tool"] is False

def test_missing_decentralised_pointer_holds():
    r = validator.validate_case(by_id("DECENTRALISED_POINTER_GAP"))
    assert finding(r, "DPP-L02")["status"] == validator.FAIL
    assert r["disposition"] == "HOLD_DATA_GAPS"

def test_future_textile_fixture_is_prep_only():
    r = validator.validate_case(by_id("FUTURE_PRODUCT_PREP_ONLY"))
    assert r["disposition"] == "PREP_ONLY_NOT_CURRENT_LEGAL_REQUIREMENT"
    assert r["legal_compliance_proven"] is False

def test_registry_generated_identifier_cannot_be_fabricated_before_registration():
    c = copy.deepcopy(by_id("BATTERY_COMPLETE_SYNTHETIC"))
    c["registry_generated_uri_before_registration"] = True
    r = validator.validate_case(c)
    assert finding(r, "DPP-R01")["status"] == validator.FAIL
    assert r["disposition"] == "HOLD_DATA_GAPS"

def test_non_imported_fixture_does_not_require_commodity_code_in_this_contract():
    r = validator.validate_case(by_id("BATTERY_COMPLETE_SYNTHETIC"))
    assert finding(r, "DPP-I02")["status"] == validator.NOT_APPLICABLE

def test_unmapped_fixture_data_point_creates_chase():
    c = copy.deepcopy(by_id("BATTERY_COMPLETE_SYNTHETIC"))
    c["mapped_data_points"].remove("performance")
    r = validator.validate_case(c)
    assert finding(r, "DPP-D01")["status"] == validator.FAIL
    assert "performance" in finding(r, "DPP-D01")["message"]

def test_unknown_required_point_model_is_not_guessed():
    r = validator.validate_case(by_id("APPLICABILITY_UNKNOWN"))
    assert finding(r, "DPP-D01")["status"] == validator.UNKNOWN

def test_correction_loop_reduces_gap_without_market_promotion():
    before = copy.deepcopy(by_id("IMPORTED_MISSING_COMMODITY"))
    after = copy.deepcopy(before)
    after["commodity_code"] = "8507-SYNTHETIC"
    delta = validator.revalidate(before, after)
    assert delta["before_gap_count"] == 1
    assert delta["after_gap_count"] == 0
    assert delta["gap_delta"] == 1
    assert delta["after_disposition"] == "READY_FOR_TEST_ENVIRONMENT_PREFLIGHT"
    assert delta["implementation_delta_observed"] is True
    assert delta["market_proof_promotion"] is False

def test_invalid_applicability_enum_rejected():
    c = copy.deepcopy(by_id("BATTERY_COMPLETE_SYNTHETIC"))
    c["applicability_status"] = "PROBABLY"
    try:
        validator.validate_case(c)
    except ValueError:
        pass
    else:
        raise AssertionError("invalid applicability must be rejected")

def test_empty_supplier_set_is_a_gap_not_silent_pass():
    c = copy.deepcopy(by_id("BATTERY_COMPLETE_SYNTHETIC"))
    c["supplier_records"] = []
    r = validator.validate_case(c)
    assert finding(r, "DPP-S01")["status"] == validator.FAIL

def test_all_cases_preserve_external_action_and_market_proof_boundary():
    for r in validator.validate_many(cases()):
        assert r["external_action_authorized"] is False
        assert r["buyer_demand_proven"] is False
        assert r["wtp_proven"] is False
        assert r["transaction_proven"] is False

def test_packet_itself_claims_no_registry_submission():
    p = packet()
    assert p["status"] == "SYNTHETIC_DESIGN_ONLY_NOT_REGISTRY_SUBMISSION"
    assert p["proof_boundary"]["registry_submission_performed"] is False
    assert p["proof_boundary"]["legal_compliance_proven"] is False
