"""Aggregate human/device evidence without hiding individual failures."""
from __future__ import annotations

def aggregate(rows:list[dict])->dict:
    if not rows: return {'status':'NO_REAL_DATA','listeners':0,'devices':{}}
    devices={}; listeners=set(); failures=[]
    for r in rows:
        listeners.add(r.get('listener_id'))
        d=r.get('device','UNKNOWN'); devices.setdefault(d,{'trials':0,'correct':0,'realism_sum':0.0,'realism_n':0})
        a=devices[d]; a['trials']+=1; a['correct']+=1 if r.get('correct') is True else 0
        if isinstance(r.get('realism'),(int,float)): a['realism_sum']+=float(r['realism']); a['realism_n']+=1
        if r.get('correct') is not True: failures.append({'listener_id':r.get('listener_id'),'device':d,'trial':r.get('trial')})
    for d,a in devices.items():
        a['accuracy']=a['correct']/a['trials'] if a['trials'] else None
        a['mean_realism']=a['realism_sum']/a['realism_n'] if a['realism_n'] else None
    return {'status':'AGGREGATED','listeners':len([x for x in listeners if x]),'devices':devices,'individual_failures':failures}
