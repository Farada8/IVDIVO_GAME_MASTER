import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "runtime" / "trade_inquiry_prequal.py"
spec = importlib.util.spec_from_file_location("trade_inquiry_prequal", MOD)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def complete(**kw):
    d=dict(area="Dublin",property_type="semi",surface="masonry",condition="normal",access="normal",photos_available=True,timing="4_weeks",authority_to_request=True,contact_consent=True)
    d.update(kw)
    return m.Inquiry(**d)


def test_01_complete_case_prequalifies():
    assert m.route(complete()) == "PREQUALIFIED_FOR_SURVEY_QUOTE_PREP"


def test_02_missing_surface_needs_info():
    assert m.route(complete(surface=None)) == "NEED_MORE_INFO"


def test_03_missing_photos_needs_info():
    assert m.route(complete(photos_available=None)) == "NEED_MORE_INFO"


def test_04_unknown_access_forces_survey():
    assert m.route(complete(access="unknown")) == "SITE_SURVEY_REQUIRED"


def test_05_difficult_access_forces_survey():
    assert m.route(complete(access="difficult")) == "SITE_SURVEY_REQUIRED"


def test_06_heavy_failure_forces_survey():
    assert m.route(complete(condition="heavy_failure")) == "SITE_SURVEY_REQUIRED"


def test_07_structural_issue_goes_specialist():
    assert m.route(complete(structural_issue=True)) == "OUT_OF_SCOPE_SPECIALIST"


def test_08_specialist_access_goes_specialist():
    assert m.route(complete(specialist_access=True)) == "OUT_OF_SCOPE_SPECIALIST"


def test_09_outside_area_holds():
    assert m.route(complete(configured_area=False)) == "HOLD_OUTSIDE_AREA"


def test_10_no_consent_holds():
    assert m.route(complete(contact_consent=False)) == "HOLD_CONSENT_OR_AUTHORITY"


def test_11_no_authority_holds():
    assert m.route(complete(authority_to_request=False)) == "HOLD_CONSENT_OR_AUTHORITY"


def test_12_quote_checklist_never_created_for_specialist_case():
    assert m.quote_prep_checklist(complete(structural_issue=True)) == tuple()


def test_modeled_delta_is_positive_but_not_observed_proof():
    i=complete()
    assert m.modeled_time_delta(i) > 0
    assert not m.can_claim_real_time_saving(None, None, 0)


def test_real_time_claim_requires_observed_pair_and_n20():
    assert not m.can_claim_real_time_saving(12,3,19)
    assert m.can_claim_real_time_saving(12,3,20)
