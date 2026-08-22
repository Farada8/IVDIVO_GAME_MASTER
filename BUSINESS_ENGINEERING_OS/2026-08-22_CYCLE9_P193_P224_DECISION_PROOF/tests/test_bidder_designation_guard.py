import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from bidder_designation_guard import (
    ACTUAL_BIDDER,
    TEST_FIXTURE_ONLY,
    BidderDesignationObject,
    designation_state,
    requirement_join_authorized,
)


def fixture(mode=TEST_FIXTURE_ONLY, actor=None, ts=None, scope="INTERNAL_ENGINE_TEST_ONLY", active=False):
    return BidderDesignationObject(
        resource_id="8872468",
        legal_entity_name="SYNTHESIS-IVDIVO LIMITED",
        registration_number="796820",
        designation_mode=mode,
        authorized_designator=actor,
        designated_at=ts,
        designation_scope=scope,
        active=active,
    )


def test_fixture_mode_never_becomes_real_bidder():
    out = designation_state(fixture())
    assert out["status"] == "TEST_FIXTURE_ONLY_NOT_BIDDER"
    assert out["internal_fixture_allowed"] is True
    assert out["explicit_bidder_designation"] is False


def test_company_context_alone_does_not_designate_bidder():
    obj = fixture(mode=None)
    out = designation_state(obj)
    assert out["explicit_bidder_designation"] is False


def test_actual_bidder_mode_requires_authorized_actor_timestamp_scope_and_active_state():
    out = designation_state(fixture(mode=ACTUAL_BIDDER, active=True))
    assert out["status"] == "HOLD_INCOMPLETE_EXPLICIT_DESIGNATION"
    assert out["explicit_bidder_designation"] is False


def test_complete_explicit_designation_can_pass_designation_gate():
    obj = fixture(
        mode=ACTUAL_BIDDER,
        actor="AUTHORIZED_FOUNDER",
        ts="2026-08-22T05:00:00+01:00",
        scope="RESOURCE_8872468_BID_EVALUATION",
        active=True,
    )
    out = designation_state(obj)
    assert out["status"] == "EXPLICIT_BIDDER_DESIGNATION_PRESENT"
    assert out["explicit_bidder_designation"] is True


def test_designation_alone_cannot_unlock_requirement_join():
    obj = fixture(
        mode=ACTUAL_BIDDER,
        actor="AUTHORIZED_FOUNDER",
        ts="2026-08-22T05:00:00+01:00",
        scope="RESOURCE_8872468_BID_EVALUATION",
        active=True,
    )
    assert requirement_join_authorized(obj, target_pack_complete=False, bidder_capability_packet_complete=True) is False
    assert requirement_join_authorized(obj, target_pack_complete=True, bidder_capability_packet_complete=False) is False
    assert requirement_join_authorized(obj, target_pack_complete=True, bidder_capability_packet_complete=True) is True


if __name__ == "__main__":
    tests = [obj for name, obj in sorted(globals().items()) if name.startswith("test_") and callable(obj)]
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
