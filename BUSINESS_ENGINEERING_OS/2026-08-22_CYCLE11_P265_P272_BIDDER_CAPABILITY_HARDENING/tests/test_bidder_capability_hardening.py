import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from bidder_capability_hardening import *


def test_01_p265_test_fixture_not_real_designation():
    obj = BidderDesignationV2("8872468", "SYNTHESIS-IVDIVO LIMITED", "796820", None, None, "tender", False, "TEST_FIXTURE_ONLY")
    out = real_designation_state(obj)
    assert not out["real_designation"] and out["status"] == "HOLD_NO_EXPLICIT_BIDDER_DESIGNATION"


def test_02_p265_real_designation_requires_authorized_actor():
    obj = BidderDesignationV2("8872468", "Entity", "1", None, "2026-08-22T05:00:00+01:00", "bid", True)
    assert not real_designation_state(obj)["real_designation"]


def test_03_p265_complete_real_designation_schema_can_pass():
    obj = BidderDesignationV2("8872468", "Entity", "1", "authorized_actor", "2026-08-22T05:00:00+01:00", "bid", True)
    assert real_designation_state(obj)["real_designation"]


def test_04_p266_higher_current_authority_resolves_identity():
    evidence = [
        IdentityEvidence("company_number", "OLD", "old", "formation", 1, "2025-01-01T00:00:00+00:00", False),
        IdentityEvidence("company_number", "796820", "current", "official_current", 5, "2026-08-22T00:00:00+00:00", True),
    ]
    out = resolve_identity(evidence)["company_number"]
    assert out["value"] == "796820" and out["status"] == "RESOLVED_CURRENT_AUTHORITY"


def test_05_p266_equal_rank_conflict_remains_null():
    evidence = [
        IdentityEvidence("status", "A", "s1", "official", 5, "2026-08-22T00:00:00+00:00", True),
        IdentityEvidence("status", "B", "s2", "official", 5, "2026-08-22T00:00:00+00:00", True),
    ]
    out = resolve_identity(evidence)["status"]
    assert out["value"] is None and out["status"] == "CONFLICT_UNRESOLVED"


def test_06_p267_expired_credential_fails():
    c = CredentialEvidence("insurance", "e1", "2026-01-01T00:00:00+00:00", "2026-06-01T00:00:00+00:00", "2026-01-01T00:00:00+00:00")
    assert credential_state(c, "2026-08-22T00:00:00+00:00") == "EXPIRED"


def test_07_p267_undated_expiry_requires_revalidation():
    c = CredentialEvidence("tax", "e1", "2026-01-01T00:00:00+00:00", None, "2026-08-22T00:00:00+00:00")
    assert credential_state(c, "2026-08-22T00:00:00+00:00") == "UNDATED_REVALIDATE"


def test_08_p267_future_credential_not_yet_valid():
    c = CredentialEvidence("cert", "e1", "2026-09-01T00:00:00+00:00", "2027-09-01T00:00:00+00:00", "2026-08-22T00:00:00+00:00")
    assert credential_state(c, "2026-08-22T00:00:00+00:00") == "NOT_YET_VALID"


def test_09_p268_claim_without_evidence_unknown():
    c = CapabilityClaim("c1", "roofing", None, None, None, None, "project", "scope", "VERIFIED")
    assert capability_claim_state(c) == "UNKNOWN_NO_EVIDENCE_BINDING"


def test_10_p268_verified_claim_requires_context():
    c = CapabilityClaim("c1", "roofing", "e1", "THIRD_PARTY", "2025", "2026", "project", "roofing", "VERIFIED")
    assert capability_claim_state(c) == "VERIFIED_CAPABILITY"


def test_11_p269_ewi_does_not_satisfy_roofing():
    out = target_specific_control(evidence_tags=["EWI", "external insulation", "render"], required_tag="roofing")
    assert out["status"] == "NO_TARGET_SPECIFIC_MATCH" and not out["met"]


def test_12_p269_direct_tag_still_not_met_without_requirement_join():
    out = target_specific_control(evidence_tags=["roofing"], required_tag="roofing")
    assert out["status"] == "DIRECT_TAG_MATCH_CANDIDATE" and not out["met"] and out["requires_requirement_evidence_join"]


def test_13_p270_self_issued_record_without_completion_proof_partial():
    p = ReferenceProject("p1", "2026-06-01T00:00:00+00:00", "supplier", ("EWI",), 10000.0, "seller_invoice", "seller_invoice", None)
    out = validate_reference(p, earliest_completion_date="2025-01-01T00:00:00+00:00", required_scope_tag="EWI")
    assert out["status"] == "PARTIAL_REFERENCE_THIRD_PARTY_COMPLETION_UNPROVEN"


def test_14_p270_scope_mismatch_visible_dimension():
    p = ReferenceProject("p1", "2026-06-01T00:00:00+00:00", "supplier", ("EWI",), 10000.0, "third_party", "client", "completion")
    out = validate_reference(p, required_scope_tag="roofing")
    assert out["dimensions"]["scope_fit"] is False and out["status"] == "REFERENCE_DIMENSION_FAIL"


def test_15_p271_planned_hire_not_current_capacity():
    r = WorkforceEvidence("future", "roofer", "cert", "2026-09-01", "2026-12-01", "planned", "PLANNED_HIRE")
    out = workforce_capacity_state([r])
    assert out["status"] == "HOLD_CURRENT_CAPACITY_UNPROVEN" and out["future_or_intent_not_counted"] == ["future"]


def test_16_p271_subcontractor_intent_not_current_capacity():
    r = WorkforceEvidence("sub1", "roofer", "cert", "2026-09-01", "2026-12-01", "unknown", "SUBCONTRACTOR_INTENT")
    assert workforce_capacity_state([r])["status"] == "HOLD_CURRENT_CAPACITY_UNPROVEN"


def test_17_p271_verified_current_complete_resource_counts():
    r = WorkforceEvidence("person1", "roofer", "cert1", "2026-08-22", "2026-12-31", "AVAILABLE", "VERIFIED_CURRENT")
    out = workforce_capacity_state([r])
    assert out["status"] == "CURRENT_CAPACITY_EVIDENCE_PRESENT" and out["verified_current"] == ["person1"]


def test_18_p272_private_dependency_survives_redaction():
    fields = {"insurance": {"status": "UNVERIFIED", "hash": "h", "source_state": "PRIVATE_UNVERIFIED"}}
    out = privacy_minimized_packet(fields, ["insurance"])
    assert out["private_dependencies"] == ["insurance"] and out["proof_upgrade"] is False


def test_19_p272_disallowed_field_not_exposed():
    fields = {"bank_account": {"status": "VERIFIED", "hash": "h", "source_state": "PRIVATE_VERIFIED"}}
    out = privacy_minimized_packet(fields, [])
    assert "bank_account" not in out["public_derivative"] and "bank_account" in out["private_dependencies"]


def test_20_p272_redaction_cannot_turn_unverified_into_verified():
    fields = {"tax": {"status": "UNVERIFIED", "hash": "h", "source_state": "PRIVATE_UNVERIFIED"}}
    out = privacy_minimized_packet(fields, ["tax"])
    assert out["public_derivative"]["tax"]["status"] == "UNVERIFIED"


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
