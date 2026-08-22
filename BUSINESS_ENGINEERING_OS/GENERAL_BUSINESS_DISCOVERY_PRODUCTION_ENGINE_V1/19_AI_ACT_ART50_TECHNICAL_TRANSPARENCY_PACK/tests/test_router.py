import copy
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import router


def cases():
    return json.loads((ROOT / "02_SYNTHETIC_SAMPLE_PACKET.json").read_text(encoding="utf-8"))["cases"]


def decision(result, obligation_id):
    return next(x for x in result["decisions"] if x["obligation_id"] == obligation_id)


def test_provider_chatbot_routes_a50_1_and_cross_cutting():
    result = router.route_case(cases()[0])
    assert decision(result, "A50_1")["status"] == router.APPLIES
    assert result["article_50_5_cross_cutting"] is True
    assert result["legal_compliance_proven"] is False


def test_obvious_interaction_is_review_not_silent_exemption():
    case = copy.deepcopy(cases()[0])
    case["ai_interaction_obvious"] = True
    result = router.route_case(case)
    assert decision(result, "A50_1")["status"] == router.PENDING_EXCEPTION_REVIEW
    assert result["status"] == "HOLD_UNRESOLVED_SCOPE_OR_EXCEPTION"


def test_provider_generator_routes_a50_2():
    result = router.route_case(cases()[1])
    assert decision(result, "A50_2")["status"] == router.APPLIES
    assert "MachineReadableMarkingEvidence" in decision(result, "A50_2")["required_evidence"]
    assert result["code_route"] == "DOCUMENT_ALTERNATIVE_EQUIVALENTLY_ADEQUATE_MEASURES"


def test_legacy_generator_gets_narrow_a50_2_transition_before_deadline():
    case = copy.deepcopy(cases()[1])
    case["placed_on_market_before_2026_08_02"] = True
    case["assessment_date"] = "2026-08-22"
    result = router.route_case(case)
    d = decision(result, "A50_2")
    assert d["status"] == router.APPLIES_TRANSITIONAL
    assert "LegacyMarketPlacementEvidence" in d["required_evidence"]
    assert result["status"] == "TRANSITIONAL_IMPLEMENTATION_DEADLINE_ACTIVE"
    assert result["legal_compliance_proven"] is False


def test_legacy_generator_transition_expires_on_2026_12_02():
    case = copy.deepcopy(cases()[1])
    case["placed_on_market_before_2026_08_02"] = True
    case["assessment_date"] = "2026-12-02"
    result = router.route_case(case)
    assert decision(result, "A50_2")["status"] == router.APPLIES
    assert result["status"] == "IMPLEMENTATION_EVIDENCE_REQUIRED"


def test_transition_claim_without_assessment_date_fails_closed():
    case = copy.deepcopy(cases()[1])
    case["placed_on_market_before_2026_08_02"] = True
    case.pop("assessment_date", None)
    result = router.route_case(case)
    assert decision(result, "A50_2")["status"] == router.UNKNOWN
    assert result["status"] == "HOLD_UNRESOLVED_SCOPE_OR_EXCEPTION"


def test_marking_exception_claim_is_pending_review():
    case = copy.deepcopy(cases()[1])
    case["standard_editing_only"] = True
    result = router.route_case(case)
    assert decision(result, "A50_2")["status"] == router.PENDING_EXCEPTION_REVIEW


def test_deployer_emotion_recognition_routes_a50_3_and_separate_data_plane():
    result = router.route_case(cases()[2])
    d = decision(result, "A50_3")
    assert d["status"] == router.APPLIES
    assert "SeparatePersonalDataLegalReview" in d["required_evidence"]


def test_creative_deepfake_keeps_disclosure_special_regime():
    result = router.route_case(cases()[3])
    d = decision(result, "A50_4_DEEPFAKE")
    assert d["status"] == router.APPLIES_SPECIAL_PRESENTATION
    assert result["article_50_5_cross_cutting"] is True
    assert result["code_route"] == "MAP_SIGNED_CODE_COMMITMENTS_TO_EVIDENCE_NO_AUTOMATIC_COMPLIANCE"


def test_public_interest_text_without_both_exception_elements_applies():
    result = router.route_case(cases()[4])
    assert decision(result, "A50_4_PUBLIC_INTEREST_TEXT")["status"] == router.APPLIES


def test_public_interest_text_editorial_exception_requires_both_elements():
    result = router.route_case(cases()[5])
    assert decision(result, "A50_4_PUBLIC_INTEREST_TEXT")["status"] == router.NOT_APPLICABLE_EXCEPTION


def test_public_interest_text_half_exception_does_not_pass():
    case = copy.deepcopy(cases()[5])
    case["editorial_responsibility_assumed"] = False
    result = router.route_case(case)
    assert decision(result, "A50_4_PUBLIC_INTEREST_TEXT")["status"] == router.APPLIES


def test_unknown_editorial_fact_fails_closed():
    case = copy.deepcopy(cases()[5])
    case["editorial_responsibility_assumed"] = None
    result = router.route_case(case)
    assert decision(result, "A50_4_PUBLIC_INTEREST_TEXT")["status"] == router.UNKNOWN
    assert result["status"] == "HOLD_UNRESOLVED_SCOPE_OR_EXCEPTION"


def test_unknown_role_fails_closed():
    result = router.route_case({"case_id": "bad", "role": "CONSULTANT"})
    assert result["status"] == "HOLD_SCOPE_ROLE_UNKNOWN"
    assert result["external_action_authorized"] is False


def test_not_signing_code_is_not_noncompliance_claim():
    result = router.route_case(cases()[1])
    assert result["code_route"] == "DOCUMENT_ALTERNATIVE_EQUIVALENTLY_ADEQUATE_MEASURES"
    assert result["legal_compliance_proven"] is False


def test_synthetic_packet_never_claims_implementation():
    packet = json.loads((ROOT / "02_SYNTHETIC_SAMPLE_PACKET.json").read_text(encoding="utf-8"))
    assert packet["status"] == "SYNTHETIC_DESIGN_ONLY_NOT_CUSTOMER_EVIDENCE"
    assert packet["proof_boundary"]["implementation_complete"] is False
    assert packet["proof_boundary"]["legal_compliance_proven"] is False
    assert packet["external_action_authorized"] is False


def test_all_sample_cases_route_deterministically():
    results = router.route_many(cases())
    assert len(results) == 6
    assert all(x["case_id"] for x in results)
    assert all(x["external_action_authorized"] is False for x in results)
