from __future__ import annotations
from typing import Any, Dict, Iterable

REQUIRED_FIELDS=("title","context","timeframe","overall_budget","photo_refs","applicant_role")

def classify_project_record(record:Dict[str,Any])->Dict[str,Any]:
    missing=[]
    for key in REQUIRED_FIELDS:
        value=record.get(key)
        if value is None or value=="" or value==[] or value=="UNKNOWN":
            missing.append(key)
    delivery_context=bool(record.get("relevant_delivery_context_proven"))
    if not delivery_context:
        missing.append("relevant_delivery_context_proven")
    ready=not missing
    if ready:
        cls="CLASS_A_SUBMISSION_READY"
    elif record.get("title") and record.get("photo_refs") and record.get("context"):
        cls="CLASS_B_DOCUMENTED_WORK_INCOMPLETE_PROJECT_FIELDS"
    else:
        cls="CLASS_C_PARTIAL_WORK_RECORD"
    return {"status":"PASS_SUBMISSION_READY" if ready else "HOLD_INCOMPLETE_PROJECT_RECORD","class":cls,"submission_ready":ready,"missing":sorted(set(missing))}

def three_project_gate(records:Iterable[Dict[str,Any]])->Dict[str,Any]:
    rows=[classify_project_record(r) for r in records]
    ready=sum(1 for r in rows if r["submission_ready"])
    return {"status":"PASS_THREE_PROJECT_EVIDENCE" if ready>=3 else "HOLD_THREE_PROJECT_EVIDENCE","submission_ready_count":ready,"required":3,"records":rows}

def bind_image_to_work(*,visual_match_only:bool,documentary_binding:bool)->str:
    if documentary_binding:
        return "BOUND"
    if visual_match_only:
        return "HOLD_VISUAL_MATCH_ONLY"
    return "UNBOUND"

def normalize_budget(value:Any,authoritative_not_applicable:bool=False)->Any:
    if authoritative_not_applicable:
        return "NOT_APPLICABLE_AUTHORITY_BOUND"
    if value in (None,"","UNKNOWN"):
        return None
    return value

def archive_loss_effect(*,archive_loss_documented:bool,missing_project_field:Any)->Any:
    if archive_loss_documented and missing_project_field in (None,"","UNKNOWN"):
        return None
    return missing_project_field
