"""Cycle5 P65-P96 additive evidence/economics guards.
This module extends, never replaces, the controlling PA3 artifact engine.
"""
from datetime import datetime
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

UNKNOWN_STRINGS={"","UNKNOWN","NOT_PROVIDED","NULL"}
def is_unknown(v):
    return v is None or (isinstance(v,str) and v.upper() in UNKNOWN_STRINGS)

def age_days(published_iso, observed_iso):
    if is_unknown(published_iso) or is_unknown(observed_iso): return None
    p=datetime.fromisoformat(published_iso.replace("Z","+00:00")); o=datetime.fromisoformat(observed_iso.replace("Z","+00:00"))
    return (o-p).total_seconds()/86400

def expiry_state(published_iso, observed_iso, half_life_days):
    age=age_days(published_iso, observed_iso)
    if age is None or half_life_days is None:return "UNKNOWN"
    if age < 0:return "INVALID_FUTURE_PUBLISHED_DATE"
    if age <= half_life_days:return "FRESH"
    if age <= 2*half_life_days:return "AGING"
    return "EXPIRED_FOR_CURRENT_SIGNAL_USE"

def canonical_url(url):
    if is_unknown(url):return None
    s=urlsplit(url.strip()); q=[]
    for k,v in parse_qsl(s.query,keep_blank_values=True):
        kl=k.lower()
        if not kl.startswith("utm_") and kl not in {"fbclid","gclid"}:q.append((k,v))
    return urlunsplit(((s.scheme or "https").lower(),s.netloc.lower(),(s.path or "/").rstrip("/") or "/",urlencode(sorted(q)),""))

def correlation_key(authority,title,root_url):
    return (str(authority or "").lower().strip()," ".join(str(title or "").lower().split()),canonical_url(root_url))

def notice_state(state,deadline_iso=None,observed_iso=None):
    allowed={"OPEN_TENDER_SUBMISSION","RESTRICTED_TENDER_SUBMISSION","EVALUATION","AWARDED","CLOSED","PIN","UNKNOWN"}
    s=(state or "UNKNOWN").upper()
    if s not in allowed:return "INVALID_STATE"
    if s in {"OPEN_TENDER_SUBMISSION","RESTRICTED_TENDER_SUBMISSION"} and deadline_iso and observed_iso:
        d=datetime.fromisoformat(deadline_iso.replace("Z","+00:00")); o=datetime.fromisoformat(observed_iso.replace("Z","+00:00"))
        if d < o:return "STALE_OPEN_CONTRADICTION"
    return s

def supersession_status(old_version,new_version,same_authority=True):
    if is_unknown(old_version) or is_unknown(new_version):return "UNKNOWN"
    if not same_authority:return "REVIEW_CROSS_AUTHORITY"
    return "SUPERSEDED" if str(old_version)!=str(new_version) else "CURRENT_MATCH"

def budget_buyer_boundary(programme_budget,buyer_intent_evidence=False):
    if programme_budget is not None and not buyer_intent_evidence:return "BUDGET_NOT_BUYER_PROOF"
    return "BUYER_INTENT_SEPARATELY_EVIDENCED" if buyer_intent_evidence else "NO_BUYER_EVIDENCE"

def access_intent_boundary(official_access_path,verified_contact_or_register,buyer_intent_evidence=False):
    if not official_access_path or not verified_contact_or_register:return "NO_VERIFIED_PUBLIC_ACCESS_PATH"
    return "ACCESS_PLUS_SEPARATE_INTENT_EVIDENCE" if buyer_intent_evidence else "PUBLIC_ACCESS_PATH_ONLY"

def market_consumption_state(nonconsumer=False,overshot=False,undershot=False,adequate_source=True):
    if not adequate_source:return "INSUFFICIENT_SOURCE"
    flags=[bool(nonconsumer),bool(overshot),bool(undershot)]
    if sum(flags)>1:return "CONFLICT"
    return "NONCONSUMPTION" if nonconsumer else "OVERSHOT" if overshot else "UNDERSHOT" if undershot else "UNRESOLVED"

def motivation_ability_delta(motivation_change=None,ability_change=None):
    if motivation_change is None or ability_change is None:return {"status":"HOLD_UNKNOWN","motivation":motivation_change,"ability":ability_change}
    return {"status":"TYPED_DELTA","motivation":bool(motivation_change),"ability":bool(ability_change)}

def incumbent_asymmetry(public_pressure,incumbent_constraint_evidence=None):
    if incumbent_constraint_evidence is None:return "PRESSURE_NOT_INCUMBENT_WEAKNESS_PROOF" if public_pressure else "UNKNOWN"
    return "ASYMMETRY_EVIDENCED" if incumbent_constraint_evidence else "NO_ASYMMETRY_EVIDENCED"

def why_now_falsifier(trigger,kill_condition):
    return "FALSIFIABLE_WHY_NOW" if not is_unknown(trigger) and not is_unknown(kill_condition) else "HOLD_MISSING_FALSIFIER"

def fatal_assumption_priority(probability,impact,testability):
    if any(x is None for x in (probability,impact,testability)):return None
    return float(probability)*float(impact)*float(testability)

def shared_assumption_update(opportunity_ids,evidence_id):
    ids=sorted(set(opportunity_ids or []))
    return {"evidence_id":evidence_id,"affected_opportunities":ids,"count_once":True}

def human_delivery_time(observed_minutes,observer_type):
    if observed_minutes is None or observer_type!="HUMAN_OBSERVED":return {"minutes":None,"status":"HOLD_NO_HUMAN_TIMING"}
    return {"minutes":float(observed_minutes),"status":"OBSERVED"}

def anti_fluff_question(asks_past_behavior=False,contains_pitch=False,hypothetical=False):
    if contains_pitch or hypothetical:return "REJECT_LEADING_OR_HYPOTHETICAL"
    return "KEEP_BEHAVIOR_EVIDENCE" if asks_past_behavior else "REWRITE_FOR_OBSERVED_BEHAVIOR"

def e3_capture(raw_quote,role,current_workaround,problem_event,model_inference_only=False):
    if model_inference_only:return "NOT_E3"
    return "E3_CONVERSATION_EVIDENCE" if all([raw_quote,role,current_workaround,problem_event]) else "HOLD_INCOMPLETE_E3"

def e4_payment_proof(kind,amount,date,transaction_id_or_doc):
    if kind not in {"DEPOSIT","PAID_PILOT","PURCHASE_ORDER","PAID_INVOICE"} or amount is None or not date or not transaction_id_or_doc:return "NOT_E4"
    return "E4_TRANSACTION_EVIDENCE"

def pricing_state(external_price_signal=None,hypothesis_range=None):
    return {"price":external_price_signal if external_price_signal is not None else None,"hypothesis_range":hypothesis_range,"evidence":"EXTERNAL_PRICE_SIGNAL" if external_price_signal is not None else "HYPOTHESIS_ONLY"}

def cash_timeline(opening_cash,events):
    balance=float(opening_cash); minimum=balance
    for event in sorted(events or [],key=lambda x:x["date"]):
        balance+=float(event["amount"]); minimum=min(minimum,balance)
    return {"closing_cash":balance,"min_cash":minimum}

def reimbursement_bridge(payment_timing,grant_timing):
    if payment_timing=="UPFRONT_COST" and grant_timing=="POST_WORK_REIMBURSEMENT":return "BRIDGE_REQUIRED"
    if grant_timing=="DEDUCTED_UPFRONT":return "GRANT_REDUCES_UPFRONT_COST"
    return "UNKNOWN_OR_NO_SPECIFIC_BRIDGE"

def funding_topology(customer_prepay=False,supplier_terms=False,grant_upfront=False,grant_reimbursement=False,founder_cash=False):
    out=[]
    if customer_prepay:out.append("CUSTOMER_FUNDED")
    if supplier_terms:out.append("SUPPLIER_TERMS")
    if grant_upfront:out.append("GRANT_UPFRONT")
    if grant_reimbursement:out.append("GRANT_REIMBURSEMENT")
    if founder_cash:out.append("FOUNDER_CASH")
    return out or ["UNKNOWN"]

def contribution_margin(revenue,variable_cost,time_cost=None,rework_cost=None):
    if revenue is None:return {"value":None,"status":"HOLD_NO_REVENUE_EVIDENCE"}
    if any(x is None for x in (variable_cost,time_cost,rework_cost)):return {"value":None,"status":"HOLD_MISSING_COST"}
    return {"value":float(revenue)-float(variable_cost)-float(time_cost)-float(rework_cost),"status":"COMPUTABLE_INPUTS_PRESENT"}

def capacity_state(arrival_rate,service_rate):
    if arrival_rate is None or service_rate in (None,0):return {"utilization":None,"status":"UNKNOWN"}
    u=float(arrival_rate)/float(service_rate)
    return {"utilization":u,"status":"OVERLOAD" if u>=1 else "HIGH_UTILIZATION" if u>=.8 else "BOUNDED"}
