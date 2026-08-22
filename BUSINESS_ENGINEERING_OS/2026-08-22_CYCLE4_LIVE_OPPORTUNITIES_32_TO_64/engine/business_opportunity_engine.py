from __future__ import annotations
from datetime import datetime,timedelta

BARRIER_ORDER={"LOW":0,"MEDIUM":1,"HIGH":2}

def _date(s): return datetime.strptime(s,"%Y-%m-%d").date()

def freshness(signal,asof="2026-08-22"):
    age=(_date(asof)-_date(signal["observed"])).days
    ttl=int(signal.get("freshness_days",30))
    return {"age_days":age,"ttl_days":ttl,"fresh":age<=ttl}

def buyer_workload(opportunity):
    return {"buyer_segment":opportunity["buyer_segment"],"observable_workload":opportunity["deliverable"],
            "willingness_to_pay":None,"law":"PUBLIC_WORKLOAD_DOES_NOT_PROVE_WTP"}

def micro_market_gate(o):
    reasons=[]
    if not o.get("buyer_segment"): reasons.append("NO_BUYER_SEGMENT")
    if not o.get("deliverable"): reasons.append("NO_DELIVERABLE")
    if not o.get("fatal_assumption"): reasons.append("NO_FATAL_ASSUMPTION")
    if o.get("founder_cash_pre_E4_eur",999)>0: reasons.append("FOUNDER_CASH_PRE_E4")
    return {"pass":not reasons,"reasons":reasons}

def public_experiment(o):
    return {"opportunity_id":o["id"],"hypothesis":o["fatal_assumption"],
            "test":o["cheapest_no_outreach_test"],"founder_cash_eur":0,"outreach":False,
            "evidence_ceiling":"E2+","failure_event":o["kill_rule"]}

def founder_cash_timeline(o):
    return {"pre_E4":0,"E4_payment_or_PO_required_before_spend":True,
            "pass":o["founder_cash_pre_E4_eur"]==0}

def funding_topology(o):
    routes=["CLIENT_DEPOSIT","PO","RETAINER","COMMISSION","SUPPLIER_TERMS","INVOICE_FINANCE","LOAN","GRANT_UPFRONT","GRANT_REIMBURSABLE","INVESTOR"]
    return [{"route":r,"founder_cash_zero_compatible":r in {"CLIENT_DEPOSIT","PO","RETAINER","COMMISSION","SUPPLIER_TERMS","GRANT_UPFRONT"},
             "approval_or_availability_proven":False} for r in routes]

def create_broker_acquire(o):
    barrier=o["credential_barrier"]
    return {"CREATE":{"feasible_preproof":o["business_type"]=="SERVICE" and barrier!="HIGH"},
            "BROKER":{"feasible_preproof":True,"requires_partner_proof":barrier=="HIGH"},
            "ACQUIRE":{"feasible_preproof":False,"reason":"capital/financing unknown"},
            "recommended":"BROKER" if barrier=="HIGH" or o["route"]=="BROKER" else "CREATE"}

def seven_domains_gate(o):
    domains={"micro_market":bool(o["buyer_segment"]),"problem_or_forced_work":bool(o["signal_fact"]),
             "offer":bool(o["deliverable"]),"access_or_route":o["route"] in {"CREATE","BROKER","ACQUIRE"},
             "economics_known":o["unit_economics"] is not None,
             "team_credentials_fit":o["credential_barrier"]!="HIGH",
             "cash_preproof_ok":o["founder_cash_pre_E4_eur"]==0}
    fatal=[k for k,v in domains.items() if not v and k!="economics_known"]
    disposition="HOLD_SPECIALIST" if "team_credentials_fit" in fatal else ("KILL_OR_RESHAPE" if fatal else "PASS_TO_TEST")
    return {"domains":domains,"fatal":fatal,"disposition":disposition,"economics_status":"NULL_PRE_PAYMENT"}

def recurring_value_gate(o):
    return {"retainer_authorized":False,"reason":"No repeated paid delivery evidence."}

def acquisition_stress(o):
    return {"purchase_price":None,"debt_service":None,"cash_flow":None,"dscr":None,"verdict":"NULL_NOT_COMPUTABLE"}

def graduation_gate(o):
    return {"phase":"EXPLORE","exploit_authorized":o["derived_offer_market_grade"] in {"E5","E6","E7"}}

def _pareto_key(o):
    return (0 if o["founder_cash_pre_E4_eur"]==0 else 1,BARRIER_ORDER.get(o["credential_barrier"],3),
            0 if o["manual_deliverable_possible"] else 1,0 if o["route"]=="CREATE" else 1,o["id"])

def portfolio_dashboard(opps,max_active=3):
    eligible=[];hold=[]
    for o in opps:
        g=seven_domains_gate(o)
        if g["disposition"]=="PASS_TO_TEST" and micro_market_gate(o)["pass"]: eligible.append(o)
        else: hold.append({"id":o["id"],"reason":g["disposition"]})
    chosen=sorted(eligible,key=_pareto_key)[:max_active]
    return {"primary":chosen[0]["id"] if chosen else None,"pilots":[x["id"] for x in chosen[1:3]],
            "active_count":len(chosen),"wip_cap":max_active,"eligible_count":len(eligible),"hold":hold}

def red_team(opps,signals):
    issues=[]; sig={s["id"]:s for s in signals}
    for o in opps:
        if o["derived_offer_market_grade"] in {"E3","E4","E5","E6","E7"} and o["willingness_to_pay"] is None:
            issues.append({"id":o["id"],"fatal":"FALSE_MARKET_PROMOTION"})
        if not freshness(sig[o["signal_id"]])["fresh"]: issues.append({"id":o["id"],"fatal":"STALE_SIGNAL"})
        if o["credential_barrier"]=="HIGH" and create_broker_acquire(o)["recommended"]=="CREATE":
            issues.append({"id":o["id"],"fatal":"CREDENTIAL_BARRIER_IGNORED"})
        if o["founder_cash_pre_E4_eur"]>0: issues.append({"id":o["id"],"fatal":"ZERO_CASH_BREACH"})
    return {"fatal_count":len(issues),"issues":issues,"pass":not issues}
