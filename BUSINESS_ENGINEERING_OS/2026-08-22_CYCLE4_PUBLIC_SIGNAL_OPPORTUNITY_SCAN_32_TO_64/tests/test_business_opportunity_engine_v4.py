from business_opportunity_engine_v4 import *


def sig(**kw):
    base = dict(signal_id="S1", title="Official signal", source_url="https://commission.europa.eu/example", jurisdiction="EU", publication_date="2026-08-01", event_date="2026-08-02", application_date="2026-08-02", current=True, cluster_id="C1", forced_action=True)
    base.update(kw)
    return PublicSignal(**base)


def opp(signal=None, **kw):
    signal = signal or sig()
    base = dict(opportunity_id="O1", signal_id=signal.signal_id, buyer_segment="SME", workload="prepare evidence", candidate_offer="evidence workflow", fatal_assumption="pain is material", create_vector="MEDIUM", broker_vector="STRONG", acquire_vector="HOLD", experiment=Experiment("X1","public artifact scan",0,False,"workflow fragmentation"), evidence_level=2, economics=None, data_path="public/forms", audit_source_url=signal.source_url)
    base.update(kw)
    return Opportunity(**base)


def test_01_library_69_plus_2_is_71():
    assert validate_library_authority(69,["ster","hub"],71)["valid"]

def test_02_duplicate_delta_not_double_counted():
    assert validate_library_authority(69,["ster","ster","hub"],71)["valid"]

def test_03_primary_eu_source_accepted():
    assert is_primary_source("https://digital-strategy.ec.europa.eu/en/x")

def test_04_primary_irish_source_accepted():
    assert is_primary_source("https://www.gov.ie/en/x")

def test_05_unrecognised_primary_host_rejected():
    assert validate_signal(sig(source_url="https://blog.example.com/x"))["valid"] is False

def test_06_date_triad_preserved():
    assert validate_signal(sig())["date_triad_preserved"]

def test_07_superseded_signal_rejected():
    assert validate_signal(sig(current=False))["reason"] == "SUPERSEDED_OR_NONCURRENT"

def test_08_cluster_counts_once():
    assert cluster_evidence_weight([sig(signal_id="a",cluster_id="same"),sig(signal_id="b",cluster_id="same")]) == 1

def test_09_distinct_clusters_count_distinct():
    assert cluster_evidence_weight([sig(signal_id="a",cluster_id="a"),sig(signal_id="b",cluster_id="b")]) == 2

def test_10_valid_public_opportunity():
    s=sig(); assert validate_opportunity(s,opp(s))["valid"]

def test_11_public_evidence_cannot_exceed_2():
    s=sig(); assert validate_opportunity(s,opp(s,evidence_level=3))["reason"] == "PUBLIC_RESEARCH_EVIDENCE_CEILING_EXCEEDED"

def test_12_deadline_does_not_prove_wtp():
    s=sig(forced_action=True); assert validate_opportunity(s,opp(s,wtp_proven=True))["valid"] is False

def test_13_forced_action_does_not_prove_commitment():
    s=sig(forced_action=True); assert validate_opportunity(s,opp(s,buyer_commitment=True))["valid"] is False

def test_14_grant_signal_does_not_prove_award():
    s=sig(); assert validate_opportunity(s,opp(s,financing_awarded=True))["valid"] is False

def test_15_grant_bridge_is_eligibility_only():
    assert grant_bridge(eligible=True)["awarded"] is False

def test_16_award_cannot_be_self_asserted():
    assert grant_bridge(eligible=True,awarded=True)["reason"] == "AWARD_REQUIRES_EXTERNAL_AWARD_EVIDENCE"

def test_17_unknown_economics_remain_null():
    s=sig(); out=validate_opportunity(s,opp(s)); assert out["economics_unknown"] is True

def test_18_no_magic_total_score():
    s=sig(); assert validate_opportunity(s,opp(s))["magic_total_score"] is None

def test_19_fatal_assumption_required():
    s=sig(); assert validate_opportunity(s,opp(s,fatal_assumption=""))["valid"] is False

def test_20_zero_cash_test_selected():
    x=select_zero_cash_decisive_test([Experiment("paid","paid",10,False,"x"),Experiment("free","public",0,False,"x")]); assert x.experiment_id=="free"

def test_21_outreach_test_rejected_in_current_mode():
    s=sig(); x=Experiment("x","interview",0,True,"demand"); assert validate_opportunity(s,opp(s,experiment=x))["reason"] == "OUTREACH_PROHIBITED"

def test_22_nonzero_founder_cash_test_rejected():
    s=sig(); x=Experiment("x","ad test",5,False,"demand"); assert validate_opportunity(s,opp(s,experiment=x))["reason"] == "NONZERO_FOUNDER_CASH_TEST"

def test_23_source_binding_required():
    s=sig(); assert validate_opportunity(s,opp(s,audit_source_url="https://gov.ie/other"))["reason"] == "AUDIT_SOURCE_BINDING_REQUIRED"

def test_24_no_legal_advice_boundary():
    s=sig(); assert validate_opportunity(s,opp(s,not_legal_advice=False))["valid"] is False

def test_25_no_automation_adjudication():
    s=sig(); assert validate_opportunity(s,opp(s,automation_adjudicates_compliance=True))["valid"] is False

def test_26_data_path_gate_holds():
    assert automation_readiness(opp(data_path=None))["ready"] is False

def test_27_data_path_allows_evidence_workflow_only():
    assert automation_readiness(opp())["ready"] is True

def test_28_external_capital_is_not_free():
    assert external_capital("GRANT",10000)["free"] is False

def test_29_transposition_gap_not_final_rule():
    assert transposition_state(eu_rule="NIS2",national_status="PENDING")["final_national_detail_proven"] is False

def test_30_public_artifact_is_proxy_only():
    assert public_artifact_proxy("https://gov.ie/form")["proxy_only"] is True

def test_31_portfolio_wip_cap():
    out=portfolio_wip([str(i) for i in range(10)],cap=5); assert len(out["active"])==5 and len(out["queued"])==5 and out["bounded"]

def test_32_si_candidate_never_auto_promotes():
    out=self_improvement_candidate("deadline_ne_demand",3,["a","b","a"]); assert out["status"]=="CANDIDATE_DISCOVERY_ONLY" and out["auto_promoted"] is False and out["evidence_refs"]==["a","b"]


if __name__ == "__main__":
    import sys
    tests=[obj for name,obj in sorted(globals().items()) if name.startswith("test_") and callable(obj)]
    fails=[]
    for t in tests:
        try:
            t(); print("PASS",t.__name__)
        except Exception as e:
            fails.append((t.__name__,e)); print("FAIL",t.__name__,type(e).__name__,e)
    print(f"{len(tests)-len(fails)}/{len(tests)} PASS")
    sys.exit(1 if fails else 0)
