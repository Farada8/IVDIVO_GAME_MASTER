#!/usr/bin/env python3
from __future__ import annotations
from typing import Any, Iterable

K_GRADES={"K0","K1","K2","K3","K4","K5"}
E_GRADES={"E0","E1","E2","E2+","E3","E4","E5","E6","E7"}

class GateError(ValueError): pass

def decision_relevance(obj: dict[str,Any]) -> bool:
    return bool(obj.get("decision") and obj["decision"].get("can_change"))

def k_e_firewall(knowledge_grade:str, market_grade:str)->bool:
    if knowledge_grade not in K_GRADES or market_grade not in E_GRADES:
        raise GateError("unknown grade")
    return True

def mechanism_confidence(source_count:int, direct:bool=True, dissent:bool=False, reproduced:bool=False)->str:
    if reproduced: return "K5"
    if direct and source_count>=2 and not dissent: return "K4"
    if direct and source_count>=1: return "K3" if source_count>=2 else "K2"
    return "K1" if source_count else "K0"

def compile_contradiction(mechanism_a:str, mechanism_b:str, route_rule:str)->dict[str,Any]:
    if not route_rule: raise GateError("route rule required")
    return {"a":mechanism_a,"b":mechanism_b,"route_rule":route_rule,"averaged":False}

def mom_test_evidence(statement:str, past_behavior:bool=False, commitment:bool=False, money_or_time:bool=False)->dict[str,Any]:
    s=statement.lower()
    compliment=any(x in s for x in ["love it","great idea","cool","would definitely","sounds good"])
    hypothetical=any(x in s for x in ["would buy","would use","might buy","could use"])
    strength=0
    if past_behavior: strength+=2
    if commitment: strength+=2
    if money_or_time: strength+=2
    if compliment: strength-=1
    if hypothetical: strength-=1
    return {"compliment":compliment,"hypothetical":hypothetical,"strength":max(0,strength),
            "demand_proof": bool((past_behavior and commitment) or money_or_time)}

def negative_evidence_gate(fatal_flags:Iterable[str])->dict[str,Any]:
    flags=[x for x in fatal_flags if x]
    return {"verdict":"KILL_OR_HOLD" if flags else "CONTINUE","fatal_flags":flags}

def vanity_metric_gate(metric_name:str, linked_decision:bool, causal_to_value:bool)->str:
    return "PASS" if linked_decision and causal_to_value else "FAIL_VANITY"

def value_of_information(priority_items:list[dict[str,Any]])->list[dict[str,Any]]:
    out=[]
    for x in priority_items:
        value=float(x.get("decision_value",0))*float(x.get("uncertainty",0))*float(x.get("flip_probability",0))
        cost=max(1e-9,float(x.get("cost",0))+float(x.get("latency_cost",0)))
        out.append({**x,"voi_ratio":value/cost})
    return sorted(out,key=lambda z:z["voi_ratio"],reverse=True)

def wip_select(items:list[dict[str,Any]],limit:int=3)->list[dict[str,Any]]:
    if limit<1: raise GateError("limit must be >=1")
    return value_of_information(items)[:limit]

def policy_resistance_scan(change:dict[str,Any])->dict[str,Any]:
    required=["intended_effect","guardrails","delays","compensating_responses"]
    missing=[k for k in required if k not in change]
    return {"verdict":"PASS" if not missing else "HOLD","missing":missing}

def double_loop_needed(local_repairs:int, recurrence:bool, model_contradiction:bool, guardrail_regression:bool)->bool:
    return bool((local_repairs>=2 and recurrence) or model_contradiction or guardrail_regression)

ROUTES=("CREATE","BROKER","ACQUIRE")
def route_vectors(route_data:dict[str,dict[str,float]])->dict[str,Any]:
    for r in ROUTES:
        if r not in route_data: raise GateError(f"missing route {r}")
    dims=list(next(iter(route_data.values())).keys())
    dominates={}
    for a in ROUTES:
        dom=[]
        for b in ROUTES:
            if a==b: continue
            def better_or_equal(d):
                if d in {"control","upside","strategic_fit"}: return route_data[a][d]>=route_data[b][d]
                return route_data[a][d]<=route_data[b][d]
            def strictly_better(d):
                if d in {"control","upside","strategic_fit"}: return route_data[a][d]>route_data[b][d]
                return route_data[a][d]<route_data[b][d]
            if all(better_or_equal(d) for d in dims) and any(strictly_better(d) for d in dims):
                dom.append(b)
        dominates[a]=dom
    return {"vectors":route_data,"pareto_dominance":dominates,"magic_total_score":None}

def missing_data_gate(obj:dict[str,Any],required_fields:list[str])->dict[str,Any]:
    missing=[k for k in required_fields if obj.get(k) is None]
    return {"verdict":"HOLD" if missing else "PASS","missing":missing}

def opportunity_ceiling(public_only:bool, buyer_contact:bool=False, paid_signal:bool=False)->str:
    if paid_signal or buyer_contact: return "E3_OR_HIGHER_REQUIRES_SPECIFIC_EVIDENCE"
    return "E2+" if public_only else "E0"

def hype_firewall(independent_outcomes:int, ai_agreements:int)->str:
    return "PASS_INDEPENDENT" if independent_outcomes>0 else ("HOLD_AI_ONLY" if ai_agreements>0 else "NO_EVIDENCE")

def build_hypothesis(problem:str, buyer:str, mechanism:str, falsifier:str, unknowns:list[str])->dict[str,Any]:
    if not all([problem,buyer,mechanism,falsifier]): raise GateError("incomplete hypothesis")
    return {"problem":problem,"buyer":buyer,"mechanism":mechanism,"falsifier":falsifier,"unknowns":unknowns}

def validate_canary(canary:dict[str,Any])->dict[str,Any]:
    missing=[]
    for k in ["bounded_scope","reversible","primary_metric","guardrails","rollback_trigger","rollback_target"]:
        if not canary.get(k): missing.append(k)
    return {"verdict":"PASS" if not missing else "FAIL_CLOSED","missing":missing}
