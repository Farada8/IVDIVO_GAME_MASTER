import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "engine"))

from authority_recovery import *


def ws():
    return TenderWorkspace(
        resource_id="8872468",
        authority="St Joseph's Secondary School (Ballybunion)",
        ca_unique_id="26-002",
        evaluation_mechanism="MEAT",
        estimated_value_eur=1600000,
        clarification_deadline="2026-08-31T14:00:00+01:00",
        submission_deadline="2026-09-02T17:00:00+01:00",
        opening_time="2026-09-02T17:30:00+01:00",
        duration_months=9,
        source_url="https://www.etenders.gov.ie/epps/cft/prepareViewCfTWS.do?resourceId=8872468",
    )


def benchmark():
    names = [
        ("Billsoft Doc.", "20260993-PD1.E0X"),
        ("Tender Documents", "St.Josephs-Etender.zip"),
        ("Tender Structure XML - Cycle 1", "c4t_8176962_1.xml"),
        ("Full ESPD request", "espdRequest-8176962.xml"),
        ("Extended ESPD request", "espdRequest-8176962.xml"),
        ("ESPD request pdf", "espdRequest-8176962.pdf"),
    ]
    return [Attachment(t, f, "8176962") for t, f in names]


# P97–P112

def test_01_p97_workspace_without_target_inventory_is_blocked():
    assert target_pack_status(ws(), None)["status"] == "BLOCKED_INCOMPLETE_TARGET_PACK"


def test_02_p98_benchmark_has_six_items_but_no_target_promotion():
    out = benchmark_fixture("8872468", "8176962", benchmark())
    assert out["valid_fixture"] and out["inventory_count"] == 6 and not out["target_promoted"]


def test_03_p99_lineage_never_carries_requirements():
    out = lineage_object([{"id": "7039079"}, {"id": "8176962"}, {"id": "8872468"}])
    assert out["relation"] == "POSSIBLE_PROJECT_LINEAGE" and not out["requirements_carried_over"]


def test_04_p100_null_supplier_claim_rejected():
    assert bind_supplier_claim(SupplierClaim("insurance", None, None))["state"] == "NULL"


def test_05_p101_unsourced_supplier_claim_rejected():
    assert bind_supplier_claim(SupplierClaim("insurance", "yes", None))["state"] == "UNSOURCED_REJECTED"


def test_06_p102_requirement_join_requires_both_authorities():
    out = requirement_join(False, False, [{"field": "insurance"}], [])
    assert not out["ready"] and out["status"] == "BLOCKED_INPUT_AUTHORITY"


def test_07_p103_missing_evidence_routes_unknown():
    assert route_requirement_gap(True, False) == "UNKNOWN"


def test_08_p104_critical_path_keeps_dates_distinct():
    out = critical_path(ws())
    assert out["clarification_deadline"] != out["submission_deadline"] and not out["dates_conflated"] and not out["demand_proven"]


def test_09_p105_meat_without_weights_cannot_score():
    out = evaluation_detail(ws())
    assert out["mechanism"] == "MEAT" and not out["numeric_score_allowed"] and out["weights"] is None


def test_10_p106_target_pack_rejects_old_pack_attachments():
    out = target_pack_status(ws(), benchmark())
    assert not out["pack_complete"] and out["status"] == "NON_TARGET_ATTACHMENTS_REJECTED"


def test_11_p107_estimated_value_does_not_create_cash_terms():
    out = finance_object(1600000)
    assert out["payment_terms"] is None and out["margin"] is None and out["cash_need"] is None


def test_12_p108_sourced_supplier_claim_is_accepted_only_as_claim():
    out = bind_supplier_claim(SupplierClaim("reference_project", "Project X", "supplier_packet:ref1"))
    assert out["accepted"] and out["state"] == "SOURCE_BOUND"


def test_13_p109_generic_knowledge_cannot_make_missing_requirement_met():
    assert route_requirement_gap(False, True) == "UNKNOWN"


def test_14_p110_bid_burden_requires_observed_inputs():
    out = bid_burden(None, None, 50)
    assert not out["observed"] and out["cost"] is None


def test_15_p111_pa4_requires_complete_supplier_and_independence():
    assert not pa4_gate(False, False, True, True)["pa4"]


def test_16_p112_self_review_cannot_be_pa4():
    assert not pa4_gate(True, True, False, True)["pa4"]


# P113–P128

def test_17_p113_pa5_requires_real_before_after_interaction_fields():
    assert not pa5_evidence(EvidenceObject("PA5"))["pa5"]


def test_18_p114_no_measurement_means_no_time_claim():
    assert bid_burden(6, None, 50)["hours"] is None


def test_19_p115_no_observed_cost_basis_is_null_safe():
    assert bid_burden(6, 4, None)["cost"] is None


def test_20_p116_substitution_with_residual_job_is_hypothesis_only():
    out = substitution_matrix({"free": ["eTenders"]}, "requirement-level supplier gap routing")
    assert out["route"] == "TEST_RESIDUAL" and not out["paid_value_proven"]


def test_21_p117_half_life_is_policy_not_truth():
    out = field_half_life_policy()
    assert out["is_policy_not_truth"] and out["pack_revision"] == "REVALIDATE_BEFORE_DECISION"


def test_22_p118_refresh_appends_and_does_not_mutate_history():
    history = [{"v": 1, "state": "old"}]
    out = immutable_refresh(history, {"v": 2, "state": "new"})
    assert history == [{"v": 1, "state": "old"}] and len(out) == 2 and out[-1]["v"] == 2


def test_23_p119_polish_and_value_cannot_upgrade_proof():
    out = false_confidence_guard(contract_value_present=True, polished=True, pack_complete=False, supplier_verified=False)
    assert not out["proof_upgraded"] and out["pa4"] is False


def test_24_p120_wip_cap_freezes_fourth_lane():
    out = wip_gate(["procurement", "retrofit", "sme-ai", "fourth"])
    assert out["active"] == ["procurement", "retrofit", "sme-ai"] and out["frozen"] == ["fourth"]


def test_25_p121_no_decisive_delta_protects_current_wip():
    out = pareto_protect_no_change([{"name": "proc", "decisive_delta": False}, {"name": "retro", "decisive_delta": False}])
    assert out["route"] == "PROTECT_NO_CHANGE" and out["magic_score"] is None


def test_26_p122_repeated_missing_authority_is_candidate_not_promotion():
    out = si_candidate("MISSING_AUTHORITY_IS_A_FIRST_CLASS_RESULT", ["tender", "property", "workflow"])
    assert out["candidate"] and not out["auto_promoted"] and len(out["cases"]) == 3


def test_27_p123_benchmark_cannot_equal_target():
    out = benchmark_fixture("8872468", "8872468", [Attachment("x", "x", "8872468")])
    assert not out["valid_fixture"] and not out["target_promoted"]


def test_28_p124_independent_review_protocol_needs_all_identity_fields():
    out = independent_review_protocol("bid_manager", True, "targethash", "supplierhash", True)
    assert out["ready"] and out["same_packet_required"] and out["divergence_log_required"]


def test_29_p125_complete_real_use_object_can_reach_pa5_schema_gate():
    obj = EvidenceObject("PA5", "bid_manager", "HOLD", "BID", "meeting:1", "2026-08-22T10:00:00+01:00")
    assert pa5_evidence(obj)["pa5"]


def test_30_p126_compliment_alone_cannot_reach_e3():
    obj = EvidenceObject("E3", "bid_manager", "HOLD", "BID", "meeting:1", "2026-08-22T10:00:00+01:00")
    assert not e3_evidence(obj)["e3"] and not e3_evidence(obj)["compliment_sufficient"]


def test_31_p127_cash_and_binding_provenance_required_for_e4():
    obj = EvidenceObject("E4", "bid_manager", "HOLD", "BID", "meeting:1", "2026-08-22T10:00:00+01:00", "PO issued", 100.0, "receipt:hash")
    assert e4_evidence(obj)["e4"] and not e4_evidence(obj)["listed_price_sufficient"]


def test_32_p128_main_not_recorded_in_pointer_forces_reconcile():
    out = authority_pointer_fresh("4d6dc7c5dc24ea77582327254d339e619173558f", ["470a8aea93385ef8624b47688dbf4cf21090c058", "a8776edcdee14ba67e9fa68c61b3e4f66c10cee3"])
    assert not out["fresh"] and out["status"] == "STOP_RECONCILE"


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failures = []
    for test in tests:
        try:
            test()
            print("PASS", test.__name__)
        except Exception as exc:
            failures.append((test.__name__, exc))
            print("FAIL", test.__name__, type(exc).__name__, exc)
    print(f"{len(tests)-len(failures)}/{len(tests)} PASS")
    raise SystemExit(1 if failures else 0)
