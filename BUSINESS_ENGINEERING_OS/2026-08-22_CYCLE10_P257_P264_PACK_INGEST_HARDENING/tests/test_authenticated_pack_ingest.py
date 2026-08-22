import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from authenticated_pack_ingest import (
    AcquisitionReceipt,
    AuthenticatedPackIngestAdapter,
    FileRecord,
    SupersessionEdge,
    bind_receipt,
    build_supersession_graph,
    canonical_manifest_hash,
    compile_authority_gap_certificate_v2,
    inventory_state,
    sanitize_ingest_metadata,
    target_requirements_only,
)


def f(name, digest, source="official-export", rev=None):
    return FileRecord(name, digest, 10, "application/pdf", source, rev)


def receipt(resource="8872468"):
    return AcquisitionReceipt(resource, "USER_PROVIDED_OFFICIAL_EXPORT", "2026-08-22T05:00:00+01:00", "authorized_actor", "https://official.example/export", "OFFICIAL_EXPORT")


def test_01_p257_rejects_password_metadata():
    try:
        sanitize_ingest_metadata({"password": "secret"})
        assert False
    except ValueError:
        assert True


def test_02_p257_rejects_nested_token_metadata():
    try:
        sanitize_ingest_metadata({"headers": {"Authorization": "Bearer x"}})
        assert False
    except ValueError:
        assert True


def test_03_p257_adapter_never_certifies_completeness():
    out = AuthenticatedPackIngestAdapter().ingest(expected_resource_id="8872468", receipt=receipt(), files=[f("a.pdf", "a")])
    assert out["pack_completeness"] == "UNPROVEN_UNTIL_SEPARATE_AUTHORITY_GATE"


def test_04_p258_wrong_resource_fails():
    try:
        bind_receipt(receipt("other"), "8872468")
        assert False
    except ValueError:
        assert True


def test_05_p258_incomplete_receipt_fails():
    bad = AcquisitionReceipt("8872468", "", "t", "actor", "url", "class")
    try:
        bind_receipt(bad, "8872468")
        assert False
    except ValueError:
        assert True


def test_06_p259_manifest_order_independent():
    a = f("a.pdf", "aaa", rev="1")
    b = f("b.pdf", "bbb", rev="2")
    assert canonical_manifest_hash([a, b]) == canonical_manifest_hash([b, a])


def test_07_p259_provenance_changes_manifest_identity():
    a1 = f("a.pdf", "aaa", source="s1")
    a2 = f("a.pdf", "aaa", source="s2")
    assert canonical_manifest_hash([a1]) != canonical_manifest_hash([a2])


def test_08_p260_no_expected_inventory_means_unproven_not_complete():
    out = inventory_state(["1", "2", "3"])
    assert out["status"] == "OBSERVED_ONLY_COMPLETENESS_UNPROVEN" and not out["authoritatively_complete"]


def test_09_p260_known_missing_item_is_incomplete():
    out = inventory_state(["1", "3"], ["1", "2", "3"], True)
    assert out["status"] == "INVENTORY_INCOMPLETE" and out["missing"] == ["2"]


def test_10_p261_full_observed_expected_set_still_needs_authority_evidence():
    out = inventory_state(["1", "2"], ["1", "2"], False)
    assert out["status"] == "EXPECTED_SET_OBSERVED_COMPLETENESS_AUTHORITY_UNPROVEN"


def test_11_p261_explicit_authority_plus_no_gap_can_be_complete():
    out = inventory_state(["1", "2"], ["1", "2"], True)
    assert out["status"] == "AUTHORITATIVELY_COMPLETE" and out["authoritatively_complete"]


def test_12_p262_unknown_relation_stays_unknown():
    out = build_supersession_graph([SupersessionEdge("a", "b", "UNKNOWN_RELATION")])
    assert out["unknown_relation_count"] == 1


def test_13_p262_self_edge_fails_closed():
    try:
        build_supersession_graph([SupersessionEdge("a", "a", "REPLACES")])
        assert False
    except ValueError:
        assert True


def test_14_p263_benchmark_carries_zero_rows():
    out = target_requirements_only(["target-row"], ["old-a", "old-b"], False)
    assert out["target_requirements"] == ["target-row"] and out["benchmark_rows_carried_over"] == 0 and not out["target_pack_complete"]


def test_15_p264_gap_certificate_reports_only_given_missing_authority():
    cert = compile_authority_gap_certificate_v2("8872468", ["CURRENT_ATTACHMENT_INVENTORY"], ["TENDER_REQUIREMENT_REGISTRY", "BID_DECISION"], "ACQUIRE_AUTHENTICATED_OFFICIAL_EXPORT")
    assert cert.missing_authority == ("CURRENT_ATTACHMENT_INVENTORY",)
    assert cert.evidence_grade_unchanged is True


def test_16_p264_no_real_gap_cannot_create_gap_certificate():
    try:
        compile_authority_gap_certificate_v2("8872468", [], ["BID_DECISION"], "x")
        assert False
    except ValueError:
        assert True


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
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
