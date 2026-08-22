from engine.public_artifact_engine import current_portfolio, validate_artifact


def run_regression():
    p, r, a = current_portfolio()
    results = []

    def check(name, condition):
        results.append((name, bool(condition)))

    check("T01_procurement_valid", validate_artifact(p) == [])
    check("T02_retrofit_valid", validate_artifact(r) == [])
    check("T03_ai_valid", validate_artifact(a) == [])
    check("T04_public_ceiling_procurement", p.market_claim_grade == "E2+")
    check("T05_public_ceiling_retrofit", r.market_claim_grade == "E2+")
    check("T06_public_ceiling_ai", a.market_claim_grade == "E2+")
    check("T07_no_wtp_procurement", p.outputs["willingness_to_pay_proven"] is False)
    check("T08_no_wtp_retrofit", r.outputs["willingness_to_pay_proven"] is False)
    check("T09_no_wtp_ai", a.outputs["willingness_to_pay_proven"] is False)
    check("T10_unknowns_preserved_procurement", "selection_criteria" in p.unknowns)
    check("T11_unknowns_preserved_retrofit", "property_eligibility" in r.unknowns)
    check("T12_unknowns_preserved_ai", "LEO_confirmation" in a.unknowns)
    check("T13_procurement_not_bid_decision", p.outputs["bid_decision"] == "UNKNOWN")
    check("T14_procurement_not_eligibility_claim", p.outputs["procurement_eligible_proven"] is False)
    check("T15_procurement_deadline_tz", p.inputs["submission_deadline"].endswith("+01:00"))
    check("T16_procurement_live_resource_bound", p.inputs["resource_id"] == "8872468")
    check("T17_retrofit_grant_before_works", any("before works start" in x for x in r.outputs["rules"]))
    check("T18_retrofit_registered_contractor", any("registered contractor" in x for x in r.outputs["rules"]))
    check("T19_retrofit_oss_managed", any("manages assessment" in x for x in r.outputs["rules"]))
    check("T20_retrofit_min_B", any("at least B BER" in x for x in r.outputs["rules"]))
    check("T21_retrofit_no_finance_approval", r.outputs["finance_approved"] is False)
    check("T22_ai_employee_sample_within_range", 1 <= a.inputs["paid_employees"] <= 50)
    check("T23_ai_dfb_within_two_years", a.inputs["digital_for_business_completed_months_ago"] <= 24)
    check("T24_ai_not_EI_IDA", a.inputs["enterprise_ireland_or_ida_client"] is False)
    check("T25_ai_trading_6_months", a.inputs["trading_months"] >= 6)
    check("T26_ai_grant_50_percent", a.outputs["grant_rate"] == 0.50)
    check("T27_ai_grant_max_5000", a.outputs["grant_max_eur"] == 5000)
    check("T28_ai_training_config_cap", a.outputs["training_configuration_share_max"] == 0.50)
    check("T29_ai_analytics_category", "analytics_AI" in a.outputs["candidate_categories"])
    check("T30_ai_new_software", a.inputs["software_new_to_business"] is True)
    check("T31_wip_limit_3", len(current_portfolio()) == 3)
    check("T32_pa_grade_public_internal", all(x.pa_grade == "PA3" for x in current_portfolio()))

    failures = [name for name, ok in results if not ok]
    return results, failures


if __name__ == "__main__":
    results, failures = run_regression()
    for name, ok in results:
        print(f"{'PASS' if ok else 'FAIL'} {name}")
    print(f"SUMMARY {sum(ok for _, ok in results)}/{len(results)} PASS")
    if failures:
        raise SystemExit(1)
