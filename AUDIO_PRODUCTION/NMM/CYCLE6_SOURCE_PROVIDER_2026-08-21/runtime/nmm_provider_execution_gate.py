from __future__ import annotations
import hashlib, json

SPOILER_RISK_TERMS={"villain","killer","sinister","menacing","guilty","secret-guilt","evil"}

def _h(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def resolve_provider(snapshot: dict|None) -> dict:
    if not snapshot or snapshot.get("verified") is not True:
        return {"status":"HOLD_EXTERNAL","reason":"AUTHENTICATED_PROVIDER_SNAPSHOT_REQUIRED","model_id":None,"output_format":None}
    if snapshot.get("fresh") is not True:
        return {"status":"HOLD_EXTERNAL","reason":"SNAPSHOT_STALE","model_id":None,"output_format":None}
    if not snapshot.get("model_id") or not snapshot.get("output_format"):
        return {"status":"FAIL_CLOSED","reason":"AMBIGUOUS_PROVIDER_CAPABILITY"}
    return {"status":"PASS","model_id":snapshot["model_id"],"output_format":snapshot["output_format"],"snapshot_hash":snapshot.get("snapshot_hash")}

def compile_candidates(*, role:str, inventory:list[dict]|None, inventory_hash:str|None, max_candidates:int=5) -> dict:
    if not inventory_hash or not inventory:
        return {"status":"HOLD_EXTERNAL","reason":"VERIFIED_INVENTORY_REQUIRED","role":role,"candidates":[],"candidate_set_hash":None}
    accepted=[]; rejected=[]
    for row in inventory:
        if len(accepted)>=max_candidates: break
        labels={str(x).lower() for x in row.get("labels",[])}
        if role=="VIVIAN_CROSS" and labels & SPOILER_RISK_TERMS:
            rejected.append({"voice_id":row.get("voice_id"),"reason":"SPOILER_NEUTRALITY_RISK"}); continue
        if not row.get("voice_id"):
            rejected.append({"voice_id":None,"reason":"MISSING_VOICE_ID"}); continue
        accepted.append({"voice_id":row["voice_id"],"provider_name":row.get("provider_name"),"labels":sorted(labels)})
    payload={"role":role,"inventory_hash":inventory_hash,"candidates":accepted}
    return {"status":"PASS" if accepted else "HOLD_EXTERNAL","role":role,"candidates":accepted,"rejected":rejected,"candidate_set_hash":_h(payload) if accepted else None,"voice_lock":False}

def freeze_s0_manifest(*, source_binding:dict, provider:dict, candidate_set:dict, settings:dict) -> dict:
    base={"source_binding":source_binding,"settings":settings,"provider_model_id":provider.get("model_id"),"output_format":provider.get("output_format"),"candidate_set_hash":candidate_set.get("candidate_set_hash")}
    complete=source_binding.get("status")=="PASS" and provider.get("status")=="PASS" and candidate_set.get("status")=="PASS"
    return {**base,"status":"FROZEN_READY" if complete else "FROZEN_SOURCE_ONLY_HOLD","manifest_hash":_h(base),"paid_dispatch_allowed":False,"voice_lock":False}

def zero_paid_plan(manifests:list[dict], price_evidence:dict|None=None) -> dict:
    jobs=len(manifests); estimated=None
    if price_evidence and price_evidence.get("verified") is True and price_evidence.get("per_job") is not None:
        estimated=round(jobs*float(price_evidence["per_job"]),6)
    return {"status":"PLAN_READY","jobs":jobs,"estimated_cost":estimated,"currency":price_evidence.get("currency") if price_evidence else None,"paid_boundary":"EXPLICIT_FOUNDER_OR_AUTHORIZED_DISPATCH_GATE","auto_dispatch":False}

def dispatch_gate(*, provider:dict, manifests:list[dict], explicit_authorization:bool=False) -> dict:
    if provider.get("status")!="PASS": return {"status":"HOLD_EXTERNAL","reason":"PROVIDER_NOT_VERIFIED"}
    if any(m.get("status")!="FROZEN_READY" for m in manifests): return {"status":"HOLD_EXTERNAL","reason":"MANIFEST_NOT_READY"}
    if not explicit_authorization: return {"status":"HOLD_AUTHORIZATION","reason":"EXPLICIT_PAID_BOUNDARY_REQUIRED"}
    return {"status":"GO_ONE_BOUNDED_CANARY","auto_batch":False}

def red_team(payload:dict) -> dict:
    text=json.dumps(payload,ensure_ascii=False).lower()
    secret_tokens=["api_key","apikey","authorization: bearer","elevenlabs_api_key"]
    leaks=[x for x in secret_tokens if x in text]
    stale=payload.get("snapshot_fresh") is False
    substitution=payload.get("auto_substitution") is True
    return {"status":"FAIL" if leaks or stale or substitution else "PASS","secret_leakage":leaks,"stale_snapshot":stale,"auto_substitution":substitution}
