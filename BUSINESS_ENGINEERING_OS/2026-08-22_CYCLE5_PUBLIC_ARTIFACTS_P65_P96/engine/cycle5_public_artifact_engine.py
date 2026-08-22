from __future__ import annotations
from datetime import datetime, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode
from typing import Any
import re

PUBLIC_EVIDENCE_CEILING = "E2+"
ACTIVE_WIP_LIMIT = 3
TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {"trk","gclid","fbclid","mc_cid","mc_eid"}
IDENTITY_QUERY_KEYS = {"resourceId"}

def _parse_iso(value: str) -> datetime:
    value = value.strip().replace("Z","+00:00")
    d = datetime.fromisoformat(value)
    if d.tzinfo is None:
        d = d.replace(tzinfo=timezone.utc)
    return d

def canonical_official_url(url: str, identity_keys: set[str] | None = None) -> str:
    identity_keys = identity_keys or IDENTITY_QUERY_KEYS
    p = urlsplit(url)
    pairs = []
    for k, v in parse_qsl(p.query, keep_blank_values=True):
        if k in identity_keys:
            pairs.append((k, v))
        elif k in TRACKING_KEYS or any(k.startswith(x) for x in TRACKING_PREFIXES):
            continue
    pairs.sort()
    return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path, urlencode(pairs), ""))

def signal_freshness(published_at: str, observed_at: str, sla_days: int) -> dict[str, Any]:
    pub, obs = _parse_iso(published_at), _parse_iso(observed_at)
    age = max(0, (obs - pub).days)
    status = "FRESH" if age <= sla_days else "REVALIDATE" if age <= 2*sla_days else "STALE"
    return {"age_days": age, "sla_days": sla_days, "status": status}

def syndication_family_key(signal: dict[str, Any]) -> str:
    issuer = re.sub(r"\W+", " ", signal.get("issuer","").lower()).strip()
    title = re.sub(r"\W+", " ", signal.get("title","").lower()).strip()
    event = signal.get("event_date") or signal.get("published_at") or ""
    return f"{issuer}|{title}|{event[:10]}"

def dedupe_syndicated(signals: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rank = {"OFFICIAL_PRIMARY":5,"OFFICIAL_PORTAL":5,"OFFICIAL_SECONDARY":4,"INDUSTRY_PRIMARY":3,"TRUSTED_SECONDARY":2,"DISCOVERY_ONLY":1}
    best: dict[str, dict[str, Any]] = {}
    for s in signals:
        key = s.get("evidence_family_id") or syndication_family_key(s)
        cur = best.get(key)
        if cur is None or rank.get(s.get("source_authority","DISCOVERY_ONLY"),0) > rank.get(cur.get("source_authority","DISCOVERY_ONLY"),0):
            best[key] = s
    return list(best.values())

def procurement_state(deadline_at: str | None, observed_at: str, portal_status: str | None, award_date: str | None = None) -> dict[str, Any]:
    if award_date:
        return {"state":"AWARDED","contradiction":False}
    if not deadline_at:
        return {"state":"UNKNOWN","contradiction":False}
    deadline, obs = _parse_iso(deadline_at), _parse_iso(observed_at)
    portal = (portal_status or "").upper()
    if obs > deadline:
        if "TENDER SUBMISSION" in portal or portal == "OPEN":
            return {"state":"REVALIDATE_STATUS_CONTRADICTION","contradiction":True}
        return {"state":"CLOSED_OR_EVALUATION","contradiction":False}
    if "TENDER SUBMISSION" in portal or portal == "OPEN":
        return {"state":"OPEN","contradiction":False}
    return {"state":"REVALIDATE_PORTAL_STATUS","contradiction":True}

def resolve_supersession(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = {}
    for r in records:
        grouped.setdefault(r["policy_id"], []).append(r)
    out = []
    for _, items in grouped.items():
        items = sorted(items, key=lambda x: _parse_iso(x["effective_at"]))
        latest = items[-1]
        for x in items:
            y = dict(x)
            y["current_authority"] = x is latest
            y["weight"] = 1 if x is latest else 0
            out.append(y)
    return out

def budget_owner_gate(program_budget: float | None, buyer_identified: bool, official_budget_owner: bool) -> dict[str, Any]:
    if program_budget is None:
        return {"buyer_proven":False,"budget_owner_confidence":"UNKNOWN"}
    if buyer_identified and official_budget_owner:
        return {"buyer_proven":True,"budget_owner_confidence":"HIGH"}
    return {"buyer_proven":False,"budget_owner_confidence":"LOW_PROGRAMME_BUDGET_ONLY"}

def buyer_access_path(path: dict[str, Any]) -> str:
    if path.get("official_register") or path.get("official_procurement_portal"):
        return "PUBLIC_PATH_VERIFIED"
    return "HOLD_NO_OFFICIAL_ACCESS_PATH"

def market_state_classifier(*, current_consumption: bool, underserved: bool, overserved: bool) -> str:
    if not current_consumption: return "NONCONSUMPTION"
    if underserved: return "UNDERSHOT"
    if overserved: return "OVERSHOT"
    return "CURRENTLY_SERVED_UNCLEAR"

def motivation_ability(signal: dict[str, Any]) -> dict[str, str]:
    motivation = "UP" if signal.get("funding") or signal.get("obligation") or signal.get("deadline") else "UNCLEAR"
    ability = "UP" if signal.get("support") or signal.get("framework") or signal.get("registered_provider_path") else "UNCLEAR"
    return {"motivation":motivation, "ability":ability}

def incumbent_asymmetry(*, incumbent_margin_attractive: bool, new_model_requires_different_process: bool, entrant_low_cost: bool) -> str:
    if incumbent_margin_attractive and new_model_requires_different_process and entrant_low_cost:
        return "ASYMMETRY_PLAUSIBLE_TEST"
    return "NO_CLEAR_ASYMMETRY"

def why_now_falsifier(claim: str, kill_condition: str, current_evidence: bool) -> dict[str, Any]:
    return {"claim":claim,"kill_condition":kill_condition,"status":"SURVIVES_PUBLIC_TEST" if current_evidence else "KILLED_OR_HOLD"}

def opportunity_half_life(signal_class: str) -> int:
    return {"PROCUREMENT_OPEN":7,"GRANT_OPEN":14,"REGULATORY_CHANGE":30,"POLICY_DIRECTION":90,"EVERGREEN_SUPPORT":90}.get(signal_class,30)

def rank_fatal_assumptions(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out=[]
    for x in items:
        z=dict(x); z["priority"]=round(float(x.get("kill_power",0))*float(x.get("uncertainty",0))*float(x.get("testability",0)),4); out.append(z)
    return sorted(out,key=lambda x:x["priority"],reverse=True)

def shared_assumption_graph(opportunities: list[dict[str, Any]]) -> dict[str, list[str]]:
    graph: dict[str,list[str]]={}
    for o in opportunities:
        for a in o.get("assumptions",[]): graph.setdefault(a,[]).append(o["opportunity_id"])
    return {k:sorted(v) for k,v in graph.items() if len(v)>1}

def select_no_outreach_experiment(experiments: list[dict[str, Any]]) -> dict[str, Any] | None:
    candidates=[e for e in experiments if e.get("founder_cash_eur",0)==0 and not e.get("requires_buyer_contact",False)]
    if not candidates: return None
    for e in candidates:
        denom=max(0.25,float(e.get("time_hours",1))+float(e.get("latency_days",0))/7)
        e["voi_rate"]=float(e.get("decision_value",0))*float(e.get("flip_probability",0))/denom
    return max(candidates,key=lambda e:e["voi_rate"])

def artifact_evidence_gate(artifact: dict[str, Any]) -> dict[str, Any]:
    return {"artifact_exists":bool(artifact.get("content")),"evidence_ceiling":PUBLIC_EVIDENCE_CEILING,"buyer_proof":False,"payment_proof":False,"willingness_to_pay":None}

def delivery_time_record(machine_seconds: float | None, human_review_minutes: float | None = None) -> dict[str, Any]:
    return {"machine_generation_seconds_observed":machine_seconds,"human_review_minutes_observed":human_review_minutes}

def e3_capture(event: dict[str, Any]) -> str:
    return "E3" if bool(event.get("external_buyer")) and bool(event.get("behavioral_signal")) else "HOLD_BELOW_E3"

def e4_payment_proof(event: dict[str, Any]) -> str:
    paid=float(event.get("cash_received",0) or 0)>0
    binding=bool(event.get("purchase_order") or event.get("paid_pilot_contract") or event.get("deposit"))
    return "E4" if paid and binding else "HOLD_BELOW_E4"

def pricing_schema(external_price_signal: float | None) -> dict[str, Any]:
    return {"price":external_price_signal if external_price_signal is not None else None,"status":"EXTERNAL_SIGNAL" if external_price_signal is not None else "NULL_UNTIL_EXTERNAL_SIGNAL"}

def founder_cash_timeline(events: list[dict[str, Any]]) -> dict[str, Any]:
    committed=[e for e in events if e.get("committed") is True]; hypothetical=[e for e in events if e.get("committed") is not True]
    return {"committed_net_cash":sum(float(e.get("amount",0)) for e in committed),"committed_events":committed,"hypothetical_events":hypothetical}

def reimbursement_bridge(grant: dict[str, Any]) -> str:
    if grant.get("reimbursement_after_spend"): return "WORKING_CAPITAL_REQUIRED"
    if grant.get("deducted_upfront"): return "UPFRONT_BRIDGE_REDUCED"
    return "UNKNOWN_CASH_TIMING"

def funding_topology(*, payer: str | None, funding_source: str | None, upfront_cash_required: bool | None) -> dict[str, Any]:
    if not payer or not funding_source or upfront_cash_required is None:
        return {"status":"HOLD_UNKNOWN_TOPOLOGY","payer":payer,"funding_source":funding_source,"upfront_cash_required":upfront_cash_required}
    return {"status":"MAPPED","payer":payer,"funding_source":funding_source,"upfront_cash_required":upfront_cash_required}

def working_capital_stress(*, materials: float | None, labour: float | None, grant_reimbursement: float | None, customer_deposit: float | None) -> dict[str, Any]:
    if None in (materials,labour,grant_reimbursement,customer_deposit): return {"peak_pre_finance_cash":None,"status":"HOLD_NULL_INPUT"}
    peak=max(0.0,float(materials)+float(labour)-float(customer_deposit)); gap=max(0.0,peak-float(grant_reimbursement))
    return {"peak_pre_finance_cash":peak,"residual_after_grant":gap,"status":"MODELLED_NOT_OBSERVED"}

def contribution_margin(*, price: float | None, variable_cost: float | None, delivery_hours: float | None, hourly_time_cost: float | None, rework_cost: float | None=0) -> dict[str, Any]:
    if None in (price,variable_cost,delivery_hours,hourly_time_cost): return {"contribution":None,"status":"HOLD_NULL_INPUT"}
    total=float(variable_cost)+float(delivery_hours)*float(hourly_time_cost)+float(rework_cost or 0)
    return {"contribution":float(price)-total,"status":"MODELLED_NOT_OBSERVED"}

def service_queue(*, arrival_per_week: float | None, service_hours_per_case: float | None, available_hours_per_week: float | None) -> dict[str, Any]:
    if None in (arrival_per_week,service_hours_per_case,available_hours_per_week): return {"utilization":None,"status":"HOLD_NULL_INPUT"}
    util=float(arrival_per_week)*float(service_hours_per_case)/max(1e-9,float(available_hours_per_week))
    return {"utilization":util,"status":"OVERLOADED" if util>=1 else "CAPACITY_AVAILABLE"}

def wip_gate(primary: str | None, pilots: list[str]) -> dict[str, Any]:
    if not primary: return {"status":"HOLD_NO_PRIMARY","count":len(pilots)}
    count=1+len(pilots)
    return {"status":"PASS" if count<=ACTIVE_WIP_LIMIT else "FREEZE_EXCESS","count":count,"limit":ACTIVE_WIP_LIMIT}
