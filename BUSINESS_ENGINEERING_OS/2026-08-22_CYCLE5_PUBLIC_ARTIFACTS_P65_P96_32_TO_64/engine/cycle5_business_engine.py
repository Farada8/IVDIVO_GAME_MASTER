"""IVDIVO Business Engineering OS Cycle5 bounded runtime.
Engineering/public-artifact utilities only. No market, legal, buyer or payment proof is inferred.
"""
from datetime import datetime
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

def _unknown(v):
    return v is None or v == "" or (isinstance(v,str) and v.upper() in {"UNKNOWN","NOT_PROVIDED","NULL"})

def age_days(published_iso, observed_iso):
    if _unknown(published_iso) or _unknown(observed_iso): return None
    p=datetime.fromisoformat(published_iso.replace("Z","+00:00"))
    o=datetime.fromisoformat(observed_iso.replace("Z","+00:00"))
    return (o-p).total_seconds()/86400

def expiry_state(published_iso, observed_iso, half_life_days=None):
    a=age_days(published_iso, observed_iso)
    if a is None or half_life_days is None: return "UNKNOWN"
    if a < 0: return "INVALID_FUTURE_PUBLISHED_DATE"
    if a <= half_life_days: return "FRESH"
    if a <= 2*half_life_days: return "AGING"
    return "EXPIRED_FOR_CURRENT_SIGNAL_USE"

def canonical_url(url):
    if _unknown(url): return None
    s=urlsplit(url.strip())
    q=[(k,v) for k,v in parse_qsl(s.query, keep_blank_values=True)
       if not (k.lower().startswith("utm_") or k.lower() in {"fbclid","gclid"})]
    scheme=(s.scheme or "https").lower()
    host=s.netloc.lower()
    path=s.path or "/"
    return urlunsplit((scheme,host,path.rstrip("/") or "/",urlencode(sorted(q)),""))

def correlation_key(source_authority, title, root_url=None):
    return (str(source_authority).lower().strip(),
            " ".join((title or "").lower().split()),
            canonical_url(root_url))

VALID_NOTICE_STATES={"OPEN_TENDER_SUBMISSION","RESTRICTED_TENDER_SUBMISSION","EVALUATION","AWARDED","CLOSED","PIN","UNKNOWN"}
def verify_notice_state(state, deadline_iso=None, observed_iso=None):
    s=(state or "UNKNOWN").upper()
    if s not in VALID_NOTICE_STATES: return {"status":"INVALID_STATE"}
    if s in {"OPEN_TENDER_SUBMISSION","RESTRICTED_TENDER_SUBMISSION"} and deadline_iso and observed_iso:
        d=datetime.fromisoformat(deadline_iso.replace("Z","+00:00"))
        o=datetime.fromisoformat(observed_iso.replace("Z","+00:00"))
        if d < o: return {"status":"STALE_OPEN_CONTRADICTION"}
    return {"status":s}

def budget_buyer_guard(programme_budget, buyer_evidence=False):
    if programme_budget is not None and not buyer_evidence:
        return {"status":"BUDGET_NOT_BUYER_PROOF","buyer":None}
    return {"status":"BUYER_EVIDENCED" if buyer_evidence else "NO_BUYER_EVIDENCE"}

def access_path_guard(official_path, contact_or_register_exists, intent_evidence=False):
    if not official_path or not contact_or_register_exists:
        return {"status":"NO_VERIFIED_PUBLIC_ACCESS_PATH"}
    return {"status":"PUBLIC_ACCESS_PATH_ONLY" if not intent_evidence else "ACCESS_PLUS_SEPARATE_INTENT_EVIDENCE"}

def market_state(nonconsumer=False, overshot=False, undershot=False, adequate_source=True):
    if not adequate_source: return "INSUFFICIENT_SOURCE"
    flags=[nonconsumer,overshot,undershot]
    if sum(bool(x) for x in flags)>1: return "CONFLICT"
    if nonconsumer:return "NONCONSUMPTION"
    if overshot:return "OVERSHOT"
    if undershot:return "UNDERSHOT"
    return "UNRESOLVED"

def why_now_falsifier(trigger, kill_condition):
    if _unknown(trigger) or _unknown(kill_condition): return "HOLD_MISSING_FALSIFIER"
    return "FALSIFIABLE_WHY_NOW"

def fatal_assumption_score(probability, impact, testability):
    if any(v is None for v in (probability,impact,testability)): return None
    return probability*impact*testability

def artifact_gate(source_count, as_of_date, unknowns_labeled, evidence_ceiling_labeled, actionable_next_step):
    ok=source_count>0 and bool(as_of_date) and unknowns_labeled and evidence_ceiling_labeled and actionable_next_step
    return "PASS_PUBLIC_ARTIFACT" if ok else "FAIL_ARTIFACT_CONTRACT"

def human_delivery_time(observed_minutes, observer_type):
    if observer_type!="HUMAN_OBSERVED" or observed_minutes is None:
        return {"human_minutes":None,"status":"HOLD_NO_HUMAN_TIMING"}
    return {"human_minutes":float(observed_minutes),"status":"OBSERVED"}

def anti_fluff_question(question, asks_past_behavior=False, contains_pitch=False, hypothetical=False):
    if contains_pitch or hypothetical: return "REJECT_LEADING_OR_HYPOTHETICAL"
    if asks_past_behavior: return "KEEP_BEHAVIOR_EVIDENCE"
    return "REWRITE_FOR_OBSERVED_BEHAVIOR"

def e3_capture(raw_quote, role, current_workaround, problem_event, model_inference_only=False):
    if model_inference_only: return {"status":"NOT_E3"}
    if all([raw_quote,role,current_workaround,problem_event]): return {"status":"E3_CONVERSATION_EVIDENCE"}
    return {"status":"HOLD_INCOMPLETE_E3"}

def e4_payment_proof(kind, amount, date, transaction_id_or_doc):
    accepted={"DEPOSIT","PAID_PILOT","PURCHASE_ORDER","PAID_INVOICE"}
    if kind not in accepted or amount is None or not date or not transaction_id_or_doc:
        return {"status":"NOT_E4"}
    return {"status":"E4_TRANSACTION_EVIDENCE","kind":kind,"amount":amount}

def pricing_schema(external_signal=None, hypothesis_range=None):
    if external_signal is None:
        return {"price":None,"hypothesis_range":hypothesis_range,"evidence":"HYPOTHESIS_ONLY"}
    return {"price":external_signal,"hypothesis_range":hypothesis_range,"evidence":"EXTERNAL_PRICE_SIGNAL"}

def cash_timeline(opening_cash, events):
    balance=float(opening_cash); out=[]
    for e in sorted(events,key=lambda x:x["date"]):
        amt=float(e["amount"]); balance += amt
        out.append({"date":e["date"],"amount":amt,"balance":balance,"kind":e.get("kind","UNKNOWN")})
    return {"closing_cash":balance,"min_cash":min([opening_cash]+[x["balance"] for x in out]),"events":out}

def reimbursement_bridge(payment_timing, grant_timing):
    if payment_timing=="UPFRONT_COST" and grant_timing=="POST_WORK_REIMBURSEMENT": return "BRIDGE_REQUIRED"
    if grant_timing=="DEDUCTED_UPFRONT": return "GRANT_REDUCES_UPFRONT_COST"
    return "UNKNOWN_OR_NO_SPECIFIC_BRIDGE"

def funding_topology(customer_prepay=False,supplier_terms=False,grant_upfront=False,grant_reimbursement=False,founder_cash=False):
    modes=[]
    if customer_prepay:modes.append("CUSTOMER_FUNDED")
    if supplier_terms:modes.append("SUPPLIER_TERMS")
    if grant_upfront:modes.append("GRANT_UPFRONT")
    if grant_reimbursement:modes.append("GRANT_REIMBURSEMENT")
    if founder_cash:modes.append("FOUNDER_CASH")
    return modes or ["UNKNOWN"]

def contribution_margin(revenue, variable_cost, time_cost=0.0, rework_cost=0.0):
    if revenue is None: return {"contribution_margin":None,"status":"HOLD_NO_REVENUE_EVIDENCE"}
    costs=[variable_cost,time_cost,rework_cost]
    if any(c is None for c in costs): return {"contribution_margin":None,"status":"HOLD_MISSING_COST"}
    return {"contribution_margin":float(revenue)-sum(float(c) for c in costs),"status":"COMPUTABLE_INPUTS_PRESENT"}

def queue_state(arrival_rate, service_rate, wip=None):
    if arrival_rate is None or service_rate in (None,0): return {"status":"UNKNOWN"}
    util=arrival_rate/service_rate
    status="OVERLOAD" if util>=1 else ("HIGH_UTILIZATION" if util>=0.8 else "BOUNDED")
    return {"utilization":util,"status":status,"wip":wip}
