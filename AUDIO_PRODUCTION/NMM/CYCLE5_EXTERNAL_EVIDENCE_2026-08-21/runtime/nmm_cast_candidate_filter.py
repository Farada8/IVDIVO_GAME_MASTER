"""Deterministic metadata-only cast filtering before any paid audio."""
from __future__ import annotations
FORBIDDEN={'villain','guilty','killer','murderer','evil','spoiler'}

def filter_candidates(rows:list[dict], *, max_candidates:int=5, role:str='UNKNOWN')->dict:
    accepted=[]; rejected=[]
    for row in rows:
        reasons=[]
        if not row.get('voice_id'): reasons.append('MISSING_VOICE_ID')
        if not row.get('name'): reasons.append('MISSING_NAME')
        labels=' '.join(str(x) for x in [row.get('name',''),row.get('description',''),row.get('labels','')]).lower()
        if role.upper()=='VIVIAN' and any(t in labels for t in FORBIDDEN): reasons.append('SPOILER_NEUTRALITY_RISK')
        if reasons: rejected.append({'voice_id':row.get('voice_id'),'reasons':reasons})
        else: accepted.append(row)
    accepted=accepted[:max_candidates]
    return {'accepted':accepted,'rejected':rejected,'cap':max_candidates,'paid_audio_calls':0}
