import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import control_verifier as cv


def fixtures():
    return json.loads((ROOT / "05_CONTROL_VERIFICATION_FIXTURES.json").read_text(encoding="utf-8"))["cases"]


def by_id():
    return {x["case_id"]: cv.verify_case(x) for x in fixtures()}


def find(result, evidence_object):
    return next(x for x in result["findings"] if x["evidence_object"] == evidence_object)


def test_all_hardening_fixtures_are_deterministic_and_non_promoting():
    results = cv.verify_many(fixtures())
    assert len(results) == 8
    assert all(x["case_id"] for x in results)
    assert all(x["legal_compliance_proven"] is False for x in results)
    assert all(x["independent_verification_proven"] is False for x in results)
    assert all(x["customer_demand_proven"] is False for x in results)
    assert all(x["wtp_proven"] is False for x in results)
    assert all(x["transaction_proven"] is False for x in results)
    assert all(x["external_action_authorized"] is False for x in results)


def test_chatbot_control_presence_passes_technical_layer_only():
    r = by_id()["CV_CHATBOT_CONTROLS_PRESENT"]
    assert r["overall"] == "PASS_TECHNICAL_CONTROLS_DECLARED"
    assert find(r, "InteractionDisclosureEvidence")["state"] == cv.PASS_CONTROL
    assert find(r, "PresentationAccessibilityEvidence")["state"] == cv.PASS_CONTROL
    assert r["legal_compliance_proven"] is False


def test_machine_mark_does_not_satisfy_deepfake_human_disclosure():
    r = by_id()["CV_DEEPFAKE_MACHINE_MARK_ONLY"]
    assert r["overall"] == "CONTROL_GAPS_FOUND"
    assert find(r, "ContentDisclosureEvidence")["state"] == cv.FAIL_CONTROL
    # MachineReadableMarkingEvidence is deliberately not a required deployer evidence object here.
    assert all(x["evidence_object"] != "MachineReadableMarkingEvidence" for x in r["findings"])


def test_provider_marking_control_can_pass_without_proving_compliance():
    r = by_id()["CV_GENERATOR_MACHINE_MARK_PRESENT"]
    assert r["overall"] == "PASS_TECHNICAL_CONTROLS_DECLARED"
    assert find(r, "MachineReadableMarkingEvidence")["state"] == cv.PASS_CONTROL
    assert r["legal_compliance_proven"] is False


def test_emotion_notice_control_passes_while_data_review_stays_separate():
    r = by_id()["CV_EMOTION_NOTICE_PRESENT"]
    assert find(r, "ExposureNoticeEvidence")["state"] == cv.PASS_CONTROL
    assert any(x["type"] == "SEPARATE_REVIEW_PLANE" for x in r["review_items"])
    assert r["overall"] == "REVIEW_REQUIRED"


def test_editorial_exception_does_not_become_technical_compliance_pass():
    r = by_id()["CV_PUBLIC_INTEREST_EDITORIAL_EXCEPTION"]
    assert r["overall"] == cv.NOT_ACTIVE
    assert r["legal_compliance_proven"] is False


def test_closed_loop_scope_claim_stays_human_review_required():
    r = by_id()["CV_CLOSED_LOOP_SCOPE_REVIEW"]
    assert r["overall"] == "REVIEW_REQUIRED"
    assert any(x["type"] == "SCOPE_OR_EXCEPTION_REVIEW_REQUIRED" for x in r["review_items"])


def test_legacy_transition_claim_is_not_automated_as_current_law():
    r = by_id()["CV_LEGACY_TRANSITION_CLAIM"]
    assert r["overall"] == "CONTROL_GAPS_FOUND" or r["overall"] == "REVIEW_REQUIRED"
    assert any(x["type"] == "LEGISLATIVE_REVIEW_REQUIRED" for x in r["review_items"])
    assert r["legal_compliance_proven"] is False


def test_unknown_control_presence_stays_unknown():
    r = by_id()["CV_ACTIVE_CONTROL_UNKNOWN"]
    assert r["overall"] == "REVIEW_REQUIRED"
    assert find(r, "MachineReadableMarkingEvidence")["state"] == cv.UNKNOWN_CONTROL
    assert find(r, "PresentationAccessibilityEvidence")["state"] == cv.UNKNOWN_CONTROL
