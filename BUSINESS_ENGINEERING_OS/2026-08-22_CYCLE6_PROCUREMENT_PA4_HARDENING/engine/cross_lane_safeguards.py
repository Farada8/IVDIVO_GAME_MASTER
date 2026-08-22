from __future__ import annotations
from typing import Any

PUBLIC_EVIDENCE_CEILING="E2+"
WIP_LIMIT=3

def decision_delta(before: Any, after: Any)->dict:
    if before is None or after is None:
        return {"delta":None,"status":"HOLD_UNOBSERVED_DECISION"}
    if before == after:
        return {"delta":False,"status":"ZERO_DELTA_HOLD"}
    return {"delta":True,"status":"DECISION_CHANGED_OBSERVED_ONLY_IF_REAL_USER"}

def time_saved_null_safe(baseline_minutes: float|None, after_minutes: float|None, *, measured: bool=False, sourced: bool=False)->dict:
    if baseline_minutes is None or after_minutes is None or not (measured or sourced):
        return {"minutes_saved":None,"status":"HOLD_NO_MEASURED_OR_SOURCED_TIME"}
    return {"minutes_saved":baseline_minutes-after_minutes,"status":"MEASURED" if measured else "SOURCED"}

def error_avoidance(observed_errors_before: int|None, observed_errors_after: int|None, cost_per_error: float|None=None)->dict:
    if observed_errors_before is None or observed_errors_after is None:
        return {"errors_avoided":None,"monetized_value":None,"status":"HOLD_UNOBSERVED_ERRORS"}
    avoided=observed_errors_before-observed_errors_after
    value=None if cost_per_error is None else avoided*cost_per_error
    return {"errors_avoided":avoided,"monetized_value":value,"status":"OBSERVED_ERRORS_VALUE_OPTIONAL"}

def artifact_rubric(**axes)->dict:
    allowed=("completeness","freshness","null_safety","decision_delta","falsifiability","next_action_clarity")
    vector={k:axes.get(k) for k in allowed}
    return {"axes":vector,"total_score":None,"status":"VECTOR_ONLY_NO_OPAQUE_TOTAL"}

def completeness_gate(required: list[str], payload: dict)->dict:
    missing=[k for k in required if payload.get(k) in (None,"",[])]
    return {"pass":not missing,"missing":missing,"status":"PASS" if not missing else "FAIL_CLOSED_MISSING_INPUT"}

def field_revalidation(field_class:str)->dict:
    days={"PROCUREMENT_DEADLINE":1,"PROCUREMENT_STATUS":1,"REGISTRY_STATUS":7,"GRANT_RULE":14,"POLICY":30,"EVERGREEN_METHOD":90}.get(field_class,30)
    return {"field_class":field_class,"revalidate_days":days}

def substitution_matrix(alternatives:list[dict], proposed_jobs:set[str])->dict:
    covered=set()
    for a in alternatives:
        if a.get("available") and a.get("price_type") in {"FREE","PUBLIC","SUBSIDISED","VENDOR_INCLUDED","INTERNAL"}:
            covered.update(a.get("jobs",[]))
    residual=sorted(proposed_jobs-covered)
    return {"covered":sorted(covered),"residual_unsolved_job":residual,"status":"DIFFERENTIATION_REQUIRED" if not residual else "RESIDUAL_JOB_EXISTS"}

def false_confidence_guard(*, polished:bool, proof_grade:str, unknown_fields:list[str])->dict:
    return {"proof_grade":proof_grade,"polished":polished,"unknown_fields":list(unknown_fields),"proof_upgrade_from_polish":False}

def wip_gate(primary:str|None,pilots:list[str])->dict:
    count=(1 if primary else 0)+len(pilots)
    return {"count":count,"limit":WIP_LIMIT,"status":"PASS" if count<=WIP_LIMIT else "FREEZE_EXCESS"}

def pareto_front(candidates:list[dict])->list[str]:
    dims=("decision_utility","evidence_accessibility","kill_power")
    front=[]
    for a in candidates:
        dominated=False
        for b in candidates:
            if a is b: continue
            ge=all(float(b.get(d,0))>=float(a.get(d,0)) for d in dims)
            gt=any(float(b.get(d,0))>float(a.get(d,0)) for d in dims)
            if ge and gt:
                dominated=True; break
        if not dominated: front.append(a["id"])
    return sorted(front)

def self_improvement_candidate(failures:list[dict])->dict:
    cases={}
    for f in failures:
        cases.setdefault(f["defect"],set()).add(f.get("case_id"))
    promoted=sorted([d for d,c in cases.items() if len({x for x in c if x is not None})>=2])
    return {"candidates":promoted,"single_failures_remain_observations":True}

def invariants(lanes:list[dict])->dict:
    violations=[]
    for x in lanes:
        if x.get("public_only") and x.get("market_grade") not in (None,"E0","E1","E2","E2+"):
            violations.append((x.get("id"),"PUBLIC_TO_MARKET_LEAK"))
        if x.get("price") is not None and not x.get("external_price_signal"):
            violations.append((x.get("id"),"UNSOURCED_PRICE"))
        if x.get("proof_upgraded_by_polish"):
            violations.append((x.get("id"),"POLISH_PROOF_LEAK"))
    return {"pass":not violations,"violations":violations}

def pa4_gate(*, same_source_packet:bool, independent_reviewer:bool, blinded_to_first_output:bool)->str:
    return "PA4_ELIGIBLE_REVIEW" if same_source_packet and independent_reviewer and blinded_to_first_output else "HOLD_NOT_INDEPENDENT_PA4"

def smallest_safe_decision_use_tests()->dict:
    return {
      "PROCUREMENT":{"artifact":"TenderQualificationObject","user":"real supplier/bid manager","action":"choose FULL_REVIEW/HOLD/REJECT","external_contact_required":True},
      "RETROFIT":{"artifact":"Route Card","user":"real property owner/contractor","action":"choose next evidence/application step","external_contact_required":True},
      "SME_AI":{"artifact":"workflow card","user":"real SME workflow owner","action":"approve/reject one implementation experiment","external_contact_required":True},
    }

def pa5_e3_gate(evidence:dict)->str:
    required=("target_user_class","decision_before","decision_after","interaction_artifact","timestamp","what_changed")
    if any(not evidence.get(k) for k in required): return "HOLD_BELOW_PA5_E3"
    if evidence.get("compliment_only"): return "HOLD_COMPLIMENT_NOT_BEHAVIOR"
    return "PA5_E3_CANDIDATE_REAL_INTERACTION"

def cycle6_eligibility(lanes:list[dict])->dict:
    advanced=[x["id"] for x in lanes if int(x.get("pa_grade_num",0))>=4]
    held=[x["id"] for x in lanes if int(x.get("pa_grade_num",0))<4]
    return {"advance":advanced,"hold":held,"status":"ADVANCE_SCOPED" if advanced else "HOLD_NO_PA4"}
