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


def test_all_hardening_fixtures_nonpromoting():
    results = cv.verify_many(fixtures())
    assert len(results) == 8
    assert all(x["legal_compliance_proven"] is False for x in results)
    assert all(x["independent_verification_proven"] is False for x in results)
    assert all(x["customer_demand_proven"] is False for x in results)
    assert all(x["wtp_proven"] is False for x in results)
    assert all(x["transaction_proven"] is False for x in results)
    assert all(x["external_action_authorized"] is False for x in results)


def test_chatbot_controls_present():
    r = by_id()["CV_CHATBOT_CONTROLS_PRESENT"]
    assert r["overall"] == "PASS_TECHNICAL_CONTROLS_DECLARED"
    assert find(r, "InteractionDisclosureEvidence")["state"] == cv.PASS_CONTROL
    assert find(r, "PresentationAccessibilityEvidence")["state"] == cv.PASS_CONTROL


def test_machine_mark_does_not_satisfy_deepfake_human_disclosure():
    r = by_id()["CV_DEEPFAKE_MACHINE_MARK_ONLY"]
    assert r["overall"] == "CONTROL_GAPS_FOUND"
    assert find(r, "ContentDisclosureEvidence")["state"] == cv.FAIL_CONTROL
    assert all(x["evidence_object"] != "MachineReadableMarkingEvidence" for x in r["findings"])


def test_provider_marking_control_passes_only_technical_layer():
    r = by_id()["CV_GENERATOR_MACHINE_MARK_PRESENT"]
    assert r["overall"] == "PASS_TECHNICAL_CONTROLS_DECLARED"
    assert find(r, "MachineReadableMarkingEvidence")["state"] == cv.PASS_CONTROL
    assert r["legal_compliance_proven"] is False


def test_emotion_notice_keeps_separate_review_plane():
    r = by_id()["CV_EMOTION_NOTICE_PRESENT"]
    assert find(r, "ExposureNoticeEvidence")["state"] == cv.PASS_CONTROL
    assert any(x["type"] == "SEPARATE_REVIEW_PLANE" for x in r["review_items"])
    assert r["overall"] == cv.REVIEW_REQUIRED


def test_editorial_exception_does_not_become_compliance_pass():
    r = by_id()["CV_PUBLIC_INTEREST_EDITORIAL_EXCEPTION"]
    assert r["overall"] == cv.NOT_ACTIVE
    assert r["legal_compliance_proven"] is False


def test_closed_loop_scope_claim_stays_review():
    r = by_id()["CV_CLOSED_LOOP_SCOPE_REVIEW"]
    assert r["overall"] == cv.REVIEW_REQUIRED
    assert any(x["type"] == "SCOPE_OR_EXCEPTION_REVIEW_REQUIRED" for x in r["review_items"])


def test_legacy_transition_claim_requires_legislative_review():
    r = by_id()["CV_LEGACY_TRANSITION_CLAIM"]
    assert any(x["type"] == "LEGISLATIVE_REVIEW_REQUIRED" for x in r["review_items"])
    assert r["legal_compliance_proven"] is False


def test_unknown_control_presence_stays_unknown():
    r = by_id()["CV_ACTIVE_CONTROL_UNKNOWN"]
    assert r["overall"] == cv.REVIEW_REQUIRED
    assert find(r, "MachineReadableMarkingEvidence")["state"] == cv.UNKNOWN_CONTROL
    assert find(r, "PresentationAccessibilityEvidence")["state"] == cv.UNKNOWN_CONTROL
