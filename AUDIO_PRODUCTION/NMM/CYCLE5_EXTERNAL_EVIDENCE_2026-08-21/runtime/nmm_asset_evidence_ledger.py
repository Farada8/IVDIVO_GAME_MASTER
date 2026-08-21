"""Append-only accepted/rejected asset evidence ledger."""
from __future__ import annotations
import json, hashlib, copy

def _h(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def append(ledger:list[dict], record:dict)->list[dict]:
    req=('asset_id','decision','artifact_sha256','evidence_class')
    miss=[k for k in req if not record.get(k)]
    if miss: raise ValueError('MISSING:'+','.join(miss))
    if record['decision'] not in ('ACCEPT','REJECT','HOLD'): raise ValueError('BAD_DECISION')
    if record['evidence_class']=='HUMAN' and not record.get('raw_response_sha256'): raise ValueError('HUMAN_RESPONSE_HASH_REQUIRED')
    out=copy.deepcopy(ledger); prev=out[-1]['record_sha256'] if out else None
    x=copy.deepcopy(record); x['previous_record_sha256']=prev; x['record_sha256']=_h(x); out.append(x); return out
