import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from bidder_evidence_hardening import *


def test_01_p265_fixture_is_not_explicit_bidder():
    obj = BidderDesignationV2("8872468", "SYNTHESIS-IVDIVO LIMITED", None, None, "TEST", False, "TEST_FIXTURE_ONLY")
    assert designation_v2_state(obj)["explicit"] is False


def test_02_p265_actual_bidder_requires_full_provenance():
    obj = BidderDesignationV2("8872468", "SYNTHESIS-IVDIVO LIMITED", "FOUNDER", "2026-08-22T05:00:00+01:00", "RESOURCE_ONLY", True)
    assert designation_v2_state(obj)["explicit"] is True


def test_03_p266_observed_core_screen_not_current_certified():
    e = [IdentityEvidence("registration_number", "796820", "core-screen", "OFFICIAL_INTERFACE_CAPTURE", "2026-08-22", False)]
    assert reconcile_identity_field("registration_number", e)["status"] == "OBSERVED_NOT_CURRENT_CERTIFIED"


def test_04_p266_equal_top_conflict_fails_closed():
    e = [
        IdentityEvidence("status", "Normal", "a", "CURRENT_CERTIFIED_AUTHORITY", current_certified=True),
        IdentityEvidence("status", "Dissolved", "b", "CURRENT_CERTIFIED_AUTHORITY", current_certified=True),
    ]
    out = reconcile_identity_field("status", e)
    assert out["value"] is None and out["status"] == "CONFLICTING_TOP_AUTHORITY_IDENTITY_EVIDENCE"


def test_05_p267_undated_expiry_does_not_count_current():
    item = CredentialEvidence("insurance", "ins-1", "2026-01-01T00:00:00+00:00", None)
    assert credential_state(item, "2026-08-22T00:00:00+00:00")["status"] == "UNKNOWN_UNDATED_EXPIRY"


def test_06_p267_expired_credential_fails_current():
    item = CredentialEvidence("insurance", "ins-1", None, "2026-01-01T00:00:00+00:00")
    assert credential_state(item, "2026-08-22T00:00:00+00:00")["status"] == "EXPIRED"


def test_07_p268_unbound_capability_stays_unknown():
    claim = CapabilityClaim("roofing", None, None, None, None, None)
    assert capability_claim_state(claim)["status"] == "UNKNOWN_UNBOUND_CAPABILITY_CLAIM"


def test_08_p268_self_evidence_can_be_bound_without_becoming_independent_truth():
    claim = CapabilityClaim("EWI", "invoice-family-1", "PRIVATE_PRIMARY", "2026-Q2", "external-insulation-site", "PENDING")
    assert capability_claim_state(claim)["status"] == "EVIDENCE_BOUND_REVIEW_PENDING"


def test_09_p269_generic_construction_does_not_satisfy_roof_energy_scope():
    out = target_specific_scope_gate(["construction"], ["roofing", "thermal_insulation"])
    assert out["match"] is False


def test_10_p269_specific_tags_can_match_without_implying_other_requirements():
    out = target_specific_scope_gate(["roofing", "thermal_insulation"], ["roofing", "thermal_insulation"])
    assert out["match"] is True


def test_11_p270_reference_dimensions_remain_separate():
    ref = ReferenceProject("ref1", "2025-06-01T00:00:00+00:00", ["thermal_insulation"], "subcontractor", None, None)
    out = reference_project_state(ref, as_of="2026-08-22T00:00:00+00:00", lookback_years=5, required_scope_tags=["thermal_insulation"])
    assert out["status"] == "REFERENCE_PARTIAL"
    assert out["dimensions"]["value_proven"] is False
    assert out["dimensions"]["client_evidence_proven"] is False


def test_12_p270_full_reference_requires_each_dimension():
    ref = ReferenceProject("ref1", "2025-06-01T00:00:00+00:00", ["roofing"], "main contractor", 100000.0, "client-ref")
    out = reference_project_state(ref, as_of="2026-08-22T00:00:00+00:00", lookback_years=5, required_scope_tags=["roofing"])
    assert out["status"] == "REFERENCE_FULLY_SUPPORTED"


def test_13_p271_speculative_hiring_never_counts_as_current_capacity():
    item = WorkforceCapacityEvidence([], [], None, ["future-hire-1", "future-hire-2"])
    out = workforce_capacity_state(item)
    assert out["speculative_future_hires_count"] == 2
    assert out["speculative_hires_count_as_current_capacity"] == 0


def test_14_p271_named_people_and_workload_remain_distinct():
    item = WorkforceCapacityEvidence(["person-a"], ["subcontractor-a"], "workload-ledger", [])
    out = workforce_capacity_state(item)
    assert out["named_available_count"] == 1
    assert out["current_workload_proven"] is True


def test_15_p272_private_fields_are_not_exposed():
    packet = privacy_minimized_packet(
        {"legal_name": "SYNTHESIS-IVDIVO LIMITED", "bank_account": "PRIVATE", "tax_id": "PRIVATE"},
        allowed_fields=["legal_name"],
        private_evidence_ids=["raw-tax-doc", "raw-bank-doc"],
    )
    assert packet["decision_fields"] == {"legal_name": "SYNTHESIS-IVDIVO LIMITED"}
    assert packet["private_raw_values_exposed"] is False


def test_16_p272_hashes_preserve_reference_without_raw_identifier():
    packet = privacy_minimized_packet({"legal_name": "X"}, allowed_fields=["legal_name"], private_evidence_ids=["secret-ref"])
    assert len(packet["private_evidence_hashes"][0]) == 64
    assert packet["private_evidence_hashes"][0] != "secret-ref"


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
