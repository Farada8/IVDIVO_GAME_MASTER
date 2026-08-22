import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from decision_proof_guard import planned_award_date_guard


def test_tender_submission_plus_future_award_date_is_not_awarded():
    out = planned_award_date_guard(
        "Tender Submission",
        "2026-09-04T17:00:00+01:00",
        False,
    )
    assert out["awarded"] is False
    assert out["status"] == "PLANNED_AWARD_DATE_NEQ_AWARDED_CONTRACT"


def test_separate_authoritative_award_provenance_is_required_for_awarded_true():
    out = planned_award_date_guard(
        "Awarded",
        "2026-09-04T17:00:00+01:00",
        True,
    )
    assert out["awarded"] is True
    assert out["status"] == "AWARD_PROVEN_BY_SEPARATE_AUTHORITY"


def test_no_award_field_and_no_award_provenance_stays_unawarded():
    out = planned_award_date_guard("Tender Submission", None, False)
    assert out["awarded"] is False
    assert out["status"] == "NO_AWARD_EVIDENCE"


if __name__ == "__main__":
    tests = [
        test_tender_submission_plus_future_award_date_is_not_awarded,
        test_separate_authoritative_award_provenance_is_required_for_awarded_true,
        test_no_award_field_and_no_award_provenance_stays_unawarded,
    ]
    failures = []
    for test in tests:
        try:
            test()
            print("PASS", test.__name__)
        except Exception as exc:
            failures.append((test.__name__, exc))
            print("FAIL", test.__name__, repr(exc))
    print(f"{len(tests)-len(failures)}/{len(tests)} PASS")
    raise SystemExit(1 if failures else 0)
