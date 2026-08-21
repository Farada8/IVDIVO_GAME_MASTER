"""Seal a real-listener session declaration before playback."""
from __future__ import annotations
import json, hashlib, copy

def h(obj): return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def seal(session:dict)->dict:
    required=('listener_id','protocol_sha256','artifact_set_sha256','device','one_listen_rule')
    missing=[k for k in required if session.get(k) in (None,'')]
    if missing: return {'status':'FAIL_PREDECLARATION','missing':missing}
    x=copy.deepcopy(session); x['answers_present']=False; x['played']=False; x['session_sha256']=h(x); x['status']='SEALED_BEFORE_PLAYBACK'; return x
