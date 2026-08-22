from __future__ import annotations
from typing import Any

AUTH={"OFFICIAL_PRIMARY":5,"INDUSTRY_PRIMARY":4,"OFFICIAL_SECONDARY":3,"TRUSTED_SECONDARY":2,"DISCOVERY_ONLY":1}

def authority_score(level:str)->int:
    return AUTH[level]

def correlation_dedupe(signals:list[dict[str,Any]])->list[dict[str,Any]]:
    best={}
    for s in signals:
        key=s["correlation_group"]
        cur=best.get(key)
        if cur is None or authority_score(s["source_authority"])>authority_score(cur["source_authority"]): best[key]=s
    return list(best.values())

def why_now(signal:dict[str,Any], forced_action:str, payer:str|None, falsifier:str)->dict[str,Any]:
    return {"event":signal["title"],"date":signal["published_at"],"actor":signal.get("actor"),"forced_action":forced_action,"payer":payer,"deadline":signal.get("deadline"),"falsifier":falsifier}

def buyer_workload(buyer:str, workload:str)->dict[str,Any]:
    return {"buyer":buyer,"workload":workload,"willingness_to_pay":None}

def classify_change(signal:dict[str,Any])->dict[str,str]:
    txt=(signal["claim"]+" "+signal["title"]).lower()
    motivation="MOTIVATION_UP" if any(k in txt for k in ["grant","funding","budget","capital plan"]) else "FORCED_ACTION" if any(k in txt for k in ["obligation","nis2","act","compliance"]) else "UNCLEAR"
    ability="ABILITY_UP" if any(k in txt for k in ["framework","register","training","support","voucher"]) else "UNCLEAR"
    return {"motivation":motivation,"ability":ability}

def micro_market_gate(o:dict[str,Any])->dict[str,Any]:
    missing=[k for k in ["buyer_segment","buyer_workload","offer","manual_first_deliverable"] if not o.get(k)]
    if o.get("evidence_grade") not in {"E1","E2","E2+"}: missing.append("public_evidence")
    return {"verdict":"PASS" if not missing else "HOLD","missing":missing}

def rank_fatal_assumptions(items:list[dict[str,Any]])->list[dict[str,Any]]:
    out=[]
    for x in items:
        out.append({**x,"priority":round(float(x.get("kill_power",0))*float(x.get("uncertainty",0))*float(x.get("testability",0)),4)})
    return sorted(out,key=lambda z:z["priority"],reverse=True)

def choose_no_outreach_experiment(experiments:list[dict[str,Any]])->dict[str,Any]|None:
    eligible=[x for x in experiments if float(x.get("founder_cash_eur",0))==0 and not x.get("requires_buyer_contact",False)]
    if not eligible: return None
    for x in eligible:
        denom=max(0.1,float(x.get("time_hours",1))+float(x.get("latency_days",0))/7)
        x["voi_rate"]=float(x.get("decision_value",0))*float(x.get("flip_probability",0))/denom
    return max(eligible,key=lambda x:x["voi_rate"])

def decay(signal_age_days:int,sla_days:int)->str:
    if signal_age_days<=sla_days: return "FRESH"
    if signal_age_days<=2*sla_days: return "REVALIDATE"
    return "STALE"

def dedupe_opportunities(ops:list[dict[str,Any]])->list[dict[str,Any]]:
    best={}
    for o in ops:
        key=(o["buyer_segment"].lower(),o["buyer_workload"].lower(),o["offer"].lower())
        if key not in best: best[key]=o
    return list(best.values())

def seven_domains_gate(o:dict[str,Any])->dict[str,Any]:
    fatal=[]
    if not o.get("buyer_segment"): fatal.append("no_target_micro_market")
    if not o.get("why_now"): fatal.append("no_why_now")
    if not o.get("manual_first_deliverable"): fatal.append("no_manual_first_deliverable")
    if o.get("founder_cash_pre_proof_eur",0)>0: fatal.append("founder_cash_required_pre_proof")
    if o.get("legal_blocker") is True: fatal.append("legal_blocker")
    if o.get("access_path") in [None,""]: fatal.append("no_access_path")
    return {"verdict":"RESHAPE_OR_KILL" if fatal else "PASS_TO_TEST","fatal":fatal}

def route_vectors(o:dict[str,Any])->dict[str,Any]:
    return {"CREATE":{"cash_gap":o.get("create_cash_gap"),"time_to_proof":o.get("create_time"),"risk":o.get("create_risk"),"control":o.get("create_control")},"BROKER":{"cash_gap":o.get("broker_cash_gap",0),"time_to_proof":o.get("broker_time",1),"risk":o.get("broker_risk",1),"control":o.get("broker_control",2)},"ACQUIRE":{"cash_gap":o.get("acquire_cash_gap"),"time_to_proof":o.get("acquire_time"),"risk":o.get("acquire_risk"),"control":o.get("acquire_control")}}

def recurring_value_gate(recurring_job:bool, recurring_value:bool)->str:
    return "PASS" if recurring_job and recurring_value else "NO_RETAINER_YET"

def power_gate(repeatable_value:bool, benefit:bool, barrier:bool)->str:
    if not repeatable_value: return "TOO_EARLY"
    return "PASS" if benefit and barrier else "HOLD_NO_POWER"

def acquisition_stress(price, sde, annual_debt_service):
    if None in [price,sde,annual_debt_service]: return {"verdict":"HOLD_NULL_INPUT","dscr":None}
    dscr=sde/max(1e-9,annual_debt_service)
    return {"verdict":"PASS" if dscr>=1.5 else "FAIL","dscr":dscr}

def graduation(evidence_grade:str, paid_repeat_buyers:int=0, unit_economics_known:bool=False)->str:
    return "EXPLOIT_ELIGIBLE" if evidence_grade in {"E4","E5","E6","E7"} and paid_repeat_buyers>=3 and unit_economics_known else "EXPLORE"

def portfolio_select(ops:list[dict[str,Any]],limit:int=3)->dict[str,Any]:
    ranked=sorted(ops,key=lambda o:(o.get("survival",0),o.get("public_signal_strength",0),o.get("voi_priority",0)),reverse=True)
    chosen=ranked[:limit]
    return {"PRIMARY":chosen[0]["opportunity_id"] if chosen else None,"PILOTS":[x["opportunity_id"] for x in chosen[1:3]],"wip_limit":3}
