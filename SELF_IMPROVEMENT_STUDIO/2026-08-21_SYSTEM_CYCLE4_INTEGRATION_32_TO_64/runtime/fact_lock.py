from __future__ import annotations
import hashlib, json

def canon(obj): return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))
def h(obj): return hashlib.sha256(canon(obj).encode()).hexdigest()

def create_fact(fact_id,value,grade,source_ref,consumers,allowed_transforms=None):
    if not fact_id or not source_ref: raise ValueError("FACT_ID_AND_SOURCE_REQUIRED")
    if grade not in {"SOURCE_EXPLICIT","CONTINUITY_REQUIRED","DERIVED_INFERENCE","DESIGN_CHOICE","UNSUPPORTED"}: raise ValueError("BAD_GRADE")
    f={"fact_id":fact_id,"value":value,"grade":grade,"source_ref":source_ref,"consumers":sorted(set(consumers)),"allowed_transforms":sorted(set(allowed_transforms or [])),"version":1}
    f["fact_hash"]=h(f); return f

def consume(fact,consumer_id,proposed_value,expected_hash,transform=None):
    if expected_hash!=fact.get("fact_hash"): return {"decision":"STOP","reason":"STALE_FACT_TOKEN"}
    if consumer_id not in fact.get("consumers",[]): return {"decision":"STOP","reason":"UNAUTHORIZED_CONSUMER"}
    if proposed_value==fact.get("value"): return {"decision":"PASS","reason":"EXACT"}
    if transform and transform in fact.get("allowed_transforms",[]): return {"decision":"REVIEW","reason":"ALLOWED_TRANSFORM_REQUIRES_SEMANTIC_CHECK"}
    return {"decision":"STOP","reason":"SEMANTIC_DRIFT"}

def mutate(fact,new_value,expected_hash):
    if expected_hash!=fact.get("fact_hash"): return {"status":"STALE_REJECTED","fact":fact}
    n=dict(fact); n["value"]=new_value; n["version"]=fact.get("version",1)+1; n.pop("fact_hash",None); n["fact_hash"]=h(n)
    return {"status":"READY","fact":n}
