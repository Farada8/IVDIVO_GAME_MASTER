import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "engine"))

from decision_proof_guard import *


def test_01_p193_missing_target_manifest_blocks_pa4():
    out = pa4_gate(FrozenPacket(None, "b"), Reviewer("r", "peer", True, True))
    assert out["status"] == "HOLD_MISSING_FROZEN_MANIFESTS" and not out["pa4"]


def test_02_p193_missing_bidder_manifest_blocks_pa4():
    out = pa4_gate(FrozenPacket("t", None), Reviewer("r", "peer", True, True))
    assert out["status"] == "HOLD_MISSING_FROZEN_MANIFESTS"


def test_03_p194_self_review_not_independent():
    out = pa4_gate(FrozenPacket("t", "b"), Reviewer("r", "peer", False, True))
    assert out["status"] == "HOLD_NO_INDEPENDENT_BLIND_REVIEWER"


def test_04_p194_reviewer_must_be_blind():
    out = pa4_gate(FrozenPacket("t", "b"), Reviewer("r", "peer", True, False))
    assert out["status"] == "HOLD_NO_INDEPENDENT_BLIND_REVIEWER"


def test_05_p195_same_packet_required():
    out = compare_rows({"x": True}, {"x": True}, False)
    assert out["status"] == "HOLD_NO_COMPARABLE_OUTPUTS"


def test_06_p196_fp_null_without_compare():
    assert compare_rows(None, {"x": False}, True)["false_positive"] is None


def test_07_p197_fn_null_without_compare():
    assert compare_rows({"x": False}, None, True)["false_negative"] is None


def test_08_p198_no_divergence_no_schema_revision():
    assert schema_revision_allowed(False) is False


def test_09_p199_reproducible_divergence_allows_review_not_auto_truth():
    assert schema_revision_allowed(True) is True


def test_10_p200_packet_compiler_guard_is_external_action_neutral():
    assert external_action_authorized(False) is False


def test_11_p201_real_user_required():
    out = pa5_gate(False, "before", "after", "t1", "t2", "artifact")
    assert not out["pa5"]


def test_12_p202_continue_is_not_outreach_authorization():
    assert not external_action_authorized(False)


def test_13_p203_missing_before_decision_blocks_delta():
    out = pa5_gate(True, None, "after", "t1", "t2", "artifact")
    assert not out["pa5"]


def test_14_p204_complete_real_decision_use_can_satisfy_pa5_schema():
    out = pa5_gate(True, "hold", "bid", "t1", "t2", "receipt")
    assert out["pa5"]


def test_15_p205_time_null_without_observation():
    assert observed_time(None, 5) is None


def test_16_p206_rework_requires_two_uses():
    assert rework_delta(3, None) is None


def test_17_p207_money_null_without_external_basis():
    assert monetary_value(10, None) is None


def test_18_p208_e3_requires_pa5():
    assert e3_gate(False, True) is False


def test_19_p208_e3_requires_behavioral_cost_or_commitment():
    assert e3_gate(True, False) is False


def test_20_p209_e4_requires_cash():
    assert e4_gate(None, "po") is False


def test_21_p209_e4_requires_binding_provenance():
    assert e4_gate(100.0, None) is False


def test_22_p210_substitute_matrix_preserves_residual_job():
    out = residual_job_gate(["discover", "qualify", "join"], ["discover"])
    assert out["status"] == "RESIDUAL_JOB_EXISTS" and out["residual_job"] == ["join", "qualify"]


def test_23_p211_zero_residual_job_kills_paid_differentiation():
    out = residual_job_gate(["discover", "qualify"], ["discover", "qualify"])
    assert out["status"] == "HOLD_RESHAPE_OR_REJECT"


def test_24_p212_wtp_not_inferred_from_residual_job():
    out = residual_job_gate(["qualify"], [])
    assert out["status"] == "RESIDUAL_JOB_EXISTS"  # no WTP field exists by design


def test_25_p213_observed_burden_required_for_comparison():
    assert observed_time(None, None) is None


def test_26_p214_negative_time_rejected():
    try:
        observed_time(-1, 0)
        assert False
    except ValueError:
        assert True


def test_27_p215_capacity_not_derived_by_this_guard_without_observation():
    assert observed_time(None, 0) is None


def test_28_p216_refresh_does_not_raise_proof_grade():
    assert proof_grade_guard("PA3", polished=False, ci_green=True) == "PA3"


def test_29_p217_stale_conflict_requires_revalidate():
    assert stale_conflict_guard("OPEN", "EXPIRED", True) == "REVALIDATE"


def test_30_p218_p219_proof_laundering_and_polish_blocked():
    assert proof_grade_guard("E2", polished=True, ci_green=True) == "E2"


def test_31_p220_p221_partial_persistence_reconciles():
    assert cross_store_commit(True, True, True, False) == "RECONCILE_PARTIAL"
    assert cross_store_commit(True, True, True, True) == "PERSISTED"


def test_32_p222_p224_root_uncertainty_protects_no_change_path():
    assert not si_candidate(1, True)
    assert next_frontier(False, False, False, False) == "ACQUIRE_TARGET_PACK"


if __name__ == "__main__":
    import inspect
    failures = []
    tests = [obj for name, obj in sorted(globals().items()) if name.startswith("test_") and callable(obj)]
    for test in tests:
        try:
            test()
            print("PASS", test.__name__)
        except Exception as exc:
            failures.append((test.__name__, exc))
            print("FAIL", test.__name__, repr(exc))
    print(f"{len(tests)-len(failures)}/{len(tests)} PASS")
    raise SystemExit(1 if failures else 0)
