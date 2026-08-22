from __future__ import annotations
import hashlib
import json
from typing import Any, Dict, Iterable, List, Optional

PUBLIC_EVIDENCE_MAX = "E2+"
PA_LEVELS = {"PA0":0,"PA1":1,"PA2":2,"PA3":3,"PA4":4,"PA5":5}
REQUIRED_SUPPLIER_FIELDS = (
    "insurance","tax_clearance","turnover","references","staff",
    "safety","certifications","capacity","geography"
)

def canonical_hash(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def pack_acquisition_status(*, authenticated_or_user_pack: bool, attachment_inventory_complete: bool,
                            revision_inventory_complete: bool, authoritative_source: bool) -> Dict[str, Any]:
    if not authoritative_source:
        return {"status":"BLOCKED_NONAUTHORITATIVE_SOURCE","pack_complete":False}
    if not authenticated_or_user_pack:
        return {"status":"BLOCKED_AUTHENTICATED_OR_USER_PACK_REQUIRED","pack_complete":False}
    if not attachment_inventory_complete:
        return {"status":"BLOCKED_ATTACHMENT_INVENTORY_INCOMPLETE","pack_complete":False}
    if not revision_inventory_complete:
        return {"status":"BLOCKED_REVISION_INVENTORY_INCOMPLETE","pack_complete":False}
    return {"status":"PASS_COMPLETE_OFFICIAL_PACK","pack_complete":True}

def supplier_profile_status(fields: Dict[str, Any], provenance: Dict[str, str]) -> Dict[str, Any]:
    missing = [k for k in REQUIRED_SUPPLIER_FIELDS if fields.get(k) in (None, "", "UNKNOWN")]
    unsourced = [k for k in REQUIRED_SUPPLIER_FIELDS if fields.get(k) not in (None, "", "UNKNOWN") and not provenance.get(k)]
    verified = not missing and not unsourced
    return {
        "status": "PASS_VERIFIED_SUPPLIER_PROFILE" if verified else "HOLD_SUPPLIER_PROFILE_INCOMPLETE",
        "verified": verified,
        "missing": missing,
        "unsourced": unsourced,
    }

def join_requirements(requirements: Iterable[Dict[str, Any]], supplier: Dict[str, Any]) -> List[Dict[str, Any]]:
    out=[]
    for req in requirements:
        key=req["field"]
        required=req.get("required", True)
        supplier_value=supplier.get(key)
        if not required:
            state="NOT_APPLICABLE"
        elif supplier_value in (None,"","UNKNOWN"):
            state="UNKNOWN"
        elif isinstance(req.get("allowed"), list) and supplier_value not in req["allowed"]:
            state="NONCURABLE"
        elif req.get("min") is not None and isinstance(supplier_value,(int,float)) and supplier_value < req["min"]:
            state="NONCURABLE"
        else:
            state="MET"
        out.append({**req,"supplier_value":supplier_value,"gap_state":state})
    return out

def route_bid_decision(*, pack_complete: bool, profile_verified: bool, joined: List[Dict[str, Any]],
                       deadline_open: bool=True) -> Dict[str, Any]:
    if not pack_complete:
        return {"decision":"HOLD","reason":"INCOMPLETE_OFFICIAL_PACK"}
    if not profile_verified:
        return {"decision":"HOLD","reason":"UNVERIFIED_SUPPLIER_PROFILE"}
    if not deadline_open:
        return {"decision":"NO_BID","reason":"DEADLINE_CLOSED"}
    states=[r["gap_state"] for r in joined]
    if "NONCURABLE" in states:
        return {"decision":"NO_BID","reason":"NONCURABLE_REQUIREMENT_GAP"}
    if "UNKNOWN" in states:
        return {"decision":"HOLD","reason":"UNKNOWN_REQUIREMENT_GAP"}
    return {"decision":"BID_CANDIDATE","reason":"ALL_VERIFIED_REQUIREMENTS_MET"}

def critical_path_clock(deadlines: Dict[str, Optional[str]]) -> Dict[str, Any]:
    ordered=[]
    for name, ts in deadlines.items():
        if ts:
            ordered.append((name, ts))
    ordered.sort(key=lambda x:x[1])
    return {"ordered":ordered,"missing":[k for k,v in deadlines.items() if not v]}

def null_safe_finance_object(**kwargs) -> Dict[str, Any]:
    keys=("estimated_value_eur","payment_days","retention_pct","bond_pct","insurance_required","working_capital_need_eur")
    return {k:kwargs.get(k) for k in keys}

def reference_matrix(required_categories: Iterable[str], supplier_refs: Iterable[Dict[str,Any]]) -> Dict[str,Any]:
    req=list(required_categories)
    refs=list(supplier_refs)
    coverage={}
    for cat in req:
        matches=[r for r in refs if cat in r.get("categories",[])]
        coverage[cat]=[r.get("id") for r in matches]
    return {"coverage":coverage,"complete":all(bool(v) for v in coverage.values()) if coverage else False}

def public_artifact_hash(packet_hash: str, schema_version: str, outputs: Dict[str,Any]) -> str:
    return canonical_hash({"packet_hash":packet_hash,"schema_version":schema_version,"outputs":outputs})

def blind_pa4_gate(*, same_packet_hash: bool, reviewer_independent: bool, reviewer_blinded: bool,
                   first_decision_hidden: bool) -> Dict[str,Any]:
    checks=[same_packet_hash,reviewer_independent,reviewer_blinded,first_decision_hidden]
    return {"status":"PASS_PA4_REVIEW_READY" if all(checks) else "HOLD_PA4_PROTOCOL_INCOMPLETE","ready":all(checks)}

def pa4_compare(first: Dict[str,Any], second: Dict[str,Any]) -> Dict[str,Any]:
    return {
        "decision_same": first.get("decision")==second.get("decision"),
        "fatal_gap_symmetric_diff": sorted(set(first.get("fatal_gaps",[])) ^ set(second.get("fatal_gaps",[]))),
        "missed_criteria": sorted(set(first.get("criteria",[])) - set(second.get("criteria",[]))),
        "extra_criteria": sorted(set(second.get("criteria",[])) - set(first.get("criteria",[]))),
    }

def decision_delta(before: Optional[str], after: Optional[str], real_target_user: bool) -> Dict[str,Any]:
    if not real_target_user:
        return {"status":"HOLD_REAL_TARGET_USER_REQUIRED","changed":None}
    return {"status":"OBSERVED","changed":before != after,"before":before,"after":after}

def observed_metric(value: Any, source_type: str) -> Dict[str,Any]:
    if source_type not in {"REAL_HUMAN_TIMING","REAL_ERROR_LOG","REAL_TRANSACTION"}:
        return {"status":"HOLD_REAL_OBSERVATION_REQUIRED","value":None}
    return {"status":"OBSERVED","value":value}

def substitute_residual_job(job_parts: Iterable[str], free_or_native_coverage: Iterable[str]) -> Dict[str,Any]:
    job=set(job_parts); covered=set(free_or_native_coverage)
    residual=sorted(job-covered)
    if not residual:
        return {"status":"HOLD_NO_PAID_RESIDUAL_JOB","residual":[]}
    return {"status":"RESIDUAL_JOB_EXISTS","residual":residual}

def field_half_life(fields: Dict[str,Any], ttl_hours: Dict[str,int]) -> Dict[str,Any]:
    return {k:{"value":v,"ttl_hours":ttl_hours.get(k),"revalidate_required":ttl_hours.get(k) is None}
            for k,v in fields.items()}

def stale_status_contradiction(*, deadline_passed: bool, portal_status: str) -> Dict[str,Any]:
    if deadline_passed and portal_status.upper()=="OPEN":
        return {"status":"REVALIDATE","reason":"DEADLINE_STATUS_CONTRADICTION"}
    return {"status":"PASS"}

def refresh_preserve_history(history: List[Dict[str,Any]], snapshot: Dict[str,Any]) -> List[Dict[str,Any]]:
    new=list(history)
    h=canonical_hash(snapshot)
    if not new or new[-1].get("snapshot_hash") != h:
        new.append({"snapshot_hash":h,"snapshot":snapshot})
    return new

def wip_guard(primary: Optional[str], pilots: Iterable[str]) -> Dict[str,Any]:
    active=([primary] if primary else []) + list(pilots)
    violations=[]
    if len(active)>3: violations.append("WIP_LIMIT_EXCEEDED")
    if len(set(active))!=len(active): violations.append("DUPLICATE_WIP")
    return {"status":"PASS" if not violations else "FAIL","violations":violations,"active":active}

def pareto_vector(*, decision_utility: str, evidence_accessibility: str, kill_power: str) -> Dict[str,str]:
    return {"decision_utility":decision_utility,"evidence_accessibility":evidence_accessibility,"kill_power":kill_power}

def self_improvement_candidate(*, defect: str, cases: int, repair: str, evidence_hashes: Iterable[str]) -> Dict[str,Any]:
    hashes=sorted(set(evidence_hashes))
    if cases < 2:
        return {"status":"DISCOVERY_ONLY","authority":"NONE","auto_promote":False}
    if not defect or not repair or not hashes:
        return {"status":"HOLD_INCOMPLETE_CANDIDATE","authority":"NONE","auto_promote":False}
    row={"status":"CANDIDATE","defect":defect,"cases":cases,"repair":repair,"evidence_hashes":hashes,
         "authority":"CANDIDATE_ONLY","auto_promote":False}
    row["candidate_hash"]=canonical_hash(row)
    return row

def pa5_object(*, real_user_class: Optional[str], before_decision: Optional[str], after_decision: Optional[str],
               interaction_artifact_hash: Optional[str], observed_at: Optional[str]) -> Dict[str,Any]:
    complete=all([real_user_class,before_decision,after_decision,interaction_artifact_hash,observed_at])
    return {"status":"PA5_OBSERVED" if complete else "HOLD_REAL_USE_EVIDENCE_REQUIRED",
            "pa_grade":"PA5" if complete else "PA4_OR_LOWER",
            "fields":{"user_class":real_user_class,"before":before_decision,"after":after_decision,
                      "interaction_artifact_hash":interaction_artifact_hash,"observed_at":observed_at}}

def e3_object(*, source_type: Optional[str], behavioral_cost_or_commitment: Any, artifact_hash: Optional[str]) -> Dict[str,Any]:
    real=source_type=="REAL_EXTERNAL_BEHAVIOR" and behavioral_cost_or_commitment not in (None,"",False) and bool(artifact_hash)
    return {"status":"E3_OBSERVED" if real else "HOLD_REAL_EXTERNAL_BEHAVIOR_REQUIRED","evidence_grade":"E3" if real else PUBLIC_EVIDENCE_MAX}

def e4_object(*, source_type: Optional[str], amount_eur: Any, transaction_id: Optional[str], artifact_hash: Optional[str]) -> Dict[str,Any]:
    try: positive=float(amount_eur)>0
    except Exception: positive=False
    real=source_type=="REAL_TRANSACTION" and positive and bool(transaction_id) and bool(artifact_hash)
    return {"status":"E4_OBSERVED" if real else "HOLD_REAL_TRANSACTION_REQUIRED","evidence_grade":"E4" if real else "E3_OR_LOWER"}

def cycle_close_gate(*, core_merged: bool, cross_lane_merged: bool, drive_readback: bool,
                     current_authority_reconciled: bool) -> Dict[str,Any]:
    ok=all([core_merged,cross_lane_merged,drive_readback,current_authority_reconciled])
    return {"status":"PASS_CYCLE6_CLOSED" if ok else "HOLD_CYCLE6_CLOSURE","closed":ok}
