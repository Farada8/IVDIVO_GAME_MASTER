"""Freeze exact-text/settings manifests before provider dispatch."""
from __future__ import annotations
import json, hashlib, copy

def canonical_hash(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def _hash_payload(manifest:dict):
    x=copy.deepcopy(manifest)
    for k in ('manifest_sha256','sealed','status'): x.pop(k,None)
    return canonical_hash(x)

def freeze(payload:dict)->dict:
    required=('exact_text','role','provider','model_id','output_format','settings')
    missing=[k for k in required if payload.get(k) in (None,'',{})]
    if missing: return {'status':'HOLD_SOURCE_OR_SETTINGS_BINDING','missing':missing,'sealed':False}
    out=copy.deepcopy(payload); out['dispatch_allowed']=False
    out['manifest_sha256']=_hash_payload(out); out['sealed']=True; out['status']='SEALED_PRE_DISPATCH'
    return out

def verify(manifest:dict)->bool:
    return bool(manifest.get('sealed') and manifest.get('manifest_sha256')==_hash_payload(manifest))
