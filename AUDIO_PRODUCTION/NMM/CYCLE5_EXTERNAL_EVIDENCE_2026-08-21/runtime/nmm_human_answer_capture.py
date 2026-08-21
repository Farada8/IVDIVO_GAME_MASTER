"""Immutable answer capture. Scoring is deliberately separate."""
from __future__ import annotations
import json, hashlib, copy

def _h(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def capture(sealed_session:dict, answers:list[dict])->dict:
    if sealed_session.get('status')!='SEALED_BEFORE_PLAYBACK': return {'status':'FAIL_SESSION_NOT_SEALED'}
    if not answers: return {'status':'HOLD_NO_REAL_ANSWERS'}
    payload={'session_sha256':sealed_session['session_sha256'],'answers':copy.deepcopy(answers)}
    payload['raw_response_sha256']=_h(payload); payload['status']='RAW_ANSWERS_FROZEN'; return payload
