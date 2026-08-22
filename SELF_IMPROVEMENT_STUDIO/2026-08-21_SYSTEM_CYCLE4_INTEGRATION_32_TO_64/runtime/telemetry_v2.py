from __future__ import annotations
import time,uuid
REQUIRED=("project_id","domain","kind","decision","evidence_class")
def make_event(**kw):
    missing=[k for k in REQUIRED if k not in kw]
    if missing:raise ValueError("MISSING:"+",".join(missing))
    e={"event_id":str(uuid.uuid4()),"ts":kw.pop("ts",time.time()),**kw}
    for k in ("human_minutes","provider_spend","token_count","accepted_minutes","generated_minutes","rework_cycles"):e.setdefault(k,None)
    return e
def validate_event(e):
    missing=[k for k in REQUIRED if not e.get(k)]
    if missing:return {"status":"FAIL","missing":missing}
    if e.get("evidence_class") in {"MACHINE","DRY_RUN","PERSISTED_STATE"} and e.get("human_signal") is True:return {"status":"FAIL","reason":"EVIDENCE_CLASS_INFLATION"}
    return {"status":"PASS"}
def aggregate(events):
    real_spend=[e["provider_spend"] for e in events if e.get("provider_spend") is not None];human=[e["human_minutes"] for e in events if e.get("human_minutes") is not None]
    return {"event_count":len(events),"provider_spend_sum":sum(real_spend) if real_spend else None,"human_minutes_sum":sum(human) if human else None,"unknown_provider_spend":sum(e.get("provider_spend") is None for e in events),"unknown_human_minutes":sum(e.get("human_minutes") is None for e in events)}
