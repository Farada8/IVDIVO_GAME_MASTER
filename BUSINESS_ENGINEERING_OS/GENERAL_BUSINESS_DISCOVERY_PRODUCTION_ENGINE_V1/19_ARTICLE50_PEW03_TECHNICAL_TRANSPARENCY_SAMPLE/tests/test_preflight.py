#!/usr/bin/env python3
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "03_preflight.py"
FIXTURE_PATH = ROOT / "02_SYNTHETIC_FIXTURE.json"

spec = importlib.util.spec_from_file_location("article50_preflight", MODULE_PATH)
preflight = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(preflight)

fixture = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
results = preflight.evaluate_fixture(fixture)
by_id = {item["case_id"]: item for item in results["results"]}


def state(case_id, control):
    for finding in by_id[case_id]["findings"]:
        if finding["control"] == control:
            return finding["state"]
    raise AssertionError(f"missing control {control} for {case_id}")


def test_fixture_count_and_no_promotion():
    assert len(results["results"]) == 9
    assert results["legal_compliance_certified"] is False
    assert results["market_proof_promoted"] is False
    assert all(item["legal_compliance_certified"] is False for item in results["results"])
    assert all(item["market_proof_promoted"] is False for item in results["results"])


def test_chatbot_disclosure_and_accessibility_pass():
    assert state("CHATBOT_FIRST_INTERACTION", "A50-1-DISCLOSURE") == "PASS"
    assert state("CHATBOT_FIRST_INTERACTION", "A50-5-ACCESSIBILITY") == "PASS"


def test_provider_marking_pass():
    assert state("GEN_IMAGE_MARKED", "A50-2-MACHINE-MARK") == "PASS"


def test_machine_mark_does_not_replace_deepfake_human_label():
    assert state("DEEPFAKE_MACHINE_MARK_ONLY", "A50-4-DEEPFAKE-LABEL") == "FAIL_CONTROL"
    assert by_id["DEEPFAKE_MACHINE_MARK_ONLY"]["overall"] == "CONTROL_GAPS_FOUND"


def test_public_interest_text_declared_editorial_exception_is_not_certification():
    assert state("PUBLIC_INTEREST_TEXT_EDITORIAL_EXCEPTION", "A50-4-PUBLIC-INTEREST-TEXT") == "NOT_APPLICABLE_DECLARED_EXCEPTION"
    assert by_id["PUBLIC_INTEREST_TEXT_EDITORIAL_EXCEPTION"]["legal_compliance_certified"] is False


def test_public_interest_text_missing_review_and_label_fails_control():
    assert state("PUBLIC_INTEREST_TEXT_NO_REVIEW_NO_LABEL", "A50-4-PUBLIC-INTEREST-TEXT") == "FAIL_CONTROL"


def test_emotion_recognition_notice_pass():
    assert state("EMOTION_RECOGNITION_NOTICE", "A50-3-EXPOSURE-NOTICE") == "PASS"


def test_closed_loop_nonfinal_not_promoted_to_human_marking_failure():
    assert state("CLOSED_LOOP_NONFINAL", "A50-2-MACHINE-MARK") == "NOT_APPLICABLE_TECHNICAL_SCOPE"


def test_legacy_transition_requires_review_not_pass():
    assert state("LEGACY_PROVIDER_MARKING_TRANSITION", "A50-2-MACHINE-MARK") == "REVIEW_REQUIRED"
    assert by_id["LEGACY_PROVIDER_MARKING_TRANSITION"]["overall"] == "REVIEW_REQUIRED"


def test_unknown_role_stays_unknown():
    assert state("UNKNOWN_ROLE_GENERATIVE_TEXT", "ROLE-00") == "UNKNOWN"
    assert state("UNKNOWN_ROLE_GENERATIVE_TEXT", "A50-2-MACHINE-MARK") == "UNKNOWN"
    assert by_id["UNKNOWN_ROLE_GENERATIVE_TEXT"]["overall"] == "REVIEW_REQUIRED"


def test_forbidden_claim_words_are_not_emitted_as_values():
    text = json.dumps(results, sort_keys=True)
    forbidden_values = [
        '"COMPLIANT"',
        '"CERTIFIED"',
        '"LEGAL_PASS"',
        '"LEGAL_FAIL"',
        '"APPROVED"',
        '"BUYER_DEMAND_PROVEN"',
        '"WTP_PROVEN"',
    ]
    for token in forbidden_values:
        assert token not in text


if __name__ == "__main__":
    # Minimal runner so CI does not depend on pytest.
    tests = [value for name, value in globals().items() if name.startswith("test_") and callable(value)]
    for test in sorted(tests, key=lambda fn: fn.__name__):
        test()
    print(f"P-EW03 ARTICLE50 PREFLIGHT: PASS — {len(tests)} deterministic tests")
