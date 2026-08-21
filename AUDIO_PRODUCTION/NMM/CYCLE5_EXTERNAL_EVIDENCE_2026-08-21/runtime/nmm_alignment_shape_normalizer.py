"""Normalize accepted alignment sidecars; quarantine malformed or ambiguous shapes."""
from __future__ import annotations

def normalize(sidecar:dict)->dict:
    words=sidecar.get('words')
    if not isinstance(words,list) or not words:
        return {'status':'QUARANTINE','reason':'WORDS_MISSING_OR_EMPTY'}
    out=[]; last=-1.0
    for i,row in enumerate(words):
        if not isinstance(row,dict): return {'status':'QUARANTINE','reason':'ROW_NOT_OBJECT','index':i}
        if row.get('text') in (None,'') or not isinstance(row.get('start'),(int,float)) or not isinstance(row.get('end'),(int,float)):
            return {'status':'QUARANTINE','reason':'ROW_SHAPE','index':i}
        if row['start']<0 or row['end']<row['start'] or row['start']<last:
            return {'status':'QUARANTINE','reason':'NON_MONOTONIC','index':i}
        out.append({'text':str(row['text']),'start_s':float(row['start']),'end_s':float(row['end'])}); last=float(row['end'])
    return {'status':'NORMALIZED','words':out,'sample_lock':False}
