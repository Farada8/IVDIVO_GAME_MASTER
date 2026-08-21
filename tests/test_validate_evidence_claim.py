from tools.validate_evidence_claim import validate


def claim(evidence_class, claim_type, result="PASS", promote=True):
    return {
        "claim_id":"T",
        "claim":"fixture",
        "claim_type": claim_type,
        "result": result,
        "evidence_class": evidence_class,
        "evidence_source":[{"source_type":"FIXTURE","locator":"fixture"}],
        "verification_method":"fixture",
        "what_this_evidence_can_prove":["fixture-level claim"],
        "what_this_evidence_cannot_prove":["anything beyond fixture"],
        "promotion_allowed": promote,
    }


def test_tests_are_not_literary_quality():
    assert validate(claim("AUTOMATED_TEST", "LITERARY_QUALITY_HUMAN_BELIEVABILITY"))["status"] == "FAIL"


def test_model_review_is_not_human_signal():
    assert validate(claim("MODEL_REVIEW", "HUMAN_SIGNAL"))["status"] == "FAIL"


def test_static_or_dry_is_not_live_provider():
    assert validate(claim("STATIC_INSPECTION", "LIVE_PROVIDER_RENDER_EXISTS"))["status"] == "FAIL"


def test_prediction_is_not_market_behavior():
    assert validate(claim("HYPOTHESIS", "MARKET_DEMAND_OR_CONVERSION"))["status"] == "FAIL"


def test_static_inspection_is_not_runtime_execution():
    assert validate(claim("STATIC_INSPECTION", "RUNTIME_BEHAVIOR_EXECUTED"))["status"] == "FAIL"


def test_actual_target_audience_can_support_human_signal():
    assert validate(claim("HUMAN_TARGET_AUDIENCE_SIGNAL", "HUMAN_SIGNAL"))["status"] == "PASS"


def test_provider_live_output_can_support_render_exists():
    assert validate(claim("PROVIDER_LIVE_OUTPUT", "LIVE_PROVIDER_RENDER_EXISTS"))["status"] == "PASS"


def test_market_behavior_can_support_conversion_claim():
    assert validate(claim("MARKET_BEHAVIOR", "MARKET_DEMAND_OR_CONVERSION"))["status"] == "PASS"
